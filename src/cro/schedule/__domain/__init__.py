# -*- coding: utf-8 -*-

"""
This module contains domain model.
"""

from __future__ import annotations

import datetime as dt
import pathlib as pl
from dataclasses import dataclass, field, replace
from functools import total_ordering
from typing import NewType, Union

import pandas as pd

from cro.schedule.__shared import convert_time

__all__ = tuple(["Schedule", "Show", "Station", "Person"])


URL = NewType("URL", str)
Title = str
Code = str
Name = str

SinceTime = Union[dt.time, str]
TillTime = Union[dt.time, str]


@dataclass(frozen=True)
class Station:
    id: str
    name: Name
    domain: str
    slogan: str
    description: str
    services: dict[str, URL] = field(hash=False)


@dataclass(frozen=True)
class Person:
    id: int
    name: Name


@dataclass(frozen=True)
class Kind:
    id: int
    code: Code
    name: Name


@dataclass(frozen=False, unsafe_hash=True)
class Show:
    id: int
    kind: Kind
    title: Title
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
    """
    The day schedule domain entity (aggregate).
    """

    date: dt.date
    station: Station
    shows: tuple[Show]
    time: tuple[SinceTime, TillTime] = dt.time.min, dt.time.max  # since, till

    #: The time format as data string input.
    __time_format__: str = "%H:%M:%S"

    def __post_init__(self) -> None:
        # Check that all shows has same date as schedule
        ...

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
        return self.time[0] > dt.time.min or self.time[1] < dt.time.max

    def as_subset(self, since: SinceTime, till: TillTime) -> Schedule:
        """
        Return the subset of this schedule.
        """
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
        return type(self)(
            date=self.date,
            time=(since, till),
            station=self.station,
            shows=self.shows_by_time(since, till),
        )

    def shows_by_time(self, since: SinceTime, till: TillTime) -> tuple[Show]:
        """
        Return the subset of shows filtered by time (till exclusive).
        """
        since = convert_time(since)
        till = convert_time(till)

        # Fix error if `show.till` is midnight 00.00.00

        return tuple(
            filter(
                lambda show: (show.since.time() >= since)
                and (show.till.time() <= till),
                self.shows,
            )
        )

    def shows_by_title(self, title: str,) -> tuple[Show]:
        """
        Return the subset of shows filtered by title.
        """
        # Use not `exact_match`?
        return tuple(
            filter(
                lambda show: (show.title == title),
                self.shows,
            )
        )

    def to_excel(self, schedule: Schedule, path: pl.Path) -> object:
        """
        Return the given schedule as Excel workbook.
        """
        schedule, path # unused
        return NotImplemented

    def to_chart(self, shedule: Schedule) -> dict:
        """
        Return the multiple schedules as a vega chart.
        """
        shedule # unused
        return NotImplemented

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
    def from_table(cls, table: pd.DataFrame, columns: dict = None) -> Schedule:
        """Factory method to create a schedule from the given dataset."""
        #
        # Preconditions:
        # - Dataset contain only data for one station and one date.
        #
        # Parse date from since or till columns.
        # Parse time from min(since) and max(till) columns.
        # Fetch station with the given station id.
        return NotImplemented
