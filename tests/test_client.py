# -*- coding: utf-8 -*-

import pytest

from cro.schedule import Client


@pytest.fixture
def client():
    return Client('plus')


def test_that_schedule_is_retrieved(client):
    result = client.get_schedule()
    assert len(result.shows) > 0


def test_that_stations_are_retrieved(client):
    result = client.get_stations()
    assert len(result) > 0
