import json
from datetime import datetime
from typing import Optional, List, Dict, Tuple

from sqlalchemy import create_engine, TIMESTAMP, TEXT, ForeignKey, String, Table, Column, and_
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    def compare(self, new_route: 'Base') -> Dict[str, Tuple[str, str]]:
        return {
            item: (
                str(self.__getattribute__(item)),
                str(new_route.__getattribute__(item)),
            )
            for item in self.__dict__
            if item != "_sa_instance_state"
            and self.__getattribute__(item) != new_route.__getattribute__(item)
        }


class Search(Base):
    __tablename__ = "search"

    search_id: Mapped[str] = mapped_column(primary_key=True)
    url: Mapped[str]
    json: Mapped[str] = mapped_column(TEXT)
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    results: Mapped[int]

    itineraries: Mapped[List["Itinerary"]] = relationship(back_populates="parent",cascade="all, delete")


itinerary2route_table = Table("itinerary2route", Base.metadata,
                              Column("search_id", ForeignKey("itinerary.search_id"), primary_key=True),
                              Column("itinerary_id", ForeignKey("itinerary.id"), primary_key=True),
                              Column("route_id", ForeignKey("route.id"), primary_key=True))


class Itinerary(Base):
    __tablename__ = "itinerary"

    search_id: Mapped[str] = mapped_column(ForeignKey("search.search_id"), primary_key=True)
    id: Mapped[str] = mapped_column(primary_key=True)
    flyFrom: Mapped[str] = mapped_column(String(3))
    flyTo: Mapped[str] = mapped_column(String(3))
    cityFrom: Mapped[str]
    cityCodeFrom: Mapped[str] = mapped_column(String(3))
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
    price: Mapped[float]
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

    parent: Mapped["Search"] = relationship(back_populates="itineraries")
    routes: Mapped[List['Route']] = relationship(secondary=itinerary2route_table,
                                                 primaryjoin=lambda: and_(
                                                     itinerary2route_table.c.search_id == Itinerary.search_id,
                                                     itinerary2route_table.c.itinerary_id == Itinerary.id),
                                                 secondaryjoin=lambda: itinerary2route_table.c.route_id == Route.id,
                                                 back_populates="itineraries")


class Route(Base):
    __tablename__ = "route"

    id: Mapped[str] = mapped_column(primary_key=True)
    combination_id: Mapped["str"]
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
    vi_connection: Mapped[bool]
    guarantee: Mapped[bool]
    equipment: Mapped[Optional[str]]
    vehicle_type: Mapped[str]

    itineraries: Mapped[List[Itinerary]] = relationship(secondary=itinerary2route_table,
                                                        primaryjoin=lambda: itinerary2route_table.c.route_id == Route.id,
                                                        secondaryjoin=lambda: and_(
                                                            itinerary2route_table.c.search_id == Itinerary.search_id,
                                                            itinerary2route_table.c.itinerary_id == Itinerary.id),
                                                        back_populates="routes")
    histories: Mapped[List["RouteHistory"]] = relationship(back_populates="route", cascade="all, delete")


class RouteHistory(Base):
    __tablename__ = "routehistory"

    route_id: Mapped[str] = mapped_column(ForeignKey("route.id"), primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(primary_key=True)
    fieldName: Mapped[str] = mapped_column(primary_key=True)
    oldValue: Mapped[str]
    newValue: Mapped[str]

    route: Mapped[Route] = relationship(back_populates="histories")


class Database:
    def __init__(self, file_name: str, debug: bool = False) -> None:
        self.engine = create_engine(f"sqlite:///{file_name}", echo=debug)
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def insert_json(self, json_data: dict, url: str = "", timestamp: datetime = None) -> bool:
        old_search = self.session.query(Search).get(json_data["search_id"])
        if old_search is not None:
            return False
        if timestamp is None:
            timestamp = datetime.now()
        json_text = json.dumps(json_data, indent=4)
        new_search = Search(search_id=json_data["search_id"], url=url, json=json_text, timestamp=timestamp,
                            results=json_data["_results"])
        self.session.add(new_search)
        for itinerary in json_data["data"]:
            local_departure = datetime.strptime(itinerary["local_departure"], "%Y-%m-%dT%H:%M:%S.000Z")
            local_arrival = datetime.strptime(itinerary["local_arrival"], "%Y-%m-%dT%H:%M:%S.000Z")
            airlines = ','.join(itinerary["airlines"])
            new_itinerary = Itinerary(search_id=json_data["search_id"], id=itinerary["id"],
                                      flyFrom=itinerary["flyFrom"],
                                      flyTo=itinerary["flyTo"], cityFrom=itinerary["cityFrom"],
                                      cityCodeFrom=itinerary["cityCodeFrom"], cityTo=itinerary["cityTo"],
                                      cityCodeTo=itinerary["cityCodeTo"],
                                      countryFromCode=itinerary["countryFrom"]["code"],
                                      countryFromName=itinerary["countryFrom"]["name"],
                                      countryToCode=itinerary["countryTo"]["code"],
                                      countryToName=itinerary["countryTo"]["name"], local_departure=local_departure,
                                      local_arrival=local_arrival, nightsInDest=itinerary["nightsInDest"],
                                      quality=itinerary["quality"], distance=itinerary["distance"],
                                      durationDeparture=itinerary["duration"]["departure"],
                                      durationReturn=itinerary["duration"]["return"], price=itinerary["price"],
                                      conversionEUR=itinerary["conversion"]["EUR"],
                                      availabilitySeats=itinerary["availability"]["seats"], airlines=airlines,
                                      booking_token=itinerary["booking_token"], deep_link=itinerary["deep_link"],
                                      facilitated_booking_available=itinerary["facilitated_booking_available"],
                                      pnr_count=itinerary["pnr_count"],
                                      has_airport_change=itinerary["has_airport_change"],
                                      technical_stops=itinerary["technical_stops"],
                                      throw_away_ticketing=itinerary["throw_away_ticketing"],
                                      hidden_city_ticketing=itinerary["hidden_city_ticketing"],
                                      virtual_interlining=itinerary["virtual_interlining"])
            self.session.add(new_itinerary)
            for route in itinerary["route"]:
                self.add_route(new_itinerary, route)
            self.session.commit()
        return True

    def add_route(self, itinerary_obj: Itinerary, route: dict) -> bool:
        local_departure = datetime.strptime(route["local_departure"], "%Y-%m-%dT%H:%M:%S.000Z")
        local_arrival = datetime.strptime(route["local_arrival"], "%Y-%m-%dT%H:%M:%S.000Z")
        new_route = Route(id=route["id"], combination_id=route["combination_id"], flyFrom=route["flyFrom"],
                          flyTo=route["flyTo"], cityFrom=route["cityFrom"], cityCodeFrom=route["cityCodeFrom"],
                          cityTo=route["cityTo"], cityCodeTo=route["cityCodeTo"], local_departure=local_departure,
                          local_arrival=local_arrival, airline=route["airline"], flight_no=route["flight_no"],
                          operating_carrier=route["operating_carrier"],
                          operating_flight_no=route["operating_flight_no"],
                          fare_basis=route["fare_basis"], fare_category=route["fare_category"],
                          fare_classes=route["fare_classes"], _return=route["return"],
                          bags_recheck_required=route["bags_recheck_required"],
                          vi_connection=route["vi_connection"],
                          guarantee=route["guarantee"], equipment=route["equipment"],
                          vehicle_type=route["vehicle_type"])

        old_route = self.session.query(Route).get(route["id"])
        if old_route is None:
            itinerary_obj.routes.append(new_route)
            return True
        diff = old_route.compare(new_route)
        if len(diff) > 0:
            self.make_history(old_route, diff)
        itinerary_obj.routes.append(old_route)
        return False

    @staticmethod
    def make_history(old_route: Route, diff: Dict[str, Tuple[str, str]]) -> None:
        for k, v in diff.items():
            history = RouteHistory(route_id=old_route.id, timestamp=datetime.now(), fieldName=k, oldValue=v[0],
                                   newValue=v[1])
            old_route.histories.append(history)
            if k in ["local_departure", "local_arrival"]:
                pass
            else:
                old_route.__setattr__(k, v[1])
