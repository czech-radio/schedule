# -*- coding: utf-8 -*-

"""
Module contains domain model.
"""


from datetime import date
from dataclasses import dataclass
from typing import Iterable, NewType


__all__ = tuple(["Station", "Schedule"])


URL = NewType("URL", str)


@dataclass(frozen=True)
class Station:
    """
    services: Dict[str, URL] e.g.
    - 'web': 'https://radiozurnal.rozhlas.cz',
    - 'player': 'https://www.mujrozhlas.cz/zive/radiozurnal',
    - 'schedule': 'https://www.rozhlas.cz/radiozurnal/program/',
    - 'rss': 'http://www.rozhlas.cz/export/radiozurnal/',
    - 'podcast': 'https://api.rozhlas.cz/data/v2/podcast/station/radiozurnal.rss',
    - 'iradio': 'http://www.rozhlas.cz/iradio/radiozurnal/',
    - 'webcam': 'http://www.rozhlas.cz/radiozurnal/studio/',
    - 'playlist': 'http://www.rozhlas.cz/radiozurnal/playlisty/',
    - 'audiolog': 'http://www.rozhlas.cz/radiozurnal/zaznamy/',
    - 'audioportal': 'http://www.rozhlas.cz/radiozurnal/audioarchiv/'

    """
    id: str
    name: str
    domain: str
    slogan: str
    description: str
    services: dict[str, URL]


@dataclass(frozen=True)
class Show:
    id: int
    title: str
    since: date
    till: date
    description: str


class Schedule:
    """
    Schedule for a given date and station.
    """

    def __init__(self, date: date, station: Station, shows: Iterable[Show]) -> None:
        self._date = date
        self._station = station
        self._shows = tuple(shows)

    @property
    def date(self) -> date:
        return self._date

    @property
    def station(self) -> Station:
        return self._station

    @property
    def shows(self) -> tuple[Show]:
        return self._shows

    def __str__(self) -> str:
        return f"{type(self).__name__}(date={self.date},station={self.station.name})"

    __repr__ = __str__

    def __iter__(self):
        return NotImplemented

    def __eq__(self, that: object) -> bool:
        return isinstance(that, type(self)) \
            and (that.date, that.station) == (self.date, self.station)

    def __hash__(self) -> int:
        return hash((type(self), self.date, self.station))


if __name__ == "__main__":

    schedule = Schedule(date(2022, 12, 31), Station("Plus"), ("Show1", "Show2"))
    print(schedule)