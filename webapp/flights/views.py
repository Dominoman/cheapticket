from flask import Blueprint, render_template, abort

from common.database import Itinerary, Search
from webapp import db

flight_blueprint = Blueprint('flight',__name__)

@flight_blueprint.route('/')
def home():
    return "Sabai sabai"

@flight_blueprint.route('/flight/<itinerary_id>')
def flight(itinerary_id):
    # get Itinerary by itinerary_id
    prices = (
        db.session.query(Itinerary.rowid,Itinerary.price, Search.timestamp)
        .join(Search, Itinerary.search_id == Search.rowid)
        .filter(Itinerary.itinerary_id == itinerary_id)
        .order_by(Search.timestamp)
        .all()
    )
    if prices is None:
        abort(404)
    itinerary=[prices[-1].rowid]
    result = db.fill_missing_itineraries(itinerary)
    return render_template('flight.html',itinerary=result['itineraries'][0],prices=prices)