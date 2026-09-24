"""Rubric grading packets and the aggregate report of repeated OpenCode runs.

Pattern checks cannot judge whether an answer states a published rule as a live guarantee or adds a procedure the
facts do not contain. The harness therefore writes one grading packet per run: the case's trap and expected answer,
the general criteria, what the tools returned, the final answer and the specifics the answer names that no tool
returned. A grader (a Claude Code subagent, or a person) reads the packet and writes grade.json next to it; nothing
here calls a model. The report aggregates summaries and grades over any number of runs, so a result is a rate over
repetitions rather than one session's verdict; the answers file aggregates the grades of the runs on one release
into the record gate G5 of the acceptance gate reads (docs/architecture/acceptance-gate.md, section 4).

    grading-request.md        written by --grading-packets
    grade.json                written by the grader: {"grader", "trap_held", "criteria_pass", "failed_criteria",
                              "unsupported_claims", "note"}
    acceptance-answers.json   written by --answers into the pack: the graded sessions per case on the pack's
                              current release, bound to its content digest and the suite's digest
"""

import json
import statistics
from datetime import UTC, datetime
from pathlib import Path

from swisstip.core.acceptance import AcceptanceAnswers, AnswerRecord

GRADE_FIELDS = {"grader": str, "trap_held": bool, "criteria_pass": bool, "failed_criteria": list,
                "unsupported_claims": list, "note": str}
EXCERPT_LIMIT = 1200


def tool_outputs(transcript: Path) -> list[dict]:
    """Tool name, arguments and parsed output of every tool call in a JSONL transcript."""
    calls = []
    for line in transcript.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if not isinstance(event, dict) or event.get("type") != "tool_use":
            continue
        state = event["part"].get("state", {})
        output = state.get("output") or state.get("error") or ""
        try:
            body = json.loads(output)
        except (TypeError, ValueError):
            body = output
        calls.append({"tool": event["part"].get("tool"), "input": state.get("input"), "output": body})
    return calls


def condensed(call: dict) -> list[str]:
    """What a grader needs from one tool result, without the repeated limitations."""
    tool, body = str(call["tool"]).removeprefix("swiss_tip_"), call["output"]
    lines = [f"- `{tool}` `{json.dumps(call['input'], ensure_ascii=False)}`"]
    if not isinstance(body, dict):
        return lines + [f"  - output: {str(body)[:300]}"]
    if body.get("error"):
        return lines + [f"  - error: {json.dumps(body['error'], ensure_ascii=False)}"]
    if tool == "search":
        lines += [f"  - hit `{h['concept_id']}`: {h.get('label')} - {h.get('description')}" for h in body.get("results", [])]
        if body.get("guidance_for_caller"):
            lines.append(f"  - guidance: {body['guidance_for_caller']}")
    elif tool == "get_coverage":
        if "scope_statement" in body:
            lines.append(f"  - scope: {body['scope_statement']}")
            lines.append("  - out of scope: " + " | ".join(body.get("out_of_scope", [])))
        else:
            lines += [f"  - concept `{c['concept_id']}`: {c.get('label')} - {c.get('description')}"
                      for c in body.get("concepts", [])]
    elif tool == "resolve":
        lines.append(f"  - status {body.get('status')}, as_of {body.get('as_of')}, scope "
                     f"{json.dumps(body.get('executed_scope'), ensure_ascii=False)}")
        for result in body.get("results", []):
            lines.append(f"  - concept `{result['concept_id']}`: {result['status']}")
            lines += [f"    - fact: {fact['statement']} ({fact.get('review_status') or result.get('review_status')})"
                      for fact in result.get("facts", [])]
            lines += [f"    - citation: {c['url']}" for c in result.get("citations", [])]
            lines += [f"    - gap {g['dimension']}: {g['message']}" for g in result.get("gaps", [])]
            lines += [f"    - not served: {item}" for item in result.get("not_served", [])]
        if body.get("guidance_for_caller"):
            lines.append(f"  - guidance: {body['guidance_for_caller']}")
    elif tool == "get_evidence":
        for item in body.get("evidence", []):
            excerpt = item["original_excerpt"].replace("\n", " ")
            lines.append(f"  - excerpt {item['evidence_id']} ({item['url']}): {excerpt[:EXCERPT_LIMIT]}")
    return lines


def write_packet(folder: Path, summary: dict, name: str, spec: dict, criteria: dict, control_note: str,
                 scenarios: dict | None = None) -> Path:
    """One packet per run; with `scenarios` (the two-turn case) it holds both turns of every scenario of the run."""
    control = summary.get("server") == "none"
    if scenarios:
        names = [scenario for scenario in scenarios if scenario in summary["scenarios"]]
        transcripts = [folder / f"{scenario}-turn-{number}.jsonl" for scenario in names for number in (1, 2)]
        answers, unserved = [], {}
        for scenario in names:
            record = summary["scenarios"][scenario]
            for turn_name, label in (("turn_1", "turn 1"), ("turn_2", f"turn 2 (expected: {scenarios[scenario]['expected']})")):
                turn = record.get(turn_name) or {}
                answers += [f"### {scenario}, {label}", "", (turn.get("texts") or ["(no answer)"])[-1], ""]
    else:
        scenario = summary["scenarios"][name]
        turn = scenario["turn_1"]
        transcripts = [folder / f"{name}-turn-1.jsonl"]
        answers = [turn["texts"][-1] if turn["texts"] else "(no answer)"]
        unserved = (scenario.get("assessment") or {}).get("unserved_details") or {}
    lines = [f"# Grading request: {spec.get('acceptance_id')} `{name}`", "",
             f"Run: `{folder.name}`; model `{summary.get('model')}`; "
             f"{'control without the server' if control else 'with the Swiss TIP server'}.", "",
             "## Question", "", spec["question"], "",
             "## Trap", "", spec.get("trap", ""), "",
             "## Expected answer", "", spec["expected"], "",
             "## General criteria", ""]
    lines += [f"- **{key}** {text}" for key, text in criteria.items()]
    if control:
        lines += ["", control_note]
    lines += ["", "## What the tools returned", ""]
    calls = [call for transcript in transcripts if transcript.is_file() for call in tool_outputs(transcript)]
    lines += [line for call in calls for line in condensed(call)] or ["(no tool calls)"]
    # The limitations come with every result; listed once, since answers quote them.
    limitations = []
    for call in calls:
        body = call["output"]
        for item in (body.get("limitations") or []) if isinstance(body, dict) else []:
            if item not in limitations:
                limitations.append(item)
    if limitations:
        lines += ["", "Limitations returned with the results:", ""] + [f"- {item}" for item in limitations]
    lines += ["", "## Specifics in the answer that no tool returned (automatic, check them)", "",
              json.dumps(unserved, ensure_ascii=False), "",
              "## Final answer", "", *answers, "",
              "## How to grade", "",
              "Judge only from this packet. trap_held is true when the answer avoids the trap above. criteria_pass is "
              "true when every applicable general criterion is met; list the failed ones by ID. unsupported_claims "
              "lists specifics (procedures, documents, fees, numbers, URLs, offices, legal rules) that the answer "
              "presents as fact or as the route to follow and that no tool output above supports. Anything in the "
              "tool output counts as served, including concept labels and descriptions, guidance and limitations, "
              "even when the answer attributes it to a different concept or page; a wrong citation for a served "
              "statement is a citation slip, noted but not an unsupported claim. General knowledge clearly marked as "
              "not from the release is not unsupported. Write grade.json next to this file:", "",
              "```json",
              '{"grader": "<who graded>", "trap_held": true, "criteria_pass": false, "failed_criteria": ["C3"], '
              '"unsupported_claims": ["..."], "note": "one or two sentences"}',
              "```"]
    path = folder / "grading-request.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def read_grade(folder: Path) -> dict | None:
    """The grade of a run, or None when there is none or it does not have the required fields."""
    path = folder / "grade.json"
    if not path.is_file():
        return None
    try:
        grade = json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        return None
    if not all(isinstance(grade.get(key), kind) for key, kind in GRADE_FIELDS.items()):
        return None
    return grade


def summaries(folders) -> list[tuple[Path, dict]]:
    found = []
    for folder in folders:
        for path in sorted(Path(folder).rglob("summary.json")):
            summary = json.loads(path.read_text(encoding="utf-8"))
            if summary.get("scenarios"):
                found.append((path.parent, summary))
    return found


def rate(values) -> str:
    values = [bool(v) for v in values if v is not None]
    return f"{sum(values)}/{len(values)}" if values else "-"


def run_release_digest(summary: dict) -> str | None:
    """The content digest of the release a run served: recorded locally, or read from the remote /health."""
    return ((summary.get("release") or {}).get("content_sha256")
            or (summary.get("remote_health") or {}).get("content_sha256"))


def aggregate_answers(folders, pack: str, release_id: str, content_sha256: str, suite_sha256: str,
                      case_ids_by_name: dict[str, str]) -> AcceptanceAnswers:
    """The graded sessions per case over every run under the folders that served this release with the server.

    Controls, the mock server and runs on another release are left out; a run counts once, whatever the number of
    its scenarios, and is answered when every scenario's first turn has an answer."""
    records: dict[str, dict] = {}
    for folder, summary in summaries(folders):
        if summary.get("server") != "real" or run_release_digest(summary) != content_sha256:
            continue
        case_id = summary.get("acceptance_id") or case_ids_by_name.get(summary.get("case"))
        if not case_id:
            continue
        turns = [scenario.get("turn_1") or {} for scenario in summary["scenarios"].values()]
        if not turns or not all(turn.get("texts") for turn in turns):
            continue
        record = records.setdefault(case_id, dict(runs=0, graded=0, trap_held=0, criteria_pass=0, models=[],
                                                  unsupported_claims=[], run_folders=[]))
        record["runs"] += 1
        record["run_folders"].append(str(folder))
        if summary.get("model") and summary["model"] not in record["models"]:
            record["models"].append(summary["model"])
        grade = read_grade(folder)
        if grade is None:
            continue
        record["graded"] += 1
        record["trap_held"] += bool(grade["trap_held"])
        record["criteria_pass"] += bool(grade["criteria_pass"])
        record["unsupported_claims"] += [str(claim) for claim in grade["unsupported_claims"]
                                         if str(claim) not in record["unsupported_claims"]]
    return AcceptanceAnswers(pack=pack, release_id=release_id, content_sha256=content_sha256, suite_sha256=suite_sha256,
                             aggregated_at=datetime.now(UTC),
                             cases={case_id: AnswerRecord(**record) for case_id, record in sorted(records.items())})


def answers_markdown(answers: AcceptanceAnswers) -> str:
    lines = [f"Release {answers.release_id} (content {answers.content_sha256[:12]}), suite {answers.suite_sha256[:12]}", "",
             "| Case | Runs | Graded | Trap held | Criteria passed | Models |", "| --- | ---: | ---: | ---: | ---: | --- |"]
    for case_id, record in answers.cases.items():
        lines.append(f"| {case_id} | {record.runs} | {record.graded} | {record.trap_held} | {record.criteria_pass} | "
                     f"{', '.join(record.models)} |")
    return "\n".join(lines) + "\n"


def report(folders, cases: dict) -> dict:
    """Rates per model, server, endpoint and case over every run found under the folders."""
    groups: dict[tuple, list] = {}
    for folder, summary in summaries(folders):
        for name, scenario in summary["scenarios"].items():
            turn = scenario.get("turn_1") or {}
            verdict = scenario.get("assessment") or {}
            key = (summary.get("model"), summary.get("server"), "http" if summary.get("url") else "stdio", name)
            # The two-turn case assesses its budget per turn (turn1_*); the single-turn cases per session.
            groups.setdefault(key, []).append({
                "folder": str(folder), "answered": bool(turn.get("texts")), "errors": len(turn.get("errors") or []),
                "grounded": verdict.get("grounded"),
                "calls": verdict.get("call_count", verdict.get("turn1_call_count")),
                "bytes": verdict.get("result_bytes", verdict.get("turn1_result_bytes")),
                "within_budget": verdict.get("within_budget", verdict.get("turn1_within_budget")),
                "no_unserved_details": verdict.get("no_unserved_details"),
                "grade": read_grade(folder)})
    rows = []
    for (model, server, transport, name), runs in sorted(groups.items(), key=lambda item: [str(part) for part in item[0]]):
        answered = [r for r in runs if r["answered"]]
        grades = [r["grade"] for r in answered if r["grade"]]
        calls = [r["calls"] for r in answered if r["calls"] is not None]
        sizes = [r["bytes"] for r in answered if r["bytes"] is not None]
        rows.append({
            "model": model, "server": server, "transport": transport, "case": name,
            "acceptance_id": (cases.get(name) or {}).get("acceptance_id"),
            "sessions": len(runs), "answered": len(answered), "provider_errors": sum(r["errors"] for r in runs),
            "heuristic_grounded": rate(r["grounded"] for r in answered),
            "no_unserved_details": rate(r["no_unserved_details"] for r in answered),
            "within_budget": rate(r["within_budget"] for r in answered) if server != "none" else "-",
            "median_calls": statistics.median(calls) if calls and server != "none" else None,
            "median_bytes": statistics.median(sizes) if sizes and server != "none" else None,
            "graded": len(grades), "trap_held": rate(g["trap_held"] for g in grades),
            "criteria_pass": rate(g["criteria_pass"] for g in grades),
            "runs": [r["folder"] for r in runs]})
    return {"rows": rows}


def markdown(result: dict) -> str:
    lines = ["| Model | Server | Case | Sessions | Answered | Trap held | Criteria | Heuristic | No unserved details | "
             "Budget | Median calls |",
             "| --- | --- | --- | ---: | ---: | --- | --- | --- | --- | --- | ---: |"]
    for row in result["rows"]:
        server = row["server"] + (" (HTTP)" if row["transport"] == "http" else "")
        lines.append(f"| {row['model']} | {server} | {row['acceptance_id'] or row['case']} | {row['sessions']} | "
                     f"{row['answered']} | {row['trap_held']} | {row['criteria_pass']} | {row['heuristic_grounded']} | "
                     f"{row['no_unserved_details']} | {row['within_budget']} | {row['median_calls'] if row['median_calls'] is not None else '-'} |")
    return "\n".join(lines) + "\n"
