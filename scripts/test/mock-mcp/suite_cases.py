"""The harness cases come from the packs' acceptance suites, releases/<pack>/acceptance.yaml.

A suite case holds the question as typed, the expected answer, the trap and the answer block: the IDs of the
general criteria a grader applies, the must-mention and must-not patterns, the URL fragments the answer must cite
and the concepts the caller must resolve (docs/architecture/acceptance-gate.md, sections 2 and 4). This module
turns such a case into the dict the harness assesses and adds what only the harness knows: the CLI name of the
case, the release it runs on, the system prompts, the language assessment and the tool checks. A suite case
without an answer block is not a harness case.
"""

from pathlib import Path

from swisstip.build.acceptance import load_acceptance
from swisstip.core.acceptance import AcceptanceFile, Case

ROOT = Path(__file__).resolve().parents[3]
SUITE_PATHS = {pack: ROOT / "releases" / pack / "acceptance.yaml" for pack in ("mvp-zurich", "mvp-wallisellen")}
RELEASE_PATHS = {pack: ROOT / "releases" / pack / "release.json" for pack in SUITE_PATHS}

# CLI names of the Zurich cases, as the records under .local/experiments/ use them, to their suite IDs.
ZURICH_NAMES = {
    "zurich-registration": "UAT-1",
    "german-work-permit": "UAT-2e",
    "family-child-deadline": "UAT-3",
    "marriage-separation": "UAT-4",
    "settlement-after-l-permit": "UAT-5",
    "social-assistance-permit": "UAT-6",
    "swiss-german-family-permit": "UAT-7",
    # The extension cases of 15 September 2026, not yet run.
    "ahv-refund-leaving": "UAT-8",
    "pension-fund-cash-out": "UAT-9",
    "tax-at-source-threshold": "UAT-10",
    "german-tax-at-source-marriage": "UAT-11",
    "foreign-licence-twelve-months": "UAT-12",
    "control-drive-licence": "UAT-13",
    "health-insurance-first-months": "UAT-14",
    "premium-reduction-arrival": "UAT-15",
    "naturalisation-b-permit": "UAT-16",
    "german-facilitated-naturalisation": "UAT-17",
    # The office-contact cases of 17 September 2026, not yet run.
    "migration-office-hours": "UAT-18",
    "migration-office-email": "UAT-19",
    "road-office-oerlikon": "UAT-20",
    "population-office-saturday": "UAT-21",
    "german-sva-visit": "UAT-22",
    "german-tax-at-source-contact": "UAT-23",
    # The daily-life cases of 17 September 2026, not yet run.
    "dog-moving-in": "UAT-24",
    "rubbish-bags": "UAT-25",
    "sofa-disposal": "UAT-26",
    "recycling-centre-saturday-cash": "UAT-27",
    "blue-zone-lunchtime": "UAT-28",
    "german-car-move": "UAT-29",
    "kindergarten-cut-off": "UAT-30",
    "german-tax-access-code": "UAT-31",
    "serafe-without-tv": "UAT-32",
    "ambulance-costs": "UAT-33",
    "road-office-hours": "UAT-34",
    # The cross-jurisdiction cases (another canton, another Zurich municipality), not yet run.
    "bern-short-contract-permit": "UAT-35",
    "aargau-commuter-registration": "UAT-36",
    "german-licence-st-gallen": "UAT-37",
    "bern-naturalisation": "UAT-38",
    "lucerne-premium-reduction": "UAT-39",
    "german-zug-tax-at-source": "UAT-40",
    "bern-migration-office": "UAT-41",
    "winterthur-registration": "UAT-42",
    "uster-dog-move": "UAT-43",
    "german-kloten-car-parking": "UAT-44",
    # The entry-and-visa cases of 17 September 2026, not yet run.
    "schengen-days-used": "UAT-45",
    "work-visa-two-years": "UAT-46",
    "schengen-visa-fee": "UAT-47",
    "etias-and-passport-stamp": "UAT-48",
    "visa-duty-one-nationality": "UAT-49",
    "l-permit-family-zurich": "UAT-50",
    # The voting-rights and tax-at-source tariff cases of 18 September 2026, not yet run.
    "c-permit-city-vote": "UAT-51",
    "winterthur-tax-at-source-rate": "UAT-52",
    "german-bern-voting-rights": "UAT-53",
    # The expat-life cases of 18 September 2026, not yet run.
    "zurich-education-allowance": "UAT-54",
    "paternity-leave": "UAT-55",
    "four-month-deposit": "UAT-56",
    "german-rent-increase-email": "UAT-57",
    "winterthur-initial-rent": "UAT-58",
    "brazilian-fiancee-marriage": "UAT-59",
    "leaving-zurich-for-good": "UAT-60",
    "pillar-3a-leaving": "UAT-61",
    "unemployment-ten-months": "UAT-62",
    "six-hours-skiing-accident": "UAT-63",
    "german-moving-goods-customs": "UAT-64",
    # The five-year settlement cases of 22 September 2026, not yet run.
    "german-citizen-settlement": "UAT-65",
    "american-settlement-five-years": "UAT-66",
    # The integration cases of 22 September 2026, not yet run.
    "winterthur-german-course": "UAT-67",
    "family-first-information": "UAT-68",
    "racist-remarks-at-work": "UAT-69",
    "uster-festival-funding": "UAT-70",
    "tamil-association": "UAT-71",
    # The customs cases of 23 September 2026, not yet run.
    "coffee-machine-konstanz": "UAT-72",
    "meat-and-wine-from-italy": "UAT-73",
    "bicycle-declaration": "UAT-74",
    "laptop-from-germany": "UAT-75",
    "small-parcels-charge": "UAT-76",
    "jacket-sent-back": "UAT-77",
    "moving-goods-from-boston": "UAT-78",
    "arriving-with-two-dogs": "UAT-79",
    "visitor-watch-refund": "UAT-80",
    # The health-insurance cases of 23 September 2026, not yet run.
    "broken-arm-bill": "UAT-81",
    "family-doctor-model": "UAT-82",
    "switch-insurer-after-rise": "UAT-83",
    "premium-differs-colleague": "UAT-84",
    "glasses-supplementary": "UAT-85",
    "unpaid-premiums": "UAT-86",
    "konstanz-cross-border-worker": "UAT-87",
    "three-weeks-in-italy": "UAT-88",
    "pensioner-in-portugal": "UAT-89",
    "doctor-bill-to-patient": "UAT-90",
    "civilian-service-premiums": "UAT-91",
    # The work and unemployment cases of 23 September 2026, not yet run.
    "notice-arrived": "UAT-92",
    "job-applications-per-month": "UAT-93",
    "benefit-duration": "UAT-94",
    "lower-paid-job": "UAT-95",
    "employer-bankrupt-wages": "UAT-96",
    "course-while-unemployed": "UAT-97",
    "benefit-runs-out": "UAT-98",
    "three-years-in-germany": "UAT-99",
    "short-time-work": "UAT-100",
    "rav-vacancies-first": "UAT-101",
    "winterthur-rav": "UAT-102",
    # The AHV and pension cases of 23 September 2026, not yet run.
    "non-working-spouse-ahv": "UAT-103",
    "going-self-employed": "UAT-104",
    "ahv-account-statement": "UAT-105",
    "eight-years-abroad": "UAT-106",
    "early-retirement-63": "UAT-107",
    "reference-age-next-spring": "UAT-108",
    "survivors-pension": "UAT-109",
    "italy-switzerland-career": "UAT-110",
    "pension-system-explained": "UAT-111",
    "zurich-ahv-office": "UAT-112",
    # The cantonal registration cases of 23 September 2026, not yet run.
    "lausanne-registration": "UAT-113",
    "italian-lugano-registration": "UAT-114",
    "german-schwyz-registration": "UAT-115",
    "french-valais-canton-change": "UAT-116",
    # The Lugano waste case of 24 September 2026, not yet run.
    "italian-lugano-waste": "UAT-117",
    # The Basel and St. Gallen waste cases of 24 September 2026, not yet run.
    "basel-waste-collection": "UAT-118",
    "german-st-gallen-waste": "UAT-119",
}

# The general criteria of docs/product/user-acceptance-tests.md, quoted in the grading packets by ID.
ZURICH_CRITERIA = {
    "A1": "Every statement in the answer traces to a served fact and its cited official page.",
    "A2": "The answer cites the URLs the server returned.",
    "A3": "Nothing the release does not know is invented: a missing user fact is asked for, an uncovered question is "
          "declined by name (no computed date before the user supplied the inputs; out-of-scope questions answered "
          "with the scope statement).",
    "A4": "The server composes no answer: the tool results carry facts, excerpts, citations, statuses and guidance "
          "only, and the answer is built from them.",
    "A5": "Review status is visible: the answer passes on the review status of the served facts.",
    "A6": "Efficiency: the case is answered within the call and byte budget (turn 1 of UAT-1 at most 3 calls and "
          "20 KB; the single-turn cases at most 4 calls and 30 KB).",
    "A7": "The grounded answer states the exception in the law that the popular answer misses.",
    "A8": "The answer is in the question's language, and the search was sent in that language rather than "
          "translated into English first.",
    "A9": "A negative the cited page states (no e-mail address, closed on Saturday, no appointment needed, a location "
          "missing from the published list) is reported as the office's own statement, not as information the "
          "service lacks, and nothing is invented in its place.",
    "A10": "The answer is scoped to the user's canton and municipality: it gives everything the release serves for "
           "that place (federal facts in every canton, Canton of Zurich facts in every Zurich municipality, the "
           "canton's own entry in SEM's directory), names the cantonal or municipal part the release does not "
           "publish for that place instead of filling it, and carries over no office, address, telephone number, "
           "opening hours, deadline, fee, form or procedure published for another canton or municipality; no "
           "resolve that returned facts was sent for another canton or municipality than the user's.",
}


def load_suite(pack: str) -> AcceptanceFile:
    return load_acceptance(SUITE_PATHS[pack])


def user_jurisdiction(case: Case) -> dict[str, str]:
    """The user's place in a cross-jurisdiction case (criterion A10): the one jurisdiction every resolve step names.

    The suite is the only place that states it, so the harness cannot drift from the replayed requests."""
    places = {tuple(sorted(step.resolve.jurisdiction.items())) for step in case.steps if step.resolve is not None}
    place = dict(next(iter(places))) if len(places) == 1 else {}
    if not place.get("canton_code"):
        raise ValueError(f"suite case {case.case_id} carries A10, so every resolve step must name the same canton")
    return place


def case_spec(case: Case, criteria_texts: dict[str, str], **extras) -> dict:
    """The harness dict of a suite case: its question, expectations and patterns, plus the harness-only extras."""
    if case.answer is None:
        raise ValueError(f"suite case {case.case_id} has no answer block and cannot be run by the harness")
    answer = case.answer
    if "A10" in answer.criteria:
        extras = {"user_jurisdiction": user_jurisdiction(case), **extras}
    return {"acceptance_id": case.case_id, "question": case.question, "expected": case.expected_answer,
            "trap": case.trap or "", "must_mention": dict(answer.must_mention), "must_not": dict(answer.must_not),
            "cites": dict(answer.cites),
            "resolved": [tuple(item) if isinstance(item, list) else item for item in answer.resolved],
            "criteria": {key: criteria_texts[key] for key in answer.criteria}, **extras}


def zurich_cases(suite: AcceptanceFile, extras: dict[str, dict]) -> dict[str, dict]:
    """Every Zurich case by CLI name, including the two-turn zurich-registration case (UAT-1)."""
    cases = {}
    for name, case_id in ZURICH_NAMES.items():
        case = suite.case(case_id)
        if case is None:
            raise ValueError(f"the mvp-zurich suite has no case {case_id} for the harness case {name}")
        cases[name] = case_spec(case, ZURICH_CRITERIA, release=RELEASE_PATHS["mvp-zurich"], **extras.get(name, {}))
    return cases
