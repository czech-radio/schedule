# -*- coding: utf-8 -*-

"""
Module contains domain model.
"""

from __future__ import annotations, with_statement

import datetime as dt
from dataclasses import dataclass, field
from functools import total_ordering
from typing import Iterable, NewType

import pandas as pd

__all__ = tuple(["Station", "Schedule", "Show", "Person"])


URL = NewType("URL", str)


# Should we define TimeRange = tuple[time, time]?


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


@dataclass(frozen=True)
@total_ordering
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

    def __iter__(self) -> Schedule:
        return self

    def __next__(self):
        try:
            result = self.shows[self.__counter]
        except IndexError:
            raise StopIteration

        self.__counter += 1

        return result

    def __lt__(self, that: Schedule) -> bool:
        return self.date < that.date

    def is_subset(self) -> bool:
        """
        Does the schedule contain only a selected time range?
        """
        return (self.time[0], self.time[1]) == (dt.time.max, dt.time.min)

    def as_table(self, without_timezone: bool = True) -> pd.DataFrame:
        """
        Return the schedule data as table.
        """
        df = pd.DataFrame(data=self.shows)

        # Use only one attribute from kins and station objects.
        df["kind"] = df["kind"].apply(lambda x: x["code"].lower())
        df["station"] = df["station"].apply(lambda x: x["id"])

        # Remove timezones for Excel exports.
        if without_timezone:
            df["till"] = df["till"].apply(lambda x: x.replace(tzinfo=None))
            df["since"] = df["till"].apply(lambda x: x.replace(tzinfo=None))

        return df

    @classmethod
    def make(cls, date, time, station, shows) -> Schedule:
        """
        Make the schedule (factory method).
        """
        return cls(date=date, time=time, station=station, shows=tuple(shows))


def schedules_as_table(schedule: Schedule) -> pd.DataFrame:
    """
    Return the multiple schedules as a pandas table.
    """
    return NotImplemented


def schedules_as_chart(shedule: Schedule) -> dict:
    """
    Return the multiple schedules as a vega chart.
    """
    return NotImplemented
