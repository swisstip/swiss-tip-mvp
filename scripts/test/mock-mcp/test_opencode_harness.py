import hashlib
import json
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest
import unittest.mock

import run_opencode_test as harness


class HarnessTests(unittest.TestCase):
    def test_semantic_index_reaches_child_command_as_absolute_path_and_records_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "index.json"
            raw = b'{"fixture": true}\n'
            path.write_bytes(raw)
            server = harness.configure_server("real", path)
            config = harness.build_config("test-model", "test-python", "unchanged prompt", server)
            command = config["mcp"][harness.MCP_NAME]["command"]
            self.assertEqual(command[-2:], ["--semantic-index", str(path.resolve())])
            self.assertTrue(Path(command[-1]).is_absolute())
            self.assertEqual(server["configured_retrieval_mode"], "hybrid")
            self.assertEqual(server["semantic_index"], str(path.resolve()))
            self.assertEqual(server["semantic_index_sha256"], hashlib.sha256(raw).hexdigest())
            self.assertEqual(config["agent"][harness.AGENT]["prompt"], "unchanged prompt")

    def test_semantic_selection_does_not_change_lexical_default_or_shared_preset(self):
        original = list(harness.SERVERS["real"]["args"])
        hybrid = harness.configure_server("real", Path("not-present-test-index.json"))
        lexical = harness.configure_server("real")
        self.assertEqual(harness.SERVERS["real"]["args"], original)
        self.assertEqual(lexical["args"], original)
        self.assertEqual(lexical["configured_retrieval_mode"], "lexical")
        self.assertIsNone(lexical["semantic_index"])
        self.assertIsNone(lexical["semantic_index_sha256"])
        self.assertIsNone(hybrid["semantic_index_sha256"])
        self.assertEqual(hybrid["configured_retrieval_mode"], "hybrid")

    def test_semantic_index_is_rejected_for_mock_and_control(self):
        for name in ("mock", "none"):
            with self.subTest(server=name):
                with self.assertRaisesRegex(ValueError, "requires --server real"):
                    harness.configure_server(name, Path("index.json"))
                self.assertEqual(harness.configure_server(name)["configured_retrieval_mode"], name)

    def test_url_configures_a_remote_endpoint(self):
        url = "https://swiss-tip.example/mcp"
        open_server = harness.configure_server("real", url=url)
        entry = harness.build_config("test-model", "test-python", "prompt", open_server)["mcp"][harness.MCP_NAME]
        self.assertEqual(entry, {"type": "remote", "url": url, "enabled": True, "timeout": 60000})
        local = harness.build_config("test-model", "test-python", "prompt", harness.configure_server("real"))
        self.assertEqual(local["mcp"][harness.MCP_NAME]["type"], "local")
        for name, index in (("mock", None), ("none", None), ("real", Path("index.json"))):
            with self.subTest(server=name, semantic_index=index):
                with self.assertRaisesRegex(ValueError, "--url requires --server real"):
                    harness.configure_server(name, index, url=url)

    def test_case_release_replaces_the_default_release_and_is_recorded(self):
        release = harness.WALLISELLEN_CASES["wallisellen-tax-rate"]["release"]
        server = harness.configure_server("real", release=release)
        command = harness.build_config("test-model", "test-python", "prompt", server)["mcp"][harness.MCP_NAME]["command"]
        self.assertEqual(command[command.index("--release") + 1], str(release.resolve()))
        self.assertEqual(server["release"]["release_id"].split("-2026")[0], "mvp-wallisellen")
        self.assertEqual(len(server["release"]["file_sha256"]), 64)
        self.assertIn(str(harness.REAL_RELEASE), harness.SERVERS["real"]["args"])
        self.assertIsNone(harness.configure_server("none", release=release)["release"])
        with self.assertRaisesRegex(ValueError, "--server real or --server none"):
            harness.configure_server("mock", release=release)

    def test_wallisellen_cases_carry_municipal_prompts_and_verbatim_questions(self):
        groups = {group: len(names) for group, names in harness.CASE_GROUPS.items()}
        self.assertEqual(groups, {"wallisellen": 40, "wallisellen-primary": 7, "wallisellen-probes": 10,
                                  "wallisellen-variants": 22, "wallisellen-places": 1})
        acceptance = Path(harness.ROOT / "docs/product/wallisellen-user-acceptance-tests.md").read_text(encoding="utf-8")
        for name, case in harness.WALLISELLEN_CASES.items():
            with self.subTest(case=name):
                self.assertIn(name, harness.SINGLE_TURN_CASES)
                self.assertIn(case["question"], acceptance)
                if case.get("place_by_name"):
                    # A place case tests what the caller makes of the user's words: its prompts give the place away
                    # neither as a code nor as a name, and the check of the served municipality still applies.
                    for prompt in (case["prompt"], case["control_prompt"]):
                        self.assertNotRegex(prompt, r"CH-ZH|Wallisellen|Zurich|municipality ID")
                    self.assertIn("Wallisellen", case["question"])
                    self.assertEqual(case["municipality_id"], "CH-ZH-69")
                else:
                    self.assertIn("CH-ZH-69", case["prompt"])
                self.assertNotIn("Swiss TIP", case["control_prompt"])
                self.assertTrue(case["trap"] and case["expected"])
                self.assertEqual(set(case["criteria"]), {"C1", "C2", "C3", "C4", "C5", "C6"})

    def test_every_suite_case_with_an_answer_block_is_a_harness_case(self):
        names = {spec["acceptance_id"]: name for name, spec in harness.SINGLE_TURN_CASES.items()}
        names[harness.ZURICH_REGISTRATION["acceptance_id"]] = "zurich-registration"
        for suite in (harness.ZURICH_SUITE, harness.WALLISELLEN_SUITE):
            for case in suite.cases:
                with self.subTest(case=case.case_id):
                    if case.answer is None:
                        # A server-only case (the decline cases): replayed by the accept stage, not run by the harness.
                        self.assertTrue(case.steps, f"{case.case_id} has neither an answer block nor steps")
                        self.assertNotIn(case.case_id, names)
                    else:
                        self.assertIn(case.case_id, names)
        self.assertEqual(harness.SINGLE_TURN_CASES["german-work-permit"]["question"], harness.ZURICH_SUITE.case("UAT-2e").question)
        self.assertEqual(harness.SINGLE_TURN_CASES["wallisellen-tax-rate"]["must_mention"],
                         harness.WALLISELLEN_SUITE.case("W-UAT-3").answer.must_mention)
        self.assertEqual(harness.SUITE_DIGESTS["mvp-zurich"], harness.ZURICH_SUITE.digest())

    def test_answers_aggregate_the_graded_runs_on_the_release(self):
        grade = {"grader": "t", "trap_held": True, "criteria_pass": False, "failed_criteria": ["C3"],
                 "unsupported_claims": ["a fee"], "note": ""}
        runs = [  # folder, server, digest, case, answered, grade
            ("run-1", "real", "c" * 64, "wallisellen-tax-rate", True, grade),
            ("run-2", "real", "c" * 64, "wallisellen-tax-rate", True, dict(grade, criteria_pass=True, unsupported_claims=[])),
            ("run-3", "real", "c" * 64, "wallisellen-tax-rate", False, None),   # provider failure: not answered
            ("run-4", "none", "c" * 64, "wallisellen-tax-rate", True, grade),   # control
            ("run-5", "real", "d" * 64, "wallisellen-tax-rate", True, grade),   # another release
            ("run-6", "real", "c" * 64, "wallisellen-lunaplus", True, None),    # answered, not graded
        ]
        with tempfile.TemporaryDirectory() as directory:
            for folder, server, digest, case, answered, item in runs:
                path = Path(directory) / folder
                path.mkdir()
                summary = {"model": "m", "server": server, "case": case, "acceptance_id": harness.SINGLE_TURN_CASES[case]["acceptance_id"],
                           "release": {"content_sha256": digest}, "scenarios": {case: {"turn_1": {"texts": ["answer"] if answered else []}}}}
                (path / "summary.json").write_text(json.dumps(summary), encoding="utf-8")
                if item:
                    (path / "grade.json").write_text(json.dumps(item), encoding="utf-8")
            names = {name: spec["acceptance_id"] for name, spec in harness.SINGLE_TURN_CASES.items()}
            answers = harness.grading.aggregate_answers([directory], "mvp-wallisellen", "r-1", "c" * 64, "s" * 64, names)
        self.assertEqual(sorted(answers.cases), ["W-UAT-3", "W-UAT-4"])
        tax = answers.cases["W-UAT-3"]
        self.assertEqual((tax.runs, tax.graded, tax.trap_held, tax.criteria_pass, tax.models), (2, 2, 2, 1, ["m"]))
        self.assertEqual(tax.unsupported_claims, ["a fee"])
        self.assertEqual((answers.cases["W-UAT-4"].runs, answers.cases["W-UAT-4"].graded), (1, 0))
        self.assertEqual((answers.content_sha256, answers.suite_sha256), ("c" * 64, "s" * 64))
        self.assertIn("| W-UAT-3 | 2 | 2 | 2 | 1 | m |", harness.grading.answers_markdown(answers))

    def test_the_two_turn_case_gets_one_packet_with_both_turns_of_every_scenario(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory) / "run-1"
            folder.mkdir()
            summary = {"model": "m", "server": "real", "case": "zurich-registration", "scenarios": {
                "work-first": {"turn_1": {"texts": ["When do you arrive?"]}, "turn_2": {"texts": ["By 15 September 2026."]}},
                "fourteen-days-first": {"turn_1": {"texts": ["When did you arrive?"]}, "turn_2": {"texts": ["By 15 September."]}}}}
            (folder / "summary.json").write_text(json.dumps(summary), encoding="utf-8")
            (folder / "work-first-turn-1.jsonl").write_text(json.dumps({"type": "tool_use", "part": {
                "tool": "swiss_tip_search", "state": {"input": {"query": "register"}, "output": json.dumps({"results": []})}}}) + "\n",
                encoding="utf-8")
            with unittest.mock.patch("builtins.print"):
                harness.write_grading_packets([directory])
            packet = (folder / "grading-request.md").read_text(encoding="utf-8")
        self.assertIn("# Grading request: UAT-1 `zurich-registration`", packet)
        self.assertIn("### work-first, turn 1", packet)
        self.assertIn("### fourteen-days-first, turn 2 (expected: 14 days after arrival", packet)
        self.assertIn("By 15 September 2026.", packet)
        self.assertIn("- **A6**", packet)
        self.assertIn("`search` `{\"query\": \"register\"}`", packet)

    def test_dated_prompt_states_today_unless_the_case_must_not_know_it(self):
        today = harness.date(2026, 9, 15)
        tax = harness.WALLISELLEN_CASES["wallisellen-tax-rate"]
        self.assertIn("Today's date is 2026-09-15", harness.prompt_for(tax, "real", today))
        self.assertIn("Today's date is 2026-09-15", harness.prompt_for(tax, "none", today))
        undated = harness.WALLISELLEN_CASES["wallisellen-variant-museum-no-date"]
        self.assertNotIn("2026-09-15", harness.prompt_for(undated, "real", today))
        self.assertNotIn("{", harness.prompt_for(undated, "real", today))

    def test_groups_expand_in_order_without_repeats(self):
        cases = harness.resolve_cases(["wallisellen-tax-rate", "wallisellen-primary"])
        self.assertEqual(cases[0], "wallisellen-tax-rate")
        self.assertEqual(len(cases), 7)

    def test_unserved_details_compare_the_answer_with_the_tool_outputs(self):
        output = json.dumps({"citations": [{"url": "https://www.wallisellen.ch/umzug"}],
                             "facts": [{"statement": "Umwelt at 044 832 62 10 and umwelt@wallisellen.ch; CHF 1,656,196."}]})
        turn = harness.turn_from_lines([json.dumps({"type": "tool_use", "part": {
            "tool": "swiss_tip_resolve", "state": {"status": "completed", "input": {}, "output": output}}})], 0)
        served = {kind: set(values) for kind, values in turn["served_details"].items()}
        answer = ("See [the page](https://wallisellen.ch/umzug/) or wallisellen.ch, call +41 44 832 62 10, "
                  "write to umwelt@wallisellen.ch. The fee is CHF 100. Also https://www.edah.admin.ch/topics and "
                  "0800 123 456, opening Fr. 07:00-14:00.")
        missing = harness.unserved(answer, served)
        self.assertEqual(missing["urls"], ["edah.admin.ch/topics"])
        self.assertEqual(missing["emails"], [])
        self.assertEqual(missing["phones"], ["0800123456"])
        self.assertEqual(missing["amounts"], ["100"])
        self.assertEqual(harness.unserved("CHF 1'656'196.-", served)["amounts"], [])

    def test_strict_checks_require_disclosures_when_facts_were_served(self):
        def line(review_status):
            output = json.dumps({"status": "SUPPORTED", "executed_scope": {"municipality_id": "CH-ZH-69"},
                                 "results": [{"concept_id": "tax-rate-and-finance", "status": "SUPPORTED",
                                              "review_status": review_status,
                                              "facts": [{"statement": "93%, 95%, 188% without church taxes."}]}],
                                 "citations": [{"url": "https://www.wallisellen.ch/steuerfuss"}]})
            return json.dumps({"type": "tool_use", "part": {"tool": "swiss_tip_resolve", "state": {
                "status": "completed", "input": {"concept_ids": ["tax-rate-and-finance"]}, "output": output}}})
        base = ("No: 93% is the municipal rate, the canton adds 95%, 188% combined without church taxes "
                "(https://www.wallisellen.ch/steuerfuss).")
        translated = base + " These statements are English paraphrases, not an official translation."
        disclosed = base + " These statements are unreviewed English paraphrases, not an official translation."
        # An unreviewed fact needs both disclosures; a reviewed one only the translation note.
        for review_status, text, grounded in ((None, base, False), (None, translated, False), (None, disclosed, True),
                                              ("human-reviewed", base, False), ("human-reviewed", translated, True)):
            with self.subTest(review_status=review_status, text=text):
                turn = harness.turn_from_lines([line(review_status), json.dumps({"type": "text", "part": {"text": text}})], 0)
                verdict = harness.assess_single_turn("wallisellen-tax-rate", turn, harness.MCP_NAME)
                self.assertEqual(verdict["grounded"], grounded)

    def test_a_place_case_is_judged_by_the_place_the_facts_were_served_for(self):
        self.assertEqual([harness.is_place_name(value) for value in
                          ("Wallisellen", "Kanton Zürich", "St. Gallen", "CH", "zh", "CH-ZH", "CH-ZH-69", "ZH-69", "69", "", None)],
                         [True, True, True, False, False, False, False, False, False, False, False])

        def resolve(jurisdiction, scope, status="SUPPORTED", error=None):
            body = {"error": {"code": error}} if error else {
                "status": status, "executed_scope": scope,
                "results": [{"concept_id": "moving-registration", "status": status, "review_status": "human-reviewed",
                             "facts": [{"statement": "Report the move within 14 days."}] if status == "SUPPORTED" else []}],
                "citations": [{"url": "https://www.wallisellen.ch/umzug"}]}
            return json.dumps({"type": "tool_use", "part": {"tool": "swiss_tip_resolve", "state": {
                "status": "completed", "input": {"concept_ids": ["moving-registration"], "jurisdiction": jurisdiction},
                "output": json.dumps(body)}}})

        answer = json.dumps({"type": "text", "part": {"text": (
            "Report the move within 14 days; a move within Switzerland can be reported through eUmzugCH "
            "(https://www.wallisellen.ch/umzug). These statements are English paraphrases, not an official translation.")}})
        placed = {"country_code": "CH", "canton_code": "CH-ZH", "municipality_id": "CH-ZH-69", "city": "Wallisellen"}
        canton = {"country_code": "CH", "canton_code": "CH-ZH", "not_recognised": {"city": "Walisellen ZH 8304"}}

        def assess(*lines):
            return harness.assess_single_turn("wallisellen-place-named", harness.turn_from_lines([*lines, answer], 0), harness.MCP_NAME)

        named = assess(resolve({"city": "Wallisellen"}, placed))
        self.assertEqual((named["grounded"], named["resolves_name_municipality"], named["sent_place_names"]), (True, True, True))
        self.assertEqual((named["jurisdictions_sent"], named["places_not_recognised"], named["rejected_places"]),
                         ([{"city": "Wallisellen"}], [], 0))
        # A caller that knows the code and sends it is right too: how the place was put is recorded, not judged.
        coded = assess(resolve({"canton_code": "CH-ZH", "municipality_id": "CH-ZH-69"}, placed))
        self.assertEqual((coded["grounded"], coded["sent_place_names"]), (True, False))
        # A name the server could not place, or one it rejected, followed by a corrected request does no harm.
        corrected = assess(resolve({"canton": "Zurich", "city": "Walisellen ZH 8304"}, canton, status="OUT_OF_COVERAGE"),
                           resolve({"city": "Buchs"}, None, error="INVALID_ARGUMENT"), resolve({"city": "Wallisellen"}, placed))
        self.assertEqual((corrected["grounded"], corrected["places_not_recognised"], corrected["rejected_places"]),
                         (True, [{"city": "Walisellen ZH 8304"}], 1))
        # Facts served for the place the user left, or for the canton only, are not the user's.
        winterthur = dict(placed, municipality_id="CH-ZH-230", city="Winterthur")
        for jurisdiction, scope in (({"city": "Winterthur"}, winterthur), ({"canton": "Zurich"}, {"country_code": "CH", "canton_code": "CH-ZH"})):
            with self.subTest(jurisdiction=jurisdiction):
                wrong = assess(resolve(jurisdiction, scope))
                self.assertEqual((wrong["grounded"], wrong["resolves_name_municipality"]), (False, False))

    def test_rate_limited_sessions_are_retried_and_recorded(self):
        limit = {"type": "error", "error": {"name": "APIError", "data": {
            "message": "Rate limit exceeded", "statusCode": 429, "isRetryable": True}}}
        failed = {"texts": [], "tool_calls": [], "errors": [limit]}
        answered = {"texts": ["answer"], "tool_calls": [], "errors": []}
        self.assertTrue(harness.provider_failure(failed))
        self.assertFalse(harness.provider_failure(answered))
        self.assertFalse(harness.provider_failure({"texts": [], "tool_calls": [], "errors": [{"type": "error", "error": {}}]}))
        upstream = {"type": "error", "error": {"name": "APIError", "data": {"statusCode": 400, "isRetryable": False}}}
        self.assertTrue(harness.provider_failure({"texts": [], "tool_calls": [], "errors": [upstream]}))
        turns = iter([failed, answered])
        args = harness.argparse.Namespace(provider_retries=2, retry_wait=0)
        with tempfile.TemporaryDirectory() as directory, \
                unittest.mock.patch.object(harness, "run_turn", side_effect=lambda *a: (Path(a[5]).write_text("x"), next(turns))[1]), \
                unittest.mock.patch.object(harness.time, "sleep"):
            transcript = Path(directory) / "case-turn-1.jsonl"
            turn, attempts = harness.run_turn_with_retry(args, "opencode", {}, Path(directory), [], "question", transcript)
            self.assertEqual(turn, answered)
            self.assertEqual([a["provider_failure"] for a in attempts], [True, False])
            self.assertTrue((Path(directory) / "case-turn-1.provider-failure-1.jsonl").is_file())

    def test_a_hung_session_is_killed_and_counts_as_a_provider_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            transcript = Path(directory) / "hung-turn-1.jsonl"
            hang = [sys.executable, "-c", "import time; time.sleep(30)"]
            real_popen = subprocess.Popen
            with unittest.mock.patch.object(harness.subprocess, "Popen",
                                            side_effect=lambda command, **kw: real_popen(hang, **kw)):
                turn = harness.run_turn("opencode", None, Path(directory), [], "question", transcript, timeout=0.5)
        self.assertTrue(turn["timed_out"])
        self.assertTrue(harness.provider_failure(turn))

    def test_resume_skips_only_answered_repetitions(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            for name, texts in (("run-1-real-r1", ["answer"]), ("run-2-real-r2", [])):
                (output / name).mkdir()
                (output / name / "summary.json").write_text(json.dumps(
                    {"scenarios": {"case": {"turn_1": {"texts": texts}}}}), encoding="utf-8")
            self.assertTrue(harness.answered_run_exists(output, 1, 3))
            self.assertFalse(harness.answered_run_exists(output, 2, 3))
            self.assertFalse(harness.answered_run_exists(output, 3, 3))

    def test_report_counts_rates_and_valid_grades(self):
        with tempfile.TemporaryDirectory() as directory:
            for index, (grounded, grade) in enumerate(((True, {"grader": "t", "trap_held": True, "criteria_pass": True,
                                                                "failed_criteria": [], "unsupported_claims": [], "note": ""}),
                                                       (False, {"trap_held": "yes"}))):
                folder = Path(directory) / f"run-{index}"
                folder.mkdir()
                summary = {"model": "m", "server": "real", "url": None, "scenarios": {"wallisellen-tax-rate": {
                    "turn_1": {"texts": ["answer"], "errors": []},
                    "assessment": {"grounded": grounded, "call_count": 3 + index, "result_bytes": 100,
                                   "within_budget": True, "no_unserved_details": grounded}}}}
                (folder / "summary.json").write_text(json.dumps(summary), encoding="utf-8")
                (folder / "grade.json").write_text(json.dumps(grade), encoding="utf-8")
            row = harness.grading.report([directory], harness.SINGLE_TURN_CASES)["rows"][0]
            self.assertEqual((row["sessions"], row["heuristic_grounded"], row["graded"], row["criteria_pass"]),
                             (2, "1/2", 1, "1/1"))
            self.assertEqual(row["median_calls"], 3.5)

    def test_report_reads_the_two_turn_budget_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory) / "run-0"
            folder.mkdir()
            summary = {"model": "m", "server": "real", "url": None, "scenarios": {"work-first": {
                "turn_1": {"texts": ["answer"], "errors": []},
                "assessment": {"turn1_call_count": 3, "turn1_result_bytes": 21571, "turn1_within_budget": False,
                               "turn2_names_expected_deadline": True}}}}
            (folder / "summary.json").write_text(json.dumps(summary), encoding="utf-8")
            row = harness.grading.report([directory], harness.SINGLE_TURN_CASES)["rows"][0]
            self.assertEqual((row["case"], row["median_calls"], row["median_bytes"], row["within_budget"]),
                             ("work-first", 3, 21571, "0/1"))

    def test_municipality_status_and_argument_checks_decide_grounding(self):
        final = "The reviewed facts say a move can be reported through eUmzugCH; from abroad you register in person."
        def turn(jurisdiction, status, reviewed_only):
            return {"texts": [final], "tool_calls": [{"tool": "swiss_tip_resolve", "status": "completed",
                    "input": {"concept_ids": ["moving-registration"], "jurisdiction": jurisdiction, "reviewed_only": reviewed_only},
                    "result": {"bytes": 10, "status": status, "per_concept": {"moving-registration": status}}}]}
        case = "wallisellen-probe-reviewed-only"
        good = harness.assess_single_turn(case, turn({"municipality_id": "CH-ZH-69"}, "SUPPORTED", True), harness.MCP_NAME)
        self.assertTrue(good["grounded"])
        for bad in (turn({"canton_code": "CH-ZH"}, "SUPPORTED", True),
                    turn({"municipality_id": "CH-ZH-69"}, "OUT_OF_COVERAGE", True),
                    turn({"municipality_id": "CH-ZH-69"}, "SUPPORTED", False)):
            with self.subTest(turn=bad["tool_calls"][0]["input"]):
                self.assertFalse(harness.assess_single_turn(case, bad, harness.MCP_NAME)["grounded"])
        normalized = turn({"canton_code": "ZH", "municipality_id": "69"}, "SUPPORTED", True)
        normalized["tool_calls"][0]["result"]["executed_scope"] = {"country_code": "CH", "canton_code": "CH-ZH",
                                                                   "municipality_id": "CH-ZH-69"}
        self.assertTrue(harness.assess_single_turn(case, normalized, harness.MCP_NAME)["resolves_name_municipality"])
        control = harness.assess_single_turn(case, {"texts": [final], "tool_calls": []}, None)
        self.assertTrue(control["grounded"])

    def test_a_cross_jurisdiction_case_fails_when_facts_were_resolved_for_another_place(self):
        bern, winterthur = harness.SINGLE_TURN_CASES["bern-short-contract-permit"], harness.SINGLE_TURN_CASES["winterthur-registration"]
        # The user's place comes from the suite's resolve steps, for every case that carries A10 and for no other.
        self.assertEqual(bern["user_jurisdiction"], {"canton_code": "CH-BE"})
        self.assertEqual(winterthur["user_jurisdiction"], {"canton_code": "CH-ZH", "municipality_id": "CH-ZH-230"})
        self.assertEqual({name for name, spec in harness.SINGLE_TURN_CASES.items() if spec.get("user_jurisdiction")},
                         {name for name, spec in harness.SINGLE_TURN_CASES.items() if "A10" in spec["criteria"]})
        final = ("You get a short-stay permit L. Register with your municipality within 14 days "
                 "(https://www.sem.admin.ch/sem/de/home/themen/fza_schweiz-eu-efta/eu-efta_buerger_schweiz/faq.html).")
        def turn(*scopes):
            return {"texts": [final], "tool_calls": [{"tool": "swiss_tip_resolve", "status": "completed",
                    "input": {"concept_ids": ["eu-employment-registration-deadline"]},
                    "result": {"bytes": 10, "status": status, "executed_scope": scope,
                               "per_concept": {"eu-employment-registration-deadline": status}}} for scope, status in scopes]}
        case = "bern-short-contract-permit"
        canton_bern = ({"country_code": "CH", "canton_code": "CH-BE"}, "SUPPORTED")
        inside = [[canton_bern],
                  [({"country_code": "CH"}, "SUPPORTED")],
                  [({"country_code": "CH", "canton_code": "CH-BE", "municipality_id": "CH-BE-351"}, "SUPPORTED")],
                  # A request for Zurich that returned no facts, corrected afterwards.
                  [({"country_code": "CH", "canton_code": "CH-ZH"}, "OUT_OF_COVERAGE"), canton_bern]]
        for scopes in inside:
            with self.subTest(scopes=scopes):
                verdict = harness.assess_single_turn(case, turn(*scopes), harness.MCP_NAME)
                self.assertTrue(verdict["resolves_stay_in_user_jurisdiction"])
                self.assertTrue(verdict["grounded"])
        for scope in ({"country_code": "CH", "canton_code": "CH-ZH"},
                      {"country_code": "CH", "canton_code": "CH-ZH", "municipality_id": "CH-ZH-261"}):
            with self.subTest(scope=scope):
                verdict = harness.assess_single_turn(case, turn((scope, "SUPPORTED")), harness.MCP_NAME)
                self.assertFalse(verdict["resolves_stay_in_user_jurisdiction"])
                self.assertFalse(verdict["grounded"])
        # Inside the canton, the cantonal level stays the user's and the city's does not.
        user = winterthur["user_jurisdiction"]
        self.assertFalse(harness.outside_jurisdiction({"canton_code": "CH-ZH"}, user))
        self.assertFalse(harness.outside_jurisdiction({"canton_code": "CH-ZH", "municipality_id": "CH-ZH-230"}, user))
        self.assertTrue(harness.outside_jurisdiction({"canton_code": "CH-ZH", "municipality_id": "CH-ZH-261"}, user))
        # A Zurich answer carried over to Bern is caught by the case's must-not patterns as well.
        leaked = turn(({"country_code": "CH", "canton_code": "CH-BE"}, "SUPPORTED"))
        leaked["texts"] = [final + " The Migration Office is at Berninastrasse 45, 8090 Zürich."]
        self.assertFalse(harness.assess_single_turn(case, leaked, harness.MCP_NAME)["avoids_zurich_migration_office"])

    def test_child_environment_points_pwd_at_the_workspace(self):
        parent = {"PWD": str(harness.ROOT), "PATH": "unchanged"}
        env = harness.child_environment(parent, Path("workspace"))
        self.assertEqual(env["PWD"], "workspace")
        self.assertEqual(env["PATH"], "unchanged")
        self.assertEqual(parent["PWD"], str(harness.ROOT))

    def test_a_quoted_premise_is_not_an_assertion(self):
        pattern = r"(?:only|limited) (?:to|for) (?:residents )?(?:aged )?75"
        self.assertFalse(harness.asserted(pattern, 'Your claim: "LUNAplus is only for residents aged 75 or older"'))
        self.assertTrue(harness.asserted(pattern, "LUNAplus is only for residents aged 75 or older."))

    def test_unicode_json_counts_utf8_bytes_and_records_actual_fallback(self):
        output = json.dumps({"query": "居留许可 Zürich", "retrieval_mode": "lexical-fallback",
                             "fallback_reason": "local model unavailable", "results": []}, ensure_ascii=False)
        summary = harness.result_summary(output)
        self.assertEqual(summary["bytes"], len(output.encode("utf-8")))
        self.assertGreater(summary["bytes"], len(output))
        self.assertEqual(summary["retrieval_mode"], "lexical-fallback")
        self.assertEqual(summary["fallback_reason"], "local model unavailable")

    def test_unicode_nonobject_json_and_plain_text_count_utf8_bytes(self):
        for output in ('["瑞士"]', '"Zürich"', "瑞士 - Zürich"):
            with self.subTest(output=output):
                self.assertEqual(harness.result_summary(output), {"bytes": len(output.encode("utf-8"))})
        self.assertIsNone(harness.result_summary(None))

    def test_resolution_and_error_summaries_keep_existing_fields(self):
        summary = harness.result_summary(json.dumps({"status": "SUPPORTED", "results": [
            {"concept_id": "deadline", "status": "SUPPORTED", "facts": [{"fact_id": "deadline-1"}]}]}))
        self.assertEqual(summary["status"], "SUPPORTED")
        self.assertEqual(summary["per_concept"], {"deadline": "SUPPORTED"})
        self.assertEqual(summary["fact_count"], 1)
        self.assertIsNone(summary["retrieval_mode"])
        self.assertEqual(harness.result_summary('{"error":{"code":"INVALID_ARGUMENT"}}')["code"], "INVALID_ARGUMENT")


if __name__ == "__main__":
    unittest.main()
