# 𝖈𝖗𝖔.𝖘𝖈𝖍𝖊𝖉𝖚𝖑𝖊-𝖈𝖑𝖎𝖊𝖓𝖙

[![build: tests](https://github.com/czech-radio/cro.schedule/actions/workflows/main.yml/badge.svg)](https://github.com/czech-radio/cro.schedule/actions/workflows/main.yml)
[![style: black](https://img.shields.io/badge/style-black-000000.svg)](https://github.com/psf/black)
[![quality: bugs](https://sonarcloud.io/api/project_badges/measure?project=czech-radio_cro.schedule&metric=bugs)](https://sonarcloud.io/dashboard?id=czech-radio_cro.schedule)
[![quality: code smells](https://sonarcloud.io/api/project_badges/measure?project=czech-radio_cro.schedule&metric=code_smells)](https://sonarcloud.io/dashboard?id=czech-radio_cro.schedule)
[![quality: reliability](https://sonarcloud.io/api/project_badges/measure?project=czech-radio_cro.schedule&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=czech-radio_cro.schedule)

- Status: developed (maintained)
- Version: 0.13.0-alpha (latest)
- Release: https://github.com/czech-radio/cro.schedule/releases/
- Website: https://czech-radio.github.io/cro.schedule/.

:star: Star us on GitHub — it motivates us!

## Purpose

Python library to work with Czech Radio schedules and playlists.

## Features

- [x] Get the list of available stations.
- [x] Get the schedule for the given station and day.
- [x] Get the schedule for the given station and week.
- [x] Get the schedule for the given station and month.
- [x] Get the schedule for the given station, period and time.
- [ ] Get the playlist for supported stations (only Radio Wave).
- [x] Convert schedule to `pandas.DataFrame`.

## Installation

**Prerequisites**

* We assume that you use at least Python 3.9.
* We assume that you use the virtual environment.

One can install package from the GitHub repository.

```
pip install git+https://github.com/czech-radio/cro.schedule.git
```

## Usage

Data are available many years to the past and circa 14 days to the future.

```python
import datetime as dt

from cro.schedule import Client
```
## Use cases

#### Fetch the available stations

```python
stations: tuple(Station) = Client.get_stations()
```

#### Create the client instance

```python
client = Client(sid = 'plus')
```

#### Fetch the available schedule for the given day

```python
schedule: Schedule = client.get_day_schedule() # current day
schedule: Schedule = client.get_day_schedule(date = '2022-01-31')
schedule: Schedule = client.get_day_schedule(date = dt.date(2022, 1, 31))
```

#### Fetch the available schedule for the given week

```python
schedule: Schedule = client.get_week_schedule() # current week
schedule: Schedule = client.get_week_schedule(date = '2022-01-31')
schedule: Schedule = client.get_week_schedule(date = dt.date(2022, 1, 31))
```

#### Fetch the available schedule for the given month

```python
schedule: Schedule = client.get_month_schedule() # current month
schedule: Schedule = client.get_month_schedule(date = '2022-01-31')
schedule: Schedule = client.get_month_schedule(date = dt.date(2022, 1, 31))
```

#### Convert to `pandas.DataFrame`

```python
df = schedule.to_table()
df.head(5)
```

<table>  <thead>  <tr>      <th></th>      <th>id</th>      <th>kind</th>      <th>title</th>      <th>station</th>      <th>description</th>      <th>since</th>      <th>till</th>      <th>duration</th>      <th>persons</th>      <th>repetition</th>    </tr>  </thead>  <tbody>    <tr>      <th>0</th>      <td>17750161</td>      <td>zpr</td>      <td>Zprávy</td>      <td>radiozurnal</td>      <td>Zpravodajství z Česka i ze světa. Sport, Zelená vlna a předpověď počasí. O dopravní situaci informujte na bezplatné lince 800 553 553.</td>      <td>2022-03-22 00:00:00</td>      <td>2022-03-22 00:09:00</td>      <td>00:09:00</td>      <td>None</td>      <td>False</td>    </tr>    <tr>      <th>1</th>      <td>17750164</td>      <td>pub</td>      <td>Dvacet minut Radiožurnálu</td>      <td>radiozurnal</td>      <td>Hostem je Josef Středula, předseda Českomoravské komory odborových svazů. V Česku se už zaregistrovalo přes dvě stě tisíc uprchlíků z Ukrajiny. Jak jejich příchod zasáhne sociální systém a pracovní trh? Je vláda na migrační vlnu připravena? Moderuje Vladimír Kroc. (repríza)</td>      <td>2022-03-22 00:10:00</td>      <td>2022-03-22 00:30:00</td>      <td>00:20:00</td>      <td>({\'id\': 5004021, \'name\': \'Vladimír Kroc\'},)</td>      <td>True</td>    </tr>    <tr>      <th>2</th>      <td>17750165</td>      <td>zpr</td>      <td>Zprávy</td>      <td>radiozurnal</td>      <td>Z domova i ze světa. Sport, Zelená vlna a počasí. O dopravní situaci informujte na bezplatné lince 800 553 553.</td>      <td>2022-03-22 00:30:00</td>      <td>2022-03-22 00:32:00</td>      <td>00:02:00</td>      <td>None</td>      <td>False</td>    </tr>    <tr>      <th>3</th>      <td>17750168</td>      <td>mag</td>      <td>Noční Radiožurnál</td>      <td>radiozurnal</td>      <td>Aktuální reportáže a nejrychlejší zpravodajství. Moderuje Petr Zajíček.</td>      <td>2022-03-22 00:33:00</td>      <td>2022-03-22 01:00:00</td>      <td>00:27:00</td>      <td>None</td>      <td>False</td>    </tr>    <tr>      <th>4</th>      <td>17750169</td>      <td>zpr</td>      <td>Zprávy</td>      <td>radiozurnal</td>      <td>Zpravodajství z Česka i ze světa. Sport, Zelená vlna a předpověď počasí. O dopravní situaci informujte na bezplatné lince 800 553 553.</td>      <td>2022-03-22 01:00:00</td>      <td>2022-03-22 01:04:00</td>      <td>00:04:00</td>      <td>None</td>      <td>False</td>    </tr>  </tbody></table>

#### Store schedule in Excel

```python
date: str = '2022-03-14'

data: list[Schedule] = []
for sid in ('plus', 'radiozurnal'):
    client.station = sid
    schedules = client.get_week_schedule(date)

    for schedule in schedules:
        print(schedule.date, schedule.station.name, len(schedule.shows))
        data.append(schedule.to_table())
        # Write single dataset to Excel.
        with pd.ExcelWriter(f"../data/sheet/Schedule_{schedule.station.name}_{schedule.date}.xlsx") as writer:
            data[-1].to_excel(writer)

# Write concatenated datasets to Excel.
with pd.ExcelWriter(f"../data/sheet/Schedule_{date}.xlsx") as writer:
    pd.concat(data).to_excel(writer)
```

See more examples in `docs/Examples.ipynb` and data outputs in `data` directory.

## Development

### Clone the project and move to the project folder

```
git clone https://github.com/czech-radio/cro.schedule.git
cd cro.schedule
```

### Create and activate the virtual environment

Vytvoř virtuální prostředí v adresáři projektu. Níže uvedený příkaz je platný pro Windows. S instalací Pythonu se do cesty vloží (zaváděcí) program `py.exe`, který lze použít pro spoustění různých verzí Python interpreteru. Zde explicitně říkáme: Zavolej interpretr Pythonu verze 3.10 (doporučené, používáme nejnovější verzi) a spusť zabudovaný modul `venv` (viz parameter `-m venv`) jako program s parametrem `.venv`. Ten vytvoří adresář `.venv`, do kterého se nakopíruje interpretr Pythonu s potřebnými balíky (knihovnami).

```
py -m venv --upgrade-deps --clear .venv
```

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

### Install the package in virtual environment

Instalace balíku v produkčním režimu.

```
pip install -U .
```

Instalace balíku ve vývojovém režimu.

```
pip install -U -e .[test,docs,lint]
```

Nyní můžeme s balíkem pracovat v našich skriptech.

### Deactivate the virtual environment

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

## Linting

    black .
    isort .

## Resources

- https://data.irozhlas.cz/opendata/
- https://cs.wikipedia.org/wiki/%C4%8Cesk%C3%BD_rozhlas
