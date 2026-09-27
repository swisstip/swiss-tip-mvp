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

Two HackYeah tasks (3-4 October 2026, Kraków) match it. The event allows
one project per task and discourages entering one project in two, so the
pack enters one of them; the choice is recorded in the implementation plan
of the code repository:

- **Smart City**, an open task with a 5 000 PLN pool: "technology that
  helps cities work better", with communication with citizens, public
  services and access to information named in the brief. Grounded answers
  to residents' questions about their own city, from the waste fee to the
  winter holidays.
- **HubMI.pl**, a partner task with a 15 000 PLN pool: "connect residents'
  needs more effectively with knowledge, proven solutions, and people ready
  to take action". The civic instruments through which a resident's idea
  reaches the city (the participatory budget, the local initiative, grants
  for social organisations) differ by city and are rarely known; the pack
  states, per city, what exists, who runs it and by when to apply. The
  task's own rules and jury are published no later than 3 October.

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

Evidence is in Polish only: every excerpt is cut from a Polish official
page and stays the authoritative text. Statements, aliases and sample
questions are in English, as editorial translations and summaries of the
excerpts, as in `mvp-zurich`; source terms are copied in Polish from the
excerpts, and sample questions are also written in Polish. The release
names English and Polish as its query languages, so the calling model is
told to call the tools in either. The pack is built at HackYeah as a proof
of concept on the code prepared before it, and its facts are reviewed by
the same named person as `mvp-zurich`.

## Civic participation

The first topic group: the participatory budget, the local initiative and
grants for non-governmental organisations, and consultations and the
resident's voice (district councils, the citizens' resolution initiative,
the debate on the report on the state of the city, council sessions), for
the three cities and under the national acts.

- **Acceptance-test document.**
  [poland-civic-acceptance-tests.md](../../docs/product/poland-civic-acceptance-tests.md)
  holds 40 trap questions in Polish with their expected answers, researched
  on 27 September 2026 from official pages and checked by an independent
  second reading; no person has reviewed them yet.
- **Catalogue.** `sources.json` (catalogue `draft-1`) has 38 registry
  entries: the national acts through the Sejm's ELI API, the national
  guidance on gov.pl, one entry per official host of each city, and one per
  council resolution in a voivodeship's official journal. `sources.md`
  lists the 270 exact pages; 39 of them are on Warsaw hosts behind a bot
  challenge and are catalogued as `manual_adapter_required`. Their notes,
  and the *not fetched* marks in `sources.md`, predate the browser session
  that now fetches them; the next catalogue version updates them together
  with the gov.pl allowlist below.
- **Run.** Downloaded on 27 September 2026 into `.local/mvp-poland/`, with
  retries: of 271 targets, 249 are saved (82 MB) and 22 are not saved.
  - The Warsaw hosts behind the challenge (`um.warszawa.pl`, its district
    servers) and the record pages of Warsaw's Public Information Bulletin,
    which answer an empty body without a session cookie, were fetched with
    `--browser-host`: 46 pages, each a plain response to the crawler's own
    request with the session's cookie, robots.txt obeyed.
  - 16 of the 22 are on `bo.katowice.eu`, the Katowice participatory-budget
    portal, which mostly did not accept connections that day. The Katowice
    budget cases PL-CIV-10 to PL-CIV-13 cite it; the council's budget
    resolutions are saved from the city's Public Information Bulletin,
    which answered every request.
  - 4 are on `cdn.um.warszawa.pl`, Warsaw's document server. It publishes no
    robots.txt of its own: the request redirects to the city portal's home
    page, and the crawler fails closed on a robots.txt it cannot read. Two
    of the four documents (the budget resolution and its amendment) are
    saved from the voivodeship's journal instead; the report on the 13th
    edition and the mayor's consolidated order 825/2019 are not.
  - 2 are on gov.pl, whose robots.txt redirects to
    `/static/code/robots.txt`, outside the entry's allowlist; the next
    catalogue version adds that path. PL-CIV-14 cites one of them beside
    the act itself, which is saved.
- **Text dataset.** `.local/mvp-poland/text/`, extractor 0.2.2, validated:
  249 records (155 HTML, 81 PDF, 13 DOCX), 248 extracted with 31,653 blocks
  and 4.0 million characters. The one without text is Warsaw's consolidated
  local-initiative resolution, a scan without a text layer.

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
  `um.warszawa.pl` and its district servers answer every request with a
  JavaScript challenge and are fetched through the downloader's browser
  session; its document server `cdn.um.warszawa.pl` is not (see "Run")
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

1. Before the event: build the prerequisites in the code repository, with
   tests on a synthetic Polish pack; retry the download of `bo.katowice.eu`
   and add the gov.pl robots path to the catalogue; restate the date-bound
   cases of the acceptance-test document as of 3 October 2026 and choose
   the cases the demo will show.
2. At the event, as the proof of concept: curate the civic-participation
   facts from the text dataset, the participatory budget of Kraków first
   (its sources are complete and the event is in Kraków), then the national
   acts, then Warsaw and Katowice as far as the review allows; review, turn
   the reviewed cases into `acceptance.yaml`, build, index and attest as
   for `mvp-zurich`; record the screenshots and the video for the
   submission.
3. Afterwards: the acceptance-test documents and catalogues of the other
   topics (waste, mobility, air and heating, schools, days and dates)
   before their pages are fetched.
