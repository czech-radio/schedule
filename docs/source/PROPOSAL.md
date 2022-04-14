# Schedule

## Motivation

Chceme mít ověřený přehled vysíláných pořadů na jednotlivých stanicích pro snadné
vyhledávaní relevantních informací potřebných k analýzám  obsahů vysílání.

## Solution

Softwarový balík `cro.schedule` se skládá z knihovny a aplikace.
Knihovna (SDK) slouží k získání programu pro příslušnou stanici a období poskytované jako REST (JSON)
aplikačním rozhraním. Jde tedy o obal nad jinak syrovýmo voláními služby pomocí HTTP protokolu. Podkytuje
také doménový modelse kterým se dobře oracuje v dalších programech. Nad touto knihovnou je postavěná služba
která za a) pravidelně stahuje a zálohuje dostupné programy b) poskytuje REST rozhraní pro další služby
c) umožňuje snadnou zprávu a přidávání dalších informací k takto získanému vysílacímu schematu.

Vysílací schema je na každé stanici tvořeno jednotlivými pořady. Pořady mají určen svůj čas začátků a konce v daném dni a dané stanici. U pořadu nás zajímá jeho název, popis a žánrové zařazení. Dála nás zajímá počet očekávaných mluvčí v daném pořady tj. případní moderátoři a respondenti. Pořady můžeme zařadit podle času vysílání do ranní, dopolední, odpolední, večerní a noční relace (DOPLNIT rozsah časů).

## Features

- Stáhuj periodicky dostupná schemata vysílání (historické od začátku roku 2022).
- Pro získané vysílací schema proveď automatické zařazení pořadů:
  - Přiřaď pořad k námi vytvořenému a udržoovanému výčtu. U toho sledujeme zejména žánr a očekávaný počet mluvčích, časy repríz.
- Umožni dodatečné korekce automaticky provedených úprav a zkus je nějak zužitkovat jako
  zpětnou vazbu pro automatické zpracování.
- K pořadu přiřaď dostupný textový přepis. Z něho se dají zjistit mluvčí a téma pořadu.
- Pro pořad s respondenty proveď určení (identifikaci) těchto respondentů pomocí databáze osob.

## Glossary

- schema vysílání (vysílací schema); program vysílání [_schedule_]
- mluvčí [_speaker_], respondent [_respondent_], moderátor [_moderator_]
- stanice [_station_]
