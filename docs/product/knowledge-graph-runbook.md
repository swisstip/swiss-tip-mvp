# Knowledge graph runbook

**Last update:** 24 September 2026

Copy-paste steps to look at, review, compile, serve, refresh and extend the
Swiss knowledge graph (`graphs/ch/`), for someone who has not run the tools
before, on Windows with PowerShell. Each step says what you should see. The design is
`swiss-tip/docs/architecture/knowledge-graph.md`.

## 0. One-time setup on Windows

All commands are for **PowerShell** (Windows Terminal or the Start menu,
"Windows PowerShell"). The project needs Python 3.14; `uv` installs it
without administrator rights.

1. Install `uv` (once):

   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

   Close PowerShell and open a new one, then check: `uv --version` prints a
   version.

2. Install Python 3.14 and create the project environment in the code
   repository (`swiss-tip\.venv`; the `.venv` one level up belongs to WSL and
   is left alone):

   ```powershell
   cd C:\Users\louis\Dev\swiss-ai-weeks\swiss-tip
   uv python install 3.14
   uv venv --python 3.14 .venv
   uv pip install --python .venv\Scripts\python.exe -e packages\core -e packages\runtime -e packages\build -e packages\ingestion -e "packages\extraction[office]" -e packages\concepts -e apps\mcp-server -e apps\knowledge-builder -e apps\admin-console -e apps\calendar-connector
   ```

   The last line ends with a list of installed packages, `swisstip-...` among
   them.

## 0b. Every time: open a PowerShell in the packs folder

```powershell
cd C:\Users\louis\Dev\swiss-ai-weeks\swiss-tip-mvp
$tools = "C:\Users\louis\Dev\swiss-ai-weeks\swiss-tip\.venv\Scripts"
& "$tools\swisstip-graph.exe" --help
```

You should see the commands `derive`, `compile`, `merge` and `embed`. Every
command below is run from this folder in a PowerShell where `$tools` is set
(set it again in every new window).

## 1. Start the admin console

```powershell
& "$tools\swisstip-admin.exe" --packs-dir . --actor "Louis"
```

You should see `swisstip-admin ... on http://127.0.0.1:8765 (edit mode, actor
'Louis' ...)`. Open **http://localhost:8765** in your browser. Leave this
PowerShell window open (stop the console later with Ctrl+C) and open a second
PowerShell window, with step 0b, for the other commands. The name after
`--actor` is recorded on every edit and every review.

On the home page, below the packs, the card **Knowledge graphs > ch** shows
the counts (about 238 nodes and 668 edges) and the review progress (0
human-reviewed at the start).

## 2. Explore the graph

Click **ch**, then **Explore**. The graph opens focused on
`domain.registration`, two steps deep.

- Click a node: the panel on the right shows its summary, its names in the
  local languages, its edges and the pack topics that use it.
- Type another node in **focus** (for example `domain.naturalisation`,
  `role.cantonal-migration-office`, `level.cantonal`) and press **Show**.
- **depth** "whole graph" shows everything; tick **hide derived links** to see
  only the agents' claims.
- A dashed outline means unreviewed, a solid one reviewed.

**Items** lists every node and edge as a table, with filters.

## 3. Review

Click **Review**. The queue lists every unreviewed item.

1. Click an item. You see the claim (a summary or a one-sentence statement)
   and, under **Evidence**, the exact excerpt of the official page it rests
   on, with a link to the live page.
2. If the excerpt says what the claim says, press **Confirm** (key `y`). You
   are recorded as the reviewer. If it is wrong, write a note and press
   **Reject** (`n`): the item is removed and kept in the rejection log. If
   you are unsure, write a note and **Flag** it (`f`). Key `j` opens the next
   unreviewed item.
3. To correct a claim, edit the summary or statement in the form on the left
   and press **Save**. The graph is compiled in memory before the file is
   written; if something is wrong you get the reasons instead.
4. On the Review page you can also tick several items and confirm them in
   bulk; each one records that it was confirmed in a bulk review.

Start with the items a caller sees most: the domains, the roles, and the
`first_contact`, `executed_by` and `instance` edges.

## 4. Compile and check

On the graph's **Overview**, press **Compile and check**. A job starts; open
its **log** from the Jobs table. You should see `compile ran` and
`check ran`, and on the Overview the compiled counts with the date and
"orientation checks: 13 of 14 passed" (the one known gap is Lugano's
residents' office, which no source names yet).

The same from the terminal:

```powershell
& "$tools\swisstip-build.exe" ch --graph --packs-dir . --from compile
```

## 5. Put the graph into the packs

Each pack's release carries a copy of the compiled graph. After compiling:

```powershell
& "$tools\swisstip-graph.exe" embed releases\mvp-zurich
& "$tools\swisstip-graph.exe" embed releases\mvp-wallisellen
```

You should see the pack, the new `release_id` and the graph's counts. Then
run the acceptance suites:

```powershell
& "$tools\swisstip-build.exe" mvp-zurich --packs-dir . --from accept --until accept
& "$tools\swisstip-build.exe" mvp-wallisellen --packs-dir . --from accept --until accept
```

You should see `"exit_code": 0`.

## 6. Attest

A changed release needs a new readiness record, signed with your name:

```powershell
& "$tools\swisstip-build.exe" mvp-zurich --packs-dir . --from accept --until ready --attested-by "Louis"
& "$tools\swisstip-build.exe" mvp-wallisellen --packs-dir . --from accept --until ready --attested-by "Louis"
```

The output lists the gates. If the answer-quality gate (G5) asks for graded
live runs that do not exist for the new release, the record says so; follow
`swiss-tip/docs/architecture/acceptance-gate.md` section 4, or serve the
release as a candidate for the demo.

## 7. Try it as a caller

In the admin console: **Packs > mvp-zurich > Sandbox**, panel
**get_knowledge_graph**. Paste and press **Call get_knowledge_graph**:

```json
{"question": "I'm a Czech citizen and starting my work in Zurich next week. By when should I register?", "jurisdiction": {"city": "Zurich"}}
```

You should see the residents' office and, for Zurich, the Personenmeldeamt,
the cantonal migration office, and `place_dependence` "municipality", known.
Remove the `jurisdiction` part and call again: the office of the City of
Zurich disappears and `place_dependence` asks for the municipality.

To serve it to an MCP client (for example the demo client or Claude Desktop):

```powershell
& "$tools\swisstip-mcp.exe" --release releases\mvp-zurich\release.json --transport streamable-http --port 8000
```

The endpoint is `http://127.0.0.1:8000/mcp`; `http://127.0.0.1:8000/health`
names the knowledge graph. A client lists five tools, `get_knowledge_graph`
first.

## 8. Refresh the sources

On the graph's **Overview**, open **Refresh**, type `ch`, and press
**Refresh**. The job downloads the graph's own pages again, extracts them,
previews Derive, compiles with the citations relocated, and runs the checks.
Robots.txt is obeyed; tick **override robots.txt** only for hosts you are
authorised to access (the run report records it). The same from the
terminal:

```powershell
& "$tools\swisstip-build.exe" ch --graph --packs-dir . --download --update-curation
& "$tools\swisstip-build.exe" ch --graph --packs-dir . --download --update-curation --no-obey-robots
```

`$env:SWISSTIP_OBEY_ROBOTS = "0"` makes the override the default for every run
started from that PowerShell window (the console too, if you start it from
there).

## 9. Extend the graph with AI

Open Claude Code in this folder (in PowerShell: `claude`, from
`C:\Users\louis\Dev\swiss-ai-weeks\swiss-tip-mvp`) and type, for example:

```text
/build-knowledge-graph extend the residents' offices of the Canton of Bern
```

The skill scouts sources, fetches them, runs Derive, sends reader agents over
the excerpts, merges their proposals, writes check cases and compiles. What
the agents write arrives unreviewed; review it as in step 3, then steps 4 to
6.

## 10. Commit

Commit from Windows Git (PowerShell, GitHub Desktop or your editor), not from
WSL: the files are checked out with Windows line endings, which Git in WSL
reports as changed everywhere. In PowerShell, per repository:

```powershell
cd C:\Users\louis\Dev\swiss-ai-weeks\swiss-tip
git status
git add -A
git commit -m "Serve a knowledge graph of Switzerland before search"
cd C:\Users\louis\Dev\swiss-ai-weeks\swiss-tip-mvp
git status
git add -A
git commit -m "Build the Swiss knowledge graph and embed it in the packs"
```

`git status` should list only the files named below; if it lists more, stop
and check before adding.

- Code repository (`swiss-tip`): everything under `packages/`, `apps/`,
  `docs/`, `docker/opencode/opencode.json`, `scripts/test/mcp/check_wheel.py`,
  `README.md`, `NOTICE`. It also contains the robots.txt switch of the branch
  `feat/robots-toggle` (commit `668d767`); merge that branch first, or commit
  it together with this work.
- Packs repository (`swiss-tip-mvp`): `.claude/`, `graphs/`, `docs/product/`,
  the two packs' `curation.yaml`, `release.json` and reports, and
  `scripts/test/mcp/check_server.py`.

## In WSL instead of Windows

The same steps work in the Ubuntu (WSL) terminal with the environment
`swiss-ai-weeks/.venv`: `cd /mnt/c/Users/louis/Dev/swiss-ai-weeks/swiss-tip-mvp`,
`source ../.venv/bin/activate`, then the commands without `& "$tools\...exe"`
(for example `swisstip-admin --packs-dir . --actor "Louis"`). Commit from
Windows Git either way.
