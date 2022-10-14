"""
Module contains HTTP REST API client.
"""

from __future__ import annotations

import datetime as dt
from calendar import monthrange
from typing import Optional, Union

from charset_normalizer import logging
from requests import Session, get

from cro.schedule._domain import Schedule, Kind, Person, Show, Station
from cro.schedule._shared import convert_date


__all__ = tuple(["Client"])


def is_time_between(begin_time: dt.time, end_time: dt.time, current_time: dt.time):
    """
    Determine if the current time is within a specified range.

    .. see: https://stackoverflow.com/a/10048290
    """
    if begin_time < end_time:
        return begin_time <= current_time <= end_time
    else:  # crosses midnight
        return (current_time >= begin_time) or (current_time <= end_time)


StationID = str


class Client:
    """
    The Czech Radio client to fetch schedules and stations metadata.
    """

    #: The service REST API V2 base URL.
    __url__: str = f"https://api.rozhlas.cz/data/v2"

    #: The date format as data string input.
    __date_format__: str = "%Y-%m-%d"

    def __init__(self, sid: StationID | None = None) -> None:
        """
        :param station_id: e.g. `radiozurnal`.
        """
        self._station = None
        self._session = None

        # Fetch the station and pick the right one.
        if sid is not None:
            try:
                self._station = type(self).get_station(sid.lower())
            except IndexError:
                raise ValueError(f"The station with id `{sid}` does not exist.")

    def __enter__(self) -> Client:
        """
        Enter the context.
        """
        self._session = Session()
        return self

    def __exit__(self, *args) -> None:  # ?type
        """
        Exit the context.
        """
        # This is a remainder how to implement manager
        # see https://peps.python.org/pep-0343/.
        # exc_type, exc_value, traceback = *args
        self._session.close()

    @property
    def station(self) -> Station | None:
        """
        Get the current station.
        """
        return self._station

    @station.setter
    def station(self, sid: StationID) -> None:
        """
        Set the current station.
        """
        try:  # Fetch the station and pick the right one.
            self._station = type(self).get_station(sid.lower())
        except IndexError:
            raise ValueError(f"The station with id `{sid}` does not exist.")

    @classmethod
    def make(cls) -> Client:
        """
        Make the client instance (factory method).
        """
        return NotImplemented

    @classmethod
    def get_stations(cls) -> tuple[Station, ...]:
        """
        Fetch the available stations.

        Examples:
            >>> Client.get_stations()
        """
        data = get(f"{cls.__url__}/meta/stations.json").json()["data"]

        return tuple(
            [
                Station(
                    id=item["id"],
                    name=item["name"],
                    domain=item["domain"],
                    slogan=item["longdescription"]["slogan"],
                    description=item["description"],
                    services=item["services"],
                )
                for item in data
            ]
        )

    @classmethod
    def get_station(cls, sid: str) -> Station | None:
        """
        Fetch the available station with the given station id (`sid`).

        :param sid: The station id.
        :return: The sequence of stations.
        """
        # Fetch the station and pick the right one.
        try:
            return tuple(filter(lambda x: x.id == sid, cls.get_stations()))[0]
        except IndexError:
            raise ValueError(f"The station with id `{id}` does not exist.")

    def get_any_schedule(
        self,
        since: dt.date | str,
        till: dt.date | str = dt.datetime.now(),
        time: tuple[dt.time, dt.time] = (dt.time.min, dt.time.max),
    ) -> tuple[Schedule, ...]:
        """
        Fetch the avalaible schedules for the given date range.
        """
        if self.station is None:
            raise ValueError("Set the station property!")

        since, till = convert_date(since), convert_date(till)

        # Get all days between since and till.
        dates = [since + dt.timedelta(days=i) for i in range((till - since).days + 1)]

        return tuple(sorted(self.get_day_schedule(date, time) for date in dates))

    def get_day_schedule(
        self,
        date: dt.date | str = dt.datetime.now(),
        time: tuple[dt.time, dt.time] = (dt.time.min, dt.time.max),
    ) -> Schedule:
        """
        Fetch the availaible schedule for the given date.

        :param date: The schedule date.
        :param time: The schedule time range (since, till).
        :return: The schedule for the given day.

        Examples:
            >>> import datetime as dt
            >>> get_day_schedule(date = dt.datetime.now())
        """

        if self.station is None:
            raise ValueError("Set the station property!")

        date = convert_date(date)

        try:
            data = get(
                f"{type(self).__url__}/schedule/day/{date.year:04d}/{date.month:02d}/{date.day:02d}/{self.station.id}.json"
            ).json()["data"]
        except Exception as ex:
            logging.error(ex)
            raise ex

        shows = []

        since, till = None, None
        for item in data:
            since, till = (
                dt.datetime.fromisoformat(item["since"]),
                dt.datetime.fromisoformat(item["till"]),
            )
            # Check if since is in time range.
            if not is_time_between(
                time[0], time[1], dt.datetime.fromisoformat(item["since"]).time()
            ):
                continue

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
                    date=since.date(),
                    since=since.time(),
                    till=till.time(),
                    moderators=tuple(
                        Person(p["id"], p["name"]) for p in item["persons"]
                    ),
                    repetition=item["repetition"],
                )
            )

        date = date.date() if isinstance(date, dt.datetime) else date

        return Schedule(date=date, time=time, station=self.station, shows=tuple(shows))

    def get_week_schedule(
        self,
        date: dt.date | str = dt.datetime.now(),
        time: tuple[dt.time, dt.time] = (dt.time.min, dt.time.max),
    ) -> tuple[Schedule, ...]:
        """
        Fetch the availaible schedules for the given week.

        :param date: The schedule week date (any).
        :param time: The schedule time range (since, till).
        :return The sequence of schedules for the given week sorted by date.

        Examples:
            >>> import datetime as dt
            >>> get_week_schedule(date = dt.datetime.now())
        """
        if self.station is None:
            raise ValueError("Set the station property!")

        date = convert_date(date)

        # Get all days of the week.
        dates = (
            date + dt.timedelta(days=i)
            for i in range(0 - date.weekday(), 7 - date.weekday())
        )

        return tuple(sorted(self.get_day_schedule(date, time) for date in dates))

    def get_month_schedule(
        self,
        date: dt.date | str = dt.datetime.now(),
        time: tuple[dt.time, dt.time] = (dt.time.min, dt.time.max),
    ) -> tuple[Schedule, ...]:
        """
        Fetch the availaible schedules for the given month.

        :param date: The schedule month date (any).
        :param time: The schedule time range (since, till).
        :return The sequence of schedules for the given week sorted by date.

        Examples:
            >>> import datetime as dt
            >>> get_month_schedule(date = dt.datetime.now())
        """
        if self.station is None:
            raise ValueError("Set the station property!")

        date = convert_date(date)

        # Get all days of the month.
        nb_days = monthrange(date.year, date.month)[1]
        dates = (dt.date(date.year, date.month, day) for day in range(1, nb_days + 1))

        return tuple(sorted(self.get_day_schedule(date, time) for date in dates))

    def get_playlist(self, date: dt.date | str = dt.datetime.now()) -> object:
        """
        Fetch the playlist for Radio Wave station.
        """
        if date is None:
            raise AssertionError
        return NotImplemented
