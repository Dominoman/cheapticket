#!/usr/bin/env python3
import datetime
import os
from pathlib import Path

import jinja2

from config.config import config
from common.database import Database, Itinerary, Search
from common.sendmail import sendmail
from common.apininja import Ninja

def punctuation(value):
    return '{:,.0f}'.format(value).replace(',', '.')

def to_time(value):
    """Convert a number of seconds to a formatted time string."""
    value = int(value)
    hours, remainder = divmod(value, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}"

def up_n_down(value):
    if value > 0:
        return '<span style="color:red;">&#8593;</span>'
    elif value < 0:
        return '<span style="color:green;">&#8595;</span>'
    else:
        return ''

def generate_template(itineraries:dict[str,list])->str:
    template_dir = os.path.join(Path(__file__).resolve().parent.parent, 'template')
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    env.filters['punctuation'] = punctuation
    env.filters['to_time'] = to_time
    env.filters['up_n_down'] = up_n_down
    template = env.get_template('mail.html')
    return template.render(itineraries=itineraries['itineraries'])

def collect_logos(itineraries:dict[str,list])->dict[str,str]:
    """
    Collects logos for the airlines in the itineraries.

    Args:
        itineraries (dict): A dictionary containing itineraries with airline codes.

    Returns:
        dict: A dictionary mapping airline codes to their logo file paths.
    """
    ninja = Ninja(config.APININJASKEY, config.LOGOS)
    logos = {}
    for itinerary in itineraries['itineraries']:
        for direction in ['route','route_return']:
            for route in itinerary[direction]:
                airline_code = route['airline']
                if airline_code not in logos:
                    logos[airline_code] = ninja.get_logo(airline_code, cached=True)
    return logos

def send_stat_mail(db:Database,send_to:str)->None:
    cheapest_itineraries_BUD = (db.session.query(Itinerary)
                            .join(Itinerary.search)  # or .join(Search) if not using relationship
                            .filter(Search.actual == 1)
                            .filter(Itinerary.flyFrom == "BUD")
                            .order_by(Itinerary.price)
                            .limit(5).all())
    itineraries = [row.rowid for row in cheapest_itineraries_BUD]
    cheapest_itineraries_VIE = (db.session.query(Itinerary)
                            .join(Itinerary.search)  # or .join(Search) if not using relationship
                            .filter(Search.actual == 1)
                            .filter(Itinerary.flyFrom == "VIE")
                            .order_by(Itinerary.price)
                            .limit(5).all())
    itineraries += [row.rowid for row in cheapest_itineraries_VIE]

    result = db.fill_missing_itineraries(itineraries)
    logos = collect_logos(result)
    html = generate_template(result)
    subject = f"Bangkok repülővel {datetime.date.today().strftime('%Y-%m-%d')}"
    sendmail(send_to, subject, html,logos)

if __name__=="__main__":
    db = Database(config.DB_FILENAME,config.DB_DEBUG)
    send_stat_mail(db, config.SMTP_TO)
    print("Stat mail sent.")