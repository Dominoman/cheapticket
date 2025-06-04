"""Convert to surrogate key

Revision ID: 1202299575f8
Revises: 8d2ec14f9542
Create Date: 2025-06-01 09:40:53.766266

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1202299575f8'
down_revision: Union[str, None] = '8d2ec14f9542'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # search table
    op.rename_table('search', 'search_old')
    op.create_table('search',
    sa.Column('rowid', sa.Integer(), primary_key=True, autoincrement=True),
    sa.Column('search_id', sa.String(length=36), nullable=False, unique=True),
    sa.Column('url', sa.String(length=2048), nullable=False),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=False),
    sa.Column('range_start', sa.Date(), nullable=False),
    sa.Column('range_end', sa.Date(), nullable=False),
    sa.Column('results', sa.Integer(), nullable=False),
    sa.Column('actual', sa.BOOLEAN(), nullable=False)
    )
    op.execute('''INSERT INTO search (search_id,url,timestamp,range_start,range_end,results,actual)
                  SELECT search_id,url,timestamp,range_start,range_end,results,actual FROM search_old''')
    op.drop_table('search_old')
    op.create_index(op.f('ix_search_actual'), 'search', ['actual'], unique=False)
    op.create_index(op.f('ix_search_search_id'), 'search', ['search_id'], unique=True)

    # itinerary table
    op.rename_table('itinerary', 'itinerary_old')
    op.create_table('itinerary',
    sa.Column('rowid', sa.Integer(), primary_key=True, autoincrement=True),
    sa.Column('search_id', sa.Integer(), nullable=False),
    sa.Column('itinerary_id', sa.String(length=255), nullable=False),
    sa.Column('flyFrom', sa.String(length=3), nullable=False),
    sa.Column('flyTo', sa.String(length=3), nullable=False),
    sa.Column('cityFrom', sa.String(length=50), nullable=False),
    sa.Column('cityCodeFrom', sa.String(length=3), nullable=False),
    sa.Column('cityTo', sa.String(length=50), nullable=False),
    sa.Column('cityCodeTo', sa.String(length=3), nullable=False),
    sa.Column('countryFromCode', sa.String(length=2), nullable=False),
    sa.Column('countryFromName', sa.String(length=50), nullable=False),
    sa.Column('countryToCode', sa.String(length=2), nullable=False),
    sa.Column('countryToName', sa.String(length=50), nullable=False),
    sa.Column('local_departure', sa.DateTime(), nullable=False),
    sa.Column('local_arrival', sa.DateTime(), nullable=False),
    sa.Column('nightsInDest', sa.Integer(), nullable=False),
    sa.Column('quality', sa.Float(), nullable=False),
    sa.Column('distance', sa.Float(), nullable=False),
    sa.Column('durationDeparture', sa.Integer(), nullable=False),
    sa.Column('durationReturn', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('conversionEUR', sa.Float(), nullable=False),
    sa.Column('availabilitySeats', sa.Integer(), nullable=True),
    sa.Column('airlines', sa.String(length=30), nullable=False),
    sa.Column('booking_token', sa.String(length=2048), nullable=False),
    sa.Column('deep_link', sa.String(length=2048), nullable=False),
    sa.Column('facilitated_booking_available', sa.Boolean(), nullable=False),
    sa.Column('pnr_count', sa.Integer(), nullable=False),
    sa.Column('has_airport_change', sa.Boolean(), nullable=False),
    sa.Column('technical_stops', sa.Integer(), nullable=False),
    sa.Column('throw_away_ticketing', sa.Boolean(), nullable=False),
    sa.Column('hidden_city_ticketing', sa.Boolean(), nullable=False),
    sa.Column('virtual_interlining', sa.Boolean(), nullable=False),
    sa.Column('rlocal_departure', sa.DateTime(), nullable=True),
    sa.Column('rlocal_arrival', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['search_id'], ['search.rowid'], ),
    sa.UniqueConstraint('search_id', 'itinerary_id')
    )
    op.execute('''INSERT INTO itinerary (search_id,itinerary_id, flyFrom, flyTo, cityFrom, cityCodeFrom, cityTo, cityCodeTo, countryFromCode, countryFromName, countryToCode, countryToName, local_departure, local_arrival, nightsInDest, quality, distance, durationDeparture, durationReturn, price, conversionEUR, availabilitySeats, airlines, booking_token, deep_link, facilitated_booking_available, pnr_count, has_airport_change, technical_stops, throw_away_ticketing, hidden_city_ticketing, virtual_interlining, rlocal_departure, rlocal_arrival )
                  SELECT (SELECT rowid FROM search WHERE search.search_id=itinerary_old.search_id),
                         id, flyFrom, flyTo, cityFrom, cityCodeFrom, cityTo, cityCodeTo, countryFromCode, countryFromName, countryToCode, countryToName, local_departure, local_arrival, nightsInDest, quality, distance, durationDeparture, durationReturn, price, conversionEUR, availabilitySeats, airlines, booking_token, deep_link, facilitated_booking_available, pnr_count, has_airport_change, technical_stops, throw_away_ticketing, hidden_city_ticketing, virtual_interlining, rlocal_departure, rlocal_arrival FROM itinerary_old;''')
    op.drop_table('itinerary_old')
    op.create_index(op.f('ix_itinerary_price'), 'itinerary', ['price'], unique=False)
    op.create_index(op.f('ix_itinerary_search_itinerary_id'), 'itinerary', ['search_id','itinerary_id'], unique=True)

    # route table
    op.rename_table('route', 'route_old')
    op.create_table('route',
                    sa.Column('rowid', sa.Integer(), primary_key=True, autoincrement=True),
                    sa.Column('route_id', sa.String(length=26), nullable=False,unique=True),
                    sa.Column('combination_id', sa.String(length=24), nullable=False),
                    sa.Column('flyFrom', sa.String(length=3), nullable=False),
                    sa.Column('flyTo', sa.String(length=3), nullable=False),
                    sa.Column('cityFrom', sa.String(length=50), nullable=False),
                    sa.Column('cityCodeFrom', sa.String(length=3), nullable=False),
                    sa.Column('cityTo', sa.String(length=50), nullable=False),
                    sa.Column('cityCodeTo', sa.String(length=3), nullable=False),
                    sa.Column('local_departure', sa.DateTime(), nullable=False),
                    sa.Column('local_arrival', sa.DateTime(), nullable=False),
                    sa.Column('airline', sa.String(length=2), nullable=False),
                    sa.Column('flight_no', sa.Integer(), nullable=False),
                    sa.Column('operating_carrier', sa.String(length=2), nullable=False),
                    sa.Column('operating_flight_no', sa.String(length=4), nullable=False),
                    sa.Column('fare_basis', sa.String(length=10), nullable=False),
                    sa.Column('fare_category', sa.String(length=1), nullable=False),
                    sa.Column('fare_classes', sa.String(length=1), nullable=False),
                    sa.Column('_return', sa.Integer(), nullable=False),
                    sa.Column('bags_recheck_required', sa.Boolean(), nullable=False),
                    sa.Column('vi_connection', sa.Boolean(), nullable=False),
                    sa.Column('guarantee', sa.Boolean(), nullable=False),
                    sa.Column('equipment', sa.String(length=4), nullable=True),
                    sa.Column('vehicle_type', sa.String(length=8), nullable=False)
                    )
    op.execute('''INSERT INTO route ( route_id, combination_id, flyFrom, flyTo, cityFrom, cityCodeFrom, cityTo, cityCodeTo, local_departure, local_arrival, airline, flight_no, operating_carrier, operating_flight_no, fare_basis, fare_category, fare_classes, _return, bags_recheck_required, vi_connection, guarantee, equipment, vehicle_type )
                  SELECT id, combination_id, flyFrom, flyTo, cityFrom, cityCodeFrom, cityTo, cityCodeTo, local_departure, local_arrival, airline, flight_no, operating_carrier, operating_flight_no, fare_basis, fare_category, fare_classes, _return, bags_recheck_required, vi_connection, guarantee, equipment, vehicle_type FROM route_old;''')
    op.drop_table('route_old')
    op.create_index(op.f('ix_route_route_id'), 'route', ['route_id'], unique=True)

    # itinerary2route table
    op.rename_table('itinerary2route', 'itinerary2route_old')
    op.create_table('itinerary2route',
    sa.Column('itinerary_id', sa.Integer(), nullable=False),
    sa.Column('route_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['route_id'], ['route.rowid'], ),
    sa.ForeignKeyConstraint(['itinerary_id'], ['itinerary.rowid'], ),
    sa.PrimaryKeyConstraint('itinerary_id', 'route_id')
    )
    op.execute('''INSERT INTO itinerary2route (itinerary_id,route_id)
                  SELECT (SELECT rowid FROM itinerary WHERE itinerary.search_id=(SELECT rowid FROM search WHERE search.search_id=itinerary2route_old.search_id)
                                                        AND itinerary.itinerary_id=itinerary2route_old.itinerary_id),
                    (SELECT rowid FROM route WHERE route.route_id=itinerary2route_old.route_id)
                    FROM itinerary2route_old;''')
    op.drop_table('itinerary2route_old')
    op.create_index('route_idx', 'itinerary2route', ['route_id'], unique=False)


def downgrade() -> None:
    # search table
    op.rename_table('search', 'search_old')
    op.create_table('search',
    sa.Column('search_id', sa.String(length=36), nullable=False),
    sa.Column('url', sa.String(length=2048), nullable=False),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=False),
    sa.Column('range_start', sa.Date(), nullable=False),
    sa.Column('range_end', sa.Date(), nullable=False),
    sa.Column('results', sa.Integer(), nullable=False),
    sa.Column('actual', sa.BOOLEAN(), nullable=False),
    sa.PrimaryKeyConstraint('search_id')
    )
    op.execute('''INSERT INTO search (search_id,url,timestamp,range_start,range_end,results,actual)
                  SELECT search_id,url,timestamp,range_start,range_end,results,actual FROM search_old''')

    # itinerary table
    op.rename_table('itinerary', 'itinerary_old')
    op.create_table('itinerary',
    sa.Column('search_id', sa.String(length=36), nullable=False),
    sa.Column('id', sa.String(length=255), nullable=False),
    sa.Column('flyFrom', sa.String(length=3), nullable=False),
    sa.Column('flyTo', sa.String(length=3), nullable=False),
    sa.Column('cityFrom', sa.String(length=50), nullable=False),
    sa.Column('cityCodeFrom', sa.String(length=3), nullable=False),
    sa.Column('cityTo', sa.String(length=50), nullable=False),
    sa.Column('cityCodeTo', sa.String(length=3), nullable=False),
    sa.Column('countryFromCode', sa.String(length=2), nullable=False),
    sa.Column('countryFromName', sa.String(length=50), nullable=False),
    sa.Column('countryToCode', sa.String(length=2), nullable=False),
    sa.Column('countryToName', sa.String(length=50), nullable=False),
    sa.Column('local_departure', sa.DateTime(), nullable=False),
    sa.Column('local_arrival', sa.DateTime(), nullable=False),
    sa.Column('nightsInDest', sa.Integer(), nullable=False),
    sa.Column('quality', sa.Float(), nullable=False),
    sa.Column('distance', sa.Float(), nullable=False),
    sa.Column('durationDeparture', sa.Integer(), nullable=False),
    sa.Column('durationReturn', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('conversionEUR', sa.Float(), nullable=False),
    sa.Column('availabilitySeats', sa.Integer(), nullable=True),
    sa.Column('airlines', sa.String(length=30), nullable=False),
    sa.Column('booking_token', sa.String(length=2048), nullable=False),
    sa.Column('deep_link', sa.String(length=2048), nullable=False),
    sa.Column('facilitated_booking_available', sa.Boolean(), nullable=False),
    sa.Column('pnr_count', sa.Integer(), nullable=False),
    sa.Column('has_airport_change', sa.Boolean(), nullable=False),
    sa.Column('technical_stops', sa.Integer(), nullable=False),
    sa.Column('throw_away_ticketing', sa.Boolean(), nullable=False),
    sa.Column('hidden_city_ticketing', sa.Boolean(), nullable=False),
    sa.Column('virtual_interlining', sa.Boolean(), nullable=False),
    sa.Column('rlocal_departure', sa.DateTime(), nullable=True),
    sa.Column('rlocal_arrival', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['search_id'], ['search.search_id'], ),
    sa.PrimaryKeyConstraint('search_id', 'id')
    )
    op.execute('''INSERT INTO itinerary (search_id,id, flyFrom, flyTo, cityFrom, cityCodeFrom, cityTo, cityCodeTo, countryFromCode, countryFromName, countryToCode, countryToName, local_departure, local_arrival, nightsInDest, quality, distance, durationDeparture, durationReturn, price, conversionEUR, availabilitySeats, airlines, booking_token, deep_link, facilitated_booking_available, pnr_count, has_airport_change, technical_stops, throw_away_ticketing, hidden_city_ticketing, virtual_interlining, rlocal_departure, rlocal_arrival )
                  SELECT (SELECT search_id FROM search_old WHERE search_old.rowid=itinerary_old.search_id),
                         itinerary_id, flyFrom, flyTo, cityFrom, cityCodeFrom, cityTo, cityCodeTo, countryFromCode, countryFromName, countryToCode, countryToName, local_departure, local_arrival, nightsInDest, quality, distance, durationDeparture, durationReturn, price, conversionEUR, availabilitySeats, airlines, booking_token, deep_link, facilitated_booking_available, pnr_count, has_airport_change, technical_stops, throw_away_ticketing, hidden_city_ticketing, virtual_interlining, rlocal_departure, rlocal_arrival FROM itinerary_old;''')

    # route table
    op.rename_table('route', 'route_old')
    op.create_table('route',
                    sa.Column('id', sa.String(length=26), nullable=False),
                    sa.Column('combination_id', sa.String(length=24), nullable=False),
                    sa.Column('flyFrom', sa.String(length=3), nullable=False),
                    sa.Column('flyTo', sa.String(length=3), nullable=False),
                    sa.Column('cityFrom', sa.String(length=50), nullable=False),
                    sa.Column('cityCodeFrom', sa.String(length=3), nullable=False),
                    sa.Column('cityTo', sa.String(length=50), nullable=False),
                    sa.Column('cityCodeTo', sa.String(length=3), nullable=False),
                    sa.Column('local_departure', sa.DateTime(), nullable=False),
                    sa.Column('local_arrival', sa.DateTime(), nullable=False),
                    sa.Column('airline', sa.String(length=2), nullable=False),
                    sa.Column('flight_no', sa.Integer(), nullable=False),
                    sa.Column('operating_carrier', sa.String(length=2), nullable=False),
                    sa.Column('operating_flight_no', sa.String(length=4), nullable=False),
                    sa.Column('fare_basis', sa.String(length=10), nullable=False),
                    sa.Column('fare_category', sa.String(length=1), nullable=False),
                    sa.Column('fare_classes', sa.String(length=1), nullable=False),
                    sa.Column('_return', sa.Integer(), nullable=False),
                    sa.Column('bags_recheck_required', sa.Boolean(), nullable=False),
                    sa.Column('vi_connection', sa.Boolean(), nullable=False),
                    sa.Column('guarantee', sa.Boolean(), nullable=False),
                    sa.Column('equipment', sa.String(length=4), nullable=True),
                    sa.Column('vehicle_type', sa.String(length=8), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.execute('''INSERT INTO route ( id, combination_id, flyFrom, flyTo, cityFrom, cityCodeFrom, cityTo, cityCodeTo, local_departure, local_arrival, airline, flight_no, operating_carrier, operating_flight_no, fare_basis, fare_category, fare_classes, _return, bags_recheck_required, vi_connection, guarantee, equipment, vehicle_type )
                  SELECT route_id, combination_id, flyFrom, flyTo, cityFrom, cityCodeFrom, cityTo, cityCodeTo, local_departure, local_arrival, airline, flight_no, operating_carrier, operating_flight_no, fare_basis, fare_category, fare_classes, _return, bags_recheck_required, vi_connection, guarantee, equipment, vehicle_type FROM route_old;''')

    # itinerary2route table
    op.rename_table('itinerary2route', 'itinerary2route_old')
    op.create_table('itinerary2route',
    sa.Column('search_id', sa.String(length=36), nullable=False),
    sa.Column('itinerary_id', sa.String(length=255), nullable=False),
    sa.Column('route_id', sa.String(length=26), nullable=False),
    sa.ForeignKeyConstraint(['route_id'], ['route.id'], ),
    sa.ForeignKeyConstraint(['search_id', 'itinerary_id'], ['itinerary.search_id', 'itinerary.id'], ),
    sa.PrimaryKeyConstraint('search_id', 'itinerary_id', 'route_id')
    )
    op.execute('''INSERT INTO itinerary2route (search_id, itinerary_id, route_id)
                  SELECT (SELECT (SELECT search_id FROM search_old WHERE search_old.rowid=itinerary_old.search_id) FROM itinerary_old WHERE itinerary_old.rowid=itinerary2route_old.itinerary_id),
                         (SELECT itinerary_id FROM itinerary_old WHERE itinerary_old.rowid=itinerary2route_old.itinerary_id), 
                         (SELECT route_id FROM route_old WHERE route_old.rowid=itinerary2route_old.route_id)
                  FROM itinerary2route_old''')

    # clean up
    op.drop_table('itinerary2route_old')
    op.create_index('route_idx', 'itinerary2route', ['route_id'], unique=False)
    op.drop_table('route_old')
    op.drop_table('itinerary_old')
    op.create_index(op.f('ix_itinerary_price'), 'itinerary', ['price'], unique=False)
    op.drop_table('search_old')
    op.create_index(op.f('ix_search_actual'), 'search', ['actual'], unique=False)
