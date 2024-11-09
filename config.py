import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

APIKEY = os.environ.get("APIKEY")
DB_FILENAME = os.environ.get("DB_FILENAME")
DB_DEBUG = os.environ.get("DB_DEBUG")
SAVEDIR = os.environ.get("SAVEDIR")
SMTP_SERVER=os.environ.get("SMTP_SERVER")
SMTP_PORT=os.environ.get("SMTP_PORT")
SMTP_FROM=os.environ.get("SMTP_FROM")
SMTP_PSW=os.environ.get("SMTP_PSW")
SMTP_TO=os.environ.get("SMTP_TO")
