from datetime import datetime, date
from typing import Optional, List, Dict, Tuple

from sqlalchemy import create_engine, TIMESTAMP, ForeignKey, String, Table, Column, select, Index, Update, Integer, \
    DateTime, Boolean, Date, UniqueConstraint, Float, func
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column, relationship, Query


class Base(DeclarativeBase):
    def compare(self, new_route: 'Base') -> Dict[str, Tuple[str, str]]:
        """ Compares the attributes of the current instance with those of a new instance."""
        return {
            item: (
                str(self.__getattribute__(item)),
                str(new_route.__getattribute__(item)),
            )
            for item in self.__dict__
            if item not in ("_sa_instance_state","rowid","itinerary")
               and self.__getattribute__(item) != new_route.__getattribute__(item)
        }


class Route(Base):
    __tablename__ = 'route'
    __table_args__ = (
        Index('ix_route_route_id', 'route_id', unique=True),
    )

    rowid: Mapped[int] = mapped_column(Integer, primary_key=True)
    route_id: Mapped[str] = mapped_column(String(26), unique=True)
    combination_id: Mapped[str] = mapped_column(String(24))
    flyFrom: Mapped[str] = mapped_column(String(3))
    flyTo: Mapped[str] = mapped_column(String(3))
    cityFrom: Mapped[str] = mapped_column(String(50))
    cityCodeFrom: Mapped[str] = mapped_column(String(3))
    cityTo: Mapped[str] = mapped_column(String(50))
    cityCodeTo: Mapped[str] = mapped_column(String(3))
    local_departure: Mapped[datetime] = mapped_column(DateTime)
    local_arrival: Mapped[datetime] = mapped_column(DateTime)
    airline: Mapped[str] = mapped_column(String(2))
    flight_no: Mapped[int] = mapped_column(Integer)
    operating_carrier: Mapped[str] = mapped_column(String(2))
    operating_flight_no: Mapped[str] = mapped_column(String(4))
    fare_basis: Mapped[str] = mapped_column(String(10))
    fare_category: Mapped[str] = mapped_column(String(1))
    fare_classes: Mapped[str] = mapped_column(String(1))
    _return: Mapped[int] = mapped_column(Integer)
    bags_recheck_required: Mapped[bool] = mapped_column(Boolean)
    vi_connection: Mapped[bool] = mapped_column(Boolean)
    guarantee: Mapped[bool] = mapped_column(Boolean)
    vehicle_type: Mapped[str] = mapped_column(String(8))
    equipment: Mapped[Optional[str]] = mapped_column(String(4))

    itinerary: Mapped[List['Itinerary']] = relationship('Itinerary', secondary='itinerary2route', back_populates='route')

    def __repr__(self):
        return (f"<Route(route_id={self.route_id!r}, flyFrom={self.flyFrom!r}, "
                f"flyTo={self.flyTo!r}, local_departure={self.local_departure!r})>")

class Search(Base):
    __tablename__ = 'search'
    __table_args__ = (
        Index('ix_search_actual', 'actual'),
        Index('ix_search_search_id', 'search_id', unique=True)
    )

    rowid: Mapped[int] = mapped_column(Integer, primary_key=True)
    search_id: Mapped[str] = mapped_column(String(36), unique=True)
    url: Mapped[str] = mapped_column(String(2048))
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP)
    range_start: Mapped[date] = mapped_column(Date)
    range_end: Mapped[date] = mapped_column(Date)
    results: Mapped[int] = mapped_column(Integer)
    actual: Mapped[bool] = mapped_column(Boolean)

    itinerary: Mapped[List['Itinerary']] = relationship('Itinerary', back_populates='search')

    def __repr__(self):
        return (f"<Search(search_id={self.search_id!r}, url={self.url!r}, "
                f"timestamp={self.timestamp!r}, actual={self.actual!r})>")

class Itinerary(Base):
    __tablename__ = 'itinerary'
    __table_args__ = (
        UniqueConstraint('search_id', 'itinerary_id'),
        Index('ix_itinerary_price', 'price'),
        Index('ix_itinerary_search_itinerary_id', 'search_id', 'itinerary_id', unique=True),
        Index('ix_itinerary_itinerary_id', 'itinerary_id')
    )

    rowid: Mapped[int] = mapped_column(Integer, primary_key=True)
    search_id: Mapped[int] = mapped_column(ForeignKey('search.rowid'))
    itinerary_id: Mapped[str] = mapped_column(String(255))
    flyFrom: Mapped[str] = mapped_column(String(3))
    flyTo: Mapped[str] = mapped_column(String(3))
    cityFrom: Mapped[str] = mapped_column(String(50))
    cityCodeFrom: Mapped[str] = mapped_column(String(3))
    cityTo: Mapped[str] = mapped_column(String(50))
    cityCodeTo: Mapped[str] = mapped_column(String(3))
    countryFromCode: Mapped[str] = mapped_column(String(2))
    countryFromName: Mapped[str] = mapped_column(String(50))
    countryToCode: Mapped[str] = mapped_column(String(2))
    countryToName: Mapped[str] = mapped_column(String(50))
    local_departure: Mapped[datetime] = mapped_column(DateTime)
    local_arrival: Mapped[datetime] = mapped_column(DateTime)
    nightsInDest: Mapped[int] = mapped_column(Integer)
    quality: Mapped[float] = mapped_column(Float)
    distance: Mapped[float] = mapped_column(Float)
    durationDeparture: Mapped[int] = mapped_column(Integer)
    durationReturn: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)
    conversionEUR: Mapped[float] = mapped_column(Float)
    airlines: Mapped[str] = mapped_column(String(30))
    booking_token: Mapped[str] = mapped_column(String(2048))
    deep_link: Mapped[str] = mapped_column(String(2048))
    facilitated_booking_available: Mapped[bool] = mapped_column(Boolean)
    pnr_count: Mapped[int] = mapped_column(Integer)
    has_airport_change: Mapped[bool] = mapped_column(Boolean)
    technical_stops: Mapped[int] = mapped_column(Integer)
    throw_away_ticketing: Mapped[bool] = mapped_column(Boolean)
    hidden_city_ticketing: Mapped[bool] = mapped_column(Boolean)
    virtual_interlining: Mapped[bool] = mapped_column(Boolean)
    availabilitySeats: Mapped[Optional[int]] = mapped_column(Integer)
    rlocal_departure: Mapped[Optional[datetime]] = mapped_column(DateTime)
    rlocal_arrival: Mapped[Optional[datetime]] = mapped_column(DateTime)

    search: Mapped[Search] = relationship('Search', back_populates='itinerary')
    route: Mapped[List[Route]] = relationship('Route', secondary='itinerary2route', back_populates='itinerary')

    def __repr__(self):
        return (f"<Itinerary(itinerary_id={self.itinerary_id!r}, flyFrom={self.flyFrom!r}, "
                f"flyTo={self.flyTo!r}, price={self.price!r})>")


t_itinerary2route = Table(
    'itinerary2route', Base.metadata,
    Column('itinerary_id', ForeignKey('itinerary.rowid'), primary_key=True, nullable=False),
    Column('route_id', ForeignKey('route.rowid'), primary_key=True, nullable=False),
    Index('route_idx', 'route_id')
)


class Database:
    KIWI_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.000Z"

    def __init__(self, db_url: str, debug: bool = False) -> None:
        self.engine = create_engine(db_url, echo=debug)
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)
        self.route_cache = {}

    def insert_json(self, json_data: dict, url: str = "", timestamp: datetime = None, range_start: date = None,
                    range_end: date = None,actual:bool=True) -> bool:
        """
        Inserts a new search and its itineraries and routes into the database from JSON data.
        Returns False if the search already exists, True if inserted.
        """
        stmt = select(Search).where(Search.search_id == json_data["search_id"])
        old_search = self.session.execute(stmt).scalar_one_or_none()
        if old_search is not None:
            return False
        if timestamp is None:
            timestamp = datetime.now()
        new_search = Search(search_id=json_data["search_id"], url=url, timestamp=timestamp,
                            results=json_data["_results"], range_start=range_start, range_end=range_end, actual=actual)
        self.session.add(new_search)
        for itinerary in json_data["data"]:
            local_departure = datetime.strptime(itinerary["local_departure"], self.KIWI_DATETIME_FORMAT)
            local_arrival = datetime.strptime(itinerary["local_arrival"], self.KIWI_DATETIME_FORMAT)
            airlines = ','.join(itinerary["airlines"])
            # booking_token és a deep_link túl sok helyet foglal, kihagyjuk
            new_itinerary = Itinerary(itinerary_id=itinerary["id"],
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
                                      booking_token='', deep_link='',
                                      facilitated_booking_available=itinerary["facilitated_booking_available"],
                                      pnr_count=itinerary["pnr_count"],
                                      has_airport_change=itinerary["has_airport_change"],
                                      technical_stops=itinerary["technical_stops"],
                                      throw_away_ticketing=itinerary["throw_away_ticketing"],
                                      hidden_city_ticketing=itinerary["hidden_city_ticketing"],
                                      virtual_interlining=itinerary["virtual_interlining"])
            new_search.itinerary.append(new_itinerary)
            for route in itinerary["route"]:
                self.add_route(new_itinerary, route)
        self.session.commit()
        return True

    def get_route_from_cache(self, route_id: str) -> Optional[Route]:
        if route_id in self.route_cache:
            return self.route_cache[route_id]
        stmt = select(Route).where(Route.route_id == route_id)
        route = self.session.execute(stmt).scalar_one_or_none()
        if route is not None:
            self.route_cache[route_id] = route
        return route

    def add_route_to_cache(self, route: Route) -> None:
        self.route_cache[route.route_id] = route

    def add_route(self, itinerary_obj: Itinerary, route: dict) -> bool:
        """
        Adds a route to the given itinerary, deduplicating by route ID.
        Updates existing route if changed. Returns True if new, False if existing.
        """
        local_departure = datetime.strptime(route["local_departure"], self.KIWI_DATETIME_FORMAT)
        local_arrival = datetime.strptime(route["local_arrival"], self.KIWI_DATETIME_FORMAT)
        new_route = Route(route_id=route["id"], combination_id=route["combination_id"], flyFrom=route["flyFrom"],
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
        # set return data to parent record
        if route["return"]==1:
            if itinerary_obj.rlocal_departure is None:
                itinerary_obj.rlocal_departure=local_departure
            itinerary_obj.rlocal_arrival=local_arrival

        old_route = self.get_route_from_cache(route["id"])
        if old_route is None:
            itinerary_obj.route.append(new_route)
            self.add_route_to_cache(new_route)
            return True
        diff = old_route.compare(new_route)
        if len(diff) > 0:
            self.make_history(old_route, diff)
        itinerary_obj.route.append(old_route)
        return False

    @staticmethod
    def make_history(old_route: Route, diff: Dict[str, Tuple[str, str]]) -> None:
        """
        Updates the old route's attributes with new values from the diff dictionary.
        """
        for k, v in diff.items():
            if k not in ["local_departure", "local_arrival"]:
                old_route.__setattr__(k, v[1])

    def get_all_search(self) -> Query:
        """
        Returns a SQLAlchemy Query for all Search records.
        """
        return self.session.query(Search)

    def delete_search(self, search: Search) -> None:
        """
        Deletes the given search and all related itineraries and unused routes from the database.
        """
        itinerary_rowids=[it.rowid for it in search.itinerary]

        subselect = (select(t_itinerary2route.c.route_id).
                     where(t_itinerary2route.c.itinerary_id.in_(itinerary_rowids)).
                     distinct()
                     )
        stmt = (select(t_itinerary2route.c.route_id).
                where(t_itinerary2route.c.route_id.in_(subselect)).
                group_by(t_itinerary2route.c.route_id).
                having(func.count('*') == 1)
                )
        unused_route_ids={row[0] for row in self.session.execute(stmt)}
        self.session.execute(t_itinerary2route.delete().
                             where(t_itinerary2route.c.itinerary_id.in_(itinerary_rowids)))
        if unused_route_ids:
            self.session.query(Route).filter(Route.rowid.in_(unused_route_ids)).delete(synchronize_session=False)
        self.session.query(Itinerary).filter(Itinerary.rowid.in_(itinerary_rowids)).delete(synchronize_session=False)
        self.session.query(Search).filter(Search.rowid == search.rowid).delete(synchronize_session=False)
        self.session.commit()

    def clean_actual_flag(self)->None:
        """
        Summary:
        Clears the 'actual' flag for all search records in the database.

        Explanation:
        This method updates the 'actual' field of all records in the 'search' table, setting it to False for those that are currently marked as True. It executes the update operation and commits the changes to the database.
        """
        update=Update(Search).where(Search.actual==True).values(actual=False)
        self.session.execute(update)
        self.session.commit()

    def fill_missing_itineraries(self,itinerary_rowids:list[int]) -> dict[str,list]:
        """
        This function must return a json that contain record from this database. The itinerary_rowsids parameter show
        what itinerary must be put in the json
        """
        itineraries = (
            self.session.query(Itinerary)
            .filter(Itinerary.rowid.in_(itinerary_rowids))
            .all()
        )
        result = {"itineraries": []}
        for it in itineraries:
            price_subquery = (
                self.session.query(Itinerary.price)
                .join(Search, Itinerary.search_id == Search.rowid)
                .filter(Itinerary.itinerary_id == it.itinerary_id, Search.actual == False)
                .order_by(Search.timestamp.desc())
                .limit(1)
            )
            latest_price = price_subquery.scalar()


            itinerary_json = {
                "id": it.itinerary_id,
                "cityFrom": it.cityFrom,
                "cityTo": it.cityTo,
                "countryFromName": it.countryFromName,
                "countryToName": it.countryToName,
                "local_departure": it.local_departure.strftime(self.KIWI_DATETIME_FORMAT),
                "local_arrival": it.local_arrival.strftime(self.KIWI_DATETIME_FORMAT),
                "rlocal_departure": it.rlocal_departure.strftime(self.KIWI_DATETIME_FORMAT),
                "rlocal_arrival": it.rlocal_arrival.strftime(self.KIWI_DATETIME_FORMAT),

                "nightsInDest": it.nightsInDest,
                "quality": it.quality,
                "distance": it.distance,
                "duration": {
                    "departure": it.durationDeparture,
                    "return": it.durationReturn,
                    "total": (it.durationDeparture or 0) + (it.durationReturn or 0),
                    "waiting_departure":0,
                    "waiting_return": 0
                },
                "price": it.price,
                "latest_price": latest_price if latest_price is not None else it.price,
                "route": [],
                "route_return": []
            }
            arrival1=arrival2=''
            for route in it.route:
                route_json = {
                    "id": route.route_id,
                    "combination_id": route.combination_id,
                    "cityFrom": route.cityFrom,
                    "cityTo": route.cityTo,
                    "local_departure": route.local_departure.strftime(self.KIWI_DATETIME_FORMAT),
                    "local_arrival": route.local_arrival.strftime(self.KIWI_DATETIME_FORMAT),
                    "airline": route.airline,
                    "flight_no": route.flight_no,
                    "return": route._return
                }
                if route._return==0:
                    itinerary_json["route"].append(route_json)
                    if arrival1!='':
                        itinerary_json["duration"]['waiting_departure']+= int(route.local_departure.timestamp() - arrival1.timestamp())
                    arrival1=route.local_arrival
                else:
                    itinerary_json["route_return"].append(route_json)
                    if arrival2!='':
                        itinerary_json["duration"]['waiting_return']+= int(route.local_departure.timestamp() - arrival2.timestamp())
                    arrival2 = route.local_arrival
            result["itineraries"].append(itinerary_json)
        return result
