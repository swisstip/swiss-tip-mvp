# Basis review of the mvp-wallisellen release

**Last update:** 16 September 2026

Rows assigned on release `mvp-wallisellen-2026-09-16-v2` and served unchanged by release `mvp-wallisellen-2026-09-16-v3`, content digest `67b174b641ef997729c69241ab178be2cfde93f65f9f7c6be250075181f04799`, 99 facts, 99 excerpts, 48 documents.

What this is: the institution of every cited page and the basis of every served excerpt, assigned on 16 September 2026 by four assistant subagents (Claude Sonnet) inside Claude Code. Each applied the concept-extraction package's classification prompt `packages/concepts/src/swisstip/concepts/prompts/basis_classification_v1.md` verbatim to one page at a time, in the payload shape of the pipeline's basis call (title, source URL, language, and per excerpt the concept label, the statement, the heading path and the quote), and read the page's reading view to name the office the page itself gives as responsible. No model API was called; the coordinating session checked that every excerpt got exactly one answer and wrote the result into `curation.yaml` beside this file (the `institutions` block and the `basis` of each citation), from which the build derives the served labels. The classification is a model assessment. Alexander Bobrovsky confirmed every row, together with every fact statement, on 16 September 2026; the assistant recorded the confirmation on each fact (`reviewed_by`, a `review:` note) on the reviewer's instruction and the release was attested in the reviewer's name.

Reading rules applied, beyond the prompt: a list of contacts, offices, telephone numbers or locations (collection points, playgrounds, rentable rooms, the council roster) is `directory`; a Wallisellen page in its own words is municipal even where it describes a cantonal service (the careers advice page about biz Kloten) or the school (Schule Wallisellen). An institution is registered only for an office the page names as its own contact; every other page is attributed to the City of Wallisellen as a whole.

## Summary

| Measure | Value |
| --- | --- |
| Excerpts by basis kind | 23 directory, 76 guidance |
| Facts by their strongest basis | 23 directory, 76 guidance |
| Documents by institution | 48 municipal: 40 Stadt Wallisellen; 3 Stadt Wallisellen, Tiefbau + Landschaft, Umwelt; 2 Stadt Wallisellen, Stadtratskanzlei; 1 Stadt Wallisellen, Bevölkerungsdienste; 1 Stadt Wallisellen, Familien und Freiwillige; 1 Stadt Wallisellen, Steuern |
| Excerpts that reproduce a norm (act, ordinance, treaty, directive) | 0 |
| Guidance excerpts naming a norm | 1: `e-population-services-3-1` (revidierte Hundeverordnung (per 1. Juni 2025)) |
| Concepts whose facts mix basis kinds | 6: `civil-status-and-naturalisation`, `facilities-museum-and-culture`, `municipal-tax-services`, `naturalisation`, `schools-and-careers`, `waste-disposal-services` |
| Validation issues | 0 |

Pages that name no office of their own (the generic Stadtverwaltung contact in the header and footer only) are attributed to the city. The waste pages that name no office (the calendar and green-waste PDFs, Abfallsammlung, Abfallarten, Sammelstellen) stay with the city, although the calendar gives the disposal telephone of Tiefbau + Landschaft, Umwelt, because they do not name the office. The bulky-waste-stamp leaflet names the department Tiefbau + Landschaft without the unit Umwelt and is attributed to the same registry entry. The Ortsmuseum page names the museum's own contact, which is a facility, not the publisher; the naturalisation subpages name the Stadtratskanzlei in their table of responsible areas.

## Institutions

| Institution | Native name | Level | Jurisdiction | Documents | Excerpts |
| --- | --- | --- | --- | ---: | ---: |
| City of Wallisellen, Population Services | Stadt Wallisellen, Bevölkerungsdienste | municipal | CH-ZH-69 | 1 | 1 |
| City of Wallisellen | Stadt Wallisellen | municipal | CH-ZH-69 | 40 | 78 |
| City of Wallisellen, Families and Volunteers | Stadt Wallisellen, Familien und Freiwillige | municipal | CH-ZH-69 | 1 | 1 |
| City of Wallisellen, City Council Chancellery | Stadt Wallisellen, Stadtratskanzlei | municipal | CH-ZH-69 | 2 | 7 |
| City of Wallisellen, Tax Office | Stadt Wallisellen, Steuern | municipal | CH-ZH-69 | 1 | 7 |
| City of Wallisellen, Civil Engineering and Landscape (Environment) | Stadt Wallisellen, Tiefbau + Landschaft, Umwelt | municipal | CH-ZH-69 | 3 | 5 |

## Every excerpt

Grouped by page. `Rule` says which rule produced the basis: here always the citation's own entry. `Office named by the page` is what the page states, copied by the classifier.

### Wallisellen

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/>

Office named by the page: none - Homepage with no single responsible department named; only the generic city footer contact appears.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-digital-city-services-1-1` | CH-ZH-69 | Municipal authority guidance | citation | Homepage's own description of the Online-Schalter service. |
| `e-digital-city-services-2-1` | CH-ZH-69 | Municipal authority guidance | citation | Homepage's own routing text pointing to the eUmzugCH portal. |
| `e-digital-city-services-3-1` | CH-ZH-69 | Municipal authority guidance | citation | Homepage's own short description linking to the emergency-numbers page. |

### Waste information leaflet (PDF)

Publisher: City of Wallisellen, Civil Engineering and Landscape (Environment) (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch/_doc/4212374; page: <https://www.wallisellen.ch/_doc/4212374>

Office named by the page: Tiefbau + Landschaft, Umwelt - The PDF's header names Tiefbau + Landschaft, Umwelt as the issuing office of this waste-information leaflet.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-waste-set-out-rules-and-fees-1-1` | CH-ZH-69 | Municipal authority guidance | citation | The evidence is the city's own waste-information leaflet explaining sorting rules, set-out times, fees and sales points in its own words, not a reproduced legal provision. |

### Green waste leaflet (PDF)

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/_doc/4236797>

Office named by the page: none - The leaflet carries no header, Kontakt block or department name identifying a responsible office.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-waste-set-out-rules-and-fees-5-1` | CH-ZH-69 | Municipal authority guidance | citation | The quote is the city's own multilingual instruction that compostable, not plastic, bags must be used for organic waste, an explanation rather than a reproduced legal text. |

### Waste calendar 2026 (PDF)

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/_doc/6512240>

Office named by the page: none - The PDF names no responsible department by title; it only gives a general disposal phone (044 832 62 10) and the environment office's e-mail (umwelt@wallisellen.ch) for service registrations, with no Kontakt or Zustaendige Stelle block.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-waste-disposal-services-5-1` | CH-ZH-69 | Municipal authority directory | citation | The quote is a map legend listing collection-point street names plus a phone number, a list of locations rather than an explanation of a rule. |
| `e-waste-disposal-services-6-1` | CH-ZH-69 | Municipal authority guidance | citation | The quote is the city's own bullet-point explanation of what each waste service (ReparierBar, Bring- und Holboerse, Hauptsammelstelle) accepts, its hours and its rules. |
| `e-waste-set-out-rules-and-fees-3-1` | CH-ZH-69 | Municipal authority guidance | citation | The quote gives the city's own instructions on how and when to set out household, green, cardboard and paper waste, a procedure explanation in its own words. |
| `e-waste-set-out-rules-and-fees-4-1` | CH-ZH-69 | Municipal authority guidance | citation | The quote explains registration, accepted/rejected items and fees for the chipping, metal and special-waste mobile services in the city's own words. |

### Bulky waste stamps leaflet 2025 (PDF)

Publisher: City of Wallisellen, Civil Engineering and Landscape (Environment) (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch/_doc/7129504; page: <https://www.wallisellen.ch/_doc/7129504>

Office named by the page: Tiefbau + Landschaft - The department name 'Tiefbau + Landschaft' appears directly under the leaflet's title in the PDF header.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-waste-collection-schedule-1-1` | CH-ZH-69 | Municipal authority guidance | citation | Instruction leaflet in the department's own words; no article or marginal number identifies a directive's norm. |
| `e-waste-set-out-rules-and-fees-2-1` | CH-ZH-69 | Municipal authority guidance | citation | Same leaflet's own-words rules on size, weight and fees, without a legal citation to support directive or act classification. |

### Wallisellen - Einbürgerung Schweizerin / Schweizer

Publisher: City of Wallisellen, City Council Chancellery (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch/_rte/thema2/1566; page: <https://www.wallisellen.ch/_rte/thema2/1566>

Office named by the page: Stadtratskanzlei - The same 'Zugehörige Objekte' block as the foreign-nationals naturalisation page names Stadtratskanzlei, under the Präsidiales Abteilung, as responsible.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-naturalisation-6-1` | CH-ZH-69 | Municipal authority guidance | citation | Own-words requirements and document list for Swiss-citizen naturalisation, without a legal citation. |

### Wallisellen - Einbürgerung Ausländerin / Ausländer

Publisher: City of Wallisellen, City Council Chancellery (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch/_rte/thema2/1567; page: <https://www.wallisellen.ch/_rte/thema2/1567>

Office named by the page: Stadtratskanzlei - The page's 'Zugehörige Objekte' block names Stadtratskanzlei as the responsible Bereich, under the Präsidiales Abteilung, with matching phone and email in both tables.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-naturalisation-1-1` | CH-ZH-69 | Municipal authority guidance | citation | City's own plain-language list of ordinary-naturalisation requirements, with no cited article. |
| `e-naturalisation-2-1` | CH-ZH-69 | Municipal authority guidance | citation | Own-words list of documents required for the application, not a legal text. |
| `e-naturalisation-3-1` | CH-ZH-69 | Municipal authority guidance | citation | Explanatory footnote in the city's own words about when tests are waived, without a legal citation. |
| `e-naturalisation-4-1` | CH-ZH-69 | Municipal authority guidance | citation | Procedure steps described by the city in its own words. |
| `e-naturalisation-5-1` | CH-ZH-69 | Municipal authority guidance | citation | Own-words list of facilitated-naturalisation requirements, without citing an article. |
| `e-naturalisation-7-1` | CH-ZH-69 | Municipal authority directory | citation | Table naming an office with phone number and email for the naturalisation topic. |

### Wallisellen - Abfallarten

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/abfallarten>

Office named by the page: none - The page only carries the generic sitewide Stadtverwaltung footer contact; no page-specific responsible office is named for the waste-category list.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-waste-categories-1-1` | CH-ZH-69 | Municipal authority guidance | citation | The quote is the city's own catalogue of collected waste categories under Das wird gesammelt, an informational listing of materials rather than an office or location directory. |

### Wallisellen - Sammelstellen

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/abfallorte>

Office named by the page: none - The page only carries the generic sitewide Stadtverwaltung footer contact; no page-specific responsible office is named for the collection-points list.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-waste-disposal-services-4-1` | CH-ZH-69 | Municipal authority directory | citation | The quote is a bare list of collection-point location names. |

### Wallisellen - Abfallsammlungen

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/abfallsammlung>

Office named by the page: none - The page names no department responsible for waste collection; the only contact given is the generic city-wide 'Kontakt' block (Stadt Wallisellen, Zentralstr. 9, 8304 Wallisellen) repeated in the header and footer, which is the city's general switchboard, not a page-specific office.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-waste-disposal-services-3-1` | CH-ZH-69 | Municipal authority guidance | citation | The quote is the city's own collection-schedule table and calendar-import feature under 'Besondere Sammeltermine', an operational procedure page in the municipality's own words, not a reproduced provision or an office directory. |
| `e-waste-collection-schedule-2-1` | CH-ZH-69 | Municipal authority guidance | citation | The quote is the same municipal collection-dates table listing service types, dates and areas, a procedure/schedule page in the city's own words, not legislation or an office directory. |
| `e-waste-collection-schedule-3-1` | CH-ZH-69 | Municipal authority guidance | citation | The quote is the same municipal collection-dates table, a schedule of the city's own waste service rather than a reproduced legal text or a list of offices. |
| `e-waste-collection-schedule-4-1` | CH-ZH-69 | Municipal authority guidance | citation | The quote is the same municipal collection-dates table, an operational schedule authored by the city, not a provision or an office directory. |
| `e-waste-collection-schedule-5-1` | CH-ZH-69 | Municipal authority guidance | citation | The quote is the same municipal collection-dates table, a service schedule in the city's own words, not a reproduced legal provision. |
| `e-waste-collection-schedule-6-1` | CH-ZH-69 | Municipal authority guidance | citation | The quote is the same municipal collection-dates table listing cardboard pickup dates, an operational schedule, not legislation or a directory of offices. |
| `e-waste-collection-schedule-7-1` | CH-ZH-69 | Municipal authority guidance | citation | The quote is the same municipal collection-dates table listing paper-collection dates, a schedule in the city's own words, not a reproduced provision. |
| `e-waste-collection-schedule-8-1` | CH-ZH-69 | Municipal authority guidance | citation | The quote is the same municipal collection-dates table listing special one-off collection services, an operational schedule authored by the city, not a legal provision or an office directory. |

### Wallisellen - Bereiche

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/aemter>

Office named by the page: none - The page lists all of the city's departments and areas side by side with their own phone numbers and e-mails; no single office is presented as responsible for the page itself.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-administration-contacts-2-1` | CH-ZH-69 | Municipal authority directory | citation | The quote is a table of department names with phone numbers and e-mail addresses. |

### Wallisellen - Alter

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/alter>

Office named by the page: none - No Kontakt or Zuständige-Stelle block names a responsible department; only the generic city footer contact appears.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-older-resident-services-1-1` | CH-ZH-69 | Municipal authority guidance | citation | City's own description of the foundation-funded LUNAplus offer, not a legal text. |
| `e-older-resident-services-2-1` | CH-ZH-69 | Municipal authority guidance | citation | Own-words summaries of several services for older residents across sub-sections of the page. |
| `e-older-resident-services-3-1` | CH-ZH-69 | Municipal authority guidance | citation | Routing sentence describing what the social-insurance and finance section covers. |

### Wallisellen - Bauen in Wallisellen

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/bauenwallisellen>

Office named by the page: none - The page only carries the generic sitewide Stadtverwaltung footer contact; no Kontakt or Zustaendige Stelle block names an office for the REK or Baubewilligungen content.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-building-and-spatial-planning-1-1` | CH-ZH-69 | Municipal authority guidance | citation | The quote is the city's own description of the REK as a preparatory instrument for revising land-use planning and where to find information and participation. |
| `e-building-and-spatial-planning-2-1` | CH-ZH-69 | Municipal authority guidance | citation | The quote is the entry-page question inviting people who want to build or convert something, the city's own procedure-page wording. |

### Wallisellen

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/berufsberatung>

Office named by the page: biz Kloten - The page itself states that biz Kloten, the cantonal careers information centre, is responsible for Wallisellen, not a city department.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-schools-and-careers-2-1` | CH-ZH-69 | Municipal authority directory | citation | The evidence names one office with its address and telephone; the text is Wallisellen's own referral note about biz Kloten, not authored by biz Kloten itself. |

### Wallisellen - Bevölkerungsdienste

Publisher: City of Wallisellen, Population Services (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch/bevoelkerungsdienste; page: <https://www.wallisellen.ch/bevoelkerungsdienste>

Office named by the page: Bevölkerungsdienste - The page's own title and breadcrumb name Bevölkerungsdienste as the unit whose services the page lists; no separate Kontakt block overrides it.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-population-services-1-1` | CH-ZH-69 | Municipal authority guidance | citation | Own-words listing of population-services entry points (permits, certificates, dogs, data block), not a legal text or contact directory. |

### Wallisellen - Weitere Bildungsinstitutionen

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/bildungprivateschulen>

Office named by the page: none - The listed schools (International School Zurich North, SIS, Bambus Privatschule) are private institutions, not city administration; no city office is named as responsible for the page.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-schools-and-careers-3-1` | CH-ZH-69 | Municipal authority directory | citation | List of private-school names, addresses and phone/fax numbers compiled by the city page. |

### Wallisellen

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/bildungueber>

Office named by the page: Schule Wallisellen - Schule Wallisellen is named as responsible for its own services, but the Budget/Rechnung page shows it is the separate Schulgemeinde (school corporation), distinct from the Politische Gemeinde / Stadt Wallisellen administration.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-schools-and-careers-1-1` | CH-ZH-69 | Municipal authority guidance | citation | Own-words note that Schule Wallisellen has its own website, listing further services it offers. |

### Wallisellen - Budget / Rechnung

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/budget>

Office named by the page: none - No responsible department is named; only the generic city footer contact appears.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-tax-rate-and-finance-2-1` | CH-ZH-69 | Municipal authority guidance | citation | City-published budget and accounts table, a factual report rather than a legal provision. |

### Wallisellen - Abteilungen

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/departemente>

Office named by the page: none - This page is itself a directory of the city's departments; no single office is stated as responsible for the page.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-administration-contacts-1-1` | CH-ZH-69 | Municipal authority directory | citation | The evidence is a table listing the city's departments with their telephone numbers and e-mail addresses. |

### Wallisellen - Einbürgerungen

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/einbuergerung>

Office named by the page: none - The page sits under the Bevölkerungsdienste navigation category but states no explicit responsible office or contact of its own; only the generic site-wide footer contact appears.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-civil-status-and-naturalisation-2-1` | CH-ZH-69 | Municipal authority directory | citation | The evidence is a bare pair of entry-point headings (for foreign and Swiss nationals) with no explanatory text. |

### Wallisellen - Energie und Klima

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/energie>

Office named by the page: none - No page-specific responsible office is named beyond the generic site-wide footer contact; the werke versorgung wallisellen ag mentioned is the external local energy supplier, not the page's author.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-energy-and-climate-1-1` | CH-ZH-69 | Municipal authority guidance | citation | The page states the Energiestadt label and Gold award in its own words. |
| `e-energy-and-climate-2-1` | CH-ZH-69 | Municipal authority guidance | citation | The page describes its own funding programme for climate-compatible investments in its own words. |
| `e-energy-and-climate-3-1` | CH-ZH-69 | Municipal authority guidance | citation | The page describes municipal energy planning and names the local energy supplier in its own words. |

### Wallisellen - Entsorgung

Publisher: City of Wallisellen, Civil Engineering and Landscape (Environment) (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch/entsorgung; page: <https://www.wallisellen.ch/entsorgung>

Office named by the page: Tiefbau + Landschaft, Umwelt - The page's own Kontakt block names Tiefbau + Landschaft, Umwelt as responsible.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-waste-disposal-services-1-1` | CH-ZH-69 | Municipal authority directory | citation | The evidence is a bare listing of two named reuse offerings (Bring- und Holbörse, ReparierBar) without explanation. |
| `e-waste-disposal-services-2-1` | CH-ZH-69 | Municipal authority guidance | citation | The page explains, in its own words, how to import or subscribe to collection reminders, with a contact line appended. |

### Wallisellen - Familien

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/familien>

Office named by the page: none - No page-specific responsible office is named; only the generic site-wide footer contact appears.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-family-support-and-childcare-1-1` | CH-ZH-69 | Municipal authority guidance | citation | The page states, in its own words, that parents can find counselling in the municipality. |
| `e-family-support-and-childcare-2-1` | CH-ZH-69 | Municipal authority guidance | citation | The page describes its own range of childcare offerings in its own words. |

### Wallisellen - Freiwilligenarbeit

Publisher: City of Wallisellen, Families and Volunteers (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch/freiwilligenarbeit; page: <https://www.wallisellen.ch/freiwilligenarbeit>

Office named by the page: Familien und Freiwillige - The page's own Kontakt block names Familien und Freiwillige, with its address, phone and e-mail, as the office for the volunteering contact point.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-youth-and-volunteering-3-1` | CH-ZH-69 | Municipal authority guidance | citation | The quote is the city's own explanation of what the volunteering contact point does, with its office contact appended, an explanatory page rather than a bare directory entry. |

### Wallisellen - Ortsmuseum

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/freizeitortsmuseum>

Office named by the page: Ortsmuseum - The page names the Ortsmuseum itself, run by a Leiterin with a wallisellen.ch address, as the entity behind the content; no separate department is named.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-facilities-museum-and-culture-2-1` | CH-ZH-69 | Municipal authority guidance | citation | The evidence is the museum's own descriptive prose about its history, exhibits, address and opening hours, not a list of multiple offices. |
| `e-facilities-museum-and-culture-5-1` | CH-ZH-69 | Municipal authority guidance | citation | Same museum information block; the phone and e-mail sit inside the museum's own descriptive text rather than a multi-entry contact list. |

### Wallisellen - Geburt, Zivilstand, Tod

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/geburtehetod>

Office named by the page: none - The page names 'Bestattungsamt' only for the death-notification subtopic, alongside a separate Zivilstandswesen section with no named office, so no single responsible office is recorded for the document as a whole.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-civil-status-and-naturalisation-1-1` | CH-ZH-69 | Municipal authority guidance | citation | Own-words instruction to contact the Bestattungsamt upon a death, a procedural direction rather than a legal citation. |

### Wallisellen - Gesundheit

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/gesundheit>

Office named by the page: none - No page-specific responsible office is named; only the generic site-wide footer contact appears.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-health-and-care-1-1` | CH-ZH-69 | Municipal authority guidance | citation | The page introduces its own links on defibrillators, emergency behaviour and numbers in its own words. |
| `e-health-and-care-2-1` | CH-ZH-69 | Municipal authority guidance | citation | The page describes its own care-provision information point and care concept in its own words. |

### Wallisellen - Jugend

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/jugend>

Office named by the page: none - No page-specific responsible office is named; only the generic site-wide footer contact appears.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-youth-and-volunteering-1-1` | CH-ZH-69 | Municipal authority guidance | citation | The page describes the Impact8304 platform's purpose in its own words. |
| `e-youth-and-volunteering-2-1` | CH-ZH-69 | Municipal authority guidance | citation | The page describes the Jugendtreff Rotacker and mobile youth work in its own words. |

### Wallisellen - Kulturförderung

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/kulturfoerderung>

Office named by the page: none - No page-specific responsible office is named; only the generic site-wide footer contact appears.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-facilities-museum-and-culture-3-1` | CH-ZH-69 | Municipal authority guidance | citation | The page describes its own funding priorities for cultural and sporting associations and youth work in its own words. |

### Wallisellen - Naherholung in Wallisellen

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/naherholung>

Office named by the page: none - The page only carries the generic sitewide Stadtverwaltung footer contact; no page-specific responsible office is named for the recreation-places list.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-recreation-sport-and-playgrounds-1-1` | CH-ZH-69 | Municipal authority directory | citation | The quote is a list of nearby recreation-area location names. |

### Wallisellen - Online-Schalter

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/online-schalter>

Office named by the page: none - No responsible-office block is present; the page is a plain listing of online services with only the generic city footer contact.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-digital-city-services-4-1` | CH-ZH-69 | Municipal authority guidance | citation | The city's own structured listing of online-counter services and forms, not a directory of offices or contacts. |

### Wallisellen - Stadtrat

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/politik>

Office named by the page: none - The page presents the city council's members and portfolios; it names no department as responsible for publishing the page itself.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-city-council-1-1` | CH-ZH-69 | Municipal authority directory | citation | The quote is a table listing council members' names, functions and Ressort (portfolio) assignments, a roster of office holders rather than an explanation. |

### Wallisellen - Stadtrat

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/politikueber>

Office named by the page: none - The page lists the city council itself (the elected executive body) rather than naming a single administrative office responsible for the page.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-city-council-2-1` | CH-ZH-69 | Municipal authority directory | citation | Roster table of city council members with their function and department (Ressort), a directory-style listing of office holders. |

### Wallisellen - Wallisellen im Überblick

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/portraitkennzahlen>

Office named by the page: none - The page cites the canton's Statistisches Amt as its data source but names no city office responsible for the page itself.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-wallisellen-profile-1-1` | CH-ZH-69 | Municipal authority guidance | citation | Wallisellen's own factual profile paragraph, citing the cantonal statistical office as source but not reproducing a legal text. |
| `e-wallisellen-profile-2-1` | CH-ZH-69 | Municipal authority guidance | citation | City-published population statistics table, a factual report rather than a legal provision or directory. |
| `e-wallisellen-profile-3-1` | CH-ZH-69 | Municipal authority guidance | citation | Same statistics table, breakdown of residents by nationality group. |

### Wallisellen - Infrastruktur zum mieten

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/raeume>

Office named by the page: none - No page-specific responsible office is named; only the generic site-wide footer contact (Stadt Wallisellen, Zentralstr. 9) appears.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-facilities-museum-and-culture-1-1` | CH-ZH-69 | Municipal authority directory | citation | The evidence is a bare listing of rentable venues and locations with one-line descriptions, not an explanation of a rule or procedure. |
| `e-facilities-museum-and-culture-4-1` | CH-ZH-69 | Municipal authority directory | citation | Same venue listing (Ortsmuseum, Pfadiheim, Vereinslokal, Waldhütte etc.) presented as a bare directory of locations. |

### Wallisellen - Rechtssammlung

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/rechtssammlung>

Office named by the page: none - No responsible department is named for the legal-collection search page; only the generic city footer contact appears.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-municipal-legal-collection-1-1` | CH-ZH-69 | Municipal authority guidance | citation | Description of the collection's own search-form fields and categories, not a reproduced legal provision. |

### Wallisellen - Sehenswertes

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/sehenswuerdigkeiten>

Office named by the page: none - The page only carries the generic sitewide Stadtverwaltung footer contact; no page-specific responsible office is named for the places-of-interest content.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-wallisellen-profile-4-1` | CH-ZH-69 | Municipal authority guidance | citation | The quote is the city's own descriptive text about local landmarks, including a historical narrative about the Doktorhaus, not a directory of contacts. |

### Wallisellen - Gemeindeversammlungen

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/sitzung>

Office named by the page: none - Only a contact email (praesidiales@wallisellen.ch) appears under 'Kontakt', without a stated office name, so none is recorded per the no-guessing rule.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-municipal-assembly-1-1` | CH-ZH-69 | Municipal authority guidance | citation | Own-words statement of the assembly's constitutional standing, without citing an article. |
| `e-municipal-assembly-2-1` | CH-ZH-69 | Municipal authority guidance | citation | City's own description of the yearly assembly schedule. |
| `e-municipal-assembly-3-1` | CH-ZH-69 | Municipal authority guidance | citation | Own-words paraphrase of the assembly's competences, without citing the enabling provision. |

### Wallisellen - Spielplätze

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/spielplaetze>

Office named by the page: none - The page only carries the generic sitewide Stadtverwaltung footer contact; no page-specific responsible office is named for the playground listing.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-recreation-sport-and-playgrounds-3-1` | CH-ZH-69 | Municipal authority directory | citation | The quote is a list of playground names paired with their street locations. |

### Wallisellen - Sportanlagen

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/sport>

Office named by the page: none - No page-specific responsible office is named; only the generic site-wide footer contact appears.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-recreation-sport-and-playgrounds-2-1` | CH-ZH-69 | Municipal authority directory | citation | The evidence is a bare listing of sports facilities and venues with one-line descriptions. |

### Wallisellen - Steuerfuss

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/steuerfuss>

Office named by the page: none - The page only carries the generic sitewide Stadtverwaltung footer contact; no page-specific responsible office is named for the tax-rate table.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-tax-rate-and-finance-1-1` | CH-ZH-69 | Municipal authority guidance | citation | The quote is the city's own published table of tax-rate percentages over the years, official figures presented in its own format, not a directory of contacts or a reproduced statute. |

### Wallisellen - Steuern

Publisher: City of Wallisellen, Tax Office (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch/steuern; page: <https://www.wallisellen.ch/steuern>

Office named by the page: Steuern - The page's own Kontakt block names the Steuern (tax) office as responsible; the Hundewesen section on the same page names Bevölkerungsdienste for dog registration but carries no separate contact block of its own.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-population-services-2-1` | CH-ZH-69 | Municipal authority guidance | citation | The quote explains the dog-registration procedure and duty to report to the Bevölkerungsdienste in the page's own words, not reproducing a legal provision. |
| `e-population-services-3-1` | CH-ZH-69 | Municipal authority guidance, referring to revidierte Hundeverordnung (per 1. Juni 2025) | citation | The quote states the dog levy amounts and training duty in its own words and only names the revised Hundeverordnung without reproducing any of its articles. |
| `e-municipal-tax-services-1-1` | CH-ZH-69 | Municipal authority guidance | citation | The page informs residents about the switch to ZHprivateTax in its own words; it does not reproduce a cantonal text or speak as the canton itself. |
| `e-municipal-tax-services-2-1` | CH-ZH-69 | Municipal authority guidance | citation | First-person 'Wir erteilen...' explains the tax office's own information service and extension-request procedure. |
| `e-municipal-tax-services-3-1` | CH-ZH-69 | Municipal authority directory | citation | The evidence is a Kontakt block giving the tax office's address, telephone and e-mail. |
| `e-municipal-tax-services-4-1` | CH-ZH-69 | Municipal authority guidance | citation | First-person 'Wir geben...Auskünfte' explains the tax certificate procedure, price and channel in the office's own words, only generically citing 'Steuergesetzgebung'. |
| `e-municipal-tax-services-5-1` | CH-ZH-69 | Municipal authority directory | citation | The evidence is a bare table row naming an online service (Fristerstreckung Steuererklärung) with its online-form link, not an explanation of a rule. |

### Wallisellen - Notfallnummern

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/telefonnummern>

Office named by the page: none - No responsible department is named for this phone-number page beyond the generic city footer contact.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-emergency-numbers-1-1` | CH-ZH-69 | Municipal authority directory | citation | Table of emergency service names and phone numbers compiled by the city. |
| `e-emergency-numbers-2-1` | CH-ZH-69 | Municipal authority directory | citation | Same emergency-numbers table, covering medical and support helplines. |
| `e-emergency-numbers-3-1` | CH-ZH-69 | Municipal authority directory | citation | Table of additional important contact numbers compiled by the city. |

### Wallisellen - Zuzug, Wegzug (eUmzug)

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/umzug>

Office named by the page: none - The page names two counters, Bevölkerungsdienste and Einwohnerkontrolle, for different procedures on the same page without one being stated as responsible for the whole page; only the generic site-wide footer contact appears otherwise.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-moving-registration-1-1` | CH-ZH-69 | Municipal authority guidance | citation | The page explains the 14-day reporting duty and who may report family members in its own words. |
| `e-moving-registration-2-1` | CH-ZH-69 | Municipal authority guidance | citation | The page describes, in its own words, that moves can be reported through the eUmzugCH portal. |
| `e-moving-registration-3-1` | CH-ZH-69 | Municipal authority guidance | citation | The page states the in-person registration requirement for weekly residents at the Bevölkerungsdienste counter in its own words. |
| `e-moving-registration-4-1` | CH-ZH-69 | Municipal authority guidance | citation | The page states the in-person registration requirement for arrivals from abroad in its own words. |
| `e-moving-registration-5-1` | CH-ZH-69 | Municipal authority guidance | citation | The page states the in-person deregistration requirement for departures abroad at the Einwohnerkontrolle counter in its own words. |
| `e-moving-registration-6-1` | CH-ZH-69 | Municipal authority guidance | citation | The page states the requirement for the other parent's consent in its own words, without citing any legal provision. |

### Wallisellen - Öffentlicher Raum, Verkehr

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/verkehrbereich>

Office named by the page: none - The page names 'Bereich Unterhalt' inline as responsible for road maintenance but has no dedicated contact block for the page as a whole; only the generic site-wide footer contact appears otherwise.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-public-space-and-mobility-1-1` | CH-ZH-69 | Municipal authority guidance | citation | The page describes the purpose of its own Strassen und Plätze strategy in its own words. |
| `e-public-space-and-mobility-2-1` | CH-ZH-69 | Municipal authority guidance | citation | The page states, in its own words, which municipal unit handles road maintenance and what the parking and winter-service pages cover. |
| `e-public-space-and-mobility-3-1` | CH-ZH-69 | Municipal authority guidance | citation | The page describes the content and purpose of the municipal transport master plan in its own words. |

### Wallisellen

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/verwaltungueber>

Office named by the page: Stadtverwaltung Wallisellen - The page's own content is the Stadtverwaltung's address, phone number and opening-hours table; the page is the general administration's own contact page.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-city-contact-hours-1-1` | CH-ZH-69 | Municipal authority directory | citation | The quote is the administration's address, telephone number and weekly opening-hours table. |
| `e-city-contact-hours-2-1` | CH-ZH-69 | Municipal authority directory | citation | The quote lists the administration's holiday closure dates, the same contact/hours listing extended with special closures. |

### Wallisellen

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/wirtschaftsstandort>

Office named by the page: none - No responsible department is named on this brief business-location page; only the generic city footer contact appears.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-business-location-support-1-1` | CH-ZH-69 | Municipal authority guidance | citation | Own-words statement that the municipality supports businesses, not a legal text. |

### Wallisellen - Wohnen

Publisher: City of Wallisellen (municipal, CH-ZH-69); attributed by registry rule www.wallisellen.ch; page: <https://www.wallisellen.ch/wohnen>

Office named by the page: none - The page mixes topics; only the Stadtliegenschaften section names a unit (Bereich Liegenschaften der Abteilung Finanzen und Liegenschaften) and only for managing city properties, not for the page's other sections, so no single office is responsible for the whole page.

| Evidence | Fact jurisdiction | Basis | Rule | Reason |
| --- | --- | --- | --- | --- |
| `e-housing-1-1` | CH-ZH-69 | Municipal authority guidance | citation | The quote is the city's own policy statement about influencing affordable housing at the planning level. |
| `e-housing-2-1` | CH-ZH-69 | Municipal authority guidance | citation | The quote explains, in the city's own words, which unit manages city-owned properties and points to rental/purchase listings. |
| `e-housing-3-1` | CH-ZH-69 | Municipal authority guidance | citation | The quote is the municipality's own statement about its two senior-housing developments. |
