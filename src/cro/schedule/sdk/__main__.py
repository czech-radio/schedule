# -*- coding: utf-8 -*-

"""
The command line interface to download the schedules.
"""

import argparse

import pandas as pd

from cro.schedule.sdk import Client

__all__ = tuple(["main"])


def main() -> None:
    parser = argparse.ArgumentParser("The `cro.schedule.sdk` command line interface.")

    parser.add_argument("-d", "--date", required=True, help="The date of period.")
    parser.add_argument(
        "-p",
        "--period",
        required=True,
        help="The period for the schedule e.g D, W, M, Y.",
    )
    parser.add_argument(
        "-s", "--stations", required=True, help="The station for the schedule."
    )
    parser.add_argument("-o", "--output", required=False)
    # parser.add_argument("--format")

    options = parser.parse_args()

    date: str = options.date
    period: str = options.period.upper()
    stations: list[str] = [s.strip() for s in options.stations.split(",")]
    output = options.output

    client = Client()

    schedule_dfs: list[pd.DataFrame] = []

    def flatten(t):
        return [item for sublist in t for item in sublist]

    for station in stations:
        client.station = station.lower()

        match period:
            case "D":
                schedules = tuple([client.get_day_schedule(date=date)])
            case "W":
                schedules = client.get_week_schedule(date=date)
            case "M":
                schedules = client.get_month_schedule(date=date)
            case _:
                print(f"Unknown period {period}!")

        schedule_dfs.append([schedule.to_table() for schedule in schedules])

    print(
        f"Fetched {len(schedules)} schedules for stations {[station.title() for station in stations]} and dates {[schedule.date.isoformat() for schedule in schedules]}."
    )
    # Store the result on disk.
    output_file_path = f"{output}/Schedule_{period}{date}.xlsx"
    with pd.ExcelWriter(output_file_path) as writer:
        pd.concat(flatten(schedule_dfs)).to_excel(writer)

    print(f"Result saved to {output_file_path}")
