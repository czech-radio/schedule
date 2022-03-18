# -*- coding: utf-8 -*-

"""
Module contains HTTP REST API client.
"""

from enum import Enum
from datetime import date, datetime

from requests import get

from cro.schedule._domain import Station, Show, Person, Schedule, Kind


__all__ = tuple(["Client"]
)


class Client:
    """
    The Czech Radio day REST API v2 client to fetch schedeles and stations data.
    """

    __URL__: str = f"https://api.rozhlas.cz/data/v2"

    def __init__(self, station_id: str):
        """
        :param station_id: e.g. `radiozurnal`.
        """
        try: # Fetch the station and pick the right one.
            self._station = self.get_station(station_id)
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
        try: # Fetch the station and pick the right one.
            return tuple(filter(lambda x: x.id == id, self.get_stations()))[0]
        except IndexError:
            raise ValueError(f"The station with id `{id}` does not exist.")

    def get_stations(self) -> tuple[Station]:
        """
        Fetch the available stations.

        Examples:
            >>> get_stations()
        """
        data = get(f"{type(self).__URL__}/meta/stations.json").json()[
            "data"
        ]
        stations = []
        for item in data:
            stations.append(
                Station(
                    id=item["id"],
                    name=item["name"],
                    domain=item["domain"],
                    slogan=item["longdescription"]["slogan"],
                    description=item["description"],
                    services=item["services"],
                )
            )
        return tuple(stations)

    def get_schedule(self, date: date = datetime.now()) -> Schedule:
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
            shows.append(Show(
                id = item["id"],
                title = item["title"],
                station = self.station,
                kind =Kind(
                    id=item["type"]["id"],
                    code=item["type"]["code"],
                    name=item["type"]["name"]
                ),
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

    def get_schedules(self, date: date = datetime.now()) -> tuple[Schedule]:
        """
        Fetch the availaible schedules for the given date.
        """
        return NotImplemented


if __name__ == "__main__":

    client = Client("plus")

    result: tuple[Schedule] = client.get_schedule()
    for item in result:
        print(item)

    # result: tuple[Station] = client.get_stations()
    # for item in result:
    #     print(item)
