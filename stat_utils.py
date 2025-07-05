#!/usr/bin/env python3
import datetime
import os

import jinja2

import config
from database import Database, Itinerary, Search
from sendmail import sendmail

def punctuation(value):
    return '{:,.0f}'.format(value).replace(',', '.')

def to_time(value):
    """Convert a number of seconds to a formatted time string."""
    value = int(value)
    hours, remainder = divmod(value, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}"

def generate_template(itineraries:dict[str,list])->str:
    template_dir = os.path.join(os.path.dirname(__file__), 'template')
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    env.filters['punctuation'] = punctuation
    env.filters['to_time'] = to_time
    template = env.get_template('mail.html')
    return template.render(itineraries=itineraries['itineraries'])

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
                            .filter(Itinerary.flyFrom == "BUD")
                            .order_by(Itinerary.price)
                            .limit(5).all())
    itineraries += [row.rowid for row in cheapest_itineraries_VIE]

    result = db.fill_missing_itineraries(itineraries)
    html = generate_template(result)
    subject = f"Bangkok repülővel {datetime.date.today().strftime('%Y-%m-%d')}"
    sendmail(send_to, subject, html)

if __name__ == "__main__":
    db=Database(config.DB_FILENAME,config.DB_DEBUG)
    send_stat_mail(db,config.SMTP_TO)
