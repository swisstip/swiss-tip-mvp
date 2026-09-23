# Datasets

**Last update:** 23 September 2026

Each folder is one pack's datasets: tables a municipality publishes as open
data, served next to the pack's release by a dataset connector (a separate
container) behind a concept the release publishes. The facts give the rule,
the dataset gives the instance: the next collection day of organic waste for
a postal code. Design, contract and status are in the code repository's
[docs/architecture/dataset-connectors.md](https://github.com/swisstip/swiss-tip/blob/main/docs/architecture/dataset-connectors.md).

| Pack | Datasets | Source | Status |
| --- | --- | --- | --- |
| `mvp-zurich/` | The five waste-collection calendars of the City of Zurich for 2026: organic waste, paper and cardboard (behind `city-zurich-organic-paper-cardboard`), household waste (`city-zurich-household-waste`) and the stops of the hazardous-waste van (`city-zurich-hazardous-waste`), by postal code | [Open Data Zürich](https://data.stadt-zuerich.ch/), datasets `entsorgungskalender_*`, published by Entsorgung + Recycling Zürich under CC0, one CSV per year | Built on 23 September 2026 from the files as published that day; not yet in an image, not yet registered with a published server, no acceptance case yet (see below) |

## Files in a dataset folder

| File | Content |
| --- | --- |
| `dataset.yaml` | What the curator writes (`swiss-tip-dataset-curation/v1`): the binding to the pack and its concept, the publisher, licence and portal page, the source files with the hash, size and download date the first build pinned, the importer with its column mapping, the published period |
| `dataset.json` | The bundle the connector serves (`swiss-tip-dataset/v1`): the manifest with the pins and the content hash, and the normalised rows, one event per row; written by `swisstip-build-dataset`, never edited by hand |
| `build-report.json` | Rows, repeated rows dropped, postal codes and one record per source of the last build |

The downloaded files stay under the Git-ignored `.local/<pack>/datasets/<dataset>/`,
as the saved pages of a release do; the bundle carries their hashes, so a
file is re-downloadable and verifiable. Line endings are pinned by
`.gitattributes` (`datasets/** -text`) like the packs'.

## Build

```shell
./.venv/Scripts/python.exe -m swisstip.build.dataset_cli --packs-dir . --pack mvp-zurich --dataset zurich-waste-bioabfall
```

The build is the one step with network: it downloads a source it does not
find under `.local/`, compares the hash with the pin (or records the pin on
the first build), imports, validates and writes the bundle. A source whose
bytes differ from the pin stops the build; `--refresh` accepts the
publisher's new file, which is how next year's calendar is taken in when
the portal publishes it (December, for the Zurich calendars). Rows are not
reviewed by a person; the pins and the validator are the whole gate, and
every bundle says so in its limitations.

## Serve

```shell
./.venv/Scripts/python.exe -m swisstip.calendar_connector.server --datasets-dir datasets/mvp-zurich
./.venv/Scripts/python.exe -m swisstip.mcp_server.server --release releases/mvp-zurich/release.json --connector http://127.0.0.1:8100
```

The server binds each dataset to its concept at startup and lists the
fifth tool `lookup`; `resolve` on a waste concept for the City of Zurich
then offers the datasets in `lookups`. The image
`swiss-tip-calendar:mvp-zurich` ([docker/mvp-zurich-calendar](../docker/mvp-zurich-calendar/Dockerfile))
carries the bundles on the connector image of the code repository, and the
profile `calendar` of that repository's `compose.yaml` starts it beside
the server.

## Acceptance cases to add

The acceptance suite gains a third step kind, `lookup`, replayed only when
the `accept` stage is given a connector; the knowledge builder does not
take one yet, so a lookup step is recorded as not judged there. The cases
below are ready for the next attestation of `mvp-zurich` and are not in
`acceptance.yaml` yet, because adding them changes the suite's digest and
so the readiness record:

```yaml
- case_id: LOOKUP-1
  label: Next organic waste collection in 8001
  spec: dataset-connectors
  question: When is the next organic waste collection in 8001?
  expected_answer: >-
    The rule of the organic-waste concept, then the next collection day the
    City of Zurich publishes for postal code 8001 on the as-of date, cited to
    the Open Data Zürich dataset page, named as published rows that no
    person reviewed.
  trap: A generic answer guesses a weekday from memory or from the interval between dates.
  steps:
  - search:
      query: When is the next organic waste collection in 8001?
      expect_concept: city-zurich-organic-paper-cardboard
  - resolve:
      concept_ids: [city-zurich-organic-paper-cardboard]
      jurisdiction: {city: Zurich}
      expect_status: {city-zurich-organic-paper-cardboard: SUPPORTED}
  - lookup:
      dataset_id: zurich-waste-bioabfall
      postal_code: '8001'
      as_of: '2026-09-23'
      limit: 1
      expect_status: SUPPORTED
      expect_first_date: '2026-09-28'
- case_id: LOOKUP-2
  label: A postal code outside the city
  spec: dataset-connectors
  question: When is the next organic waste collection in 8304?
  expected_answer: >-
    No date: 8304 is not a postal code the City of Zurich publishes a
    calendar for; the caller says so and derives no date.
  trap: A generic answer serves a Zurich date for a Wallisellen postal code.
  steps:
  - lookup:
      dataset_id: zurich-waste-bioabfall
      postal_code: '8304'
      as_of: '2026-09-23'
      expect_status: OUT_OF_COVERAGE
      expect_gap: postal_code_not_covered
- case_id: LOOKUP-3
  label: Next year before its calendar is published
  spec: dataset-connectors
  question: When is organic waste collected in 8001 in January 2027?
  expected_answer: >-
    Not published yet: the 2026 file ends on 31 December 2026; the caller
    says the publisher has not published that period.
  trap: A generic answer extrapolates the weekly rhythm into next year.
  steps:
  - lookup:
      dataset_id: zurich-waste-bioabfall
      postal_code: '8001'
      as_of: '2026-09-23'
      start: '2027-01-01'
      end: '2027-01-31'
      expect_status: OUT_OF_COVERAGE
      expect_gap: period_not_published
```
