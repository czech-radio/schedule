# -*- coding: utf-8 -*-

"""
Module contains domain model.
"""


from datetime import date
from dataclasses import dataclass
from typing import Iterable


__all__ = tuple(["Station", "Schedule"])


@dataclass(frozen=True)
class Station:
    name: str


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