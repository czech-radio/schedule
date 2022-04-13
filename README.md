# mini-schedule-client

![Python](https://img.shields.io/badge/Language-Python-blue.svg)
[![build: tests](https://github.com/czech-radio/cro.schedule/actions/workflows/main.yml/badge.svg)](https://github.com/czech-radio/cro.schedule/actions/workflows/main.yml)
[![style: black](https://img.shields.io/badge/style-black-000000.svg)](https://github.com/psf/black)
[![quality: bugs](https://sonarcloud.io/api/project_badges/measure?project=czech-radio_cro.schedule&metric=bugs)](https://sonarcloud.io/dashboard?id=czech-radio_cro.schedule)
[![quality: code smells](https://sonarcloud.io/api/project_badges/measure?project=czech-radio_cro.schedule&metric=code_smells)](https://sonarcloud.io/dashboard?id=czech-radio_cro.schedule)
[![quality: reliability](https://sonarcloud.io/api/project_badges/measure?project=czech-radio_cro.schedule&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=czech-radio_cro.schedule)

- Status: developed (maintained)
- Version: 0.1.0-alpha (latest)
- Category: library, client
- Suppport: Python 3.9+, Windows, macOS, Ubuntu

## Purpose

Python library to work with Czech Radio schedules.

## Features

- [x] Get the list of available stations.
- [x] Get the schedule for the given station and day.
- [ ] Get the schedule for the given station, period and time.
- [x] Convert schedule to `pandas.DataFrame`.

## Installation


## Usage

```python
import datetime as dt

from cro.schedule import DaySchedule
```
### Use cases

#### Fetch the available stations

```python

stations = Broadcast()

```

#### Fetch the available schedule for a station on a given day

```python

schedule = DaySchedule("plus") # current day
schedule = DaySchedule("radiozurnal",date = '2022-01-31')
schedule = DaySchedule("wave",date = dt.date(2022, 1, 31))
```
#### Store schedule in Excel

Not implemented
