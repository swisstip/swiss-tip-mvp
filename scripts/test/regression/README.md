# Regression pack runner

**Last update:** 24 September 2026

`run_regression.py` replays a pack's regression pack, its `acceptance.yaml`
and `regression.yaml` together, against the committed release, with no model:
once with lexical search only and once with hybrid search, as the container
serves it. It writes `releases/<pack>/regression-report.json` and
`releases/<pack>/test-cases.md`, the readable page of every case: per group
an overview table with one row per case (question, status, outcome per
mode), then each case with its question, expected answer, trap, steps,
claims and latest results in both modes, plus the live-caller grades of
`acceptance-answers.json` for the acceptance cases that have them. The format, the rules of the cases and the
committed-pack test that checks the report and the page are described in
section 10 of
[docs/architecture/acceptance-gate.md](https://github.com/swisstip/swiss-tip/blob/main/docs/architecture/acceptance-gate.md).

```sh
./.venv/Scripts/python.exe scripts/test/regression/run_regression.py
./.venv/Scripts/python.exe scripts/test/regression/run_regression.py --pack mvp-zurich --lexical-only --no-write
./.venv/Scripts/python.exe scripts/test/regression/run_regression.py --render-only
```

| Option | Meaning |
| --- | --- |
| `--pack` | The pack folder under `releases/` (default `mvp-zurich`) |
| `--ollama-url` | The loopback Ollama endpoint (default `http://127.0.0.1:11434`) |
| `--timeout` | Seconds per embedding request (default 60) |
| `--lexical-only` | Skip the hybrid run; the report records why and does not pass |
| `--no-write` | Print the outcome without writing the report or the page |
| `--render-only` | Rewrite `test-cases.md` from the committed suites and reports without a replay, for example after `acceptance-answers.json` changed |

The hybrid run needs a local Ollama with the embedding model named in the
pack's `semantic-index.json`, at the digest the index was built with
(`ollama pull qwen3-embedding:0.6b` for the committed packs).

What the replay sends:

- Search steps send the case's `query`. A question in one of the release's
  query languages (German and English for `mvp-zurich`) is sent as asked; a
  question in any other language is sent as the key terms its author
  translated into the preferred language (`translated: true`), as a caller
  following the server's language note would send them.
- Resolve steps send the concepts, jurisdiction and context of the case, with
  the release's snapshot date as `as_of` unless the step names its own.
- A `retrieval: hybrid` search step is recorded but not judged in the lexical
  run.

Exit codes: 0 when every blocking case passes in both modes, 1 when a
blocking case fails, 2 when the hybrid run is impossible or a query fell back
to lexical search.

Run it after every change to the release, its semantic index, the search code
or either suite, and commit the report and the page with the change: the
committed-pack test fails while the report names another release or suite, or
while the page is not the one the committed files render. The output lists
quarantined cases that now pass; make them blocking in `regression.yaml`.

## The knowledge graph

`run_graph_regression.py` asks the knowledge graph in the pack's release
every question of the same two suites, as a caller following the server's
instructions would, and judges the orientation against what the suites
already expect; it needs no expectations of its own and no model. A question
whose search expects a concept must reach a domain its topic bridges to
(`graph_nodes`) among the first three, with the topic in `covered_topics`; a
question the release declines must not be pointed at a covered topic with a
strong match. It writes `releases/<pack>/graph-regression-report.json`, a
measurement to compare graphs and matching methods, not a gate.

```sh
./.venv/Scripts/python.exe scripts/test/regression/run_graph_regression.py --pack mvp-zurich
```

The design is section 10 of
[docs/architecture/knowledge-graph.md](https://github.com/swisstip/swiss-tip/blob/main/docs/architecture/knowledge-graph.md).
