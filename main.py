#!/usr/bin/env python3

import calendar
import os
from datetime import datetime

import logging

import config
from database import Database
from kiwi import Tequila

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    logging.basicConfig(filename="app.log",level=logging.DEBUG,format="{asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%M")
    logging.info("Start")
    kiwi = Tequila(config.APIKEY)
    db=Database(config.DB_FILENAME, config.DB_DEBUG)
    start_date = datetime.now()
    for _ in range(12):
        next_month = start_date.month % 12 + 1
        next_year = start_date.year + (start_date.month // 12)
        start_date = datetime(next_year, next_month, 1)
        end_date = datetime(next_year, next_month, calendar.monthrange(next_year, next_month)[1])
        logging.info("Search")
        result = kiwi.search("BUD,VIE", start_date, end_date, "BKK", 5, 18, max_fly_duration=17, max_stopovers=1,
                             limit=1000)
        fname=f"{config.SAVEDIR}/{datetime.now().strftime('%Y%m%d%H%M%S')}-{start_date.strftime('%Y%m')}.json"
        logging.info("Insert DB")
        db.insert_json(result,kiwi.search_url,store_json_database=False,store_json_file_path=fname)

    logging.info("Finished")
