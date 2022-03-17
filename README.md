# Rozhlas Schedule

_Python domain model and HTTP REST API client for "Program vysílání ČRo"._

## Instalace

__[1]__ Naklonuj projekt lokálně a přesuň se do adresáře.

    git clone https://github.com/czech-radio/cro.schedule.git
    cd cro.schedule

Vytvoř virtuální prostředí v adresáři projektu. Níže uvedený příkaz je platný pro Windows. S instalací Pythonu se do cesty vloží (zaváděcí) program `py.exe`, který lze použít pro spoustění různých verzí Python interpreteru. Zde explicitně říkáme: Zavolej interpretr Pythonu verze 3.10 (doporučené, používáme nejnovější verzi) a spusť zabudovaný modul `venv` (viz parameter `-m venv`) jako program s parametrem `.venv`. Ten vytvoří adresář `.venv`, do kterého se nakopíruje interpretr Pythonu s potřebnými balíky (knihovnami).

    py -3.10 -m venv .venv

__[2]__ Aktivujeme virtuální prostředí tzn., že všechny instalace a spouštění interpreteru budou probíhat v adresáři `.venv`.

    .\.venv\Scripts\activate

Měli bychom vidět podobný prefix s názvem `(.venv)` v terminálu, který ukazuje, že máme aktivní virtuální prostředí daného jména.

    (.venv) PS cro.schedule>

Jako jméno jsme mohli zvolit cokoliv, ale `.venv` je standardem (je např. uveden i v souboru `.gitignore`, protože ho rozhodně nechceme přidávat do repozitáře).

__[3]__ Nainstalujeme si projekt (balík).

    pip install .                    # production
    pip install -e .[test,docs,lint] # development (editable) mode

Nyní můžeme s balíkem pracovat v našich skriptech.

__[4]__ Deakivace virtuálního prostředi se provede příkazem `deactivate` nebo stačí aktivivat jiné virtuáln prostředí.

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

## Testování

Pokud chceme spustit testy, použijeme následující příkaz.

    pytest -sv

## Zadání

- [ ] Získej program pro daný den a všechny stanice.
- [ ] Získej program pro daný den a vybranou stanici.
- [ ] Získej program pro daný den a daný rozhah hodin např.
  - [ ] program od/do 12:00 (PM)
  - [ ] program od 06:00 do 12:00 (PM)
- [ ] Umožni export do `pandas.DataFrame`
- [ ] Program by měl uchovávat atributy `date: Date` a `station: String | Station`.
- [ ] Program by měl být iterátor, který krokuje po jednotlivých pořadech.
- [ ] Pořad by měl uchovávvat atributy, `id`, `since Date`, `till: Date`, `title: String`, `description: String`, dále moderátor a počet osob?
- [ ] Vytvoři schéma databáze pro ukládání programu, možnost napojení na přepisy.
- [ ] Vytvoř webvou apliakci pro prohlížení uložených programů.
- [ ] Získej konkrétní pořad podle zadaného času.


Návrh na podobu _flat_ (_tidy_) výstupu programu.

|id|station|date|since|till|title|description|
|--|-------|----|-----|----|-----|-----------|
| | | | | | | |
| | | | | | | |
| | | | | | | |

TODO ^^^ Doplnit příklady řádků.


## Program vysílání ČRo

Data jsou dostupná mnoho let do historie a cca 14 dnů do budoucnosti.

```python
from cro.schedule import Client
```

### Aktuální den a všechny stanice

```python
client = Client()
result = client.schedule()
```
__Endpoint__
```
https://api.rozhlas.cz/data/v2/schedule/day.json
```

### Konkrétní den a všechny stanice

```python
client = Client()
result = client.get_schedule(date = date(2022, 12, 1))
```
__Endpoint__
```
https://api.rozhlas.cz/data/v2/schedule/day/[YYYY]/[MM]/[DD].json
např. https://api.rozhlas.cz/data/v2/schedule/day/2019/09/01.json
```

### Aktuální den a konkrétní stanice

```python
client = Client(station='plus')
result = client.get_schedule()
```
__Endpoint__
```
https://api.rozhlas.cz/data/v2/schedule/day/[STATION_ID].json
např. https://api.rozhlas.cz/data/v2/schedule/day/plus.json
```

### Konkrétní den a konkrétní stanici

```python

from datetime import date

client = Client('plus')
result = client.get_schedule(date = date(2021, 12, 31)
```
__Endpoint__
```
https://api.rozhlas.cz/data/v2/schedule/day/[YYYY]/[MM]/[DD]/[STATION_ID].json
např. https://api.rozhlas.cz/data/v2/schedule/day/2019/09/01/plus.json
```

### Seznam stanic a jejich zkratek

```python

result = Client.get_stations()
```
__Endpoint__
```
https://api.rozhlas.cz/data/v2/meta/stations.json
```

## Popis položek JSON objektu

### Schedule

- `station` textové ID stanice (číselník viz https://api.rozhlas.cz/data/v2/meta/stations.json )
- `id` NEunikátní identifikátor převzatý z interního systému, ve kterém se plánuje vysílání; položka má vždy nějakou hodnotu
- `title` název pořadu; položka má vždy nějakou hodnotu
- `description` - popis pořadu; položka může být prázdná
- `since` - začátek vysílání pořadu; položka má vždy nějakou hodnotu
- `till` - konec vysílání pořadu; položka má vždy nějakou hodnotu
- `type` - nedokumentováno
- `edition` - pokud pro pořad existuje tzv. "webová vizitka", položka obsahuje objekt s příslušnými informacemi (např asset - vizuál pořadu); položka ovšem může být prázdná, vizitky totiž zatím neexistují pro všechny pořady
- `persons` pole objektů moderátorů pořadu (tzv. osoby), kterých může být 0-N (obsahuje kromě jiného také asset - fotografii moderátora); položka může být prázdná, protože ne každý pořad někdo moderuje a také ne pro všechny osoby máme k dispozici fotografie

### Stations

...

## Zdroje

- https://data.irozhlas.cz/opendata/
- https://cs.wikipedia.org/wiki/%C4%8Cesk%C3%BD_rozhlas
