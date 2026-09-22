# Coverage

**Last update:** 22 September 2026

What the Swiss TIP MCP server serves today, and what it does not. This file
describes the committed release that the server loads by default; it is
updated from that release whenever the knowledge base changes (see
[AGENTS.md](AGENTS.md), "Coverage and limitations documents"). The
submission is `mvp-zurich`; `mvp-wallisellen` was a proof of concept that a
second, municipal pack can be built with the same tooling, is frozen at its
attested release and is not extended, tested or documented further.

**Release:** `mvp-zurich-2026-09-22-v6` (pack `mvp-zurich`, KB1)<br>
**Content digest:** `9518b36a60a99ae5cdd1bf34be3ca5af79112382fd8a59419ce9cf7bf9eb8f41`<br>
**Snapshot date:** 19 September 2026, the latest access date of a cited page
(10 of the 196 were saved on 19 September, 25 on 18 September, 47 on 17
September, 49 on 15 September, 59 on 11 September and 6 on 10 or 14
September); maximum age 60 days, stale from 18 November 2026<br>
**Contents:** 17 topics, 156 concepts, 712 facts, 926 evidence excerpts
(812 German, 114 English), 203 cited documents<br>
**Review:** all 712 facts are `human-reviewed` by one named reviewer, confirmed
in the console: the 104 of the residence and contacts topics on 14 September
2026, the 149 of the five topics added on 15 September 2026 that day, the
37 of the 13 `fza-*` concepts, drafted from the Agreement on the Free Movement
of Persons, on 16 September 2026, the 41 of the office contacts and the 86
of the daily-life topics (with three City of Zurich naturalisation facts read
from the pages' data tables) on 17 September 2026, and the 49 of the entry
and visa topic and the two Zurich family-reunification concepts on 17
September 2026, and the 29 of the voting-rights topic and the two
tax-at-source tariff concepts on 18 September 2026, and the 106 of the
expat-life extension that day (in groups of 100 and 6), most in bulk
groups. The first 253 were also read card by
card against their excerpts on 15 September 2026. The 114 excerpts added on
19 September 2026 (the English versions of federal pages, see "Jurisdictions
and languages") are not reviewed by a person. The 92 facts of
22 September 2026 were confirmed in the console that day: the 9 of
`permit-c-five-years` and `zh-permit-c-five-years`, the 77 of the twenty
concepts curated from pages the catalogue already held, and the 6 whose
review was reopened when a second citation of the law was added to them. The
25 facts of the integration topic were confirmed in one bulk group on
22 September 2026. Not
a legal review (see [LIMITATIONS.md](LIMITATIONS.md))<br>
**Places:** the release embeds a place register, so a caller names the
user's place instead of a code: Switzerland, the 26 cantons and the 2,110
municipalities of the Federal Statistical Office's register of
municipalities (snapshot of 18 September 2026), with 115 other-language
names on 50 of them (see "Jurisdictions and languages")<br>
**Readiness:** attested on 22 September 2026 by the reviewer, after the
review of all 712 facts: `readiness.json` names this release and binds its
bytes, so the server with `--require-ready` and the pack image serve it. No
graded
live-caller session covers the `fza-*` concepts, the office contacts, the
daily-life topics, the cross-jurisdiction cases, entry and visas, voting
rights, the tax-at-source tariffs or the expat-life topics<br>
**Coverage of the run:** `curation-coverage.md` next to the release lists,
per candidate record of the run, which content sections a fact cites, which a
disposition in `curation-coverage.yaml` settles and which are open; on this
release 558 of 2,077 units are cited, 544 dispositioned and 975 open;
repeated boilerplate (contact cards, closure notices) is set aside and traced
to the page where a fact cites it, so the Migrationsamt address and hours are
served once, from the office's own page (see [LIMITATIONS.md](LIMITATIONS.md),
"Retrieval limitations")<br>
**Publishers and basis:** every cited document names the institution that
published it (105 federal, 51 cantonal, 40 municipal) and every excerpt what
it is: 450 facts rest on an authority's own guidance, 77 on an office
directory (the SEM list of cantonal offices and the Zurich offices' own
contact entries), 50 on a ch.ch portal summary, 47 on a federal act, 37 on
the Agreement on the Free Movement of Persons, 17 on a federal ordinance, 7
on a cantonal directive and 2 on the Constitution of the Canton of Zurich
(see "Cited sources")

## Scope statement

Foreign nationals and newcomers in Switzerland: federal rules with Canton of
Zurich and City of Zurich procedures. Entry and visas: the visa duty, the visa
types C and D, the 90-in-180-days rule, the entry requirements, ETIAS and the
Entry/Exit System. Residence permits and registration (AIG, the free-movement
agreement FZA, SEM and ch.ch guidance, Zurich procedures), the
migration-office contact of every canton, and the Zurich offices' addresses,
opening hours and contacts. Marriage and leaving the City of Zurich. Family
allowances and parental leave. Renting a home. Social insurance on leaving,
pillar 3a and unemployment. Tax at source with its tariff codes and the Zurich
tariff rules, the City of Zurich tax return and tax office, and the radio and
television fee. Driving licence, vehicles and household goods after a move,
and City of Zurich parking permits. Health and accident insurance and premium
reduction. Naturalisation and voting rights. Life in the City of Zurich: first
steps, waste and recycling, dogs, kindergarten and school holidays, and
medical emergencies.

This is the `scope_statement` of the release manifest, served verbatim by
`get_coverage`. A calling assistant that receives a question outside it is
told to say so and not to answer from general knowledge.

## Jurisdictions and languages

| Level | Published values |
| --- | --- |
| Federal | `CH` |
| Cantonal | all 26 cantons (`CH-AG` to `CH-ZH`), of which only `CH-ZH` carries procedures beyond the migration-office contact |
| Federal, for daily life | `CH` also carries the radio and television fee (SERAFE) |
| Municipal | `CH-ZH-261` (City of Zurich) |

The residence topic's cantonal and municipal procedures, and every cantonal
fact of social insurance, unemployment, family allowances, tax at source,
driving licence, health insurance, naturalisation, voting rights and the
rental form, every office contact and the cantonal facts of dogs and
vehicles, are those of Zurich. For another canton `resolve` serves the
federal facts of these topics and answers the Zurich concepts
`OUT_OF_COVERAGE`. The Canton of Zurich concepts serve every municipality of
the canton; the City of Zurich concepts (naturalisation, marriage, departure, office
contacts and 16 of the 18 daily-life concepts) serve only `CH-ZH-261`. Facts served for a
place whose own cantonal or municipal level the topic publishes for Zurich
only carry a caveat: the gap `more_specific_jurisdiction_not_published` names
the deepest level that applies and the places served more deeply, and the
guidance tells the caller to say that the cantonal or municipal part is not
published for the user's place and to carry nothing over from Zurich.

A caller does not need these codes. `resolve` takes the place in the parts
`country`, `canton` and `city`, each a name in English or the local language
or a code (`{"canton": "Zurich", "city": "Wallisellen"}`, `{"city":
"Genf"}`), and the release's place register turns them into codes: the
country, the 26 cantons and the 2,110 municipalities of the register of
municipalities of the Federal Statistical Office
(<https://www.agvchapp.bfs.admin.ch/api/communes/snapshot?date=18-09-2026>,
read on 18 September 2026, response hash `e0748c06c754...`), with their
official names, and 115 hand-written other-language names on 50 places
(`Geneva`, `Genf`, `Ginevra`; `config/places/ch-aliases.json`). A city alone
supplies its canton; `executed_scope` echoes the codes and the official
names; a part the register does not hold (a quarter, a postcode, a
misspelling) is named in `executed_scope.not_recognised` and the request
runs for the broader place; a name several municipalities share is an error
that lists them. Gap messages name a place next to its code (`CH-ZH-261
(municipality of Zürich)`). The register covers all of Switzerland so that a
user anywhere can be placed; it publishes no fact of its own.

Statements are published in English (`en`); the excerpts they cite are in the
language of the source page, German (`de`) for 686 excerpts. On 112 facts of
27 concepts the English version of the same SEM, FOPH, FOCBS, SECO or SERAFE
page is cited next to the German excerpt the statement was written from (113
English excerpts), and on one fact the German SEM residence overview next to
its English version. The assistant added these 114 excerpts on 19 September
2026 after comparing the two versions. No second excerpt was added for 12
excerpts whose versions differ on something the fact states (among them the
type D visa threshold, the ETIAS passport validity and a SERAFE page whose
mobile table shows another fee), nor for the 7 of the SEM citizenship FAQ,
which has no English version. The SVA Zurich pages declare no language; the
release records them as German (`page_languages`). A question may be asked in
English, German or Swiss German: concept discovery carries the 1237 search
terms the build counts, copied verbatim from the cited excerpts, German except
for the English ones on 25 concepts, alongside authored everyday words in German and English, at
least one English and one German sample question on every concept (the build
checks it), and three Zurich German spellings.

## Topics and concepts

### Residence permits and registration (`residence`) - 73 concepts

| Concept | Subject | Jurisdiction | Facts |
| --- | --- | --- | ---: |
| `permit-authority` | Authority issuing residence permits | CH | 1 |
| `aig-short-stay` | AIG baseline for stays without work | CH | 2 |
| `aig-work-permit` | AIG employment permit procedure | CH | 2 |
| `aig-registration` | Registration under AIG Article 12 | CH | 2 |
| `permit-l` | Short-stay permit: AIG Article 32 | CH | 2 |
| `permit-b` | Residence permit: AIG Article 33 | CH | 2 |
| `permit-c` | Settlement permit: AIG Article 34 | CH | 4 |
| `permit-c-five-years` | Settlement permit after five years: states with settlement agreements | CH | 3 |
| `permit-types` | Foreign-national permit types | CH | 1 |
| `permit-card-eu-efta` | EU/EFTA permit cards B, L, Ci and G | CH | 4 |
| `permit-card-third-country` | Third-country permit cards Ci and G | CH | 3 |
| `travel-documents-foreign-nationals` | Travel documents for foreign nationals | CH | 5 |
| `permit-renewal` | Renewing a residence permit | CH | 3 |
| `permit-lost` | Lost or stolen permit | CH | 1 |
| `aig-study` | Study admission under AIG Article 27 | CH | 2 |
| `integration-criteria` | Integration criteria and personal circumstances | CH | 2 |
| `family-swiss` | Family reunification with a Swiss sponsor: Article 42(1) | CH | 2 |
| `family-c` | Family reunification with a settlement-permit sponsor | CH | 2 |
| `family-b` | Family reunification with a residence-permit sponsor | CH | 2 |
| `family-eu-efta` | Family reunification with an EU/EFTA sponsor | CH | 1 |
| `family-deadlines` | AIG family-reunification deadlines | CH | 3 |
| `family-requirements` | Family reunification: relationship, housing, means and entry documents | CH | 3 |
| `family-member-rights` | Permit and work rights of reunited family members | CH | 1 |
| `family-separation` | Residence after dissolution of family life | CH | 3 |
| `canton-change` | Change of canton under AIG Article 37 | CH | 2 |
| `third-country-work` | Third-country employment admission | CH | 2 |
| `third-country-work-procedure` | Third-country workers: exemptions, application, visa and registration | CH | 4 |
| `third-country-work-conditions` | Third-country labour-market admission: the conditions | CH | 8 |
| `eu-short-employment` | EU/EFTA short employment: notification | CH | 2 |
| `eu-permit-mobility` | EU/EFTA employment permit: validity and job changes | CH | 1 |
| `eu-self-employment` | EU/EFTA self-employment: registration and documents | CH | 1 |
| `eu-job-search` | EU/EFTA nationals looking for work | CH | 1 |
| `notification-responsibility` | Who submits a short-work notification | CH | 1 |
| `posted-service-notification` | Cross-border services: duration and notification timing | CH | 2 |
| `uk-new-employment` | New short-term employment by UK nationals | CH | 3 |
| `biometric-permit` | Biometric residence-card data and issuance | CH | 2 |
| `language-evidence` | Evidence of language skills | CH | 2 |
| `social-assistance-review` | Social assistance and permit consequences | CH | 1 |
| `zh-eu-registration` | Zurich registration for EU/EFTA nationals | CH-ZH | 2 |
| `zh-eu-l` | Zurich EU/EFTA short-stay employment permit | CH-ZH | 1 |
| `zh-eu-b` | Zurich EU/EFTA residence employment permit | CH-ZH | 1 |
| `zh-eu-self-employment` | Zurich EU/EFTA self-employment documentation | CH-ZH | 1 |
| `zh-eu-nonworking` | Zurich EU/EFTA residence without employment | CH-ZH | 1 |
| `zh-eu-family-documents` | Zurich EU/EFTA family-reunification documents | CH-ZH | 1 |
| `zh-third-country-work` | Zurich: working as a third-country national | CH-ZH | 6 |
| `zh-permit-card` | Zurich: applying for the permit card and the biometrics appointment | CH-ZH | 5 |
| `zh-entry-permit-non-working` | Zurich: entry permit for retirees and for close relatives in need of care | CH-ZH | 4 |
| `zh-third-country-retirement` | Zurich third-country retirement applications | CH-ZH | 1 |
| `zh-permit-c-five-years` | Zurich: settlement permit after five years | CH-ZH | 6 |
| `city-zurich-arrival` | City of Zurich: registering arrival from abroad | CH-ZH-261 | 1 |
| `city-zurich-arrival-documents` | City of Zurich: documents for arrival from abroad | CH-ZH-261 | 1 |
| `eu-employment-registration-deadline` | EU/EFTA employment: municipal registration deadline after arrival | CH | 2 |
| `health-insurance-enrolment` | Compulsory health-insurance enrolment timing | CH | 2 |
| `fza-overview` | Agreement on the Free Movement of Persons (FZA): aims and principles | CH | 4 |
| `fza-entry` | FZA: entry with an identity card or passport | CH | 1 |
| `fza-job-search` | FZA: staying to look for work | CH | 1 |
| `fza-employee-permit` | FZA: residence permit of an EU employee | CH | 5 |
| `fza-mobility` | FZA: changing job, employer, profession or place | CH | 2 |
| `fza-self-employment` | FZA: residence permit of a self-employed EU national | CH | 3 |
| `fza-cross-border-commuter` | FZA: cross-border commuters | CH | 2 |
| `fza-family-members` | FZA: family members of an EU national | CH | 4 |
| `fza-non-working` | FZA: residence without gainful employment | CH | 5 |
| `fza-services` | FZA: cross-border services up to 90 working days | CH | 5 |
| `fza-right-to-remain` | FZA: right to remain after working | CH | 1 |
| `fza-equal-treatment` | FZA: equal treatment at work | CH | 3 |
| `zh-family-l-permit` | Zurich: family reunification by holders of a short-stay L permit | CH-ZH | 4 |
| `zh-family-b-c-permit` | Zurich: family reunification by a B or C permit holder | CH-ZH | 5 |
| `zh-family-swiss-sponsor` | Zurich: family reunification by a Swiss citizen | CH-ZH | 4 |
| `zh-family-fza` | Zurich: family reunification under the free movement agreement | CH-ZH | 3 |
| `zh-family-refugee-asylum` | Zurich: family reunification by recognised refugees granted asylum | CH-ZH | 5 |
| `marriage-switzerland` | Getting married in Switzerland | CH | 8 |
| `city-zurich-marriage` | Marriage preparation at the City of Zurich | CH-ZH-261 | 9 |
| `city-zurich-departure` | Deregistering when leaving the City of Zurich | CH-ZH-261 | 9 |

The two `zh-family-*` concepts of 17 September 2026 are the Migration Office's
own guidance for two sponsor groups the other family concepts do not cover:
a third-country national on a short-stay permit, and a recognised refugee
whose family members SEM did not include in their refugee status. Neither
concept serves the asylum procedure itself, which the pack does not publish;
their `not_served` lists say so.

Marriage and departure were added on 18 September 2026: ch.ch's page on
marrying in Switzerland (conditions, the three-month window, witnesses, the
cost), the City of Zurich civil registry office's pages (a lawful stay is
required, the documents from the home country at the latest two months before
the wedding, the preparation at the latest one month before, the language
requirement), and the City of Zurich's pages on deregistering (within 14 days
after moving out, at the earliest 30 days before) and on taxes when moving
abroad (all taxes fall due; when a tax representative is needed). Other
municipalities' offices are not published.

The `fza-*` concepts cite the treaty text itself (SR 0.142.112.681,
consolidated version of 15 December 2020). They sit next to the SEM, ch.ch and
Zurich concepts on the same subjects, which state how Switzerland applies the
treaty (permit letters, deadlines, documents); the treaty names no permit
letter. All but `fza-overview`, `fza-entry` and `fza-services` need the
`population` context field and serve `eu_efta`; the treaty covers nationals of
the EU member states, and the EFTA Convention is not in the release.

### Cantonal migration offices (`contacts`) - 1 concept

| Concept | Subject | Jurisdiction | Facts |
| --- | --- | --- | ---: |
| `cantonal-migration-contact` | Cantonal migration-office contact | all 26 cantons | 26 |

### Zurich office contacts (`offices`) - 9 concepts

| Concept | Subject | Jurisdiction | Facts |
| --- | --- | --- | ---: |
| `zh-migrationsamt-contact` | Migration Office of the Canton of Zurich: address, opening hours and contact | CH-ZH | 4 |
| `zh-naturalisation-division-contact` | Naturalisation Division of the Canton of Zurich: address and contact | CH-ZH | 4 |
| `zh-road-traffic-office-locations` | Road Traffic Office of the Canton of Zurich: locations, opening hours and contact | CH-ZH | 14 |
| `zh-tax-office-contact` | Cantonal Tax Office of Zurich: address, office hours and tax-at-source contact | CH-ZH | 2 |
| `zh-economy-office-contact` | Office for the Economy of the Canton of Zurich: work-permit contacts | CH-ZH | 3 |
| `zh-sva-contact` | SVA Zurich: address, opening hours and directions | CH-ZH | 5 |
| `zh-sva-telephone-numbers` | SVA Zurich: telephone numbers by topic | CH-ZH | 2 |
| `city-zurich-population-office` | Population Office of the City of Zurich: address, opening hours and appointments | CH-ZH-261 | 5 |
| `city-zurich-naturalisation-contact` | Naturalisation office of the City of Zurich: address and contact | CH-ZH-261 | 3 |

These concepts serve what the offices' own pages state: street and postal
addresses, counter, office and telephone hours, e-mail addresses where a
page gives one, and the statements a page makes in the negative (the
Migration Office has no e-mail address; the Population Office is closed on
Saturday and Sunday and renews a permit card only by appointment; the SVA
Zurich needs no appointment; the Road Traffic Office's published list of
eight locations). Directions are served for the SVA Zurich, the only office
that publishes them; the Canton of Zurich pages link a Google route, the
City of Zurich page a public transport timetable. The special opening days
of the Road Traffic Office (2026 and 2027) and the SVA Zurich (2026) are
served until the end of their year. Since release `mvp-zurich-2026-09-17-v2`
the City of Zurich naturalisation office's telephone hours are served too,
read from a data table of its page.

### First steps and life in the City of Zurich (`newcomer`) - 7 concepts

| Concept | Subject | Jurisdiction | Facts |
| --- | --- | --- | ---: |
| `city-zurich-first-steps` | First steps after moving to the City of Zurich | CH-ZH-261 | 7 |
| `city-zurich-dog-registration` | Registering a dog in the City of Zurich | CH-ZH-261 | 5 |
| `zh-dog-keeping` | Keeping a dog in the Canton of Zurich | CH-ZH | 5 |
| `city-zurich-kindergarten` | Kindergarten and school entry in the City of Zurich | CH-ZH-261 | 7 |
| `city-zurich-school-holidays` | School holidays in the City of Zurich | CH-ZH-261 | 3 |
| `city-zurich-school-languages` | Public school explained in other languages (City of Zurich) | CH-ZH-261 | 2 |
| `city-zurich-medical-emergency` | Medical emergencies in the City of Zurich | CH-ZH-261 | 3 |

The first-steps checklist of the City of Zurich names what a newcomer
arranges beyond registration (electricity and water, vehicles, health
insurance, the service booklet, self-employment, school); the dog concepts
add the city's registration and the canton's training duty of 1 June 2025;
schooling is served as kindergarten entry, the school holidays of 2026/27
and 2027/28 and the city's information in other languages, not as the
school system.

### Waste and recycling in the City of Zurich (`waste`) - 7 concepts

| Concept | Subject | Jurisdiction | Facts |
| --- | --- | --- | ---: |
| `city-zurich-waste-sorting` | City of Zurich: where a particular item goes | CH-ZH-261 | 5 |
| `city-zurich-household-waste` | Household waste and the Züri-Sack in the City of Zurich | CH-ZH-261 | 7 |
| `city-zurich-organic-paper-cardboard` | Organic waste, paper and cardboard collection in the City of Zurich | CH-ZH-261 | 6 |
| `city-zurich-bulky-waste-pickup` | Bulky waste pickup in the City of Zurich | CH-ZH-261 | 3 |
| `city-zurich-recycling-centres` | Recycling centres of the City of Zurich | CH-ZH-261 | 5 |
| `city-zurich-recycling-points` | Glass, metal, oil, textiles and plastic recycling in the City of Zurich | CH-ZH-261 | 4 |
| `city-zurich-hazardous-waste` | Hazardous waste in the City of Zurich | CH-ZH-261 | 3 |

Collection days are not served for a street: the facts point to the
personal disposal calendar and the ERZ app, which compute them.

### Parking, vehicles and moving goods (`vehicles-parking`) - 3 concepts

| Concept | Subject | Jurisdiction | Facts |
| --- | --- | --- | ---: |
| `city-zurich-parking-permits` | Parking permits and the blue zone in the City of Zurich | CH-ZH-261 | 6 |
| `zh-vehicle-registration-move` | Vehicles after moving to the Canton of Zurich | CH-ZH | 5 |
| `moving-goods-customs` | Importing moving goods (household effects and vehicles) when moving to Switzerland | CH | 7 |

### Tax return and household fees (`household-taxes`) - 3 concepts

| Concept | Subject | Jurisdiction | Facts |
| --- | --- | --- | ---: |
| `city-zurich-tax-return` | Tax return of individuals in the City of Zurich | CH-ZH-261 | 5 |
| `city-zurich-tax-office-contact` | Tax office of the City of Zurich: address and opening hours | CH-ZH-261 | 4 |
| `radio-tv-household-fee` | Radio and television fee for households (Serafe) | CH | 3 |

The tax facts are procedural (who files, the deadline of the 2025 return,
filing channels, documents, consequences of not filing); tariffs, rates,
deductions and amounts of tax are not served.

### Social insurance, pillar 3a and unemployment (`social-insurance`) - 8 concepts

| Concept | Subject | Jurisdiction | Facts |
| --- | --- | --- | ---: |
| `ahv-agreement-states` | Social security agreements: the states and what they coordinate | CH | 7 |
| `ahv-contribution-refund` | Refund of AHV contributions on leaving Switzerland | CH | 10 |
| `ahv-pension-abroad` | AHV pensions and benefits after moving abroad | CH | 6 |
| `bvg-cash-out-departure` | Cash payment of pension fund assets on leaving Switzerland | CH | 9 |
| `fza-social-security` | FZA: coordination of social security | CH | 1 |
| `pillar-3a` | Pillar 3a private pension | CH | 8 |
| `unemployment-benefit` | Unemployment benefit | CH | 9 |
| `zh-unemployment-benefit` | Unemployment benefit in the Canton of Zurich | CH-ZH | 4 |

### Tax at source (`tax-at-source`) - 5 concepts

| Concept | Subject | Jurisdiction | Facts |
| --- | --- | --- | ---: |
| `tax-at-source-liability` | Tax at source: federal rules | CH | 7 |
| `zh-tax-at-source-liability` | Tax at source in the Canton of Zurich: liability and its end | CH-ZH | 7 |
| `zh-tax-at-source-ordinary-assessment` | Subsequent ordinary assessment for persons taxed at source in the Canton of Zurich | CH-ZH | 12 |
| `tax-at-source-tariff-codes` | Tax at source: federal tariff codes | CH | 5 |
| `zh-tax-at-source-tariffs` | Tax-at-source tariffs in the Canton of Zurich | CH-ZH | 12 |

The two tariff concepts of 18 September 2026 say how the tariff is set, not
what it comes to: the tariff codes of the Tax at Source Ordinance (QStV
Art. 1), the Canton of Zurich's code format (letter, number of children,
church tax Y or N), which tariff applies to whom, the flat rate for
cross-border commuters from Germany, the tariff calculator, the tariff tables
of the 2026 edition and their calculation parameters. The parameters answer
whether the municipality matters: the canton calculates one tariff with the
weighted average of the municipal tax multipliers (109.90 per cent without
church tax, 116.00 per cent with, in 2026), so the tax at source is the same
in every municipality of the canton; that sentence of fact
`zh-tax-at-source-tariffs-9` is the assistant's reading of the parameter
sheet, confirmed by the reviewer (see [LIMITATIONS.md](LIMITATIONS.md)). The tariff tables themselves
and the amount of tax for a salary are not served.

### Foreign driving licence (`driving-licence`) - 3 concepts

| Concept | Subject | Jurisdiction | Facts |
| --- | --- | --- | ---: |
| `foreign-licence-exchange` | Driving on a foreign licence: federal rules | CH | 5 |
| `zh-foreign-licence-exchange` | Exchanging a foreign driving licence in the Canton of Zurich | CH-ZH | 11 |
| `zh-control-drive` | Control drive for a foreign driving licence in the Canton of Zurich | CH-ZH | 7 |

### Health and accident insurance (`health-insurance`) - 5 concepts

| Concept | Subject | Jurisdiction | Facts |
| --- | --- | --- | ---: |
| `health-insurance-deadline` | Health insurance duty on taking up residence | CH | 8 |
| `zh-health-insurance-exemption` | Exemption from the health insurance duty in the Canton of Zurich | CH-ZH | 5 |
| `premium-reduction` | Health insurance premium reduction: federal frame | CH | 5 |
| `zh-premium-reduction` | Premium reduction in the Canton of Zurich | CH-ZH | 8 |
| `accident-insurance` | Compulsory accident insurance (UVG) and suspending accident cover in health insurance | CH | 7 |

`health-insurance-deadline` and the residence concept
`health-insurance-enrolment` cite the same FOPH page: the first serves its
general statements without a context field, the second its FAQ answers for a
person whose insurance duty applies.

### Naturalisation (`naturalisation`) - 10 concepts

| Concept | Subject | Jurisdiction | Facts |
| --- | --- | --- | ---: |
| `naturalisation-ordinary` | Ordinary naturalisation: federal conditions | CH | 9 |
| `zh-naturalisation-ordinary` | Ordinary naturalisation in the Canton of Zurich | CH-ZH | 13 |
| `city-zurich-naturalisation` | Ordinary naturalisation in the City of Zurich | CH-ZH-261 | 8 |
| `naturalisation-third-generation` | Facilitated naturalisation of the third generation | CH | 4 |
| `city-zurich-naturalisation-language` | City of Zurich: German for naturalisation | CH-ZH-261 | 4 |
| `city-zurich-naturalisation-civics` | City of Zurich: the civic knowledge test | CH-ZH-261 | 3 |
| `naturalisation-facilitated-spouse` | Facilitated naturalisation of the spouse of a Swiss citizen | CH | 9 |
| `zh-naturalisation-facilitated` | Facilitated naturalisation in the Canton of Zurich | CH-ZH | 5 |
| `city-zurich-naturalisation-facilitated` | Facilitated naturalisation in the City of Zurich | CH-ZH-261 | 7 |
| `city-zurich-citizenship-swiss` | City of Zurich: city citizenship for Swiss citizens | CH-ZH-261 | 4 |

### Entry and visas (`entry-visas`) - 9 concepts

| Concept | Subject | Jurisdiction | Facts |
| --- | --- | --- | ---: |
| `entry-visa-need` | Who needs a visa: the rules by nationality and the visa duty of the VEV | CH | 4 |
| `entry-visa-types` | Schengen visa (type C) and national visa (type D) | CH | 5 |
| `entry-short-stay-rule` | The short stay of 90 days in any 180, and how it is counted | CH | 5 |
| `entry-requirements-third-country` | Entry requirements for third-country nationals, with the means of subsistence | CH | 4 |
| `entry-requirements-eu-efta` | Entry requirements for EU/EFTA nationals and their family members | CH | 4 |
| `entry-visa-application` | Where and how to apply for a visa | CH | 6 |
| `entry-visa-fee-insurance` | Visa fee, travel health insurance and processing time | CH | 4 |
| `entry-etias` | The ETIAS travel authorisation | CH | 5 |
| `entry-exit-system` | The Entry/Exit System (EES) at the Schengen border | CH | 3 |

Added on 17 September 2026 from SEM's entry pages, the FDFA visa page and the
Ordinance on Entry and the Granting of Visas (VEV, SR 142.204). The topic is
federal throughout, so it applies in every canton. Four facts cite the VEV by
article (entry requirements for short and longer stays, the visa duty for
each); the rest rest on the two authorities' guidance. The `entry-etias`
statement that no ETIAS application can yet be filed is what SEM's page said
when the copy was taken, and names that date.

### Voting rights (`political-rights`) - 2 concepts

| Concept | Subject | Jurisdiction | Facts |
| --- | --- | --- | ---: |
| `political-rights-federal` | Voting rights: federal rules | CH | 7 |
| `zh-political-rights` | Voting rights in the Canton of Zurich | CH-ZH | 5 |

Added on 18 September 2026 from the Federal Constitution (Art. 39 and 136),
the Constitution of the Canton of Zurich (Art. 22 and 40, published on Fedlex
as a federally guaranteed cantonal constitution), ch.ch's page on the right
to vote and the Canton of Zurich's page on how to vote. They answer who may
vote and elect: Swiss citizens aged 18 or over, and in cantonal and communal
matters of the Canton of Zurich, including the City, only those resident in
the canton; foreign nationals have no federal vote, whatever their permit or
length of stay, and no cantonal or communal vote in Zurich. The one exception
the canton's page names is the Evangelical Reformed church, whose elections
and votes are open to B, C and Ci permit holders. For other cantons the
federal concept serves ch.ch's statement that the cantons decide and that
Jura and Neuchâtel grant foreign nationals a cantonal vote; no other canton's
rule is published. The dates, subjects and results of votes are not served.

### Family allowances and parental leave (`family-benefits`) - 3 concepts

| Concept | Subject | Jurisdiction | Facts |
| --- | --- | --- | ---: |
| `family-allowances` | Family allowances (federal minimum) | CH | 9 |
| `zh-family-allowances` | Family allowances in the canton of Zurich | CH-ZH | 7 |
| `parental-leave` | Maternity, other-parent and adoption leave | CH | 8 |

Added on 18 September 2026 from the FSIO's pages on family allowances and on
income compensation for parents, and SVA Zurich's family-allowance pages: the
federal minimum child and education allowances, the income thresholds, the
order of priority when two parents are entitled, the Canton of Zurich's
amounts (CHF 215 to 12, CHF 268 to 16, CHF 268 education allowance to 25) and
how employees and non-employed persons claim them; the 14 weeks of maternity
leave at 80 per cent up to CHF 220 a day, the two weeks of the other parent
and the adoption leave. Allowances for children abroad are named as subject
to special conditions, which the release does not detail.

### Renting a home (`housing`) - 3 concepts

| Concept | Subject | Jurisdiction | Facts |
| --- | --- | --- | ---: |
| `tenancy-agreement` | Tenancy agreement: contents, deposit, subletting and termination | CH | 9 |
| `rent-changes` | Rent increases, the reference interest rate and defects | CH | 8 |
| `zh-initial-rent-form` | Canton of Zurich: initial rent notification form | CH-ZH | 4 |

Added on 18 September 2026 from the Code of Obligations (Art. 257e, 264,
266c, 266l, 266m, 269d and 270), ch.ch's tenancy pages, the Federal Office for
Housing's page on the reference interest rate and the Canton of Zurich's page
on tenancy forms: the deposit of at most three months' rent in an account in
the tenant's name, subletting, the three-month notice period, notice in
writing and on the approved form, leaving early with a replacement tenant,
abusive notice, rent increases on the official form at least ten days before
the notice period, the reference rate and the 3 and 2.91 per cent steps, the
challenge of the initial rent within 30 days, defects, and the Canton of
Zurich's duty to notify the initial rent on the official form. Rent levels,
flats on offer and the address of an individual conciliation authority are
not served.

### Integration offers and German courses (`integration`) - 5 concepts

| Concept | Subject | Jurisdiction | Facts |
| --- | --- | --- | ---: |
| `zh-integration-offers` | Finding integration offers and German courses | CH-ZH | 3 |
| `zh-newcomer-first-information` | First information and counselling for newcomers | CH-ZH | 5 |
| `zh-racism-protection` | Protection from racist discrimination | CH-ZH | 6 |
| `zh-migrant-associations` | Platform for migrant associations | CH-ZH | 3 |
| `zh-integration-project-funding` | Contributions to integration projects | CH-ZH | 8 |

Added on 22 September 2026 from seven pages of the Canton of Zurich's
Fachstelle Integration that the run had held since the first crawl and that
no fact cited: the offer database and the free German-course advice in 16
languages, the municipalities' duty to inform newcomers and the three groups
the canton names as needing support early, ZüRAS and the national bodies
against racism with the legal bases (BV Art. 8(2), StGB Art. 261bis, AIG
Art. 53), the platform for migrant associations, and the project
contributions under KIP 3 with their amounts, deadlines and applicants. The
canton's integration funding for municipalities and providers and its
support system for refugees (Integrationsagenda IAZH) are out of scope by the
reviewer's decision of 22 September 2026 and are named in the manifest's
`out_of_scope`; the pages that carry them are dispositioned in
`curation-coverage.yaml`. Which offers exist in a given municipality, their
dates and prices, and whether a project is funded are not served.

## Context fields of the added topics

Four concepts route their facts by a context field the caller derives from
the question; `resolve` answers `NEEDS_CONTEXT` without it.

| Concept | Field | Values |
| --- | --- | --- |
| `ahv-contribution-refund` | `agreement_status` | `eu_efta` (Swiss and EU/EFTA nationals), `agreement` (another state with a social security agreement), `none` |
| `bvg-cash-out-departure` | `destination` | `eu_efta` (an EU state, Iceland, Norway or Liechtenstein), `other` |
| `zh-foreign-licence-exchange` | `licence_state` | `eu_efta` and `listed` (the two lists of the Canton of Zurich page), `other` |
| `zh-premium-reduction` | `arrival_from` | `abroad`, `other_canton` |

Facts carry a validity window only where the cited page states a date: the
BVG cash-payment restriction since 1 June 2007, the United Kingdom's national
law for cash payments since 1 November 2021, the SVA Zurich's competence for
exemption requests since 1 October 2023, the six facts citing the Zurich
directive ZStB 87.3, valid from 1 January 2024, the City of Zurich's
appointment requirement since 4 May 2026, the Canton of Zurich's dog
training duty since 1 June 2025, and the facts that end with a date: the
special opening days of 2026 and 2027, the Bülach construction notice (until
30 June 2027, read from "spring 2027"), the closing days of 2026 of the City
of Zurich permit and tax offices, the 2026 kindergarten start, the school
holidays of 2026/27 and 2027/28, and the deadline of the 2025 tax return
(served until the end of 2026), and the Canton of Zurich's tax-at-source
tariff tables of the 2026 edition and their calculation parameters, and the
pillar 3a maximum contributions for 2026 (served until the end of 2026).

## Cited sources

Every fact cites an exact excerpt of one of these 196 documents, with the URL
and the date the copy was taken. `get_evidence` returns the excerpt in its
original language.

| Publisher | Document | Language | Accessed |
| --- | --- | --- | --- |
| Canton of Zurich, Cantonal Tax Office | Merkblatt des kantonalen Steueramtes über die Quellenbesteuerung von Arbeitnehmerinnen und Arbeitnehmern | Kanton Zürich | de | 2026-09-15 |
| Canton of Zurich, Cantonal Tax Office | Nachträgliche ordentliche Veranlagung beantragen | Kanton Zürich | de | 2026-09-15 |
| Canton of Zurich, Cantonal Tax Office | Quellensteuer | Kanton Zürich | de | 2026-09-15 |
| Canton of Zurich, Cantonal Tax Office | Quellensteuer-Tarife | Kanton Zürich | de | 2026-09-18 |
| Canton of Zurich, Cantonal Tax Office | Quellensteuerpflichtige Personen | Kanton Zürich | de | 2026-09-15 |
| Canton of Zurich, Cantonal Tax Office | Steueramt | Kanton Zürich | de | 2026-09-17 |
| Canton of Zurich, Cantonal Tax Office | Zurich: tax-at-source tariffs from 2026, basis and calculation parameters (PDF) | de | 2026-09-18 |
| Canton of Zurich, Directorate of Justice and Home Affairs, tenancy forms | Formulare im Mietwesen | Kanton Zürich | de | 2026-09-18 |
| Canton of Zurich, Health Directorate | Prämienverbilligung Krankenversicherung | Kanton Zürich | de | 2026-09-15 |
| Canton of Zurich, Migration Office | Aufenthalt für EU/EFTA-Staatsangehörige | Kanton Zürich | de | 2026-09-11 |
| Canton of Zurich, Migration Office | Aufenthalt mit Erwerbstätigkeit für Drittstaatsangehörige | Kanton Zürich | de | 2026-09-11 |
| Canton of Zurich, Migration Office | Aufenthalt ohne Erwerbstätigkeit für Drittstaatsangehörige | Kanton Zürich | de | 2026-09-11 |
| Canton of Zurich, Migration Office | Ausländerausweis beantragen | Kanton Zürich | de | 2026-09-11 |
| Canton of Zurich, Migration Office | Ausländerausweise im Kreditkartenformat | Kanton Zürich | de | 2026-09-11 |
| Canton of Zurich, Migration Office | Biometrietermin verschieben | Kanton Zürich | de | 2026-09-11 |
| Canton of Zurich, Migration Office | Einreisebewilligung für Rentnerinnen und Rentner beantragen | Kanton Zürich | de | 2026-09-11 |
| Canton of Zurich, Migration Office | Einreisebewilligung für nahe Verwandte beantragen | Kanton Zürich | de | 2026-09-11 |
| Canton of Zurich, Migration Office | Familiennachzug durch Flüchtlinge mit Asyl beantragen | Kanton Zürich | de | 2026-09-11 |
| Canton of Zurich, Migration Office | Familiennachzug durch Personen mit einer B- oder C-Bewilligung beantragen | Kanton Zürich | de | 2026-09-11 |
| Canton of Zurich, Migration Office | Familiennachzug durch Personen mit einer L-Bewilligung beantragen | Kanton Zürich | de | 2026-09-11 |
| Canton of Zurich, Migration Office | Familiennachzug durch Schweizer Staatsangehörige beantragen | Kanton Zürich | de | 2026-09-11 |
| Canton of Zurich, Migration Office | Familiennachzug nach dem Freizügigkeitsabkommen beantragen | Kanton Zürich | de | 2026-09-11 |
| Canton of Zurich, Migration Office | Migrationsamt | Kanton Zürich | de | 2026-09-17 |
| Canton of Zurich, Migration Office | Niederlassungsbewilligung | Kanton Zürich | de | 2026-09-11 |
| Canton of Zurich, Migration Office | Organisation | Kanton Zürich | de | 2026-09-17 |
| Canton of Zurich, Office for Municipalities, Naturalisation Division | Abteilung Einbürgerungen | Kanton Zürich | de | 2026-09-17 |
| Canton of Zurich, Office for Municipalities, Naturalisation Division | Einbürgerungsgesuch einreichen | Kanton Zürich | de | 2026-09-15 |
| Canton of Zurich, Office for Municipalities, Naturalisation Division | Erleichterte Einbürgerung | Kanton Zürich | de | 2026-09-15 |
| Canton of Zurich, Office for Municipalities, Naturalisation Division | Ordentliche Einbürgerung | Kanton Zürich | de | 2026-09-15 |
| Canton of Zurich, Office for the Economy | Amt für Wirtschaft | Kanton Zürich | de | 2026-09-17 |
| Canton of Zurich, Office for the Economy | Arbeitslosenentschädigung | Kanton Zürich | de | 2026-09-18 |
| Canton of Zurich, Office for the Economy | Erwerbstätigkeit von Ausländerinnen und Ausländern | Kanton Zürich | de | 2026-09-17 |
| Canton of Zurich, Road Traffic Office | Ausländischen Führerausweis umtauschen | Kanton Zürich | de | 2026-09-15 |
| Canton of Zurich, Road Traffic Office | Fahrzeug importieren | Kanton Zürich | de | 2026-09-17 |
| Canton of Zurich, Road Traffic Office | So bereiten Sie sich gut auf Ihre Kontrollfahrt vor | Kanton Zürich | de | 2026-09-15 |
| Canton of Zurich, Road Traffic Office | Standorte und Öffnungszeiten des Strassenverkehrsamts | Kanton Zürich | de | 2026-09-17 |
| Canton of Zurich, Road Traffic Office | Strassenverkehrsamt | Kanton Zürich | de | 2026-09-17 |
| Canton of Zurich, Road Traffic Office | Umtausch eines ausländischen Führerausweises | Kanton Zürich | de | 2026-09-15 |
| Canton of Zurich, Road Traffic Office | Umzug innerhalb oder in den Kanton Zürich melden | Kanton Zürich | de | 2026-09-17 |
| Canton of Zurich, Statistical Office, elections and votes | So stimme ich ab | Kanton Zürich | de | 2026-09-18 |
| Canton of Zurich, Veterinary Office | Hunde | Kanton Zürich | de | 2026-09-17 |
| Central Compensation Office CCO | Anspruch auf AHV-Rentenzahlungen ausserhalb der Schweiz | de | 2026-09-15 |
| Central Compensation Office CCO | Bilaterale Abkommen | de | 2026-09-15 |
| Central Compensation Office CCO | Rückvergütungen | de | 2026-09-15 |
| Central Compensation Office CCO | Staatsangehörigkeit eines Staates mit Sozialversicherungsabkommen (AHV) | de | 2026-09-15 |
| City of Zurich, City Police | Anmeldung eines Hundes bei der Wohngemeinde | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, City Police | Hundekontrolle | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, Civil Registry Office | Benötigte Dokumente für die Heirat | Stadt Zürich | de | 2026-09-18 |
| City of Zurich, Civil Registry Office | Ehevorbereitung | Stadt Zürich | de | 2026-09-18 |
| City of Zurich, Civil Registry Office | Heiraten mit ausländischem Pass und Wohnort Zürich | Stadt Zürich | de | 2026-09-18 |
| City of Zurich, Naturalisation Division | Deutschkenntnisse | Stadt Zürich | de | 2026-09-15 |
| City of Zurich, Naturalisation Division | Einbürgerung und Stadtbürgerrecht | Stadt Zürich | de | 2026-09-15 |
| City of Zurich, Naturalisation Division | Erleichterte Einbürgerung | Stadt Zürich | de | 2026-09-15 |
| City of Zurich, Naturalisation Division | Grundkenntnisse | Stadt Zürich | de | 2026-09-15 |
| City of Zurich, Naturalisation Division | Ordentliche Einbürgerung | Stadt Zürich | de | 2026-09-15 |
| City of Zurich, Naturalisation Division | Stadtbürgerrecht in der Stadt Zürich beantragen | Stadt Zürich | de | 2026-09-15 |
| City of Zurich, Population Office | Erste Schritte | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, Population Office | Terminpflicht beim Personenmeldeamt | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, Population Office | Wegzug aus der Stadt Zürich | Stadt Zürich | de | 2026-09-18 |
| City of Zurich, Population Office | Zuzug in die Stadt Zürich | Stadt Zürich | de | 2026-09-11 |
| City of Zurich, Protection and Rescue Zurich | Medizinischer Notfall – richtig handeln | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, School Office | Einschulung | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, School Office | Kindergarten | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, School Office | Schulbotschafter*innen – Volksschule in verschiedenen Sprachen erklärt | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, School Office | Schulferien und schulfreie Tage | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, Tax Office | Kontakte und Öffnungszeiten des Steueramts | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, Tax Office | Steuererklärung für natürliche Personen der Stadt Zürich | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, Tax Office | Wegzug ins Ausland | Stadt Zürich | de | 2026-09-18 |
| City of Zurich, Traffic Department | Anwohnerparkkarte für Privatpersonen und Firmen | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, Traffic Department | Parkbewilligungen | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, Traffic Department | Parkscheibe für die Blaue Zone | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, Traffic Department | Tagesbewilligungen | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | Abfuhr Bioabfall | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | Abfuhr Hauskehricht | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | Abfuhr Sperrgut, Metall, Elektrogeräte und Grubengut | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | Entsorgungskalender | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | Gewusst wie | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | Kartonsammlung | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | Kunststoffsammlung | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | Papiersammlung | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | Recyclinghof | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | Sonderabfall-Sammelstelle | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | Wertstoff-Sammelstellen | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | Wo und wann entsorgen | Stadt Zürich | de | 2026-09-17 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | Züri-Sack | Stadt Zürich | de | 2026-09-17 |
| Federal Department of Foreign Affairs FDFA | Visabestimmungen für die Einreise in die Schweiz | de | 2026-09-17 |
| Federal Office for Customs and Border Security FOCBS | Moving to Switzerland: Procedure | en | 2026-09-11 |
| Federal Office for Customs and Border Security FOCBS | Umzug in die Schweiz: Vorgehen | de | 2026-09-11 |
| Federal Office for Housing BWO | Hypothekarischer Referenzzinssatz | de | 2026-09-18 |
| Federal Office of Public Health FOPH | Accident insurance: Who is subject to compulsory insurance? | en | 2026-09-19 |
| Federal Office of Public Health FOPH | Health insurance: Insured persons eligible to suspend accident cover | en | 2026-09-19 |
| Federal Office of Public Health FOPH | Health insurance: Premium subsidies | en | 2026-09-19 |
| Federal Office of Public Health FOPH | Health insurance: Requirement to obtain insurance for persons resident in Switzerland | en | 2026-09-11 |
| Federal Office of Public Health FOPH | Krankenversicherung: Prämienverbilligung | de | 2026-09-15 |
| Federal Office of Public Health FOPH | Krankenversicherung: Versicherungspflicht für in der Schweiz wohnhafte Versicherte | de | 2026-09-11 |
| Federal Office of Public Health FOPH | Krankenversicherung: Zur Sistierung der Unfalldeckung berechtigte Versicherte | de | 2026-09-18 |
| Federal Office of Public Health FOPH | Unfallversicherung: Wer ist obligatorisch versichert? | de | 2026-09-18 |
| Federal Social Insurance Office FSIO | EO bei Adoption | de | 2026-09-15 |
| Federal Social Insurance Office FSIO | EO bei Mutterschaft | de | 2026-09-15 |
| Federal Social Insurance Office FSIO | EO bei Vaterschaft | de | 2026-09-15 |
| Federal Social Insurance Office FSIO | Familienzulagen - Übersicht | de | 2026-09-15 |
| Federal Social Insurance Office FSIO | Kann ich mein BVG-Altersguthaben bar beziehen, wenn ich die Schweiz endgültig verlasse? | BSV | de | 2026-09-15 |
| Federal Social Insurance Office FSIO | Leistungen und Voraussetzungen | de | 2026-09-15 |
| Federal Social Insurance Office FSIO | Urlaub und Erwerbsersatz bei Mutterschaft, Vaterschaft und Adoption | de | 2026-09-15 |
| Federal Social Insurance Office FSIO | Welche Beiträge kann ich in die Säule 3a einzahlen? | BSV | de | 2026-09-18 |
| Federal Social Insurance Office FSIO | Wer kann eine Säule 3a (gebundene Selbstvorsorge) einrichten? | BSV | de | 2026-09-18 |
| Federal Tax Administration FTA | Schweizerische Quellensteuer QST | de | 2026-09-11 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | AIG / LEI / FNIA, SR 142.20 | de | 2026-09-10 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | FZA / ALCP, SR 0.142.112.681 | de | 2026-09-10 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | Fedlex: Code of Obligations, SR 220 | de | 2026-09-18 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | Fedlex: Constitution of the Canton of Zurich, SR 131.211 | de | 2026-09-18 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | Fedlex: Federal Constitution, SR 101 | de | 2026-09-18 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | Fedlex: Federal Direct Tax Act, SR 642.11 | de | 2026-09-15 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | Fedlex: Health Insurance Act, SR 832.10 | de | 2026-09-15 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | Fedlex: Ordinance on Entry and the Granting of Visas, SR 142.204 | de | 2026-09-17 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | Fedlex: Ordinance on the Admission of Persons and Vehicles to Road Traffic, SR 741.51 | de | 2026-09-15 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | Fedlex: Swiss Citizenship Act, SR 141.0 | de | 2026-09-15 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | Fedlex: Swiss Citizenship Ordinance, SR 141.01 | de | 2026-09-15 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | Fedlex: Tax at Source Ordinance of the FDF, SR 642.118.2 | de | 2026-09-15 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | Fedlex: Vested Benefits Act, SR 831.42 | de | 2026-09-15 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | Fedlex: ordinance on the refund of AHV contributions paid by foreign nationals, SR 831.131.12 | de | 2026-09-15 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | VZAE / OASA, SR 142.201 | de | 2026-09-10 |
| SERAFE AG, the Confederation's collection agency for the radio and television fee | Abgabeübersicht | de | 2026-09-17 |
| SERAFE AG, the Confederation's collection agency for the radio and television fee | Basic principle | en | 2026-09-19 |
| SERAFE AG, the Confederation's collection agency for the radio and television fee | Fee overview | en | 2026-09-19 |
| SERAFE AG, the Confederation's collection agency for the radio and television fee | Grundsatz | de | 2026-09-17 |
| SVA Zürich, the cantonal social insurance office | Beratung vor Ort | de | 2026-09-17 |
| SVA Zürich, the cantonal social insurance office | Familienzulagen: Angestellte | de | 2026-09-15 |
| SVA Zürich, the cantonal social insurance office | Familienzulagen: Nichterwerbstätige | de | 2026-09-15 |
| SVA Zürich, the cantonal social insurance office | Familienzulagen: Sinn und Zweck | de | 2026-09-15 |
| SVA Zürich, the cantonal social insurance office | Kontakt | de | 2026-09-17 |
| SVA Zürich, the cantonal social insurance office | Krankenversicherungspflicht: Anmeldung | de | 2026-09-15 |
| SVA Zürich, the cantonal social insurance office | Krankenversicherungspflicht: Wer kann sich befreien lassen? | de | 2026-09-15 |
| SVA Zürich, the cantonal social insurance office | Prämienverbilligung: Wer hat Anspruch? | de | 2026-09-15 |
| SVA Zürich, the cantonal social insurance office | Spezielle Öffnungszeiten | de | 2026-09-17 |
| SVA Zürich, the cantonal social insurance office | Telefon | de | 2026-09-17 |
| State Secretariat for Economic Affairs SECO, public employment service | Anmeldung und Registrierung | arbeit.swiss | de | 2026-09-18 |
| State Secretariat for Economic Affairs SECO, public employment service | FAQ zur Arbeitslosenentschädigung | arbeit.swiss | de | 2026-09-18 |
| State Secretariat for Economic Affairs SECO, public employment service | FAQs on unemployment benefit | arbeit.swiss | en | 2026-09-19 |
| State Secretariat for Economic Affairs SECO, public employment service | Signing on and registration | arbeit.swiss | en | 2026-09-19 |
| State Secretariat for Migration SEM | Aufenthalt | de | 2026-09-11 |
| State Secretariat for Migration SEM | Aufenthaltsbewilligungen für Nicht-EU/EFTA-Angehörige | de | 2026-09-11 |
| State Secretariat for Migration SEM | Ausländerinnen und Ausländer der dritten Generation | de | 2026-09-15 |
| State Secretariat for Migration SEM | Ausweis B EU/EFTA (Aufenthaltsbewilligung) | de | 2026-09-11 |
| State Secretariat for Migration SEM | Ausweis C EU/EFTA (Niederlassungsbewilligung) | de | 2026-09-11 |
| State Secretariat for Migration SEM | Ausweis Ci (Aufenthaltsbewilligung mit Erwerbstätigkeit) | de | 2026-09-11 |
| State Secretariat for Migration SEM | Ausweis Ci EU/EFTA (Aufenthaltsbewilligung mit Erwerbstätigkeit) | de | 2026-09-11 |
| State Secretariat for Migration SEM | Ausweis G (Grenzgängerbewilligung) | de | 2026-09-11 |
| State Secretariat for Migration SEM | Ausweis G EU/EFTA (Grenzgängerbewilligung) | de | 2026-09-11 |
| State Secretariat for Migration SEM | Ausweis L EU/EFTA (Kurzaufenthaltsbewilligung) | de | 2026-09-11 |
| State Secretariat for Migration SEM | Biometric residence permits for foreign nationals | en | 2026-09-11 |
| State Secretariat for Migration SEM | Brauche ich ein ETIAS? | de | 2026-09-11 |
| State Secretariat for Migration SEM | Cantonal immigration and employment market authorities | en | 2026-09-11 |
| State Secretariat for Migration SEM | Der biometrische Ausländerausweis | de | 2026-09-11 |
| State Secretariat for Migration SEM | Die Ordentliche Einbürgerung | de | 2026-09-15 |
| State Secretariat for Migration SEM | Do I require an ETIAS? | en | 2026-09-11 |
| State Secretariat for Migration SEM | Einreise mit Visum | de | 2026-09-11 |
| State Secretariat for Migration SEM | Einreise ohne Visum | de | 2026-09-11 |
| State Secretariat for Migration SEM | Einreisevoraussetzungen nach Staatsangehörigkeit | de | 2026-09-11 |
| State Secretariat for Migration SEM | Entry requirements by nationality | en | 2026-09-11 |
| State Secretariat for Migration SEM | Entry with visa | en | 2026-09-11 |
| State Secretariat for Migration SEM | Entry without visa | en | 2026-09-11 |
| State Secretariat for Migration SEM | Entry/Exit System (EES) | de | 2026-09-11 |
| State Secretariat for Migration SEM | Entry/Exit System (EES) | en | 2026-09-11 |
| State Secretariat for Migration SEM | FAQ Aufenthalt und Integrationskriterien | de | 2026-09-11 |
| State Secretariat for Migration SEM | FAQ – Einreise | de | 2026-09-11 |
| State Secretariat for Migration SEM | FAQ – Entry | en | 2026-09-11 |
| State Secretariat for Migration SEM | FAQ – Fragen zur Personenfreizügigkeit | de | 2026-09-11 |
| State Secretariat for Migration SEM | FAQ – Free Movement of Persons | en | 2026-09-11 |
| State Secretariat for Migration SEM | FAQ – Schweizer Bürgerrecht | de | 2026-09-15 |
| State Secretariat for Migration SEM | Grundlagen zur Arbeitsmarktzulassung | de | 2026-09-11 |
| State Secretariat for Migration SEM | Kantonale Migrations- und Arbeitsmarktbehörden | de | 2026-09-11 |
| State Secretariat for Migration SEM | Married with a Swiss citizen | en | 2026-09-19 |
| State Secretariat for Migration SEM | Meldeverfahren für kurzfristige Erwerbstätigkeit | de | 2026-09-11 |
| State Secretariat for Migration SEM | Nicht-EU/EFTA-Angehörige | de | 2026-09-11 |
| State Secretariat for Migration SEM | Non-EU/EFTA nationals | en | 2026-09-11 |
| State Secretariat for Migration SEM | Notification procedure for short-term work in Switzerland | en | 2026-09-19 |
| State Secretariat for Migration SEM | Ordinary naturalisation | en | 2026-09-19 |
| State Secretariat for Migration SEM | Regeln zur Berechnung der Aufenthaltsdauer | de | 2026-09-11 |
| State Secretariat for Migration SEM | Reisedokumente für ausländische Personen | de | 2026-09-11 |
| State Secretariat for Migration SEM | Residence | en | 2026-09-11 |
| State Secretariat for Migration SEM | Rules for calculating the length of stay | en | 2026-09-11 |
| State Secretariat for Migration SEM | Schengen Area | en | 2026-09-11 |
| State Secretariat for Migration SEM | Schengen-Raum | de | 2026-09-11 |
| State Secretariat for Migration SEM | Verheiratet mit einer Schweizerin oder einem Schweizer | de | 2026-09-15 |
| State Secretariat for Migration SEM | Visumantragsformular | de | 2026-09-11 |
| ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery) | Als Ausländerin oder Ausländer in der Schweiz arbeiten | de | 2026-09-14 |
| ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery) | Aufenthaltsbewilligung für die Schweiz: Gesuch und Erneuerung | de | 2026-09-14 |
| ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery) | Die 3. Säule der Altersvorsorge: 3a und 3b in der Schweiz | de | 2026-09-18 |
| ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery) | Gesuch um Familiennachzug in die Schweiz | de | 2026-09-14 |
| ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery) | Heiraten in der Schweiz | de | 2026-09-18 |
| ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery) | Mietvertrag, Untermietvertrag, Pachtvertrag in der Schweiz. | de | 2026-09-18 |
| ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery) | Stimm- und Wahlrecht in der Schweiz | de | 2026-09-18 |
| ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery) | Umzug in die Schweiz | de | 2026-09-15 |
| ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery) | Verlust, Diebstahl, Umtausch des Führerausweises in der Schweiz | de | 2026-09-15 |
| ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery) | Wohnen: Ruhezeiten, Mietzins und Mängel in der Schweiz | de | 2026-09-18 |

### Who published the pages, and what the excerpts are

Since release `mvp-zurich-2026-09-16-v2` every document names its
institution, served on every citation as the publisher with its level of
the state and the jurisdiction it speaks for:

| Institution | Level | Speaks for | Documents |
| --- | --- | --- | ---: |
| State Secretariat for Migration SEM | federal | CH | 46 |
| Canton of Zurich, Migration Office | cantonal | CH-ZH | 16 |
| Fedlex, the Swiss federal law collection (Federal Chancellery) | federal | CH | 15 |
| City of Zurich, Waste Disposal and Recycling (ERZ) | municipal | CH-ZH-261 | 13 |
| ch.ch, the information portal of the Confederation, cantons and communes (Federal Chancellery) | federal | CH | 10 |
| SVA Zürich, the cantonal social insurance office | cantonal | CH-ZH | 10 |
| Federal Social Insurance Office FSIO | federal | CH | 9 |
| Federal Office of Public Health FOPH | federal | CH | 8 |
| Canton of Zurich, Cantonal Tax Office | cantonal | CH-ZH | 7 |
| Canton of Zurich, Road Traffic Office | cantonal | CH-ZH | 7 |
| City of Zurich, Naturalisation Division | municipal | CH-ZH-261 | 6 |
| State Secretariat for Economic Affairs SECO, public employment service | federal | CH | 4 |
| SERAFE AG, the Confederation's collection agency for the radio and television fee | federal | CH | 4 |
| Central Compensation Office CCO | federal | CH | 4 |
| City of Zurich, Population Office | municipal | CH-ZH-261 | 4 |
| City of Zurich, School Office | municipal | CH-ZH-261 | 4 |
| City of Zurich, Traffic Department | municipal | CH-ZH-261 | 4 |
| Canton of Zurich, Office for Municipalities, Naturalisation Division | cantonal | CH-ZH | 4 |
| City of Zurich, Tax Office | municipal | CH-ZH-261 | 3 |
| City of Zurich, Civil Registry Office | municipal | CH-ZH-261 | 3 |
| Canton of Zurich, Office for the Economy | cantonal | CH-ZH | 3 |
| Federal Office for Customs and Border Security FOCBS | federal | CH | 2 |
| City of Zurich, City Police | municipal | CH-ZH-261 | 2 |
| Federal Office for Housing BWO | federal | CH | 1 |
| Federal Department of Foreign Affairs FDFA | federal | CH | 1 |
| Federal Tax Administration FTA | federal | CH | 1 |
| City of Zurich, Protection and Rescue Zurich | municipal | CH-ZH-261 | 1 |
| Canton of Zurich, Health Directorate | cantonal | CH-ZH | 1 |
| Canton of Zurich, Directorate of Justice and Home Affairs, tenancy forms | cantonal | CH-ZH | 1 |
| Canton of Zurich, Statistical Office, elections and votes | cantonal | CH-ZH | 1 |
| Canton of Zurich, Veterinary Office | cantonal | CH-ZH | 1 |
