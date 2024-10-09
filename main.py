#!/usr/bin/env python3

import json
import logging
import os
import time
import datetime

from dateutil.relativedelta import relativedelta

import config
from database import Database, Search
from kiwi import Tequila


def savefile(json_data: dict)->None:
    fname = f"{config.SAVEDIR}/{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{range_start.strftime('%Y%m')}.json"
    with open(fname, "w") as fo:
        json.dump(json_data,fo,indent=4)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    logging.basicConfig(filename="app.log", level=logging.DEBUG, format="{asctime} - {levelname} - {message}",
                        style="{", datefmt="%Y-%m-%d %H:%M")
    logging.info("Start")
    kiwi = Tequila(config.APIKEY)
    db = Database(config.DB_FILENAME, config.DB_DEBUG)
    db.clean_actual_flag()
    range_start = datetime.datetime.now().date()
    measure_kiwi=0
    measure_db=0
    for _ in range(12):
        range_start = range_start + relativedelta(months=1, day=1)
        range_end = range_start + relativedelta(months=1, days=-1)
        max_trying = 10
        while max_trying > 0:
            max_trying -= 1
            logging.info("Search")
            time_start=time.time()
            result = kiwi.search("BUD,VIE", range_start, range_end, "BKK", 5, 18, max_fly_duration=17, max_stopovers=2,
                                 limit=1000)
            savefile(result)
            time_end=time.time()
            measure_kiwi=time_end-time_start if measure_kiwi==0 else measure_kiwi+time_end-time_start
            if kiwi.status_code == 200:
                logging.info("Insert DB")
                time_start=time.time()
                db.insert_json(result, kiwi.search_url, range_start=range_start, range_end=range_end)
                time_end=time.time()
                measure_db = time_end - time_start if measure_db == 0 else measure_db + time_end - time_start
                break

    logging.info("Clean Up")
    clean_up_start=time.time()
    today = datetime.date.today()
    result = db.get_all_search().where(Search.range_end < today).all()
    for search in result:
        if search.range_end < today:
            db.delete_search(search)
    measure_clean_up = time.time()-clean_up_start

    logging.info("Finished")
    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}Running kiwi time:{measure_kiwi}, running database time:{measure_db}, clean up time:{measure_clean_up}")
