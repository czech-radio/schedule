# -*- coding: utf-8 -*-

"""
Module contains HTTP REST API client.
"""

from enum import Enum
from datetime import date, datetime

from requests import get

from cro.schedule._domain import Station, Schedule
from cro.schedule._domain import Show, Person, Kind  # package protected


__all__ = tuple(["Client"])


class Client:
    """
    The Czech Radio day REST API v2 client to fetch schedeles and stations data.
    """

    # Interní dokumehtace položek JSON objektu
    # - `station` textové ID stanice (číselník viz https://api.rozhlas.cz/data/v2/meta/stations.json )
    # - `id` NEunikátní identifikátor převzatý z interního systému, ve kterém se plánuje vysílání; položka má vždy nějakou hodnotu
    # - `title` název pořadu; položka má vždy nějakou hodnotu
    # - `description` - popis pořadu; položka může být prázdná
    # - `since` - začátek vysílání pořadu; položka má vždy nějakou hodnotu
    # - `till` - konec vysílání pořadu; položka má vždy nějakou hodnotu
    # - `type` - nedokumentováno
    # - `edition` - pokud pro pořad existuje tzv. "webová vizitka", položka obsahuje objekt s příslušnými informacemi (např asset - vizuál pořadu); položka ovšem může být prázdná, vizitky totiž zatím neexistují pro všechny pořady
    # - `persons` pole objektů moderátorů pořadu (tzv. osoby), kterých může být 0-N (obsahuje kromě jiného také asset - fotografii moderátora); položka může být prázdná, protože ne každý pořad někdo moderuje a také ne pro všechny osoby máme k dispozici fotografie

    __URL__: str = f"https://api.rozhlas.cz/data/v2"

    def __init__(self, station_id: str):
        """
        :param station_id: e.g. `radiozurnal`.
        """
        try:  # Fetch the station and pick the right one.
            self._station = self.get_station(station_id.lower())
        except IndexError:
            raise ValueError(f"The station with id `{self.station_id}` does not exist.")

    @property
    def station(self) -> Station:
        """
        Get the current station.
        """
        return self._station

    def get_station(self, id: str) -> Station:
        """
        Fetch the available station with the given id.
        """
        try:  # Fetch the station and pick the right one.
            return tuple(filter(lambda x: x.id == id, self.get_stations()))[0]
        except IndexError:
            raise ValueError(f"The station with id `{id}` does not exist.")

    def get_stations(self) -> tuple[Station]:
        """
        Fetch the available stations.

        Examples:
            >>> get_stations()
        """
        data = get(f"{type(self).__URL__}/meta/stations.json").json()["data"]
        return tuple(
            [
                Station(
                    id=item["id"],
                    name=item["name"],
                    domain=item["domain"],
                    slogan=item["longdescription"]["slogan"],
                    description=item["description"],
                    services=item["services"],
                )
                for item in data
            ]
        )

    def get_day_schedule(self, date: date = datetime.now()) -> Schedule:
        """
        Fetch the availaible schedule for the given date.

        Examples:
            >>> get_schedule(dt.now())
        """

        data = get(
            f"{type(self).__URL__}/schedule/day/{date.year:04d}/{date.month:02d}/{date.day:02d}/{self.station.id}.json"
        ).json()["data"]

        shows = []

        for item in data:
            shows.append(
                Show(
                    id=item["id"],
                    title=item["title"],
                    station=self.station,
                    kind=Kind(
                        id=item["type"]["id"],
                        code=item["type"]["code"],
                        name=item["type"]["name"],
                    ),
                    description=item["description"],
                    since=item["since"],
                    till=item["till"],
                    persons=tuple(
                        (Person(p["id"], p["name"]) for p in item["persons"])
                    ),
                    repetition=item["repetition"],
                )
            )
        return Schedule(date=date, station=self.station, shows=shows)

    def get_week_schedule(self, date = datetime.now()) -> Schedule:
        """
        :param date: Any date in week
        """
        import datetime
        # Get all days of the week.
        dates = [date + datetime.timedelta(days=i) for i in range(0 - date.weekday(), 7 - date.weekday())]
        schedules = [ self.get_day_schedule(date) for date in dates]
        return schedules

    def get_month_schedule(self, date: datetime.now()) -> Schedule:
        # Get all days of the month.
        # dates = [date + datetime.timedelta(days=i) for i in range(0 - date.weekday(), 7 - date.weekday())]
        # schedules = [ self.get_day_schedule(date) for date in dates]
        # return schedules
        return NotImplemented
