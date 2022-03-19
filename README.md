# Rozhlas Schedule

_Python HTTP REST API client for Czech Radio broadcast day schedule._

## Features

- [x] Získej program pro daný den a všechny stanice.
- [x] Získej program pro daný den a vybranou stanici.
- [ ] Získej program pro daný den a daný rozsah hodin např.
  - [ ] program od/do 12:00 (PM)
  - [ ] program od 06:00 do 12:00 (PM)
- [ ] Umožni export do `pandas.DataFrame`
- [ ] Program by měl uchovávat atributy `date: Date` a `station: String | Station`.
- [ ] Program by měl být iterátor, který krokuje po jednotlivých pořadech.
- [ ] Pořad by měl uchovávvat atributy, `id`, `since Date`, `till: Date`, `title: String`, `description: String`, dále moderátor a počet osob?
- [ ] Vytvoři schéma databáze pro ukládání programu, možnost napojení na přepisy.
- [ ] Vytvoř webvou apliakci pro prohlížení uložených programů.
- [ ] Získej konkrétní pořad podle zadaného času.
- [x] Získej seznam stanic.

## Usage

Data jsou dostupná mnoho let do historie a cca 14 dnů do budoucnosti.

```python
from cro.schedule import Client

client = Client('plus')

schedule: Schedule = client.get_schedule()        # Fetch the available schedule for current date.
stations: tuple(Station) = client.get_stations()  # Fetch the available stations.
```

## Install

__1. Naklonuj projekt lokálně a přesuň se do adresáře.__

    git clone https://github.com/czech-radio/cro.schedule.git
    cd cro.schedule

Vytvoř virtuální prostředí v adresáři projektu. Níže uvedený příkaz je platný pro Windows. S instalací Pythonu se do cesty vloží (zaváděcí) program `py.exe`, který lze použít pro spoustění různých verzí Python interpreteru. Zde explicitně říkáme: Zavolej interpretr Pythonu verze 3.10 (doporučené, používáme nejnovější verzi) a spusť zabudovaný modul `venv` (viz parameter `-m venv`) jako program s parametrem `.venv`. Ten vytvoří adresář `.venv`, do kterého se nakopíruje interpretr Pythonu s potřebnými balíky (knihovnami).

    py -3.10 -m venv .venv

__2. Aktivujeme virtuální prostředí tzn., že všechny instalace a spouštění interpreteru budou probíhat v adresáři `.venv`.__

__Windows__

    .\.venv\Scripts\activate

__UNIX__

    source ./venv/bin/activate

Měli bychom vidět podobný prefix s názvem `(.venv)` v terminálu, který ukazuje, že máme aktivní virtuální prostředí daného jména.

    (.venv) $ cro.schedule>

Jako jméno jsme mohli zvolit cokoliv, ale `.venv` je standardem (je např. uveden i v souboru `.gitignore`, protože ho rozhodně nechceme přidávat do repozitáře).

__3. Nainstalujeme si projekt (balík).__

Instalace balíku v produkčním režimu.

    pip install -U .

Instalace balíku ve vývojovém režimu.

    pip install -U -e .[test,docs,lint]

Nyní můžeme s balíkem pracovat v našich skriptech.

__4. Deakivace virtuálního prostředi se provede příkazem `deactivate` nebo stačí aktivivat jiné virtuáln prostředí.__

    deactivate

 Další informace k virtuálním prostředím naleznete [zde](https://docs.python.org/3/library/venv.html)

Pokud si chcem být jistí, že spouštíme Python interpretr ze správného prostředí použijeme

__Windows__

    where.exe python

    C:\Users\{name}\Projects\{project}\.venv\Scripts\python.exe
    ^^^ OK: Jako výchozí spouštíme z virtuálního prostředí a další v řadě jsou následující:

    C:\Users\{name}\AppData\Local\Programs\Python\Python310\python.exe
    C:\Users\{name}\AppData\Local\Programs\Python\Python39\python.exe
    C:\Users\{name}\AppData\Local\Microsoft\WindowsApps\python.exe

__UNIX__

    which python

## Testing

Pokud chceme spustit testy, použijeme následující příkaz.

    pytest -sv

## resources

- https://data.irozhlas.cz/opendata/
- https://cs.wikipedia.org/wiki/%C4%8Cesk%C3%BD_rozhlas
