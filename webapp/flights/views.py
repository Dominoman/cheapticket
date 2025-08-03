from flask import Blueprint, render_template, abort

from common.database import Itinerary, Search
from common.stat_utils import collect_logos
from webapp import db

flight_blueprint = Blueprint('flight',__name__)

@flight_blueprint.route('/')
def home():
    return "Sabai sabai"

@flight_blueprint.route('/flight/<itinerary_id>')
def flight(itinerary_id):
    prices = (
        db.session.query(Itinerary.rowid,Itinerary.price, Search.timestamp)
        .join(Search, Itinerary.search_id == Search.rowid)
        .filter(Itinerary.itinerary_id == itinerary_id)
        .order_by(Search.timestamp)
        .all()
    )
    if not prices:
        abort(404)
    itinerary=[prices[-1].rowid]
    labels = [p.timestamp.strftime("%Y.%m.%d") for p in prices]
    values = [int(p.price) for p in prices]
    result = db.fill_missing_itineraries(itinerary)
    logos = collect_logos(result)
    return render_template('flight.html',itinerary=result['itineraries'][0],logos=logos,labels=labels,prices=values)