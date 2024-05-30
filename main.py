#!/usr/bin/env python
import datetime
import json
import os

import config
from database import Database
from kiwi import Tequila


def export(data: dict) -> None:
    with open(f"tmp\\{datetime.datetime.now().strftime('%Y%m%d%H%M%SBKK')}.json", "w") as fw:
        fw.write(json.dumps(data, indent=4))


if __name__ == "__main__":
    # kiwi = Tequila(config.APIKEY)
    # response = kiwi.search("BUD,VIE", datetime.datetime(2024, 6, 1), datetime.datetime(2024, 6, 30), "BKK",
    #                        nights_in_dst_from=5, nights_in_dst_to=14, max_fly_duration=20, ret_from_diff_city=True,
    #                        ret_to_diff_city=True, max_stopovers=1, limit=1000)
    # export(response)
    db = Database(config.DB_FILENAME, config.DB_DEBUG)
    for file in os.listdir("tmp"):
        with open(os.path.join("tmp",file),"r") as fo:
            response = json.load(fo)
        db.insert_json(response, "")
