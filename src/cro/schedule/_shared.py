import datetime as dt
from typing import Optional, Union, Any


__all__ = tuple(["convert_date", "convert_time", "flatten"])


def convert_date(date: Union[dt.date, str], date_format="%Y-%m-%d") -> dt.date:
    """
    Convert date from text with the given format to date object.

    :param: The date object or string to convert.
    :return: The formated date.
    :raises: ValuError: when given format is wrong.
    """
    if isinstance(date, str):
        return dt.datetime.strptime(date, date_format).date()
    return date


def convert_time(time: Union[dt.time, str], time_format="%H:%M:%S") -> dt.time:
    """
    Convert time from text with the given format to date object.

    :param time: The time object or string to convert.
    :return: The formated time.
    :raises: ValuError: when given format is wrong.
    """
    if isinstance(time, str):
        return dt.datetime.strptime(time, time_format).time()
    return time


def flatten(lst: list[Any]) -> list[Any]:
    """
    The helper to flatten a list of lists.

    :param lst: The list to flatten.
    :return: The flat list.
    """
    return [item for sublst in lst for item in sublst]
