# Swiss TIP - MVP knowledge bases

The knowledge bases of the Swiss TIP MVP: curated packs of facts about Swiss
public information, each fact tied to an exact excerpt of an official page,
with its URL, access date and hashes, and reviewed by a person before release.

This repository holds the **data of the MVP** - a first, deliberately narrow
set of packs, not every knowledge base the server could serve. The server
itself is knowledge-base agnostic; it and the pipeline that builds these packs
are in [swiss-tip](https://github.com/swisstip/swiss-tip).

## The first pack: mvp-zurich

Someone moving to Zurich deals with three levels of government at once, and
no single official site covers all three. Whether you may bring your spouse
is federal law. Which office you register at, and by when, is cantonal. Which
bag your rubbish goes in, and what the school day looks like, is municipal.
The pages that answer these questions are authoritative, but they are
scattered across dozens of sites, mostly in German, and written for people
who already know which authority they belong to.

`mvp-zurich` is one pack that answers across all three levels - federal
rules, the Canton of Zurich and the City of Zurich - for a foreign national
living in Zurich. It is built, reviewed and served.

### Current coverage

**Release `mvp-zurich-2026-09-24-v1`:** 20 topics, 212 concepts and **1,273
facts, all reviewed by one named person**, cited to 1,531 excerpts (1,363
German, 114 English, 43 French, 11 Italian) across 336 official documents.
Source snapshot 23 September 2026, stale from 22 November 2026. Jurisdictions:
federal rules and arrival registration for all 26 cantons, the full procedures
of the Canton of Zurich and the City of Zurich, and waste hand-over in the City
of Lugano. The full, current account - what is served and what is not - is in
[COVERAGE.md](COVERAGE.md); the running server reports it live through
`get_coverage` and `/health`.

### Topics

| | |
| --- | --- |
| Residence permits and registration | Cantonal migration offices |
| Zurich office contacts | First steps and life in the City of Zurich |
| Waste and recycling (City of Zurich) and Lugano hand-over | Parking, vehicles and moving goods |
| Tax return and household fees | AHV, the pillar system and retirement |
| Social insurance and pillar 3a | Losing a job, the RAV and unemployment insurance |
| Tax at source | Foreign driving licence |
| Health and accident insurance | Naturalisation |
| Entry and visas | Voting rights |
| Family allowances and parental leave | Renting a home |
| Customs: travelling, ordering from abroad, moving goods | Integration offers and German courses |

### Example concepts

A topic is a heading; a concept is one question a person actually asks, with
the facts that answer it. Some of the concepts these topics carry:

- **Residence permits and registration** - who issues a permit; registration
  deadlines; short-stay, residence and settlement permits; family reunification.
- **Entry and visas** - who needs a visa; Schengen type C against national
  type D; how long a short stay may last; where to apply and what it costs.
- **Tax at source** - when liability starts and ends; tariff codes; when an
  ordinary assessment follows instead.
- **Naturalisation** - ordinary and facilitated routes, and how the federal,
  cantonal and municipal conditions stack on top of each other.
- **Waste and recycling** - which bag, which collection day, where the
  recycling centres are, what to do with bulky and hazardous waste.
- **Renting a home** - what belongs in a tenancy agreement; deposit,
  subletting and termination; rent increases and the reference interest rate.

### Sources

Only official publishers, at the level that actually owns the rule:

| Level | Publishers |
| --- | --- |
| Federal | State Secretariat for Migration; Fedlex, the federal law collection; ch.ch; Federal Office of Public Health; Federal Office for Customs and Border Security; SECO; Federal Tax Administration; Federal Social Insurance Office; Central Compensation Office; Federal Office for Housing; Federal Department of Foreign Affairs; SERAFE |
| Cantonal | Canton of Zurich: Migration Office, Cantonal Tax Office, Road Traffic Office, Health Directorate, Office for the Economy, Veterinary Office, Naturalisation Division, tenancy forms, Statistical Office; SVA Zürich |
| Municipal | City of Zurich: Population Office, Civil Registry Office, Tax Office, School Office, Traffic Department, Waste Disposal and Recycling (ERZ), Naturalisation Division, City Police, Protection and Rescue |

### What would make a fact usable

Every fact should carry what an assistant needs in order to answer
responsibly rather than plausibly:

- **An exact excerpt** of the official page it came from, with the URL, the
  date it was retrieved and content hashes - not a summary of the page.
- **Its basis**: whether the excerpt is a federal act and article, an
  ordinance, the free-movement agreement, a cantonal directive, an
  authority's guidance or a portal summary. A statute and a FAQ are both
  useful, and they are not the same thing.
- **Jurisdiction and validity**, so a rule for one canton is never served for
  another, and an expired one is marked rather than quietly returned.
- **Human review** before release, with the release bound to a content hash.

And when a question falls outside the pack, the server should say so by name
instead of guessing. The absence of an answer is itself an answer.

## Repository

| Path | Contents |
| --- | --- |
| `config/places/` | The Swiss place register: the country, the 26 cantons and every municipality with their codes, official names and accepted aliases, embedded in every release so that a caller's place resolves to the jurisdiction a fact is published for |
| `releases/<pack>/` | One pack: `sources.json` (the source catalogue), `curation.yaml` (the facts a curator writes), `release.json` (the built, hashed release), `readiness.json` (its attestation), `semantic-index.json`, the acceptance and regression suites with their reports, and the pack's README |
| `scripts/test/` | The checks of the packs: suites, reports, readiness records, catalogues, round trips against the served release, the regression runner and the OpenCode harness |
| `docker/` | The pack images and the demo image; the generic images they build on are in the code repository |
| `deploy/aws/` | One CloudFormation template that hosts the two-container setup on an EC2 instance behind HTTPS |
| `docs/` | The acceptance-test documents of the packs, the related work, and the hackathon pitch |

A pack is built, reviewed and served with the tools of the code repository:
the knowledge builder and the admin console take this checkout as their
packs directory, and the server takes a pack's `release.json`. The pack
files are written by those tools and attested; they are never edited by hand.
Contributor conventions are in [AGENTS.md](AGENTS.md).

## The hackathon

Built for the **Swiss {ai} Weeks** hackathon in Zurich, 24 and 25 September
2026, for the challenge **Swiss Grounding MCP**, set by Swisscom's myAI team:

<https://zh.ai-weeks.ch/challenges/swiss-grounding-mcp>

## Status

- **The submission — served and reviewed:** `mvp-zurich`, release
  `mvp-zurich-2026-09-24-v1`, the pack described above: 20 topics, 212
  concepts, 1,273 facts, every fact reviewed by one named person, with an
  attested readiness record.
- **Proof of concept — frozen:** `mvp-wallisellen` (99 facts, German), a
  municipal pack whose facts an assistant wrote and one person reviewed;
  it shows the same tooling builds a second pack and is not extended further.
- **Checked:** every push that changes a pack replays its acceptance suite
  and regression pack and runs the round trips against the served release
  ([knowledge-bases.yml](.github/workflows/knowledge-bases.yml)); the
  pack images and the demo image are built, tested and pushed by
  [container-images.yml](.github/workflows/container-images.yml), on the
  images without a release that the code repository's
  [workflow of the same name](https://github.com/swisstip/swiss-tip/blob/main/.github/workflows/container-images.yml)
  pushes.

What the packs cover is in [COVERAGE.md](COVERAGE.md); what is weak or
missing is in [LIMITATIONS.md](LIMITATIONS.md). The facts were reviewed by
one person against the excerpts, which is not a legal review.
