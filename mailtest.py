#!/usr/bin/env python3
from datetime import datetime

from mako.template import Template
from sqlalchemy import select

import config
from database import Database, Base
from sendmail import SMTP

if __name__=="__main__":
    db = Database(config.DB_FILENAME,config.DB_DEBUG)
    server=SMTP(config.SMTP_SERVER,config.SMTP_PORT,config.SMTP_FROM,config.SMTP_PSW)
    context={"timestamp":datetime.now().strftime("%Y.%m.%d %H:%M")}

    itinerary=Base.metadata.tables["itinerary"]
    search=Base.metadata.tables["search"]
    query=select(
        itinerary.c.search_id,
        itinerary.c.id,
        itinerary.c.cityFrom,
        itinerary.c.cityTo,
        itinerary.c.countryFromName,
        itinerary.c.countryToName,
        itinerary.c.local_departure,
        itinerary.c.local_arrival,
        itinerary.c.nightsInDest,
        itinerary.c.quality,
        itinerary.c.distance,
        itinerary.c.durationDeparture,
        itinerary.c.durationReturn,
        itinerary.c.price
    ).select_from(itinerary.join(search, itinerary.c.search_id == search.c.search_id)).where(search.c.actual == 1).order_by(itinerary.c.price).limit(20)
    context["query"] = db.session.execute(query).fetchall()

    template=Template(filename="templates/template.html").render(**context)
    server.send_mail(config.SMTP_TO,"Hello",template,["templates/down.png","templates/up.png","templates/repcsi.jpg","templates/vonal.png"])
    print("Ok")