from flask import Flask

from common.database import Database
from common.stat_utils import punctuation, to_time, up_n_down
from config.config import config

db = Database(config.DB_FILENAME,config.DB_DEBUG)
app = Flask(
    __name__,
    static_url_path = '/flight/static',
    static_folder = 'static'
)

from webapp.flights.views import flight_blueprint
app.register_blueprint(flight_blueprint)
app.jinja_env.filters['punctuation'] = punctuation
app.jinja_env.filters['to_time'] = to_time
app.jinja_env.filters['up_n_down'] = up_n_down
