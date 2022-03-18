# -*- coding: utf-8 -*-

import pytest

from cro.schedule import Client


@pytest.fixture
def client():
    return Client


def test_that_stations_are_retrieved(client):
    result = client.get_stations()
    assert len(result["data"]) > 0
