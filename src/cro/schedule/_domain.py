# -*- coding: utf-8 -*-

"""
Module contains domain model.
"""


import datetime as dt
from dataclasses import dataclass, field
from typing import Iterable, NewType

import pandas as pd

__all__ = tuple(["Station", "Schedule", "Show", "Person"])


URL = NewType("URL", str)


# TimeRange = tuple[time, time]


@dataclass(frozen=True)
class Station:
    """
    Station domain model.

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
class Person:
    id: int
    name: str


@dataclass(frozen=True)
class Kind:
    id: int
    code: str
    name: str


@dataclass(frozen=True)
class Show:
    id: int
    kind: Kind
    title: str
    station: Station
    description: str
    since: dt.datetime
    till: dt.datetime
    persons: tuple[Person]
    repetition: bool


@dataclass(frozen=False)
class Schedule:
    """
    Schedule for a given date and station.
    """

    date: dt.date
    station: Station
    shows: tuple[Show]
    time: tuple[dt.time, dt.time] = dt.time.min, dt.time.max
    __counter: int = field(init=False, repr=False, default=0)

    def __str__(self) -> str:
        return f"{type(self).__name__}(station={self.station.name}, date={self.date}, shows={len(self.shows)})"

    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self.shows[self.__counter]
        except IndexError:
            raise StopIteration

        self.__counter += 1

        return result

    def report(format: str = None) -> pd.DataFrame:
        """
        Návrh na podobu _flat_ (_tidy_) výstupu programu.

        |id|station|date|since|till|title|description|
        |--|-------|----|-----|----|-----|-----------|
        """
        return NotImplemented
