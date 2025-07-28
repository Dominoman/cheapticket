from flask import Blueprint, render_template

flight_blueprint = Blueprint('flight',__name__)

@flight_blueprint.route('/')
def home():
    return "Sabai sabai"

@flight_blueprint.route('/flight/<flight_id>')
def flight(flight_id):
    return render_template('flight.html',flight_id=flight_id)