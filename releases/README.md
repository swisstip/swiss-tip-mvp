# Releases

**Last update:** 20 September 2026

Each folder is one knowledge-base pack. A pack
starts as a source catalogue and grows into a served release: the curation
file, the run with the saved snapshots and the text dataset, and the validated
`release.json` are added next to `sources.json` as they are produced. Every
pack keeps its run outside Git under `.local/<pack>/`; a clone holds the
catalogues, curation files, releases and their reports, but not the saved
pages or the text datasets. The steps from the idea to a published release
are in the code repository's
[docs/architecture/knowledge-base-pipeline.md](https://github.com/swisstip/swiss-tip/blob/main/docs/architecture/knowledge-base-pipeline.md).

| Pack | Scope | Sources | Status |
| --- | --- | --- | --- |
| `mvp-zurich/` | KB1, the MVP: federal sources plus Canton of Zurich and City of Zurich; extended on 15 September 2026 with the moving-to-Switzerland topics (social insurance on arrival and departure, tax at source, the foreign driving licence, health insurance and premium reduction) and naturalisation, at the same three levels, on 17 September 2026 with the contact pages of the Zurich offices these topics name, with daily life in the City of Zurich (waste, parking, vehicles, dogs, kindergarten, the tax return, the radio and television fee, medical emergencies) and with entry and visas, and on 18 September 2026 with voting rights, the tax-at-source tariff and the expat-life topics (family allowances and parental leave, renting a home, marriage, leaving the City of Zurich, pillar 3a, unemployment, accident insurance, customs on moving), and on 19 September 2026 with the English versions of 24 cited federal pages (SEM, FOPH, FOCBS, SECO, SERAFE) next to the German ones | 96 (55 federal, 29 cantonal Zurich, 12 municipal): the 35 of the rehearsal, 25 of the topic extension, 8 of the office contacts, 10 of daily life, 2 of entry and visas, 4 of voting rights and 12 of expat life, plus 173 explicit pages in `sources.md` (the extensions' seeds and their subpages, and the English versions) | Catalogue `draft-8`, saved in the local run (519 of 528 targets; five pages answer HTTP 404, and the four Fedlex pages added since 17 September are application shells whose dated documents are saved); the served release `mvp-zurich-2026-09-19-v15` (16 topics, 133 concepts, 601 facts, 800 excerpts of which 114 English, and the place register of all Swiss cantons and municipalities, so that a caller names a place instead of its code) is built and validated, passes its acceptance suite (UAT-1 to UAT-64 and the decline cases) and its regression pack (`regression-report.json`), and carries a rebuilt semantic index; its readiness record is not yet attested (it names v10); every concept has authored everyday aliases and at least one sample question in English and one in German, which the build checks; all 601 facts are reviewed by one person (confirmed in the console, most in bulk groups; the first 253 also read card by card on 15 September), the 114 excerpts added on 19 September are not; the published image and GitHub release are named in the pack's `README.md`; its contents and review status are in [COVERAGE.md](../COVERAGE.md) and [LIMITATIONS.md](../LIMITATIONS.md) |
| `mvp-wallisellen/` | Multi-topic municipal MVP: stable resident-facing information published by Stadt Wallisellen | 10 registry entries and 55 explicit catalogue targets: 50 pages and the five waste PDFs linked from the waste disposal page | All 55 targets saved with no gaps; 54 extracted, the collection-area map PDF has no text layer (no OCR); release `mvp-wallisellen-2026-09-18-v1` (the facts of `mvp-wallisellen-2026-09-16-v3` with the place register added, attested again on 18 September 2026 and, after a change to one answer pattern of its suite, on 19 September 2026) with 99 assistant-authored facts across 30 concepts and 10 topics, including the 2026 collection dates by area, fee bags, bulky-waste stamps and set-out rules; a registry of six city institutions and the basis of every excerpt (76 municipal guidance, 23 municipal directory), assigned by assistant subagents with the pipeline's basis prompt and listed in [basis-review.md](mvp-wallisellen/basis-review.md); every fact, institution and basis confirmed by one person on 16 September 2026, who attested the release; built, thoroughly validated, passing the forty-one cases of its acceptance suite, with a rebuilt semantic index and an attested readiness record; the [acceptance questions](../docs/product/wallisellen-user-acceptance-tests.md) were also run through the OpenCode harness |

## Files in a pack

| File | Content |
| --- | --- |
| `sources.json` | Machine-readable catalogue: scope, planning topics, language policy, scan sets, crawl budgets and one entry per source with start URL, host and path allowlist, authority, jurisdiction, language, discovery reference and scan status |
| `sources.md` | Optional human-readable inventory of explicit catalogue links with notes on scope and acquisition |
| `curation.yaml` | The facts of the pack, each with statement, jurisdiction, condition, validity, provenance and review status, and its citations into the text dataset with anchors; it also names the place files the build embeds (`place_register`, `place_aliases`), which the packs of one country share under [config/places/](../config/places/) |
| `release.json` | The validated, hashed bundle the server serves, built by `swisstip-build-release`; the server has no default pack and takes it with `--release` |
| `semantic-index.json` | Optional prebuilt concept embeddings, bound to the exact release and embedding model digest (`mvp-zurich` and `mvp-wallisellen` have committed indexes; the semantic container images ([docker/README.md](https://github.com/swisstip/swiss-tip/blob/main/docker/README.md) of the code repository) require one) |
| `build-report.json` | Every citation outcome of the last build and every dropped fact |
| `acceptance.yaml` | The acceptance suite: one case per user question of the pack's acceptance-test document, with the expected answer, the trap, the tool requests to replay and the claims the served facts must carry; format in [docs/architecture/acceptance-gate.md](https://github.com/swisstip/swiss-tip/blob/main/docs/architecture/acceptance-gate.md) |
| `acceptance-report.json` | The outcome of the last `accept` stage per case, step and claim, bound to the release's content digest and the suite's digest |
| `regression.yaml` | The regression pack's own cases: plain and declined questions beyond the acceptance-test document, in the suite format, replayed together with `acceptance.yaml`; not a readiness gate (`mvp-zurich` only); section 10 of [docs/architecture/acceptance-gate.md](https://github.com/swisstip/swiss-tip/blob/main/docs/architecture/acceptance-gate.md) |
| `regression-report.json` | The regression pack replayed lexically and with hybrid search by `scripts/test/regression/run_regression.py`, bound to the release's content digest and the digests of both suites |
| `test-cases.md` | Every case of `acceptance.yaml` and `regression.yaml` on one readable page, an overview table per group followed by each case with question, expected answer, trap, steps, claims and the latest results of `regression-report.json` and `acceptance-answers.json`; written by the same script, never edited by hand (`mvp-zurich` only) |
| `acceptance-answers.json` | The grades of the OpenCode harness's live-caller runs on the current release, aggregated per case (`--answers` of the harness), bound to the release's content digest and the suite's digest; read by the `ready` stage as gate G5; present for `mvp-zurich` since 15 September 2026 (52 graded sessions of UAT-1 to UAT-17), not yet for `mvp-wallisellen` |
| `readiness.json` | The readiness record the `ready` stage writes when every gate passed: bound to the bytes of `release.json` and to the suite's digest, with the attesting person and time, the verdict per gate and the case counts; the server's `--require-ready` and the container refuse a release without a matching one |
| `pipeline-report.json` | One record per stage of the last `swisstip-build` run (status, seconds, counts, error) |
| `basis-review.md` | The institution of every cited page and the basis of every served excerpt, with the rule that produced it, as an assistant assigned them; the review input for the `institutions` block and the citation `basis` entries of `curation.yaml` (`mvp-zurich`, `mvp-wallisellen`) |
| `README.md` | MVP pack only: the user-facing image README of the published release image, copied into the image beside the release files as `/srv/swiss-tip/README.md`; it quotes the release ID, the content digest and the scope statement, so it is rebuilt from the release whenever the release changes |
| `kb1-migration-report.json` | MVP pack only: how each of the predecessor's 84 facts was relocated or why it was dropped |
| `checks.yaml` | Stored tool checks: a name, a tool, a request validated against the contract and the expectations, with the result of the last run; written by the admin console's sandbox, not yet present in either pack |

The run of a pack, outside Git in `.local/<pack>/`, has the run layout of
the ingestion and extraction packages:

| File | Content |
| --- | --- |
| `pages/`, `fedlex-documents/` | Saved responses, one folder per URL with every attempt, and the dated Fedlex acts |
| `plan.json`, `plugin-plan.json`, `catalogue.json` | The download plan bound to the hash of `sources.json`, and the catalogue as planned |
| `summary.json`, `README.md` | Download outcome per target |
| `gap-report.json`, `gap-report.md` | What was not saved and why |
| `import-ledger.json` | Every file copied from the predecessor's runs, with its hash |
| `text/` | The text dataset: records, reading views, index, summary, validation |

The knowledge builder, the admin console and the per-package commands take
`.local/<pack>/` as the run directory (`releases/<pack>/` only when it holds a
`plan.json`, which no pack does); `--run-dir` selects another. The console's
job, audit and call logs are under `.local/<pack>/console/`. `.gitattributes`
marks `releases/` as binary for Git, so no line ending is converted and every
catalogue, curation file and release keeps its hash.
The format of the curation file and the release, the provenance kinds and
review statuses, and the build are described in
[docs/architecture/release-format.md](https://github.com/swisstip/swiss-tip/blob/main/docs/architecture/release-format.md).

A pack's `semantic-index.json` is bound to the served release by its ID
and content digest. It contains the published concept text, one vector of
1,024 dimensions per concept, and model/version hashes. Its model is
`qwen3-embedding:0.6b`; model weights are not part of the index. Serving with
`--semantic-index releases/mvp-zurich/semantic-index.json` requires that
model to be installed in local Ollama for query embeddings; the semantic
container images bundle Ollama and the model, the embedding sidecar supplies
both to a slim release image from a second container, and the semantic base
image rebuilds an index with exactly that model
([docker/README.md](https://github.com/swisstip/swiss-tip/blob/main/docker/README.md)). Default serving
remains lexical. The index must be rebuilt when the release or model changes;
a mismatch produces explicit lexical fallback. Preparation and validation
commands are in the [runtime README](https://github.com/swisstip/swiss-tip/blob/main/packages/runtime/README.md).

## What the catalogues contain

URLs and planning metadata only. No page content, quotations, legal rules,
facts or model-generated concepts. `scan_status: ready` means eligible for a
bounded crawl, not that content, live availability or robots access has
been verified.

The `mvp-zurich` pack lists every language version registered for its sources; most
entries are the German page. Its curation cites the German pages, with
one English SEM overview, and states its facts in English, as described in
section 3.4 of the
[functional specification](https://github.com/swisstip/swiss-tip/blob/main/docs/product/functional-specification.md).
The `mvp-wallisellen` catalogue selects the official German municipal pages;
its English fact statements are editorial paraphrases, not official translations.

## Saved pages

The pages of the Zurich catalogue are saved in the run layout of the ingestion
package, outside Git in `.local/mvp-zurich/` (see
[packages/ingestion/README.md](https://github.com/swisstip/swiss-tip/blob/main/packages/ingestion/README.md)). They were
downloaded on 10 and 11 September 2026 by the original SwissTIP tooling and
imported byte for byte with hash verification by a one-time script that is
not part of the repository; `import-ledger.json` in each run lists every
copied file. Each catalogue page keeps every attempt: the 10
September response as `attempt-001` (with any retry as `attempt-002`) and the
11 September response as the last attempt, which `latest.json` points at. The
three Fedlex acts of the MVP rehearsal (six dated HTML and PDF files) are
under `fedlex-documents/`. The 47 explicit pages of the MVP extension and the
dated documents of its eight further Fedlex acts were downloaded into the same run
on 15 September 2026 by the current bounded downloader, which followed no link.

The 50 explicit Wallisellen catalogue pages, in `.local/mvp-wallisellen/`,
were downloaded on 15 September 2026 by the current bounded downloader: 48 in the first run and the two naturalisation subpages, added to
`sources.md` after the OpenCode acceptance run, in a second run in the same
run directory that skipped the saved pages. On 16 September 2026 the five waste PDFs
linked from the waste disposal page (information leaflet, waste calendar 2026,
collection-area map, green-waste and bulky-waste-stamp leaflets) were added to
`sources.md` and downloaded into the same run, again skipping the saved pages;
the earlier plan and summary are kept beside the new ones as
`plan-2026-09-15.json` and `summary-2026-09-15.json`. It made no recursive
requests and produced no gaps.

The Zurich run also holds the *discovered pages* of the 11 September crawl, which
followed links from the catalogue pages. They are attributed to catalogue
sources in `plan.json`: `in-scope` when the URL lies inside a source's host
and path allowlist, `language-variant` when reached through a published
language link from such a page, `out-of-scope` otherwise. The MVP run holds
the in-scope pages and language variants of its 35 sources.

Download outcome, from `gap-report.md` in each run:

| Pack | Catalogue targets | Discovered pages | Saved | Size | Gaps |
| --- | ---: | ---: | ---: | ---: | --- |
| `mvp-zurich/` | 90 | 351 (164 in-scope, 187 language variants) | 436 of 441 | 62 MB | Catalogue: one explicit page of the extension answers HTTP 404 (Canton of Zurich, important information for the control drive); the eleven Fedlex ELI pages are JavaScript shells whose dated documents are in `fedlex-documents/`. Discovered: four dead SEM links (two with a trailing `%20`), three Federal Publications shop pages that are application shells |
| `mvp-wallisellen/` | 55 | 0 | 55 of 55 | 20 MB | None; the bounded run snapshots the explicit targets without following their links |

Only the catalogue targets and the in-scope and language-variant pages
carry a source attribution. A catalogue gap does not close with a plain
retry of the same URL: a failed page needs an alternative official URL, a
corrected host name or an access review, so it is a catalogue decision. To
re-run the download or retry after a catalogue change, use the commands in
the ingestion README with a new run directory.

## Text datasets

Each run also holds the text dataset of its saved pages under `text/`
(`.local/mvp-zurich/text/`, `.local/mvp-wallisellen/text/`), written in
the layout of the extraction package (see
[packages/extraction/README.md](https://github.com/swisstip/swiss-tip/blob/main/packages/extraction/README.md)): one JSON
record per saved response with labelled text blocks, code-point offsets and
hashes, a Markdown reading view per eligible record, an index and a summary.
This is what the knowledge expert reads and what the release build cites.

The Zurich dataset was first adopted from the predecessor's intermediate records
(matched by URL and raw hash, blocks, offsets and hashes untouched,
`legacy-text-import.json` in the dataset is the ledger) and then replaced
by a fresh extraction with extractor version 0.1.0, which kept every block
ID, offset and hash the release cites and added its labels (furniture labels,
PDF paragraphs, declared charsets). Version 0.2.0 only adds the rows of
client-side data tables embedded in a `data-entities` attribute; none of the
saved `mvp-zurich` pages has one, so its records were not re-extracted. The
Wallisellen dataset was re-extracted with 0.2.0, which recovered such rows on
14 of its 50 pages (emergency numbers, collection dates, contact directories);
its one record without text is the collection-area map, a PDF page that is an
image, and the month grids of the waste calendar PDF lost their layout, so the
release takes the dates from the HTML collection list.

| Pack | Records | Extracted | Excluded | No text | Blocks | Text | Disk |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `mvp-zurich/` | 461 (92 catalogue, 160 in-scope, 187 language variants, 22 Fedlex documents) | 444 | 17 | 0 | 86,135 | 6.85 M chars | 96 MB |
| `mvp-wallisellen/` | 55 (50 catalogue pages, 5 PDFs) | 54 | 0 | 1 | 12,122 | 393,249 chars | 12 MB |

Excluded records are application shells (the Fedlex ELI pages, whose dated
documents are separate records; Federal Publications shop pages; undated
Fedlex pages), maintenance pages and soft error pages. Among `mvp-zurich`'s seventeen
are the first responses of the three ch.ch catalogue pages (family
reunification, permits, work): "Error Page (404)" pages served with HTTP 200,
which `www.ch.ch` sends to any client whose User-Agent does not begin like a
browser's. The later attempts, fetched with the crawler's current User-Agent,
are ordinary records that supersede them; the gap report classifies such
responses as `soft-error-page`.

## Selecting sources

The Zurich catalogue carries these named scan sets:

| Scan set | Sources |
| --- | --- |
| `smoke` | 2 |
| `federal` | 25 |
| `zurich` | 10 |
| `multilingual` | 4 (SEM residence overview in de, en, fr, it) |
| `moving` | 19 (the extension's social insurance, tax at source, driving licence and health insurance sources) |
| `naturalisation` | 6 |
| `all` | 60 |

The `smoke`, `federal`, `zurich` and `multilingual` sets of `mvp-zurich`
are the residence-topic sets of the rehearsal and unchanged; `moving` and
`naturalisation` select the extension of 15 September 2026, whose pages are
also listed one by one in `sources.md`.

The Wallisellen catalogue has `smoke` (2 registry entries), `resident` (6),
`civic` (3) and `all` (10). Its `sources.md` adds all 55 exact targets
when the full pack is planned.
