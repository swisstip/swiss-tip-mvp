# Mock Swiss TIP MCP server and OpenCode caller test

**Last update:** 20 September 2026

A stdio MCP server with hardcoded content for one scenario, plus a harness
that runs OpenCode against it. It is advertised to clients as `swiss-tip-mock`
and configured in OpenCode under the name `swiss_tip`. The server behaves like the target
implementation described in section 4 of the
[functional specification](https://github.com/swisstip/swiss-tip/blob/main/docs/product/functional-specification.md):
same four tools, same request and result contracts, same statuses and gap
names. Its purpose is to test the calling LLM and to give every work package
a running target from the first hour of the day. It is not the knowledge
base.

The scenario: EU/EFTA nationals taking up employment in Switzerland must
register with their municipality within 14 days of arrival **and** before
starting work. The resolve result lists the user facts still needed (arrival
date, first working day) and a decision rule. The decision is left to the LLM.

Files:

- `contracts.py` - re-exports the protocol from `swisstip.core.contracts`
  (`packages/core`): Pydantic request and result models for `get_coverage`,
  `search`, `resolve` and `get_evidence`, the typed tool error, the tool
  descriptions, and a JSON Schema export. The mock and the real server
  (`apps/mcp-server`) serve the same models.
  The field tables and examples are documented in
  [docs/architecture/tool-contracts.md](https://github.com/swisstip/swiss-tip/blob/main/docs/architecture/tool-contracts.md) of the code repository;
  the exported bundle is committed next to it.
- `mock_residence_mcp.py` - the server. Four concepts (federal registration
  deadline, Canton of Zurich procedure, City of Zurich move-in, short-term
  notification), eight evidence excerpts from official pages saved on
  11 September 2026, constants only. One log line per call on stderr with
  tool, status, bytes and latency.
- `check_mock_mcp.py` - standalone MCP client round trip, no LLM; exercises
  every tool, every status and the typed errors.
- `run_opencode_test.py` - OpenCode harness (CLI), see below. `--server real`
  runs it against the real server on `releases/mvp-zurich/release.json`;
  `--case german-work-permit` sends the second standing case, a
  third-country national's work-permit question in German,
  `swiss-german-family-permit` a Swiss citizen's Zurich German question
  about a residence permit for a foreign spouse (both with the language of
  every search query in the assessment), and the four edge cases of
  `docs/product/user-acceptance-tests.md` have their own case names; the
  `wallisellen-*` cases serve `releases/mvp-wallisellen/release.json`.
- `wallisellen_cases.py` - the Wallisellen cases, prompts and criteria (see
  "Wallisellen suite").
- `details.py` - URLs, e-mail addresses, telephone numbers and amounts of an
  answer compared with the session's tool outputs.
- `grading.py` - grading packets, grade files and the aggregate report.
- `Start-OpenCodeDesktop.ps1` - launcher for the OpenCode desktop app.
- `requirements.txt` - the two dependencies (`mcp`, `pydantic`).

## Setup

```shell
python -m venv .venv
./.venv/Scripts/python.exe -m pip install -r scripts/test/mock-mcp/requirements.txt
```

On macOS or Linux replace `.venv/Scripts/` with `.venv/bin/`.

## Server self-check

```shell
./.venv/Scripts/python.exe scripts/test/mock-mcp/check_mock_mcp.py
```

Print the JSON Schema of all four tools:

```shell
./.venv/Scripts/python.exe scripts/test/mock-mcp/contracts.py
```

## What the target design looks like on the wire

| Call | Result |
| --- | --- |
| `get_coverage` with no arguments | Root page of about 1.5 KB: release ID, scope statement, out-of-scope list, jurisdictions `CH`, `CH-ZH`, `CH-ZH-261`, languages, freshness window, one topic |
| `get_coverage` with `parent_id: "residence"` | The four concepts with label, description, aliases, jurisdiction, required context fields and context schema |
| `search` with the user's question | Ranked concept IDs; the federal registration concept comes first for the Czech question |
| `resolve` with two concept IDs, `canton_code: "CH-ZH"`, `as_of` and context `population`, `purpose` | Per-concept `SUPPORTED` results with facts, citations, the answering jurisdiction, a `more_specific_jurisdiction_available` gap pointing at the City of Zurich, the required user facts and the decision rule |
| `resolve` without context | `NEEDS_CONTEXT` naming `population` and `purpose`, with guidance to derive them from the question |
| `resolve` with `canton_code: "CH-BE"` | Federal concept `SUPPORTED` with a `more_specific_jurisdiction_not_published` gap naming `CH-ZH` and `CH-ZH-261`, Zurich concept `OUT_OF_COVERAGE` with published value `CH-ZH` |
| `resolve` with `as_of` after 10 November 2026 | `STALE` with the facts and a freshness warning |
| `get_evidence` with up to five IDs | Full original excerpts with publisher, language, URL and access date |
| Any malformed request | `isError` with `INVALID_ARGUMENT` and the offending path |

Jurisdiction containment: a federal concept answers for any canton, the
cantonal concept only for `CH-ZH` and its municipalities, the municipal
concept only for `CH-ZH-261`. Never upward or sideways; an answer for another
canton, or for another municipality of the Canton of Zurich, says in a gap
that its own narrower level is not published.

## OpenCode CLI test

Default model: `opencode/ling-3.0-flash-fin-free`. Override with `--model`.

`--server real` uses lexical search by default. To exercise the optional
hybrid search with the committed index, add `--semantic-index`; this option
is accepted only for the real server:

```shell
./.venv/Scripts/python.exe scripts/test/mock-mcp/run_opencode_test.py \
  --server real --semantic-index releases/mvp-zurich/semantic-index.json \
  --live --case german-work-permit
```

Ollama must be running locally with the index's exact embedding model
installed, as described in the [server README](https://github.com/swisstip/swiss-tip/blob/main/apps/mcp-server/README.md) of the code repository.
The harness records the configured retrieval mode, absolute index path and
index SHA-256 in `summary.json`. Each search result summary also records its
actual `retrieval_mode` and any `fallback_reason`; requesting hybrid search
does not establish that the local model was available. Result sizes count
UTF-8 bytes of returned strings, excluding transport framing.

Offline harness tests use temporary files and no model or network:

```shell
./.venv/Scripts/python.exe -m unittest discover -s scripts/test/mock-mcp -p test_opencode_harness.py
```

```shell
./.venv/Scripts/python.exe scripts/test/mock-mcp/run_opencode_test.py --check-connection
./.venv/Scripts/python.exe scripts/test/mock-mcp/run_opencode_test.py --live
./.venv/Scripts/python.exe scripts/test/mock-mcp/run_opencode_test.py --live --scenario work-first --no-followup
```

Each live run creates `.local/mock-mcp/runs/run-<timestamp>/` with the
generated `opencode.json`, one JSONL transcript per turn and `summary.json`.
The configuration is passed to the child process only (`OPENCODE_CONFIG` and
`OPENCODE_CONFIG_CONTENT`); the user's own OpenCode configuration is
unchanged. OpenCode runs in a temporary workspace so the repository's
`AGENTS.md` is not injected as instructions. OpenCode takes its project
directory from the `PWD` environment variable rather than from the process
working directory, so the harness also sets `PWD` to the workspace for the
child. Without that, a shell that exports `PWD` (Git Bash does) makes
OpenCode load the repository's `AGENTS.md` into the system prompt.

Turn 1 sends exactly:

> I'm a Czech citizen and starting my work in Zurich next week. By when latest
> should I register my stay on the municipal authority?

Turn 2 answers with the scenario's dates in the same session:

| Scenario | Arrival | First working day | Expected answer |
| --- | --- | --- | --- |
| `work-first` | Sun 13 Sep 2026 | Wed 16 Sep 2026 | Register before 16 Sep (by 15 Sep); the 14-day limit (27 Sep) does not bind |
| `fourteen-days-first` | Tue 1 Sep 2026 | Fri 18 Sep 2026 | Register by 15 Sep (14 days after arrival), earlier than the first working day |

The assessment printed at the end is heuristic (string checks on the final
answer): MCP called, at most three calls, `resolve` returned `SUPPORTED`,
arrival date asked for, both limits stated, no date computed before the
arrival date was known, SEM FAQ cited, expected deadline named in turn 2.
Read the transcript before drawing conclusions.

The generated agent `residence-assistant` has every built-in OpenCode tool
disabled, so only the MCP tools remain, and a short system prompt that
mentions the tools exist without saying when to call them and asks for the
answer in the language of the question, because a German question was
answered in another language without that line. Replace the
prompt with `--prompt-file` to test other instructions; `--regrade <run
folder>` re-applies the current assessment to a saved run without calling
the model.

The single-turn cases (`--case`) need `--server real`: the mock release
covers EU/EFTA registration only, so the German, Zurich German and
edge-case questions find nothing on the mock server.

## Cases from the acceptance suites

Every case the harness runs is a case of a pack's acceptance suite,
`releases/<pack>/acceptance.yaml` (format:
[docs/architecture/acceptance-gate.md](https://github.com/swisstip/swiss-tip/blob/main/docs/architecture/acceptance-gate.md)):
the question as typed, the expected answer, the trap and the `answer` block
with the must-mention and must-not patterns, the URL fragments to cite, the
concepts to resolve and the IDs of the general criteria the grader applies.
`suite_cases.py` loads the suites (it needs `swisstip-build` from the
checkout's venv, for the YAML) and turns a case into the dict the
assessment reads; the harness adds only what the suite cannot know: the CLI
name of each case (`suite_cases.ZURICH_NAMES`, `wallisellen_cases.NAMES`),
the release it runs on, the system prompts, the language assessment of the
eleven non-English cases (UAT-2e, UAT-7, UAT-11, UAT-17, UAT-22, UAT-23,
UAT-29, UAT-31, UAT-37, UAT-40, UAT-44) and the tool checks of the cases
that need them. The
extension cases UAT-8 to UAT-17, the office-contact cases UAT-18 to UAT-23
(`migration-office-hours`, `migration-office-email`, `road-office-oerlikon`,
`population-office-saturday`, `german-sva-visit`,
`german-tax-at-source-contact`), the daily-life cases UAT-24 to UAT-34
(`dog-moving-in`, `rubbish-bags`, `sofa-disposal`,
`recycling-centre-saturday-cash`, `blue-zone-lunchtime`, `german-car-move`,
`kindergarten-cut-off`, `german-tax-access-code`, `serafe-without-tv`,
`ambulance-costs`, `road-office-hours`) and the cross-jurisdiction cases
UAT-35 to UAT-44 (`bern-short-contract-permit`,
`aargau-commuter-registration`, `german-licence-st-gallen`,
`bern-naturalisation`, `lucerne-premium-reduction`,
`german-zug-tax-at-source`, `bern-migration-office`,
`winterthur-registration`, `uster-dog-move`, `german-kloten-car-parking`)
have names and no recorded run on
the current release yet; criterion A9 of the office cases checks that a
negative the cited page states is reported as the office's statement. A
cross-jurisdiction case carries criterion A10: its user lives in another
canton or in a Zurich municipality other than the city, which the harness
reads from the suite's resolve steps (`user_jurisdiction`), and the
assessment fails when a resolve that returned facts ran for another canton
or municipality (`resolves_stay_in_user_jurisdiction`, with the observed
scopes in `resolve_scopes_observed`), for example for `CH-ZH` on behalf of a
user in Bern; the case's must-not patterns name the Zurich addresses,
telephone numbers and fees an answer must not carry over. A
suite case with an `answer` block that has no harness name fails
`test_opencode_harness.py`, so the suite stays the one list. To change what
an answer must say, edit the suite; the knowledge builder's `accept` stage
replays the suite's tool steps with no model, this harness runs its
questions through one.

## Wallisellen suite

The cases of
[docs/product/wallisellen-user-acceptance-tests.md](../../../docs/product/wallisellen-user-acceptance-tests.md)
are the thirty-nine cases of `releases/mvp-wallisellen/acceptance.yaml`, named in
`wallisellen_cases.py`, in three groups that `--case` accepts by name:
`wallisellen-primary` (W-UAT-1 to W-UAT-7), `wallisellen-probes` (the ten
cross-cutting probes, W-PROBE-1 to W-PROBE-10 in the order of the document's
table), `wallisellen-variants` (the twenty-two prompt edge variants,
W-UAT-1e1 to W-UAT-7e6) and `wallisellen` (all thirty-nine). They carry their own release: with
`--server real` the server is started on `releases/mvp-wallisellen/release.json`,
and both the server run and the `--server none` control use a municipal
system prompt that names Wallisellen, `CH-ZH-69`, as the user's municipality
and today's date (`--today`, default the current date; two museum cases that
set their own date or must ask for one leave it out), so the questions are
sent verbatim. The tool-request variants of W-UAT-2 need no model and are in
`scripts/test/mcp/check_wallisellen.py`.

The assessment adds to the phrase checks, for runs with the server:

- every `resolve` that returned facts executed for `CH-ZH-69` (the server's
  `executed_scope`, so `"69"` with canton `"ZH"` counts);
- the museum case sees `STALE`; the reviewed-only probe sends
  `reviewed_only: true` and sees `SUPPORTED`, every fact being reviewed;
- **no unserved details:** every URL, e-mail address, Swiss telephone number
  and money amount in the answer occurs in a tool output of the session or in
  the question (`details.py`; dates and plain numbers are not compared);
- when facts were served, the answer says that the English statements are
  not official translations, and, when a served fact is not
  `human-reviewed`, that it is unreviewed.

Controls record their unserved details too, as a comparison.

```shell
H=scripts/test/mock-mcp/run_opencode_test.py
./.venv/Scripts/python.exe $H --server real --live --case wallisellen-primary wallisellen-probes   --repeat 3 --resume --pause 10 --output <absolute-output>/server
./.venv/Scripts/python.exe $H --server none --live --case wallisellen-primary --repeat 3 --output <absolute-output>/control
./.venv/Scripts/python.exe $H --server real --url http://127.0.0.1:8000/mcp --live --case wallisellen ...
```

Several cases or `--repeat` above one put each case's run folders in a
subfolder named after the case, with `-r<n>` in the folder name. `--resume`
skips a repetition whose folder already holds an answered session.

A session that ends without an answer because the model provider refused it
(any provider API error before an answer: the free tier's
`FreeUsageLimitError` with HTTP 429, and "Upstream request failed" with HTTP
400 marked non-retryable, after which a fresh session succeeds) says
nothing about the model or the server. The harness waits `--retry-wait`
seconds (default 90, doubled per retry), starts a fresh session, keeps the
failed transcript as `<case>-turn-1.provider-failure-<n>.jsonl` and records
the attempts in `summary.json`; `--provider-retries` (default 3) bounds it.
The free quota is per model: when one model is exhausted, the others may
still answer. An OpenCode session that stops producing output (observed once on
15 September 2026, a session silent for ten minutes) is killed after
`--session-timeout` seconds (default 900) and retried the same way.

### Grading and report

Patterns cannot judge whether an answer states a published rule as a live
guarantee. `--grading-packets FOLDER...` writes `grading-request.md` next to
every saved run without a grade: the case's trap and expected answer, the
general criteria the case names (A1 to A8 for the Zurich cases, C1 to C6 for
Wallisellen), a condensed view of what the tools returned, the unserved
details and the final answer (`grading.py`); a `zurich-registration` run
gets one packet with both turns of both scenarios. A grader, a Claude Code
subagent or a person, reads the packet and writes `grade.json` next to it:

```json
{"grader": "...", "trap_held": true, "criteria_pass": false, "failed_criteria": ["C3"],
 "unsupported_claims": ["..."], "note": "..."}
```

`--report FOLDER...` prints one row per model, server, transport and case over
every saved run below the folders: sessions, answered sessions, trap held and
criteria passed from the grades, the heuristic verdict, sessions without
unserved details, the budget and the median call count; `--report-json` writes
the rows. A rate over repetitions is the result; a single session is an
observation.

`--answers FOLDER... --pack <pack>` turns the grades into the record the
acceptance gate reads: every answered run under the folders that used the
server (`--server real`, locally or over `--url`) on the pack's current
release, by content digest, counts for its case, and
`releases/<pack>/acceptance-answers.json` records per case the answered and
graded sessions, how many held the trap and passed every criterion, the
models, the unsupported claims and the run folders, bound to the release's
content digest and the suite's digest. The knowledge builder's `ready` stage
reads it as gate G5 under the suite's policy (`answer_check`,
`answer_repetitions`, `answer_pass_rate`; see
[acceptance-gate.md](https://github.com/swisstip/swiss-tip/blob/main/docs/architecture/acceptance-gate.md)):

```shell
./.venv/Scripts/python.exe $H --grading-packets <output>/server
# grade every grading-request.md, then
./.venv/Scripts/python.exe $H --answers <output>/server --pack mvp-wallisellen
./.venv/Scripts/python.exe -m swisstip.builder.cli mvp-wallisellen --from accept --until ready --attested-by "<name>"
```

Controls and runs on another release are left out of the record; a run's
`summary.json` names the release it served (`release.content_sha256`, or
`remote_health.content_sha256` for a remote endpoint).

## OpenCode TUI

The harness also writes a stable copy to `.local/mock-mcp/opencode.json`. In
PowerShell:

```powershell
$env:OPENCODE_CONFIG = "<repository>\.local\mock-mcp\opencode.json"
Set-Location $env:TEMP\swiss-tip-mock-workspace
opencode
```

Select the `residence-assistant` agent (Tab) and paste the question. Setting
`OPENCODE_CONFIG` replaces the user configuration for that process only.

## OpenCode desktop app

```powershell
./scripts/test/mock-mcp/Start-OpenCodeDesktop.ps1 -Server mock
```

It passes the configuration through `OPENCODE_CONFIG` and inline through
`OPENCODE_CONFIG_CONTENT`; the inline copy is applied last, so it also
overrides a project-level `opencode.json`. Do not start the app from a shell
that runs inside VS Code's extension host: that environment carries
`ELECTRON_RUN_AS_NODE=1` and other Electron variables, which make the app
exit immediately. The launcher strips them.
