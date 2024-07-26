#!/usr/bin/env python

from os import path
from urllib.parse import urlparse, parse_qs

import config
from database import Database

if __name__ == "__main__":
    db = Database(config.DB_FILENAME, config.DB_DEBUG)
    for search in db.get_all_search():
        query = urlparse(search.url).query
        date_from = parse_qs(query)["date_from"][0].split('/')
        date_to = parse_qs(query)["date_to"][0].split('/')
        fname = search.timestamp.strftime("%Y%m%d%H%M%S")
        fname += f"-{date_from[2]}{date_from[1]}.json"
        with open(path.join("tmp",fname),"w") as fo:
            fo.write(search.json)
        print(search.timestamp)
