# rozhlas-schedule-client
Python client for "Program vysílání ČRo"

## Program vysílání ČRo

### Aktuální den a všechny stanice
https://api.rozhlas.cz/data/v2/schedule/day.json

### Aktuální den a konkrétní stanici
https://api.rozhlas.cz/data/v2/schedule/day/[STATION_ID].json
např. https://api.rozhlas.cz/data/v2/schedule/day/radiowave.json

### Konkrétní den a všechny stanice
https://api.rozhlas.cz/data/v2/schedule/day/[YYYY]/[MM]/[DD].json
např. https://api.rozhlas.cz/data/v2/schedule/day/2019/09/01.json

### Konkrétní den a konkrétní stanici:
https://api.rozhlas.cz/data/v2/schedule/day/[YYYY]/[MM]/[DD]/[STATION_ID].json
např. https://api.rozhlas.cz/data/v2/schedule/day/2019/09/01/radiowave.json

Data jsou dostupná mnoho let do historie a cca 14 dnů do budoucnosti.

### Popis položek JSON objektu

- `station` textové ID stanice (číselník viz https://api.rozhlas.cz/data/v2/meta/stations.json )
- `id` NEunikátní identifikátor převzatý z interního systému, ve kterém se plánuje vysílání; položka má vždy nějakou hodnotu
- `title` název pořadu; položka má vždy nějakou hodnotu
- `description` - popis pořadu; položka může být prázdná
- `since` - začátek vysílání pořadu; položka má vždy nějakou hodnotu
- `till` - konec vysílání pořadu; položka má vždy nějakou hodnotu
- `type` - nedokumentováno
- `edition` - pokud pro pořad existuje tzv. "webová vizitka", položka obsahuje objekt s příslušnými informacemi (např asset - vizuál pořadu); položka ovšem může být prázdná, vizitky totiž zatím neexistují pro všechny pořady
- `persons` pole objektů moderátorů pořadu (tzv. osoby), kterých může být 0-N (obsahuje kromě jiného také asset - fotografii moderátora); položka může být prázdná, protože ne každý pořad někdo moderuje a také ne pro všechny osoby máme k dispozici fotografie
