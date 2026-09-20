"""Standalone round trip against the Swiss TIP server on the Wallisellen release (no LLM).

    ./.venv/Scripts/python.exe scripts/test/mcp/check_wallisellen.py [--release releases/mvp-wallisellen/release.json]
    ./.venv/Scripts/python.exe scripts/test/mcp/check_wallisellen.py --url http://127.0.0.1:8000/mcp

The tool-request checks of docs/product/wallisellen-user-acceptance-tests.md that
need no model: the jurisdiction variants of W-UAT-2, STALE for the museum on
1 November 2026 and for the city president from 16 October 2026, reviewed_only,
the status-specific guidance with its disclosures, not_served, and search for
every primary question (the expected concept among the first three hits, and
no list of every concept). Prints one line per check; exit code 1 on any failure.
"""

import argparse
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "mock-mcp"))
from check_server import ROOT, connect  # noqa: E402
from suite_cases import load_suite  # noqa: E402
from wallisellen_cases import build_wallisellen_cases  # noqa: E402

WALLISELLEN_CASES = build_wallisellen_cases(load_suite("mvp-wallisellen"))

WALLISELLEN = {"country_code": "CH", "canton_code": "CH-ZH", "municipality_id": "CH-ZH-69"}


async def run(release: Path, url: str | None = None) -> int:
    failures = []

    def check(label, condition):
        print(("ok   " if condition else "FAIL ") + label)
        if not condition:
            failures.append(label)

    def per_concept(result):
        return {item["concept_id"]: item for item in result.structuredContent["results"]}

    async with connect(release, url) as (read, write, health):
        async with ClientSession(read, write) as session:
            await session.initialize()
            if health is not None:
                check(f"health route names a Wallisellen release: {health.get('release_id')}",
                      str(health.get("release_id", "")).startswith("mvp-wallisellen"))

            async def resolve(**arguments):
                return await session.call_tool("resolve", arguments)

            canton = await resolve(concept_ids=["moving-registration"], jurisdiction={"canton_code": "CH-ZH"}, as_of="2026-09-15")
            gap = per_concept(canton)["moving-registration"]["gaps"][0]
            check("W-UAT-2: canton only -> OUT_OF_COVERAGE, published below the requested jurisdiction",
                  canton.structuredContent["status"] == "OUT_OF_COVERAGE" and gap["dimension"] == "jurisdiction_not_covered"
                  and gap["published_values"] == ["CH-ZH-69"])
            check("OUT_OF_COVERAGE guidance says the request is not covered",
                  "does not cover it" in canton.structuredContent.get("guidance_for_caller", ""))
            zurich = await resolve(concept_ids=["moving-registration"],
                                   jurisdiction={"canton_code": "CH-ZH", "municipality_id": "CH-ZH-261"}, as_of="2026-09-15")
            check("W-UAT-2: City of Zurich -> OUT_OF_COVERAGE with no facts",
                  per_concept(zurich)["moving-registration"]["status"] == "OUT_OF_COVERAGE"
                  and not per_concept(zurich)["moving-registration"]["facts"])
            ok = await resolve(concept_ids=["moving-registration", "population-services"], jurisdiction=WALLISELLEN,
                               as_of="2026-09-15")
            body = ok.structuredContent
            check("W-UAT-2: Wallisellen -> SUPPORTED, executed scope CH-ZH-69",
                  body["status"] == "SUPPORTED" and body["executed_scope"]["municipality_id"] == "CH-ZH-69")
            guidance = body.get("guidance_for_caller", "")
            check("SUPPORTED guidance forbids unserved additions and names the translation disclosure",
                  "cite only the returned URLs" in guidance and "have not been reviewed by a person" not in guidance
                  and "not official translations" in guidance)
            check("moving registration declares what it does not serve",
                  "a document list for registration" in per_concept(ok)["moving-registration"].get("not_served", []))
            short = await resolve(concept_ids=["moving-registration"], jurisdiction={"canton_code": "ZH", "municipality_id": "69"})
            check("short jurisdiction codes normalise to CH-ZH-69",
                  short.structuredContent["executed_scope"]["municipality_id"] == "CH-ZH-69"
                  and short.structuredContent["status"] in ("SUPPORTED", "STALE"))
            named = await resolve(concept_ids=["moving-registration"], jurisdiction={"canton": "Zurich", "city": "Wallisellen"})
            scope = named.structuredContent.get("executed_scope", {})
            check("the city given by name resolves to CH-ZH-69 and is echoed with the register's names",
                  scope.get("municipality_id") == "CH-ZH-69" and (scope.get("canton"), scope.get("city")) == ("Zürich", "Wallisellen")
                  and named.structuredContent.get("status") in ("SUPPORTED", "STALE"))
            elsewhere = await resolve(concept_ids=["moving-registration"], jurisdiction={"city": "Winterthur"})
            gap = per_concept(elsewhere)["moving-registration"]["gaps"][0]
            check("another Zurich city is placed by the register and told, by name, that the concept is Wallisellen's",
                  elsewhere.structuredContent["executed_scope"].get("municipality_id") == "CH-ZH-230"
                  and gap["dimension"] == "jurisdiction_not_covered" and "municipality of Wallisellen" in gap["message"])

            museum = await resolve(concept_ids=["facilities-museum-and-culture"], jurisdiction=WALLISELLEN, as_of="2026-11-01")
            guidance = museum.structuredContent.get("guidance_for_caller", "")
            check("W-UAT-5: 1 November 2026 -> STALE with facts",
                  museum.structuredContent["status"] == "STALE" and per_concept(museum)["facilities-museum-and-culture"]["facts"])
            check("STALE guidance: published on the snapshot, not confirmed for as_of, no earlier as_of",
                  "not what holds on 2026-11-01" in guidance and "earlier as_of" in guidance and "Answer now" not in guidance)
            check("W-UAT-5: the museum is listed as rentable, availability is not served",
                  any("private celebrations" in f["statement"] for f in per_concept(museum)["facilities-museum-and-culture"]["facts"])
                  and any("availability" in item for item in per_concept(museum)["facilities-museum-and-culture"]["not_served"]))
            before = await resolve(concept_ids=["facilities-museum-and-culture"], jurisdiction=WALLISELLEN, as_of="2026-10-14")
            check("14 October 2026 is still SUPPORTED", before.structuredContent["status"] == "SUPPORTED")
            president = await resolve(concept_ids=["city-council"], jurisdiction=WALLISELLEN, as_of="2026-10-16")
            check("city president on 16 October 2026 -> STALE", president.structuredContent["status"] == "STALE")

            reviewed = await resolve(concept_ids=["moving-registration"], jurisdiction=WALLISELLEN, reviewed_only=True)
            check("reviewed_only -> SUPPORTED, every fact human-reviewed",
                  reviewed.structuredContent["status"] == "SUPPORTED" and not per_concept(reviewed)["moving-registration"]["gaps"])

            emergency = await resolve(concept_ids=["emergency-numbers"], jurisdiction=WALLISELLEN)
            statements = " ".join(f["statement"] for f in per_concept(emergency)["emergency-numbers"]["facts"])
            check("emergency numbers are served, including the ambulance number 144",
                  emergency.structuredContent["status"] in ("SUPPORTED", "STALE") and "144" in statements)
            naturalisation = await resolve(concept_ids=["naturalisation"], jurisdiction=WALLISELLEN)
            item = per_concept(naturalisation)["naturalisation"]
            check("W-UAT-6: naturalisation requirements served, fees declared not served",
                  "C permit" in " ".join(f["statement"] for f in item["facts"]) and "naturalisation fees" in item["not_served"])

            for name, spec in WALLISELLEN_CASES.items():
                if spec["group"] != "primary":
                    continue
                found = await session.call_tool("search", {"query": spec["question"]})
                hits = [hit["concept_id"] for hit in found.structuredContent["results"]]
                check(f"search {spec['acceptance_id']}: {spec['resolved']} in the first three of {found.structuredContent['matched_count']} "
                      f"matches {hits[:3]}",
                      all(any(concept in hits[:3] for concept in (item if isinstance(item, tuple) else (item,)))
                          for item in spec["resolved"]) and found.structuredContent["matched_count"] <= 10)
            nothing = (await session.call_tool("search", {"query": "Wallisellen"})).structuredContent
            if nothing["retrieval_mode"] == "hybrid":
                # The embedding model places every concept of a municipal pack near the municipality's name.
                check("a query of only the municipality's name matches no concept lexically",
                      all(hit["matched_on"] == ["semantic"] for hit in nothing["results"]))
            else:
                check("a query of only the municipality's name matches no concept",
                      nothing["results"] == [] and "does not cover it" in nothing["guidance_for_caller"])

    print(f"\n{len(failures)} failure(s)")
    return 1 if failures else 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--release", type=Path, default=ROOT / "releases/mvp-wallisellen/release.json")
    parser.add_argument("--url", help="Streamable HTTP endpoint of a running server, for example http://127.0.0.1:8000/mcp")
    args = parser.parse_args(argv)
    return asyncio.run(run(args.release.resolve(), args.url))


if __name__ == "__main__":
    raise SystemExit(main())
