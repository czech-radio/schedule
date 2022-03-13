# -*- coding: utf-8 -*-


from requests import get
from datetime import datetime as dt
from enum import Enum


__all__ = tuple([
    "get_schedule",
    "get_stations",
])


__URL__ = "https://api.rozhlas.cz/data/v2"

class Stations(Enum):
    PLUS: "plus"
    RADIOZURNAL: "radiozurnal"


def get_stations() -> dict:
    """
    Get a available stations.

    Examples:
        >>> get_stations()
    """
    return get(f"{__URL__}/meta/stations.json").json()


def get_schedule(date: dt.date = dt.now(), station: str=None) -> dict:
    """
    Get a schedule for the given day and station.

    Examples:
        >>> get_schedule(dt.now())

    """
    if station is None:
        url = f"{__URL__}/schedule/day/{date.year:04d}/{date.month:02d}/{date.day:02d}.json"
    else:
        url = f"{__URL__}/schedule/day/{date.year:04d}/{date.month:02d}/{date.day:02d}/{station}.json"

    return get(url).json()


if __name__ == "__main__":

    result = get_schedule()
    print(result)

    # result = get_stations()
    print(type(result))