"""
This module contains domain model.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from enum import Enum
from functools import cached_property, total_ordering
from typing import NewType, Union

import pandas as pd

from cro.schedule._shared import convert_time

__all__ = tuple(["Schedule", "Show", "Station", "Person"])


URL = NewType("URL", str)
Title = str
Code = str
Name = str

SinceTime = Union[dt.time, str]
TillTime = Union[dt.time, str]


@dataclass(frozen=True)
class Station:
    """
    The Czech Radio station.
    """

    id: str  # pylint: disable=C0103
    name: Name
    domain: str
    slogan: str
    description: str
    services: dict[str, URL] = field(hash=False)


class KindName(Enum):
    """
    The show kind name as defined by internal systems.
    """

    ZPR: str  # Zprávy
    PUB: str  # Publicistika
    PDF: str  # Publicistika - Dokument/Feature
    PRO: str  # Literární pořady - Próza
    MAG: str  # Magazín zpravodajství, publicistiky a hudby


@dataclass(frozen=True)
class Kind:
    """
    The kind of show as defined by internal systems.
    """

    id: int  # pylint: disable=C0103
    code: Code
    name: Name  # Better to use :code:`KindName` enumaration?


@dataclass(frozen=True)
class Person:
    """
    The person associated with show e.g. moderator or respondent.
    """

    id: int  # pylint: disable=C0103
    name: Name


@total_ordering
@dataclass(frozen=True)
class Show:
    """
    The Czech Radio show.
    """

    id: int  # pylint: disable=C0103
    kind: Kind
    title: Title
    station: Station
    description: str
    date: dt.date
    since: dt.time
    till: dt.time
    moderators: tuple[Person] = field(hash=False)
    repetition: bool

    @cached_property
    def type(self) -> str:
        """
        The show type recognized by the broadcast time.
        We recognize morning, noon, afternoon, evening and night.

        :return: The show type as text (change to enumeration?).
        """
        if self.since >= dt.time(6, 0, 0) and self.since < dt.time(10, 0, 0):
            return "MORNING"
        elif self.since >= dt.time(10, 0, 0) and self.since < dt.time(12, 0, 0):
            return "NOON"
        elif self.since >= dt.time(12, 0, 0) and self.since < dt.time(18, 0, 0):
            return "AFTERNOON"
        elif self.since >= dt.time(18, 0, 0) and self.since < dt.time(22, 0, 0):
            return "EVENING"
        return "NIGHT"

    @cached_property
    def duration(self) -> float:
        """
        Get the show duration in seconds.

        Should we return :code:`dt.time`?
        :return: The duration in seconds.
        """
        return dt.timedelta(
            hours=self.till.hour - self.since.hour,
            minutes=self.till.minute - self.since.minute,
            seconds=self.till.second - self.since.second,
        ).total_seconds()

    def __lt__(self, that) -> bool:
        """
        Compare the shows by the *since* time so we can sort them.
        """
        return self.since < that.since


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
        return (
            f"{type(self).__name__}("
            f"station={self.station.name}, "
            f"date={self.date}, "
            f"shows={len(self.shows)})"
        )

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
                lambda show: (show.since >= since) and (show.till <= till),
                self.shows,
            )
        )

    def shows_by_title(
        self,
        title: str,
    ) -> tuple[Show]:
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

    def to_chart(self, shedule: Schedule) -> dict:
        """
        Return the multiple schedules as a vega chart.
        """
        if shedule is None:
            raise AssertionError
        return NotImplemented

    def to_table(self, without_timezone: bool = True) -> pd.DataFrame:
        """
        Return the schedule data as table.
        """
        df = pd.DataFrame(data=self.shows)

        # Use only some attributes from `kind` and `station` objects.
        df["kind"] = df["kind"].apply(lambda x: x["code"].lower())

        df["station"] = df["station"].apply(lambda x: x["id"])

        df.moderators = df.moderators.apply(
            lambda xs: ";".join([x["name"] for x in xs])
        )

        # Remove timezones for Excel exports.
        if without_timezone:
            df["till"] = df["till"].apply(lambda x: x.replace(tzinfo=None))
            df["since"] = df["since"].apply(lambda x: x.replace(tzinfo=None))

        since = df.since.apply(lambda x: dt.datetime.combine(self.shows[0].date, x))
        till = df.till.apply(lambda x: dt.datetime.combine(self.shows[0].date, x))

        df["duration"] = till - since
        df.duration = df.duration.apply(
            lambda x: "{:0>8}".format(str(dt.timedelta(seconds=x.total_seconds())))
        )

        return df[
            [
                "id",
                "station",
                "date",
                "since",
                "till",
                "duration",
                "repetition",
                "title",
                "moderators",
                "description",
            ]
        ]

    @classmethod
    def from_table(cls, table: pd.DataFrame, columns: dict = None) -> Schedule:
        """
        Factory method to create a schedule from the given data frame.
        """
        #
        # Preconditions:
        # - Dataset contain only data for one station and one date.
        #
        # Parse date from since or till columns.
        # Parse time from min(since) and max(till) columns.
        # Fetch station with the given station id.
        if not table:
            raise AssertionError(columns is not None)
        return NotImplemented
