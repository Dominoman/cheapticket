import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config:
    APIKEY = os.environ.get("APIKEY")
    DB_FILENAME = os.environ.get("DB_FILENAME", "sqlite:///database.db")
    DB_DEBUG = os.environ.get("DB_DEBUG", "false") == "true"
    SAVEDIR = os.environ.get("SAVEDIR", "../tmp")
    SMTP_SERVER = os.environ.get("SMTP_SERVER", "localhost")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", 25))
    SMTP_FROM = os.environ.get("SMTP_FROM", "admin@admin.hu")
    SMTP_PSW = os.environ.get("SMTP_PSW")
    SMTP_TO = os.environ.get("SMTP_TO", "nobody")
    APININJASKEY = os.environ.get("APININJASKEY")
    LOGOS = os.environ.get("LOGOS", "logos")
    AUTO_CLEANUP = os.environ.get("AUTO_CLEANUP","false") == "true"

config = Config()
