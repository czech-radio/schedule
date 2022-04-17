# -*- coding: utf-8 -*-

"""
Contains tests for domain model.
"""

import datetime as dt

import pytest

from cro.schedule.sdk import Schedule, Show, Station


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


@pytest.fixture
def lhs_fake_show():
    return Show(
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
        moderators=tuple([]),
    )


@pytest.fixture
def rhs_fake_show():
    return Show(
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
        moderators=tuple([]),
    )


@pytest.mark.domain
def test_that_schedule_show_time_filtering_works(lhs_fake_show, rhs_fake_show):
    schedule = Schedule(
        date=dt.date(2022, 12, 1),
        shows=[lhs_fake_show, rhs_fake_show],
        station=Station(
            id=1, name="Fake", domain="_", slogan="_", description="_", services=()
        ),
    )
    shows = schedule.shows_by_time("06:00:00", "07:45:00")

    assert len(shows) == 1  # filtered
    assert len(schedule.shows) == 2  # original


@pytest.mark.domain
def test_that_schedule_show_time_filtering_works(lhs_fake_show, rhs_fake_show):
    schedule = Schedule(
        date=dt.date(2022, 12, 1),
        shows=[lhs_fake_show, rhs_fake_show],
        station=Station(
            id=1, name="Fake", domain="_", slogan="_", description="_", services=()
        ),
    )
    shows = schedule.shows_by_title("t1")

    assert len(shows) == 1  # filtered
    assert len(schedule.shows) == 2  # original


@pytest.mark.domain
def test_that_schedule_is_subset(lhs_fake_show, rhs_fake_show):
    schedule = Schedule(
        date=dt.date(2022, 12, 1),
        shows=[lhs_fake_show, rhs_fake_show],
        station=Station(
            id=1, name="Fake", domain="_", slogan="_", description="_", services=()
        ),
    )

    schedule_subset = schedule.as_subset(since="06:00:00", till="07:30:00")

    assert schedule_subset.is_subset()
    assert len(schedule.shows) == 2
    assert len(schedule_subset.shows) == 1
