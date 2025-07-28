from flask import Flask

from webapp.flights.views import flight_blueprint

app = Flask(__name__)
app.register_blueprint(flight_blueprint)
