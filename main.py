#!/usr/bin/env python3

import json
import logging
import os
import time
import datetime

from dateutil.relativedelta import relativedelta

from config.config import config
from common.database import Database, Search
from common.kiwi import Tequila
from common.stat_utils import send_stat_mail


def savefile(json_data: dict,range_start:datetime)->None:
    if not os.path.exists(config.SAVEDIR):
        os.makedirs(config.SAVEDIR)
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
    for _ in range(13):
        range_end = range_start + relativedelta(months=1, day=1, days=-1)
        max_trying = 10
        while max_trying > 0:
            max_trying -= 1
            logging.info("Search")
            time_start=time.time()
            try:
                result = kiwi.search("BUD,VIE", range_start, range_end, "BKK", 5, 18, max_fly_duration=17, max_stopovers=2,
                                 limit=1000,hidden_city_ticketing="true")
            except Exception as ex:
                logging.exception("Kiwi Error:")
                logging.debug(f"Kiwi response: {kiwi.status_code}")
            else:
                savefile(result,range_start)
                time_end=time.time()
                measure_kiwi=time_end-time_start if measure_kiwi==0 else measure_kiwi+time_end-time_start
                if kiwi.status_code == 200:
                    logging.info("Insert DB")
                    time_start=time.time()
                    db.insert_json(result, kiwi.search_url, range_start=range_start, range_end=range_end)
                    time_end=time.time()
                    measure_db = time_end - time_start if measure_db == 0 else measure_db + time_end - time_start
                    break
        range_start = range_start + relativedelta(months=1, day=1)

    clean_up_start=time.time()
    if config.AUTO_CLEANUP:
        logging.info("Clean Up")
        today = datetime.date.today()
        result = db.get_all_search().where(Search.range_end < today).all()
        for search in result:
            db.delete_search(search)
        measure_clean_up = time.time()-clean_up_start
    logging.info(f"Running kiwi time:{measure_kiwi}, running database time:{measure_db}, clean up time:{measure_clean_up}")
    send_stat_mail(db, config.SMTP_TO)
    logging.info("Finished")