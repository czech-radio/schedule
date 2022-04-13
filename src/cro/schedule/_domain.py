# -*- coding: utf-8 -*-

"""
This module contains domain model.
"""

from __future__ import annotations

import pathlib as pl
import datetime as dt
from typing import NewType, List, Optional, Union, Dict
#from functools import total_ordering
from dataclasses import dataclass, field
from requests import get, Session

import pandas as pd

__all__ = tuple(["Station", "DaySchedule", "Kind", "Show", "Person", "Broadcast"])

URL: str = f"https://api.rozhlas.cz/data/v2"

def get_stations() -> Broadcast:
    """
    Fetch available stations.

    """
    data = get(f"{URL}/meta/stations.json").json()["data"]

    return [ Station(
                id=item["id"],
                name=item["name"],
                domain=item["domain"],
                slogan=item["longdescription"]["slogan"],
                description=item["description"],
                services=item["services"],
            )
            for item in data
        ]


def populate_columns():
    """
    Temporary to fetch Shows columns
    """
    return [k for k in vars(Show)['__annotations__'].keys()]

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

    def __repr__(self):
        return f'{self.id}:{self.name}'

@dataclass(frozen=True)
class Broadcast:
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


@dataclass(frozen=False)
class DaySchedule:
    date: Union[dt.date, str]
    station: Station = None
    shows: tuple[Show] = ()
    
    #: The service REST API V2 base URL.
    __url__: str = f"https://api.rozhlas.cz/data/v2"

    #: The date format as data string input.
    __date_format__: str = "%Y-%m-%d"

    def __init__(self, sid: Optional[StationID] = None, date = dt.datetime.now()) -> None:
        """
        :param station_id: e.g. `radiozurnal`.
        :param date: e.g. `2022-04-10`
        """

        # Fetch the station and pick the right one.
        if sid is not None:
            try:
                self.station = type(self).get_station(sid.lower())
            except IndexError:
                raise ValueError(f"The station with id `{sid}` does not exist.")
        
        date = (
            dt.datetime.strptime(date, type(self).__date_format__).date()
            if isinstance(date, str)
            else date
        )

        data = get(
            f"{type(self).__url__}/schedule/day/{date.year:04d}/{date.month:02d}/{date.day:02d}/{self.station.id}.json"
        ).json()["data"]

        since, till = None, None
        shows = []
        for item in data:
            since, till = (
                dt.datetime.fromisoformat(item["since"]),
                dt.datetime.fromisoformat(item["till"]),
            )

            shows.append(
                Show(
                    id=item["id"],
                    title=item["title"],
                    station=self.station,
                    kind=Kind(
                        id=item["type"]["id"],
                        code=item["type"]["code"],
                        name=item["type"]["name"],
                    ),
                    description=item["description"],
                    since=since,
                    till=till,
                    persons=tuple(
                        (Person(p["id"], p["name"]) for p in item["persons"])
                    ),
                    repetition=item["repetition"],
                )
            )

        self.shows = tuple(shows)
        self.date = date.date() if isinstance(date, dt.datetime) else date


    def __str__(self) -> str:
        return f"{type(self).__name__}(station={self.station.name}, date={self.date}, shows={len(self.shows)})"

    def __len__(self) -> int:
        return len(self.shows)

    def to_table(self, without_timezone: bool = True) -> pd.DataFrame:
        """
        Return the schedule data as pandas dataframe.
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
        #[[k for k,v in self.columns_to_display.items() if v]]
    
    def filter_by_content(self, to_search ='', column='title', case=False, repeated=False) -> pd.DataFrame:
        """
        Return filtered schedule data by text content.
        """
        df = self.to_table()
        return df[(df[column].str.contains(to_search,case=case)) & (df.repetition==repeated)]

    def filter_by_columns(self, *columns) -> pd.DataFrame:
        """
        Return filtered schedule data by text content.
        """
        
        return self.to_table()[[*columns]]

    @classmethod
    def get_station(cls, sid: str) -> Optional[Station]:
        """
        Fetch the available station with the given station id (`sid`).

        :param sid: The station id.
        :return: The sequence of stations.
        """
        # Fetch the station and pick the right one.
        try:
            return tuple(filter(lambda x: x.id == sid, get_stations()))[0]
        except IndexError:
            # Should we aise ValueError(f"The station with id `{id}` does not exist.")?
            raise
