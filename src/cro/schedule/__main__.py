"""
The command line interface to download the schedules.
"""

import argparse
import sys

import pandas as pd

from cro.schedule import Client
from cro.schedule._shared import flatten as _flatten

__all__ = ("main",)


def main() -> None:
    # #########################################################################
    # Define options and flags.
    # #########################################################################

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
    parser.add_argument(
        "-f", "--format", required=False, help="The export file format (xls, csv)"
    )

    # #########################################################################
    # Parse arguments and check the values.
    # #########################################################################
    options = parser.parse_args()

    date: str = options.date
    period: str = options.period.upper()
    station_ids: list[str] = [s.strip() for s in options.stations.split(",")]
    output = options.output
    format = options.format

    # Pick the output format.
    match format:
        case None:
            format = "csv"
        case "csv" | "xls":
            format = format.lower()
        case _:
            print("The allowed format is ('csv', 'xls').")
            sys.exit(1)

    # #########################################################################
    # The main procedures.
    # #########################################################################
    client = Client()
    schedule_dfs: list[list[pd.DataFrame]] = []

    # -------------------------------------------------------------------------
    # Fetch the schedules.
    # -------------------------------------------------------------------------
    for station_id in station_ids:
        # Pick the station.
        try:
            client.station = client.get_station(station_id.lower())
        except:
            raise ValueError(
                f"The station with id `{station_id}` could not be fetched."
            )
        # Pick the period.
        match period:
            case "D":
                schedules = [
                    client.get_day_schedule(date=date),
                ]
            case "W":
                schedules = list(client.get_week_schedules(date=date))
            case "M":
                schedules = list(client.get_month_schedules(date=date))
            case _:
                raise ValueError(f"Unknown period {period}!")

        schedule_dfs.append([schedule.to_table() for schedule in schedules])

    print(
        (
            f"Fetched {len(schedules)} schedules for stations "
            f"{[station.title() for station in station_ids]} and "
            f"dates {[schedule.date.isoformat() for schedule in schedules]}."
        )
    )

    # -------------------------------------------------------------------------
    # Store the schedules.
    # -------------------------------------------------------------------------
    output_file_path = f"{output}/Schedule_{period}{date}"
    match format:
        case "csv":
            output_file_path = f"{output_file_path}.csv"
            pd.concat(_flatten(schedule_dfs)).to_csv(
                output_file_path, sep="\t", encoding="utf-8", index=False
            )
        case "xls":
            output_file_path = f"{output_file_path}.xlsx"
            with pd.ExcelWriter(output_file_path) as writer:
                pd.concat(_flatten(schedule_dfs)).to_excel(writer, index=False)

    print(f"Result saved to {output_file_path}")
