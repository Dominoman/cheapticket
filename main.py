#!/home/laca/workspace/cheapticket/.venv/bin/python3

import calendar
from datetime import datetime

import config
from database import Database
from kiwi import Tequila

if __name__ == "__main__":
    kiwi = Tequila(config.APIKEY)
    db=Database(config.DB_FILENAME, config.DB_DEBUG)
    start_date = datetime.now()
    for _ in range(12):
        next_month = start_date.month % 12 + 1
        next_year = start_date.year + (start_date.month // 12)
        start_date = datetime(next_year, next_month, 1)
        end_date = datetime(next_year, next_month, calendar.monthrange(next_year, next_month)[1])
        result = kiwi.search("BUD,VIE", start_date, end_date, "BKK", 5, 18, max_fly_duration=17, max_stopovers=1,
                             limit=1000)
        print(kiwi.search_url)
        db.insert_json(result,kiwi.search_url)
