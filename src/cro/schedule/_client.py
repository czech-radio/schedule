# -*- coding: utf-8 -*-

"""
Module contains HTTP REST API client.
"""

from enum import Enum
import datetime as dt
from calendar import monthrange
from typing import Optional, Union

from requests import get

from cro.schedule._domain import Station, Schedule
from cro.schedule._domain import Show, Person, Kind  # package protected


__all__ = tuple(["Client"])


def is_time_between(begin_time, end_time, check_time=None):
    """
    Determine if current time is within a specified range

    @author https://stackoverflow.com/users/48837/joe-holloway
    @see https://stackoverflow.com/a/10048290
    """
    # If check time is not given, default to current UTC time.
    check_time = check_time or dt.datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time


class Client:
    """
    The Czech Radio client to fetch schedules and stations metadata.
    """

    __URL__: str = f"https://api.rozhlas.cz/data/v2"

    def __init__(self, station_id: str):
        """
        :param station_id: e.g. `radiozurnal`.
        """
        try:  # Fetch the station and pick the right one.
            self._station = self.get_station(station_id.lower())
        except IndexError:
            raise ValueError(f"The station with id `{self.station_id}` does not exist.")

    @property
    def station(self) -> Station:
        """
        Get the current station.
        """
        return self._station

    @classmethod
    def get_stations(cls) -> tuple[Station]:
        """
        Fetch the available stations.

        Examples:
            >>> Client.get_stations()
        """
        data = get(f"{cls.__URL__}/meta/stations.json").json()["data"]
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
    def get_station(cls, id: str) -> Optional[Station]:
        """
        Fetch the available station with the given id.
        """
        try:  # Fetch the station and pick the right one.
            return tuple(filter(lambda x: x.id == id, cls.get_stations()))[0]
        except IndexError:
            # Should we aise ValueError(f"The station with id `{id}` does not exist.")?
            return None

    def get_day_schedule(
        self,
        date: Union[dt.date, str] = dt.datetime.now(),
        time: tuple[dt.time, dt.time] = (dt.time.min, dt.time.max),
    ) -> Schedule:
        """
        Fetch the availaible schedule for the given date.

        Examples:
            >>> import datetime as dt
            >>> get_day_schedule(date = dt.datetime.now())
        """

        date = (
            dt.datetime.strptime(date, "%Y-%m-%d").date()
            if isinstance(date, str)
            else date
        )

        data = get(
            f"{type(self).__URL__}/schedule/day/{date.year:04d}/{date.month:02d}/{date.day:02d}/{self.station.id}.json"
        ).json()["data"]

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
                    since=since,
                    till=till,
                    persons=tuple(
                        (Person(p["id"], p["name"]) for p in item["persons"])
                    ),
                    repetition=item["repetition"],
                )
            )

        date = date.date() if isinstance(date, dt.datetime) else date

        return Schedule(date=date, time=time, station=self.station, shows=shows)

    def get_week_schedule(
        self,
        date: dt.date | str = dt.datetime.now(),
        time: tuple[dt.time, dt.time] = (dt.time.min, dt.time.max),
    ) -> tuple[Schedule]:
        """
        Fetch the availaible schedules for the given week.

        :param date: Any date in the week

        Examples:
            >>> import datetime as dt
            >>> get_week_schedule(date = dt.datetime.now())
        """
        date = (
            dt.datetime.strptime(date, "%Y-%m-%d").date()
            if isinstance(date, str)
            else date
        )

        # Get all days of the week.
        dates = (
            date + dt.timedelta(days=i)
            for i in range(0 - date.weekday(), 7 - date.weekday())
        )

        return tuple(sorted((self.get_day_schedule(date, time) for date in dates)))

    def get_month_schedule(
        self,
        date: Union[dt.date, str] = dt.datetime.now(),
        time: tuple[dt.time, dt.time] = (dt.time.min, dt.time.max),
    ) -> tuple[Schedule]:
        """
        Fetch the availaible schedules for the given month.

        :param date: Any date in the month.

        :return The collection of schedules sorted by date.

        Examples:
            >>> import datetime as dt
            >>> get_month_schedule(date = dt.datetime.now())
        """
        date = (
            dt.datetime.strptime(date, "%Y-%m-%d").date()
            if isinstance(date, str)
            else date
        )

        # Get all days of the month.
        nb_days = monthrange(date.year, date.month)[1]
        dates = (dt.date(date.year, date.month, day) for day in range(1, nb_days + 1))

        return tuple(sorted((self.get_day_schedule(date, time) for date in dates)))

    def get_playlist(self, date: Union[dt.date, str] = dt.datetime.now()) -> object:
        """
        Fetch the playlist for Radio Wave station.
        """
        return NotImplemented
