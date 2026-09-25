# User acceptance tests

**Last update:** 25 September 2026
**Scope:** the two standing cases of section 3.3 of the
[functional specification](https://github.com/swisstip/swiss-tip/blob/main/docs/product/functional-specification.md), four further
cases chosen because the popular answer misses an exception in the law, a
Swiss citizen's question in Zurich
German about a residence permit for a foreign spouse, and their edge cases,
as a user would experience them through an MCP-capable assistant; ten cases
on the moving-to-Switzerland topics and naturalisation (UAT-8 to UAT-17);
six office-contact cases (UAT-18 to UAT-23), four of them with a negative
answer the cited page states; eleven daily-life cases (UAT-24 to UAT-34) on
waste, parking, vehicles, dogs, kindergarten, the tax return, the radio and
television fee and medical emergencies; ten
cross-jurisdiction cases (UAT-35 to UAT-44) asked from another canton or
from a Zurich municipality other than the city, which expect everything the
release serves for that place and nothing published for another; six
entry-and-visa cases (UAT-45 to UAT-50); three cases on voting rights and the
tax-at-source tariff (UAT-51 to UAT-53); eleven expat-life cases (UAT-54 to
UAT-64); two settlement-permit cases on the five-year routes by nationality
(UAT-65 and UAT-66); five cases on the integration offers of the Canton of
Zurich (UAT-67 to UAT-71); nine customs cases on travelling, ordering from
abroad and moving goods (UAT-72 to UAT-80); eight cases on basic health
insurance, its cost sharing, models, change of insurer and cover abroad
(UAT-81 to UAT-88); and nineteen
server-only decline cases (DECLINE-1 to
DECLINE-12 and SEARCH-DECLINE-1 to SEARCH-DECLINE-7) that check the server
rejects a request the release does not cover, at the resolve step and at
the search step.<br>
**System under test:** the Swiss TIP MCP server (`apps/mcp-server`) on the
active KB1 release. The calling assistant is not under test; any MCP client
with a capable model may run the cases.<br>
**How to execute:** `scripts/test/mock-mcp/run_opencode_test.py --server
real --live` (UAT-1, both scenarios) and `--case <name>` for the single-turn
cases (`german-work-permit`,
`swiss-german-family-permit`, `family-child-deadline`,
`marriage-separation`, `settlement-after-l-permit`,
`social-assistance-permit`, and the extension cases
`ahv-refund-leaving`, `pension-fund-cash-out`, `tax-at-source-threshold`,
`german-tax-at-source-marriage`, `foreign-licence-twelve-months`,
`control-drive-licence`, `health-insurance-first-months`,
`premium-reduction-arrival`, `naturalisation-b-permit`,
`german-facilitated-naturalisation`, and the office-contact cases
`migration-office-hours`, `migration-office-email`, `road-office-oerlikon`,
`population-office-saturday`, `german-sva-visit`,
`german-tax-at-source-contact`, and the daily-life cases `dog-moving-in`,
`rubbish-bags`, `sofa-disposal`, `recycling-centre-saturday-cash`,
`blue-zone-lunchtime`, `german-car-move`, `kindergarten-cut-off`,
`german-tax-access-code`, `serafe-without-tv`, `ambulance-costs`,
`road-office-hours`, and the cross-jurisdiction cases
`bern-short-contract-permit`, `aargau-commuter-registration`,
`german-licence-st-gallen`, `bern-naturalisation`,
`lucerne-premium-reduction`, `german-zug-tax-at-source`,
`bern-migration-office`, `winterthur-registration`, `uster-dog-move`,
`german-kloten-car-parking`, and the voting-rights and tariff cases
`c-permit-city-vote`, `winterthur-tax-at-source-rate`,
`german-bern-voting-rights`, and the expat-life cases
`zurich-education-allowance` to `german-moving-goods-customs`); `--server none` runs the same question without
any server as the control. For the optional hybrid configuration, add
`--semantic-index releases/mvp-zurich/semantic-index.json` to `--server real`.
The offline edge cases run in
`scripts/test/mcp/check_server.py` without a model, and the decline cases
in the build's `accept` stage. Every execution is
recorded under `.local/experiments/`; this document holds no run data beyond
the current state under Execution records.

Search expectations depend on the configured and observed retrieval mode.
Default lexical search uses the release's indexed terms; French
questions may need reformulation using English or German terms. Optional
hybrid search accepts original-language queries through the local embedding
model. Each run records the requested configuration and every returned
`retrieval_mode` and `fallback_reason`: configured hybrid search may fall
back to lexical search. An empty candidate list does not establish that a
topic is uncovered, and a nonempty list does not establish applicability or
complete support for the question. The caller uses the coverage declaration
and scoped `resolve` results to determine what is supported. The answer,
citation, context and efficiency requirements below apply in both modes.

## Case index

| Test | Question | The trap a generic answer falls into | Served concepts |
| --- | --- | --- | --- |
| UAT-1a, 1b | Czech citizen starting work in Zurich: by when to register with the municipality | Counting 14 days from the first working day; computing a date before knowing the arrival | `eu-employment-registration-deadline`, `zh-eu-registration`, `city-zurich-arrival` |
| UAT-2e | Third-country national (an Indian citizen), in German: may I work in Switzerland, under which conditions | Mixing in EU/EFTA rules; inventing quotas and procedures; translating the question into English before searching, and answering in English, although the release carries German aliases and the search accepts German | `third-country-work`, `aig-work-permit`, `permit-authority`, `permit-b` |
| UAT-3 | B permit holder wants to bring a 13-year-old child after four years | A plain yes; the twelve-month deadline for children over twelve is missed | `family-deadlines`, `family-b` |
| UAT-4 | Spouse of a Swiss citizen separating after two years of marriage | Three years of marriage treated as the only route; loss predicted as certain | `family-separation`, `family-swiss` |
| UAT-5 | Ten years in Switzerland, three on an L permit: C permit now? | Counting presence instead of the last five continuous years on B; carrying the five-year rule over to a nationality the served list does not name | `permit-c`, `permit-c-five-years` |
| UAT-6 | B permit holder about to need social assistance: is the permit revoked? | Automatic revocation asserted | `social-assistance-review`, `permit-b` |
| UAT-7 | Swiss citizen, in Zurich German: residence permit for a Brazilian spouse, and by when to claim reunification | Applying the Art. 44 conditions (housing, income, language) to a Swiss sponsor; translating the dialect into English before searching | `family-swiss`, `family-deadlines`, `permit-authority` |
| UAT-8 | German citizen leaving for good: can the AHV contributions be refunded | A plain yes with the refund form; the refund exists only for nationals of states without a social security agreement and of the named agreement states | `ahv-contribution-refund`, `ahv-pension-abroad` (planned) |
| UAT-9 | Moving to Munich for a job: whole pension fund in cash | Definitive departure treated as a full cash-out; since 2007 the mandatory part stays blocked while the person is insured in the EU/EFTA state | `bvg-cash-out-departure` (planned) |
| UAT-10 | B permit, CHF 135,000 gross, taxed at source: must a tax return be filed | Tax at source treated as final; from CHF 120,000 the subsequent ordinary assessment is mandatory | `zh-tax-at-source-ordinary-assessment`, `zh-tax-at-source-liability` (planned) |
| UAT-11 | B permit holder marrying a Swiss citizen, in German: still taxed at source | Tax at source tied to the permit; marriage to a Swiss or C permit holder ends it | `zh-tax-at-source-liability`, `tax-at-source-liability` (planned) |
| UAT-12 | US licence, 14 months in Zurich: still allowed to drive, still exchangeable | Foreign licence treated as valid indefinitely; after twelve months no driving until the exchange | `zh-foreign-licence-exchange`, `foreign-licence-exchange` (planned) |
| UAT-13 | Indian licence, two months in Zurich: a simple swap | A plain swap, or the full Swiss test; a control drive with one attempt | `zh-foreign-licence-exchange`, `zh-control-drive` (planned) |
| UAT-14 | Two months in Zurich, no health insurance yet: too late, and from when are premiums due | Cover and premiums from the signing date; both run from the date of residence when joining within three months | `health-insurance-deadline`, `zh-health-insurance-exemption` (planned) |
| UAT-15 | Arrived from Italy in May on a modest salary: premium reduction, and from when | One national rule, automatic, or next year; cantonal, on application, from the month after arrival | `zh-premium-reduction`, `premium-reduction` (planned) |
| UAT-16 | Turkish citizen, eleven years in Switzerland, B permit, eighteen months in the city: citizenship now | Counting the years; the C permit and two years in the municipality are missing | `naturalisation-ordinary`, `zh-naturalisation-ordinary`, `city-zurich-naturalisation` (planned) |
| UAT-17 | Brazilian spouse of a Swiss citizen on a B permit, in German: facilitated naturalisation without a C permit | The C permit of the ordinary procedure applied to the facilitated one | `naturalisation-facilitated-spouse`, `zh-naturalisation-facilitated` (planned) |
| UAT-18 | Address and opening hours of the cantonal Migration Office | Generic hours, invented directions or e-mail, the city office instead of the cantonal one | `zh-migrationsamt-contact` |
| UAT-19 | E-mail address of the Migration Office | An invented address, or "no information", although the office states it has no e-mail address | `zh-migrationsamt-contact` |
| UAT-20 | Road traffic office in Oerlikon | An invented branch; the published list has no Oerlikon location | `zh-road-traffic-office-locations` |
| UAT-21 | Renewing a permit card at the Personenmeldeamt on a Saturday without an appointment | A walk-in or Saturday hours; the office is closed on Saturdays and renewals need an appointment | `city-zurich-population-office` |
| UAT-22 | SVA Zurich, in German: appointment and the way from the main station | An appointment assumed; an invented route | `zh-sva-contact`, `zh-sva-telephone-numbers` |
| UAT-23 | Tax-at-source department, in German: telephone and hours | The general number only; an invented e-mail address | `zh-tax-office-contact` |
| UAT-24 | Moving into the City of Zurich with a dog | Registration only; "no course needed", although the cantonal training duty of June 2025 applies to people moving in | `city-zurich-dog-registration`, `zh-dog-keeping` |
| UAT-25 | Rubbish bags, their price and the collection day | Any bag; the fee share quoted as the price; an invented weekday | `city-zurich-household-waste` |
| UAT-26 | An old sofa, no car | Leaving it on the street; a free day or an online booking | `city-zurich-bulky-waste-pickup`, `city-zurich-recycling-centres`, `city-zurich-hazardous-waste` |
| UAT-27 | Werdhölzli recycling centre on Saturday afternoon, paying cash | Weekday hours applied to Saturday; cash assumed | `city-zurich-recycling-centres` |
| UAT-28 | Blue zone, arriving at 12:10 | One hour from arrival; the lunchtime rule (until 14.30) is missed | `city-zurich-parking-permits` |
| UAT-29 | Moving from Bern with a car, in German | Keeping the plates; the insurance certificate missed | `zh-vehicle-registration-move`, `city-zurich-first-steps` |
| UAT-30 | Kindergarten for a child born on 10 August 2023 | August 2027; the 31 July cut-off is missed | `city-zurich-kindergarten` |
| UAT-31 | Lost access code for the online tax return, in German | The city's tax office named; a deadline from memory | `city-zurich-tax-return` |
| UAT-32 | The Serafe invoice without a TV | "No device, no fee" | `radio-tv-household-fee` |
| UAT-33 | Medical emergency: the number and who pays the ambulance | A free ambulance; basic insurance pays it all | `city-zurich-medical-emergency` |
| UAT-34 | Road Traffic Office: opening hours and appointments | Generic hours; an appointment required | `zh-road-traffic-office-locations` |
| UAT-35 | German citizen, eight-month contract, living and working in Bern: which permit, where to apply | The Canton of Zurich's page (the fifteen-hour condition, the Zurich Migration Office) given for Bern; or a refusal although the federal rules answer it | `fza-employee-permit`, `eu-employment-registration-deadline`, `permit-authority`, `cantonal-migration-contact` (Bern); `zh-eu-l` rejected |
| UAT-36 | French citizen living in Baden (Aargau), job in Zurich: where to register, which office issues the permit | Following the employer's address to the Zurich Migration Office or the City of Zurich's Personenmeldeamt | `eu-employment-registration-deadline`, `aig-registration`, `permit-authority`, `cantonal-migration-contact` (Aargau); `zh-eu-registration`, `city-zurich-arrival`, `zh-migrationsamt-contact` rejected |
| UAT-37 | Brazilian licence, ten months in St. Gallen, in German: how long still, how to exchange | The Zurich Road Traffic Office, its form and its country lists given for St. Gallen | `foreign-licence-exchange`; `zh-foreign-licence-exchange`, `zh-control-drive`, `zh-road-traffic-office-locations` rejected |
| UAT-38 | Portuguese citizen with a C permit, twelve years in Switzerland, three in the city of Bern: citizenship, years in Bern, cost | Zurich's two years in the municipality, its CHF 500 and its Gemeindeamt given for Bern | `naturalisation-ordinary`; `zh-naturalisation-ordinary`, `city-zurich-naturalisation`, `zh-naturalisation-division-contact` rejected |
| UAT-39 | Moved from Austria to Lucerne on a modest salary: premium reduction, where to apply | The SVA Zurich and Zurich's start of entitlement given for Lucerne; a Lucerne office from general knowledge | `premium-reduction`; `zh-premium-reduction`, `zh-sva-contact` rejected |
| UAT-40 | B permit, CHF 140,000, resident of Zug, in German: tax return, which office | The Zurich Cantonal Tax Office or the Zurich directive given for Zug; tax at source treated as final | `tax-at-source-liability`; `zh-tax-at-source-ordinary-assessment`, `zh-tax-at-source-liability`, `zh-tax-office-contact` rejected |
| UAT-41 | Address and opening hours of the migration office of the Canton of Bern | The Zurich Migration Office's hours or address given for Bern; invented hours or e-mail address | `cantonal-migration-contact` (Bern); `zh-migrationsamt-contact` rejected |
| UAT-42 | Spanish citizen moving from Madrid to Winterthur: how to register, appointment needed | The City of Zurich's compulsory appointment and its Personenmeldeamt given for Winterthur | `eu-employment-registration-deadline`, `zh-eu-registration`, `zh-eu-b`; `city-zurich-arrival`, `city-zurich-arrival-documents`, `city-zurich-population-office` rejected |
| UAT-43 | Moving from Germany to Uster with a dog: duties, where to register | The City Police's dog control given for Uster; "no course is needed" | `zh-dog-keeping`; `city-zurich-dog-registration` rejected |
| UAT-44 | Moving from Lucerne to Kloten with a car, in German: the Road Traffic Office, the price of a resident parking card | The City of Zurich's CHF 300 card and permit office given for Kloten | `zh-vehicle-registration-move`; `city-zurich-parking-permits`, `city-zurich-first-steps` rejected |
| UAT-45 | 60 Schengen days already used, 50 more planned: is that allowed | A fresh 90 days per entry, per country or per calendar half-year; a date computed without the user's dates | `entry-short-stay-rule` |
| UAT-46 | Two-year job in Zurich: which visa, and who approves it | A Schengen visa C for a two-year stay; a visa granted without the cantonal migration office | `entry-visa-types`, `entry-visa-application` |
| UAT-47 | Schengen visa for an adult and an eight-year-old: fee, decision time, insurance | One flat fee, a decision in days, no insurance requirement | `entry-visa-fee-insurance` |
| UAT-48 | ETIAS before the flight, and the passport stamp | Telling the user to apply for ETIAS now; saying the passport is still stamped | `entry-etias`, `entry-exit-system` |
| UAT-49 | Indian citizen, two-week holiday: do I need a visa | Answering yes or no from memory, although the release serves the rule and not the country list | `entry-visa-need` |
| UAT-50 | Short-stay L permit in Zurich: can the wife and a ten-year-old come, with which documents | Refusing reunification on an L permit outright; the documents of the B or C route | `zh-family-l-permit` |
| UAT-51 | Twelve years on a C permit in the city of Zurich: may I vote in the city elections | A yes for the long stay or the C permit; "some municipalities allow it" carried over from other cantons | `zh-political-rights`, `political-rights-federal` |
| UAT-52 | B permit in Winterthur, taxed at source: how much, and less in the city of Zurich | A percentage from memory; Winterthur's own tax multiplier said to change the deduction | `zh-tax-at-source-tariffs`, `tax-at-source-tariff-codes` |
| UAT-53 | Ten years on a C permit in Bern, in German: may I vote in the cantonal elections | The Canton of Zurich's rule or its church exception given for Bern; a yes or no for Bern from memory | `political-rights-federal`; `zh-political-rights` rejected |
| UAT-54 | Employee in Zurich, 17-year-old son in vocational school: family allowance and how to claim | The child allowance of CHF 215 for a 17-year-old; another canton's rate; a claim at SVA Zurich by an employee | `zh-family-allowances`, `family-allowances` |
| UAT-55 | Paternity leave: length, timing and pay | Four weeks or more; one block right after the birth; full pay | `parental-leave` |
| UAT-56 | A deposit of four months' rent paid into the landlord's account | Accepting it because the market is tight | `tenancy-agreement` |
| UAT-57 | A rent increase by e-mail from next month, in German | Accepting an increase without the official form and the notice period | `rent-changes` |
| UAT-58 | Previous tenant paid 15 percent less, flat in Winterthur | No challenge after signing; the City of Zurich's offices given for Winterthur | `rent-changes`, `zh-initial-rent-form` |
| UAT-59 | Brazilian fiancée abroad, groom on a B permit in the city of Zurich: can we marry, how early to start | No check of a lawful stay; starting a few weeks before | `city-zurich-marriage`, `marriage-switzerland` |
| UAT-60 | Leaving the City of Zurich for India: deregistration deadline and taxes | No deadline; leaving taxes open | `city-zurich-departure` |
| UAT-61 | Employee with a pension fund: pillar 3a maximum and withdrawal on leaving | The self-employed maximum; no withdrawal before retirement | `pillar-3a` |
| UAT-62 | Ten months of work on a B permit, job lost: unemployment benefit? | A plain yes because of the B permit, ignoring the 12 months of contributions | `unemployment-benefit`, `zh-unemployment-benefit` |
| UAT-63 | Cleaner working six hours a week: insured for a skiing accident? | The employer's insurance assumed to cover leisure accidents whatever the hours | `accident-insurance` |
| UAT-64 | Moving from Munich with furniture and a car, in German: customs duty? | Duty on everything, or duty-free without prior use and the form | `moving-goods-customs` |
| UAT-65 | German citizen, five years in Zurich: settlement permit already, or only after ten years? | The ten-year rule applied to every nationality; a language certificate asked of a German national | `permit-c-five-years`, `zh-permit-c-five-years` |
| UAT-66 | US citizen, five years in Zurich, after an Italian colleague's remark: does the five-year route apply? | Ten years because the user is a third-country national; the language exemption carried over from Germany, Austria and Liechtenstein | `zh-permit-c-five-years` |
| UAT-67 | Brazilian newcomer in Winterthur looking for a German course and for advice on choosing one | The cantonal database only, although Winterthur keeps its own; invented course names, dates or prices | `zh-integration-offers` |
| UAT-68 | Family on a family-reunification permit, two weeks in the canton: whose job is it to inform them? | The Migration Office named as the body that informs about integration offers; a welcome talk promised | `zh-newcomer-first-information` |
| UAT-69 | Remarks about skin colour at work: is it racist discrimination, and who advises? | A definition without an address; the described behaviour called punishable although Article 261bis covers acts in public | `zh-racism-protection` |
| UAT-70 | Association in Uster asking for 4,000 francs for a neighbourhood festival | The 31 October deadline or the 50,000-franc maximum of the larger projects; the money promised | `zh-integration-project-funding` |
| UAT-71 | Tamil associations in the canton: are there any, and how to find one? | Associations named from general knowledge; or claiming the canton has no directory | `zh-migrant-associations` |

## Acceptance criteria that apply to every case

| # | Criterion | How it is judged |
| --- | --- | --- |
| A1 | Every statement in the answer traces to a served fact and its cited official page | Compare the answer with the facts and citations in the resolve result |
| A2 | The answer cites the URLs the server returned | URLs present in the answer |
| A3 | Nothing the release does not know is invented: a missing user fact is asked for, an uncovered question is declined by name | No computed date before the user supplied the inputs; out-of-scope questions answered with the scope statement |
| A4 | The server composes no answer: results carry facts, excerpts, citations, statuses and guidance only | Inspect the tool results |
| A5 | Review status is visible: every result's `limitations` name the review status of the served facts | Present in every tool result |
| A6 | Efficiency: the case is answered within the call and byte budget | Tool calls and result bytes counted by the harness |
| A9 | For UAT-19 to UAT-22, UAT-27, UAT-31 and UAT-34: a negative the cited page states is reported as the office's statement, not as missing information, and nothing is invented in its place | The answer says "no e-mail address", "closed on Saturdays", "no appointment needed", "no location in Oerlikon", "no cash" or "the city cannot issue the code" and names no invented address, hours or office |
| A10 | For UAT-35 to UAT-44, UAT-52, UAT-53 and UAT-58: the answer is scoped to the user's canton and municipality. It gives everything the release serves for that place (federal facts in every canton, Canton of Zurich facts in every Zurich municipality, the canton's own entry in SEM's directory), names the cantonal or municipal part the release does not publish for that place instead of filling it, and carries over no office, address, telephone number, opening hours, deadline, fee, form or procedure published for another canton or municipality | Compare the answer with the facts the resolve results served for the user's place; the harness also checks that no resolve that returned facts ran for another canton or municipality than the user's (`resolves_stay_in_user_jurisdiction`), and the case's must-not patterns name the Zurich details most likely to be carried over |

Budgets: UAT-1 turn 1 at most 3 tool calls and 20 KB of tool results; the
single-turn cases UAT-2e to UAT-44 at most 4 calls and 30 KB. Sizes are UTF-8
bytes of returned tool-output strings: 20,000 and 30,000 bytes respectively,
excluding transport framing.

A7, for UAT-3 to UAT-6, UAT-8 to UAT-17, the daily-life cases with a
named trap (UAT-24 to UAT-26, UAT-28 to UAT-30, UAT-32 and UAT-33), the
cross-jurisdiction cases UAT-40 and UAT-43 and the settlement-permit cases
UAT-65 and UAT-66: the grounded answer states the
exception in the law that the popular answer misses. The control run without
the server shows whether the model states it on its own; the comparison is
part of the record, not of the verdict.

A8, for the non-English cases UAT-2e, 7, 11, 17, 22, 23, 29, 31, 37, 40, 44, 53, 57 and 64: the answer is in the
question's language. Where the release's aliases cover the question's
language, the search is sent in that language and not translated into
English first; the harness records the language of every search query.
Neither translation nor its absence establishes a pass: the returned mode
and the final answer's grounding must also be checked.

## UAT-1: Czech citizen registering in Zurich

**Preconditions.** The release serves the federal registration deadline
for EU/EFTA nationals (concept `eu-employment-registration-deadline`, with
the required user facts arrival date, first working day, employment duration
and the decision rule "the earlier of 14 days after arrival and before the
first working day"), the Canton of Zurich procedure (`zh-eu-registration`)
and the City of Zurich move-in procedure (`city-zurich-arrival`).

**Turn 1, user:** "I'm a Czech citizen and starting my work in Zurich next
week. By when latest should I register my stay on the municipal authority?"

**Expected after turn 1**

- The assistant derives `population = eu_efta` from "Czech citizen" and
  resolves the federal, cantonal and city concepts for `CH-ZH` (and
  `CH-ZH-261` when it assumes the city).
- The answer states both limits: within 14 days of arrival and before
  starting work, and that the earlier one binds.
- The answer asks for the arrival date (and the first working day) instead
  of computing a date. It does not treat the first working day as the
  arrival date.
- The answer cites the SEM free-movement FAQ and the Zurich pages.
- At most 3 tool calls.

**Turn 2, user:** the two dates and the contract length (scenario table).

**Expected after turn 2**

| Scenario | User supplies | Expected deadline |
| --- | --- | --- |
| 1a work-first | Arrival Sunday 13 September 2026, first working day Wednesday 16 September 2026, open-ended contract | Before 16 September, so by Tuesday 15 September 2026; the 14-day limit (27 September) is shown as not binding |
| 1b fourteen-days-first | Arrived Tuesday 1 September 2026, first working day Friday 18 September 2026, two-year contract | 1 September plus 14 days: Tuesday 15 September 2026, which is earlier than the first working day |

Both limits are shown so the user sees which one binds. The answer may add
the served practical facts (appointment at the Personenmeldeamt, documents
to bring); it must not add anything the release does not serve.

### UAT-1 edge cases

| ID | Variation | Expected |
| --- | --- | --- |
| 1c | Arrival date equals the first working day | Registration must be complete before work starts, which is the arrival day itself; the answer says so and notes that registration is possible only after the actual move-in |
| 1d | Arrival on a day the office is closed (weekend) | The deadline is not moved; the answer names the last office day before the binding limit and says opening hours and appointment availability are not covered (out of scope) |
| 1e | Contract of up to three months | Covered: `eu-short-employment` with `population = eu_efta` is `SUPPORTED` with the notification procedure (the employer notifies online by the day before work starts; no permit; longer employment needs a residence permit), and the deadline concept's `employment_duration` instruction points to it; the assistant states the notification instead of the 14-day rule. Pinned in the round-trip check |
| 1f | Third-country national (for example an Indian citizen) asks the same question | `population = third_country`: the EU/EFTA deadline concept is `OUT_OF_COVERAGE` with `context_not_covered` naming `population=eu_efta`; the federal registration duty (`aig-registration`) and the third-country work admission still apply; the answer must not state the 14-day EU/EFTA rule as applicable |
| 1g | Nationality not stated | The deadline concept returns `NEEDS_CONTEXT` for `population` with the allowed values; the assistant asks whether the user is an EU/EFTA citizen before answering |
| 1h | The user lives in another canton (Bern) | Federal facts `SUPPORTED` at `CH (federal)`; the Zurich concepts `OUT_OF_COVERAGE` with `jurisdiction_not_covered` naming `CH-ZH`; the Bern migration-office contact is served; the answer gives the federal rule and says no cantonal procedure is published for Bern |
| 1i | A municipality in the Canton of Zurich other than the city (`CH-ZH-53`) | Cantonal facts `SUPPORTED`; the City of Zurich concept `OUT_OF_COVERAGE`; the appointment rule of the city is not stated as applying |
| 1j | Jurisdiction sent in short form (`ZH`, `261`) | Normalized to `CH-ZH` and `CH-ZH-261`; same result as the full codes; `executed_scope` shows the normalized codes |
| 1n | Jurisdiction sent in names, the city alone (`{"city": "Zurich"}`) | The place register turns it into `CH-ZH-261` and supplies `CH-ZH`; same result as the codes; `executed_scope` shows the codes and the official names (`Switzerland`, `Zürich`, `Zürich`). Pinned in the round-trip check and in the regression cases `PN-1` to `PN-4` |
| 1o | A quarter given as the city (`{"canton": "Kanton Zürich", "city": "Oerlikon"}`) | A quarter is not a municipality: `executed_scope.not_recognised` names `city: Oerlikon`, the request runs for `CH-ZH`, the cantonal facts are served and the guidance says which place the result is for and that the municipality's official name resolves the city's facts. Pinned in the round-trip check |
| 1p | A name several municipalities share (`{"city": "Buchs"}`) | `INVALID_ARGUMENT` on `jurisdiction.city` listing Buchs (AG), Buchs (SG) and Buchs (ZH) with their codes; the assistant asks for the canton. Pinned in the round-trip check |
| 1k | Applicability date after 13 November 2026 (`as_of` later than `stale_from`) | Status `STALE`: the facts are served with a freshness warning naming the snapshot date; the answer passes the warning on |
| 1l | UK citizen taking up new employment | Covered: `uk-new-employment` with `population = uk_new` (valid from 1 January 2021) is `SUPPORTED` (no notification procedure, a work permit under the AIG applied for by the Swiss employer), and the EU/EFTA deadline concept is `OUT_OF_COVERAGE` with `context_not_covered` for `uk_new`; the assistant does not treat the user as EU/EFTA. Pinned in the round-trip check |
| 1m | The user asks the fee or the processing time | Out of scope by name; the assistant quotes the scope statement and does not guess |

## UAT-2e: third-country national asking about a work permit, in German

The second standing case. It keeps the ID UAT-2e that the acceptance suite,
the harness and the records use.

**Preconditions.** The release serves the third-country work admission
(`third-country-work`), the federal permit duty (`aig-work-permit`), the
issuing authority (`permit-authority`), the permit types L, B and C and the
integration criteria, all conditioned or unconditioned as published. It
carries German terms for the concepts the question touches: authored aliases
(`third-country-work`: `Arbeitsbewilligung Drittstaaten`,
`Erwerbstaetigkeit Nicht-EU/EFTA`; `permit-b`: `Aufenthaltsbewilligung B`;
`aig-work-permit`: `Bewilligung Erwerbstaetigkeit`; `permit-authority`:
`kantonales Migrationsamt`), source terms copied from the SEM and Fedlex
excerpts (`Nicht-EU/EFTA-Angehörige`, `gut qualifiziert`, `Führungskräfte`,
`Arbeitgeber`, `Aufenthaltsbewilligung`, `Kurzaufenthaltsbewilligung`) and
everyday words (`Drittstaatsangehörige`, `darf ich in der Schweiz
arbeiten`), so default lexical search ranks `third-country-work` among the
first hits for the question as typed. The current `search` description
explains lexical and optional semantic retrieval and treats hits as
candidates; it does not guarantee complete support for the question. The
manifest declares `de` and `en` as evidence languages (the SEM excerpts
behind `third-country-work` are German).

**User:** "Ich habe die indische Staatsbürgerschaft. Darf ich in der Schweiz
arbeiten? Welche Voraussetzungen gelten für eine Arbeitsbewilligung und eine
Aufenthaltsbewilligung?" ("I hold Indian citizenship. May I work in
Switzerland? Which conditions apply to a work permit and a residence
permit?")

**What this case demonstrates.** The server has no language parameter and
translates nothing. For a language its aliases cover, the caller does not
need to translate either: the German question, sent to default lexical
`search` as typed, ranks `third-country-work` among the first three hits
(aliases matched); the offline round-trip check exercises the lexical
retrieval. Optional hybrid search may rank those candidates differently, so
its actual results are recorded separately. The answer is composed in
German from the English fact statements, as in every other case.

**Expected**

- The first `search` carries the German question or its German key terms
  (Arbeitsbewilligung, Aufenthaltsbewilligung, Schweiz, arbeiten,
  Staatsbürgerschaft), not an English rendering; the record lists every
  query the caller sent. An empty result is a retrieval miss, not proof that
  the release lacks third-country work facts.
- The assistant resolves `third-country-work` with `population =
  third_country` (with `permit-b` and the other permit concepts as it sees
  fit) and answers in German from the served facts: admission limited to
  well-qualified persons (managers, specialists, graduates with experience),
  the employer's proof that nobody suitable is available in Switzerland or
  the EU/EFTA, pay, social contributions and conditions at local standards,
  the permit required before work regardless of duration and applied for by
  the employer, the cantonal migration office as issuing authority, B permit
  for stays over a year.
- It cites the SEM third-country work page (and Fedlex where the AIG is
  quoted) and states the snapshot date. It does not apply EU/EFTA rules (no
  EU/EFTA registration deadline, no notification procedure) and does not add
  quotas, procedures or fees. A 14-day registration duty is correct only as
  the served third-country fact (`third-country-work-procedure`: register
  within 14 days of arrival and before starting work).
- At most 4 tool calls and 30 KB.

### UAT-2e edge cases

| ID | Variation | Expected |
| --- | --- | --- |
| 2a | The same question from an EU/EFTA citizen (for example a German) | The third-country concept is `OUT_OF_COVERAGE` with `context_not_covered`; the EU/EFTA concepts apply instead (registration deadline, Zurich procedures where the canton is known) |
| 2b | The user asks about annual quotas | Out of scope by name (the scope list names quotas); the assistant declines the quota question based on that declaration. Search may return adjacent concepts in either mode, but their presence does not establish quota coverage |
| 2c | The user asks for the application procedure step by step or the forms | Out of scope by name; only the served facts that the employer applies to the cantonal authority are stated |
| 2d | The user asks about family reunification for the worker's spouse | Covered: the family reunification concepts for a B or C permit holder are served with their conditions (`sponsor_status`); the assistant asks for the sponsor's permit when unknown |
| 2f | The user is already in Switzerland and asks whether they may start work before the permit | The served AIG facts apply: a permit is required before taking up work; nothing about interim permission is invented |
| 2g | The user asks whether their qualification is sufficient | The assistant states the published criteria and says that the release does not decide individual eligibility (scope statement) |
| 2h | The same question in French | Same facts, answered in French. Default lexical search has limited French terms and may need reformulation in English or German; optional hybrid search can receive the French question directly. The record names the actual mode and any fallback. Search results alone do not decide coverage |

## UAT-3: family reunification for a child over twelve

**Preconditions.** The release serves the reunification deadlines of AIG
Art. 47 (`family-deadlines`: five years, twelve months for children over
twelve; the start of the deadline; late reunification only for important
family reasons, children over fourteen heard) and the conditions for a
residence-permit sponsor under Art. 44 (`family-b`, `sponsor_status = b`).

**User:** "I have had a Swiss B permit since March 2022 and work in Zurich.
My son is 13 and still lives with my mother in Pristina. Can I bring him to
live with me now?"

**The trap.** The popular answer is a plain yes with the usual conditions
(housing, income). It misses the deadline: for a child over twelve the claim
must be made within twelve months of the permit grant, which for a permit of
March 2022 ended in March 2023.

**Expected**

- The assistant resolves `family-deadlines` and `family-b` with
  `sponsor_status = b`.
- The answer states the twelve-month deadline for children over twelve,
  that it ran from the grant of the permit, and that a reunification claimed
  now is late and is approved only for important family reasons; it says the
  release does not assess those reasons.
- It states the Art. 44 conditions as conditions, not as a promise of
  approval (Art. 44 permits rather than guarantees).
- It cites the Fedlex AIG page. It does not answer with a plain yes.

| ID | Variation | Expected |
| --- | --- | --- |
| 3a | The child is 9 | The five-year deadline applies and has not run out; the Art. 44 conditions are stated |
| 3b | The child is 15 | As the base case, plus: the child is heard where necessary |
| 3c | The sponsor is Swiss (Art. 42(1)) | The deadline starts with the Swiss family member's entry or the creation of the relationship; the entitlement of Art. 42(1) replaces the Art. 44 conditions |
| 3d | The sponsor holds a C permit | Art. 43 entitlement and conditions (`sponsor_status = c`) instead of Art. 44; the same deadlines |
| 3e | Sponsor's permit status not stated | `NEEDS_CONTEXT` for `sponsor_status`; the assistant asks which permit the sponsor holds; the deadline facts, which need no context, can already be given |
| 3f | The user asks how to prove important family reasons | Not published; the assistant says so instead of inventing examples |

## UAT-4: permit after a marriage ends before three years

**Preconditions.** The release serves Art. 50 (`family-separation`:
continued permission after dissolution rests on a union of at least three
years with integration, or on important personal reasons, and the two must
not be collapsed into one three-year rule) and the entitlement of a spouse
of a Swiss citizen under Art. 42(1) (`family-swiss`, `sponsor_status =
swiss`).

**User:** "I am a Brazilian citizen, married to a Swiss woman for two years,
and living in Zurich on a B permit. We are separating. Will I lose my permit
because we were not married for three years?"

**The trap.** The popular answer treats three years of marriage as the one
condition and predicts loss of the permit. The law has a second, independent
route: important personal reasons requiring continued residence.

**Expected**

- The assistant resolves `family-separation` (no context) and `family-swiss`
  with `sponsor_status = swiss`.
- The answer names both alternatives, says the second does not depend on the
  length of the marriage, and does not predict loss of the permit as certain.
- It says the release does not assess individual reasons or domestic-violence
  evidence and that the cantonal authority decides.
- It cites the Fedlex AIG page.

| ID | Variation | Expected |
| --- | --- | --- |
| 4a | Married four years, integration criteria met | The first alternative applies; integration criteria as published (`integration-criteria`) |
| 4b | Married four years, no language skills | The first alternative needs integration too; the release states the criteria and the personal-circumstances clause, and decides nothing |
| 4c | The spouse holds a C permit instead of Swiss citizenship | Art. 50 covers the Art. 43 route as well; `family-c` replaces `family-swiss` |
| 4d | The spouse holds a B permit | Art. 50 covers the Art. 44 route; `family-b` replaces `family-swiss` |
| 4e | The user asks whether domestic violence counts as an important reason | The release does not assess it and says so; the alternative exists in the served statement |
| 4f | The same question in German ("Wir trennen uns nach zwei Jahren Ehe. Verliere ich meine Aufenthaltsbewilligung?") | Default lexical search, untranslated, ranks `family-separation` first through the authored everyday aliases (`Trennung`, `Scheidung`), which the source terms alone (`Auflösung der Ehe`) do not do, because the question uses neither word. Pinned in the round-trip check; optional hybrid rankings are recorded separately |

## UAT-5: settlement permit after years on a short-stay permit

**Preconditions.** The release serves Art. 34 (`permit-c`: unlimited and
unconditional permit; ten years on L or B permits with the last five years
continuously on B, integration and no revocation grounds; paragraphs 3 and 4
offer shorter routes so ten years is not universal; temporary stays do not
count toward the continuous five years, education stays count under a
condition) and, since 22 September 2026, the five-year routes by nationality
(`permit-c-five-years`: SEM's list of the states whose nationals reach the
settlement permit after five years, and that the free movement agreement
itself carries no settlement provisions).

**User:** "I am an Indian citizen. I have lived in Switzerland for ten years:
three years on an L permit and then seven years on a B permit. Can I apply
for a C permit now?"

**The trap.** The popular answer counts ten years of presence and says yes,
or carries the five-year rule of the settlement-agreement states over to a
nationality the served list does not name. The law asks for the last five
years continuously on a residence permit, excludes temporary stays from that
period, and makes the ten years a baseline rather than a universal rule.

**Expected**

- The assistant resolves `permit-c` and `permit-c-five-years`.
- The answer states the Art. 34(2) conditions: ten years on L or B permits,
  the last five continuous on B, integration, no revocation grounds; and that
  temporary stays do not count toward the continuous five years.
- It says why the five-year route does not help this user: it rests on
  settlement agreements, and the served list of those states does not name
  India.
- Applied to the user: seven continuous years on B satisfy the five-year
  condition and the ten-year total is met; integration and revocation
  grounds remain to be assessed by the authority.
- It cites the Fedlex AIG page and the SEM page.

| ID | Variation | Expected |
| --- | --- | --- |
| 5a | Five years on L, five on B | Ten years met, five continuous years on B met on the day; same caveats |
| 5b | Eight years on B with a one-year gap abroad in the last five | The continuous five-year condition is the issue; the release states the condition and does not decide the gap |
| 5c | Four years of studies, then six years on B | Education stays count only when followed by two uninterrupted years with a residence permit for a durable stay; the assistant states the condition rather than adding the years |
| 5d | EU/EFTA citizen asks the same | Covered since 22 September 2026: if the state is on the served list the five-year route applies (UAT-65), and for the EU states the list does not name, the ten-year rule stands |
| 5e | The user asks whether a C permit can be taken away | Not published (revocation grounds are referenced, not served); the assistant says so |

## UAT-6: social assistance and the permit

**Preconditions.** The release serves the SEM FAQ statement
(`social-assistance-review`: receipt of social assistance can have
immigration consequences but does not cause them automatically; the cantonal
migration authority decides individually and proportionately), and the
permit renewal facts (`permit-b`).

**User:** "I have a B permit and just lost my job in Zurich. I may have to
apply for social assistance for a few months. Will my permit be revoked?"

**The trap.** The popular answer says social assistance leads to revocation
or non-renewal. The published position is that consequences are possible,
not automatic, and decided case by case and proportionately.

**Expected**

- The assistant resolves `social-assistance-review` (and may add
  `permit-b`).
- The answer says revocation is not automatic, that the cantonal authority
  decides individually and proportionately, and that the release does not
  decide the user's case.
- It cites the SEM FAQ page. It does not claim automatic revocation and does
  not invent thresholds or durations.

| ID | Variation | Expected |
| --- | --- | --- |
| 6a | C permit holder | The same SEM statement applies; the release publishes no C-specific revocation rule and says so |
| 6b | EU/EFTA citizen | The same statement; no EU/EFTA-specific rule is served |
| 6c | The user asks for the amount or duration that triggers consequences | Not published; the assistant says so instead of inventing a threshold |
| 6d | The user asks whether unemployment benefit counts as social assistance | Not published; declined by name |
| 6e | The same question in German ("Ich habe eine B-Bewilligung und habe meine Stelle verloren. Wenn ich Sozialhilfe beziehen muss, wird meine Bewilligung widerrufen?") | Default lexical search, untranslated, ranks `social-assistance-review` first through the authored aliases (`Sozialhilfe beziehen`, `Stelle verloren`); the shared source term `Sozialhilfe` alone places the retirement and permit concepts ahead of it. Pinned in the round-trip check; optional hybrid rankings are recorded separately |

## UAT-7: Swiss citizen asking in Zurich German about a residence permit for a foreign spouse

**Preconditions.** The release serves the entitlement of a Swiss citizen's
foreign spouse under AIG Art. 42(1) (`family-swiss`, `sponsor_status =
swiss`: entitled to a residence permit and its renewal if they live
together), the reunification deadlines of Art. 47 (`family-deadlines`: five
years; for Swiss family members the deadline starts with entry or the
creation of the family relationship; late reunification only for important
family reasons) and the issuing authority (`permit-authority`). The Zurich
family-documents concept (`zh-eu-family-documents`) is published for EU/EFTA
nationals only. The German `Familiennachzug` stems to `famili`, which does
not meet the English `family`, so a German search finds no family concept
through the English label alone. Every concept carries source terms copied
from its excerpts (`family-swiss`: `Familienangehörige von Schweizerinnen
und Schweizern`, `Ehegatten`, `zusammenwohnen`; `family-deadlines`: `Frist
für den Familiennachzug`, `fünf Jahren`, `Kinder über zwölf Jahre`), and
lexical `search` weighs a token by its rarity, so the Standard German form
of this question ranks `family-swiss` first. `family-swiss` also carries the
everyday words (`geheiratet`, `mit Schweizerin verheiratet`) and the three
Zurich German spellings of this question (`Schwiizer`, `Schwiizerin`,
`ghüratet`) as authored aliases, so default lexical search ranks
`family-swiss` first for the dialect question as typed as well;
`Ufenthaltsbewilligung` still matches no indexed term. Those aliases do not
establish coverage of other dialect spellings. Optional hybrid search can
rank a dialect query through embeddings, with its actual mode and results
recorded separately.

**User:** "Ich han de Schwiizer Pass und han en Brasilianer ghüratet. Er
wohnt no in São Paulo und sött jetzt zu mir nach Züri zügle. Was bruuchts,
dass er en Ufenthaltsbewilligung überchunnt, und bis wänn müend mir de
Familienachzug aamälde?" ("I hold a Swiss passport and married a Brazilian.
He still lives in São Paulo and should now move to me in Zurich. What does
he need to get a residence permit, and by when do we have to apply for
family reunification?")

**The trap.** A generic answer applies the conditions of Art. 44 (suitable
housing, no social assistance, language) to a Swiss sponsor, or quotes
documents, fees and processing times from memory. Under Art. 42(1) the
spouse is entitled to the permit if the couple live together; the five-year
deadline runs from the marriage or the entry.

**What this case demonstrates.** A Swiss citizen writes in dialect as a
matter of course. The case shows what a dialect question does to the caller
and to the server: whether the caller sends it as typed, normalises it to
Standard German or translates it into English, and what the server finds in
each form. Without a German term on the family concepts the German forms
find nothing useful, which is what the source terms and the authored aliases
are for.

**Expected**

- The assistant resolves `family-swiss` with `sponsor_status = swiss` and
  `family-deadlines` (no context), with `permit-authority` as it sees fit.
- The answer, in German (dialect or Standard German), states the entitlement
  under Art. 42(1) conditioned on living together, does not apply the
  Art. 44 conditions, states the five-year deadline and its start (marriage
  or entry), and names the cantonal migration office as the authority.
- It says the release lists no documents for the spouse of a Swiss citizen
  (the Zurich list is for EU/EFTA nationals) and states no fees or
  processing times.
- It cites the Fedlex AIG page.
- The record lists every search query with its language.
- At most 4 tool calls and 30 KB.

| ID | Variation | Expected |
| --- | --- | --- |
| 7a | The Swiss citizen's child is over twelve | The twelve-month deadline of `family-deadlines` instead of five years; the entitlement of Art. 42(1) covers unmarried children under 18 |
| 7b | The couple married more than five years ago and the spouse never moved | The deadline has run out; late reunification only for important family reasons; the release does not assess them |
| 7c | The sponsor holds a C permit, not Swiss citizenship | `family-c` (Art. 43, `sponsor_status = c`) replaces `family-swiss`; the same deadlines |
| 7d | The user asks which documents to bring or how long the office takes | Not published for a third-country spouse of a Swiss citizen; declined by name (documents beyond the covered pages, fees and processing times are out of scope) |
| 7e | The same question in Standard German | The same answer expectation; default lexical search ranks `family-swiss` first for the Standard German question, before the Zurich registration concepts the question also touches; pinned in the round-trip check together with the dialect form. Optional hybrid rankings are recorded separately |

## Extension cases: moving to Switzerland and naturalisation

UAT-8 to UAT-17 cover the topics a newly arrived resident meets after
registration (social insurance on arrival and departure, tax at source, the
foreign driving licence, health insurance and premium reduction) and
naturalisation, at the same three levels as the residence topic. The current
release serves them with assistant-authored facts that one person confirmed
in bulk groups and then read card by card; the sources are catalogued in
`releases/mvp-zurich/sources.json` (scan sets `moving` and
`naturalisation`), listed page by page in `sources.md` and saved in the
pack's run. The concept IDs below are the concept IDs of the curation file
and of the acceptance suite. The expectations that no saved page states are
listed in [LIMITATIONS.md](../../LIMITATIONS.md) as gaps of this extension;
the paragraphs below state what the pages state. Each case names the pages
its expected answer was checked against, so the reviewer can see whether the
saved page still states it. Budgets and criteria A1 to A6 are those of the
single-turn cases; A7 applies to every case of this section, A8 to UAT-11
and UAT-17.

### UAT-8: refund of AHV contributions on leaving Switzerland

**Preconditions.** The release serves the ZAS refund rules
(`ahv-contribution-refund`: a refund is published for nationals of states
without a social security agreement and for nationals of the states named
on the page whose agreement provides for it; Swiss and EU/EFTA nationals
and nationals of agreement states whose agreement does not provide for it
are excluded; at least one full year of contributions; the person, their
spouse and children under 25 must have left Switzerland for good or intend
to; pensions already received are deducted), conditioned on the nationality
group (planned context field `agreement_status` with `eu_efta`,
`agreement` and `none`), and the ZAS statement on AHV pensions paid abroad
(`ahv-pension-abroad`) as published. Checked against the ZAS refund page
and its agreement-state page.

**User:** "I'm a German citizen and after six years of working in Zurich I
am moving back to Berlin for good. Can I get my AHV contributions paid
back?"

**The trap.** The popular answer says yes and describes the refund form, or
confuses the AHV with the pension fund. The refund exists only for
nationals of states without a social security agreement and of the named
states whose agreement provides for it; EU/EFTA nationals are excluded by
name.

**Expected**

- The assistant derives `agreement_status = eu_efta` from "German citizen"
  and resolves `ahv-contribution-refund` (and `ahv-pension-abroad` as it
  sees fit).
- The answer says no refund is published for EU/EFTA nationals and names
  the groups for which one is; it states the general conditions (one full
  year of contributions, definitive departure of the family) as conditions
  of the refund, not as applying to the user; it says the release computes
  no pension and no amount.
- It cites the ZAS page. It does not describe the refund procedure as open
  to the user and does not mix in the pension fund (UAT-9).
- At most 4 tool calls and 30 KB.

| ID | Variation | Expected |
| --- | --- | --- |
| 8a | Indian citizen | India is among the states named on the ZAS page whose agreement provides for a refund: `agreement_status = agreement` is `SUPPORTED` with the conditions; the release does not compute the amount |
| 8b | Brazilian citizen | The served statement gives nationals of Brazil the choice between a pension and a refund; both are stated as published, neither is recommended |
| 8c | Nationality not stated | `NEEDS_CONTEXT` for `agreement_status`; the assistant asks for the nationality |
| 8d | Contributions for eight months only | The one-full-year condition is stated; the release does not decide the case |
| 8e | The user asks what happens to the contributions instead | Only what `ahv-pension-abroad` states; nothing else is invented |
| 8f | The user asks about the pension fund in the same breath | UAT-9 applies; both concepts are resolved in one call |

### UAT-9: pension fund cash-out when moving to an EU state

**Preconditions.** The release serves the BSV FAQ statement
(`bvg-cash-out-departure`: cash payment of the BVG retirement assets on
proof of definitive departure; since 1 June 2007 not for the mandatory part
when moving to an EU state, Iceland or Norway if the person remains insured
there against old age, death and disability; the extra-mandatory part
remains payable; the spouse's written consent; departure to Liechtenstein
excluded; and FZG Article 4: an insured person who joins no new pension fund
names a permitted form of keeping the pension cover, otherwise the vested
benefit goes to the substitute occupational benefit institution),
conditioned on the destination (planned context
field `destination` with `eu_efta` and `other`). Checked against the BSV
FAQ answer on BVG cash payment on leaving Switzerland.

**User:** "I'm moving from Zurich to Munich for good next month and start a
job there. Can I have my whole pension fund paid out in cash?"

**The trap.** The popular answer says yes: leaving Switzerland permanently
allows a cash payment. Since 2007 the mandatory part stays in Switzerland
while the person is compulsorily insured in the EU/EFTA state; only the
extra-mandatory part can be paid out.

**Expected**

- The assistant derives `destination = eu_efta` and resolves
  `bvg-cash-out-departure`.
- The answer says the whole amount is not paid out: the mandatory part is
  blocked while the user is insured in Germany against old age, death and
  disability, a condition the release states and does not decide, so the
  answer does not assert that the user is insured there; the extra-mandatory
  part can be paid out; what is not paid out is kept in a permitted form
  named by the insured person, otherwise it goes to the substitute
  occupational benefit institution (FZG Article 4); a married user needs the
  spouse's written consent.
- It cites the BSV FAQ page. It states no tax consequence and no amount.
- At most 4 tool calls and 30 KB.

| ID | Variation | Expected |
| --- | --- | --- |
| 9a | Moving to Brazil | `destination = other`: cash payment on proof of definitive departure; the EU/EFTA restriction is not stated as applying |
| 9b | Moving to Munich without taking up work or insurance there | The condition "remains insured there" is stated; the release does not decide whether it is met |
| 9c | Moving to Liechtenstein | The served statement excludes cash payment on departure to Liechtenstein |
| 9d | The user asks whether the pension fund or a bank is the right counterpart | The served facts state only FZG Article 4 (a permitted form named by the insured person, otherwise the substitute occupational benefit institution); no account, policy or institution is named or recommended |
| 9e | The user asks how the payout is taxed | Not published; declined by name |

### UAT-10: tax at source above CHF 120,000

**Preconditions.** The release serves the Zurich tax-at-source facts
(`zh-tax-at-source-liability`: liable are employees of a Swiss employer
without the C permit or Swiss citizenship, unless married to or in a
registered partnership with a person who has either; the liability ends
with the C permit, citizenship or such a marriage, after which the ordinary
assessment applies and the tax at source already paid in that year is
credited) and the subsequent ordinary assessment
(`zh-tax-at-source-ordinary-assessment`: mandatory for the whole income and
assets when the gross income of a person taxed at source reaches
CHF 120,000 in a tax year; for double-earner couples when one spouse's
gross income reaches it; mandatory on request when other income exceeds
CHF 3,000 or assets exceed CHF 80,000, CHF 160,000 for jointly taxed
persons; otherwise on request by 31 March of the following year, a deadline
that is not extended, after which it continues ex officio until the
liability ends), with the federal counterparts
(`tax-at-source-liability` from the ESTV page; the threshold of Art. 9
QStV). Checked against the Zurich tax-at-source pages and ZStB 87.3.

**User:** "I'm a Spanish citizen with a B permit working in Zurich, gross
salary CHF 135,000. Tax is deducted at source. Do I have to file a tax
return?"

**The trap.** The popular answer says tax at source settles everything for
a B permit holder, or that filing is optional. From CHF 120,000 of gross
income the subsequent ordinary assessment is mandatory, with a tax return
for the whole income and assets; below it, a request by 31 March binds for
the following years.

**Expected**

- The assistant resolves `zh-tax-at-source-ordinary-assessment` and
  `zh-tax-at-source-liability` for `CH-ZH` (and the federal concepts as it
  sees fit).
- The answer says yes: at CHF 135,000 the assessment is mandatory, the tax
  at source stays deducted and is credited, and the return covers the whole
  income and assets; it adds the double-earner rule only if the user is
  married; it does not present the assessment as a choice.
- It cites the Zurich pages (and the ordinance where quoted). It states no
  tariff, rate or amount.
- At most 4 tool calls and 30 KB.

| ID | Variation | Expected |
| --- | --- | --- |
| 10a | Gross salary CHF 95,000, wants to deduct pillar 3a contributions | The voluntary request by 31 March of the following year; once requested, the assessment continues in the following years; no deadline extension |
| 10b | Married, the spouse earns CHF 125,000 | The double-earner rule: the assessment is mandatory when one spouse's gross income reaches the threshold |
| 10c | Other income of CHF 5,000 from abroad | A request is mandatory above CHF 3,000 of other income (or CHF 80,000 of assets) |
| 10d | The user asks the tax rate or the tariff code | Tariff tables are out of scope by name; the assistant says so |
| 10e | The user lives in Germany and commutes to Zurich | The served Zurich facts are for residents; the Zurich page states the liability of persons resident abroad, but the release does not serve it (`not_served`); declined by name |
| 10f | The same question for an employee in Bern | Federal facts `SUPPORTED`; the Zurich concepts `OUT_OF_COVERAGE` with `jurisdiction_not_covered` |

### UAT-11: tax at source after marrying a Swiss citizen, in German

**Preconditions.** As UAT-10 (`zh-tax-at-source-liability`,
`tax-at-source-liability`), with German source terms copied from the Zurich
excerpts (`quellensteuerpflichtig`, `Niederlassungsbewilligung C`,
`ordentliche Veranlagung`) and everyday aliases (`heiraten`, `Schweizer
heiraten`, `Quellensteuer`).

**User:** "Ich habe eine B-Bewilligung, arbeite in Zürich und heirate
nächsten Monat einen Schweizer. Werde ich weiterhin an der Quelle
besteuert?" ("I have a B permit, work in Zurich and marry a Swiss citizen
next month. Will I still be taxed at source?")

**The trap.** The popular answer ties tax at source to the B permit and
says it continues until the C permit. Marriage to a person with Swiss
citizenship or the C permit ends the liability: the couple is assessed in
the ordinary procedure with a tax return, and the tax at source already
deducted that year is credited.

**Expected**

- The first `search` carries the German question or its key terms; the
  assistant resolves `zh-tax-at-source-liability` for `CH-ZH`.
- The answer, in German, says the tax at source ends with the marriage,
  that the couple files a tax return in the ordinary assessment, and that
  the tax at source already paid in the year is credited in the final bill;
  it states no month from which the change applies unless a served fact
  gives one.
- It cites the Zurich page. At most 4 tool calls and 30 KB.

| ID | Variation | Expected |
| --- | --- | --- |
| 11a | The spouse holds a B permit | The liability continues; the ordinary assessment follows the rules of UAT-10 |
| 11b | The user receives the C permit instead | The same end of the liability, on the grant of the permit |
| 11c | The user asks whether the couple pays more or less | Not published; declined by name |
| 11d | The same question in English | The same facts; the English aliases rank the concept |

### UAT-12: driving on a foreign licence after twelve months

**Preconditions.** The release serves the Zurich foreign-licence facts
(`zh-foreign-licence-exchange`: a Swiss licence is needed to drive; twelve
months from the date of entry to exchange the foreign licence; after twelve
months driving in Switzerland is not permitted until the licence is
exchanged; the states whose licences are exchanged without a control drive,
in two lists (EU/EFTA and the named other states, with Taiwan limited to
categories A1 and B); for the second list an additional theory test only to
keep categories C, D, C1 and D1, while the first list needs neither a control
drive nor a theory test; every other state's licence requires a control
drive; the
documents: eye test not older than two years, photo, identity document,
original licence, a translation when the licence is not in Latin script;
the offices), conditioned on the licence's state (planned context field
`licence_state` with `eu_efta`, `listed` and `other`), and the federal rule
(`foreign-licence-exchange`: the twelve months of Art. 42 VZV and the ch.ch
statement that an exchange is still possible after the twelve months but a
fine may be charged, without an amount). Checked against the Zurich foreign-licence pages.

**User:** "I moved from California to Zurich 14 months ago and still drive
on my US licence. Am I still allowed to, and can I still exchange it?"

**The trap.** The popular answer treats a US licence as valid indefinitely
with an international permit, or says one year and then a simple swap at
any time. The served rule: twelve months from entry; after that no driving
in Switzerland until the exchange; the US is on the list without a control
drive for category B.

**Expected**

- The assistant derives `licence_state = listed` and resolves
  `zh-foreign-licence-exchange` for `CH-ZH` (and
  `foreign-licence-exchange`).
- The answer says the user is not permitted to drive until the licence is
  exchanged, that the exchange for a US licence needs no control drive (and
  no theory test for category B), and lists the documents and where to
  apply. It says, as the ch.ch fact states, that an exchange is still
  possible after the twelve months but a fine may be charged, and names no
  amount because none is served.
- It cites the Zurich page. At most 4 tool calls and 30 KB.

| ID | Variation | Expected |
| --- | --- | --- |
| 12a | German licence, ten months in Switzerland | `eu_efta`: exchange without control drive or theory test within the twelve months |
| 12b | Category C licence from Canada for professional driving | For the second list, the additional theory test for categories C, D, C1 and D1 and for professional passenger transport is stated; an Austrian licence (first list) needs neither a control drive nor a theory test |
| 12c | Licence not in Latin script | The translation requirement is stated as published |
| 12d | A tourist without residence | Not covered: the served facts are for persons who took up residence; declined by name |
| 12e | The user asks the fee | Only a served statement is given; otherwise declined by name |
| 12f | The user lives in Winterthur | The cantonal concept serves every municipality of the canton; the offices are those published |

### UAT-13: control drive for a licence from a state not on the lists

**Preconditions.** As UAT-12, plus the control-drive facts
(`zh-control-drive`: only one attempt; on passing the Swiss licence is
issued; on failing the person may no longer drive in Switzerland and the
full route applies: theory test, learner's licence, traffic awareness
course, driving test; the preparation page). Checked against the Zurich
control-drive pages.

**User:** "I'm from India, arrived in Zurich two months ago and have an
Indian licence. Can I simply swap it for a Swiss one?"

**The trap.** The popular answer says yes, a simple exchange, or the
opposite: that the full Swiss driving test is required. India is on neither
list, so the exchange needs a control drive with a single attempt, and only
a failed control drive leads to the full examination route.

**Expected**

- `licence_state = other`; the assistant resolves
  `zh-foreign-licence-exchange` and `zh-control-drive`.
- The answer says the exchange is possible within twelve months of entry
  and requires a control drive; that it can be taken once; what follows a
  pass and a fail; the documents; that the release does not assess driving
  skills.
- It cites the Zurich pages. At most 4 tool calls and 30 KB.

| ID | Variation | Expected |
| --- | --- | --- |
| 13a | Licence from Japan | On the second list: no control drive for category B |
| 13b | The user asks what the control drive covers | The served preparation facts; nothing beyond them |
| 13c | The user asks to postpone the exchange until next year | After twelve months from entry driving is not permitted until the exchange (UAT-12) |
| 13d | The user asks whether a second attempt is possible after a failed control drive | The served statement: only one attempt; then the full route |

### UAT-14: health insurance in the first three months

**Preconditions.** The release serves the FOPH insurance-duty facts
(`health-insurance-deadline`: everyone taking up residence must take out
insurance within three months; on timely joining cover starts from the date
of residence and the premiums are owed from that date; on late joining
cover starts from the joining date and an inexcusable delay costs a premium
surcharge; the canton assigns an insurer to those who do not insure
themselves; the exemption groups) and the Zurich exemption facts
(`zh-health-insurance-exemption`: the SVA Zurich decides exemption requests
since 1 October 2023; the groups; the proof of foreign cover at least
equivalent to the KVG; employees with a European health insurance card are
not exempted). Checked against the FOPH page, the Canton of Zurich
premium-reduction page (which states the SVA Zurich's competence since
1 October 2023) and the SVA Zurich exemption page.

**User:** "I arrived in Zurich from Canada two months ago on a B permit and
haven't taken out health insurance yet. Is it too late, and from when will I
pay?"

**The trap.** The popular answer says cover and premiums start when the
policy is signed, or that the first year is optional. The duty runs from
the date of residence: within three months, cover and premiums are
retroactive to that date; later, cover starts only at joining and a
surcharge is due.

**Expected**

- The assistant resolves `health-insurance-deadline` (federal) and
  `zh-health-insurance-exemption` for `CH-ZH` as it sees fit.
- The answer says it is not too late (two of three months), that cover and
  premiums run from the date of residence when the user joins within the
  three months, what happens after the deadline, and that the exemption
  groups do not include an employed resident from a non-EU/EFTA state
  unless a served fact says so.
- It cites the FOPH page. It recommends no insurer and states no premium.
- At most 4 tool calls and 30 KB.

| ID | Variation | Expected |
| --- | --- | --- |
| 14a | Posted by a German employer for 18 months, keeps German insurance | An exemption is possible for posted workers on proof of equivalent cover; the SVA Zurich decides; the release does not decide |
| 14b | EU student, not employed | The student group is served; the same proof |
| 14c | EU employee with a European health insurance card | Not exempted, as published |
| 14d | Arrived five months ago | Late joining: cover from the joining date; the surcharge for inexcusable delay; the canton's assignment; the release does not judge the excuse |
| 14e | The user asks for the cheapest insurer | Not covered; declined by name |

### UAT-15: premium reduction after arriving from abroad

**Preconditions.** The release serves the federal frame
(`premium-reduction`: the canton of residence decides who is entitled and
by how much; some cantons reduce premiums without an application, others
on application; minimum reductions for children and young adults in
training; the application goes to the cantonal office) and the Zurich facts
(`zh-premium-reduction`: the SVA Zurich runs the reduction, which is paid
only on application; after arrival from abroad the entitlement can start
from the month after arrival and the registration is possible at once;
after arrival from another canton the application is possible from
1 January of the following year; residence in the canton on 1 January of
the year of payment; the calculator is a tool, not a served amount),
conditioned on the origin (planned context field `arrival_from` with
`abroad` and `other_canton`). Checked against the FOPH premium-reduction
page, the Zurich Health Directorate page and the SVA Zurich entitlement
page.

**User:** "I moved from Italy to Zurich in May on a modest salary. Can I
get help with my health insurance premiums, and from when?"

**The trap.** The popular answer gives one national rule, says the
reduction is automatic, or says to apply next year. The reduction is
cantonal; in Zurich it is paid only on application, and after arrival from
abroad it can start from the month after arrival.

**Expected**

- `arrival_from = abroad`; the assistant resolves `zh-premium-reduction`
  for `CH-ZH` and `premium-reduction`.
- The answer says the reduction is cantonal and in Zurich paid only on
  application to the SVA Zurich, that after arrival from abroad the
  entitlement can start from the month after arrival and the user should
  register at once, and that the release states no income limit or amount
  (the SVA calculator is named, not computed).
- It cites the Zurich and FOPH pages. At most 4 tool calls and 30 KB.

| ID | Variation | Expected |
| --- | --- | --- |
| 15a | Moved from Bern to Zurich | `other_canton`: the application is possible from 1 January of the following year |
| 15b | The user asks how much | Not published; the calculator is named |
| 15c | The user has two children | The federal minimum reductions for children and young adults in training are stated as the canton's duty, not as an amount |
| 15d | The user lives in Wallisellen | The cantonal concept serves every municipality of the canton |

### UAT-16: ordinary naturalisation on a B permit after eleven years

**Preconditions.** The release serves the federal conditions
(`naturalisation-ordinary`: the C permit; ten years of residence in
Switzerland, three of them in the last five years before the application;
the years between the ages of 8 and 18 count double, with at least six
years of actual residence; language B1 oral and A2 written; the cantons set
an additional minimum residence of two to five years in the canton and the
municipality; the application form from and to the authority of the place
of residence), the Zurich conditions (`zh-naturalisation-ordinary`: a valid
C permit; ten years in Switzerland; at least two years in the same
municipality before the application, or two years in the canton for
applicants under 25; German A2 written and B1 oral or the cantonal German
test; basic knowledge of Switzerland, the canton and the municipality; no
unpaid debt-enforcement entries in the last five years; no relevant
criminal record or pending proceedings; the application to the cantonal
Gemeindeamt, Naturalisation Division) and the City of Zurich conditions
(`city-zurich-naturalisation`: two years in the city; the years with a C or
B permit count fully, with an F permit half, with an N or L permit not at
all; the procedure of about two years and the fee as published). Checked
against the SEM pages, the Zurich cantonal pages and the City of Zurich
page.

**User:** "I'm a Turkish citizen and have lived in Switzerland for eleven
years, the last eighteen months in the city of Zurich after nine and a half
years in Bern. I hold a B permit. Can I apply for Swiss citizenship now?"

**The trap.** The popular answer counts the eleven years and says yes,
perhaps adding a twelve-year rule from before 2018. Two served conditions
are not met: the C permit, and two years in the municipality (the canton
counts residence in the same municipality, the city its own).

**Expected**

- The assistant resolves `naturalisation-ordinary`,
  `zh-naturalisation-ordinary` and `city-zurich-naturalisation` for
  `CH-ZH-261`.
- The answer says not yet: the C permit is required and the user holds a B
  permit; two years in the same municipality are required and eighteen
  months have passed; the ten years and the three of the last five are met.
  It states the language, knowledge, debt and criminal-record conditions as
  conditions, names the cantonal Gemeindeamt as the place to file, and says
  the release does not decide eligibility.
- It cites the SEM, Zurich and city pages. At most 4 tool calls and 30 KB.

| ID | Variation | Expected |
| --- | --- | --- |
| 16a | The same user is 23 | The canton's exception: two years in the canton suffice for applicants under 25; the city's two years are its own condition |
| 16b | Arrived at the age of 10, now 19 | The years between 8 and 18 count double; at least six actual years; the release does not compute the total |
| 16c | Holds the C permit, lives in Wallisellen for three years | Federal and cantonal conditions `SUPPORTED`; the city concept `OUT_OF_COVERAGE`; the municipality's own conditions are not published here (the Wallisellen pack has its entry point) |
| 16d | The user asks what the knowledge test asks | Only what the served page states; no questions are invented |
| 16e | The user asks the fee | The served amounts are the canton's (CHF 500, CHF 250 under 25, none under 20), the Confederation's (CHF 100, CHF 150 for a couple, CHF 50 under 18) and the city's (none under 25, CHF 500 over 25, read from the page's fee table) |
| 16f | EU citizen asks the same | The same conditions; the release publishes no nationality-based route |

### UAT-17: facilitated naturalisation of a Swiss citizen's spouse, in German

**Preconditions.** The release serves the SEM conditions
(`naturalisation-facilitated-spouse`: three years of marital community with
the Swiss spouse; five years of residence in Switzerland in total, the last
year immediately before the application; integration and language B1 oral
and A2 written; the application to the SEM; the served facts state no
permit requirement) and the Zurich and city facts
(`zh-naturalisation-facilitated`, `city-zurich-naturalisation-facilitated`:
the SEM decides; the application goes to the SEM by post; the duration and
fee as published), with German source terms (`erleichterte Einbürgerung`,
`ehelicher Gemeinschaft`, the inflected form the excerpts use) and aliases
(`Schweizer heiraten`, `mit Schweizer
verheiratet`, `einbürgern lassen`). Checked against the SEM spouse page and
FAQ, the Zurich cantonal page and the City of Zurich page.

**User:** "Ich bin Brasilianerin und seit vier Jahren mit einem Schweizer
verheiratet. Wir leben seit sechs Jahren zusammen in Zürich, ich habe eine
B-Bewilligung. Kann ich mich erleichtert einbürgern lassen, obwohl ich keine
C-Bewilligung habe?" ("I am Brazilian and have been married to a Swiss
citizen for four years. We have lived together in Zurich for six years; I
hold a B permit. Can I apply for facilitated naturalisation although I do
not have a C permit?")

**The trap.** The popular answer applies the C permit of the ordinary
procedure to the facilitated one, or stops at "three years of marriage".
The facilitated procedure has its own conditions: three years of marital
community, five years in Switzerland with the last year before the
application, integration and language; the C permit is a condition of the
ordinary procedure only.

**Expected**

- The first `search` carries the German question or its key terms; the
  assistant resolves `naturalisation-facilitated-spouse` and the Zurich
  facilitated concept for `CH-ZH-261`.
- The answer, in German, says the served conditions of the facilitated
  procedure are met on the user's figures (four years of marriage, six
  years in Switzerland including the last year), that the C permit is a
  condition of the ordinary procedure and not among the served conditions
  of the facilitated one, states language and integration as conditions,
  and names the SEM as the deciding authority. It says the release does not
  decide the case.
- It cites the SEM page. At most 4 tool calls and 30 KB.

| ID | Variation | Expected |
| --- | --- | --- |
| 17a | Married two years | The three-year condition is not met yet; nothing else changes |
| 17b | Lived in Switzerland three years, married five | The five-year residence condition is not met; the SEM page describes spouses living abroad, but the release does not serve that rule (`not_served`); declined by name |
| 17c | Registered partnership instead of marriage | Not published as a facilitated route; declined by name |
| 17d | The spouse became Swiss after the marriage | The served facts state the conditions; a distinction by the date of the spouse's citizenship is not published unless a served fact states it |
| 17e | The same question in English | The same answer expectation; the English aliases rank the concept |

## Office-contact cases

UAT-18 to UAT-23 check the contact facts of the Zurich offices (topic
`offices`): plain lookups of an address and of
opening or telephone hours, and questions whose correct answer is negative
because the office's own page says so. Criterion A9 applies to the negative
ones: a negative the cited page states is reported as the office's
statement ("the Migration Office states that it has no e-mail address"),
not as information the service lacks ("I found no e-mail address"), and a
location missing from the published list is named as missing. The facts
were written by the assistant from the saved pages and confirmed by one
reviewer; the location list of the Road Traffic Office
(`zh-road-traffic-office-locations-14`), added for UAT-20, awaits review.
Budgets and criteria A1 to A6 are those of the single-turn cases; A8
applies to UAT-22 and UAT-23.

### UAT-18: address and opening hours of the Migration Office

**Preconditions.** `zh-migrationsamt-contact` serves the address
(Berninastrasse 45, Postfach, 8090 Zürich), the counter-hall hours (Monday
to Friday 08.00 to 16.30) and the telephone (+41 43 259 88 00, Monday to
Friday 08.00 to 11.45 and 13.00 to 16.30), from the Migration Office's own
page.

**User:** "I need to go to the Migration Office of the Canton of Zurich in
person. What is the address and when is it open?"

**The trap.** Generic office hours, an invented address or directions, or
the City of Zurich Population Office instead of the cantonal office.

**Expected**

- The assistant resolves `zh-migrationsamt-contact` for `CH-ZH`.
- The answer gives the address, the counter-hall hours and the telephone
  hours, names no e-mail address and says the release publishes no
  directions. It cites the Migration Office page.

### UAT-19: e-mail address of the Migration Office

**Preconditions.** `zh-migrationsamt-contact-3` serves the office's
statement that it has no e-mail address and takes written requests through
an online contact form (excerpt: "Wir verfügen über keine
E-Mail-Adresse").

**User:** "What is the e-mail address of the Migration Office of the
Canton of Zurich?"

**The trap.** An invented address (`info@…`, `migrationsamt@zh.ch`), the
media address, or "I could not find an e-mail address".

**Expected**

- The answer says the office states that it has no e-mail address, points
  to the online contact form and names the telephone as the other channel.
  It contains no e-mail address (A9). It cites the Migration Office page.

| ID | Variation | Expected |
| --- | --- | --- |
| 19a | The same question in German ("Hat das Migrationsamt Zürich eine E-Mail-Adresse?") | The same answer in German; pinned in the regression pack as Q-DE-32 |
| 19b | The user adds that they want to send documents by e-mail | The same answer; lexical search reads the longer question weak, hybrid search strong; the release does not say how documents are submitted beyond the served facts |

### UAT-20: a road traffic office that does not exist

**Preconditions.** `zh-road-traffic-office-locations` serves the location
list of the Road Traffic Office's locations page (eight locations:
Zürich-Albisgütli, Winterthur, Bassersdorf, Bülach, Hinwil, Regensdorf, the
Administrative Measures division and the Navigation Inspectorate in
Oberrieden) and the address and hours of each counter location.

**User:** "Where is the road traffic office in Oerlikon and when is it open?
I need to go there about my driving licence."

**The trap.** An invented Oerlikon branch with an address and hours, or
"nothing is known about Oerlikon" instead of the published list.

**Expected**

- The assistant resolves `zh-road-traffic-office-locations` for
  `CH-ZH-261`.
- The answer says the office lists no location in Oerlikon (A9), names
  Zürich-Albisgütli (Uetlibergstrasse 301, 8036 Zürich) as the location in
  the city, with its counter hours and no appointment needed for counter
  business, and may list the other locations. It cites the locations page.

### UAT-21: walking into the Population Office on a Saturday

**Preconditions.** `city-zurich-population-office` serves the address in
the Stadthaus (Stadthausquai 17, 8001 Zürich), the opening hours (Monday to
Friday 08.00 to 16.30, closed on Saturday and Sunday) and the appointment
requirement since 4 May 2026, which always applies to renewing a foreign
national's identity card.

**User:** "I need to renew my B permit card at the Personenmeldeamt of the
City of Zurich. Can I walk in on Saturday morning without an appointment?"

**The trap.** A walk-in is fine, or Saturday hours are given.

**Expected**

- The assistant resolves `city-zurich-population-office` for `CH-ZH-261`.
- The answer says no on both counts (A9): the renewal needs a booked
  appointment and a personal visit since 4 May 2026, and the office is
  closed on Saturdays; it gives the address and the weekday hours and says
  the release has no appointment slots. It cites the appointment page.

### UAT-22: visiting the SVA Zurich, in German

**Preconditions.** `zh-sva-contact` serves the public customer service at
Röntgenstrasse 17, 8005 Zürich, open Monday to Friday 8 to 17 without
appointment, and the SVA's own directions from the main station;
`zh-sva-telephone-numbers` serves the premium-reduction line.

**User:** "Ich muss bei der SVA Zürich etwas wegen der Prämienverbilligung
klären. Brauche ich einen Termin, und wie komme ich vom Hauptbahnhof
dorthin?" ("I need to sort out something about premium reduction at the
SVA Zurich. Do I need an appointment, and how do I get there from the main
station?")

**The trap.** An appointment assumed to be required, an invented route, or
an answer in English.

**Expected**

- The first `search` carries the German question or its key terms; the
  assistant resolves `zh-sva-contact`.
- The answer, in German, says no appointment is needed (A9), gives the
  address and hours, the tram and bus route via Limmatplatz or the walk
  along Zollstrasse, and may give the premium-reduction number
  044 448 53 75. It cites the SVA page "Beratung vor Ort".

### UAT-23: reaching the tax-at-source department, in German

**Preconditions.** `zh-tax-office-contact` serves the tax-at-source
department of the Cantonal Tax Office (Bändliweg 21, Postfach, 8090 Zürich;
+41 43 259 37 00; Monday to Friday 08.00 to 11.45 and 13.30 to 17.00; the
tax-at-source contact form) and the office's general line.

**User:** "Ich werde an der Quelle besteuert und habe eine Frage zu meiner
Quellensteuer. Wie erreiche ich das kantonale Steueramt Zürich telefonisch,
und wann?" ("I am taxed at source and have a question about it. How do I
reach the Cantonal Tax Office of Zurich by telephone, and when?")

**The trap.** Only the general number, an invented e-mail address, or an
answer in English.

**Expected**

- The answer, in German, gives the tax-at-source number and hours and the
  contact form, and may name the general line. It cites the Zurich
  tax-at-source page.

## Daily-life cases

UAT-24 to UAT-34 check the daily-life topics (`newcomer`, `waste`,
`vehicles-parking`, `household-taxes`) and, in UAT-34, the Road Traffic
Office's opening hours of the office-contact topic: plain lookups a newcomer
asks in the first weeks, most with a trap a generic answer falls into. The
facts were written by the assistant from the saved pages and confirmed by
one reviewer. Budgets and criteria A1 to A6 are those of the single-turn
cases; A7 applies where a trap is named, A8 to UAT-29 and UAT-31, A9 to
UAT-27, UAT-31 and UAT-34. UAT-24, UAT-25 and UAT-34 are sample questions of
the demo image's welcome panel
([docker/demo-opencode/](../../docker/demo-opencode/README.md)).

### UAT-24: moving into the City of Zurich with a dog

**Preconditions.** `city-zurich-dog-registration` serves the city's
registration duty (within ten days of moving in, dogs over three months,
AMICUS) and the dog control's contact; `zh-dog-keeping` serves the canton's
duties (liability insurance of at least CHF 1 million, the annual dog tax to
the municipality, whose amount is not served) and the training duty of
1 June 2025 with its exemptions.

**User:** "I'm moving to the city of Zurich next month with my two-year-old
dog. What do I have to do for the dog?"

**The trap.** Registration only, or "no course is needed": the federal
course duty ended in 2016, but the Canton of Zurich's training duty applies
since 1 June 2025, also to people moving in with their dog.

**Expected**

- The assistant resolves both concepts for `CH-ZH-261`.
- The answer names the registration within ten days and AMICUS, the
  liability insurance, the dog tax without an amount, the theory course
  within two months (unless a dog was kept for six months in the last ten
  years) and the practical course of at least six lessons (unless the
  Veterinary Office confirms equivalent training). It cites the City of
  Zurich dog-control page and the cantonal dog page.

### UAT-25: rubbish bags and collection day

**Preconditions.** `city-zurich-household-waste` serves the blue Züri-Sack
and its sizes, the fee share per size, the shop price range of June 2025,
weekly emptying, the disposal calendar and the ERZ app.

**User:** "I just moved into a flat in the city of Zurich. Which rubbish
bags do I have to use, what do they cost, and when is the rubbish
collected?"

**The trap.** Any bag will do; the fee share quoted as the price; an
invented collection weekday.

**Expected**

- The answer names the blue Züri-Sack, gives the fee share (CHF 1.30 for
  35 litres) and says shops set the higher sale price (ten 35-litre bags
  CHF 15.45 to 19.95 in June 2025), says containers are emptied weekly and
  must be out before 7 a.m., and points to the personal disposal calendar
  or the ERZ app for the street's day instead of naming one. It cites the
  ERZ pages.

### UAT-26: getting rid of an old sofa without a car

**Preconditions.** `city-zurich-bulky-waste-pickup` serves the paid pickup
(telephone orders only, the size limits, CHF 86.50 per 15 minutes, no cash);
`city-zurich-recycling-centres` the centres' prices; `city-zurich-hazardous-waste`
the mobile recycling centre in the neighbourhood.

**User:** "How do I get rid of an old sofa in the city of Zurich? I don't
have a car."

**The trap.** Leaving the sofa on the street, a free bulky-waste day, or an
online booking.

**Expected**

- The answer describes the pickup ordered by telephone (ideally three
  working days ahead), the 2 m limit for sofas, the 7 a.m. deadline and the
  CHF 86.50 flat price without cash on site, and names the recycling centres
  and the mobile recycling centre as the alternatives. It cites the ERZ
  pickup page.

### UAT-27: Werdhölzli on a Saturday afternoon with cash

**Preconditions.** `city-zurich-recycling-centres` serves the hours and
payment of both centres: Werdhölzli Monday to Friday 13 to 19 and Saturday
7.30 to 14, cards and TWINT only; Looächer also takes cash; electrical
appliances are free.

**User:** "I want to drop off an old fridge at the Werdhölzli recycling
centre in Zurich on Saturday afternoon and pay in cash. Is that possible?"

**The trap.** The weekday afternoon hours applied to Saturday; cash
assumed; a fee invented for the fridge.

**Expected**

- The answer says no on both counts (A9): Werdhölzli closes at 14 on
  Saturday and takes no cash; the fridge is free; Looächer takes cash. It
  cites the recycling-centre page.

### UAT-28: blue-zone parking at lunchtime

**Preconditions.** `city-zurich-parking-permits` serves the blue-zone rules:
one hour between 8 and 11.30 and between 13.30 and 18; arrival between
11.30 and 13.30 allows parking until 14.30; the disc rules and fines.

**User:** "I park my car in a blue zone in the city of Zurich at 12:10 on a
Tuesday. Until when may I stay?"

**The trap.** One hour from arrival (13.10, or 13.30 with the disc rule);
the lunchtime rule is missed.

**Expected**

- The answer says until 14.30, and that the disc is set to the next mark and
  must be clearly visible (no electronic disc). It cites the parking-disc
  page.

### UAT-29: moving from Bern with a car, in German

**Preconditions.** `zh-vehicle-registration-move` serves the canton's
procedure (online form, original documents by post to the
Strassenverkehrsamt Bülach, the insurance certificate after a change of
canton, new plates within 5 to 10 working days, no driving licence needed);
`city-zurich-first-steps` the city checklist's 14 days.

**User:** "Ich ziehe mit meinem Auto von Bern in die Stadt Zürich. Was muss
ich beim Strassenverkehrsamt erledigen, und brauche ich neue
Nummernschilder?" ("I am moving with my car from Bern to the city of
Zurich. What do I have to do at the Road Traffic Office, and do I need new
number plates?")

**The trap.** Keeping the Bern plates, or sending the driving licence; the
insurance certificate for a change of canton is missed.

**Expected**

- The search is sent in German; the answer, in German, gives the canton's
  procedure and the city's 14 days as their pages state them (see
  LIMITATIONS.md on the two deadlines), and may add that a resident parking
  card for a car with plates of another canton is applied for in writing.
  It cites the cantonal vehicle page.

### UAT-30: kindergarten entry after the 31 July cut-off

**Preconditions.** `city-zurich-kindergarten` serves the cut-off (four
years old by 31 July), the registration letter and «Meine Kinder», the
district school authority for families moving in later, and the German
questionnaire.

**User:** "Our daughter was born on 10 August 2023 and we have just moved to
the city of Zurich. When does she start kindergarten, and how do we
register her?"

**The trap.** August 2027, because she is four when school starts.

**Expected**

- The answer applies the 31 July cut-off: she turns four on 10 August 2027
  and starts in the summer of 2028; it says the release serves the dates of
  2026/27 and 2027/28 only, and describes the registration. It cites the
  kindergarten and school-entry pages.

### UAT-31: lost access code for the online tax return, in German

**Preconditions.** `city-zurich-tax-return` serves that the city's tax
office cannot issue a new access code (the Cantonal Tax Office's technical
support does), the deadline of the 2025 return (31 March 2026) and the
extension and reminder rules.

**User:** "Ich wohne in der Stadt Zürich und habe den Zugangscode für die
Online-Steuererklärung verloren. Kann mir das Steueramt der Stadt einen
neuen ausstellen, und bis wann muss die Steuererklärung 2025 eingereicht
sein?" ("I live in the city of Zurich and lost the access code for the
online tax return. Can the city's tax office issue a new one, and by when
must the 2025 tax return be filed?")

**The trap.** Sending the user to the city's tax office; a deadline from
another canton or from memory.

**Expected**

- The answer, in German, says the city's tax office cannot issue the code
  (A9) and names the Cantonal Tax Office's support, gives 31 March 2026 and
  the extension rule. It cites the City of Zurich tax-return page.

### UAT-32: the Serafe invoice without a TV

**Preconditions.** `radio-tv-household-fee` serves the device-independent
household fee, CHF 335 a year for a private household and the three
exemptions.

**User:** "I don't own a TV or a radio. Do I still have to pay the Serafe
invoice, and how much is it?"

**The trap.** "No device, no fee", the rule before 2019.

**Expected**

- The answer says yes, CHF 335 a year (CHF 85.75 per quarter with quarterly
  invoices), and names the exemptions, none of which is having no device.
  It cites the SERAFE pages.

### UAT-33: medical emergency and the ambulance costs

**Preconditions.** `city-zurich-medical-emergency` serves the emergency
number 144, the dispatcher's questions and who pays the rescue costs.

**User:** "My flatmate collapsed in our flat in Zurich. What number do I
call, and who pays for the ambulance?"

**The trap.** A free ambulance, or basic insurance paying it all.

**Expected**

- The answer says to call 144 at once, what the dispatcher asks, that basic
  insurance pays part of the costs for an illness (all depending on the
  policy), the accident insurance for an accident, and that the invoice
  goes to the patient. It cites the Schutz & Rettung page.

### UAT-34: opening hours of the Road Traffic Office

**Preconditions.** `zh-road-traffic-office-locations` serves Zürich-Albisgütli
(Uetlibergstrasse 301, 8036 Zürich), its counter hours, that counter
business needs no appointment, and the telephone hours.

**User:** "When is the Road Traffic Office in Zurich open, and do I need an
appointment?"

**The trap.** Generic hours; an appointment required; an invented branch in
the city centre.

**Expected**

- The answer gives the address and counter hours (Monday and Tuesday 7.15
  to 17.00, Wednesday to Friday 7.15 to 16.00) and says no appointment is
  needed for counter business (A9). It cites the Road Traffic Office pages.

## Cross-jurisdiction cases

UAT-35 to UAT-44 are asked from a place the release does not publish: another
canton (UAT-35 to UAT-41) or a municipality of the Canton of Zurich other
than the city (UAT-42 to UAT-44). The release holds three levels, federal
facts (`CH`), Canton of Zurich facts (`CH-ZH`) and City of Zurich facts
(`CH-ZH-261`), and one entry per canton of SEM's directory of migration
offices. `resolve` serves a fact where its level contains the user's place:
federal facts in every canton, cantonal facts in every Zurich municipality,
never sideways to another canton or city. An answer is judged on both sides
of that rule (criterion A10):

- as much as the release serves for the user's place: the federal facts, in
  a Zurich municipality also the cantonal facts, and the user's own canton
  from SEM's directory where an office is asked for. A refusal of the whole
  question because "the service covers Zurich" fails;
- nothing else: the cantonal or municipal part the release does not publish
  for that place is named as not published, not filled from general
  knowledge and not from the Zurich facts. A Zurich office, address,
  telephone number, opening hours, deadline, fee, form or procedure given to
  a user elsewhere fails, and so does a resolve for `CH-ZH` or `CH-ZH-261`
  made for that user.

The server says so itself: a concept answered for a place whose own
cantonal or municipal level the topic publishes for another place only
carries the gap `more_specific_jurisdiction_not_published`, which names the
deepest level that applies and the places served more deeply (`CH-ZH`,
`CH-ZH-261`), and `guidance_for_caller` tells the caller to say that the
cantonal or municipal part is not published for the user's place and to
carry nothing over. A topic that serves every canton equally deeply (the
cantonal migration offices, UAT-41) carries no such gap.

The `accept` stage replays each case for the user's place: the concepts that
apply must be `SUPPORTED` with the claims of the expected answer and, where
the topic holds a Zurich level, with that gap; the Zurich concepts a caller
might request alongside must be `OUT_OF_COVERAGE` with
`jurisdiction_not_covered`, and `must_not_serve` names the Zurich facts no
step may return. The live run adds must-not patterns for the Zurich details
most likely to be carried over and the harness check that no resolve that
returned facts ran for another place. Budgets and criteria A1 to A6 are
those of the single-turn cases; A7 applies to UAT-40 and UAT-43, A8 to
UAT-37, UAT-40 and UAT-44. The search queries are planned key terms that
find the applicable concept among the first three hits in lexical and in
hybrid mode; they are sent without a `jurisdiction`, which `search` also
accepts, so a Zurich concept may rank above it.

A rule that holds in all of Switzerland or in the whole canton is served
elsewhere only if the release cites a source of that level for it. The
release publishes some such rules on a narrower page only: the end of tax at
source on marrying a Swiss citizen and the single attempt at a control drive
on Canton of Zurich pages; the emergency number 144, the blue-zone times,
the kindergarten cut-off date and the leash season on City of Zurich pages.
They are rejected for a user elsewhere like any other Zurich fact (UAT-37
pins this for the control drive, the regression cases XC-10 and OOS-38 for
the marriage rule and the kindergarten date); whether the release should
cite a federal or cantonal source for them is a curation question, listed in
[LIMITATIONS.md](../../LIMITATIONS.md).

### UAT-35: permit for an eight-month contract in Bern

**Preconditions.** `fza-employee-permit` serves FZA Annex I Article 6
(a contract of more than three months and less than one year: a permit for
the contract's duration); `eu-employment-registration-deadline` serves SEM's
14 days, the documents and the permit L for contracts up to 364 days;
`permit-authority` that the cantonal migration offices issue permits;
`cantonal-migration-contact` SEM's entry for Bern. `zh-eu-l` is the Canton of
Zurich's page on the permit L, with a working-time condition the federal
facts do not state.

**User:** "I'm a German citizen and have signed an eight-month employment
contract with a company in Bern, where I will also live. Which permit will
I get, and where do I apply for it?"

**The trap.** The Bern gap filled from the Canton of Zurich's page (more
than fifteen hours a week, the Zurich Migration Office's address and hours),
a resolve for `CH-ZH`, or a refusal of the whole question.

**Expected**

- The assistant resolves for `CH-BE` with `population: eu_efta`;
  `zh-eu-l`, if requested, is rejected with `jurisdiction_not_covered`.
- The answer names the short-stay permit L for the duration of the
  contract, the registration with the municipality of residence within 14
  days of arrival and before starting work with the identity document and
  the employer's confirmation, and that the cantonal migration office
  issues the permit; it may add Bern's entry from SEM's directory
  (Ostermundigenstrasse 99B, 3006 Bern). It says that no Bern procedure,
  form, fee or opening hours are published, computes no date, and cites the
  SEM free-movement FAQ.

### UAT-36: living in Aargau and working in Zurich

**Preconditions.** As UAT-35, with `aig-registration` (AIG Article 12: the
authority at the place of residence) and SEM's entry for Aargau. The
question names two places; registration and the permit follow the place of
residence, as the served federal facts state.

**User:** "I'm a French citizen. I have rented a flat in Baden in the Canton
of Aargau and start a permanent job in Zurich next month. Where do I have to
register, and which office issues my residence permit?"

**The trap.** Following the employer's address: the Zurich Migration Office
at Berninastrasse 45, the City of Zurich's Personenmeldeamt with its
appointment duty, or the Canton of Zurich's registration page; a deadline
computed without the arrival date.

**Expected**

- The assistant resolves for `CH-AG`; `zh-eu-registration`,
  `city-zurich-arrival` and `zh-migrationsamt-contact`, if requested, are
  rejected.
- The answer sends the user to the municipality of residence, Baden, within
  14 days of arrival and before starting work, names the residence permit B
  for an open-ended contract and Aargau's migration office from SEM's
  directory (Amt für Migration und Integration, Bahnhofstrasse 88, 5001
  Aarau), asks for the arrival date, says that no Aargau or Baden procedure
  is published, and cites the SEM FAQ and SEM's directory.

### UAT-37: a foreign licence in St. Gallen, in German

**Preconditions.** `foreign-licence-exchange` serves VZV Article 42 and the
ch.ch summary: twelve months on the foreign licence, the exchange with the
original licence and an eye test, a control drive for a licence from outside
the EU/EEA; exchange fees are named as not served. The Canton of Zurich's
exchange page, its control-drive page and its Road Traffic Office are
rejected for `CH-SG`.

**User:** "Ich bin vor zehn Monaten aus Brasilien nach St. Gallen gezogen und
fahre noch mit meinem brasilianischen Führerausweis. Wie lange darf ich das
noch, und was muss ich für den Umtausch tun?" ("I moved from Brazil to St.
Gallen ten months ago and still drive on my Brazilian licence. How long may
I still do that, and what do I have to do for the exchange?")

**The trap.** The Zurich Road Traffic Office's locations, application form,
country lists or control-drive rules given for St. Gallen; the foreign
licence treated as valid without limit.

**Expected**

- The search is sent in German; the assistant resolves for `CH-SG`.
- The answer, in German, says that two of the twelve months remain, that a
  Swiss licence is needed afterwards and a later exchange may cost a fine,
  that the exchange needs the original licence and an eye test, and that a
  Brazilian licence requires a control drive. It says that no St. Gallen
  procedure, office, form or fee is published, and cites the ch.ch page.

### UAT-38: ordinary naturalisation in the city of Bern

**Preconditions.** `naturalisation-ordinary` serves SEM's federal conditions,
that cantonal law adds a minimum residence of two to five years in the
municipality and the canton, that the form comes from and the application
goes to the competent authority at the place of residence, and the federal
fee of CHF 100 with cantonal and municipal fees added. The Canton of Zurich
states two years in the municipality and CHF 500, the City of Zurich its own
fee; both are rejected for `CH-BE-351`.

**User:** "I'm a Portuguese citizen with a C permit. I have lived in
Switzerland for twelve years, the last three of them in the city of Bern.
Can I apply for Swiss citizenship now, how long must I have lived in Bern,
and what does it cost?"

**The trap.** Zurich's figures given for Bern: two years in the
municipality, CHF 500, or the Gemeindeamt at Wilhelmstrasse 10 as the place
to file; a plain yes that decides eligibility.

**Expected**

- The assistant resolves for `CH-BE` (or `CH-BE-351`).
- The answer states the C permit, the ten years with three of the last
  five, and the integration conditions as conditions; that the canton sets
  the minimum residence within two to five years and that Bern's figure is
  not published; the federal fee of CHF 100, with cantonal and municipal
  fees not published for Bern; and the competent authority at the place of
  residence as the place to file, without naming one. It cites the SEM
  pages.

### UAT-39: premium reduction in Lucerne

**Preconditions.** `premium-reduction` serves the FOPH's federal frame (the
cantons reduce the premiums of insured persons in modest circumstances, the
canton decides who, how much and how, with or without an application,
payment to the insurer) and declares "the procedure of a canton other than
Zurich" as not served. `zh-premium-reduction` and the SVA Zurich's contact
are rejected for `CH-LU`.

**User:** "I moved from Austria to Lucerne in June and earn a modest salary.
Can I get a reduction of my health insurance premiums, and where do I
apply?"

**The trap.** The Canton of Zurich's procedure given for Lucerne: the SVA
Zurich, "only on application", the entitlement from the month after the
move; a Lucerne office, income limit or amount from general knowledge.

**Expected**

- The assistant resolves for `CH-LU`.
- The answer gives the federal frame, says that whether an application is
  needed and where it goes is decided by the canton and that the release
  publishes this for no canton other than Zurich, names no Lucerne office,
  deadline, income limit or amount, and cites the FOPH page.

### UAT-40: tax at source in Zug, in German

**Preconditions.** `tax-at-source-liability` serves the ESTV's statements and
QStV Article 9: from a gross income of at least CHF 120,000 the subsequent
ordinary assessment is mandatory and is kept until the liability ends; the
employer transfers the tax to the competent cantonal tax administration; the
tariff depends on the canton. The Canton of Zurich's two tax-at-source
concepts and its Cantonal Tax Office are rejected for `CH-ZG`.

**User:** "Ich wohne in Zug, habe eine B-Bewilligung und verdiene brutto
140'000 Franken im Jahr. Mein Arbeitgeber zieht Quellensteuer ab. Muss ich
trotzdem eine Steuererklärung ausfüllen, und an welches Amt wende ich mich?"
("I live in Zug, hold a B permit and earn CHF 140,000 gross a year. My
employer deducts tax at source. Do I still have to file a tax return, and
which office do I turn to?")

**The trap.** The Cantonal Tax Office of Zurich (Bändliweg 21, its
tax-at-source telephone number) or the Zurich directive ZStB 87.3 given to a
resident of Zug; tax at source treated as final.

**Expected**

- The search is sent in German; the assistant resolves for `CH-ZG`.
- The answer, in German, says that the subsequent ordinary assessment is
  mandatory from CHF 120,000 and continues until the liability ends, that
  the tax at source keeps being deducted, and that the office is the tax
  administration of the canton of residence, whose contact the release does
  not publish for Zug. It names no tariff or amount and cites the ordinance.

### UAT-41: the migration office of the Canton of Bern

**Preconditions.** `cantonal-migration-contact` serves SEM's entry for Bern
(Amt für Bevölkerungsdienste des Kantons Bern, Ostermundigenstrasse 99B,
3006 Bern, +41 31 633 53 15). Opening hours are published for the Zurich
Migration Office only, and `zh-migrationsamt-contact` is rejected for
`CH-BE`. DECLINE-6 checks the same rejection at the server alone; this case
adds the live answer. The same question asked for Basel reads `weak` in
lexical search in every wording tried and is kept as the regression case
`XC-23`.

**User:** "What is the address of the migration office of the Canton of
Bern, and when is it open?"

**The trap.** The Zurich office's counter hours (08.00 to 16.30), address
or telephone given for Bern; hours or an e-mail address from general
knowledge.

**Expected**

- The assistant resolves for `CH-BE`.
- The answer gives the address and the telephone number of SEM's entry,
  says that the release publishes no opening hours for Bern and names
  none, and cites SEM's directory page.

### UAT-42: registering in Winterthur

**Preconditions.** For `CH-ZH-230` the federal deadline and the Canton of
Zurich's registration facts are served (in person at the residents'
registration office of the municipality within 14 days, which forwards the
application to the cantonal Migration Office; a B permit for a contract of
more than a year). The appointment duty, the documents list and the
Personenmeldeamt are the City of Zurich's and are rejected.

**User:** "I'm a Spanish citizen and move from Madrid to Winterthur next
month for a two-year job. How do I register there, and do I have to book an
appointment first?"

**The trap.** The City of Zurich's procedure given for Winterthur: a
compulsory appointment, the Personenmeldeamt Zürich Süd at Stadthausquai 17
or the Kreisbüro; a resolve for `CH-ZH-261` because the canton is Zurich.

**Expected**

- The assistant resolves for `CH-ZH` or `CH-ZH-230`; the city concepts, if
  requested, are rejected.
- The answer gives the personal registration with the municipality within
  14 days of arrival and before starting work, the documents the federal
  fact names, the forwarding to the cantonal Migration Office and the B
  permit; it says that the appointment duty the release publishes is the
  City of Zurich's and that nothing is published on Winterthur's office or
  appointments; it asks for the arrival date and cites the SEM FAQ and the
  Canton of Zurich page.

### UAT-43: moving to Uster with a dog

**Preconditions.** `zh-dog-keeping` serves the canton's duties for every
Zurich municipality (report to the municipality of residence and AMICUS
within ten days, liability insurance of at least CHF 1 million, the dog tax
without an amount, the training duty of 1 June 2025 with its exemptions).
`city-zurich-dog-registration` (the City Police's dog control, the city's
leash season and breed list) is rejected for `CH-ZH-198`. UAT-24 is the same
question asked in the city.

**User:** "I'm moving from Germany to Uster with my three-year-old dog. What
do I have to do for the dog, and where do I register it?"

**The trap.** The City Police's dog control at Hohenbühlstrasse 15 given for
Uster; "no course is needed".

**Expected**

- The assistant resolves for `CH-ZH-198` (or `CH-ZH`).
- The answer names the report to the municipality of residence and AMICUS
  within ten days, the liability insurance, the dog tax without an amount,
  the theory course within two months and the practical course of at least
  six lessons with their exemptions; it says that no Uster office or
  address is published, and cites the cantonal dog page.

### UAT-44: moving to Kloten with a car, in German

**Preconditions.** `zh-vehicle-registration-move` serves the canton's
procedure for every Zurich municipality (UAT-29 is the same move into the
city). The resident parking card (CHF 300 a year, the permit office at
Mühlegasse 18) and the city checklist are the City of Zurich's and are
rejected for `CH-ZH-62`.

**User:** "Ich ziehe mit meinem Auto von Luzern nach Kloten. Was muss ich
beim Strassenverkehrsamt erledigen, und was kostet eine Anwohnerparkkarte?"
("I am moving with my car from Lucerne to Kloten. What do I have to do at
the Road Traffic Office, and what does a resident parking card cost?")

**The trap.** The City of Zurich's card given for Kloten: CHF 300, the
permit office or its telephone number; the city's 14 days for the plates;
keeping the Lucerne plates.

**Expected**

- The search is sent in German; the assistant resolves for `CH-ZH-62` (or
  `CH-ZH`).
- The answer, in German, gives the canton's procedure (the online form, the
  original documents by post to the Strassenverkehrsamt Bülach, the
  insurance certificate, new plates within 5 to 10 working days, no driving
  licence needed) and declines the second part by name: the parking card
  the release publishes is the City of Zurich's, and nothing is published
  for Kloten. It cites the cantonal vehicle page.

## Entry-and-visa cases

UAT-45 to UAT-50 check the `entry-visas` topic and the two Zurich
family-reunification concepts, built from SEM's entry pages, the FDFA visa
page and the Ordinance on Entry and the Granting of Visas (VEV,
SR 142.204). The facts were written by the assistant from the saved pages
and confirmed by one reviewer. Budgets and criteria A1 to A6 are those of
the single-turn cases; A7 applies to all six, because each names a trap, and
A9 to UAT-49, where the release serves the rule but not the answer for a
single nationality. The topic is federal, so every case resolves for the
Canton of Zurich but the served facts apply in every canton.

### UAT-45: how the 90 days in 180 are counted

**Preconditions.** `entry-short-stay-rule` serves SEM's rule (at most 90
days within 180, the day of entry and the day of departure counted, the
rolling 180-day window, 90 days outside the area before a new stay) and
SEM's three worked examples.

**User:** "I am from a country whose citizens need no visa. I was in the
Schengen area for 60 days between March and May and now want to spend
another 50 days in Zurich. Is that allowed?"

**The trap.** Treating the 90 days as a fresh allowance per entry, per
country or per calendar half-year, or computing an exact date although the
user gave no arrival date.

**Expected**

- No: with 60 days already used inside the rolling window only 30 remain.
  The answer explains the rolling 180 days, says the day of entry counts,
  and asks for the exact dates instead of computing a date (A3). It cites
  SEM's page on calculating the duration of stay.

### UAT-46: which visa for a two-year job in Zurich

**Preconditions.** `entry-visa-types` serves the two visa types and the
cantonal approval of the type D visa; `entry-visa-application` serves that
the representation forwards a type D application to the cantonal migration
office.

**User:** "I am a third-country national with a job offer in Zurich for two
years. Which visa do I need and who has to approve it?"

**The trap.** A Schengen visa C for a two-year job, or a visa the
representation grants on its own without the cantonal migration office.

**Expected**

- A national visa of type D, for stays of more than 90 days and for gainful
  employment, granted only with the approval of the cantonal migration
  office of the intended place of residence. It cites SEM's entry FAQ and
  the FDFA visa page.

### UAT-47: what a Schengen visa costs

**Preconditions.** `entry-visa-fee-insurance` serves the fees (EUR 90 for
adults, EUR 45 for children from 6 to 12, the service provider's own fee),
the processing times (as a rule 15 days, exceptionally 30 or 60; at least a
month for a type D visa) and the travel health insurance of up to
EUR 30,000.

**User:** "What does a Schengen visa cost for me and my eight-year-old
daughter, how long does the decision take, and do we need insurance?"

**The trap.** One flat fee for every applicant, a decision "within a few
days", or no insurance requirement.

**Expected**

- EUR 90 and EUR 45, the external service provider's fee on top, a decision
  as a rule within 15 days, and travel health insurance covering up to
  EUR 30,000 for the whole stay. It cites SEM's entry FAQ.

### UAT-48: ETIAS before flying, and the passport stamp

**Preconditions.** `entry-etias` serves what ETIAS is, that no application
could be filed when the page was saved, the validity of up to three years
and the EUR 20 fee; `entry-exit-system` serves that the EES has been
introduced since 12 October 2025 and replaces the manual stamp.

**User:** "Do I have to apply for ETIAS before I fly to Zurich next month,
and will my passport still be stamped at the border?"

**The trap.** Telling the user to apply for ETIAS now, or saying the
passport is still stamped as before.

**Expected**

- On the cited page no application can be filed yet and no step is needed;
  the answer says this is the state of the page, not of today (A3). The
  stamp is replaced by an EES entry, which also calculates the duration of
  stay. It cites SEM's ETIAS and EES pages.

### UAT-49: visa duty of one nationality

**Preconditions.** `entry-visa-need` serves that the visa duty depends on
nationality, names SEM's overview by nationality (Annex CH-1, List 1) and
the VEV's visa duty for short and longer stays. Its `not_served` names the
visa rules of an individual country.

**User:** "I am an Indian citizen and would like to visit Zurich for two
weeks. Do I need a visa?"

**The trap.** Answering "yes, you need a Schengen visa" or "no" from model
memory, as if the release carried the country list.

**Expected**

- The answer gives the rule, says that the list for a single nationality is
  not served and points to SEM's page (A9), and does not state a duty for
  Indian citizens. It may add that a two-week visit falls under the
  90-in-180-days rule.

### UAT-50: family reunification on a short-stay L permit in Zurich

**Preconditions.** `zh-family-l-permit` serves the Migration Office's
conditions (spouse or registered partner and children under 18, an adequate
flat, no social assistance, no supplementary benefits, no grounds for
revocation), the documents for a spouse and for children, and that the
documents can be handed in at the counter, online or by post.

**User:** "I am a third-country national with a short-stay L permit in the
Canton of Zurich. Can my wife and our ten-year-old son come, and what do I
have to submit?"

**The trap.** Refusing family reunification for a short-stay permit
outright, or quoting the documents of the B or C permit route (twelve months
of payslips, a language certificate).

**Expected**

- Yes, an entry application is possible under the named conditions, with the
  entry application, the legalised marriage certificate, the tenancy
  agreement, the landlord's consent, six months of payslips, the employment
  contract and a debt-collection register extract. It cites the Canton of
  Zurich family-reunification pages.

## Voting-rights and tax-at-source tariff cases

UAT-51 to UAT-53 check the `political-rights` topic and the two
tax-at-source tariff concepts, built from the Federal Constitution, the
Constitution of the Canton of Zurich, ch.ch, the Canton of Zurich's voting
page, the Tax at Source Ordinance and the Canton of Zurich's tariff page and
2026 parameter sheet. The facts were written by the assistant from the saved
pages and confirmed by one reviewer. Budgets and criteria A1 to A6 are those
of the single-turn cases; A7 applies to all three, A8 to UAT-53 and A10 to
UAT-52 (Winterthur) and UAT-53 (Bern). UAT-51 asks the voting question,
which the release covers; DECLINE-1 declines a rent question instead.

### UAT-51: voting in the city elections after twelve years on a C permit

**Preconditions.** `zh-political-rights` serves the Constitution of the
Canton of Zurich (Art. 22: the political rights in cantonal and communal
matters belong to Swiss citizens resident in the canton, aged 18 or over),
the canton's statement of who may vote and the Evangelical Reformed church's
exception; `political-rights-federal` serves that foreign nationals have no
federal vote.

**User:** "I have had a C permit for twelve years and live in the city of
Zurich. Can I vote in the city elections next spring?"

**The trap.** A yes because of the long stay or the C permit, or "some
municipalities allow it" carried over from cantons that do; the church
exception presented as a general municipal vote.

**Expected**

- No: in the Canton of Zurich, including the City, only Swiss citizens
  resident in the canton and aged 18 or over vote in cantonal and communal
  matters, and foreign nationals have no federal vote, whatever the permit
  or the length of stay. The answer may name the elections and votes of the
  Evangelical Reformed church, open to B, C and Ci permit holders, as the
  one exception, and naturalisation as the route to the vote. It cites the
  cantonal constitution or the canton's voting page.

### UAT-52: the tax at source in Winterthur compared with the City of Zurich

**Preconditions.** `zh-tax-at-source-tariffs` serves the tariff code format,
the tariffs by civil status, the tariff calculator, the 2026 tariff tables and
the 2026 calculation parameters, among them the weighted average of the
municipal tax multipliers; `tax-at-source-tariff-codes` serves the federal
codes.

**User:** "I live in Winterthur, have a B permit and am taxed at source. How
much tax at source do I pay, and would it be less if I lived in the city of
Zurich?"

**The trap.** A percentage of the salary quoted from memory, or Winterthur's
own municipal tax multiplier said to change the deduction, or the ordinary
tax rates of the two municipalities compared.

**Expected**

- No amount: the deduction depends on the tariff code (civil status,
  children, church tax) and the gross monthly salary, and the answer points
  to the canton's tariff calculator (not legally binding) and tables. The
  canton calculates its tariffs with the weighted average of the municipal
  tax multipliers (in 2026, 109.90 per cent without church tax and 116.00
  with), so living in the City of Zurich would not change the tax at source.
  It cites the canton's tariff page or the parameter sheet.

### UAT-53: voting rights of a C permit holder in Bern, in German

**Preconditions.** `political-rights-federal` serves ch.ch's statement that
foreign nationals have no federal vote, that the canton and the commune
decide on a cantonal or communal vote and that Jura and Neuchâtel grant a
cantonal one, and Article 39 of the Federal Constitution; the Canton of
Zurich concept is refused for Bern.

**User:** "Ich wohne seit zehn Jahren mit einer C-Bewilligung in Bern. Darf
ich bei den kantonalen Wahlen abstimmen?"

**The trap.** The Canton of Zurich's rule (Swiss citizens only) or its
church exception given for Bern, or a plain yes or no for Bern from general
knowledge.

**Expected**

- In German: no federal vote; whether a foreign national votes in cantonal
  matters is the canton's decision, and the release names Jura and Neuchâtel
  as the cantons that grant it but publishes no rule of the Canton of Bern,
  which the answer says instead of deciding for Bern. It cites ch.ch or the
  Federal Constitution and names nothing of the Canton of Zurich.

## Expat-life cases

UAT-54 to UAT-64 check the topics `family-benefits` and `housing` and the
concepts of the residence, social-insurance, health-insurance and vehicles
topics that cover marriage, leaving the City of Zurich, pillar 3a,
unemployment, accident insurance and customs on moving. The facts were
drafted by assistant subagents, checked against their excerpts by the
coordinating assistant and confirmed by one reviewer. Budgets and criteria
A1 to A6 are those of the single-turn cases; A7 applies to all eleven, A8 to
UAT-57 and UAT-64, A10 to UAT-58 (Winterthur). The questions, expected
answers, traps and claims are in `releases/mvp-zurich/acceptance.yaml`; the
index above gives each case's trap and served concepts.

### UAT-54: family allowance for a 17-year-old in Zurich

"I work full-time in Zurich and my 17-year-old son is at a vocational school.
How much family allowance do we get per month, and how do I claim it?" The
Canton of Zurich's education allowance of CHF 268 a month from 16 to 25,
claimed through the employer; SVA Zurich's pages cited.

### UAT-55: paternity leave

Two weeks within six months of the birth, in a block or day by day, 80
percent of earnings up to CHF 220 a day, at most CHF 3,080; the FSIO page
cited.

### UAT-56: a deposit of four months' rent

No: at most three months' rent, on an account in the tenant's name (Code of
Obligations Art. 257e); the law cited.

### UAT-57: a rent increase by e-mail, in German

No, not in that form: the official form, reasons, at least ten days before
the notice period, at the earliest to the next termination date (Art. 269d);
answered in German.

### UAT-58: challenging the initial rent in Winterthur

Within 30 days of taking over the flat, if the rent rose significantly
against the previous tenant's (Art. 270); the Canton of Zurich's initial-rent
form applies in Winterthur; nothing of the City of Zurich.

### UAT-59: marrying a Brazilian fiancée in Zurich

Yes with a lawful stay (visa or permit card); documents from the home
country take 3 days to 6 months and must reach the civil registry office two
months before, the preparation must end one month before.

### UAT-60: leaving Zurich for good

Deregister at the earliest 30 days before and at the latest 14 days after
moving out; moving abroad ends the tax liability and all taxes fall due;
contact the City's tax office.

### UAT-61: pillar 3a on leaving Switzerland

CHF 7,258 in 2026 for an employee with a pension fund; leaving Switzerland
permanently allows an early withdrawal.

### UAT-62: unemployment after ten months

Not on the contributions alone: 12 months within 2 years are required unless
an exemption applies, which the answer asks about; sign on with the RAV at
the latest on the first day claimed.

### UAT-63: a skiing accident on six hours a week

Leisure accidents are covered by the employer's insurance only from 8 hours
a week with the same employer; below that through the health insurance.

### UAT-64: customs on furniture and a car, in German

Duty-free with the move of residence, 6 months of prior use and continued
use, form 18.44 at the entry customs office, within two years of the move.

## Settlement-permit cases

UAT-65 and UAT-66 check the two concepts added on 22 September 2026,
`permit-c-five-years` (SEM) and `zh-permit-c-five-years` (the Migration
Office of the Canton of Zurich), which publish the five-year routes to the
settlement permit that rest on settlement agreements and treaties. Until
then the release served the ten-year rule of AIG Art. 34 alone, and the
recorded UAT-5 sessions showed a caller inventing the exclusion it could
not read anywhere ("there are no special EU/EFTA shortcuts that apply to
you"). Both pages were already in the catalogue and the text dataset; no
source was added. Budgets and criteria A1 to A6 are those of the
single-turn cases, A7 applies to both. The nine facts are
`assistant-authored-unreviewed` until the reviewer confirms them, so both
cases run against unreviewed statements and every result's `limitations`
says so. The questions, expected answers, traps and claims are in
`releases/mvp-zurich/acceptance.yaml`.

Neither case decides an application: the pages state conditions, and
whether a particular person meets them is the Migration Office's
assessment. The distinction the Migration Office's own directive draws
between an agreement that confers an entitlement and a treaty that does not
is **not** published here: the web pages put both lists under "can obtain",
and the release says no more than they do.

### UAT-65: German citizen after five years in Zurich

"As a German citizen with five years in Zurich, can I get the settlement
permit already, or only after ten years?" Germany is on the list of
countries with a settlement agreement; five years of uninterrupted
residence, the integration criteria and no grounds for revocation; German
nationals submit no language evidence. SEM's page names Germany in the same
five-year list.

### UAT-66: US citizen asking about the five-year settlement permit

"I'm American and have been living in Zurich for five years. My Italian
colleague told me she can apply for the C permit now. Does that apply to me
too?" The Canton of Zurich lists the United States of America among the
countries with settlement treaties, so the five-year route is open on the
same conditions; unlike the colleague and unlike German, Austrian and
Liechtenstein nationals, the user submits evidence of German at A2 spoken
and A1 written. SEM's five-year list is the EU/EFTA one and does not name
the United States.

### UAT-67: Newcomer looking for a German course

"I moved to Winterthur from Brazil last month and my German is poor. Where do
I find a German course, and is there someone who can advise me which one
fits?" The offer database of the Fachstelle Integration lists what the canton
finances with the municipalities, searched by category and municipality. For
choosing a course there is advice: many municipalities have integration
contact persons, and where a municipality has none the cantonal
German-course advice is free and available in 16 languages; the canton also
keeps a German-course and language-examination database. Winterthur is one of
the two cities with their own databases, which the answer should name.

### UAT-68: Who informs a newly arrived family

"We arrived in the Canton of Zurich two weeks ago on a family reunification
permit. Nobody has told us anything about courses or counselling. Whose job is
that?" The municipalities inform newly arrived migrants soon after arrival,
give a first orientation and arrange access to German courses where needed;
the canton supports them with a guide. People in family reunification are one
of the three groups the canton names as needing support early. For further
advice there are the regular services and migration-specific counselling, for
which the Fachstelle keeps a list updated at least once a year and with no
claim to completeness.

### UAT-69: Where to turn after racist discrimination

"My colleague keeps making remarks about my skin colour and my manager laughs
along. Is that racist discrimination, and who advises me in Zurich?" The
canton counts demeaning statements as a form of racist discrimination and
names the workplace as a place where it occurs. ZüRAS advises those affected,
in several languages and free for people living in the canton, run by the AOZ
on behalf of canton and city. Beyond the canton there are the counselling
network for victims of racism and the reporting platform for online hate
speech. The legal bases are BV Art. 8(2), StGB Art. 261bis for acts committed
in public, and AIG Art. 53; whether this case is punishable is not the
service's to decide.

### UAT-70: An association asks for project money

"Our association in Uster wants to run a neighbourhood festival for Swiss and
migrant families and needs about 4,000 francs. Can the Canton of Zurich
contribute, and how do we apply?" Yes in principle: non-profit organisations
seated in the canton can apply, and the festival falls under the priority
"living together and participation". At 4,000 francs it is a small project:
up to 5,000 francs, rolling while funds last, simplified rules, a budget on
the mandatory template, and a web form that cannot be saved in between. The
deadline of 31 October 2026 and the 50,000-franc maximum belong to the larger
projects.

### UAT-71: Finding an association of one's own community

"Are there Tamil associations in the Canton of Zurich, and how do I find one
near me?" The release does not publish associations by community; it publishes
the platform for migrant associations, searchable by criteria such as
municipality or region, on which associations register themselves. The answer
points at the platform instead of naming associations.

## Customs cases

UAT-72 to UAT-80 check the eight concepts of the `customs` topic added on
22 September 2026 from the pages of the Federal Office for Customs and Border
Security. Until then the release served one customs statement, inside the
moving topics: what happens to household goods on a move. The recorded UAT-64
session showed the gap - a caller asked about furniture and a car and got the
removal-goods rule with nothing about the value limit, the quantities or what
a parcel costs. Budgets and criteria A1 to A6 are those of the single-turn
cases. The facts are `assistant-authored-unreviewed` until the reviewer
confirms them, so every result's `limitations` says so. The questions,
expected answers, traps and claims are in
`releases/mvp-zurich/acceptance.yaml`.

Two boundaries run through the whole group. The value limit and the duty-free
quantities are separate limits that both apply, and a traveller's allowance
says nothing about a consignment that arrives by post. And the release
publishes the rules, never the outcome for one item: tariff numbers, duty
rates per product and the treatment of an individual consignment are out of
scope, which DECLINE-11 checks.

### UAT-72: Two people, one coffee machine

"My partner and I are driving to Konstanz on Saturday. If we buy a coffee
machine together for 280 euros, are we under the limit because there are two
of us?" No. The value-free limit applies per person and per day to goods in
private use or given as gifts, and the allowances of several travellers
cannot be added together for one item, so the machine is declared and import
tax falls due on its whole value. The trap is the arithmetic the question
invites: two allowances, therefore nothing to declare. The answer states the
limit the page gives and says which of the two rules - per person, not per
item - decides the case.

### UAT-73: Meat and wine on the way back from Italy

"We are driving back from Italy with about four kilos of meat, six litres of
wine and a bottle of grappa. What do we have to declare?" The release
publishes the rule and not the table. Goods brought in for private use or as a
gift are free of duty except for sensitive goods, on which duty falls due
above a quantity; the quantities count per person and per day; animal products
may be brought in only from the countries the page lists; and once the total
value carried passes the value limit, value-added tax is due on everything
carried, food included. The FOCBS publishes the quantities themselves as a
graphic, so no fact carries them and the concept says so in its `not_served`.
The trap is the one a general model walks into every time: confident numbers -
a kilo of meat, five litres of wine, two hundred cigarettes - that the release
cannot support. A correct answer gives the rules it has, says that the
quantities per product are not published here, and invents none.

### UAT-74: Declaring a bicycle before the border

"I am bringing a bicycle worth 900 francs back from Germany tomorrow. Can I
declare it online before I get there, or do I have to stop at the border?"
Both work: the QuickZoll app declares the goods and takes the payment before
or at the crossing, and at a staffed crossing the red channel does the same
in person. The green channel is not a choice for goods above the limits. The
trap is treating the green channel or an unstaffed crossing as permission not
to declare; the answer names what the page says not declaring means.

### UAT-75: A laptop ordered from a German shop

"I ordered a laptop for 900 euros from a German shop. What will I pay on top
of the price when it arrives?" Import tax on the value of the consignment,
the carrier's own clearance charge, which is not a tax, and customs duty
where the goods carry one. The recipient is the importer, which is why the
bill arrives here. The trap is the traveller's value limit: it applies to
goods a person carries across, not to a consignment, so a caller who answers
"under 150 francs, so nothing to pay" is wrong twice over - wrong rule, and
the limit is not a threshold for the tax either.

### UAT-76: Sometimes a charge, sometimes not

"I order small things from a platform abroad. Sometimes there is a charge and
sometimes there is not. Why?" Two different reasons, and the answer must
separate them. A consignment is not taxed when the tax that would be due
stays under the amount the page names - a threshold on the tax, not on the
price. And a seller or platform that is registered for Swiss VAT charges the
tax at the sale and imports in its own name, so nothing more is collected at
the border. The trap is stating a single price limit under which everything
arrives free.

### UAT-77: Sending a jacket back

"I am sending a jacket back to Germany that I paid tax and duty on when it
arrived. Do I get that money back?" Under the conditions the page states, and
only against the declaration and the evidence it names - it is not automatic
and not a refund the carrier makes. The same section covers goods sent abroad
for repair. The trap is the assumption that a return cancels the import by
itself.

### UAT-78: Furniture and a car from Boston

"We are moving from Boston to Zurich in November with our furniture and our
car. What does customs want?" Removal goods come in free of duty when they
were used before the move and are kept afterwards, declared with the
inventory and the form the page names, within the window it states; a vehicle
is removal goods too but carries its own conditions; goods inherited abroad
follow a separate rule. The trap is the single sentence the release served
before this wave, which named the relief and none of its conditions: the
answer must state the used-before-and-kept-after condition and the window,
and must not promise that the car is simply free.

### UAT-79: Arriving with two dogs

"We are moving to Zurich with our two dogs. What do we need at the border,
and what do we have to do once we are here?" Two different sets of rules, and
the answer must give both without mixing them: at the border the
identification and the rabies vaccination the page requires, with the number
of animals that still counts as a private import; in the city, the
registration and the dog rules the release already publishes. The trap is
answering only one of the two, or treating the city's registration as a
customs formality.

### UAT-80: A visitor taking a watch home

"A friend visiting from London bought a watch here. Can she get the Swiss VAT
back when she flies home?" Yes, under the export conditions the page states:
a buyer resident abroad, the goods leaving within the period it names, the
minimum amount and the export document confirmed as the page describes. The
trap is generalising the refund to anyone leaving the country: a person
resident in Switzerland taking their own goods abroad is the other rule on
the same page, and it does not refund the tax.

## Basic health insurance cases

UAT-81 to UAT-88 check the eight concepts added to the `health-insurance` topic on
23 September 2026 from the pages of the Federal Office of Public Health and the
premium-information service priminfo. Until then the release served the insurance
duty, the Zurich exemption, premium reduction federally and in Zurich, and accident
insurance: a newcomer learned that they must insure themselves within three months
and nothing about what the insurance then costs them, what it pays for, or how to
change it. Budgets and criteria A1 to A6 are those of the single-turn cases. The
facts are `assistant-authored-unreviewed` until the reviewer confirms them, so every
result's `limitations` says so.

Two boundaries run through the group. Every condition rests on an excerpt of the
authority's own page or of the law; where a priminfo page says the same thing in
plain language it stands beside that excerpt and never alone, and the basis served
with the citation says which is which. And the release publishes the rules, never the
prices: premiums, premium reductions and the comparison calculator are out of scope,
which DECLINE-12 checks.

### UAT-81: A broken arm and the bill

"My son fell off his bike and the bill is 1,200 francs. We have the lowest franchise.
What do we actually have to pay ourselves?" The answer must separate the two parts of
cost sharing - the franchise the insured pays first, then the retention as a
percentage of what remains, up to its annual cap - and must say that children are
treated differently from adults. Where the answer gives an amount it must be the
amount the cited page states, with the year it applies to. The trap is treating the
franchise as the whole of the cost sharing, or quoting an adult's cap for a child.

### UAT-82: The cheaper family-doctor model

"My insurer offers a family-doctor model that is 15 per cent cheaper. What am I giving
up?" The answer must say what restricting the choice of provider means in practice:
the insured undertakes to contact the named first point of contact before any other
treatment, the insurer grants a discount for that, and the model binds the insured for
the period the contract states. The release carries no discount percentage, so the
answer must not confirm, correct or invent one; it may repeat the caller's own figure
only as the caller's. The trap is presenting the discount without the obligation,
claiming the choice of doctor is unaffected, or stating a percentage as if the release
held it.

### UAT-83: Changing insurer after a rise

"My premium is going up again. Can I switch insurer, and by when?" The answer must
give the two notice periods the act sets apart: the ordinary one of three months to the
end of a calendar half-year, and the shorter one that the announcement of a new premium
opens - one month's notice to the end of the month before the month from which the new
premium applies. It may work that second period out for the usual case, where premiums
apply from 1 January and notice therefore has to be given by the end of November, but it
must not present that date as the only rule. It must add that the new insurer may not
refuse an applicant for basic insurance, that the old cover runs until the new insurer
has confirmed cover without interruption, and that the old insurer may not make the
change conditional on giving up a supplementary insurance. The trap is saying the
insured can leave at any time, or that a poor claims history can be refused.

### UAT-84: Why my premium differs from my colleague's

"My colleague lives two towns away and pays less than I do for the same insurer. How is
that possible?" The answer must name the three things that make premiums differ - the
canton, the premium region within it, and the age group - and say who sets the regions.
It must not state a premium: the release publishes the rules and points at the official
comparison for the prices, which it does not carry. The trap is inventing a figure, or
explaining the difference by the insurer alone.

### UAT-85: Glasses, and whether supplementary insurance is needed

"Does basic insurance pay for my glasses, and do I need supplementary insurance?" The
answer must say that basic insurance covers the same defined benefits everywhere, that
the list is set federally and not by the insurer, and that supplementary insurance is a
different contract which an insurer may refuse. Where the cited pages do not say
whether one particular item is covered, the answer must say so rather than guess. The
trap is answering the glasses question from general knowledge.

### UAT-86: Months of unpaid premiums

"I lost my job and have not paid my premiums for four months. Can they cancel my
insurance?" The answer must give the sequence the page states - reminder, then debt
enforcement - and say what the canton does with a list of defaulters and what remains
covered while the arrears stand. It must add that the arrears block a change of insurer
until they are paid in full, which is what a caller reaches for next, and that arrears
for the children alone do not block the parent's own change. The trap is saying that
cover simply ends, which is what a general answer assumes, or sending the caller off to
a cheaper insurer they cannot join.

### UAT-87: Living in Germany, working in Zurich

"I live in Konstanz and start work in Zurich next month. Which country's health
insurance do I take?" The answer must start from the place-of-work principle, which
makes Swiss insurance the rule, then name the right of option that the agreements with
the neighbouring states open, and the three months from the start of the employment
relationship within which an application for exemption has to be filed with the
authority of the canton of work. It must say that a merely tacit exercise of the option
is not legally valid, so a commuter who never filed can still be insured in Switzerland,
and it must say that the family members are covered by the same duty. The release does
not say whether an option once validly exercised can be reversed or used again, so the
answer must not claim either. The trap is answering "Switzerland, because you work
there" without the option, or asserting that the choice is made once and for all.

### UAT-88: Three weeks in Italy

"We are going to Italy for three weeks. Are we covered if something happens?" The
answer must say that basic insurance pays for treatment given abroad in an emergency,
and must give the test the ordinance sets for one: the person needs treatment during a
temporary stay abroad and a return journey to Switzerland is not reasonable. It must say
that there is no emergency where someone travels abroad in order to be treated, and it
must give the ceiling - at most twice what the same treatment would be reimbursed at in
Switzerland. The release does not carry the European health insurance card or the
coordination rules of the agreement with the EU, so an answer that leans on the card
rather than on the emergency rule is wrong even where it sounds right. The trap is
promising that everything is covered anywhere, or presenting the card as the instrument
the release describes.

### UAT-89: A pensioner in Portugal

"I have retired to Portugal and kept my Swiss health insurance. Why is my premium not
the one I paid in Zurich, and can I still get a premium reduction?" The answer must say
that a person living in an EU or EFTA state or the United Kingdom pays the premium that
applies to their state of residence, that the insurer calculates a separate premium per
state from the costs there, and that for pensioners the premium reduction is the
Confederation's business, carried out by the joint institution under the health
insurance act, rather than the canton's. It must not name an amount for any country:
the release carries the rule and not the price. The trap is applying the Zurich premium
or the cantonal premium reduction to someone who no longer lives in Switzerland.

### UAT-90: A bill from the doctor, not from the insurer

"My doctor sent the bill to me and not to my health insurer. Is that allowed?" The
answer must say that this is the ordinary case: unless the insurer and the provider have
agreed otherwise, the insured person owes the provider and then has a claim for
reimbursement against the insurer, and the other arrangement, under which the insurer is
billed directly, exists by agreement and covers the insurer's share for inpatient care.
It must add that the bill has to be detailed and comprehensible and to carry what is
needed to check how the payment was calculated. The release does not carry how long an
insurer may take to reimburse, what to do when the bill cannot be paid, or any ombudsman,
and the answer must not invent them. The trap is telling the caller the doctor made a
mistake.

### UAT-91: Four months of service

"I am starting four months of civilian service. Do I keep paying my health insurance?"
The answer must give the threshold - the duty to insure is suspended for people subject
to the military insurance for more than 60 consecutive days - and the step the caller has
to take themselves: telling their insurer at least eight weeks before it begins, failing
which the insurer stops charging only from the next date it can manage, at the latest
eight weeks after being told. The trap is answering that premiums simply continue, or
that the suspension happens by itself without the caller doing anything.
## Work and unemployment cases

Written on 23 September 2026 before the pages were curated, so that the cases
ask what a person out of work actually asks and not what the release happens to
carry. The topic `work-unemployment` is new; `unemployment-benefit` and
`zh-unemployment-benefit` move into it unchanged, and UAT-62 already covers the
contribution period, so these cases do not repeat it.

The release publishes the rules of unemployment insurance and never an amount
of daily allowance: `out_of_scope` names benefit amounts and every calculator.
Where a case says the answer must not give a figure, that is the point of the
case.

### UAT-92: The day the notice arrives

"I got my notice this morning. My last working day is at the end of November.
What do I have to do, and when?" The answer must put the registration first and
tie it to a date: a person threatened with unemployment registers with the RAV
as early as possible, and at the latest on the first day for which they claim
benefit, so registration belongs in the notice period and not after the last
working day. It must say that registration and the claim are two steps, and that
an unemployment fund is chosen. The trap is telling the caller to wait until the
employment ends, which costs them benefit days.

### UAT-93: How many applications, and can I say no

"How many job applications do I have to write each month, and can I refuse a job
that pays less than my old one?" The answer must give the duty to look for work
before and during unemployment and say that the RAV agrees the number of
applications rather than the law fixing one, that appointments at the RAV are
part of the duty, and that work is suitable within limits the rules set - a job
is not unsuitable merely because it pays less. It must name suspension days as
the consequence of a breach. The trap is inventing a fixed number of
applications a month.

### UAT-94: How long the benefit runs

"How long can I draw unemployment benefit, and how much will I get?" The answer
must give the structure and not a figure: waiting days before the first payment,
a number of daily allowances that depends on age and on months of contribution,
the two-year frame, and that the benefit is a percentage of insured earnings
with a higher percentage for a person with a maintenance obligation towards
children. It must not compute an amount in francs for the caller. The trap is
producing a monthly figure, or a single duration that ignores age and
contribution months.

### UAT-95: A job that pays less

"I have been offered a job that pays about half my old salary. If I take it, do
I lose my unemployment benefit?" The answer must explain interim earnings: the
insurance makes up part of the difference rather than the benefit simply
stopping, so taking the lower-paid job is not the loss the caller fears. It must
say that the interim earnings have to be declared. The trap is answering that
any work ends the entitlement.

### UAT-96: The employer goes bankrupt owing wages

"My employer went bankrupt and still owes me two months' wages. Is that lost?"
The answer must name insolvency compensation as the benefit for exactly this,
say which body it is claimed from and that it is claimed within a deadline, and
point to the Canton of Zurich's own route for a person living there. The trap is
treating it as ordinary unemployment benefit, or as a matter for the courts
alone.

### UAT-97: A course while unemployed

"Can I do a course while I am unemployed, and who pays for it?" The answer must
name the labour-market measures - courses, employment programmes and the
allowances - say that the RAV decides on them rather than the jobseeker
enrolling freely, and mention that allowances exist for a trial period or for
commuting. The trap is promising that any course the caller chooses will be
paid.

### UAT-98: The benefit runs out

"My daily allowances run out in two months and I still have no job. What
happens then?" The answer must say what ending the entitlement means, what the
RAV still offers afterwards, and that support beyond unemployment insurance is a
matter for the canton or municipality. Social assistance is named in
`out_of_scope`, so the answer must say the release does not cover it rather than
explain how to claim it. The trap is explaining social assistance.

### UAT-99: Three years working in Germany

"I worked in Germany for three years and moved to Zurich two months ago. Does
that time count if I lose my job here?" The answer must name the coordination
with the EU and EFTA: contribution periods completed in a member state can be
taken into account, the portable document U1 is how they are evidenced, and a
person who wants to look for work in another state while drawing Swiss benefit
needs the portable document U2. It must not promise that the German period
counts unconditionally. The trap is answering only from the Swiss contribution
period and ignoring the coordination entirely.

### UAT-100: Hours cut to sixty per cent

"My employer has cut everyone to 60 per cent and says we are on short-time work.
What does that mean for me?" The answer must say that short-time work
compensation is applied for by the employer and not by the employee, that it
covers a share of the earnings lost, and that the employee has to consent to it.
The trap is telling the employee to apply themselves, or treating it as
unemployment benefit.

### UAT-101: Seeing vacancies before everyone else

"A friend said jobseekers registered with the RAV see some vacancies before they
are public. Is that true?" The answer must give the job-registration duty:
occupations with unemployment above a threshold must be reported to the RAV
before being advertised elsewhere, and jobseekers registered with the public
placement service get access first for a period. It must not state the threshold
percentage or the head-start period unless the cited page states them. The trap
is dismissing it as a rumour.

### UAT-102: Which RAV, in Winterthur

"I live in Winterthur and have to sign on. Which RAV do I go to, and which
unemployment fund?" The answer must say how the responsible RAV is found for a
place of residence in the Canton of Zurich, that the jobseeker chooses an
unemployment fund at registration, and that the cantonal office offers
counselling and qualification. It must not name an office for a place outside
the Canton of Zurich as if the release covered it. The trap is inventing a
street address for the Winterthur RAV.

## AHV, the pillars and retirement cases

Written on 23 September 2026 before the pages were curated. The topic
`ahv-pension` is new. The release already serves what happens when a person
*leaves* Switzerland - the refund of contributions, the agreement states, the
pension abroad, the pension-fund cash payment - so these cases ask about being
here: who is insured, what is owed, what the record shows, and what happens at
the reference age.

The release publishes the rules and never a pension amount, and it does not
cover the invalidity insurance, the supplementary benefits or the bridging
benefit. Where a case says the answer must not give a figure or must decline a
neighbouring benefit, that is the point of the case.

### UAT-103: Not working, and asked to pay AHV

"I moved to Zurich with my husband and I don't work. Someone told me I still
have to pay AHV. Is that right?" The answer must say that insurance follows
residence and not employment, so a person living in Switzerland is insured even
without earnings, and that a non-employed person owes contributions in their own
right - while naming the exception for a spouse whose partner's contributions
count for both. It must say which office the person deals with. The trap is
answering that only employees pay, which is what most newcomers assume.

### UAT-104: Going self-employed

"I am leaving my job to work for myself. What changes for my AHV?" The answer
must say that a self-employed person registers with a compensation office and
owes the contributions themselves, where an employee splits them with the
employer, and must say what decides whether the authority accepts someone as
self-employed. It must not state a contribution rate or a franc amount unless
the cited page prints it. The trap is treating the change as automatic, or
giving a rate the pages do not carry.

### UAT-105: Checking the record

"How do I find out how much I have paid into the AHV over the years?" The answer
must name the individual account and the account statement, say that it is
ordered free of charge from a compensation office, and say what the AHV number
is for. It must say which office holds the account. The trap is confusing the
account statement with a forecast of the pension, which is a different thing and
which this release does not serve.

### UAT-106: Eight years abroad

"I lived abroad for eight years before moving here. Will that reduce my
pension?" The answer must say that a full pension requires a complete
contribution record, that a missing year reduces the pension, and how a gap can
be closed where the rules allow it. It must point the person at checking their
individual account early rather than at the moment of retirement. It must not
compute the reduction. The trap is promising that years abroad count, or
quantifying the cut.

### UAT-107: When can I stop

"I am 63. Can I retire now, and what does it cost me?" The answer must give the
reference age and the transitional rules that apply to women of the affected
cohorts, say that the pension can be drawn early or deferred, and say what each
does to it in the terms the page uses. It must not produce a percentage or an
amount unless the cited page prints it, and must not confuse the AHV reference
age with the rules of an occupational pension fund. The trap is a single
retirement age with no transitional rule.

### UAT-108: Turning sixty-five next spring

"I reach the reference age next March. Does the pension come automatically?"
The answer must say that it does not - the pension is claimed, some months
before the reference age, from the compensation office that holds the record -
and say what the person needs for the claim. The trap is telling the caller to
wait for a letter.

### UAT-109: After a death in the family

"My husband died last month. Is there anything from the AHV for me and our two
children?" The answer must name the widow's, widower's and orphan's pensions,
give the conditions the page states and say what ends them. Where the answer
touches the invalidity insurance or the supplementary benefits it must say the
release does not cover them rather than explain them. The trap is explaining
supplementary benefits, or promising a widower the same conditions as a widow
without checking what the page says.

### UAT-110: A career in two countries

"I worked in Italy for fifteen years and in Switzerland for twenty. Who pays my
pension?" The answer must say that under the coordination with the EU and EFTA
each state pays its own pension for the periods completed there, that periods
can be taken into account for the entitlement, and that contributions are not
refunded to nationals of Switzerland or an EU or EFTA state. It must distinguish
that from a third state with an agreement and from one without. The trap is
promising one combined pension from Switzerland.

### UAT-111: How does any of this work

"I have just moved to Switzerland. Can you explain how the pension system works
here?" The answer must lay out the three pillars and say which risk each covers,
and name the other branches - unemployment, accident, health and loss of
earnings - as parts of the same system. It must stay at the level of the map and
not drift into the rules of one branch. The trap is answering only about the
AHV, or inventing a pillar structure the pages do not state.

### UAT-112: Which office in Zurich

"Who do I contact about my AHV in Zurich, and how do I get my account
statement?" The answer must name the cantonal compensation office for the Canton
of Zurich, say who registers there, and say how the account statement is
requested. It must not name a compensation office for a place outside the canton
as if the release covered it. The trap is inventing an address or a form number.

### UAT-117: Waste day in Lugano

"Mi sono appena trasferita a Lugano. In che giorno passa la raccolta dei rifiuti
e dove metto i sacchi?" (I have just moved to Lugano. On which day is the waste
collected, and where do I put the bags?) Lugano publishes no collection day for
residents. The answer must say that household waste goes only in the official
red bags, into the underground or semi-underground containers. It must say
that residents may, as a rule, use those containers on every day of the week,
and that bulky and garden waste go only to the ecocentri. The trap is inventing
a weekly collection day or a street calendar, which is what a general assistant
does when it answers from other Swiss cities.

### UAT-118: Bin day in Basel

"I just moved to Basel. When is my garbage collected and when do I have to put
the bags out?" The answer must say that household waste goes in the blue
Bebbi-Sack, put out on the pavement twice a week, from 19:00 the evening before
or by 07:00 on the day. It must also say that the days depend on the
collection zone, which the city's zone search finds from the address. The trap
is naming a weekday for all of Basel, or answering with the Zurich rule.

### UAT-119: Collection area in St. Gallen

"Wann wird in St. Gallen der Kehricht abgeholt, und wie finde ich heraus,
welches Abfuhrgebiet ich habe?" (When is household waste collected in
St. Gallen, and how do I find out which collection area I am in?) The answer
must say that household waste is collected weekly and that the dates depend on
the collection area, one of A to K, L Ost and L West. It must say that the
online collection plan finds the area from the street, and that a street
directory lists it. The trap is naming one weekday for the whole city.

### UAT-120: Moving to Zurich with a Rottweiler

"I plan to bring my Rottweiler from Pargue to cita of Zuerich - what is the
procedure?" The misspellings are the user's and stay in the query. The answer
must open with the ban: the Rottweiler has been on breed-type list II of the
cantonal dog ordinance since 1 January 2025. Nobody may move into the Canton
of Zurich with a dog of that list, crosses with at least ten percent of their
blood included, and no test or temperament assessment makes an exception.
There is therefore no procedure for bringing the dog. The trap is listing the
registration steps (the dog control within ten days, AMICUS, the courses) and
the import rules as if the dog could come, or naming the ban only after them.
Search must rank `zh-banned-dog-breeds` among the first three hits, and the
answer must cite the Canton of Zurich page on banned dog breeds.

### UAT-121: Moving to Winterthur with a Rottweiler

"We are moving from Germany to Winterthur with our Rottweiler. Is that
allowed?" The answer must say no: the ban of breed-type list II is cantonal
and applies in Winterthur as everywhere in the Canton of Zurich, and it must
cite the Canton of Zurich page on banned dog breeds. The trap is calling the
ban a City of Zurich rule, or giving the City of Zurich's registration steps
for Winterthur.

### UAT-122: Autumn holidays in Geneva

"When are the autumn school holidays 2026 in Geneva?" The answer must give
Monday 19 October to Friday 23 October 2026, one week, from the Canton of
Geneva's page of the school year 2026/27. The trap is two weeks in October,
as in most German-speaking cantons.

### UAT-123: Summer holidays in the town of Lucerne

"Wann beginnen die Sommerferien 2027 in der Stadt Luzern?" (When do the
summer holidays 2027 start in the town of Lucerne?) The answer must give
Saturday 3 July 2027, until 15 August 2027, from the town of Luzern's row
of the canton's plan by municipality. The trap is one date for the whole
canton, whose municipalities set their own holidays.

### UAT-124: School holidays in Emmen

"When are the autumn school holidays 2026 in Emmen?" The release serves the
dates by municipality only for the town of Luzern, so for Emmen it serves
that the municipalities set their own holidays, the canton's frame and the
canton's plan for 2027/28, and never the town of Luzern's 2026/27 dates.
The trap is giving Luzern's dates as Emmen's.

## Decline cases

These cases check that the server rejects a request the release does not
cover and names the reason. They test the server only. After a rejection
the calling assistant may answer from other sources, and what it finds
there cannot be predicted, so no expectation applies to its answer. The
cases have no live run and no control. The `accept` stage replays them
from `releases/mvp-zurich/acceptance.yaml`: each resolve step must return
`OUT_OF_COVERAGE` for the declined concept together with the gap that
gives the reason (`expect_gap`, see
[acceptance-gate.md](https://github.com/swisstip/swiss-tip/blob/main/docs/architecture/acceptance-gate.md)). Concepts
requested alongside that the release does cover must stay `SUPPORTED`.
The search-decline cases check the step before: a question outside the
release still produces incidental hits ("Schweiz", "permit", "get" match
some concept), and `search` must report `match_strength` `weak` or `none`
with the scope statement (`expect_strength`), so the caller declines
instead of resolving the incidental hits. The same questions are pinned in
the round-trip check, and the VAT question in the image build in hybrid
mode.

| ID | Question | Request | Expected rejection |
| --- | --- | --- | --- |
| DECLINE-1 | "My 13-year-old daughter is moving with us to the city of Zurich. How does she get into a Gymnasium?" (a topic outside the release) | `gymnasium-admission`, a guessed concept ID, for `CH-ZH-261` | `OUT_OF_COVERAGE`, `concept_not_published` listing the published concept IDs |
| DECLINE-2 | "Ich bin tschechische Staatsbürgerin und fange nächste Woche in München an zu arbeiten. Bis wann muss ich mich dort anmelden?" (another country) | `eu-employment-registration-deadline` for `country_code: DE`, `population: eu_efta` | `OUT_OF_COVERAGE`, `jurisdiction_not_covered` with the published value `CH` |
| DECLINE-3 | "I'm an Italian citizen and moved to Geneva last week for a new job. Which office do I register with, and what is the procedure there?" (another canton) | `eu-employment-registration-deadline`, `zh-eu-registration`, `cantonal-migration-contact` for `CH-GE`, `population: eu_efta` | `zh-eu-registration` `OUT_OF_COVERAGE`, `jurisdiction_not_covered`; the federal deadline `SUPPORTED` with the caveat `more_specific_jurisdiction_not_published` naming `CH-ZH` and `CH-ZH-261`, and SEM's Geneva migration-office contact `SUPPORTED` |
| DECLINE-4 | "I'm moving from Milan to Winterthur for a job. Do I need an appointment at the Kreisbüro before I register?" (a municipality other than the City of Zurich) | `zh-eu-registration`, `city-zurich-arrival` for `CH-ZH-230`, `population: eu_efta`, `arrival_origin: abroad` | `city-zurich-arrival` `OUT_OF_COVERAGE`, `jurisdiction_not_covered` naming `CH-ZH-261`; the cantonal concept `SUPPORTED` with the caveat `more_specific_jurisdiction_not_published` naming `CH-ZH-261` |
| DECLINE-5 | "I'm a German citizen with a job offer in Zurich. Does my employer have to prove that nobody in Switzerland is available for the job?" (a rule for another population group) | `third-country-work` for `CH-ZH`, `population: eu_efta` | `OUT_OF_COVERAGE`, `context_not_covered` naming `population=third_country` |
| SEARCH-DECLINE-1 | "Wie hoch ist die Erbschaftssteuer?" (another tax) | `search` with the question | `match_strength` `weak`, the scope statement in the result. Until the customs cases of 22 September 2026 this case asked "Wie hoch ist die Mehrwertsteuer in der Schweiz?"; the release now publishes the rate of the tax on imports, so that question is covered and was replaced, as X1 prescribes |
| SEARCH-DECLINE-2 | "What is the speed limit on Swiss motorways?" (road traffic beyond the driving licence) | `search` | `weak` |
| SEARCH-DECLINE-3 | "How do I get a Halbtax?" (public transport) | `search` | `weak` |
| SEARCH-DECLINE-4 | "annual quotas for work permits" (named in `out_of_scope`) | `search` | `weak`; the work-permit concepts stay listed as incidental hits |
| SEARCH-DECLINE-5 | "Wann sind die nächsten eidgenössischen Abstimmungen?" (the dates of votes, which the voting-rights concepts do not serve) | `search` | `weak` |
| DECLINE-6 | "What are the opening hours of the Migration Office in Bern?" (the Zurich office asked for another canton) | `zh-migrationsamt-contact`, `cantonal-migration-contact` for `CH-BE` | `zh-migrationsamt-contact` `OUT_OF_COVERAGE`, `jurisdiction_not_covered`; SEM's Bern entry (address, no hours) `SUPPORTED` |
| DECLINE-7 | "Wann hat das Einwohneramt Winterthur offen?" (the City of Zurich office asked for another municipality) | `city-zurich-population-office` for `CH-ZH-230` | `OUT_OF_COVERAGE`, `jurisdiction_not_covered` naming `CH-ZH-261` |
| SEARCH-DECLINE-6 | "Opening hours of the Zurich zoo" (a place the release does not publish) | `search` | `weak`: "opening hours" and "Zurich" name no subject |
| SEARCH-DECLINE-7 | "What are the opening hours of the Zurich city library?" | `search` | `weak` |
| DECLINE-8 | "Wir wohnen in Wädenswil. Wann sind die Herbstferien 2026, und ab wann geht meine Tochter, die im Juni vier wird, in den Kindergarten?" (City of Zurich school dates asked for another Zurich municipality) | `city-zurich-school-holidays`, `city-zurich-kindergarten` for `CH-ZH-293` | both `OUT_OF_COVERAGE`, `jurisdiction_not_covered` naming `CH-ZH-261`; no cantonal or federal concept covers school dates, so nothing is served |
| DECLINE-9 | "Which rubbish bags do I have to use in Basel, and what do they cost?" (City of Zurich waste rules asked for another canton) | `city-zurich-household-waste` for `CH-BS-2701` | `OUT_OF_COVERAGE`, `jurisdiction_not_covered`; nothing is served |
| DECLINE-10 | "Which accredited IAZH offer types can I assign a refugee to, and how is the cost shared with the canton?" (the canton's integration funding and its refugee support system, named in `out_of_scope`) | `zh-iazh-accredited-offers` for `CH-ZH` | `OUT_OF_COVERAGE`, `concept_not_published` |
| DECLINE-11 | "How much duty do I pay per kilo on a leather handbag from Italy, and what is its tariff number?" (tariff numbers and duty rates per product, named in `out_of_scope`) | `customs-tariff-rate`, a guessed concept ID, for `CH` | `OUT_OF_COVERAGE`, `concept_not_published` listing the published concept IDs; the customs concepts stay available for the rules they do publish |
| DECLINE-12 | "Which insurer is cheapest for me at 8006 Zurich with a 2,500-franc franchise?" (premium amounts and the comparison calculator, named in `out_of_scope`) | `health-insurance-premium` and `premium-calculator`, guessed concept IDs, for `CH-ZH-261` | `OUT_OF_COVERAGE`, `concept_not_published` for both; the health-insurance concepts stay available for the rules they do publish |
| DECLINE-13 | "Wie viel Arbeitslosengeld bekomme ich pro Monat bei einem Lohn von 7'000 Franken?" (the amount of a daily allowance, named in `out_of_scope`) | `unemployment-daily-allowance-amount` and `unemployment-calculator`, guessed concept IDs, for `CH-ZH` | `OUT_OF_COVERAGE`, `concept_not_published` for both; the unemployment concepts stay available for the rules they do publish |
| DECLINE-14 | "Wie hoch wird meine AHV-Rente sein, wenn ich mit 65 aufhöre?" (a pension amount and an individual calculation, named in `out_of_scope`) | `ahv-pension-amount` and `ahv-pension-calculator`, guessed concept IDs, for `CH-ZH` | `OUT_OF_COVERAGE`, `concept_not_published` for both; the AHV concepts stay available for the rules they do publish |

DECLINE-3, DECLINE-4 and DECLINE-6 to DECLINE-9 check the rejection of a
Zurich concept for another place at the server alone. The cross-jurisdiction
cases (UAT-35 to UAT-44) check the same rejections together with what is
still served for the user's place, and judge the live answer on both.

Two further rejections are covered elsewhere: an unreviewed fact requested
with `reviewed_only` (`review_status_not_met`) by the runtime tests and by
the Wallisellen probe W-PROBE-7, and a request whose `as_of` lies after the
freshness window (`STALE`) by the round-trip check.

## Cross-cutting edge cases (offline, in the round-trip check)

| ID | Case | Expected |
| --- | --- | --- |
| X1 | Question outside the topics (housing and rent, schooling) | The coverage root's `out_of_scope` names it; the assistant follows `out_of_scope_response` and makes no further call. A `search` for it reports `match_strength` `weak` or `none` and carries the scope statement (SEARCH-DECLINE-1 to 5). An example that becomes a topic is replaced by one the release does not cover |
| X2 | Question about another country (Germany, Austria) | `jurisdiction_not_covered` with published value `CH`; declined by name. Also DECLINE-2 |
| X3 | Unknown concept ID in a resolve | `concept_not_published` gap listing the published IDs; the other concepts of the same call are unaffected |
| X4 | Unknown context field | `context_not_covered` naming the known fields |
| X5 | A fact ID passed to `get_evidence` | The fact's evidence is returned; an unknown ID is an `INVALID_ARGUMENT` error |
| X6 | Malformed request (unknown field, empty list, six evidence IDs) | `INVALID_ARGUMENT` with the field path; nothing is served |
| X7 | Unknown release ID | `RELEASE_UNAVAILABLE` naming the active release |
| X8 | Coverage root size | Under 8.7 KB, so one call suffices to refuse an outside question. Raised from 6 KB to 8 KB on 23 September 2026, when the two committed bounds were found drifted apart at 6,144 and 8,000 and the four waves of 22-23 September had taken the root to 7,640 bytes; raised again to 8.5 KB the same day, when disclosing registration coverage for all 26 cantons in the manifest took the root to 8,317; raised to 8.7 KB on 25 September 2026, when the school holidays of 23 cantons took it to 8,592 |

## Execution records

On release `mvp-zurich-2026-09-15-v2` every case has three graded live
runs (UAT-8 four) through OpenCode with the model
`opencode/ling-3.0-flash-fin-free`
(record `.local/experiments/2026-09-15-opencode-kb1-extension-acceptance.md`);
the runs have not been repeated on a later release:
the trap held in 50 of 52 sessions; every criterion was met in 8 (UAT-12
three times, UAT-11 twice, UAT-9, UAT-14 and UAT-15 once); 38 sessions
added a specific no tool result supports (A1, A3); 32 exceeded the call or
byte budget (A6), on the release side because a `resolve` of the added
concepts returns up to 28 KB and on the caller side because the older
cases still explore (UAT-7 in dialect: 15 calls at the median); two answers
to UAT-17 were in Portuguese and one to UAT-7 not in German (A8); UAT-13
twice missed the single-attempt rule because the caller never resolved
`zh-control-drive` (A7). UAT-1's turn-2 deadlines were right in all six
scenarios. The grades are in `releases/mvp-zurich/acceptance-answers.json`;
the suite's `answer_check` stays `advisory`.

Edge cases 1e, 1g, 1h, 1j, 1k, 1l, 2a, 2b, the search step of 2e, the search steps
of UAT-7 in English, Standard German and Zurich German, the German search
steps 4f and 6e and the cross-cutting cases X2 to X8 are exercised by the
offline round-trip check on every change. These search checks use default
lexical retrieval; optional hybrid results are recorded separately. The
`accept` stage of the build replays UAT-1 to UAT-44, DECLINE-1 to
DECLINE-9 and SEARCH-DECLINE-1 to SEARCH-DECLINE-7 as the cases of
`releases/mvp-zurich/acceptance.yaml` (the recorded resolve requests, the
planned requests and variation steps of UAT-8 to UAT-17, the planned
requests of UAT-18 to UAT-44, the German search
queries of 2e, UAT-7, UAT-11, UAT-17, UAT-22, UAT-23, UAT-29, UAT-31, UAT-37, UAT-40 and UAT-44, and the claims of the expected
answers the served facts must state; format in
[acceptance-gate.md](https://github.com/swisstip/swiss-tip/blob/main/docs/architecture/acceptance-gate.md)), and the OpenCode
harness runs the same cases' questions through a live model with the
patterns and criteria of their `answer` blocks. 2e and UAT-7 have recorded runs; 1c to 1f, 1i, 1l, 1m, 2c, 2d, 2f, 2g, 2h, X1 and the remaining edge
cases of UAT-3 to UAT-7 are specified here and not yet part of a recorded
run. The decline cases have no live run by design.
