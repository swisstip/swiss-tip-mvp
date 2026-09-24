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
        self.assertEqual(len(mvp["sources"]), 96)
        scan_sets = mvp["scan_sets"]
        self.assertLessEqual({"smoke", "federal", "zurich", "multilingual", "moving", "naturalisation", "contacts",
                              "daily-life", "entry", "voting-tax", "expat-life", "all"}, set(scan_sets))
        # The extensions of 15 September (topics), 17 September (office contacts, daily life) and 18 September
        # (voting rights and the tax-at-source tariff) name these sources.
        extension = set(scan_sets["moving"]) | set(scan_sets["naturalisation"])
        self.assertEqual(len(extension), 25)
        self.assertEqual(len(set(scan_sets["contacts"])), 8)
        self.assertEqual(len(set(scan_sets["daily-life"])), 10)
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
            self.assertEqual(len(plan["targets"]), 96)
            self.assertEqual(plan["catalog_ref"]["artifact_id"], "residence-sources-mvp-zurich")
            fedlex = [s["url"] for s in json.loads((output / "plugin-plan.json").read_text(encoding="utf-8"))["sources"]]
            # the VEV joined the eleven Fedlex documents on 17 September 2026, the two constitutions and the Code of
            # Obligations on 18 September
            self.assertEqual(len(fedlex), 15)
            self.assertTrue(all(url.startswith("https://www.fedlex.admin.ch/eli/cc/") for url in fedlex))


if __name__ == "__main__":
    unittest.main()
