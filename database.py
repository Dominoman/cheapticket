import datetime
from typing import Optional, List

from sqlalchemy import create_engine, TIMESTAMP, TEXT, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Search(Base):
    __tablename__ = "search"

    search_id: Mapped[str] = mapped_column(primary_key=True)
    url: Mapped[str]
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC))
    json: Mapped[str] = mapped_column(TEXT)
    results: Mapped[int]
    itineraries: Mapped[List["Itinerary"]] = relationship(back_populates="parent")


class Itinerary(Base):
    __tablename__ = "itinerary"

    search_id: Mapped[str] = mapped_column(ForeignKey("search.search_id"),primary_key=True)
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
    local_departure: Mapped[datetime.datetime]
    local_arrival: Mapped[datetime.datetime]
    nightsInDest: Mapped[int]
    quality: Mapped[float]
    distance: Mapped[float]
    durationDeparture: Mapped[int]
    durationReturn: Mapped[int]
    price: Mapped[float]
    conversionEUR: Mapped[float]
    currency: Mapped[str] = mapped_column(String(3))
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
    parent: Mapped["Search"]=relationship(back_populates="itineraries")


class Database:
    def __init__(self, file_name: str, debug: bool = False) -> None:
        self.engine = create_engine(f"sqlite:///{file_name}", echo=debug)
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def insert_json(self, json_data: dict, url: str) -> bool:
        row = self.session.query(Search).get(json_data["search_id"])
        if row is None:
            self.session.add(Search(search_id=json_data["search_id"], url=url, json="", results=json_data["_results"]))
        for itinerary in json_data["data"]:
            local_departure = datetime.datetime.strptime(itinerary["local_departure"], "%Y-%m-%dT%H:%M:%S.000Z")
            local_arrival = datetime.datetime.strptime(itinerary["local_arrival"], "%Y-%m-%dT%H:%M:%S.000Z")
            airlines = ",".join(itinerary["airlines"])
            self.session.add(
                Itinerary(search_id=json_data["search_id"], id=itinerary["id"], flyFrom=itinerary["flyFrom"],
                          flyTo=itinerary["flyTo"], cityFrom=itinerary["cityFrom"],
                          cityCodeFrom=itinerary["cityCodeFrom"], cityTo=itinerary["cityTo"],
                          cityCodeTo=itinerary["cityCodeTo"], countryFromCode=itinerary["countryFrom"]["code"],
                          countryFromName=itinerary["countryFrom"]["name"],
                          countryToCode=itinerary["countryTo"]["code"],
                          countryToName=itinerary["countryTo"]["name"], local_departure=local_departure,
                          local_arrival=local_arrival, nightsInDest=itinerary["nightsInDest"],
                          quality=itinerary["quality"], distance=itinerary["distance"],
                          durationDeparture=itinerary["duration"]["departure"],
                          durationReturn=itinerary["duration"]["return"], price=itinerary["price"],
                          conversionEUR=itinerary["conversion"]["EUR"], currency=json_data["currency"],
                          availabilitySeats=itinerary["availability"]["seats"], airlines=airlines,
                          booking_token=itinerary["booking_token"], deep_link=itinerary["deep_link"],
                          facilitated_booking_available=itinerary["facilitated_booking_available"],
                          pnr_count=itinerary["pnr_count"],
                          has_airport_change=itinerary["has_airport_change"],
                          technical_stops=itinerary["technical_stops"],
                          throw_away_ticketing=itinerary["throw_away_ticketing"],
                          hidden_city_ticketing=itinerary["hidden_city_ticketing"],
                          virtual_interlining=itinerary["virtual_interlining"]))
        self.session.commit()
        return True
