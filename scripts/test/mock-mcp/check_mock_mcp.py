"""Standalone stdio round trip against the mock MCP server (no LLM).

Exercises every tool and every status the target design defines, the way a
client library sees them: tool listing, compact root coverage, topic listing,
search, multi-concept resolve with jurisdiction containment and named gaps,
NEEDS_CONTEXT, OUT_OF_COVERAGE, STALE, evidence reads and typed errors.
"""

import asyncio
import json
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = Path(__file__).resolve().parent / "mock_residence_mcp.py"
FEDERAL = "residence.registration-after-arrival-eu-efta"
CANTON = "residence.zh.registration-eu-efta"
CITY = "residence.zh.city-zurich-registration"
SHORT_TERM = "residence.short-term-notification-eu-efta"
QUESTION = ("I'm a Czech citizen and starting my work in Zurich next week. "
            "By when latest should I register my stay on the municipal authority?")
EU_EMPLOYMENT = {"population": "EU_EFTA", "purpose": "EMPLOYMENT", "employment_duration": "MORE_THAN_3_MONTHS"}


async def run():
    params = StdioServerParameters(command=sys.executable, args=[str(SERVER)],
                                   env={"PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"})
    failures = []

    def check(label, condition):
        print(("ok   " if condition else "FAIL ") + label)
        if not condition:
            failures.append(label)

    def by_concept(result):
        return {item["concept_id"]: item for item in result.structuredContent["results"]}

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            check(f"initialize: server {init.serverInfo.name} {init.serverInfo.version}",
                  init.serverInfo.name == "swiss-tip-mock")
            tools = (await session.list_tools()).tools
            check("tools advertised: " + ", ".join(t.name for t in tools),
                  [t.name for t in tools] == ["get_coverage", "search", "resolve", "get_evidence"])
            check("every tool carries an inlined input schema and an output schema",
                  all("$ref" not in json.dumps(t.inputSchema) and t.outputSchema for t in tools))

            root = await session.call_tool("get_coverage", {})
            body = root.structuredContent
            size = len(root.content[0].text.encode("utf-8"))
            check(f"root coverage is compact ({size} bytes) and names scope, out_of_scope, topics, freshness",
                  not root.isError and size < 4000 and body["scope_statement"] and body["out_of_scope"]
                  and body["topics"][0]["topic_id"] == "residence" and body["freshness"]["stale_from"] == "2026-11-10")

            topic = await session.call_tool("get_coverage", {"parent_id": "residence"})
            concepts = {c["concept_id"]: c for c in topic.structuredContent["concepts"]}
            check("topic page lists the four concepts with descriptions and required context",
                  not topic.isError and set(concepts) == {FEDERAL, CANTON, CITY, SHORT_TERM}
                  and all(c["description"] for c in concepts.values())
                  and concepts[FEDERAL]["required_context"] == ["population", "purpose"])

            found = await session.call_tool("search", {"query": QUESTION})
            hits = [h["concept_id"] for h in found.structuredContent["results"]]
            check(f"search ranks the federal registration concept first for the question: {hits[:2]}",
                  not found.isError and hits and hits[0] == FEDERAL)
            german = await session.call_tool("search", {"query": "Anmeldung Wohngemeinde Zuerich", "limit": 3})
            check("search matches German aliases",
                  {h["concept_id"] for h in german.structuredContent["results"]} >= {FEDERAL, CANTON})

            incomplete = await session.call_tool("resolve", {"concept_ids": [FEDERAL, CANTON],
                                                             "jurisdiction": {"canton_code": "CH-ZH"}})
            body = incomplete.structuredContent
            check("resolve without context -> NEEDS_CONTEXT naming population and purpose, with guidance",
                  not incomplete.isError and body["status"] == "NEEDS_CONTEXT"
                  and [m["field"] for m in by_concept(incomplete)[FEDERAL]["missing_context"]] == ["population", "purpose"]
                  and body.get("guidance_for_caller"))

            resolved = await session.call_tool("resolve", {
                "concept_ids": [FEDERAL, CANTON], "jurisdiction": {"country_code": "CH", "canton_code": "CH-ZH"},
                "as_of": "2026-09-12", "context": EU_EMPLOYMENT})
            body = resolved.structuredContent
            per = by_concept(resolved)
            check("resolve federal + canton for EU/EFTA employment in CH-ZH -> SUPPORTED for both",
                  not resolved.isError and body["status"] == "SUPPORTED"
                  and per[FEDERAL]["status"] == "SUPPORTED" and per[CANTON]["status"] == "SUPPORTED")
            statements = " ".join(f["statement"] for f in per[FEDERAL]["facts"])
            check("federal facts state 14 days AND before taking up work",
                  "within 14 days" in statements and "before taking up work" in statements)
            check("required user facts include arrival_date and first_working_day; decision rule present",
                  {"arrival_date", "first_working_day"} <= {f["name"] for f in body["required_user_facts"]}
                  and body["decision_rule"]["steps"])
            check("canton result names a more specific jurisdiction gap for the City of Zurich",
                  any(g["dimension"] == "more_specific_jurisdiction_available" and g["published_values"] == ["CH-ZH-261"]
                      for g in per[CANTON]["gaps"]))
            check("citations carry URLs, language and access date",
                  all(c["url"].startswith("https://") and c["language"] and c["accessed_on"] == "2026-09-11"
                      for c in per[FEDERAL]["citations"]))
            check("text content equals structured content", json.loads(resolved.content[0].text) == body)

            city = await session.call_tool("resolve", {
                "concept_ids": [FEDERAL, CANTON, CITY],
                "jurisdiction": {"canton_code": "CH-ZH", "municipality_id": "CH-ZH-261"}, "context": EU_EMPLOYMENT})
            per = by_concept(city)
            check("with municipality CH-ZH-261 the city concept is SUPPORTED and the gap disappears",
                  per[CITY]["status"] == "SUPPORTED" and not per[CANTON]["gaps"]
                  and any(f["fact_id"] == "f-zh-city-appointment" for f in per[CITY]["facts"]))

            bern = await session.call_tool("resolve", {
                "concept_ids": [FEDERAL, CANTON], "jurisdiction": {"canton_code": "CH-BE"}, "context": EU_EMPLOYMENT})
            per = by_concept(bern)
            check("canton CH-BE: federal SUPPORTED, Zurich concept OUT_OF_COVERAGE naming CH-ZH",
                  bern.structuredContent["status"] == "SUPPORTED" and per[FEDERAL]["status"] == "SUPPORTED"
                  and per[CANTON]["status"] == "OUT_OF_COVERAGE"
                  and per[CANTON]["gaps"][0]["dimension"] == "jurisdiction_not_covered"
                  and per[CANTON]["gaps"][0]["published_values"] == ["CH-ZH"])
            check("canton CH-BE: the federal answer says that the narrower levels are published for Zurich only",
                  [(g["dimension"], g["published_values"]) for g in per[FEDERAL]["gaps"]]
                  == [("more_specific_jurisdiction_not_published", ["CH-ZH", "CH-ZH-261"])]
                  and "carry over no rule" in (bern.structuredContent.get("guidance_for_caller") or ""))

            federal_only = await session.call_tool("resolve", {"concept_ids": [FEDERAL], "context": EU_EMPLOYMENT})
            check("resolve without canton answers at the federal level",
                  by_concept(federal_only)[FEDERAL]["answering_jurisdiction"] == "CH (federal)")

            third = await session.call_tool("resolve", {
                "concept_ids": [FEDERAL], "context": {"population": "THIRD_COUNTRY", "purpose": "EMPLOYMENT"}})
            per = by_concept(third)
            check("third-country -> OUT_OF_COVERAGE with context_not_covered gap",
                  third.structuredContent["status"] == "OUT_OF_COVERAGE"
                  and per[FEDERAL]["gaps"][0]["dimension"] == "context_not_covered")

            short = await session.call_tool("resolve", {
                "concept_ids": [FEDERAL, SHORT_TERM],
                "context": {"population": "EU_EFTA", "purpose": "EMPLOYMENT", "employment_duration": "UP_TO_3_MONTHS"}})
            per = by_concept(short)
            check("up to three months: federal concept points to the short-term concept, which is SUPPORTED",
                  per[FEDERAL]["status"] == "OUT_OF_COVERAGE" and SHORT_TERM in per[FEDERAL]["gaps"][0]["message"]
                  and per[SHORT_TERM]["facts"][0]["fact_id"] == "f-short-term-notification")

            stale = await session.call_tool("resolve", {
                "concept_ids": [FEDERAL], "as_of": "2027-01-15", "context": EU_EMPLOYMENT})
            check("as_of after the freshness window -> STALE with facts and a warning",
                  stale.structuredContent["status"] == "STALE" and by_concept(stale)[FEDERAL]["facts"]
                  and any("older than" in item for item in stale.structuredContent["limitations"]))

            abroad = await session.call_tool("resolve", {
                "concept_ids": [FEDERAL], "jurisdiction": {"country_code": "DE"}, "context": EU_EMPLOYMENT})
            check("country DE -> OUT_OF_COVERAGE", abroad.structuredContent["status"] == "OUT_OF_COVERAGE")

            unknown = await session.call_tool("resolve", {"concept_ids": ["nope"], "context": EU_EMPLOYMENT})
            check("unknown concept -> OUT_OF_COVERAGE listing the published concept IDs",
                  by_concept(unknown)["nope"]["gaps"][0]["dimension"] == "concept_not_published"
                  and FEDERAL in by_concept(unknown)["nope"]["gaps"][0]["published_values"])

            ids = [e for c in by_concept(resolved)[FEDERAL]["citations"] for e in c["evidence_ids"]][:5]
            evidence = await session.call_tool("get_evidence", {"evidence_ids": ids})
            check(f"get_evidence returns {len(ids)} excerpts with URLs",
                  not evidence.isError and [e["evidence_id"] for e in evidence.structuredContent["evidence"]] == ids
                  and all(e["url"].startswith("https://") and e["original_excerpt"] for e in evidence.structuredContent["evidence"]))

            bad = await session.call_tool("get_evidence", {"evidence_ids": ["nope"]})
            check("unknown evidence ID -> isError INVALID_ARGUMENT",
                  bad.isError and bad.structuredContent["error"]["code"] == "INVALID_ARGUMENT")
            too_many = await session.call_tool("get_evidence", {"evidence_ids": ids[:1] * 6})
            check("six evidence IDs -> isError from schema validation", too_many.isError)
            extra = await session.call_tool("resolve", {"concept_ids": [FEDERAL], "surprise": 1})
            check("unknown request field -> isError naming the field",
                  extra.isError and extra.structuredContent["error"]["issues"][0]["path"] == "surprise")
            unknown_tool = await session.call_tool("get_coverage", {"parent_id": "other"})
            check("unknown parent_id -> isError", unknown_tool.isError)

    print(f"\n{len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(run()))
