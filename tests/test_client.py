# -*- coding: utf-8 -*-

"""
Contains tests for REST client.
"""

import pytest

from cro.schedule import Client


@pytest.fixture
def client():
    return Client("plus")


def test_that_stations_are_retrieved(client):
    result = client.get_stations()
    assert len(result) > 0


def test_that_day_schedule_is_retrieved(client):
    result = client.get_day_schedule()
    assert len(result.shows) > 0


def test_that_week_schedule_is_retrieved(client):
    result = client.get_week_schedule()
    assert len(result) == 7


# def test_that_month_schedule_is_retrieved(client):
#     result = client.get_month_schedule()
#     assert len(result.shows) > 0
