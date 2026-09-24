# Datasets

**Last update:** 24 September 2026

Each folder is one pack's datasets: tables a municipality publishes as open
data, served next to the pack's release by a dataset connector (a separate
container) behind a concept the release publishes. The facts give the rule,
the dataset gives the instance: the next collection day of organic waste for
a postal code, or for a collection zone where the city publishes its dates by zone. Design, contract and status are in the code repository's
[docs/architecture/dataset-connectors.md](https://github.com/swisstip/swiss-tip/blob/main/docs/architecture/dataset-connectors.md).

| Pack | Datasets | Source | Status |
| --- | --- | --- | --- |
| `mvp-zurich/` | The five waste-collection calendars of the City of Zurich for 2026: organic waste, paper and cardboard (behind `city-zurich-organic-paper-cardboard`), household waste (`city-zurich-household-waste`) and the stops of the hazardous-waste van (`city-zurich-hazardous-waste`), by postal code | [Open Data Zürich](https://data.stadt-zuerich.ch/), datasets `entsorgungskalender_*`, published by Entsorgung + Recycling Zürich under CC0, one CSV per year | Built on 23 September 2026 from the files as published that day; the calendar image `swiss-tip-calendar:mvp-zurich` was built, tested and pushed the same day on the 0.3.0rc4 rehearsal and registered its five datasets beside the slim image; the lookup cases are in the acceptance suite (LOOKUP-1 to 3) |
| `mvp-zurich/` | The collection calendars of the City of Basel for 2026 - household waste, paper and cardboard, green waste, metal, bulky waste, non-combustibles (`basel-waste-*`, behind `city-basel-waste-collection`) - and of the City of St. Gallen to June 2027 - household waste, paper, cardboard, green waste (`st-gallen-waste-*`, behind `city-st-gallen-waste-collection`), by collection zone | Open Data Basel-Stadt, dataset 100096 (Tiefbauamt, CC BY 4.0); Open Data St. Gallen, dataset `abfuhrdaten-stadt-stgallen-calendar-data` (Entsorgung St.Gallen, CC BY 4.0); each source is the portal's CSV export filtered to one waste type from 2026-01-01 | Built on 24 September 2026; keyed by zone (Basel A-H and GUF, St. Gallen A-K, L Ost, L West) with the city's zone finder in the manifest; lookup cases LOOKUP-4 to 6 in the acceptance suite |

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

## Acceptance cases

The acceptance suite of `mvp-zurich` holds the lookup cases LOOKUP-1 to 6:
the next organic-waste date in 8001, a postal code outside Zurich, January
2027 before its file exists, the next household-waste date in Basel zone B,
the next paper date in St. Gallen area "l-west" spelled loosely, and a zone
Basel does not have. The knowledge builder's `accept` stage takes no
connector, so it records their lookup steps as not judged; replayed with
`swisstip.runtime.acceptance` against the connector serving this folder,
all six pass (24 September 2026).

## A dataset keyed by zone

A city that publishes its dates by collection zone, not by postal code,
names the zone column in the importer (`zone: <column>` instead of
`postal_code:`) and the page where a resident finds their zone
(`zone_lookup_url`). The bundle then lists its zones; `resolve` offers the
dataset with `requires: ["zone"]`, the zones and that page, and `lookup`
takes the zone as the user gives it, ignoring case, spaces, hyphens and a
leading "Zone". Nothing checks that the zone is the one of the user's
address: that is the user's statement, and every bundle says so.
