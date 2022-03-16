# -*- coding: utf-8 -*-

"""
Module contains HTTP REST API client.
"""

from requests import get
from datetime import date, datetime
from enum import Enum
from cro.schedule.domain import Station


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
    __VERSION__ = 2

    def __init__(self, station: str = None):
        self._station = station

    @property
    def date(self) -> date:
        return self._date

    @property
    def station(self) -> Station:
        return self._station

    @classmethod
    def get_stations(cls) -> dict:
        """
        Fetch a available stations.

        Examples:
            >>> get_stations()
        """
        return get(f"{cls.__URL__}/v{cls.__VERSION__}/meta/stations.json").json()

    def get_schedule(self, date: date = datetime.now()) -> dict:
        """
        Fetch a schedule for the given day and station.

        Examples:
            >>> get_schedule(dt.now())

        """
        return get(
            f"{type(self).__URL__}/v{type(self).__VERSION__}/schedule/day/{date.year:04d}/{date.month:02d}/{date.day:02d}.json" \
            if self.station is None else \
            f"{type(self).__URL__}/v{type(self).__VERSION__}/schedule/day/{date.year:04d}/{date.month:02d}/{date.day:02d}/{self.station}.json"
        ).json()


if __name__ == "__main__":

    client = Client("plus")

    result = client.get_stations()

    fst = result["data"][0]

    print(fst)
    print("-----")
    print(fst["id"])
    print(fst["name"])
    print(fst["domain"])
    print(fst["description"])
    print("-----")
    print(fst["longdescription"])
    print("-----")
    print(fst["services"])

    # 'web': 'https://radiozurnal.rozhlas.cz',
    # 'player': 'https://www.mujrozhlas.cz/zive/radiozurnal',
    # 'schedule': 'https://www.rozhlas.cz/radiozurnal/program/',
    # 'rss': 'http://www.rozhlas.cz/export/radiozurnal/',
    # 'podcast': 'https://api.rozhlas.cz/data/v2/podcast/station/radiozurnal.rss',
    # 'iradio': 'http://www.rozhlas.cz/iradio/radiozurnal/',
    # 'webcam': 'http://www.rozhlas.cz/radiozurnal/studio/',
    # 'playlist': 'http://www.rozhlas.cz/radiozurnal/playlisty/',
    # 'audiolog': 'http://www.rozhlas.cz/radiozurnal/zaznamy/',
    # 'audioportal': 'http://www.rozhlas.cz/radiozurnal/audioarchiv/'}

    # result = client.get_schedule()
    # print(result["data"])