# Swiss TIP MCP server - container image

```text
ghcr.io/swisstip/swiss-tip:mvp-zurich-2026-09-18-v10
```

Swiss TIP, the Swisscom Trusted Information Platform, is an MCP (Model
Context Protocol) server that gives AI assistants grounded access to
official Swiss public information. This image contains the server, one
curated, versioned knowledge release, a bundled local embedding model
for hybrid concept search and the calendar connector with the pack's
waste-collection calendars, and nothing else: no credentials and no network
access are needed to serve it. The tags ending in `-slim` name the same
server and release without the embedding model, which a second container
supplies (see "Two containers" below).

The server does not write answers. The assistant that calls it interprets
the question and composes the reply. The server supplies the facts that
apply to a stated place, date and situation, the exact excerpts of the
official pages they come from, the citations, and a typed statement of what
is missing or not covered. It offers five read-only tools:

| Tool | What it returns |
| --- | --- |
| `get_coverage` | The scope statement, topics, jurisdictions, languages, freshness and out-of-scope list in one call under 8.7 KB; with a topic ID, that topic's concepts |
| `search` | Concepts matching a question, in English or German, with the context each concept needs; lexical matching fused with the bundled embedding model's ranking |
| `resolve` | For concept IDs, the place the user lives in (a canton and a city by name, or their codes), a date and the user's situation: the facts, each with the basis of its excerpt (a federal act and its article, an ordinance, the free-movement agreement, a cantonal directive, an authority's guidance, a portal summary), the citations with the publisher's level and jurisdiction, and a status: `SUPPORTED`, `NEEDS_CONTEXT` (naming the missing field), `OUT_OF_COVERAGE` (naming what is covered) or `STALE` |
| `get_evidence` | The full original-language excerpts behind facts or citations, each with its basis and publisher |
| `lookup` | The next collection dates of a waste-collection calendar (Zurich by postal code, Basel and St. Gallen by collection zone) that `resolve` offers on a waste concept, with the publisher and licence of the open dataset |

## The bundled knowledge base

**Release `mvp-zurich-2026-09-18-v10`:** foreign nationals in Switzerland,
from entry and visas, residence permits and registration to social insurance
on arrival and departure, tax at source and its tariffs, the foreign driving
licence, health insurance and premium reduction, naturalisation and voting
rights, with the contacts and opening hours of the Zurich offices and daily
life in the City of Zurich (waste and recycling, parking, vehicles, dogs,
kindergarten, the tax return, the radio and television fee, medical
emergencies); federal rules with the Canton of Zurich and the City of
Zurich. The release content digest (SHA-256) is
`d0dd18b09eeeed7709565c66e1a72af08be562b1065ff544af4f011b20afc8cb`.

Scope, as the server states it to every caller:

> Foreign nationals and newcomers in Switzerland: federal rules with Canton
> of Zurich and City of Zurich procedures. Entry and visas: the visa duty,
> the visa types C and D, the 90-in-180-days rule, the entry requirements,
> ETIAS and the Entry/Exit System. Residence permits and registration (AIG,
> the free-movement agreement FZA, SEM and ch.ch guidance, Zurich
> procedures), the migration-office contact of every canton, and the Zurich
> offices' addresses, opening hours and contacts. Social insurance on
> leaving (AHV refunds, pensions abroad, pension fund cash payment). Tax at
> source with its tariff codes and the Zurich tariff rules, the City of
> Zurich tax return and tax office, and the radio and television fee.
> Driving licence, vehicles after a move or import, and City of Zurich
> parking permits. Health insurance and premium reduction. Naturalisation
> and voting rights. Life in the City of Zurich: first steps, waste and
> recycling, dogs, kindergarten and school holidays, and medical
> emergencies.

| | |
| --- | --- |
| Topics | 14: residence permits and registration (58 concepts), cantonal migration offices (1), Zurich office contacts (9), first steps and life in the City of Zurich (7), waste and recycling (6), parking and vehicles (2), tax return and household fees (3), social insurance on arrival and departure (4), tax at source (5), foreign driving licence (3), health insurance and premium reduction (4), naturalisation (6), entry and visas (9), voting rights (2) |
| Concepts | 119 |
| Facts | 495, each with at least one cited excerpt (568 evidence items) |
| Cited documents | 109 official documents: 108 in German, 1 in English |
| Jurisdictions | Switzerland (`CH`), all 26 cantons (`CH-AG` to `CH-ZH`) and the City of Zurich (`CH-ZH-261`); the added topics are cantonal for Zurich only |
| Places | A caller names the user's place instead of a code: `resolve` takes `country`, `canton` and `city` as names in English or the local language (`{"city": "Wallisellen"}`, `Genf`, `Kanton Zürich`) or as codes, and turns them into codes with the release's place register: Switzerland, the 26 cantons and the 2,110 municipalities of the Federal Statistical Office's register of municipalities of 18 September 2026 |
| Languages | Fact statements in English; excerpts in the language of the page; search accepts English and German |
| Snapshot | Pages saved on 10, 11, 14, 15, 17 and 18 September 2026; `resolve` answers `STALE` for dates from 17 November 2026 (the date defaults to today) |
| Review | All 495 facts `human-reviewed`: confirmed by one named reviewer in the review console, the first 253 also read card by card against their cited excerpts; not a legal review |
| Readiness | Attested on 18 September 2026; the image serves no release without a matching readiness record |

What the concepts cover:

- **Entry and visas (SEM, FDFA, VEV):** who needs a visa, the Schengen visa
  C and the national visa D, the 90 days in any 180, the entry requirements
  of third-country and of EU/EFTA nationals and their family members, where
  and how to apply, the fee, the travel health insurance and the processing
  time, the ETIAS travel authorisation and the Entry/Exit System.
- **Federal permits and procedures (AIG, SEM, ch.ch):** the L, B and C
  permits and the other permit cards (Ci, G, F, N, S), which states are EU
  and EFTA, renewing a residence permit, a lost or stolen permit,
  registration under Article 12, the authority that issues permits, the
  employment permit procedure, stays without work, study admission, change
  of canton, the biometric permit card, integration criteria, evidence of
  language skills, social assistance and its consequences for a permit.
- **Family:** reunification with a Swiss, EU/EFTA, settlement-permit or
  residence-permit sponsor, the marriage or registered-partnership
  requirement, housing, means and entry documents, the permit and work rights
  of family members, the reunification deadlines, and residence after the
  family relationship ends.
- **Work:** third-country employment admission, exemptions, who applies,
  the visa caveat and registration before starting work; the EU/EFTA
  registration deadline after arrival, permit validity and job changes,
  self-employment and job search; the notification procedure for short
  employment and cross-border services; and new short-term employment of UK
  nationals.
- **The Agreement on the Free Movement of Persons (FZA, treaty text):**
  its aims and non-discrimination, entry on an identity card, staying to look
  for work, the residence permits of EU employees, self-employed persons and
  persons without work (students and retirees included), cross-border
  commuters, family members of any nationality and their right to work,
  occupational and geographical mobility, equal treatment, the right to
  remain, services of up to 90 working days, and the coordination of social
  security.
- **Canton and City of Zurich, residence:** registration, short-stay and
  residence permits, self-employment and family documents for EU/EFTA
  nationals, residence without employment, retirement applications of
  third-country nationals, family reunification by holders of an L permit
  and by recognised refugees granted asylum; registering an arrival in the
  city and the documents to bring.
- **Every canton:** the migration-office contact.
- **Zurich offices:** the address, opening and telephone hours and contact
  channels of the cantonal Migration Office, Naturalisation Division, Road
  Traffic Office (all eight locations), Cantonal Tax Office and Office for
  the Economy, of the SVA Zurich (with directions and holiday hours) and of
  the City of Zurich Population Office (appointments since May 2026) and
  naturalisation office, including what a page states in the negative, such
  as the Migration Office having no e-mail address.
- **Daily life in the City of Zurich:** the newcomer checklist (registration,
  electricity and water, vehicles, health insurance, the service booklet);
  the Züri-Sack, its fees and the collections of household waste, organic
  waste, paper and cardboard; bulky-waste pickup, the recycling centres and
  points and hazardous waste; blue-zone parking, the resident parking card
  and day permits; registering a dog and the Canton of Zurich's dog-keeping
  and training duties; kindergarten entry, the school holidays of 2026/27
  and 2027/28 and school information in other languages; the tax return and
  the city's tax office; medical emergencies (144).
- **Vehicles (Canton of Zurich):** reporting a move with a vehicle, new
  plates after a change of canton, and importing a vehicle.
- **Radio and television fee (SERAFE):** the household fee, its amount and
  the exemptions.
- **Social insurance on leaving (ZAS, BSV, Fedlex):** which nationals can
  have their AHV contributions refunded and on what conditions, who keeps an
  AHV pension abroad, the cash payment of pension-fund assets on leaving for
  good and its restriction for EU/EFTA destinations since 2007, and the
  Vested Benefits Act's rules on keeping the cover.
- **Tax at source (ESTV, Canton of Zurich):** who is taxed at source, when
  the liability ends (C permit, citizenship, marriage), and the subsequent
  ordinary assessment: mandatory from CHF 120,000, on request by 31 March,
  and what the request binds; the federal tariff codes (A, B, C, H and the
  others) and how the Canton of Zurich sets the tariff, with the number of
  children and the church tax.
- **Driving licence (VZV, ch.ch, Canton of Zurich):** the twelve months after
  taking up residence, the two lists of states whose licences are exchanged
  without a control drive, the control drive and its single attempt, the
  documents and the road traffic offices.
- **Health insurance (FOPH, Canton of Zurich, SVA Zurich):** the three months
  to insure, cover and premiums from the date of residence, late joining,
  who can be exempted and on what proof, and the premium reduction: who
  decides, how to apply, and when an entitlement starts after a move.
- **Naturalisation (SEM, Canton and City of Zurich):** the federal, cantonal
  and city conditions of ordinary naturalisation (C permit, years of
  residence and how permit years count, language, knowledge, debts,
  criminal record), the procedure and fees (the City of Zurich's included),
  and facilitated naturalisation of a Swiss citizen's spouse.
- **Voting rights (Federal Constitution, Constitution of the Canton of
  Zurich, ch.ch):** political rights in federal matters belong to Swiss
  citizens; what the cantons may grant foreign nationals, and the rule of the
  Canton of Zurich and its municipalities.

The cited documents, with the number of facts each supports:

| Publisher | Page | Facts |
| --- | --- | --- |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | [FZA / ALCP, SR 0.142.112.681](https://fedlex.data.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/2002/243/20201215/de/html/fedlex-data-admin-ch-eli-cc-2002-243-20201215-de-html-9.html) | 37 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | [AIG / LEI / FNIA, SR 142.20](https://fedlex.data.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/2007/758/20260612/de/html/fedlex-data-admin-ch-eli-cc-2007-758-20260612-de-html-3.html) | 28 |
| State Secretariat for Migration SEM | [Kantonale Migrations- und Arbeitsmarktbehörden](https://www.sem.admin.ch/sem/de/home/sem/kontakt/kantonale_behoerden/adressen_kantone_und.html) | 26 |
| State Secretariat for Migration SEM | [FAQ – Einreise](https://www.sem.admin.ch/sem/de/home/themen/einreise/faq.html) | 14 |
| Canton of Zurich, Road Traffic Office | [Standorte und Öffnungszeiten des Strassenverkehrsamts - Kanton Zürich](https://www.zh.ch/de/sicherheitsdirektion/strassenverkehrsamt/standorte-oeffnungszeiten.html) | 13 |
| Canton of Zurich, Office for Municipalities, Naturalisation Division | [Ordentliche Einbürgerung - Kanton Zürich](https://www.zh.ch/de/migration-integration/einbuergerung/ordentliche-einbuergerung.html) | 11 |
| Federal Office of Public Health FOPH | [Krankenversicherung: Versicherungspflicht für in der Schweiz wohnhafte Versicherte](https://www.bag.admin.ch/de/krankenversicherung-versicherungspflicht-fuer-in-der-schweiz-wohnhafte-versicherte) | 10 |
| Canton of Zurich, Cantonal Tax Office | [Quellensteuerpflichtige Personen - Kanton Zürich](https://www.zh.ch/de/steuern-finanzen/steuern/quellensteuer/Quellensteuerpflichtige-Personen.html) | 10 |
| Canton of Zurich, Cantonal Tax Office | [Quellensteuer-Tarife - Kanton Zürich](https://www.zh.ch/de/steuern-finanzen/steuern/quellensteuer/quellensteuer-tarife.html) | 9 |
| City of Zurich, Population Office | [Erste Schritte - Stadt Zürich](https://www.stadt-zuerich.ch/de/lebenslagen/neu-in-zuerich/erste-schritte.html) | 8 |
| State Secretariat for Migration SEM | [Meldeverfahren für kurzfristige Erwerbstätigkeit](https://www.sem.admin.ch/sem/de/home/themen/fza_schweiz-eu-efta/meldeverfahren.html) | 8 |
| City of Zurich, Naturalisation Division | [Ordentliche Einbürgerung - Stadt Zürich](https://www.stadt-zuerich.ch/de/lebenslagen/einwohner-services/einbuergerung/ordentliche-einbuergerung.html) | 8 |
| Canton of Zurich, Road Traffic Office | [Umtausch eines ausländischen Führerausweises - Kanton Zürich](https://www.zh.ch/de/mobilitaet/fuehrerausweis-fahren-lernen/auslaendischer-fuehrerausweis.html) | 8 |
| ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery) | [Als Ausländerin oder Ausländer in der Schweiz arbeiten](https://www.ch.ch/de/auslander-in-der-schweiz/in-der-schweiz-arbeiten/) | 7 |
| Central Compensation Office CCO | [Anspruch auf AHV-Rentenzahlungen ausserhalb der Schweiz](https://www.zas.admin.ch/de/anspruch-auf-ahv-rentenzahlungen-ausserhalb-der-schweiz) | 7 |
| Canton of Zurich, Migration Office | [Aufenthalt für EU/EFTA-Staatsangehörige - Kanton Zürich](https://www.zh.ch/de/migration-integration/aufenthalt/aufenthalt-fuer-euefta-staatsangehoerige.html) | 7 |
| ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery) | [Aufenthaltsbewilligung für die Schweiz: Gesuch und Erneuerung](https://www.ch.ch/de/auslander-in-der-schweiz/einreise-in-die-schweiz/aufenthaltsbewilligung/) | 7 |
| City of Zurich, Naturalisation Division | [Erleichterte Einbürgerung - Stadt Zürich](https://www.stadt-zuerich.ch/de/lebenslagen/einwohner-services/einbuergerung/erleichterte-einbuergerung.html) | 7 |
| State Secretariat for Migration SEM | [FAQ – Schweizer Bürgerrecht](https://www.sem.admin.ch/sem/de/home/integration-einbuergerung/schweizer-werden/faq.html) | 7 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | [Fedlex: Tax at Source Ordinance of the FDF, SR 642.118.2](https://fedlex.data.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/2018/274/20250110/de/html/fedlex-data-admin-ch-eli-cc-2018-274-20250110-de-html-1.html) | 7 |
| Canton of Zurich, Cantonal Tax Office | [Merkblatt des kantonalen Steueramtes über die Quellenbesteuerung von Arbeitnehmerinnen und Arbeitnehmern - Kanton Zürich](https://www.zh.ch/de/steuern-finanzen/steuern/treuhaender/steuerbuch/steuerbuch-definition/zstb-87-3.html) | 7 |
| Central Compensation Office CCO | [Rückvergütungen](https://www.zas.admin.ch/de/rueckverguetungen) | 7 |
| Canton of Zurich, Road Traffic Office | [Ausländischen Führerausweis umtauschen - Kanton Zürich](https://www.zh.ch/de/mobilitaet/fuehrerausweis-fahren-lernen/auslaendischer-fuehrerausweis/auslaendischen-fuehrerausweis-umtauschen.html) | 6 |
| ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery) | [Gesuch um Familiennachzug in die Schweiz](https://www.ch.ch/de/auslander-in-der-schweiz/einreise-in-die-schweiz/familiennachzug/) | 6 |
| Federal Social Insurance Office FSIO | [Kann ich mein BVG-Altersguthaben bar beziehen, wenn ich die Schweiz endgültig verlasse? - BSV](https://faq.bsv.admin.ch/de/berufliche-vorsorge/kann-ich-mein-bvg-altersguthaben-bar-beziehen-wenn-ich-die-schweiz-endgueltig) | 6 |
| State Secretariat for Migration SEM | [Verheiratet mit einer Schweizerin oder einem Schweizer](https://www.sem.admin.ch/sem/de/home/integration-einbuergerung/schweizer-werden/verheiratet.html) | 6 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | [Abfuhr Hauskehricht - Stadt Zürich](https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/wo-und-wann-entsorgen/abfuhr-hauskehricht.html) | 5 |
| State Secretariat for Migration SEM | [Brauche ich ein ETIAS?](https://www.sem.admin.ch/sem/de/home/themen/einreise/info-einreise/voraussetzungen-nach-staat/etias.html) | 5 |
| State Secretariat for Migration SEM | [Die Ordentliche Einbürgerung](https://www.sem.admin.ch/sem/de/home/integration-einbuergerung/schweizer-werden/ordentlich.html) | 5 |
| City of Zurich, School Office | [Einschulung - Stadt Zürich](https://www.stadt-zuerich.ch/de/bildung/volksschule/schullaufbahn/einschulung.html) | 5 |
| Canton of Zurich, Office for Municipalities, Naturalisation Division | [Erleichterte Einbürgerung - Kanton Zürich](https://www.zh.ch/de/migration-integration/einbuergerung/erleichterte-einbuergerung.html) | 5 |
| Canton of Zurich, Migration Office | [Familiennachzug durch Flüchtlinge mit Asyl beantragen - Kanton Zürich](https://www.zh.ch/de/migration-integration/aufenthalt/familiennachzug-von-drittstaatsangehoerigen/familiennachzug-durch-fluechtlinge-mit-asyl-beantragen.html) | 5 |
| Canton of Zurich, Veterinary Office | [Hunde - Kanton Zürich](https://www.zh.ch/de/umwelt-tiere/tiere/haustiere-heimtiere/hunde.html) | 5 |
| Federal Office of Public Health FOPH | [Krankenversicherung: Prämienverbilligung](https://www.bag.admin.ch/de/krankenversicherung-praemienverbilligung) | 5 |
| SVA Zürich, the cantonal social insurance office | [Prämienverbilligung: Wer hat Anspruch?](https://svazurich.ch/unsere-produkte/weitere-produkte/krankenversicherung--kvg-/praemienverbilligung/wer-hat-anspruch-.html) | 5 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | [Recyclinghof - Stadt Zürich](https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/wo-und-wann-entsorgen/recyclinghof.html) | 5 |
| Federal Tax Administration FTA | [Schweizerische Quellensteuer QST](https://www.estv.admin.ch/de/quellensteuer) | 5 |
| City of Zurich, Tax Office | [Steuererklärung für natürliche Personen der Stadt Zürich - Stadt Zürich](https://www.stadt-zuerich.ch/de/lebenslagen/steuern/natuerliche-personen/steuererklaerung.html) | 5 |
| City of Zurich, Population Office | [Terminpflicht beim Personenmeldeamt - Stadt Zürich](https://www.stadt-zuerich.ch/de/lebenslagen/einwohner-services/online-schalter/personenmeldeamt-terminpflicht.html) | 5 |
| Canton of Zurich, Office for Municipalities, Naturalisation Division | [Abteilung Einbürgerungen - Kanton Zürich](https://www.zh.ch/de/direktion-der-justiz-und-des-innern/gemeindeamt/abteilung-einbuergerungen.html) | 4 |
| State Secretariat for Migration SEM | [Einreise ohne Visum](https://www.sem.admin.ch/sem/de/home/themen/einreise/info-einreise/voraussetzungen-nach-staat/ohne-visum.html) | 4 |
| Canton of Zurich, Migration Office | [Familiennachzug durch Personen mit einer L-Bewilligung beantragen - Kanton Zürich](https://www.zh.ch/de/migration-integration/aufenthalt/familiennachzug-von-drittstaatsangehoerigen/familiennachzug-durch-personen-mit-einer-l-bewilligung-beantragen.html) | 4 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | [Fedlex: Ordinance on Entry and the Granting of Visas, SR 142.204](https://fedlex.data.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/2018/493/20260612/de/html/fedlex-data-admin-ch-eli-cc-2018-493-20260612-de-html-1.html) | 4 |
| City of Zurich, City Police | [Hundekontrolle - Stadt Zürich](https://www.stadt-zuerich.ch/de/stadtleben/veranstaltungen-und-bewilligungen/hundekontrolle.html) | 4 |
| City of Zurich, School Office | [Kindergarten - Stadt Zürich](https://www.stadt-zuerich.ch/de/bildung/volksschule/schullaufbahn/kindergarten.html) | 4 |
| City of Zurich, Tax Office | [Kontakte und Öffnungszeiten des Steueramts - Stadt Zürich](https://www.stadt-zuerich.ch/de/lebenslagen/steuern/kontakt.html) | 4 |
| SVA Zürich, the cantonal social insurance office | [Krankenversicherungspflicht: Wer kann sich befreien lassen?](https://svazurich.ch/unsere-produkte/weitere-produkte/krankenversicherung--kvg-/krankenversicherungspflicht0/krankenversicherungspflicht-wer-hat-anspruch.html) | 4 |
| Canton of Zurich, Health Directorate | [Prämienverbilligung Krankenversicherung - Kanton Zürich](https://www.zh.ch/de/gesundheit/praemienverbilligung_krankenversicherung.html) | 4 |
| Canton of Zurich, Road Traffic Office | [So bereiten Sie sich gut auf Ihre Kontrollfahrt vor - Kanton Zürich](https://www.zh.ch/de/mobilitaet/fuehrerausweis-fahren-lernen/auslaendischer-fuehrerausweis/so-bereiten-sie-sich-gut-auf-ihre-kontrollfahrt-vor.html) | 4 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | [Sonderabfall-Sammelstelle - Stadt Zürich](https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/wo-und-wann-entsorgen/sonderabfall-sammelstelle.html) | 4 |
| ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery) | [Stimm- und Wahlrecht in der Schweiz](https://www.ch.ch/de/abstimmungen-und-wahlen/abstimmungen/stimm-und-wahlrecht/) | 4 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | [Abfuhr Bioabfall - Stadt Zürich](https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/wo-und-wann-entsorgen/abfuhr-bioabfall.html) | 3 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | [Abfuhr Sperrgut, Metall, Elektrogeräte und Grubengut - Stadt Zürich](https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/wo-und-wann-entsorgen/abfuhr-sperrgut-metall-elektro-grubengut.html) | 3 |
| City of Zurich, Naturalisation Division | [Einbürgerung und Stadtbürgerrecht - Stadt Zürich](https://www.stadt-zuerich.ch/de/lebenslagen/einwohner-services/einbuergerung.html) | 3 |
| Canton of Zurich, Office for Municipalities, Naturalisation Division | [Einbürgerungsgesuch einreichen - Kanton Zürich](https://www.zh.ch/de/migration-integration/einbuergerung/ordentliche-einbuergerung/einbuergerungsgesuch-einreichen.html) | 3 |
| State Secretariat for Migration SEM | [Entry/Exit System (EES)](https://www.sem.admin.ch/sem/de/home/themen/einreise/fachinfo-einreise/informationssysteme-schengen/ees.html) | 3 |
| State Secretariat for Migration SEM | [FAQ Aufenthalt und Integrationskriterien](https://www.sem.admin.ch/sem/de/home/themen/aufenthalt/faq.html) | 3 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | [Fedlex: Federal Constitution, SR 101](https://fedlex.data.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/1999/404/20240303/de/html/fedlex-data-admin-ch-eli-cc-1999-404-20240303-de-html-10.html) | 3 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | [Fedlex: Vested Benefits Act, SR 831.42](https://fedlex.data.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/1994/2386_2386_2386/20240101/de/html/fedlex-data-admin-ch-eli-cc-1994-2386_2386_2386-20240101-de-html-3.html) | 3 |
| City of Zurich, Protection and Rescue Zurich | [Medizinischer Notfall – richtig handeln - Stadt Zürich](https://www.stadt-zuerich.ch/de/stadtleben/notfall/notfaelle/medizinischer-notfall.html) | 3 |
| Canton of Zurich, Migration Office | [Migrationsamt - Kanton Zürich](https://www.zh.ch/de/sicherheitsdirektion/migrationsamt.html) | 3 |
| Canton of Zurich, Cantonal Tax Office | [Nachträgliche ordentliche Veranlagung beantragen - Kanton Zürich](https://www.zh.ch/de/steuern-finanzen/steuern/quellensteuer/nachtraegliche-ordentliche-veranlagung-oder-quellensteuerkorrekt.html) | 3 |
| City of Zurich, School Office | [Schulferien und schulfreie Tage - Stadt Zürich](https://www.stadt-zuerich.ch/de/bildung/volksschule/schulferien.html) | 3 |
| Canton of Zurich, Statistical Office, elections and votes | [So stimme ich ab - Kanton Zürich](https://www.zh.ch/de/politik-staat/wahlen-abstimmungen/so-stimme-ich-ab.html) | 3 |
| SVA Zürich, the cantonal social insurance office | [Telefon](https://svazurich.ch/ueber-uns/sva-zuerich/kontakt/telefon.html) | 3 |
| Canton of Zurich, Road Traffic Office | [Umzug innerhalb oder in den Kanton Zürich melden - Kanton Zürich](https://www.zh.ch/de/mobilitaet/fahrzeuge-kontrollschilder/umzug-melden.html) | 3 |
| ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery) | [Verlust, Diebstahl, Umtausch des Führerausweises in der Schweiz](https://www.ch.ch/de/ausweise-und-dokumente/fuhrerausweis/fuhrerausweis-umtauschen/) | 3 |
| Federal Department of Foreign Affairs FDFA | [Visabestimmungen für die Einreise in die Schweiz](https://www.eda.admin.ch/de/visabestimmungen-fuer-die-einreise-in-die-schweiz) | 3 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | [Wertstoff-Sammelstellen - Stadt Zürich](https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/wo-und-wann-entsorgen/wertstoff-sammelstellen.html) | 3 |
| City of Zurich, Population Office | [Zuzug in die Stadt Zürich - Stadt Zürich](https://www.stadt-zuerich.ch/de/lebenslagen/einwohner-services/umziehen-melden/zuzug.html) | 3 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | [Züri-Sack - Stadt Zürich](https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/zueri-sack.html) | 3 |
| SERAFE AG, the Confederation's collection agency for the radio and television fee | [Abgabeübersicht](https://www.serafe.ch/de/abgabe/abgabeuebersicht/) | 2 |
| City of Zurich, City Police | [Anmeldung eines Hundes bei der Wohngemeinde - Stadt Zürich](https://www.stadt-zuerich.ch/de/stadtleben/veranstaltungen-und-bewilligungen/hundekontrolle/anmeldung.html) | 2 |
| SVA Zürich, the cantonal social insurance office | [Beratung vor Ort](https://svazurich.ch/ueber-uns/sva-zuerich/kontakt/beratung-vor-ort.html) | 2 |
| State Secretariat for Migration SEM | [Der biometrische Ausländerausweis](https://www.sem.admin.ch/sem/de/home/themen/aufenthalt/biometr_auslaenderausweis.html) | 2 |
| State Secretariat for Migration SEM | [Einreise mit Visum](https://www.sem.admin.ch/sem/de/home/themen/einreise/info-einreise/voraussetzungen-nach-staat/mit-visum.html) | 2 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | [Entsorgungskalender - Stadt Zürich](https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/entsorgungskalender.html) | 2 |
| Canton of Zurich, Office for the Economy | [Erwerbstätigkeit von Ausländerinnen und Ausländern - Kanton Zürich](https://www.zh.ch/de/wirtschaft-arbeit/erwerbstaetigkeit-auslaender.html) | 2 |
| State Secretariat for Migration SEM | [FAQ – Fragen zur Personenfreizügigkeit](https://www.sem.admin.ch/sem/de/home/themen/fza_schweiz-eu-efta/eu-efta_buerger_schweiz/faq.html) | 2 |
| Canton of Zurich, Road Traffic Office | [Fahrzeug importieren - Kanton Zürich](https://www.zh.ch/de/mobilitaet/fahrzeuge-kontrollschilder/import-fahrzeuge/fahrzeug-importieren.html) | 2 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | [Fedlex: Constitution of the Canton of Zurich, SR 131.211](https://fedlex.data.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/2006/14_fga/20240701/de/html/fedlex-data-admin-ch-eli-cc-2006-14_fga-20240701-de-html-1.html) | 2 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | [Fedlex: Ordinance on the Admission of Persons and Vehicles to Road Traffic, SR 741.51](https://fedlex.data.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/1976/2423_2423_2423/20260101/de/html/fedlex-data-admin-ch-eli-cc-1976-2423_2423_2423-20260101-de-html-3.html) | 2 |
| SERAFE AG, the Confederation's collection agency for the radio and television fee | [Grundsatz](https://www.serafe.ch/de/abgabebefreiung/grundsatz/) | 2 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | [Kartonsammlung - Stadt Zürich](https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/wo-und-wann-entsorgen/kartonsammlung.html) | 2 |
| State Secretariat for Migration SEM | [Nicht-EU/EFTA-Angehörige](https://www.sem.admin.ch/sem/de/home/themen/arbeit/nicht-eu_efta-angehoerige.html) | 2 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | [Papiersammlung - Stadt Zürich](https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/wo-und-wann-entsorgen/papiersammlung.html) | 2 |
| City of Zurich, Traffic Department | [Parkbewilligungen - Stadt Zürich](https://www.stadt-zuerich.ch/de/mobilitaet/parkieren/parkbewilligungen.html) | 2 |
| City of Zurich, Traffic Department | [Parkscheibe für die Blaue Zone - Stadt Zürich](https://www.stadt-zuerich.ch/de/mobilitaet/parkieren/parkbewilligungen/parkscheibe.html) | 2 |
| State Secretariat for Migration SEM | [Regeln zur Berechnung der Aufenthaltsdauer](https://www.sem.admin.ch/sem/de/home/themen/einreise/info-einreise/voraussetzungen-nach-staat/mit-visum/aufenthaltsrechner.html) | 2 |
| City of Zurich, School Office | [Schulbotschafter*innen – Volksschule in verschiedenen Sprachen erklärt - Stadt Zürich](https://www.stadt-zuerich.ch/de/bildung/volksschule/schulorganisation/verschiedene-sprachen.html) | 2 |
| SVA Zürich, the cantonal social insurance office | [Spezielle Öffnungszeiten](https://svazurich.ch/ueber-uns/sva-zuerich/kontakt/oeffnungszeiten-ueber-die-feiertage.html) | 2 |
| Canton of Zurich, Road Traffic Office | [Strassenverkehrsamt - Kanton Zürich](https://www.zh.ch/de/sicherheitsdirektion/strassenverkehrsamt.html) | 2 |
| Canton of Zurich, Cantonal Tax Office | [Zurich: tax-at-source tariffs from 2026, basis and calculation parameters (PDF)](https://www.zh.ch/content/dam/zhweb/bilder-dokumente/themen/steuern-finanzen/steuern/quellensteuer/quellensteuertarif/2026/grundlagen_und_berechnungsparameter_2026.pdf) | 2 |
| Canton of Zurich, Office for the Economy | [Amt für Wirtschaft - Kanton Zürich](https://www.zh.ch/de/volkswirtschaftsdirektion/amt-fuer-wirtschaft.html) | 1 |
| City of Zurich, Traffic Department | [Anwohnerparkkarte für Privatpersonen und Firmen - Stadt Zürich](https://www.stadt-zuerich.ch/de/mobilitaet/parkieren/parkbewilligungen/anwohnerparkkarte.html) | 1 |
| Canton of Zurich, Migration Office | [Aufenthalt ohne Erwerbstätigkeit für Drittstaatsangehörige - Kanton Zürich](https://www.zh.ch/de/migration-integration/aufenthalt/aufenthalt-ohne-erwerbstaetigkeit-fuer-drittstaatsangehoerige.html) | 1 |
| State Secretariat for Migration SEM | [Einreisevoraussetzungen nach Staatsangehörigkeit](https://www.sem.admin.ch/sem/de/home/themen/einreise/info-einreise/voraussetzungen-nach-staat.html) | 1 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | [Fedlex: ordinance on the refund of AHV contributions paid by foreign nationals, SR 831.131.12](https://fedlex.data.admin.ch/filestore/fedlex.data.admin.ch/eli/cc/1996/688_688_688/20250101/de/html/fedlex-data-admin-ch-eli-cc-1996-688_688_688-20250101-de-html-4.html) | 1 |
| SVA Zürich, the cantonal social insurance office | [Kontakt](https://svazurich.ch/ueber-uns/sva-zuerich/kontakt.html) | 1 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | [Kunststoffsammlung - Stadt Zürich](https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/wo-und-wann-entsorgen/kunststoffsammlung.html) | 1 |
| Canton of Zurich, Migration Office | [Organisation - Kanton Zürich](https://www.zh.ch/de/sicherheitsdirektion/migrationsamt/organisation.html) | 1 |
| Canton of Zurich, Cantonal Tax Office | [Quellensteuer - Kanton Zürich](https://www.zh.ch/de/steuern-finanzen/steuern/quellensteuer.html) | 1 |
| State Secretariat for Migration SEM | [Residence](https://www.sem.admin.ch/sem/en/home/themen/aufenthalt.html) | 1 |
| State Secretariat for Migration SEM | [Schengen-Raum](https://www.sem.admin.ch/sem/de/home/themen/einreise/fachinfo-einreise/schengen.html) | 1 |
| Central Compensation Office CCO | [Staatsangehörigkeit eines Staates mit Sozialversicherungsabkommen (AHV)](https://www.zas.admin.ch/de/staatsangehoerigkeit-eines-staates-mit-sozialversicherungsabkommen-ahv) | 1 |
| Canton of Zurich, Cantonal Tax Office | [Steueramt - Kanton Zürich](https://www.zh.ch/de/finanzdirektion/steueramt.html) | 1 |
| City of Zurich, Traffic Department | [Tagesbewilligungen - Stadt Zürich](https://www.stadt-zuerich.ch/de/mobilitaet/parkieren/parkbewilligungen/tagesbewilligungen.html) | 1 |
| State Secretariat for Migration SEM | [Visumantragsformular](https://www.sem.admin.ch/sem/de/home/themen/einreise/visumantragsformular.html) | 1 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | [Wo und wann entsorgen - Stadt Zürich](https://www.stadt-zuerich.ch/de/umwelt-und-energie/entsorgung/wo-und-wann-entsorgen.html) | 1 |

Not covered, and answered as out of coverage:

- Other topics: schooling beyond kindergarten entry and school holidays, asylum, family allowances, parental income compensation, other social insurance benefits, housing and rent, and utilities.
- Fees and appointment availability for any permit.
- Annual quotas, the detailed procedure, forms, appointments and fees of an office or of a Swiss representation, processing times, documents beyond those listed on a covered page, the visa rules of an individual nationality (SEM's Annex CH-1 lists) and airport-transit visas.
- Tax tariff tables, rates and deductions, amounts of tax, refunds, pensions, premiums, premium reductions, dog tax or allowances beyond the served statements; calculators.
- Cantons other than Zurich beyond their migration-office contact, and municipal procedures outside the City of Zurich; federal rules still apply there and are served with a caveat.
- Eligibility decisions for a specific person: the rules route population groups to pre-authored statements and compute no outcome.
- Live data such as current processing times, appointment slots or insurer premiums.
- Any country other than Switzerland, including German and Austrian rules that look similar.

## Run the container

```shell
docker run --rm -p 8000:8000 ghcr.io/swisstip/swiss-tip:mvp-zurich-2026-09-18-v10
```

| Address | What it serves |
| --- | --- |
| `http://127.0.0.1:8000/mcp` | The MCP endpoint (Streamable HTTP) |
| `http://127.0.0.1:8000/health` | The release ID, counts, jurisdictions, languages, freshness, review status, readiness (who attested the release and when) and the configured search mode as JSON |
| `http://127.0.0.1:8000/` | The server name, release ID and endpoint paths |

```shell
curl http://127.0.0.1:8000/health
```

Options:

- **Tags.** `mvp-zurich-2026-09-18-v10` names the release;
  `content-d0dd18b09eee` names its content digest; `mvp-zurich` is the
  pack's current release and `latest` the most recent release. A new release
  is a new image with new tags; the release inside a release tag never
  changes, even when the tag is rebuilt for a server fix.
- **Search.** Hybrid: lexical matching over labels, aliases and source terms,
  fused with the ranking of a bundled local embedding model
  (`qwen3-embedding:0.6b` on a CPU-only Ollama inside the container, on the
  loopback address only). `search.configured_mode` in `/health` reports it;
  the first search after a start loads the model and takes a few seconds.
  The image is about 700 MB and starts in about ten seconds.
- **Calendars.** The calendar connector runs beside the server in the
  same container, on the loopback address only, and is registered before
  the server starts: `connectors` in `/health` lists its 15 calendars.
  `docker run --rm -p 8000:8000 -e SWISSTIP_CONNECTORS= <image>` leaves it
  out, and the server lists the four other tools.
- **Port.** The server listens on `$PORT`, 8000 by default:
  `docker run --rm -e PORT=9000 -p 9000:9000 <image>`. Hosts that set `PORT`
  themselves (for example Google Cloud Run) need no extra setting.
- **Local network.** The server binds all interfaces inside the container,
  so a notebook running the image serves every machine that can reach it:
  clients use `http://<host-address>:8000/mcp`. Allow the port in the host's
  firewall if it blocks incoming connections.
- **stdio.** `docker run --rm -i <image> --transport stdio` serves MCP over
  standard input and output instead, for clients that only start local
  processes.
- **Health report.** `docker run --rm <image> --health` validates the release
  and prints the health JSON.
- **Readiness.** The image serves only a release with a matching readiness
  record (`/srv/swiss-tip/readiness.json`, written when the release passed
  its acceptance gate: validation, no dropped fact, the fixed acceptance
  cases, a freshness runway). The server starts with `--require-ready` and
  refuses a release without one; `readiness` in the health JSON names the
  person and time of the attestation.
- **Logs.** One line per tool call on standard error, with tool, status,
  bytes, latency and release ID: `docker logs <container>`.
- **Help.** `docker run --rm <image> --help` lists every option.

The image runs as an unprivileged user, declares a Docker `HEALTHCHECK` on
`/health`, and speaks plain HTTP; put HTTPS in front of it (the container
host's load balancer or a reverse proxy) when it is reachable beyond a
trusted local network. The endpoint is stateless, so any number of replicas can serve it
without session affinity.

### Two containers

The slim image `ghcr.io/swisstip/swiss-tip:mvp-zurich-2026-09-18-v10-slim`
(moving tag `mvp-zurich-slim`, about 60 MB to pull) carries the same server,
release and semantic index without Ollama and the model. On its own it
serves lexical search. Hybrid search comes from the embedding sidecar
`ghcr.io/swisstip/swiss-tip-ollama:qwen3-embedding-0.6b`, the same
CPU-only Ollama and model in a container of its own, which joins the server's
network namespace; the model stays on the loopback address and is reachable
from nowhere else. With the repository's `compose.yaml`, which needs no
other file:

```shell
docker compose up -d --wait
```

Or with Docker alone:

```shell
docker run -d --name swiss-tip -p 8000:8000 ghcr.io/swisstip/swiss-tip:mvp-zurich-2026-09-18-v10-slim \
  --semantic-index /srv/swiss-tip/semantic-index.json
docker run -d --name swiss-tip-embeddings --network container:swiss-tip \
  ghcr.io/swisstip/swiss-tip-ollama:qwen3-embedding-0.6b
```

The addresses, the tools and the answers are those of the single image. If
the sidecar is not running, the server keeps serving and every search
reports `retrieval_mode: lexical-fallback` with the reason.

## Connect a client

The examples use `http://127.0.0.1:8000/mcp`; replace it with the URL where
the container is reachable. The OpenCode configuration below was tested
against this image on 18 September 2026; the other clients follow their
published configuration formats and have not been tested here.

### OpenCode

In `opencode.json` of the project, or `~/.config/opencode/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "swiss_tip": {
      "type": "remote",
      "url": "http://127.0.0.1:8000/mcp",
      "enabled": true,
      "timeout": 60000
    }
  }
}
```

`opencode mcp list` should show `swiss_tip connected`. The tools appear as
`swiss_tip_get_coverage`, `swiss_tip_search`, `swiss_tip_resolve` and
`swiss_tip_get_evidence`.

### Claude Code

```shell
claude mcp add --transport http swiss-tip http://127.0.0.1:8000/mcp
```

### VS Code

In `.vscode/mcp.json`:

```json
{
  "servers": {
    "swiss-tip": { "type": "http", "url": "http://127.0.0.1:8000/mcp" }
  }
}
```

### Other clients with an `mcpServers` file

Clients that connect to a URL (for example Cursor):

```json
{
  "mcpServers": {
    "swiss-tip": { "url": "http://127.0.0.1:8000/mcp" }
  }
}
```

Clients that only start a local process (for example Claude Desktop) run the
image over stdio; Docker must be installed where the client runs:

```json
{
  "mcpServers": {
    "swiss-tip": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "ghcr.io/swisstip/swiss-tip:mvp-zurich-2026-09-18-v10", "--transport", "stdio"]
    }
  }
}
```

### Try it

Questions the release is built to ground:

- I'm a Czech citizen and starting my work in Zurich next week. By when
  latest should I register my stay on the municipal authority?
- Ich habe die indische Staatsbürgerschaft. Darf ich in der Schweiz
  arbeiten? Welche Voraussetzungen gelten für eine Arbeitsbewilligung und
  eine Aufenthaltsbewilligung?
- I'm a Spanish citizen with a B permit working in Zurich, gross salary
  CHF 135,000. Tax is deducted at source. Do I have to file a tax return?
- I moved from California to Zurich 14 months ago and still drive on my US
  licence. Am I still allowed to, and can I still exchange it?
- I'm a Turkish citizen and have lived in Switzerland for eleven years, the
  last eighteen months in the city of Zurich. I hold a B permit. Can I apply
  for Swiss citizenship now?

A well-behaved caller reads `get_coverage` once, searches in English or
German (a French question is best searched with English or German
terms), calls `resolve` with the place the user named (`{"city": "Zurich"}`
is enough: the server turns it into the codes and echoes what it understood
in `executed_scope`) and the context the concept asks for, asks the user for a missing fact instead of guessing (for the first
question: the arrival date and the first working day), cites the returned
URLs, and declines what the coverage names as out of scope. The tool
descriptions and each result's `guidance_for_caller` say the same to the
model. Asking the assistant to answer in the language of the question helps:
without that instruction, models have answered in another language.

## Limitations

- Every statement was written by an assistant reading the cited page and
  checked by one reviewer against its excerpt. It is not legal advice and not
  a legal review; English statements paraphrase the original text and are not
  official translations.
- The server routes population groups to published statements; it does not
  decide a specific person's eligibility.
- Freshness counts from the date the page was accessed, not from a check
  that the page is unchanged. From 17 November 2026 results are marked `STALE`.
- The added topics are published for the Canton and City of Zurich; for
  another canton only their federal facts are served.
- A place is recognised by the official name of its municipality or canton,
  and by the other-language names of the cantons and larger cities. A
  quarter, a postcode or a misspelling is not: the request then runs for the
  canton or the country and the result says so.
- The endpoint has no authentication, rate limiting or usage accounting;
  anyone who can reach it can call it. It serves only the public information
  of the release.

## Licence

The software is licensed under the Apache License, Version 2.0. The excerpts
in the release reproduce official publications of the Swiss Confederation
(SEM, Fedlex, FOPH, ESTV, BSV and the Central Compensation Office ZAS), the
ch.ch portal of the Confederation, cantons and communes, the Canton of
Zurich, the City of Zurich and the SVA Zurich as cited evidence, with their
source URLs and access dates; they remain the property of their publishers.
The image carries the release files only (`/srv/swiss-tip/release.json`,
`readiness.json`, `semantic-index.json`); the `LICENSE` and `NOTICE` files
are in the repository.
