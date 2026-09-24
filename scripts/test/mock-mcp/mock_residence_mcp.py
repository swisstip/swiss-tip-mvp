"""Mock Swiss TIP (Swisscom Trusted Information Platform) MCP server with hardcoded content for one scenario.

The server speaks MCP over stdio and advertises the four tools of the target
design (get_coverage, search, resolve, get_evidence) with the request and
result models from contracts.py. Every answer comes from the constants in this
file; it never reads a release file or the network. Diagnostics
and one log line per call (tool, status, bytes, latency) go to stderr; stdout
carries the protocol.

Covered scenario: EU/EFTA nationals taking up employment in Switzerland must
register with their municipality within 14 days of arrival and before starting
work, with the Canton of Zurich and City of Zurich procedures. The resolve
result tells the calling assistant which user facts are still missing (arrival
date, first working day) and how to decide which limit binds. The decision
itself is left to the caller.
"""

import asyncio
from datetime import date, timedelta
import json
import logging
import re
import sys
import time

from mcp import types
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server
from pydantic import ValidationError

from contracts import (
    ConceptResolution, ConceptSummary, ContextField, CoverageGap, CoverageRoot, CoverageTopic,
    DecisionRule, ErrorBody, ErrorCode, Evidence, Fact, FreshnessPolicy, GetCoverageRequest,
    GetEvidenceRequest, GetEvidenceResult, MissingContext, RequiredUserFact, ResolveRequest, ResolveResult,
    SCHEMA_VERSION, SearchHit, SearchRequest, SearchResult, Status, TOOL_CONTRACTS, TOOL_DESCRIPTIONS, ToolError,
    TopicSummary, ValidationIssue, page_citations, shared_review, tool_input_schema, tool_output_schema,
)
from contracts import ExecutedScope
from swisstip.core.places import PlaceError, PlaceIndex  # importable once `contracts` has found the core package
from swisstip.core.release import Place, PlaceRegister

SERVER_NAME = "swiss-tip-mock"
SERVER_VERSION = "0.1.0"
RELEASE_ID = "mock-residence-registration-2026-09-11"
TOPIC_ID = "residence"
SNAPSHOT_DATE = date(2026, 9, 11)
FRESHNESS = FreshnessPolicy(snapshot_date=SNAPSHOT_DATE, max_age_days=60,
                            stale_from=SNAPSHOT_DATE + timedelta(days=60))
MOCK_NOTE = ("Mock server: hardcoded content for one scenario, taken from official pages saved on "
             "2026-09-11. Not the curated knowledge base and not legal advice.")

CITY_OF_ZURICH = "CH-ZH-261"

# The places the mock can be told about in names, as hardcoded as the rest: the real server reads the whole official
# register from its release. A place missing here is reported as not recognised, like a misspelt one there.
PLACES = PlaceIndex(PlaceRegister(
    title="Mock place register", publisher="Mock", url="https://example.invalid/mock-places", accessed_on=SNAPSHOT_DATE,
    raw_sha256="0" * 64, generic_words=["canton of", "Kanton", "city of", "Stadt", "Gemeinde"],
    places=[Place(code="CH", name="Switzerland", aliases=["Schweiz", "Suisse", "Svizzera"]),
            Place(code="CH-ZH", name="Zürich", aliases=["Zurigo"]), Place(code="CH-BE", name="Bern / Berne"),
            Place(code="CH-GE", name="Genève", aliases=["Geneva", "Genf"]), Place(code="CH-VD", name="Vaud", aliases=["Waadt"]),
            Place(code="CH-BS", name="Basel-Stadt", aliases=["Basel"]), Place(code="CH-LU", name="Luzern", aliases=["Lucerne"]),
            Place(code=CITY_OF_ZURICH, name="Zürich", aliases=["Zurigo"]), Place(code="CH-ZH-230", name="Winterthur"),
            Place(code="CH-ZH-69", name="Wallisellen"), Place(code="CH-BE-351", name="Bern", aliases=["Berne"]),
            Place(code="CH-GE-6621", name="Genève", aliases=["Geneva", "Genf"]), Place(code="CH-VD-5586", name="Lausanne"),
            Place(code="CH-BS-2701", name="Basel", aliases=["Basle"]), Place(code="CH-LU-1061", name="Luzern", aliases=["Lucerne"])]),
    ["CH", "CH-ZH", CITY_OF_ZURICH])

EVIDENCE = {
    "e-sem-faq-en": {
        "source_title": "SEM - FAQ: EU/EFTA citizens in Switzerland (English)",
        "publisher": "State Secretariat for Migration SEM",
        "language": "en",
        "original_excerpt": (
            "Within 14 days of their arrival and before actually taking up work, nationals of "
            "EU/EFTA states have to register with the local authorities of the commune in which "
            "they are residing and apply for a residence permit. A valid ID or passport and a "
            "written confirmation of employment (e.g. the contract of employment containing "
            "details of the duration of employment and the number of working hours) have to be "
            "presented."),
        "url": "https://www.sem.admin.ch/sem/en/home/themen/fza_schweiz-eu-efta/eu-efta_buerger_schweiz/faq.html",
    },
    "e-sem-faq-de": {
        "source_title": "SEM - FAQ: EU/EFTA-Buergerinnen und -Buerger in der Schweiz (Deutsch)",
        "publisher": "Staatssekretariat fuer Migration SEM",
        "language": "de",
        "original_excerpt": (
            "Innert 14 Tagen nach ihrer Ankunft in der Schweiz und vor Stellenantritt, muessen "
            "sich die Buergerinnen und Buerger der EU/EFTA bei ihrer Wohngemeinde anmelden und "
            "eine Aufenthaltsbewilligung beantragen."),
        "url": "https://www.sem.admin.ch/sem/de/home/themen/fza_schweiz-eu-efta/eu-efta_buerger_schweiz/faq.html",
    },
    "e-aig-art12": {
        "source_title": "AIG (SR 142.20) Art. 12 Anmeldepflicht",
        "publisher": "Fedlex - Swiss federal law",
        "language": "de",
        "original_excerpt": (
            "Art. 12 Anmeldepflicht. 1 Auslaenderinnen und Auslaender, die eine Kurzaufenthalts-, "
            "Aufenthalts- oder Niederlassungsbewilligung benoetigen, muessen sich vor Ablauf des "
            "bewilligungsfreien Aufenthalts oder vor der Aufnahme einer Erwerbstaetigkeit bei der "
            "am Wohnort in der Schweiz zustaendigen Behoerde anmelden. [...] 3 Der Bundesrat "
            "bestimmt die Anmeldefristen."),
        "url": "https://www.fedlex.admin.ch/eli/cc/2007/758/de",
    },
    "e-vzae-art10": {
        "source_title": "VZAE (SR 142.201) Art. 10 Aufenthalt mit Anmeldung",
        "publisher": "Fedlex - Swiss federal law",
        "language": "de",
        "original_excerpt": (
            "Art. 10 Aufenthalt mit Anmeldung. 1 Zur Regelung des Aufenthalts muessen sich "
            "Auslaenderinnen und Auslaender innerhalb von 14 Tagen nach der Einreise bei der "
            "durch den Kanton bezeichneten Stelle anmelden [...]"),
        "url": "https://www.fedlex.admin.ch/eli/cc/2007/759/de",
    },
    "e-zh-eu-efta": {
        "source_title": "Kanton Zuerich - Aufenthalt fuer EU/EFTA-Staatsangehoerige",
        "publisher": "Kanton Zuerich, Migrationsamt",
        "language": "de",
        "original_excerpt": (
            "Als EU/EFTA-Angehoerige, die laenger als 90 Tage in der Schweiz arbeiten moechten, "
            "muessen Sie sich innerhalb von 14 Tagen persoenlich bei Ihrer Wohngemeinde anmelden."),
        "url": "https://www.zh.ch/de/migration-integration/aufenthalt/aufenthalt-fuer-euefta-staatsangehoerige.html",
    },
    "e-zh-weisung-fza": {
        "source_title": "Kanton Zuerich - Weisung Freizuegigkeitsabkommen EU-26, EFTA-Staaten, Ziff. 2.3 und 3.4.4",
        "publisher": "Kanton Zuerich, Migrationsamt",
        "language": "de",
        "original_excerpt": (
            "Betreffend Anmeldung bei der fuer den Wohnort zustaendigen Einwohnerkontrolle gelten "
            "die in Art. 12 AIG sowie in den Art. 9, 10, 12, 13, 15 und 16 VZAE vorgesehenen "
            "Verpflichtungen und Fristen. [...] Die Taetigkeit kann nach der persoenlichen "
            "Anmeldung und Gesuchseinreichung bei der Einwohnerkontrolle aufgenommen werden."),
        "url": "https://www.zh.ch/content/dam/zhweb/bilder-dokumente/themen/migration-integration/einreise-aufenthalt/weisungen/Freiz%C3%BCgigkeitsabkommen%20EU-26,%20EFTA-Staaten_IW.pdf",
    },
    "e-stadt-zh-zuzug": {
        "source_title": "Stadt Zuerich - Zuzug anmelden",
        "publisher": "Stadt Zuerich, Personenmeldeamt",
        "language": "de",
        "original_excerpt": (
            "Sie muessen sich innerhalb von 14 Tagen bei der Stadt Zuerich anmelden (Meldepflicht). "
            "Eine Anmeldung ist erst ab dem effektiven Einzug moeglich. [...] Fuer die Anmeldung "
            "aus dem Ausland muessen Sie einen Termin vereinbaren. Die Anmeldung findet "
            "persoenlich beim Personenmeldeamt Zuerich Sued statt."),
        "url": "https://www.stadt-zuerich.ch/de/lebenslagen/einwohner-services/umziehen-melden/zuzug.html",
    },
    "e-sem-factsheet-short-term": {
        "source_title": "SEM factsheet - Residence permits for EU/EFTA nationals (English)",
        "publisher": "State Secretariat for Migration SEM",
        "language": "en",
        "original_excerpt": (
            "Employment of up to three months per calendar year does not require a residence "
            "permit; such employment requires the electronic notification of short-term stays. "
            "The employer has to submit an online notification form no later than the day before "
            "starting work."),
        "url": "https://www.sem.admin.ch/dam/sem/en/data/eu/fza/personenfreizuegigkeit/factsheets/fs-bew-aufenthalt.pdf.download.pdf/fs-bew-aufenthalt.pdf",
    },
}

CONTEXT_SCHEMA = {
    "population": ContextField(
        enum=["EU_EFTA", "THIRD_COUNTRY"],
        description="EU_EFTA for citizens of an EU or EFTA state (for example Czech, German, Norwegian), "
                    "otherwise THIRD_COUNTRY."),
    "purpose": ContextField(
        enum=["EMPLOYMENT", "SELF_EMPLOYMENT", "NO_EMPLOYMENT", "FAMILY_REUNIFICATION"],
        description="Main purpose of the stay in Switzerland."),
    "employment_duration": ContextField(
        enum=["UP_TO_3_MONTHS", "MORE_THAN_3_MONTHS", "UNKNOWN"],
        description="Contract length. Jobs of up to three months per calendar year follow a different "
                    "notification procedure."),
}

# Concepts: id -> definition. A concept is published for exactly one jurisdiction
# and serves every place inside it (federal for any canton, cantonal for its
# municipalities, municipal only for that municipality).
CONCEPTS = {
    "residence.registration-after-arrival-eu-efta": {
        "jurisdiction": "CH",
        "label": "Registration with the municipality after arrival (EU/EFTA nationals taking up employment)",
        "description": "Federal deadline and order of steps: register with the municipality of residence and "
                       "apply for the permit within 14 days of arrival and before taking up work.",
        "aliases": ["Anmeldung bei der Wohngemeinde", "Anmeldefrist", "14 Tage", "14 days", "register stay",
                    "municipal registration", "Meldepflicht", "residence permit application EU citizen",
                    "Kreisbuero", "Einwohnerkontrolle"],
        "questions": ["By when must I register my stay with the municipal authority?",
                      "I start work in Zurich soon. When do I have to register?",
                      "Is the 14-day registration deadline counted from arrival or from the first working day?"],
        "required_context": ["population", "purpose"],
        "condition": {"population": "EU_EFTA", "purpose": "EMPLOYMENT"},
        "facts": [
            {"fact_id": "f-14-days-and-before-work",
             "statement": "EU/EFTA nationals taking up employment in Switzerland for more than three months "
                          "must register in person with the municipality of residence and apply for a "
                          "residence permit within 14 days of their arrival in Switzerland AND before taking "
                          "up work. Both limits apply at the same time.",
             "evidence_ids": ["e-sem-faq-en", "e-sem-faq-de", "e-aig-art12"]},
            {"fact_id": "f-period-starts-at-arrival",
             "statement": "The 14-day period starts on the day of arrival in Switzerland (moving in), not on "
                          "the first working day. The first working day does not define the arrival date.",
             "evidence_ids": ["e-sem-faq-en", "e-vzae-art10"]},
            {"fact_id": "f-register-before-work",
             "statement": "Work may only be taken up after registration with the competent authority at the "
                          "place of residence. Registration therefore has to be completed before the first "
                          "working day, even if fewer than 14 days have passed since arrival.",
             "evidence_ids": ["e-aig-art12"]},
            {"fact_id": "f-documents",
             "statement": "Bring a valid identity card or passport and the employer's written confirmation "
                          "of employment (for example the employment contract stating duration and working "
                          "hours).",
             "evidence_ids": ["e-sem-faq-en"]},
        ],
    },
    "residence.zh.registration-eu-efta": {
        "jurisdiction": "CH-ZH",
        "label": "Canton of Zurich: registration of EU/EFTA nationals taking up work",
        "description": "Cantonal procedure: personal registration with the municipality within 14 days; work "
                       "may start after registration and submission of the permit application.",
        "aliases": ["Zurich registration", "Kanton Zuerich Anmeldung", "Migrationsamt Zuerich", "Zuerich 14 Tage",
                    "Weisung Freizuegigkeitsabkommen", "EU/EFTA Zurich"],
        "questions": ["Where and how do I register in the canton of Zurich as an EU citizen?",
                      "Can I start work in Zurich before my registration?"],
        "required_context": ["population"],
        "condition": {"population": "EU_EFTA"},
        "facts": [
            {"fact_id": "f-zh-canton-14-days",
             "statement": "The canton of Zurich instructs EU/EFTA nationals who will work longer than 90 days "
                          "to register in person with their municipality within 14 days.",
             "evidence_ids": ["e-zh-eu-efta"]},
            {"fact_id": "f-zh-work-after-registration",
             "statement": "In the canton of Zurich the federal registration duties and deadlines apply; work "
                          "may be taken up after the personal registration and submission of the application "
                          "at the residents' registration office.",
             "evidence_ids": ["e-zh-weisung-fza"]},
        ],
    },
    "residence.zh.city-zurich-registration": {
        "jurisdiction": CITY_OF_ZURICH,
        "label": "City of Zurich: registering a move-in from abroad",
        "description": "Municipal procedure of the City of Zurich: 14-day notification duty, registration "
                       "only from the actual move-in date, appointment required when arriving from abroad.",
        "aliases": ["Stadt Zuerich Zuzug", "Personenmeldeamt", "Zuzug anmelden", "City of Zurich move in",
                    "Zurich city registration appointment", "Kreisbuero Zuerich"],
        "questions": ["How do I register my move to the City of Zurich?",
                      "Do I need an appointment to register in Zurich city?"],
        "required_context": [],
        "condition": None,
        "facts": [
            {"fact_id": "f-zh-city-14-days",
             "statement": "In the City of Zurich, new residents must register within 14 days (notification "
                          "duty).",
             "evidence_ids": ["e-stadt-zh-zuzug"]},
            {"fact_id": "f-zh-city-appointment",
             "statement": "In the City of Zurich, registration is possible only from the actual move-in date, "
                          "and registration after arriving from abroad requires a booked appointment at the "
                          "Personenmeldeamt (in person).",
             "evidence_ids": ["e-stadt-zh-zuzug"]},
        ],
    },
    "residence.short-term-notification-eu-efta": {
        "jurisdiction": "CH",
        "label": "Short-term employment up to three months (EU/EFTA nationals): notification instead of permit",
        "description": "Federal rule: for employment of up to three months per calendar year no residence "
                       "permit is needed; the employer submits an online notification before work starts.",
        "aliases": ["Meldeverfahren", "notification procedure", "short-term stay", "90 days", "three months",
                    "Kurzaufenthalt", "employer notification"],
        "questions": ["I have a three-month contract in Switzerland; do I need a permit?",
                      "What is the notification procedure for short assignments?"],
        "required_context": ["population"],
        "condition": {"population": "EU_EFTA"},
        "facts": [
            {"fact_id": "f-short-term-notification",
             "statement": "For employment of up to three months per calendar year, EU/EFTA nationals need no "
                          "residence permit. Instead the employer must notify the job online no later than "
                          "the day before work starts.",
             "evidence_ids": ["e-sem-factsheet-short-term"]},
        ],
    },
}

REQUIRED_USER_FACTS = [
    RequiredUserFact(
        name="arrival_date", status="NOT_PROVIDED_BY_SERVICE",
        instruction="Ask the user for the date on which they arrive (or arrived) in Switzerland. Never assume "
                    "the arrival date equals the first working day; people usually arrive earlier. Without the "
                    "arrival date the 14-day limit cannot be computed."),
    RequiredUserFact(
        name="first_working_day", status="NOT_PROVIDED_BY_SERVICE",
        instruction="Confirm the exact first working day; registration must be completed before it."),
    RequiredUserFact(
        name="employment_duration", status="UNKNOWN",
        instruction="If unknown, confirm that the contract exceeds three months; otherwise the short-term "
                    "notification procedure applies instead of this rule (concept "
                    "residence.short-term-notification-eu-efta)."),
]

DECISION_RULE = DecisionRule(
    description="The binding deadline is the EARLIER of two limits: (A) 14 days after the arrival date and "
                "(B) before the first working day.",
    steps=[
        "1. Obtain arrival_date and first_working_day from the user; do not guess them.",
        "2. Compute limit A = arrival_date + 14 days.",
        "3. Limit B = registration completed before the first working day, i.e. at the latest on the last "
        "working day of the office before the first working day.",
        "4. If limit B falls before limit A, tell the user to register before the first working day and name "
        "that date. Otherwise tell the user to register within 14 days of arrival and name the date of limit A.",
        "5. State both limits so the user understands which one binds, and note that registration is only "
        "possible after the actual move-in.",
    ])

SCOPE_STATEMENT = ("Residence permits and registration for foreign nationals in Switzerland: federal rules "
                   "(apply in every canton), Canton of Zurich procedures and the City of Zurich move-in "
                   "procedure. This mock release covers one scenario: EU/EFTA nationals taking up employment.")
OUT_OF_SCOPE = [
    "Third-country (non-EU/EFTA) nationals: not in this mock release",
    "Cantons other than Zurich beyond the federal rules",
    "Fees, processing times, office hours and appointment availability",
    "Visas for tourism, asylum, naturalisation",
    "Any topic outside residence permits and registration",
    "Legal advice",
]
OUT_OF_SCOPE_RESPONSE = ("Tell the user that this service does not cover their question, quote the scope "
                         "statement, and do not answer from general knowledge as if it were grounded.")


def jurisdiction_label(code):
    return {"CH": "CH (federal)", "CH-ZH": "CH-ZH (Canton of Zurich)", CITY_OF_ZURICH: "CH-ZH-261 (City of Zurich)"}[code]


def concept_summary(concept_id):
    concept = CONCEPTS[concept_id]
    return ConceptSummary(
        concept_id=concept_id, topic_id=TOPIC_ID, label=concept["label"], description=concept["description"],
        jurisdictions=[concept["jurisdiction"]], required_context=concept["required_context"])


def citations(evidence_ids):
    return page_citations([(evidence_id, dict(source_title=item["source_title"], publisher=item["publisher"],
                                              url=item["url"], language=item["language"], accessed_on=SNAPSHOT_DATE))
                           for evidence_id in evidence_ids for item in [EVIDENCE[evidence_id]]])


def invalid(exc):
    issues = [ValidationIssue(path=".".join(str(part) for part in error["loc"]) or "request",
                              message=error["msg"]) for error in exc.errors()]
    return ToolError(error=ErrorBody(code=ErrorCode.INVALID_ARGUMENT, issues=issues))


def argument_error(path, message):
    return ToolError(error=ErrorBody(code=ErrorCode.INVALID_ARGUMENT,
                                     issues=[ValidationIssue(path=path, message=message)]))


# --- tools ------------------------------------------------------------------


def get_coverage(request: GetCoverageRequest):
    if request.release_id not in (None, RELEASE_ID):
        return argument_error("release_id", f"Unknown release_id {request.release_id!r}; the active release is {RELEASE_ID!r}.")
    if request.parent_id is None:
        return CoverageRoot(
            release_id=RELEASE_ID, schema_version=SCHEMA_VERSION, scope_statement=SCOPE_STATEMENT,
            out_of_scope=OUT_OF_SCOPE, out_of_scope_response=OUT_OF_SCOPE_RESPONSE,
            jurisdictions=["CH", "CH-ZH", CITY_OF_ZURICH], languages=["en", "de"], freshness=FRESHNESS,
            topics=[TopicSummary(topic_id=TOPIC_ID,
                                 title="Residence permits and registration for foreign nationals",
                                 concept_count=len(CONCEPTS))],
            limitations=[MOCK_NOTE])
    if request.parent_id != TOPIC_ID:
        return argument_error("parent_id", f"Unknown parent_id {request.parent_id!r}; use {TOPIC_ID!r} or omit it.")
    return CoverageTopic(release_id=RELEASE_ID, topic_id=TOPIC_ID,
                         title="Residence permits and registration for foreign nationals",
                         concepts=[concept_summary(concept_id) for concept_id in CONCEPTS], limitations=[MOCK_NOTE])


STOPWORDS = {"a", "an", "and", "as", "at", "by", "do", "for", "i", "in", "is", "it", "my", "of", "on", "or",
             "the", "to", "when", "with", "should", "must", "have", "need", "can", "am", "me", "next", "week",
             "latest", "der", "die", "das", "und", "ich", "bei", "in", "mit", "wann", "muss"}


def tokens(text):
    return {token for token in re.findall(r"[a-z0-9]+", text.lower()) if token not in STOPWORDS and len(token) > 1}


def search(request: SearchRequest):
    query = tokens(request.query)
    hits = []
    for concept_id, concept in CONCEPTS.items():
        fields = {"label": (concept["label"], 3.0), "aliases": (" ".join(concept["aliases"]), 2.0),
                  "questions": (" ".join(concept["questions"]), 2.0), "description": (concept["description"], 1.0)}
        score = 0.0
        matched = []
        for name, (text, weight) in fields.items():
            overlap = query & tokens(text)
            if overlap:
                score += weight * len(overlap)
                matched.append(name)
        if score:
            hits.append((score, concept_id, matched))
    hits.sort(key=lambda item: (-item[0], item[1]))
    results = [SearchHit(concept_id=concept_id, topic_id=TOPIC_ID, label=CONCEPTS[concept_id]["label"],
                         description=CONCEPTS[concept_id]["description"],
                         jurisdictions=[CONCEPTS[concept_id]["jurisdiction"]],
                         required_context=CONCEPTS[concept_id]["required_context"],
                         score=round(score, 2), matched_on=matched)
               for score, concept_id, matched in hits[:request.limit]]
    return SearchResult(release_id=RELEASE_ID, query=request.query, results=results, limitations=[MOCK_NOTE])


def jurisdiction_gap(concept_jurisdiction, requested):
    """Return a gap when the concept's jurisdiction does not contain the requested scope, else None."""
    if not requested.served:
        return CoverageGap(dimension="jurisdiction_not_covered",
                           message="Only Switzerland (CH) is served.", published_values=["CH"])
    if concept_jurisdiction == "CH":
        return None
    if concept_jurisdiction == "CH-ZH":
        if requested.canton_code == "CH-ZH":
            return None
        if requested.canton_code is None:
            return CoverageGap(dimension="jurisdiction_not_covered",
                               message="This concept is published for the Canton of Zurich; add the canton "
                                       "if the user lives there, otherwise only federal concepts apply.",
                               published_values=["CH-ZH"])
        return CoverageGap(dimension="jurisdiction_not_covered",
                           message=f"This concept is published for CH-ZH, not {requested.canton_code}; no cantonal "
                                   "procedure is published for that canton. Federal concepts still apply.",
                           published_values=["CH-ZH"])
    if concept_jurisdiction == CITY_OF_ZURICH:
        if requested.municipality_id == CITY_OF_ZURICH:
            return None
        return CoverageGap(dimension="jurisdiction_not_covered",
                           message="This concept is published for the City of Zurich only; add the city "
                                   "if the user moves to the city.",
                           published_values=[CITY_OF_ZURICH])
    return CoverageGap(dimension="concept_not_published", message="Unknown jurisdiction.", published_values=[])


def resolve_concept(concept_id, request: ResolveRequest, as_of, requested):
    concept = CONCEPTS.get(concept_id)
    if concept is None:
        return ConceptResolution(concept_id=concept_id, status=Status.OUT_OF_COVERAGE, gaps=[CoverageGap(
            dimension="concept_not_published",
            message="Unknown concept_id; take IDs from get_coverage or search.", published_values=list(CONCEPTS))])
    gap = jurisdiction_gap(concept["jurisdiction"], requested)
    if gap:
        return ConceptResolution(concept_id=concept_id, status=Status.OUT_OF_COVERAGE, gaps=[gap])
    missing = [MissingContext(field=field, options=CONTEXT_SCHEMA[field].enum, hint=CONTEXT_SCHEMA[field].description)
               for field in concept["required_context"] if not request.context.get(field)]
    if missing:
        return ConceptResolution(concept_id=concept_id, status=Status.NEEDS_CONTEXT, missing_context=missing)
    unknown = [field for field in request.context if field not in CONTEXT_SCHEMA]
    if unknown:
        return ConceptResolution(concept_id=concept_id, status=Status.OUT_OF_COVERAGE, gaps=[CoverageGap(
            dimension="context_not_covered", message=f"Unknown context fields: {unknown}.",
            published_values=list(CONTEXT_SCHEMA))])
    for field, value in (concept["condition"] or {}).items():
        if request.context.get(field) != value:
            return ConceptResolution(concept_id=concept_id, status=Status.OUT_OF_COVERAGE, gaps=[CoverageGap(
                dimension="context_not_covered",
                message=f"This concept is published for {field}={value}; the mock release has no facts for "
                        f"{field}={request.context.get(field)}. Say that the service has no coverage for it.",
                published_values=[f"{field}={value}"])])
    if concept_id == "residence.registration-after-arrival-eu-efta" \
            and request.context.get("employment_duration") == "UP_TO_3_MONTHS":
        return ConceptResolution(concept_id=concept_id, status=Status.OUT_OF_COVERAGE, gaps=[CoverageGap(
            dimension="context_not_covered",
            message="For employment of up to three months the notification procedure applies instead; resolve "
                    "residence.short-term-notification-eu-efta.",
            published_values=["employment_duration=MORE_THAN_3_MONTHS", "employment_duration=UNKNOWN"])])
    # The mock's content is hardcoded and was never confirmed by a person, so it serves the unreviewed
    # status the real server would; reviewed_only therefore withholds every mock fact.
    facts = [Fact(fact_id=item["fact_id"], statement=item["statement"], jurisdiction=concept["jurisdiction"],
                  condition=concept["condition"], evidence_ids=item["evidence_ids"],
                  review_status="assistant-authored-unreviewed") for item in concept["facts"]]
    if request.reviewed_only:
        return ConceptResolution(concept_id=concept_id, status=Status.OUT_OF_COVERAGE, gaps=[CoverageGap(
            dimension="review_status_not_met",
            message="No fact of this concept has been confirmed by a person, and the request asked for "
                    "human-reviewed facts only. Say that the service has no reviewed coverage for it; "
                    "resolve again without reviewed_only to see the unreviewed statements.",
            published_values=["assistant-authored-unreviewed"])])
    evidence_ids = []
    for fact in facts:
        for evidence_id in fact.evidence_ids:
            if evidence_id not in evidence_ids:
                evidence_ids.append(evidence_id)
    status = Status.STALE if as_of >= FRESHNESS.stale_from else Status.SUPPORTED
    gaps = []
    if concept["jurisdiction"] == "CH-ZH" and requested.municipality_id is None:
        gaps.append(CoverageGap(
            dimension="more_specific_jurisdiction_available",
            message="A municipal procedure is published for the City of Zurich (concept "
                    "residence.zh.city-zurich-registration); add the city to resolve it if the user lives there.",
            published_values=[CITY_OF_ZURICH]))
    # The mirror image: the mock publishes a cantonal and a municipal procedure for Zurich only, so an answer for
    # another canton, or for another municipality of the canton, says that its own narrower level is not published.
    elsewhere = None
    if requested.canton_code not in (None, "CH-ZH"):
        elsewhere = ("CH", ["CH-ZH", CITY_OF_ZURICH])
    elif requested.canton_code == "CH-ZH" and requested.municipality_id not in (None, CITY_OF_ZURICH):
        elsewhere = ("CH-ZH", [CITY_OF_ZURICH])
    if elsewhere:
        place = requested.municipality_id or requested.canton_code
        gaps.append(CoverageGap(
            dimension="more_specific_jurisdiction_not_published",
            message=f"For {place} this topic publishes nothing narrower than {jurisdiction_label(elsewhere[0])}; its "
                    f"narrower facts are published for {', '.join(elsewhere[1])} only and do not apply to {place}.",
            published_values=elsewhere[1]))
    facts, review = shared_review(facts)
    return ConceptResolution(concept_id=concept_id, status=status,
                             answering_jurisdiction=jurisdiction_label(concept["jurisdiction"]), **review,
                             facts=facts, citations=citations(evidence_ids), gaps=gaps)


def overall_status(results):
    statuses = {result.status for result in results}
    if Status.NEEDS_CONTEXT in statuses:
        return Status.NEEDS_CONTEXT
    if Status.STALE in statuses:
        return Status.STALE
    if Status.SUPPORTED in statuses:
        return Status.SUPPORTED
    return Status.OUT_OF_COVERAGE


def resolve(request: ResolveRequest):
    if len(set(request.concept_ids)) != len(request.concept_ids):
        return argument_error("concept_ids", "Concept IDs must be unique.")
    try:
        scope = PLACES.resolve(request.jurisdiction.country, request.jurisdiction.canton, request.jurisdiction.city)
    except PlaceError as exc:
        return argument_error(exc.path, exc.message)
    as_of = request.as_of or date.today()
    results = [resolve_concept(concept_id, request, as_of, scope) for concept_id in request.concept_ids]
    status = overall_status(results)
    limitations = [MOCK_NOTE]
    guidance = None
    if status == Status.NEEDS_CONTEXT:
        guidance = ("Derive the missing fields from what the user already said (for example a Czech citizen is "
                    "population EU_EFTA and 'starting my work' is purpose EMPLOYMENT) and call resolve again. "
                    "Ask the user only for fields that cannot be derived.")
    elif any(gap.dimension == "more_specific_jurisdiction_not_published" for result in results for gap in result.gaps):
        guidance = ("For the user's place this release publishes only the broader level named in the gaps: where the "
                    "question has a cantonal or municipal part, tell the user that it is not published for their "
                    "place, and carry over no rule, office, fee or deadline published for another canton or "
                    "municipality.")
    if status == Status.STALE:
        limitations.append(f"The source snapshot of {FRESHNESS.snapshot_date.isoformat()} is older than "
                           f"{FRESHNESS.max_age_days} days on {as_of.isoformat()}; verify the cited pages before relying on the facts.")
    federal_supported = any(result.concept_id == "residence.registration-after-arrival-eu-efta"
                            and result.status in (Status.SUPPORTED, Status.STALE) for result in results)
    if federal_supported:
        limitations.append("Office opening hours and appointment availability are not covered.")
    duration = request.context.get("employment_duration") or "UNKNOWN"
    user_facts = [fact.model_copy(update={"status": duration}) if fact.name == "employment_duration" else fact
                  for fact in REQUIRED_USER_FACTS] if federal_supported else []
    if scope.not_recognised:
        parts = " and ".join(f"the {part} {value!r}" for part, value in scope.not_recognised.items())
        guidance = ((guidance or "") + f" The mock's place list does not hold {parts}, so this result is for "
                    f"{PLACES.label(scope.code)}; resolve again with the municipality's official name or with the canton "
                    "if the narrower place matters.").strip()
    executed = ExecutedScope(country_code=scope.country_code, canton_code=scope.canton_code,
                             municipality_id=scope.municipality_id, country=scope.country, canton=scope.canton,
                             city=scope.city, not_recognised=scope.not_recognised)
    return ResolveResult(release_id=RELEASE_ID, status=status, as_of=as_of, executed_scope=executed,
                         freshness=FRESHNESS, results=results, required_user_facts=user_facts,
                         decision_rule=DECISION_RULE if federal_supported else None,
                         guidance_for_caller=guidance, limitations=limitations)


def get_evidence(request: GetEvidenceRequest):
    if request.release_id not in (None, RELEASE_ID):
        return argument_error("release_id", f"Unknown release_id {request.release_id!r}; the active release is {RELEASE_ID!r}.")
    unknown = [item for item in request.evidence_ids if item not in EVIDENCE]
    if unknown:
        return argument_error("evidence_ids", f"Unknown evidence IDs: {unknown}.")
    return GetEvidenceResult(
        release_id=RELEASE_ID,
        evidence=[Evidence(evidence_id=item, accessed_on=SNAPSHOT_DATE, **EVIDENCE[item]) for item in request.evidence_ids],
        limitations=[MOCK_NOTE])


HANDLERS = {"get_coverage": get_coverage, "search": search, "resolve": resolve, "get_evidence": get_evidence}


def dispatch(name, arguments):
    """Validate the arguments against the request model and run the handler."""
    if name not in HANDLERS:
        return argument_error("name", f"Unknown tool {name!r}.")
    request_model = TOOL_CONTRACTS[name][0]
    try:
        request = request_model.model_validate(arguments or {})
    except ValidationError as exc:
        return invalid(exc)
    return HANDLERS[name](request)


def create_server():
    server = Server(SERVER_NAME, version=SERVER_VERSION)
    log = logging.getLogger(SERVER_NAME)

    @server.list_tools()
    async def list_tools():
        return [types.Tool(name=name, description=TOOL_DESCRIPTIONS[name],
                           inputSchema=tool_input_schema(request), outputSchema=tool_output_schema(result),
                           annotations=types.ToolAnnotations(readOnlyHint=True, destructiveHint=False,
                                                            openWorldHint=False))
                for name, (request, result) in TOOL_CONTRACTS.items()]

    @server.call_tool(validate_input=False)
    async def call_tool(name, arguments):
        started = time.perf_counter()
        result = dispatch(name, arguments)
        payload = result.model_dump(mode="json", exclude_none=True)
        text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        is_error = isinstance(result, ToolError)
        status = result.error.code.value if is_error else payload.get("status", "OK")
        log.info("tool=%s status=%s bytes=%d ms=%.1f", name, status, len(text.encode("utf-8")),
                 (time.perf_counter() - started) * 1000)
        return types.CallToolResult(content=[types.TextContent(type="text", text=text)],
                                    structuredContent=payload, isError=is_error)

    return server


async def serve():
    server = create_server()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    logging.basicConfig(stream=sys.stderr, level=logging.INFO,
                        format="%(asctime)s %(name)s %(levelname)s %(message)s")
    asyncio.run(serve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
