"""The Zurich release as the server serves it: it is ready, it answers the standing question over stdio with the
coverage root under its size limit, and the frozen retrieval fixture of the code repository still refers to
concepts and facts it publishes. The server itself is tested on synthetic fixtures in the code repository
(apps/mcp-server/tests and packages/runtime/tests); the server has no default release, so every command here
names this one."""

import asyncio
from contextlib import redirect_stdout
from io import StringIO
import json
import sys
import unittest
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from swisstip.core.release import load_release
from swisstip.mcp_server.server import health, main
from swisstip.runtime.search_cli import load_cases
from swisstip.runtime.service import ReleaseService

ROOT = Path(__file__).resolve().parents[3]
RELEASE = ROOT / "releases" / "mvp-zurich" / "release.json"
# The retrieval fixture is a test input of the runtime package, not a record; it is read from a checkout of the code
# repository next to this one, when there is one.
HOLDOUT = ROOT.parent / "swiss-tip" / "packages" / "runtime" / "tests" / "fixtures" / "semantic-search-queries.json"


class ZurichReleaseTests(unittest.TestCase):
    def test_the_zurich_release_is_committed_and_healthy(self):
        self.assertTrue(RELEASE.is_file())
        report = health(ReleaseService.from_file(RELEASE))
        self.assertEqual(report["status"], "ok")
        self.assertGreaterEqual(report["facts"], 70)
        self.assertIn("CH-ZH-261", report["jurisdictions"])

    def test_health_reports_the_release_as_ready(self):
        output = StringIO()
        with redirect_stdout(output):
            code = main(["--release", str(RELEASE), "--health", "--require-ready"])
        self.assertEqual(code, 0)
        report = json.loads(output.getvalue())
        self.assertEqual(report["readiness"]["status"], "ready")
        self.assertEqual(report["readiness"]["release_id"], report["release_id"])
        self.assertTrue(report["readiness"]["attested_by"])

    def test_stdio_round_trip_on_the_release(self):
        async def run():
            params = StdioServerParameters(command=sys.executable,
                                           args=["-m", "swisstip.mcp_server.server", "--release", str(RELEASE)],
                                           env={"PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"})
            async with stdio_client(params) as (read, write):
                async with ClientSession(read, write) as session:
                    init = await session.initialize()
                    listed = (await session.list_tools()).tools
                    root = await session.call_tool("get_coverage", {})
                    resolved = await session.call_tool("resolve", {
                        "concept_ids": ["eu-employment-registration-deadline"], "jurisdiction": {"canton_code": "CH-ZH"},
                        "as_of": "2026-09-12", "context": {"population": "eu_efta"}})
                    return init, listed, root, resolved

        init, listed, root, resolved = asyncio.run(run())
        # The release's query languages reach the caller before its first search: in the instructions, in the search
        # description and in the query field, and on the coverage root.
        # swisstip-mcp 0.3.0 asks for one search and no longer calls German "preferred"; the published 0.2.5 that
        # the workflow installs until then carries the older sentence.
        note = r"Write (the search query|search queries) in German( \(preferred\))? or English:"
        self.assertRegex(init.instructions, note)
        search = next(t for t in listed if t.name == "search")
        self.assertRegex(search.description, note)
        self.assertRegex(search.inputSchema["properties"]["query"]["description"], note)
        self.assertEqual([q["code"] for q in root.structuredContent["query_languages"]], ["de", "en"])
        self.assertFalse(root.isError)
        # Criterion X8 keeps the coverage root small enough to refuse an outside question in one call. Two bounds
        # had drifted apart: this one at 6,144 bytes and check_server.py at 8,000, with the root at 7,640 - so the
        # round trip had been failing while the server check passed. The user settled it on 23 September 2026:
        # 8,000 is the real bound, in both places and in X8. The four waves of 22-23 September took the root from
        # 6,033 to 7,640 bytes. The cantonal wave then did not fit: stating in the manifest that registration is
        # published for all 26 cantons, with the caveats that go with it, costs about 370 bytes and took the root to
        # 8,317. The alternatives were a terser and less precise disclosure or rewriting reviewed limitations, and
        # the user chose on 23 September 2026 to raise the bound to 8,500 instead, because the pack grew from one
        # canton to twenty-six and the root grew with it. Shorten a topic description before raising this again.
        self.assertLess(len(root.content[0].text.encode("utf-8")), 8500)
        self.assertEqual(resolved.structuredContent["status"], "SUPPORTED")
        self.assertTrue(resolved.structuredContent["results"][0]["citations"][0]["url"].startswith("https://www.sem.admin.ch/"))

    def test_frozen_authored_holdout_references_released_facts(self):
        if not HOLDOUT.is_file():
            self.skipTest(f"no code checkout next to this one: {HOLDOUT} is missing")
        release = load_release(RELEASE)
        # The holdout is frozen for the release it was authored on (its hash is cited by the measurement records);
        # the reviewed release that followed publishes the same concepts and facts, which load_cases verifies.
        dataset = load_cases(HOLDOUT, release, allow_release_change=True)
        self.assertEqual(dataset["release_id"], "mvp-zurich-2026-09-13-v5")
        self.assertEqual(len(dataset["cases"]), 42)
        self.assertEqual({case["language"] for case in dataset["cases"]}, {"en", "de", "fr", "it", "zh", "gsw"})
        self.assertEqual(sum(not case["expected_concept_ids"] for case in dataset["cases"]), 7)


if __name__ == "__main__":
    unittest.main()
