# Rozhlas Schedule 

_Python domain model and HTTP REST API client for "Program vysílání ČRo"._

## Zadání

- [ ] Získej program pro daný den a všechny stanice.
- [ ] Získej program pro daný den a vybranou stanici.
- [ ] Získej program pro daný den a daný rozhah hodin např.
  - [ ] program od/do 12:00 (PM)
  - [ ] program od 06:00 do 12:00 (PM)
- [ ] Umožni export do `pandas.DataFrame`
- [ ] Program by měl uchovávat atributy `date: Date` a `station: String | Station`.
- [ ] Program by měl být iterátor, který krokuje po jednotlivých pořadech.
- [ ] Pořad by měl uchovávvat atributy `from: Date`, `till: Date`, `title: String`, dále moderátor a počet osob?
- [ ] Vytvoři schéma databáze pro ukládání programu, možnost napojení na přepisy.

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
result = client.schedule(date = date(2022, 12, 1))
```
__Endpoint__
```
https://api.rozhlas.cz/data/v2/schedule/day/[YYYY]/[MM]/[DD].json
např. https://api.rozhlas.cz/data/v2/schedule/day/2019/09/01.json
```

### Aktuální den a konkrétní stanice

```python
client = Client()
result = client.schedule(station = 'plus')
```
__Endpoint__
```
https://api.rozhlas.cz/data/v2/schedule/day/[STATION_ID].json
např. https://api.rozhlas.cz/data/v2/schedule/day/plus.json
```

### Konkrétní den a konkrétní stanici

```python

from datetime import date

client = Client()
result = client.schedule(date = date(2021, 12, 31, station = 'plus')
```
__Endpoint__
```
https://api.rozhlas.cz/data/v2/schedule/day/[YYYY]/[MM]/[DD]/[STATION_ID].json
např. https://api.rozhlas.cz/data/v2/schedule/day/2019/09/01/plus.json
```

### Seznam stanic a jejich zkratek

```python

client = Client()
result = client.stations()
```
__Endpoint__
```
https://api.rozhlas.cz/data/v2/meta/stations.json
```

## Popis položek JSON objektu

### Client

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
