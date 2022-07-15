# -*- coding: utf-8 -*-

"""
Test the project as a package e.g. check the version, style etc.
"""

from cro.schedule.sdk import __version__


EXPECTED_PACKAGE_VERSION = "1.1.0"


def test_version():
    assert __version__ == EXPECTED_PACKAGE_VERSION


def test_readme_version():
    with open("./README.md", encoding="utf8") as file:
        lines = file.readlines()
        version_line = lines[5].strip()[-15:-10]
        assert version_line.strip() == EXPECTED_PACKAGE_VERSION
