# mvp-poland

**Last update:** 27 September 2026

A pack in preparation: official public information for everyone who lives
in a Polish city, served by the same server and built by the same pipeline
as `mvp-zurich`. Its first topic group, civic participation, has a source
catalogue, a downloaded run and an acceptance-test document (see "Civic
participation"). There is no curation file, release or report yet, and the
server does not yet accept Polish jurisdictions (see "Prerequisites in the
code").

## Why

Everyday city rules in Poland are set at four levels, and the answer to a
plain question - what the waste fee is, whether a car may enter the centre,
whether a fireplace may be lit, when the winter school holidays are -
changes from one voivodeship or city to the next. A generic assistant gives
one answer for the whole country. The pack serves the rule that applies to
the resident's own city, with the excerpt of the official page it comes
from, and says when a city is not covered.

It answers two HackYeah challenges:

- **Smart City** - technology that makes everyday life in a city easier,
  with communication with citizens and public services named in the brief:
  grounded answers to residents' questions about their own city.
- **Connecting residents' needs with knowledge and people ready to act** -
  the civic instruments through which a resident's idea reaches the city
  (the participatory budget, the local initiative, grants for social
  organisations) differ by city and are rarely known; the pack states, per
  city, what exists, who runs it and by when to apply.

## Scope

The audience is the whole population of a city. The first scope is the
questions whose answer depends on where the resident lives:

| Level | Units | Example of what differs |
| --- | --- | --- |
| National (`państwo`) | 1 | Days off, Sunday trading, the minimum wage |
| Voivodeship (`województwo`) | 16 | Winter school holidays, the anti-smog resolution |
| County (`powiat`) | 380 | Vehicle registration, driving licences |
| Commune (`gmina`) | 2,479 | Waste fees and how they are calculated, clean transport zones, a city's own anti-smog rules, the participatory budget and the local initiative |

The counts are those of the GUS TERYT register (TERC) as of 1 January
2026, downloaded on 27 September 2026 into `.local/mvp-poland/places/`.

The first places are the City of Kraków (Małopolskie), the City of Warsaw
(Mazowieckie) and the City of Katowice (Śląskie): three voivodeships and
three cities, so that every question above has at least two different
answers in the pack.

Planned topics:

| Topic | Examples |
| --- | --- |
| Waste | The fee and its method (per person, per household, per water use), what goes in which bin, bulky waste, the collection calendar |
| Mobility | Clean transport zones and their exemptions, paid parking zones, resident discounts on public transport |
| Air and heating | The anti-smog resolutions, what a fireplace or boiler may burn and by when an old boiler must be replaced, subsidies for replacing it |
| Schools and families | Winter school holidays by voivodeship, school and kindergarten enrolment |
| Civic participation | The participatory budget (who may propose and vote, the dates), the local initiative, open calls for social organisations |
| Days and dates | Days off, trading Sundays |

Evidence is in Polish. Statements are planned in Polish, with English
aliases and sample questions, so that the pack serves residents in their
own language; `mvp-zurich` states its facts in English, so this is a
decision to confirm.

## Candidate sources

- `gov.pl` and its office sites, `podatki.gov.pl`
- Acts and ordinances of Dziennik Ustaw through the Sejm's ELI API
  (`api.sejm.gov.pl`), which serves the same PDFs; ISAP and
  dziennikustaw.gov.pl disallow every crawler in robots.txt
- Council resolutions as published in the voivodeships' official journals
- The voivodeship assemblies' anti-smog resolutions, and the voivodeship
  portals (`powietrze.malopolska.pl`, `powietrze.slaskie.pl`)
- The Public Information Bulletin (BIP) of each city, and the city portals
  (`krakow.pl`, `bip.krakow.pl`, `warszawa19115.pl`, `katowice.eu`);
  `um.warszawa.pl` and its document and district servers answer every
  request with a JavaScript challenge, so they are catalogued but not
  fetched
- The GUS TERYT register for the place register
- Open data on `dane.gov.pl` for dataset connectors (waste-collection
  calendars, as in `mvp-zurich`), where a city publishes it

Normative acts and official documents are not protected by copyright in
Poland (Art. 4 of the copyright act), so quoting excerpts is on firm ground.

## Prerequisites in the code

These change the code repository, not this pack. The source catalogue
already accepts a Polish scope with declared levels, and the downloader
saves the DOCX resolutions some city offices publish; the rest is not
started:

- **Jurisdiction codes.** `packages/core` accepts only `CH` codes of up to
  three levels. Poland needs a fourth level and TERYT-based codes, one
  segment per level: `PL`, `PL-12` (Małopolskie), `PL-12-61` (the county
  of Kraków), `PL-12-61-011` (the commune of Kraków, the last three digits
  of its TERYT code).
- **Institution levels.** `InstitutionLevel` is fixed to federal, cantonal
  and municipal; Poland needs national, voivodeship, county and commune.
- **Place register.** An importer for TERYT next to the BFS importer, with
  its files under `config/places/`.
- **Basis labels.** `ustawa`, `rozporządzenie`, `akt prawa miejscowego`
  (a voivodeship assembly's or commune council's `uchwała`), authority
  guidance.
- **Polish search.** Lexical search counts matching tokens, and Polish
  inflects (`opłata`, `opłaty`, `opłatę`). It needs lemmatisation or
  stemming, measured on a Polish regression pack.
- **Context vocabulary.** The resident's situation as the rules name it,
  for example the type of building (block of flats or single-family
  house), whether bio-waste is composted at home, the fuel and emission
  standard of a car and where it is registered.

## Draft acceptance questions

Questions with a trap, collected on 26 and 27 September 2026 and checked
against web search results that quote the official sources. They are not
yet cases of an `acceptance.yaml`: the expected answers must be curated
from the saved pages and reviewed before they become claims.

| Question | Expected answer | Trap |
| --- | --- | --- |
| *Ile płacę za wywóz śmieci?* | Kraków: 35 zł per person a month. Warsaw: per household, from 1 April 2026 85 zł in a block of flats and 107 zł in a single-family house, 9 zł less when bio-waste is composted at home | A national average, or per person and per household mixed up |
| *Mam diesla z 2008 roku (Euro 4). Czy mogę wjechać do centrum?* | Kraków and Warsaw: no, their clean transport zones require Euro 5 for diesels since 1 January 2026, subject to each city's exemptions. Katowice: no zone | No zones in Poland, or one city's standards applied to another |
| *Czy mogę palić drewnem w kominku?* | Kraków: no, all solid fuels banned since 1 September 2019. Śląskie: yes, if the fireplace reaches 80% efficiency or has a dust filter | One answer for all of Poland |
| *Kiedy moje dziecko ma ferie zimowe w 2027 roku?* | Śląskie 18-31 January, Mazowieckie 1-14 February, Małopolskie 15-28 February 2027 | One date for the whole country |
| *Czy w niedzielę 13 grudnia 2026 r. sklepy będą otwarte?* | Yes: a trading Sunday (6, 13 and 20 December 2026) | The general Sunday trading ban |
| *Mój szef mówi, że 24 grudnia normalnie pracujemy, bo to nie jest święto. Czy ma rację?* | No: since 2025, 24 December is a statutory day off, with sector exceptions | The rule before 2025 |
| *Mam pomysł na zieleniec na moim osiedlu. Jak mogę go zgłosić do miasta i do kiedy?* | Per city: the participatory budget's current edition and dates, and the local initiative (the civic-participation cases below give each city's rules) | One generic procedure, or last year's dates |

The Katowice answer on clean transport zones rests on the sources naming
only Warsaw and Kraków as cities with a zone in force; it must be confirmed
on the city's own pages.

## Next steps

1. Decide the first scope with the team and write the acceptance-test
   document before any page is fetched.
2. Build the prerequisites in the code repository, with tests on a
   synthetic Polish pack.
3. Write `sources.json` for the chosen scope and run the bounded download
   into `.local/mvp-poland/`.
4. Curate, review, build and attest as for `mvp-zurich`.
