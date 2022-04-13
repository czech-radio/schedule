# -*- coding: utf-8 -*-

"""
The command line interface to download the schedules..
"""

import argparse


__all__ = tuple(["main"])


def main() -> None:
    parser = argparse.ArgumentParser("cro-schedule-cli")

    parser.add_argument("--station")
    parser.add_argument("--since")
    parser.add_argument("--till")
    parser.add_argument("--output")
    parser.add_argument("--format")

    # To be continued.

    print("--OK--")
