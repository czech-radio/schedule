# -*- coding: utf-8 -*-

"""
Module contains HTTP REST API client. 
"""

from requests import get
from datetime import date, datetime
from enum import Enum


__all__ = tuple([
    "Client",
    "Stations",
])


class Stations(Enum):
    PLUS = "plus"
    RADIOZURNAL = "radiozurnal"


class Client:
    """
    The Czech Radio schedule client.
    """

    __URL__ = "https://api.rozhlas.cz/data"

    def __init__(self, version: int = 2):
        self.version = version

    def stations(self) -> dict:
        """
        Get a available stations.

        Examples:
            >>> get_stations()
        """
        return get(f"{type(self).__URL__}/v{self.version}/meta/stations.json").json()


    def schedule(self, date: date = datetime.now(), station: str = None) -> dict:
        """
        Get a schedule for the given day and station.

        Examples:
            >>> get_schedule(dt.now())

        """
        if station is None:
            url = f"{type(self).__URL__}/v{self.version}/schedule/day/{date.year:04d}/{date.month:02d}/{date.day:02d}.json"
        else:
            url = f"{type(self).__URL__}/v{self.version}/schedule/day/{date.year:04d}/{date.month:02d}/{date.day:02d}/{station}.json"

        return get(url).json()


if __name__ == "__main__":

    client = Client()

    result = client.stations()
    print(result)

    result = client.schedule(date(2021, 12, 31))
    print(result)
