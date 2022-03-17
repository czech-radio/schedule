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

__Endpoint__
```
https://api.rozhlas.cz/data/v2/schedule/day.json
```

```python
client = Client()
result = client.get_schedule()
```

### Konkrétní den a všechny stanice

__Endpoint__
```
https://api.rozhlas.cz/data/v2/schedule/day/[YYYY]/[MM]/[DD].json
např. https://api.rozhlas.cz/data/v2/schedule/day/2019/09/01.json
```

```python
client = Client()
result = client.get_schedule(date = date(2022, 12, 1))
```

### Aktuální den a konkrétní stanice

__Endpoint__
```
https://api.rozhlas.cz/data/v2/schedule/day/[STATION_ID].json
např. https://api.rozhlas.cz/data/v2/schedule/day/plus.json
```

```python
client = Client(station='plus')
result = client.get_schedule()
```

### Konkrétní den a konkrétní stanici

__Endpoint__
```
https://api.rozhlas.cz/data/v2/schedule/day/[YYYY]/[MM]/[DD]/[STATION_ID].json
např. https://api.rozhlas.cz/data/v2/schedule/day/2019/09/01/plus.json
```

```python

from datetime import date

client = Client('plus')
result = client.get_schedule(date = date(2021, 12, 31)
```

### Seznam stanic

__Endpoint__
```
https://api.rozhlas.cz/data/v2/meta/stations.json
```

```python

result = Client.get_stations()

Station(id='radiozurnal', name='Radiožurnál', domain='radiozurnal', slogan='Vaše zpravodajství. Vaše rádio.', description='zpravodajství a publicistika')
Station(id='dvojka', name='Dvojka', domain='dvojka', slogan='Rádio na vlně pohody', description='Rádio, které vás baví')
Station(id='vltava', name='Vltava', domain='vltava', slogan='Biograf pro Vaše uši', description='zaměřeno na kulturu v širším slova smyslu')
Station(id='plus', name='Plus', domain='plus', slogan='Pojďte s námi do hloubky!', description='analyticko-publicistická stanice')
Station(id='radiozurnal-sport', name='Radiožurnál Sport', domain='sport', slogan='Nové digitální rádio pro fanoušky sportu', description='Nové digitální rádio pro fanoušky sportu')
Station(id='radiowave', name='Radio Wave', domain='wave', slogan='wwwlna, která tě strhne!', description='vysílání pro mladé')
Station(id='d-dur', name='D-dur', domain='d-dur', slogan='Klasická hudba od renesance až po 21. století v digitální kvalitě 24 hodin denně', description='klasická hudba od renesance až po 21. století')
Station(id='jazz', name='Jazz', domain='jazz', slogan='', description='vysílání pro náročné jazzové posluchače')
Station(id='radiojunior', name='Rádio Junior', domain='junior', slogan='', description='Nejlepší pohádky, nejhezčí písničky, zábavné soutěže a veselé povídání pro všechny děti, od rána až do večera.')
Station(id='pohoda', name='Český rozhlas Pohoda', domain='pohoda', slogan='Písničky a vzpomínky', description='Písničky a vzpomínky')
Station(id='webik', name='Rádio Junior Písničky', domain='webik', slogan='', description='Rádio Junior Písničky – písničky pro menší děti')
Station(id='cro7', name='Radio Prague Int.', domain='cro7', slogan='Vysílání Českého rozhlasu do zahraničí', description='vysílání do zahraničí')
Station(id='brno', name='Brno', domain='brno', slogan='Rozhlas naší Moravy', description='Rozhlas jižní Moravy. Evergreeny, informace, vzdělání, zábava')
Station(id='cb', name='České Budějovice', domain='budejovice', slogan='Rádio Vašeho kraje', description='Reportáže z jižních Čech, písničky na přání a dechovka')
Station(id='hradec', name='Hradec Králové', domain='hradec', slogan='Rádio Vašeho kraje', description='Seriózní a regionální. Zábava, písničky, soutěže')
Station(id='kv', name='Karlovy Vary', domain='vary', slogan='', description='Zábavní hosté, užitečné rady a zprávy ze západu Čech')
Station(id='liberec', name='Liberec', domain='liberec', slogan='', description='Zprávy ze severních Čech, zajímaví hosté, užitečné rady')
Station(id='olomouc', name='Olomouc', domain='olomouc', slogan='Vaše moravské rádio', description='Denně s vámi. Reportáže, zábava a dobrá muzika')
Station(id='ostrava', name='Ostrava', domain='ostrava', slogan='Rádio Vašeho kraje', description='Zprávy, rozhovory, magazíny, písničková přání, dechovky')
Station(id='pardubice', name='Pardubice', domain='pardubice', slogan='Region jako na dlani', description='Informace, hudba a zábava pro východní Čechy')
Station(id='plzen', name='Plzeň', domain='plzen', slogan='Rádio Vašeho kraje', description='Zábavní hosté, užitečné rady a zprávy ze západu Čech')
Station(id='regina', name='Rádio DAB Praha', domain='dabpraha', slogan='Vaše pražské rádio', description='Právě teď v Praze - zajímaví hosté, hity 80. a 90. let')
Station(id='strednicechy', name='Region', domain='region', slogan='Rádio Vašeho kraje', description='Informace ze středních Čech, české písničky a zábava')
Station(id='sever', name='Sever', domain='sever', slogan='Rádio, které žije s Vámi', description='Zprávy ze severních Čech, zajímaví hosté, užitečné rady')
Station(id='vysocina', name='Vysočina', domain='vysocina', slogan='Rádio Vašeho kraje', description='České písničky, zajímaví hosté, zprávy a doprava')
Station(id='zlin', name='Zlín', domain='zlin', slogan='Rozhlas pro Zlínský kraj', description='Rozhlas pro Zlínský kraj')

```


## Popis položek JSON objektu

### `Schedule`

- `station` textové ID stanice (číselník viz https://api.rozhlas.cz/data/v2/meta/stations.json )
- `id` NEunikátní identifikátor převzatý z interního systému, ve kterém se plánuje vysílání; položka má vždy nějakou hodnotu
- `title` název pořadu; položka má vždy nějakou hodnotu
- `description` - popis pořadu; položka může být prázdná
- `since` - začátek vysílání pořadu; položka má vždy nějakou hodnotu
- `till` - konec vysílání pořadu; položka má vždy nějakou hodnotu
- `type` - nedokumentováno
- `edition` - pokud pro pořad existuje tzv. "webová vizitka", položka obsahuje objekt s příslušnými informacemi (např asset - vizuál pořadu); položka ovšem může být prázdná, vizitky totiž zatím neexistují pro všechny pořady
- `persons` pole objektů moderátorů pořadu (tzv. osoby), kterých může být 0-N (obsahuje kromě jiného také asset - fotografii moderátora); položka může být prázdná, protože ne každý pořad někdo moderuje a také ne pro všechny osoby máme k dispozici fotografie

### `Stations`

...

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

## Zdroje

- https://data.irozhlas.cz/opendata/
- https://cs.wikipedia.org/wiki/%C4%8Cesk%C3%BD_rozhlas
