"""Every committed release passes its committed acceptance suite, its committed report is the report of exactly that
release and suite, and its readiness record names exactly the committed release file and suite. A changed release or
suite therefore cannot be committed without the accept and ready stages run again. A pack's regression pack
(acceptance.yaml plus regression.yaml) passes lexically, its committed report, which also holds the hybrid run,
is the report of exactly that release and those suites, and its committed test-cases.md is the page those files
render."""

import json
import unittest
from pathlib import Path

from swisstip.build.acceptance import REGRESSION_FILE, load_acceptance, load_regression
from swisstip.build.case_catalogue import CATALOGUE_FILE, load_case_catalogue
from swisstip.core.readiness import load_readiness, readiness_path, readiness_status
from swisstip.runtime.acceptance import check_acceptance, issues_of
from swisstip.runtime.service import ReleaseService

ROOT = Path(__file__).resolve().parents[3]


class CommittedPackTests(unittest.TestCase):
    def test_every_committed_release_passes_its_acceptance_suite(self):
        releases = sorted((ROOT / "releases").glob("*/release.json"))
        self.assertTrue(releases, "no committed release found")
        for release_path in releases:
            pack = release_path.parent.name
            with self.subTest(pack=pack):
                suite_path = release_path.parent / "acceptance.yaml"
                self.assertTrue(suite_path.is_file(), f"{pack} has a release but no acceptance suite")
                suite = load_acceptance(suite_path)
                self.assertEqual(suite.pack, pack)
                service = ReleaseService.from_file(release_path)
                report = check_acceptance(service, suite)
                self.assertEqual(issues_of(report), [])
                self.assertTrue(report["passed"])
                committed = json.loads((release_path.parent / "acceptance-report.json").read_text(encoding="utf-8"))
                self.assertEqual(committed["content_sha256"], report["content_sha256"], f"{pack}: the committed report is for another release")
                self.assertEqual(committed["suite_sha256"], report["suite_sha256"], f"{pack}: the committed report is for another suite")
                self.assertTrue(committed["passed"])
                self.assertTrue(readiness_path(release_path).is_file(), f"{pack} has a release but no readiness record; run the ready stage")
                status = readiness_status(release_path)
                self.assertEqual(status["status"], "ready", f"{pack}: {status.get('reason')}")
                record = load_readiness(readiness_path(release_path))
                self.assertEqual(record.suite_sha256, suite.digest(), f"{pack}: the readiness record is for another suite; run the ready stage")
                self.assertEqual(record.content_sha256, report["content_sha256"])

    def test_every_committed_regression_pack_passes_and_its_report_is_current(self):
        for suite_path in sorted((ROOT / "releases").glob(f"*/{REGRESSION_FILE}")):
            pack_dir = suite_path.parent
            with self.subTest(pack=pack_dir.name):
                acceptance, regression, combined = load_regression(pack_dir)
                self.assertEqual(regression.pack, pack_dir.name)
                # Lexically: the hybrid-only search steps are recorded without being judged.
                report = check_acceptance(ReleaseService.from_file(pack_dir / "release.json"), combined)
                self.assertEqual(issues_of(report), [])
                committed = json.loads((pack_dir / "regression-report.json").read_text(encoding="utf-8"))
                self.assertEqual(committed["content_sha256"], report["content_sha256"],
                                 f"{pack_dir.name}: the regression report is for another release; run scripts/test/regression")
                self.assertEqual((committed["acceptance_sha256"], committed["regression_sha256"]),
                                 (acceptance.digest(), regression.digest()),
                                 f"{pack_dir.name}: the regression report is for other suites; run scripts/test/regression")
                self.assertEqual(committed["runs"]["hybrid"].get("retrieval_mode"), "hybrid",
                                 f"{pack_dir.name}: the committed regression report has no hybrid run")
                self.assertTrue(committed["passed"])
                catalogue = pack_dir / CATALOGUE_FILE
                self.assertTrue(catalogue.is_file(), f"{pack_dir.name}: no {CATALOGUE_FILE}; run scripts/test/regression")
                self.assertEqual(catalogue.read_text(encoding="utf-8"), load_case_catalogue(pack_dir),
                                 f"{pack_dir.name}: {CATALOGUE_FILE} is not the page of the committed suites and "
                                 "reports; run scripts/test/regression/run_regression.py --render-only")


if __name__ == "__main__":
    unittest.main()
