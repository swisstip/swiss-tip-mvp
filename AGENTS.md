# Repository instructions

**Last update:** 20 September 2026

## The code

- This repository holds data: the packs under `releases/<pack>/`, the place
  register under `config/places/` and the checks of the packs under
  `scripts/test/`. The code that builds and serves the packs is the sibling
  repository [swiss-tip](https://github.com/swisstip/swiss-tip); its
  packages are installed in a `.venv`, either that checkout's or the one of
  the folder that holds both repositories side by side. Use that
  interpreter directly (`.venv\Scripts\python.exe` on Windows,
  `.venv/bin/python` on macOS/Linux), never a system `python`.
- The knowledge builder and the admin console take this checkout as their
  packs directory: `--packs-dir <this checkout>` or `SWISSTIP_PACKS`. The
  server takes a pack's `release.json` with `--release`.
- The runs of the packs (saved pages, text datasets, working files) live
  under the Git-ignored `.local/<pack>/`, not in the pack folder.

## Pack files

- `release.json`, `readiness.json`, `semantic-index.json`, the build,
  acceptance, regression and pipeline reports and `sources.json` are
  written by the pipeline and the console, never edited by hand. The
  release is hashed and its readiness record names that hash; a hand edit
  breaks the attestation. `curation.yaml` is the file a curator writes.
- Line endings are pinned by `.gitattributes` (`releases/** -text`): keep
  that rule, and never let an editor convert a pack file.
- A pack's facts are reviewed by a person before the release is attested,
  and the readiness record names that person. Never attest in another
  person's name.

## One-time scripts

- Scripts that serve a single migration, copy or analysis and are not part
  of the pipeline are created under the Git-ignored `.local/scripts/`
  directory, not under `scripts/`. Delete them once the task is done unless
  there is a reason to keep them locally. Reusable logic they need belongs
  in the code repository, with tests.

## Coverage and limitations documents

- `COVERAGE.md` and `LIMITATIONS.md` at the repository root are submission
  deliverables: the challenge requires documented coverage and limitations.
  They describe the released packs.
- Update both in the same change that alters what a pack serves. That
  includes a rebuilt or re-versioned release, a concept or fact added,
  removed or reworded, a change to the manifest's `scope_statement`,
  `out_of_scope` or `limitations`, a catalogue or source change, and a
  review that moves facts to `human-reviewed`. A change that leaves the
  release byte-identical does not need them touched.
- Every number in them is taken from the release, not written from memory:
  the release ID and content digest, the snapshot and stale dates, the
  topic, concept, fact, evidence and document counts, the jurisdictions,
  the languages and the `review_statuses` counts. Read them out of
  `releases/<pack>/release.json` and the pack's reports before editing.
- `LIMITATIONS.md` states the review status in absolute numbers, names what
  is missing or weak, and never softens it. The manifest's own `limitations`
  list is served to every caller, so the file and the release must agree.

## Writing conventions

- Use the ASCII hyphen-minus (`-`) instead of en dashes or em dashes in repository text.
- Documentation states what is implemented and tested separately from what is planned.

## Dates and history in documents

- A living document (the root documents, `releases/README.md`, the
  documents under `docs/` and the README of every pack and test script)
  describes the present state. Its only date is one line directly under the
  title: `**Last update:** 20 September 2026`, changed in every commit that
  changes its content. Exception: the root `README.md` carries no date line.
- No date in a section heading and no dated progress markers in the text.
  Dates that are content stay: the hackathon days, deadlines, a snapshot or
  stale date, the access date of a source, the date inside a release ID.
- When earlier states are worth keeping, move them into a companion document
  `docs/history/<document>-history.md`, newest entry first, and link it from
  the living document with one line. A living document never carries its
  own history.
- Dated records (experiment records under `.local/experiments/`, acceptance
  run records) keep their dates. A factual error in a record is corrected
  with a dated correction note, not by rewriting the record.
- State a changing number in one place and link to it instead of repeating
  it: release contents in `COVERAGE.md`, the review status in
  `LIMITATIONS.md`. Other documents name "the current release" rather than
  its ID unless the ID is the point.

## Shell conventions

- Prefer PowerShell instead of Bash for working commands and ad hoc scripts
  unless the user explicitly requests another shell.
- Continue to prefer Unix-style shell commands in repository documentation.

## Secrets

- Never commit credentials. `.env` and `.env.*` are Git-ignored; keys are
  passed as environment variables.

## Commit messages

- After every substantial repository update, propose a one-line commit message in the final response.
- Before proposing the message, inspect the subjects of the 10 most recent commits and follow their established style.
- Never add a Claude or Anthropic attribution trailer; see `CLAUDE.md`.
