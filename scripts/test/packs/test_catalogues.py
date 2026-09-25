"""The committed source catalogues: every pack's catalogue validates offline, the Zurich catalogue carries the scan
sets its extensions added, and the download planner plans every Zurich source without a request. The catalogue
code itself is tested on a fixture in the code repository (packages/ingestion/tests)."""

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from swisstip.ingestion import download_cli
from swisstip.ingestion.catalog import load_source_catalog, select_sources

ROOT = Path(__file__).resolve().parents[3]
MVP = ROOT / "releases/mvp-zurich/sources.json"


class CommittedCatalogueTests(unittest.TestCase):
    def test_every_committed_catalogue_validates_offline(self) -> None:
        catalogues = sorted((ROOT / "releases").glob("*/sources.json"))
        self.assertTrue(catalogues, "no committed catalogue found")
        for path in catalogues:
            with self.subTest(pack=path.parent.name):
                catalogue = load_source_catalog(path)
                self.assertTrue(catalogue["sources"], f"{path.parent.name}: the catalogue names no source")
                self.assertEqual(len(select_sources(catalogue)), len(catalogue["sources"]))

    def test_the_zurich_catalogue_carries_its_extensions(self) -> None:
        mvp = load_source_catalog(MVP)
        # 251 sources, then on 23 September 2026 the City of Lugano's waste source (daily-life) and one registry
        # seed per host for the English versions (english), which the downloader now needs to attribute them; on
        # 24 September 2026 the waste-collection pages of Basel and St. Gallen (daily-life); on 25 September 2026
        # the school-holiday page of each of the 26 cantons (school-holidays).
        self.assertEqual(len(mvp["sources"]), 286)
        self.assertEqual(len(set(mvp["scan_sets"]["english"])), 6)
        scan_sets = mvp["scan_sets"]
        self.assertLessEqual({"smoke", "federal", "zurich", "multilingual", "moving", "naturalisation", "contacts",
                              "daily-life", "entry", "voting-tax", "expat-life", "cantons", "all"}, set(scan_sets))
        # The cantonal registration wave of 23 September 2026: 71 sources over the 25 cantons other than
        # Zurich, which is served by its own zh-* sources. Twenty-one of them are consolidated statutes,
        # because nine cantons publish the registration deadline in law and nowhere else.
        self.assertEqual(len(set(scan_sets["cantons"])), 71)
        cantonal = {s["definition"]["jurisdiction"] for s in mvp["sources"]
                    if s["definition"]["source_id"] in set(scan_sets["cantons"])}
        self.assertEqual(len(cantonal), 25)
        self.assertNotIn("CH-ZH", cantonal)
        # The school holidays of 25 September 2026: one seed per canton. GL and TG reset the connection for the
        # crawler and are fetched with a browser User-Agent; BL, SH and NW could not be fetched and stay recorded.
        holidays = [s for s in mvp["sources"] if s["definition"]["source_id"] in set(scan_sets["school-holidays"])]
        self.assertEqual(len({s["definition"]["jurisdiction"] for s in holidays}), 26)
        self.assertEqual({s["definition"]["source_id"] for s in holidays if s.get("user_agent") == "browser"},
                         {"gl-school-holidays", "tg-school-holidays"})
        self.assertEqual({s["definition"]["source_id"] for s in holidays if s["scan_status"] == "needs_access_review"},
                         {"bl-school-holidays", "sh-school-holidays", "nw-school-holidays"})
        # The extensions of 15 September (topics), 17 September (office contacts, daily life) and 18 September
        # (voting rights and the tax-at-source tariff) name these sources.
        extension = set(scan_sets["moving"]) | set(scan_sets["naturalisation"])
        self.assertEqual(len(extension), 25)
        self.assertEqual(len(set(scan_sets["contacts"])), 8)
        self.assertEqual(len(set(scan_sets["daily-life"])), 13)
        voting_tax = set(scan_sets["voting-tax"]) - extension
        self.assertEqual(voting_tax, {"ch-fedlex-bv", "zh-fedlex-kv", "zh-voting", "ch-chch-voting"})
        source_ids = {entry["definition"]["source_id"] for entry in mvp["sources"]}
        for name, members in scan_sets.items():
            with self.subTest(scan_set=name):
                self.assertLessEqual(set(members), source_ids, f"scan set {name} names a source the catalogue lacks")

    def test_the_mvp_catalogue_plans_every_source_offline(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "run"
            with patch.object(download_cli, "snapshot") as fetch, redirect_stdout(io.StringIO()):
                self.assertEqual(download_cli.main(["--catalogue", str(MVP), "--output", str(output)]), 0)
                fetch.assert_not_called()
            plan = json.loads((output / "plan.json").read_text(encoding="utf-8"))
            self.assertEqual(len(plan["targets"]), 286)
            self.assertEqual(plan["catalog_ref"]["artifact_id"], "residence-sources-mvp-zurich")
            fedlex = [s["url"] for s in json.loads((output / "plugin-plan.json").read_text(encoding="utf-8"))["sources"]]
            # the VEV joined the eleven Fedlex documents on 17 September 2026, the two constitutions and the Code of
            # Obligations on 18 September, and the KVV and KLV on 23 September, when the health-insurance wave needed
            # an ordinance beside the guidance for the cost-sharing amounts
            self.assertEqual(len(fedlex), 17)
            self.assertTrue(all(url.startswith("https://www.fedlex.admin.ch/eli/cc/") for url in fedlex))


if __name__ == "__main__":
    unittest.main()
