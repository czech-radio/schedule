"""
Test the project as a package e.g. check the version, style etc.
"""

from cro.schedule import __version__


EXPECTED_PACKAGE_VERSION = "1.2.0"


def test_package_version():
    assert __version__ == EXPECTED_PACKAGE_VERSION


def test_package_readme_version():
    LINE_NUMBER = 135
    with open("./README.rst", encoding="utf8") as file:
        lines = file.readlines()
        version_line = lines[LINE_NUMBER - 1].split("-")[1]
        assert version_line.strip() == EXPECTED_PACKAGE_VERSION
