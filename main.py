#!/usr/bin/env python3

import calendar
import json
import os
from datetime import datetime

import logging

from dateutil.relativedelta import relativedelta

import config
from database import Database
from kiwi import Tequila


def savefile(json_data: dict):
    json_text = json.dumps(json_data, indent=4)
    fname = f"{config.SAVEDIR}/{datetime.now().strftime('%Y%m%d%H%M%S')}-{range_start.strftime('%Y%m')}.json"

    with open(fname, "w") as fo:
        fo.write(json_text)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    logging.basicConfig(filename="app.log", level=logging.DEBUG, format="{asctime} - {levelname} - {message}",
                        style="{", datefmt="%Y-%m-%d %H:%M")
    logging.info("Start")
    kiwi = Tequila(config.APIKEY)
    db = Database(config.DB_FILENAME, config.DB_DEBUG)
    range_start = datetime.now().date()
    for _ in range(12):
        range_start = range_start + relativedelta(months=1, day=1)
        range_end = range_start + relativedelta(months=1, days=-1)
        i = 3
        print(range_start, range_end)
        while i > 0:
            i -= 1
            logging.info("Search")
            result = kiwi.search("BUD,VIE", range_start, range_end, "BKK", 5, 18, max_fly_duration=17, max_stopovers=1,
                                 limit=1000)
            savefile(result)
            if kiwi.status_code == 200:
                logging.info("Insert DB")
                db.insert_json(result, kiwi.search_url, range_start=range_start, range_end=range_end)
                i = 0

    logging.info("Finished")
