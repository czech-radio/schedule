# -*- coding: utf-8 -*-

"""
Test the project as a package e.g. check the version, style etc.
"""

from cro.schedule import __version__


def test_that_readme_version_matches_package_version():
    EXPECTED_PACKAGE_VERSION = "1.2.0"
    with open("./README.md") as file:
        lines = file.readlines()
        version_line = lines[5].strip()[-15:-10]
        assert __version__ == EXPECTED_PACKAGE_VERSION
        assert version_line.strip() == EXPECTED_PACKAGE_VERSION
