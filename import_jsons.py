#!/usr/bin/env python3

import json
import os
from datetime import datetime

from tqdm import tqdm

from config import *
from database import Database
from dateutil.relativedelta import relativedelta

if __name__ == "__main__":

    db = Database(DB_FILENAME, DB_DEBUG)
    pbar = tqdm(os.listdir(SAVEDIR))
    pbar.set_description("Processing json")
    for file in pbar:
        with open(os.path.join(SAVEDIR, file), "r") as fo:
            data = json.loads(fo.read())
            timestamp = datetime.strptime(file[:14], "%Y%m%d%H%M%S")
            range_start = datetime.strptime(file[15:21]+"01", "%Y%m%d").date()
            range_end=range_start+relativedelta(months=1,days=-1)
            db.insert_json(data, timestamp=timestamp, range_start=range_start, range_end=range_end)
