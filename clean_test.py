#!/usr/bin/env python3

import datetime
import logging
import os

from tqdm import tqdm

import config
from database import Database, Search

if __name__=="__main__":
    handler = logging.FileHandler(f"{os.path.splitext(__file__)[0]}.log")
    handler.setLevel(logging.DEBUG)
    logging.getLogger('sqlalchemy').addHandler(handler)
    db = Database(config.DB_FILENAME, config.DB_DEBUG)
    today= datetime.date.today()
    result=db.get_all_search().where(Search.range_end<today).all()
    for search in tqdm(result,"Processing rows"):
        if search.range_end<today:
            db.delete_search(search)
