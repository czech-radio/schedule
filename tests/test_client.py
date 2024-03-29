"""
Contains tests for REST client.

They are in fact the integration tests because we call the external REST service.
They can fail with connection or timeout issue. Keep it in mind!
"""

from datetime import date, time

import pytest

from cro.schedule import Client


@pytest.fixture
def client():
    _client = Client(sid="plus")
    assert _client.station is not None
    return _client


# Retrieve station(s)


@pytest.mark.client
def test_that_stations_are_retrieved(client):
    result = client.get_stations()
    assert len(result) > 0


# Retrieve schedule(s)


@pytest.mark.client
def test_that_day_schedule_is_retrieved(client):
    result = client.get_day_schedule(date=date(2022, 1, 1))
    assert len(result.shows) > 0


@pytest.mark.client
def test_that_day_schedule_works_with_date_isoformat(client):
    result = client.get_day_schedule(date="2022-01-31")
    assert len(result.shows) > 0


@pytest.mark.client
def test_that_week_schedule_are_retrieved(client):
    result = client.get_week_schedules(date=date(2022, 1, 1))
    assert len(result) == 7


@pytest.mark.client
def test_that_week_schedules_are_sorted(client):
    result = client.get_week_schedules(date=date(2022, 1, 3))
    for _ in result:
        assert result[0] <= result[-1]


@pytest.mark.client
def test_that_any_schedule_are_retrieved(client):
    result = client.get_any_schedules(since=date(2022, 1, 1), till=date(2022, 1, 15))
    assert len(result) == 15


@pytest.mark.client
def test_that_month_schedules_are_retrieved(client):
    result = client.get_month_schedules(date=date(2022, 1, 1))
    assert len(result) == 31


@pytest.mark.client
def test_that_month_schedules_are_sorted(client):
    result = client.get_month_schedules(date=date(2022, 1, 1))
    for _ in result:
        assert result[0] <= result[-1]


# Make subset


@pytest.mark.client
def test_that_day_schedule_subset_is_retrieved(client):
    result = client.get_day_schedule(
        date=date(2022, 1, 1), time=[time(8, 0, 0), time(11, 0, 0)]
    )
    assert result.is_subset()
    assert len(result.shows) > 0
