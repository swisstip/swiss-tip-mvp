"""The match-strength thresholds, replayed on the committed Zurich release.

The constants in `service.py` were measured on release mvp-zurich-2026-09-16-v2: every question of the acceptance
suite and of the round-trip check must report a strong lexical match, and a set of off-topic questions that share a
word with some concept ("Schweiz", "Anmeldung", "permit") must not. The hybrid thresholds are replayed from the raw
cosines measured inside the published image, since the tests have no embedding model. A release that adds concepts
changes the token weights; when a case here fails after a rebuild, re-measure the signals before moving a threshold.
"""

import unittest
from pathlib import Path

from swisstip.runtime.service import (LEXICAL_PARTIAL_WEIGHT, LEXICAL_STRONG_SHARE, LEXICAL_STRONG_WEIGHT,
                                      SEMANTIC_PARTIAL_SCORE, SEMANTIC_STRONG_SCORE, SEMANTIC_VETO_SCORE,
                                      ReleaseService, match_strength)

try:
    import yaml
except ImportError:  # pragma: no cover - the suite replay needs PyYAML, which the build tooling installs
    yaml = None

ROOT = Path(__file__).resolve().parents[3]
RELEASE = ROOT / "releases" / "mvp-zurich" / "release.json"
SUITE = ROOT / "releases" / "mvp-zurich" / "acceptance.yaml"

# Questions outside the release. Each shares at least one indexed word with a concept, so lexical search returns
# hits for it; the verdict must still be weak or none.
OFF_TOPIC = [
    "Wie hoch ist die Mehrwertsteuer in der Schweiz?",
    "What is the speed limit on Swiss motorways?",
    "How do I get a Halbtax?",
    "annual quotas for work permits",
    "Wann sind die nächsten eidgenössischen Abstimmungen?",
    "How does my child get into a Gymnasium in Zurich?",
    "Wo kann ich in Zürich günstig Ski fahren?",
    "Was kostet ein GA der SBB?",
    "How do I open a bank account in Switzerland?",
    "Ich suche eine Wohnung in Zürich, wo finde ich Inserate?",
    # Facet words ("opening hours", "Öffnungszeiten") alone do not make an office question covered (FACET_WORDS).
    "Opening hours of the Zurich zoo",
    "Wann hat das Passbüro Zürich offen?",
]
# Off-topic until release mvp-zurich-2026-09-17-v1, which added the Zurich office contacts, or v2, which added daily
# life in the City of Zurich, vehicles and the radio and television fee.
NOW_COVERED = {"What are the opening hours of the Migrationsamt Zurich?": "zh-migrationsamt-contact",
               "Where do I pay the Serafe radio and TV fee?": "radio-tv-household-fee",
               "Wie melde ich mein Auto in Zürich an?": "zh-vehicle-registration-move"}
# One lexical coincidence the lexical signals cannot see through: "Anmeldung" and "Bern" are anchors of the arrival
# and contact concepts. Hybrid search vetoed it (cosine 0.40 in the image of 2026-09-16-v2); lexical search reports
# strong. Since release 2026-09-17-v2 kindergarten registration is a City of Zurich concept, so hybrid search reads it
# strong as well, and Bern is refused at resolve (jurisdiction_not_covered).
LEXICAL_BLIND_SPOT = "Kindergarten Anmeldung Bern"
# A covered question in French, and the key terms a caller sends after translating them into German.
FRENCH_REGISTRATION = ("Je suis citoyen tchèque et je commence à travailler à Zurich. Dans quel délai dois-je annoncer "
                       "mon arrivée à la commune?")
FRENCH_REGISTRATION_IN_GERMAN = "Tschechischer Staatsangehöriger Stellenantritt Zürich Anmeldefrist Gemeinde Ankunft"

# (lexical share, anchored weight, best raw cosine) measured on 16 September 2026, with the verdict the rule must give.
# The cosines come from the published image mvp-zurich-2026-09-16-v2; the queries are those of the suite, the
# round-trip check and the off-topic list.
MEASURED_HYBRID = [
    ("UAT-1 register stay municipal authority Zurich", 1.00, 1.80, 0.64, "strong"),
    ("UAT-2e German work-permit terms", 0.85, 1.78, 0.62, "strong"),
    ("UAT-7 Zurich German family terms", 0.35, 1.61, 0.72, "strong"),
    ("German EU registration question", 0.61, 2.2, 0.74, "strong"),
    ("residence permit cost (in-scope topic, out-of-scope subject)", 0.54, 1.9, 0.65, "strong"),
    ("Italian registration question", 0.06, 0.4, 0.62, "weak"),
    ("French registration question", 0.14, 0.9, 0.53, "weak"),
    ("VAT rate, in German", 0.14, 0.34, 0.60, "weak"),
    ("Halbtax", 0.36, 0.57, 0.58, "weak"),
    ("annual quotas for work permits", 0.23, 0.51, 0.58, "weak"),
    ("speed limit on motorways", 0.10, 0.31, 0.50, "weak"),
    ("kindergarten registration in Bern", 0.57, 1.11, 0.40, "weak"),
    ("Chinese question, semantic only", 0.0, 0.0, 0.74, "strong"),
]


class ThresholdRuleTests(unittest.TestCase):
    def test_measured_hybrid_signals_give_the_recorded_verdicts(self):
        for label, share, weight, cosine, expected in MEASURED_HYBRID:
            with self.subTest(label):
                self.assertEqual(match_strength(share, weight, cosine), expected)

    def test_the_lexical_signals_decide_alone_without_a_cosine(self):
        self.assertEqual(match_strength(0.0, LEXICAL_STRONG_WEIGHT, None), "strong")
        self.assertEqual(match_strength(LEXICAL_STRONG_SHARE, 0.0, None), "strong")
        self.assertEqual(match_strength(0.49, 1.49, None), "weak")
        # The partial route needs both a partial weight and a partial cosine; a strong cosine needs nothing else.
        self.assertEqual(match_strength(0.0, LEXICAL_PARTIAL_WEIGHT, SEMANTIC_PARTIAL_SCORE), "strong")
        self.assertEqual(match_strength(0.0, LEXICAL_PARTIAL_WEIGHT - 0.01, SEMANTIC_PARTIAL_SCORE), "weak")
        self.assertEqual(match_strength(0.0, 0.0, SEMANTIC_STRONG_SCORE), "strong")
        # The veto beats every lexical signal.
        self.assertEqual(match_strength(1.0, 9.0, SEMANTIC_VETO_SCORE - 0.01), "weak")
        self.assertEqual(match_strength(1.0, 9.0, SEMANTIC_VETO_SCORE), "strong")


@unittest.skipUnless(RELEASE.is_file(), "the committed Zurich release is not in this checkout")
class CommittedReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.service = ReleaseService.from_file(RELEASE)

    def verdict(self, query: str):
        result = self.service.dispatch("search", {"query": query})
        return result.match_strength, result.match_signals

    def test_every_suite_question_and_search_query_is_a_strong_lexical_match(self):
        if yaml is None:
            self.skipTest("PyYAML is not installed")
        suite = yaml.safe_load(SUITE.read_text(encoding="utf-8"))
        for case in suite["cases"]:
            if "DECLINE" in case["case_id"]:
                continue  # the decline cases pin their own verdicts through expect_strength
            queries = [case["question"]] + [step["search"]["query"] for step in case.get("steps", []) if "search" in step]
            for query in queries:
                with self.subTest(case=case["case_id"], query=query[:60]):
                    strength, signals = self.verdict(query)
                    self.assertEqual(strength, "strong", signals)

    def test_off_topic_questions_are_weak_or_empty_and_keep_the_scope_statement(self):
        for query in OFF_TOPIC:
            with self.subTest(query=query):
                result = self.service.dispatch("search", {"query": query})
                self.assertIn(result.match_strength, ("weak", "none"), result.match_signals)
                self.assertEqual(result.scope_statement, self.service.release.manifest.scope_statement)
                self.assertTrue(result.guidance_for_caller.startswith(("Weak candidates only", "No candidates matched")))

    def test_office_questions_once_off_topic_now_find_their_concept(self):
        for query, concept_id in NOW_COVERED.items():
            with self.subTest(query=query):
                result = self.service.dispatch("search", {"query": query})
                self.assertEqual(result.match_strength, "strong", result.match_signals)
                self.assertEqual(result.results[0].concept_id, concept_id)

    def test_a_french_question_reads_weak_and_its_german_key_terms_find_the_concept(self):
        # The release indexes no French terms: the question about a covered subject reads weak on incidental words,
        # and the guidance allows one search with the key terms in German, the release's preferred query language.
        french = self.service.dispatch("search", {"query": FRENCH_REGISTRATION})
        self.assertEqual(french.match_strength, "weak", french.match_signals)
        self.assertIn("translated into German", french.guidance_for_caller)
        german = self.service.dispatch("search", {"query": FRENCH_REGISTRATION_IN_GERMAN})
        self.assertEqual(german.match_strength, "strong", german.match_signals)
        self.assertIn("eu-employment-registration-deadline", [hit.concept_id for hit in german.results[:3]])
        self.assertNotIn("translated", german.guidance_for_caller)

    def test_the_lexical_blind_spot_is_the_one_recorded(self):
        strength, signals = self.verdict(LEXICAL_BLIND_SPOT)
        self.assertEqual(strength, "strong")
        self.assertGreaterEqual(signals.lexical_share, LEXICAL_STRONG_SHARE)
        self.assertLess(signals.anchored_weight, LEXICAL_STRONG_WEIGHT)


if __name__ == "__main__":
    unittest.main()
