# Swiss before/after baseline

**Last update:** 27 September 2026

Two local proofs that a code change in
[swiss-tip](https://github.com/swisstip/swiss-tip) leaves the attested Swiss
packs untouched: `mvp-zurich` and `mvp-wallisellen` must validate, build and
answer exactly as before. They serve the country-profile work of
[docs/architecture/country-profiles.md](https://github.com/swisstip/swiss-tip/blob/main/docs/architecture/country-profiles.md)
(sections 10.2 and 10.3) and run after every step of it. There is no
allowlist: any difference fails.

Both scripts read the committed packs and import the swiss-tip packages
installed in the `.venv`, so they prove the checkout that `.venv` points at
(the editable install), not a published version. They write nothing under
`releases/`.

## The capture: `snapshot_results.py`

Records, per pack, every tool result a caller can see, in-process with the
`ReleaseService` the server uses (lexical search, no model, no network), one
JSON line per request with the exact payload the server sends. The script's
docstring lists the record families: instructions and tool metadata, every
acceptance and regression step, the acceptance reports, every excerpt, the
case questions as asked, the register sweep, the error probes, the concept by
place matrix and the stdio `initialize` and `tools/list` of a real server
session. Every resolve carries an explicit `as_of`.

The first line of each `<pack>.jsonl` is a header. Its `binding` (release
bytes and digest, suite digests, semantic index) must be equal for a
comparison to run; its `info` (swiss-tip commit and changed paths, package
and Python versions, hash seed) is printed where it differs.

```sh
# the baseline, taken before a code change
./.venv/Scripts/python.exe scripts/test/baseline/snapshot_results.py --out .local/baseline/before-v2
# after the change: once with a fixed and once with a random hash seed
PYTHONHASHSEED=0 ./.venv/Scripts/python.exe scripts/test/baseline/snapshot_results.py --out .local/baseline/after --compare .local/baseline/before-v2
./.venv/Scripts/python.exe scripts/test/baseline/snapshot_results.py --out .local/baseline/after --compare .local/baseline/before-v2
```

In PowerShell, set the seed with `$env:PYTHONHASHSEED = "0"` and remove it
with `Remove-Item Env:PYTHONHASHSEED`. The `.venv` is the checkout's own or
the one of the folder that holds both repositories.

| Option | Meaning |
| --- | --- |
| `--out` | Directory for one `<pack>.jsonl` per pack |
| `--pack` | A pack folder under `releases/`; repeatable; default the attested Swiss packs `mvp-wallisellen` and `mvp-zurich`, so a pack being built (`mvp-poland`) is captured only when named |
| `--compare` | An earlier `--out` directory to compare with |
| `--skip-stdio` | Leave out the stdio server sessions (they start four server processes) |

Exit codes: 0 when every pack prints `0 differ`, 1 when a record differs
(the first differences are printed), 2 when a header refuses the comparison
(another release, suite or index) or the earlier capture lacks a pack's file.
The header's `diff_sha256` covers the uncommitted diff and the untracked
files of the swiss-tip checkout, so it names the code a capture ran on.

Not captured: hybrid search itself. It needs the query vectors recorded once
from a local Ollama with the model of the pack's `semantic-index.json` and
replayed offline; that recording is not implemented. What hybrid search takes
from the lexical side is captured: every case search and raw question also
records its whole lexical ranking with exact scores (all hits, everywhere and
among the concepts that apply at its place) and its anchored match. The
fused ranking is checked by the regression replay of `scripts/test/regression/`.

## The rebuild proof: `rebuild_swiss.py`

Builds `mvp-zurich` and `mvp-wallisellen` in memory from `curation.yaml`,
the place files it names and the pack's text dataset, with `created_at`,
`acceptance_suite_sha256` and `schema_version` pinned from the committed
manifest (`mvp-wallisellen` is `swiss-tip-release/v1`). It passes when the
committed `release.json` loads and dumps back to its own bytes, the rebuilt
release dumps to exactly those bytes, and their sha256 is the
`release_sha256` of `readiness.json`.

```sh
./.venv/Scripts/python.exe scripts/test/baseline/rebuild_swiss.py
./.venv/Scripts/python.exe scripts/test/baseline/rebuild_swiss.py --pack mvp-zurich --text mvp-zurich=<text dataset>
```

The text datasets are Git-ignored, so the proof runs locally only. A pack's
dataset is the first of `.local/<pack>/text` in this checkout and in the
folder that holds both repositories that has an `index.json`; `--text`
overrides it. Exit codes: 0 when both packs are byte-identical, 1 when one
differs (the first differing position is printed), 2 when a release or a
text dataset is missing.
