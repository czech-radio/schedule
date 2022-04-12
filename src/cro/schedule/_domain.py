# -*- coding: utf-8 -*-

"""
This module contains domain model.
"""

from __future__ import annotations

import pathlib as pl
import datetime as dt
from typing import NewType, List
#from functools import total_ordering
from dataclasses import dataclass, field
from requests import get, Session

import pandas as pd

__all__ = tuple(["Station", "DaySchedule", "Kind", "Show", "Person"])

URL: str = f"https://api.rozhlas.cz/data/v2"

def get_stations():
    """
    Fetch the available stations.
    """
    data = get(f"{URL}/meta/stations.json").json()["data"]

    return[ Station(
                id=item["id"],
                name=item["name"],
                domain=item["domain"],
                slogan=item["longdescription"]["slogan"],
                description=item["description"],
                services=item["services"],
            )
            for item in data
        ]

@dataclass(frozen=True)
class Station:
    id: str
    name: str
    domain: str
    slogan: str
    description: str
    services: dict[str, URL] = field(hash=False)

    def __str__(self):
        return f'{self.id}:{self.name}'

@dataclass(frozen=True)
class Stations:
    stations: List[Station] = field(default_factory=get_stations)
        

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
    persons: tuple[Person] =  field(hash=False)
    repetition: bool

    def __post_init__(self) -> None:
        self.duration = (dt.datetime.min + (self.till - self.since)).time()


@dataclass(frozen=True)
class DaySchedule:
    date: dt.date
    station: Station
    shows: tuple[Show]
    time: tuple[dt.time, dt.time] = dt.time.min, dt.time.max

    def __str__(self) -> str:
        return f"{type(self).__name__}(station={self.station.name}, date={self.date}, shows={len(self.shows)})"

    def __len__(self) -> int:
        return len(self.shows)

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

