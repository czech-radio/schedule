# Rozhlas Schedule

_Python HTTP REST API client for Czech Radio broadcast day schedule._

## Features

- [x] Získej seznam dostupných stanic.
- [x] Získej program pro vybranou stanici a daný den.
- [x] Získej program pro vybranou stanici a daný týden.
- [x] Získej program pro vybranou stanici a daný měsíc.
- [x] Získej program pro daný den/týden/měsíc a daný rozsah hodin např.
  - [x] program od/do 12:00 (PM)
  - [x] program od 06:00 do 12:00 (PM)
- [ ] Umožni export do `pandas.DataFrame`
- [ ] Vytvoři schéma databáze pro ukládání programu, možnost napojení na přepisy.
- [ ] Vytvoř webvou aplikaci pro prohlížení uložených programů.
- [ ] Získej konkrétní pořad podle zadaného času.

## Usage

Data jsou dostupná mnoho let do historie a cca 14 dnů do budoucnosti.

```python
from cro.schedule import Client

client = Client('plus')

 # Fetch the available schedule for current date.
schedule: Schedule = client.get_day_schedule(date = datetime.now())

schedule: Schedule = client.get_week_schedule(date = datetime.now())

schedule: Schedule = client.get_month_schedule(date = datetime.now())

# Fetch the available stations.
stations: tuple(Station) = client.get_stations(date = datetime.now())
```

See more examples in `docs/Examples.ipynb`.

## Install

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
```

## Resources

- https://data.irozhlas.cz/opendata/
- https://cs.wikipedia.org/wiki/%C4%8Cesk%C3%BD_rozhlas
