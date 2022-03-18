# -*- coding: utf-8 -*-

"""
Module contains HTTP REST API client.
"""

from enum import Enum
from datetime import date, datetime
from pydoc import describe

from requests import get

from cro.schedule._domain import Station, Show, Person, Schedule, Type


__all__ = tuple([
    "Client",
    "Stations",
])


class Stations(Enum):
    PLUS = "plus"
    RADIOZURNAL = "radiozurnal"


class Client:
    """
    The Czech Radio day schedule client.
    """

    __URL__ = "https://api.rozhlas.cz/data"
    __VERSION__ = 2

    def __init__(self, station_id: str = None):
        """
        :param station_id: e.g. `radiozurnal`.
        """
        # Fetch the station.
        self._station = filter(lambda x: x.id == station_id, type(self).get_stations())

    @property
    def date(self) -> date:
        return self._date

    @property
    def station(self) -> Station:
        return self._station

    @classmethod
    def get_stations(cls) -> tuple[Station]:
        """
        Fetch the available stations.

        Examples:
            >>> get_stations()
        """
        data = get(
            f"{cls.__URL__}/v{cls.__VERSION__}/meta/stations.json"
        ).json()["data"]

        stations = []
        for item in data:
            stations.append(Station(
                id = item["id"],
                name = item["name"],
                domain = item["domain"],
                slogan = item["longdescription"]["slogan"],
                description = item["description"],
                services = item["services"]
            ))

        return tuple(stations)

    def get_schedule(self, date: date = datetime.now()) -> Schedule:
        """
        Fetch the schedule for the given day and station.

        Examples:
            >>> get_schedule(dt.now())

        """
        data = get(
            f"{type(self).__URL__}/v{type(self).__VERSION__}/schedule/day/{date.year:04d}/{date.month:02d}/{date.day:02d}.json" \
            if self.station is None else \
            f"{type(self).__URL__}/v{type(self).__VERSION__}/schedule/day/{date.year:04d}/{date.month:02d}/{date.day:02d}/{self.station}.json"
        ).json()["data"]

        shows = []

        station_id = self.station

        for item in data:
            shows.append(
                Show(
                    id = item["id"],
                    type = Type(
                        id = item["type"]["id"],
                        code = item["type"]["code"],
                        name = item["type"]["name"]
                    ),
                    title = item["title"],
                    description = item["description"],
                    since = item["since"],
                    till = item["till"],
                    persons = tuple((Person(p["id"], p["name"]) for p in item["persons"])),
                    repetition = item["repetition"]
                )
            )

        return Schedule(
            date = date,
            station = self.station,
            shows = shows
        )


if __name__ == "__main__":

    client = Client("plus")

    # Shows
    result = client.get_schedule()

    print(result.date)
    print(result.station)

    # for item in result:
    #     print(item)

    # Stations
    # result: tuple[Station] = client.get_stations()

    # for item in result:
    #     print(item)
