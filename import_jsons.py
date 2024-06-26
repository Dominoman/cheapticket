import json
import os

from tqdm import tqdm

from config import *
from database import Database

if __name__ == "__main__":
    JSONS_PATH = "tmp"

    db = Database(DB_FILENAME, DB_DEBUG)
    pbar = tqdm(os.listdir(JSONS_PATH))
    pbar.set_description("Processing json")
    for file in pbar:
        with open(os.path.join(JSONS_PATH, file), "r") as fo:
            data = json.loads(fo.read())
            db.insert_json(data, "")
