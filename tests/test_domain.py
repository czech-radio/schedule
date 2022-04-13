# -*- coding: utf-8 -*-

"""
Contains tests for domain model.
"""

import datetime as dt
from unicodedata import name

import pytest

from cro.schedule import Schedule, Station, Show


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


@pytest.mark.skip
@pytest.mark.domain
def test_that_schedule_show_time_filtering_works():
    assert False


@pytest.mark.skip
@pytest.mark.domain
def test_that_schedule_show_title_filtering_works():
    assert False


@pytest.mark.domain
def test_that_schedule_is_subset():
    schedule = Schedule(
        date=dt.date(2022, 12, 1),
        shows=(
            Show(
                id=1,
                kind="k1",
                title="t1",
                station=Station(
                    id=1,
                    name="Fake",
                    domain="_",
                    slogan="_",
                    description="_",
                    services=(),
                ),
                description="d1",
                since=dt.datetime(2022, 12, 1, 6, 0, 0),
                till=dt.datetime(2022, 12, 1, 7, 0, 0),
                repetition=False,
                persons=tuple([]),
            ),
            Show(
                id=2,
                kind="k2",
                title="t2",
                station=Station(
                    id=1,
                    name="Fake",
                    domain="_",
                    slogan="_",
                    description="_",
                    services=(),
                ),
                description="d2",
                since=dt.datetime(2022, 12, 1, 7, 0, 0),
                till=dt.datetime(2022, 12, 1, 8, 0, 0),
                repetition=False,
                persons=tuple([]),
            ),
        ),
        station=Station(
            id=1, name="Fake", domain="_", slogan="_", description="_", services=()
        ),
    )

    schedule_subset = schedule.as_subset(since="06:00:00", till="06:30:00")

    assert schedule_subset.is_subset()
    assert len(schedule.shows) == 2
    assert len(schedule_subset.shows) == 1
