#!/usr/bin/env python3

import json
import os
from datetime import datetime

from dateutil.relativedelta import relativedelta
from tqdm import tqdm

from config.config import config
from database import Database

if __name__ == "__main__":
    db = Database(config.DB_FILENAME, config.DB_DEBUG)
    all_jsons=[ f for f in os.listdir(config.SAVEDIR) if f.endswith(".json")]
    pbar = tqdm(all_jsons, desc="Processing json files", unit="file", ncols=100, mininterval=1.0)
    for file in pbar:
        with open( os.path.join(config.SAVEDIR,file), "r") as fo:
            data = json.loads(fo.read())
            timestamp = datetime.strptime(file[:14], "%Y%m%d%H%M%S")
            range_start = datetime.strptime(file[15:21]+"01", "%Y%m%d").date()
            range_end=range_start+relativedelta(months=1,days=-1)
            db.insert_json(data, timestamp=timestamp, range_start=range_start, range_end=range_end, actual=False)
