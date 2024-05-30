from datetime import datetime
from typing import Optional

from sqlalchemy import create_engine, Text, String, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Search(Base):
    __tablename__ = "search"

    search_id: Mapped[str] = mapped_column(primary_key=True)
    url: Mapped[str]
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    json: Mapped[str] = mapped_column(Text())
    results: Mapped[int]


class Itinerary(Base):
    __tablename__ = "itinerary"

    id: Mapped[str] = mapped_column(primary_key=True)
    search_id: Mapped[str] = mapped_column(primary_key=True)
    flyFrom: Mapped[str] = mapped_column(String(3))
    flyTo: Mapped[str] = mapped_column(String(3))
    cityFrom: Mapped[str]
    cityCodeFrom: Mapped[str]
    cityTo: Mapped[str]
    cityCodeTo: Mapped[str] = mapped_column(String(3))
    countryFromCode: Mapped[str] = mapped_column(String(2))
    countryFromName: Mapped[str]
    countryToCode: Mapped[str] = mapped_column(String(2))
    countryToName: Mapped[str]
    local_departure: Mapped[datetime]
    local_arrival: Mapped[datetime]
    nightsInDest: Mapped[int]
    quality: Mapped[float]
    distance: Mapped[float]
    durationDeparture: Mapped[int]
    durationReturn: Mapped[int]
    price: Mapped[int]
    conversionEUR: Mapped[float]
    availabilitySeats: Mapped[Optional[int]]
    airlines: Mapped[str]
    booking_token: Mapped[str]
    deep_link: Mapped[str]
    facilitated_booking_available: Mapped[bool]
    pnr_count: Mapped[int]
    has_airport_change: Mapped[bool]
    technical_stops: Mapped[int]
    throw_away_ticketing: Mapped[bool]
    hidden_city_ticketing: Mapped[bool]
    virtual_interlining: Mapped[bool]


class Route(Base):
    __tablename__ = "route"

    id: Mapped[str] = mapped_column(primary_key=True)
    combination_id: Mapped[str]
    flyFrom: Mapped[str] = mapped_column(String(3))
    flyTo: Mapped[str] = mapped_column(String(3))
    cityFrom: Mapped[str]
    cityCodeFrom: Mapped[str] = mapped_column(String(3))
    cityTo: Mapped[str]
    cityCodeTo: Mapped[str] = mapped_column(String(3))
    local_departure: Mapped[datetime]
    local_arrival: Mapped[datetime]
    airline: Mapped[str]
    flight_no: Mapped[int]
    operating_carrier: Mapped[str]
    operating_flight_no: Mapped[str]
    fare_basis: Mapped[str]
    fare_category: Mapped[str]
    fare_classes: Mapped[str]
    _return: Mapped[int]
    bags_recheck_required: Mapped[bool]
    vi_connection: Mapped[str]
    guarantee: Mapped[str]
    equipment: Mapped[Optional[str]]
    vehicle_type: Mapped[str]


class Database:
    def __init__(self, file_name: str, debug: bool = True) -> None:
        self.engine = create_engine(f"sqlite:///{file_name}", echo=debug)
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def insert_json(self, response: dict, url: str) -> bool:
        row = self.session.query(Search).get(response["search_id"])
        if row is None:
            self.session.add(Search(search_id=response["search_id"], url=url, json="",results=response["_results"]))
        for data in response["data"]:
            for route in data["route"]:
                self.insert_route(route)
            self.insert_itinerary(response["search_id"], data)
        self.session.commit()
        return True

    def insert_itinerary(self, search_id: str, itinerary: dict) -> bool:
        row = self.session.query(Itinerary).get([itinerary["id"], search_id])
        if row is None:
            local_departure = datetime.strptime(itinerary['local_departure'], '%Y-%m-%dT%H:%M:%S.000Z')
            local_arrival = datetime.strptime(itinerary['local_arrival'], '%Y-%m-%dT%H:%M:%S.000Z')
            airlines = '.'.join(itinerary["airlines"])
            self.session.add(
                Itinerary(id=itinerary["id"], search_id=search_id, flyFrom=itinerary["flyFrom"],
                          flyTo=itinerary["flyTo"],
                          cityFrom=itinerary["cityFrom"], cityCodeFrom=itinerary["cityCodeFrom"],
                          cityTo=itinerary["cityTo"],
                          cityCodeTo=itinerary["cityCodeTo"], countryFromCode=itinerary["countryFrom"]["code"],
                          countryFromName=itinerary["countryFrom"]["name"],
                          countryToCode=itinerary["countryTo"]["code"],
                          countryToName=itinerary["countryTo"]["name"], local_departure=local_departure,
                          local_arrival=local_arrival, nightsInDest=itinerary["nightsInDest"],
                          quality=itinerary["quality"],
                          distance=itinerary["distance"], durationDeparture=itinerary["duration"]["departure"],
                          durationReturn=itinerary["duration"]["return"], price=itinerary["price"],
                          conversionEUR=itinerary["conversion"]["EUR"],
                          availabilitySeats=itinerary["availability"]["seats"],
                          airlines=airlines, booking_token=itinerary["booking_token"],
                          deep_link=itinerary["deep_link"],
                          facilitated_booking_available=itinerary["facilitated_booking_available"],
                          pnr_count=itinerary["pnr_count"], has_airport_change=itinerary["has_airport_change"],
                          technical_stops=itinerary["technical_stops"],
                          throw_away_ticketing=itinerary["throw_away_ticketing"],
                          hidden_city_ticketing=itinerary["hidden_city_ticketing"],
                          virtual_interlining=itinerary["virtual_interlining"]))
            return True
        return False

    def insert_route(self, route: dict) -> bool:
        row = self.session.query(Route).get(route["id"])
        if row is None:
            local_departure = datetime.strptime(route['local_departure'], '%Y-%m-%dT%H:%M:%S.000Z')
            local_arrival = datetime.strptime(route['local_arrival'], '%Y-%m-%dT%H:%M:%S.000Z')
            self.session.add(Route(id=route["id"],combination_id=route["combination_id"],flyFrom=route["flyFrom"],
                                   flyTo=route["flyTo"],cityFrom=route["cityFrom"],cityCodeFrom=route["cityCodeFrom"],
                                   cityTo=route["cityTo"], cityCodeTo=route["cityCodeTo"],
                                   local_departure=local_departure, local_arrival=local_arrival,
                                   airline=route["airline"],flight_no=route["flight_no"],
                                   operating_carrier=route["operating_carrier"],
                                   operating_flight_no=route["operating_flight_no"],fare_basis=route["fare_basis"],
                                   fare_category=route["fare_category"], fare_classes=route["fare_classes"],
                                   _return=route["return"], bags_recheck_required=route["bags_recheck_required"],
                                   vi_connection=route["vi_connection"], guarantee=route["guarantee"],
                                   equipment=route["equipment"], vehicle_type=route["vehicle_type"]))
            return True
        return False
