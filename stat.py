#!/usr/bin/env python3
import os

import jinja2

import config
from database import Database
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


if __name__ == "__main__":
    db=Database(config.DB_FILENAME,config.DB_DEBUG)
    itineraries=[2001,2102,2737]
    result=db.fill_missing_itineraries(itineraries)
    html=generate_template(result)
    sendmail("sirrobinofc@gmail.com", "Itineraries",html)
    with open("tmp\\valami.html","w", encoding="utf-8") as f:
        f.write(html)

