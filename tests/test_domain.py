# -*- coding: utf-8 -*-

"""
Contains tests for domain model.
"""

import datetime as dt
import sched

import pytest

from cro.schedule import Schedule, Station


@pytest.mark.domain
def test_that_schedule_is_sortable():
    lhs = Schedule(
        date=dt.date(2022, 12, 1),
        shows=(),
        station=Station(
            id=1, name="Fake", domain="_", slogan="_", description="_", services=()
        ),
    )
    rhs = Schedule(
        date=dt.date(2022, 11, 1),
        shows=(),
        station=Station(
            id=1, name="Fake", domain="_", slogan="_", description="_", services=()
        ),
    )
    first, second = sorted((lhs, rhs))
    assert (first, second) == (rhs, lhs)


@pytest.mark.domain
def test_that_schedule_is_not_subsest():
    schedule = Schedule(
        date=dt.date(2022, 12, 1),
        shows=(),
        time=(dt.time.min, dt.time.max),
        station=Station(
            id=1, name="Fake", domain="_", slogan="_", description="_", services=()
        ),
    )
    assert not schedule.is_subset()
