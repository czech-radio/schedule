# -*- coding: utf-8 -*-

"""
Contains tests for REST client.
"""

from datetime import date

import pytest

from cro.schedule import Client


@pytest.fixture
def client():
    return Client("plus")


@pytest.mark.client
def test_that_stations_are_retrieved(client):
    result = client.get_stations()
    assert len(result) > 0


@pytest.mark.client
def test_that_day_schedule_is_retrieved(client):
    result = client.get_day_schedule(date=date(2022, 1, 1))
    assert len(result.shows) > 0


@pytest.mark.client
def test_that_week_schedule_are_retrieved(client):
    result = client.get_week_schedule(date=date(2022, 1, 1))
    assert len(result) == 7


@pytest.mark.client
def test_that_week_schedules_are_sorted(client):
    result = client.get_week_schedule(date=date(2022, 1, 1))
    assert result[0] < result[-1]


@pytest.mark.client
def test_that_month_schedules_are_retrieved(client):
    result = client.get_month_schedule(date=date(2022, 1, 1))
    assert len(result) == 31


@pytest.mark.client
def test_that_month_schedules_are_sorted(client):
    result = client.get_month_schedule(date=date(2022, 1, 1))
    assert result[0] < result[-1]
