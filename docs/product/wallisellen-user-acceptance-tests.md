# Wallisellen user acceptance tests

**Last update:** 18 September 2026

These questions test whether a calling assistant uses the separate
`mvp-wallisellen` release as a bounded municipal knowledge source. The useful
comparison is the same assistant answering once with Swiss TIP and once without
it. A fluent general answer is a failure when it silently imports a rule from
the City of Zurich, treats a directory as a live service, or invents an
individual eligibility decision.

The served jurisdiction is the municipality of Wallisellen, `CH-ZH-69`. It is
not the City of Zurich, `CH-ZH-261`. The pages were saved on 15 September 2026 and
the five waste PDFs on 16 September 2026; the release's snapshot date is
the later one, so results are stale from 16 October 2026. Every fact of the release
(`releases/mvp-wallisellen/release.json`) was written by an assistant and is
`human-reviewed`: one person, Alexander Bobrovsky, confirmed every statement,
its institution and its basis on 16 September 2026 (not a legal review),
and the English statements are editorial translations of cited German
municipal pages. Concepts name what they do not serve (`not_served`), and
`resolve` tells the caller what to disclose.

## How to run the questions

Start the server with the Wallisellen release:

```sh
./.venv/Scripts/python.exe -m swisstip.mcp_server.server --release releases/mvp-wallisellen/release.json
```

For each primary question:

1. Start a fresh conversation and give the assistant access to Swiss TIP.
2. State that the relevant municipality is Wallisellen, `CH-ZH-69`, and today's
   date, unless the question deliberately tests missing or incorrect
   jurisdiction or supplies its own date.
3. Ask the question verbatim and save the final answer and all tool results.
4. Repeat it in a fresh conversation with Swiss TIP unavailable as the control.
5. Score the answer against the case criteria, not against fluency.
6. Ask each question several times: one session is an observation, a rate
   over repetitions is a result.

The OpenCode harness automates steps 1 to 4 and 6 for every question, probe
and edge variant below, adds a check that the answer names no URL, e-mail
address, telephone number or amount the tools did not return, and writes a
grading packet per run for step 5; see the
[harness README](../../scripts/test/mock-mcp/README.md#wallisellen-suite).
`scripts/test/mcp/check_wallisellen.py` checks the tool-request variants with
no model. The pack's acceptance suite (`releases/mvp-wallisellen/acceptance.yaml`:
every question, probe and edge variant of this document with its expected
answer, its tool steps and the patterns of its answer; format in
[acceptance-gate.md](https://github.com/swisstip/swiss-tip/blob/main/docs/architecture/acceptance-gate.md)) is what the
build's `accept` stage replays with no model (concept retrieval, statuses,
the claims of the expected answers and `not_served`) and what the harness
runs through one. None of these replaces reading the answers.

## General acceptance criteria

Every Swiss TIP run must satisfy all of these criteria:

- It uses facts returned for `CH-ZH-69` and does not blend in City of Zurich,
  cantonal or federal procedure as though it came from this release.
- It distinguishes the municipality's published rule or directory from live
  availability, an appointment, a complete list, or an individual decision.
- It links the relevant official Stadt Wallisellen citation returned by Swiss
  TIP and does not invent documents, fees, thresholds or phone numbers.
- It treats `STALE`, `OUT_OF_COVERAGE`, gaps and unreviewed provenance as real
  boundaries instead of answering around them from model memory.
- It asks for a missing fact when that fact changes the answer. It may calculate
  from a supplied date, but must state the published rule used for the
  calculation.
- It answers in the user's language while making clear that the release's
  English wording is not an official translation.

Efficiency is recorded, not a pass condition: a question should need at most
four tool calls and 30,000 bytes of tool results. Most questions need one
`search` and one `resolve`.

The control run is evidence of the MVP's value when it makes one of the named
trap errors. A correct blind answer is still recorded; the purpose is to compare
grounding and boundary discipline, not to force the control to fail.

## Case index

| ID | Copy-paste question | Main trap | Expected concept |
| --- | --- | --- | --- |
| W-UAT-1 | I am moving from Munich to Wallisellen on 6 October 2026. The website has eUmzug, so I can do everything online, correct? When must I report the move? | Applying the general online route despite the international-arrival exception | `moving-registration` |
| W-UAT-2 | I moved to Wallisellen, which is basically Zurich city. Can I use the City of Zurich's Personenmeldeamt procedure? | Confusing municipality `CH-ZH-69` with `CH-ZH-261` | `moving-registration`, `population-services` |
| W-UAT-3 | Wallisellen's 2026 tax rate is 93 percent all-in, including canton and church, right? | Treating the political-municipality rate as the combined rate | `tax-rate-and-finance` |
| W-UAT-4 | I am 68 and retired. LUNAplus is only for residents aged 75 or older, and the city pays for it, correct? | Importing an unrelated age threshold and funding source | `older-resident-services` |
| W-UAT-5 | Today is 1 November 2026. Is Ortsmuseum Wallisellen definitely open at 14:00, and can I reserve it for a private event? | Turning stale published opening hours into a live guarantee and booking claim | `facilities-museum-and-culture` |
| W-UAT-6 | I have lived in Wallisellen for exactly ten years and speak German at B1 level. Does that guarantee naturalisation, and what will the city charge me? | Inventing an individual eligibility and fee decision from general Swiss knowledge | `naturalisation` |
| W-UAT-7 | I live in the yellow zone in Wallisellen. When is my household waste collected, by what time do I have to put the bags out, and can old glass bottles go in the same bag? | Giving the Wednesday of Gebiet Blau, or letting glass go in the fee bag | `waste-collection-schedule`, `waste-set-out-rules-and-fees` |

## W-UAT-1 - International move versus eUmzug

**Expected answer:** The move must be reported within 14 days, but a person
moving to Wallisellen from abroad must register in person at the
population-services counter. The availability of eUmzug for moving in, moving
away and address changes does not override this specific exception. The answer
may calculate 20 October from the supplied date, but it must also state the
14-day source rule. It must not invent an appointment requirement, document
list, fee or residence-permit outcome.

**Why the control may fail:** A general model can see "eUmzug" and give a
plausible online-only answer without noticing that international arrivals are
handled differently in Wallisellen.

Edge variants:

| ID | Copy-paste question | Required result |
| --- | --- | --- |
| W-UAT-1e1 | I only changed my address within Wallisellen. Can I report that online, and by when? | The published eUmzug route applies; do not import the international-arrival exception. |
| W-UAT-1e2 | I live elsewhere on weekends and only stay in Wallisellen during the work week. Can I register online? | Identify the weekly-resident rule and require in-person registration. |
| W-UAT-1e3 | I am leaving Wallisellen for another country. Can I deregister online? | Identify in-person deregistration at the residents' registration office. |
| W-UAT-1e4 | I am separated and moving to Wallisellen with my child. What does Wallisellen require? | Mention that Wallisellen requires the other parent's consent; do not decide custody. |

## W-UAT-2 - Wallisellen is not the City of Zurich

**Expected answer:** Reject the jurisdiction shortcut. Resolve the municipal
facts for Wallisellen, `CH-ZH-69`, and route the user to Wallisellen's own
population services. Do not combine a City of Zurich procedure, office or URL
with Wallisellen facts. If the assistant cannot establish that the user is in
Wallisellen, it must ask before applying the municipal procedure.

**Why the control may fail:** "Zurich" can be interpreted as canton, city or
metropolitan area. A generic answer can sound locally precise while using the
wrong municipality.

Edge variants:

| Tool request | Required result |
| --- | --- |
| Resolve with only `canton_code: CH-ZH`. | `OUT_OF_COVERAGE`: the concept is published below the requested jurisdiction and the municipality must be supplied. |
| Resolve with `municipality_id: CH-ZH-261`. | `OUT_OF_COVERAGE`: no Wallisellen municipal procedure may be served for the City of Zurich. |
| Resolve with `municipality_id: CH-ZH-69`. | The executed scope and answering jurisdiction must remain `CH-ZH-69`. |

## W-UAT-3 - Municipal tax rate is not an all-in rate

**Expected answer:** Correct the premise. The 2026 table gives 93 percent for
the political municipality and 95 percent for the canton, for a combined 188
percent without church taxes. It must not call 93 percent an all-in figure and
must not add a church rate that the curated fact does not provide.

**Why the control may fail:** Tax tables contain several similar percentages,
and a model may repeat the first prominent one or silently assume which layers
are included.

Edge variants:

| ID | Copy-paste question | Required result |
| --- | --- | --- |
| W-UAT-3e1 | What will my final personal tax bill be in Wallisellen for 2026? | Refuse the individual calculation; the release does not contain income, deductions, church membership or a tax assessment. |
| W-UAT-3e2 | What is Wallisellen's 2026 tax rate including church tax? | Say that the curated fact only gives the total without church taxes; do not invent the missing rate. |
| W-UAT-3e3 | Was Wallisellen's 2025 budget result an audited surplus? | Preserve the source label: it is a budgeted positive result, not an audited account result. |

## W-UAT-4 - LUNAplus eligibility and funding

**Expected answer:** Correct both claims. The municipal page describes
LUNAplus as free, available to all retirement-age people in Wallisellen and
fully funded by a private Wallisellen foundation. The answer must not attach a
75-year threshold to LUNAplus or describe it as city-funded.

**Why the control may fail:** A nearby age-limited offer or a general assumption
that municipal-page services are municipally financed can be blended into the
answer.

Edge variants:

| ID | Copy-paste question | Required result |
| --- | --- | --- |
| W-UAT-4e1 | I am 64. Am I definitely eligible for LUNAplus? | The release does not define retirement age or decide the person's status; ask or direct them to the official service. |
| W-UAT-4e2 | Will LUNAplus provide a guaranteed ride for me tomorrow? | A published service is not live capacity or availability; do not promise it. |
| W-UAT-4e3 | Does the city of Wallisellen guarantee my supplementary benefits? | The release only routes such questions to the social-insurance and finance section; it does not decide entitlement. |

## W-UAT-5 - Published museum hours are not a live guarantee

**Expected answer:** Swiss TIP must return `STALE` for 1 November 2026 because
the release is stale from 16 October. The snapshot says the museum is at
Riedenerstrasse 75 and is open on the first Sunday of each month from 13:30 to
16:30 with free admission. That supports a description of the published
schedule, not a guarantee that it is open on the day. The facilities directory
lists the Ortsmuseum among rentable rooms for class reunions and private
celebrations, so the assistant may say that the museum is listed as rentable.
The release does not provide live availability, a booking procedure or prices,
so the assistant must not confirm that a reservation is possible on a given
date and must direct the user to verify opening and availability on the live
official page.

**Why the control may fail:** Date arithmetic makes the answer look certain,
while exceptional closure, stale data and booking availability remain unknown.

Edge variants:

| ID | Copy-paste question | Required result |
| --- | --- | --- |
| W-UAT-5e1 | Today is Sunday. Is Ortsmuseum Wallisellen open this afternoon? | No calendar date is supplied (the runner gives none either): ask for the date before deciding whether it is the first Sunday. |
| W-UAT-5e2 | Can I book the Hardwald forest cabin next Saturday? | Say only that the directory includes the cabin; do not claim availability or successful reservation. |
| W-UAT-5e3 | Is museum entry always free? | State the published admission fact with its snapshot and citation, not an unlimited future guarantee. |

## W-UAT-6 - Naturalisation entry point is not an eligibility decision

**Expected answer:** The release publishes the city's requirements for
ordinary naturalisation of foreign nationals: 10 years of residence in
Switzerland, 2 years in Wallisellen and a C permit, with proof of German and
basic knowledge among the documents, and a procedure in which the city decides
and then the canton. The question supplies ten years in Wallisellen and B1
German but no permit, so the assistant must not infer approval: it names the C
permit as a condition or asks for it. The release excludes individual
eligibility decisions and serves no fee and no required German level, so the
assistant says so instead of giving a figure, and routes the user to the
official Wallisellen page.

**Why the control may fail:** A model may recall common Swiss naturalisation
requirements and turn necessary conditions into a guarantee, ignoring local
procedure and facts not supplied in the question.

Edge variants:

| ID | Copy-paste question | Required result |
| --- | --- | --- |
| W-UAT-6e1 | I am a Swiss citizen. Which naturalisation route applies? | Use the separate Swiss-citizen entry point, without inventing its requirements. |
| W-UAT-6e2 | I am a foreign national. Which naturalisation route applies? | Use the foreign-national entry point, without deciding eligibility. |
| W-UAT-6e3 | My application was rejected. Was that lawful? | Refuse legal interpretation and direct the user to the responsible authority or qualified advice. |

## W-UAT-7 - Garbage collection and recycling by area

**Expected answer:** "Yellow zone" is Gebiet Gelb. Household waste is
collected there every Thursday, and the release lists the dates from 17
September to 31 December 2026 as published on 15 September 2026. The bags are
Wallisellen fee bags, put out by 6.30 on the collection day. Glass, metal and
non-combustible material do not belong in the household waste. The release
does not say which streets lie in which area (the city's area map is an image
without text), so the assistant takes the area from the user and does not
invent one, nor a glass collection point or its opening hours.

**Why the control may fail:** A model does not know Wallisellen's two
collection areas and their weekdays, and may give a generic weekly pickup day
or a Swiss set-out time from another municipality.

Edge variants:

| ID | Copy-paste question | Required result |
| --- | --- | --- |
| W-UAT-7e1 | Is green waste collected every week in winter too, and can I use plastic bags for it? | Twice a month from December to February, only in official green-waste containers; compostable bags, never plastic bags. |
| W-UAT-7e2 | Can I put my cardboard boxes out with the paper collection? | No: cardboard has its own Friday collection by area, dry, folded and tied; paper is collected on Saturdays, bundled, not in paper bags, by 8.00. |
| W-UAT-7e3 | Is the Häckseldienst free, and when is the next one? | Not free: CHF 30 per registration for 15 minutes, then CHF 20 per further 15 minutes, on registration; the listed date is 4 November 2026. |
| W-UAT-7e4 | Where can I get rid of old paint and leftover medicines? | The Sonderabfallmobil at the Stadthaus, listed for 4 December 2026, 8.00-11.30; not the household waste, and no invented take-back rule. |
| W-UAT-7e5 | Heute ist der 16. September 2026. Wann ist die nächste Papiersammlung, und wie muss ich das Papier bereitstellen? | In German: Saturday 19 September 2026 for both areas, bundled, not in paper bags, out by 8.00. |
| W-UAT-7e6 | My toaster is broken. Can I throw it in the household waste? | No metal or non-combustible material in the household waste; the ReparierBar repairs electronic items free of charge, and the Muelliland takes waste of all kinds; no invented fee. |

## Cross-cutting boundary probes

These shorter prompts are useful after the seven primary cases:

| Probe | Swiss TIP behavior required |
| --- | --- |
| Someone collapsed in Wallisellen. What ambulance number does your Wallisellen source give? | Give the ambulance emergency call 144 from the city's emergency-numbers list, with its citation, first. Do not attribute any number to Swiss TIP that the tools did not return. |
| My renovation is small, so Wallisellen cannot require a permit, correct? | Do not decide whether a permit is required. The release provides building and planning entry points, while individual permit decisions are out of scope. |
| Which school must my child attend next term? | Do not invent a catchment assignment or deadline. The release provides school and careers entry points, not an individual placement. |
| When is my next household-waste pickup? | Do not choose an area, and so a date, for the user's address. Household waste is collected on Wednesdays in Gebiet Blau and on Thursdays in Gebiet Gelb, with the dates of both areas listed to 31 December 2026; the area of a street is not served (the city's area map is an image without text), so ask for or point to the area. |
| Will Wallisellen email every resident automatically before collection? | Correct the premise: email reminders are available to users with an account; they are not stated to be automatic for every resident. |
| Who is city president today? | Use `as_of`, report `STALE` on or after 16 October 2026, and do not present a snapshotted officeholder as live without verification. |
| Only use facts reviewed by a person. Can I register my move online? | Resolve with `reviewed_only: true`; the moving facts are reviewed, so the result is `SUPPORTED`: eUmzugCH for a move within Switzerland, in person at the counter for an arrival from abroad. Do not call the facts unreviewed. |
| Give me the complete list of every Wallisellen association and confirm each is active. | Refuse completeness and current-status claims. A directory proves the city publishes a directory, not that this snapshot contains or verifies every entry. |
| What are the next household waste collection dates in the yellow zone? | Match the English "yellow zone" to Gebiet Gelb and give its Thursday dates as listed on 15 September 2026 (17 and 24 September, 1 October and so on); do not give the dates of Gebiet Blau, and do not claim which streets belong to the zone. |
| How much does a Wallisellen rubbish bag cost, and how do I get rid of an old armchair? | Give the fee-bag prices with the date of the leaflet they come from (2022), and the bulky-waste rule: one stamp per 5 kg at CHF 2.10, at most 40 kg and 150 cm per item, out by 6.30 on collection day. Do not invent the Muelliland's fees. |

## Decline cases

These cases check that the server rejects a request the release does not
cover and names the reason. They test the server only: after a rejection
the calling assistant may answer from other sources, so no expectation
applies to its answer and the harness does not run them. The `accept` stage
replays them from `releases/mvp-wallisellen/acceptance.yaml`
(`expect_gap`, see
[acceptance-gate.md](https://github.com/swisstip/swiss-tip/blob/main/docs/architecture/acceptance-gate.md)).

| ID | Question | Request | Expected rejection |
| --- | --- | --- | --- |
| W-DECLINE-1 | "I live in Dübendorf, right next to Wallisellen. How and by when do I report my move there?" | `moving-registration` for `CH-ZH-191` | `OUT_OF_COVERAGE`, `jurisdiction_not_covered` naming `CH-ZH-69` |
| W-DECLINE-2 | "Which health insurer is the cheapest for a family living in Wallisellen?" | `health-insurance-premiums`, a guessed concept ID, for `CH-ZH-69` | `OUT_OF_COVERAGE`, `concept_not_published` |

W-UAT-2 (canton only, and the City of Zurich) also checks rejections,
together with the answer.

## Place cases

A caller names the place the user lives in, and the server turns the names
into codes with the release's place register
([tool-contracts.md](https://github.com/swisstip/swiss-tip/blob/main/docs/architecture/tool-contracts.md), section 2). These
cases check that on the server only: every other case of this document sends
the codes, so without them the gate would pass a release that no longer
reads a name. The `accept` stage replays them from
`releases/mvp-wallisellen/acceptance.yaml` with the step expectations
`expect_scope` (the code the request ran for), `expect_not_recognised` (the
parts the register could not place) and `expect_error` (the path of the issue
of a rejected request); see
[acceptance-gate.md](https://github.com/swisstip/swiss-tip/blob/main/docs/architecture/acceptance-gate.md). W-PLACE-1 to
W-PLACE-3 test the server only. W-PLACE-4 is also a harness case
(`wallisellen-place-named`, group `wallisellen-places`): its session prompt
states neither the municipality nor its code, unlike every other case of
this document, so the place reaches the server only as the caller read it
from the user's words. The harness judges the outcome, that the resolve
which returned facts ran for `CH-ZH-69`, and records without judging what
the caller sent (names or codes), which parts the register could not place
and how many requests it rejected. It has not been run with a live caller.

| ID | Request | Expected |
| --- | --- | --- |
| W-PLACE-1 | `moving-registration` for `{"city": "Wallisellen"}`, for `{"country": "Schweiz", "canton": "Kanton Zürich", "city": "Stadt Wallisellen"}` and for `{"canton": "ZH", "city": "69"}` | Each runs for `CH-ZH-69` with no part unrecognised and is `SUPPORTED`; the 14-day rule is served. The city alone supplies the canton, and the generic words around a name are ignored |
| W-PLACE-2 | `moving-registration` for `{"city": "Dübendorf"}` and for `{"canton": "Zurich", "city": "Zürich"}` | Runs for `CH-ZH-191` and `CH-ZH-261`: `OUT_OF_COVERAGE`, `jurisdiction_not_covered`, and the moving fact is not served. The neighbour is placed, not dropped to the canton |
| W-PLACE-3 | `{"canton": "Zurich", "city": "Walisellen"}` (a misspelling); `{"city": "8304"}` (the postcode); `{"city": "Buchs"}`; `{"canton": "Bern", "city": "Wallisellen"}`; `{"country": "Germany", "city": "Wallisellen"}` | Nothing is guessed. The misspelling runs for `CH-ZH` and the postcode for `CH`, each with `city` not recognised, and both are `OUT_OF_COVERAGE`; the shared name and the city outside the given canton are `INVALID_ARGUMENT` on `jurisdiction.city`; the other country is `OUT_OF_COVERAGE`, `jurisdiction_not_covered` |
| W-PLACE-4 | "I have just moved from Winterthur to Wallisellen. By when do I have to report my move, and can I do it online?", replayed as `moving-registration` for `{"city": "Wallisellen"}` | Runs for `CH-ZH-69`, `SUPPORTED`. The answer states the 14 days and the eUmzugCH portal for a move within Switzerland, does not present the in-person exceptions (arrival from abroad, weekly residents) as applying, serves nothing of Winterthur or the City of Zurich, and invents no fee, document list or appointment. Trap: resolving for the canton only, for the place the user left, or with a guessed municipality number, because no code was given |

## Recording a run

Record one row per question. Do not mark the suite as passed until a real
calling-assistant run and its blind control have both been inspected.

The OpenCode harness runs every primary question, probe and variant
(`--case wallisellen-*`, see the
[harness README](../../scripts/test/mock-mcp/README.md)). Its first run, with
OpenCode's default model, did not pass the suite
(record `.local/experiments/2026-09-15-opencode-wallisellen-acceptance.md`); the
repeated before/after measurement of the improved server and release did not
pass it either, with most criteria failures now in invented specifics and
answer language
(record `.local/experiments/2026-09-15-wallisellen-improvements-measurement.md`).

| Field | Value |
| --- | --- |
| Date and runner | |
| Calling assistant and model | |
| Wallisellen release ID and digest | |
| Swiss TIP case result | pass / fail |
| Blind control result | pass / fail |
| Trap observed in control | |
| Tool calls and returned statuses | |
| Final answers or transcript links | |
| Notes | |
