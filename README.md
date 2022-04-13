# 𝖈𝖗𝖔-𝖘𝖈𝖍𝖊𝖉𝖚𝖑𝖊-𝖘𝖉𝖐

**Python library to work with Rozhlas schedule REST service.**

![Python](https://img.shields.io/badge/language-Python-blue.svg)
![package-version](https://img.shields.io/badge/version-0.15.0-blue)
[![build: tests](https://github.com/czech-radio/cro.schedule/actions/workflows/main.yml/badge.svg)](https://github.com/czech-radio/cro.schedule/actions/workflows/main.yml)
[![style: black](https://img.shields.io/badge/style-black-000000.svg)](https://github.com/psf/black)
[![quality: bugs](https://sonarcloud.io/api/project_badges/measure?project=czech-radio_cro.schedule&metric=bugs)](https://sonarcloud.io/dashboard?id=czech-radio_cro.schedule)
[![quality: code smells](https://sonarcloud.io/api/project_badges/measure?project=czech-radio_cro.schedule&metric=code_smells)](https://sonarcloud.io/dashboard?id=czech-radio_cro.schedule)
[![quality: reliability](https://sonarcloud.io/api/project_badges/measure?project=czech-radio_cro.schedule&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=czech-radio_cro.schedule)

- Status: developed (maintained)
- Version: 0.13.0-alpha (latest)
- Release: https://github.com/czech-radio/cro.schedule/releases/
- Examples: https://github.com/czech-radio/cro-schedule-sdk/tree/main/docs/source/notebooks
- Website: https://czech-radio.github.io/cro.schedule/.
- Category: library, client, SDK
- Suppport: Python 3.9+, Windows, macOS, Ubuntu

:star: Star us on GitHub — it motivates us!

## Purpose

Python library to work with Czech Radio schedules and playlists.

## Install

**Prerequisites**

* We assume that you use at least Python 3.9.
* We assume that you use the virtual environment.

Install the package latest version from the GitHub repository.

```
pip install git+https://github.com/czech-radio/cro-schedule-client.git
```

## Features & Usage

Data are available many years to the past and circa 14 days to the future.

- [x] Get the list of available stations [recipe](https://github.com/czech-radio/cro-schedule-sdk/blob/main/docs/source/notebooks/Recipe_Get_Available_Stations.ipynb).
- [x] Get the schedule for the given station and day [recipe].
- [x] Get the schedule for the given station and week [recipe].
- [x] Get the schedule for the given station and month [recipe].
- [x] Get the schedule for the given station, period and time [recipe].
- [ ] Get the playlist for supported stations (only Radio Wave) [recipe].
- [x] Convert schedule to `pandas.DataFrame` [recipe].

Both `date = '2022-01-31'` and `dt.date(2022, 1, 31)` are valid date formats.

See more examples in `docs/notebooks` and data outputs in `data` directory.

## Contribute

See the documentn [here]().github\CONTRIBUTING.md)

## References

- https://data.irozhlas.cz/opendata/
- https://cs.wikipedia.org/wiki/%C4%8Cesk%C3%BD_rozhlas
