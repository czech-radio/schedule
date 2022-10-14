# -*- coding: utf-8 -*-


import datetime as dt
from typing import Optional, Union, Any


__all__ = tuple(["convert_date", "convert_time", "flatten"])


def convert_date(
    date: Union[dt.date, str], date_format="%Y-%m-%d"
) -> Optional[dt.date]:
    """
    Convert date from string to date object if needed.

    :param: The date object or string to convert.
    :return: The formated date.
    """
    return (
        dt.datetime.strptime(date, date_format).date()
        if isinstance(date, str)
        else date
    )


def convert_time(
    time: Union[dt.time, str], time_format="%H:%M:%S"
) -> Optional[dt.time]:
    """
    Convert date from string to date object if needed.

    :param time: The time object or string to convert.
    :return: The formated time.
    """
    return (
        dt.datetime.strptime(time, time_format).time()
        if isinstance(time, str)
        else time
    )


def flatten(lst: list[Any]) -> list[Any]:
    """
    The helper to flatten a list of lists.

    :param lst: The list to flatten.
    :return: The flat list.
    """
    return [item for sublst in lst for item in sublst]
