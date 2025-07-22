#!/usr/bin/env python3

import datetime

from tqdm import tqdm

from config.config import config
from database import Database, Search

if __name__ == "__main__":
    today = datetime.date.today()
    db = Database(config.DB_FILENAME, config.DB_DEBUG)
    result = db.get_all_search().where(Search.range_end < today).all()
    pbar = tqdm(result, desc="Deleting old searches", unit="search", ncols=100, mininterval=1.0)
    for search in pbar:
        db.delete_search(search)