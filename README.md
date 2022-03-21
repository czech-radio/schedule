# Rozhlas Schedule

_Python client and domain model to work with Czech Radio broadcast schedule._


[![build](https://github.com/czech-radio/cro.schedule/actions/workflows/main.yml/badge.svg)](https://github.com/czech-radio/cro.schedule/actions/workflows/main.yml)
[![quality](https://sonarcloud.io/api/project_badges/measure?project=czech-radio_cro.schedule&metric=bugs)](https://sonarcloud.io/dashboard?id=czech-radio_cro.schedule)
[![quality](https://sonarcloud.io/api/project_badges/measure?project=czech-radio_cro.schedule&metric=code_smells)](https://sonarcloud.io/dashboard?id=czech-radio_cro.schedule)
[![quality](https://sonarcloud.io/api/project_badges/measure?project=czech-radio_cro.schedule&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=czech-radio_cro.schedule)

## Features

- [x] Get the list of available stations.
- [x] Get the schedule for the given station and day.
- [x] Get the schedule for the given station and week.
- [x] Get the schedule for the given station and month.
- [x] Get the schedule for the given station and period.
- [x] Get the schedule shows between given time range 06--12:00.
- [ ] Convert schedule to `pandas.DataFrame`.
- [ ] Manage schedules via flask application.

## Usage

Data are available many years to the past and circa 14 days to the future.

```python

import datetime as dt

from cro.schedule import Client

# Fetch the available stations.
stations: tuple(Station) = Client.get_stations()

client = Client('plus')

# Fetch the available schedule for the given day.
schedule: Schedule = client.get_day_schedule(date = dt.date(2022, 1, 31))

# Fetch the available schedule for the given week.
schedule: Schedule = client.get_week_schedule(date = dt.date(2022, 1, 31))

# Fetch the available schedule for the given month.
schedule: Schedule = client.get_month_schedule(date = dt.date(2022, 1, 31))
```

See more examples in `docs/Examples.ipynb`.

## Install

Yuu can install package directly from GitHub repository.

```
pip install git+https://github.com/czech-radio/cro.schedule.git
```

__1. Clone the project and move to the project folder.__

    git clone https://github.com/czech-radio/cro.schedule.git
    cd cro.schedule

Vytvoř virtuální prostředí v adresáři projektu. Níže uvedený příkaz je platný pro Windows. S instalací Pythonu se do cesty vloží (zaváděcí) program `py.exe`, který lze použít pro spoustění různých verzí Python interpreteru. Zde explicitně říkáme: Zavolej interpretr Pythonu verze 3.10 (doporučené, používáme nejnovější verzi) a spusť zabudovaný modul `venv` (viz parameter `-m venv`) jako program s parametrem `.venv`. Ten vytvoří adresář `.venv`, do kterého se nakopíruje interpretr Pythonu s potřebnými balíky (knihovnami).

```
py -3.10 -m venv .venv
```

__2. Activate the virtual environment.__

__Windows__

```
.\.venv\Scripts\activate
```

__UNIX__

```
source ./venv/bin/activate
```

Měli bychom vidět podobný prefix s názvem `(.venv)` v terminálu, který ukazuje, že máme aktivní virtuální prostředí daného jména tzn., že všechny instalace balíků a spouštění interpreteru bude probíhat v adresáři `.venv`.

```
(.venv) $ cro.schedule>
```

Jako jméno jsme mohli zvolit cokoliv, ale `.venv` je standardem (je např. uveden i v souboru `.gitignore`, protože ho rozhodně nechceme přidávat do repozitáře).

__3. Install the package in active virtual environment.__

Instalace balíku v produkčním režimu.

```
pip install -U .
```

Instalace balíku ve vývojovém režimu.

```
pip install -U -e .[test,docs,lint]
```

Nyní můžeme s balíkem pracovat v našich skriptech.

__4. Deactivate the virtual environment.__

Provedeme příkazem `deactivate` nebo stačí aktivivat jiné virtuální prostředí.

```
deactivate
```

Další informace k virtuálním prostředím naleznete [zde](https://docs.python.org/3/library/venv.html)

Pokud si chcem být jistí, že spouštíme Python interpretr ze správného prostředí použijeme

__Windows__

```
where.exe python

C:\Users\{name}\Projects\{project}\.venv\Scripts\python.exe
^^^ OK: Jako výchozí spouštíme z virtuálního prostředí a další v řadě jsou následující:

C:\Users\{name}\AppData\Local\Programs\Python\Python310\python.exe
C:\Users\{name}\AppData\Local\Programs\Python\Python39\python.exe
C:\Users\{name}\AppData\Local\Microsoft\WindowsApps\python.exe
```

__UNIX__

```
which python
```

## Testing

Pokud chceme spustit testy, použijeme následující příkaz.

```
pytest -sv
pytest -sv -m domain
pytest -sv -m client
pytest -sv -m "not client"
```

## Resources

- https://data.irozhlas.cz/opendata/
- https://cs.wikipedia.org/wiki/%C4%8Cesk%C3%BD_rozhlas
