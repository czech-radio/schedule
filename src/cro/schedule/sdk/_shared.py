# -*- coding: utf-8 -*-


import datetime as dt
from typing import Optional, Union

__all__ = tuple(["convert_date", "convert_time"])


def convert_date(
    date: Union[dt.date, str], date_format="%Y-%m-%d"
) -> Optional[dt.date]:
    """
    Convert date from string to date object if needed.

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
    """
    return (
        dt.datetime.strptime(time, time_format).time()
        if isinstance(time, str)
        else time
    )
