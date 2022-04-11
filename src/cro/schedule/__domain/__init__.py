# -*- coding: utf-8 -*-

"""
This module contains domain model.
"""

from __future__ import annotations

import datetime as dt
import pathlib as pl
from dataclasses import dataclass, field
from functools import total_ordering
from typing import NewType, Union

import pandas as pd

__all__ = tuple(["Station", "Schedule", "Show", "Person"])


URL = NewType("URL", str)


@dataclass(frozen=True)
class Station:
    id: str
    name: str
    domain: str
    slogan: str
    description: str
    services: dict[str, URL] = field(hash=False)


@dataclass(frozen=True)
class Person:
    id: int
    name: str


@dataclass(frozen=True)
class Kind:
    id: int
    code: str
    name: str


@dataclass(frozen=False, unsafe_hash=True)
class Show:
    id: int
    kind: Kind
    title: str
    station: Station
    description: str
    since: dt.datetime
    till: dt.datetime
    duration: dt.time = field(init=False)
    persons: tuple[Person] = field(hash=False)
    repetition: bool

    def __post_init__(self) -> None:
        self.duration = (dt.datetime.min + (self.till - self.since)).time()


@dataclass(frozen=True)
@total_ordering
class Schedule:
    date: dt.date
    station: Station
    shows: tuple[Show]
    time: tuple[dt.time, dt.time] = dt.time.min, dt.time.max

    #: The time format as data string input.
    __time_format__: str = "%H:%M:%S"

    def __str__(self) -> str:
        return f"{type(self).__name__}(station={self.station.name}, date={self.date}, shows={len(self.shows)})"

    def __lt__(self, that: Schedule) -> bool:
        return self.date < that.date

    def __len__(self) -> int:
        return len(self.shows)

    def is_subset(self) -> bool:
        """
        Does the schedule contain only a selected time range?
        """
        return (self.time[0], self.time[1]) == (dt.time.max, dt.time.min)

    def shows_between(self, since: Union[dt.time, str], till: Union[dt.time, str]) -> tuple[Show]:
        since = (
            dt.datetime.strptime(since, type(self).__time_format__).time()
            if isinstance(since, str)
            else since
        )

        till = (
            dt.datetime.strptime(till, type(self).__time_format__).time()
            if isinstance(till, str)
            else till
        )

        return tuple(
            filter(lambda show: (show.since.time() >= since) and (show.till.time() < till) , self.shows))

    def to_table(self, without_timezone: bool = True) -> pd.DataFrame:
        """
        Return the schedule data as table.
        """
        df = pd.DataFrame(data=self.shows)

        # Use only one attribute from kind and station objects.
        df["kind"] = df["kind"].apply(lambda x: x["code"].lower())
        df["station"] = df["station"].apply(lambda x: x["id"])

        # Replace empty persosn by None/NaN?
        df.persons = df.persons.apply(lambda xs: None if len(xs) == 0 else xs)

        # Remove timezones for Excel exports.
        if without_timezone:
            df["till"] = df["till"].apply(lambda x: x.replace(tzinfo=None))
            df["since"] = df["since"].apply(lambda x: x.replace(tzinfo=None))

        return df

    @classmethod
    def from_table(cls, table: pd.DataFrame) -> Schedule:
        """Factory method to create a schedule from the given dataset."""
        #
        # Preconditions:
        # - Dataset contain only data for one station and one date.
        #
        # Parse date from since or till columns.
        # Parse time from min(since) and max(till) columns.
        # Fetch station with the given station id.
        return NotImplemented


def schedule_as_table(schedule: Schedule) -> pd.DataFrame:
    """
    Return the multiple schedules as a pandas table.
    """
    return NotImplemented


def schedule_as_chart(shedule: Schedule) -> dict:
    """
    Return the multiple schedules as a vega chart.
    """
    return NotImplemented


def save_schedule_as_excel(schedule: Schedule, path: pl.Path) -> None:
    """
    Save the given schedule as Excel.

    :raise: IOError
    """
    return NotImplemented
