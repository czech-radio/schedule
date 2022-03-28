# -*- coding: utf-8 -*-

"""
Test the project as a package e.g. check the version, style etc.
"""

from cro.schedule import __version__

def test_version():
    assert __version__ == "0.13.0"
