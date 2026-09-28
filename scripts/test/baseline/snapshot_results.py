"""Record everything a caller can see from a committed release, and compare it with an earlier record byte for byte.

    ./.venv/Scripts/python.exe scripts/test/baseline/snapshot_results.py --out .local/baseline/before-v2
    ./.venv/Scripts/python.exe scripts/test/baseline/snapshot_results.py --out .local/baseline/after --compare .local/baseline/before-v2

For the attested Swiss packs (or the packs named with --pack), in-process with the ReleaseService the server uses, lexical
search, no model and no network. Each record is one JSON line: a key naming the request and the exact JSON the server
would send (`model_dump(mode="json", exclude_none=True)`, compact separators). The first line of a pack's file is a
header: what the capture is bound to (the release bytes, the content digest, the suites and the semantic index) and,
for information, what produced it (the swiss-tip commit and working-tree state, the package, pydantic, mcp and Python
versions, the hash seed). The records:

- the connect-time instructions with get_coverage listed and hidden; each tool's description, input schema and output
  schema; the tool lists; the health payload; the coverage root and every topic page;
- every search and resolve step of the pack's acceptance and regression suites (resolve at the suite's policy date),
  and the acceptance report of each suite without checked_at;
- get_evidence for every excerpt those resolves serve, then for every other excerpt of the release, five at a time;
- raw questions: every case question searched as asked (limit 10), plus Polish and "Ł" probes;
- the register sweep: every place of the place register named every way a caller can name it (official name, each
  alias, the name without its qualifier and each part of a "/" name, "<name> <canton abbreviation>", the code, the
  code without the country, the lower-case zero-padded code, the bare number next to its canton), each resolved for
  two concepts (the one whose facts span the most levels, and one published only at the release's deepest level);
  the record keeps what depends on the place (executed_scope, status, guidance and per concept the status, answering
  jurisdiction, basis, gaps, missing context and fact IDs), or the whole error; and the label and the described form
  of every place;
- error probes: ambiguous and misplaced cities, countries not served, places not recognised, flattened top-level
  place parts, every alias field name, malformed requests, each for resolve and search where it applies;
- the concept by place matrix: every concept at its own jurisdictions and at CH, CH-BE, CH-BE-351, CH-ZH-230,
  CH-GE-6621, CH-TI-5192 and DE, at the policy date without context, with each context its facts are conditioned on,
  at stale_from, the day before its earliest valid_from, the day after its latest valid_through, and reviewed_only;
- over stdio, one server session per pack with and without --with-coverage: the initialize result without
  serverInfo.version and the tools/list result (--skip-stdio leaves them out).

Every resolve carries an explicit as_of, so a capture does not depend on the day it runs; search takes no date. Hybrid
search is not recorded: it needs recorded query vectors, which are not part of this capture. What hybrid search takes
from the lexical side is: every case search and raw question also records its whole lexical ranking with exact scores
(everywhere, and among the concepts that apply at its place) and its anchored match.

--compare refuses (exit code 2) unless both headers bind the same release, suites and semantic index; the informative
header fields that differ are printed. A code change that must leave the Swiss packs untouched passes when --compare
finds no difference; the exit code is 1 otherwise, and the first differences are printed. Run the after-capture once
with PYTHONHASHSEED=0 and once with a random seed.
"""

import argparse
import asyncio
import hashlib
import importlib.metadata
import json
import os
import platform
import re
import subprocess
import sys
import time
from datetime import date, timedelta
from pathlib import Path

import swisstip.core
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from swisstip.build.acceptance import load_acceptance, load_regression
from swisstip.core.contracts import GetCoverageRequest, ToolError, tool_output_schema
from swisstip.core.places import PlaceError
from swisstip.mcp_server import SERVER_VERSION
from swisstip.mcp_server.server import health
from swisstip.runtime.acceptance import check_acceptance, policy_date
from swisstip.runtime.service import ALL_TOOL_CONTRACTS, ReleaseService

ROOT = Path(__file__).resolve().parents[3]
HEADER_VERSION = "swiss-tip-baseline-capture/v3"
DISTRIBUTIONS = ["swisstip-core", "swisstip-runtime", "swisstip-build", "swisstip-mcp-server", "swisstip-extraction",
                 "pydantic", "pydantic-core", "mcp", "PyYAML"]

# Requests a caller could send to any release; answered the same way before and after a country-neutral change.
PROBES = [
    ("resolve", {"concept_ids": ["{concept}"], "jurisdiction": {"country": "Poland"}}),
    ("resolve", {"concept_ids": ["{concept}"], "jurisdiction": {"country": "PL", "region": "PL-12"}}),
    ("resolve", {"concept_ids": ["{concept}"], "jurisdiction": {"country": "Polska", "city": "Kraków"}}),
    ("resolve", {"concept_ids": ["{concept}"], "jurisdiction": {"region": "Małopolskie"}}),
    ("resolve", {"concept_ids": ["{concept}"], "jurisdiction": {"canton": "Zürich", "city": "Winterthur"}}),
    ("resolve", {"concept_ids": ["{concept}"], "jurisdiction": {"city": "Łódź"}}),
    ("resolve", {"concept_ids": ["{concept}"], "jurisdiction": {"canton": "CH-ZH", "city": "CH-ZH-261"}}),
    ("resolve", {"concept_ids": ["{concept}"], "jurisdiction": {"canton": "ZH"}, "context": {"unknown_field": "x"}}),
    ("resolve", {"concept_ids": ["no-such-concept"], "jurisdiction": {"canton": "ZH"}}),
    ("resolve", {"concept_ids": [], "jurisdiction": {}}),
    ("search", {"query": "budżet obywatelski Kraków"}),
    ("search", {"query": "participatory budget Warsaw", "jurisdiction": {"country": "Poland"}}),
    ("search", {"query": "Aufenthaltsbewilligung", "jurisdiction": {"canton": "Zürich"}}),
    ("search", {"query": ""}),
    ("get_evidence", {"evidence_ids": ["no-such-evidence"]}),
    ("get_coverage", {"parent_id": "no-such-topic"}),
    ("no_such_tool", {}),
]

# Jurisdictions sent to resolve (for the first concept) and to search (with its label).
PLACE_PROBES = [
    # A name several municipalities share, with and without the canton that singles one out.
    {"city": "Buchs"}, {"city": "buchs"}, {"city": "BUCHS"}, {"canton": "ZH", "city": "Buchs"},
    {"canton": "SG", "city": "Buchs"}, {"canton": "BE", "city": "Buchs"}, {"city": "Buchs ZH"}, {"city": "Buchs (ZH)"},
    {"city": "Buchs (BE)"},
    # A city outside the given canton.
    {"canton": "BE", "city": "Winterthur"}, {"canton": "Bern", "city": "Winterthur"},
    {"canton": "CH-BE", "city": "CH-ZH-230"}, {"canton": "BE", "city": "ZH-230"}, {"canton": "Zürich", "city": "Bern"},
    {"canton": "ZH", "city": "Genève"},
    # Countries, served or not.
    {"country": "Germany"}, {"country": "DE"}, {"country": "de"}, {"country": "Deutschland", "city": "Berlin"},
    {"country": "Narnia"}, {"country": "XX"}, {"country": "Switzerland"}, {"country": "Schweiz"},
    {"country": "Suisse"}, {"country": "ch"}, {"country": "CHE"}, {"country": "Poland", "city": "Kraków"},
    {"country": "CH", "canton": "ZH", "city": "Zürich"}, {"country": "Germany", "canton": "ZH"},
    # Places the register does not hold, and codes that parse but are not listed.
    {"canton": "Narnia"}, {"city": "Atlantis"}, {"canton": "ZH", "city": "Atlantis"}, {"city": "8001"},
    {"canton": "ZH", "city": "8001"}, {"city": "Zürich Altstetten"}, {"city": "Kreis 4"}, {"canton": "ZZ"},
    {"canton": "CH-ZZ"}, {"city": "CH-ZH-9999"}, {"city": "ZH-99999"}, {"city": "261"}, {"canton": "ZH", "city": "0261"},
    {"canton": "CH-ZH", "city": "CH-BE-351"}, {"canton": "Narnia", "city": "Wallisellen"},
    {"canton": "ZH", "city": "Narnia"}, {"city": "Łyss"}, {"city": "Łausanne"}, {"canton": "Łucerne"},
    {"city": "Lyss"}, {"city": "Lausanne"}, {"canton": "Kanton Zürich"}, {"city": "Stadt Zürich"},
    {"city": "Gemeinde Wallisellen"}, {"canton": "canton of Bern", "city": "city of Bern"},
    # Empty and padded parts.
    {"city": ""}, {"city": "   "}, {"canton": " ZH ", "city": " Wallisellen "}, {},
]

# Every name a place part answers to, sent inside jurisdiction and flattened to the top level.
ALIAS_FIELDS = [("country", "CH"), ("country_code", "CH"), ("canton", "ZH"), ("canton_code", "CH-ZH"),
                ("state", "ZH"), ("region", "ZH"), ("city", "Wallisellen"), ("municipality", "Wallisellen"),
                ("municipality_id", "CH-ZH-69"), ("commune", "Wallisellen"), ("town", "Wallisellen")]

# Whole argument objects: flattened parts, conflicts, malformed values.
MALFORMED = [
    ("resolve", {"concept_ids": ["{concept}"], "as_of": "{as_of}", "city": "Wallisellen"}),
    ("resolve", {"concept_ids": ["{concept}"], "as_of": "{as_of}", "canton": "ZH"}),
    ("resolve", {"concept_ids": ["{concept}"], "as_of": "{as_of}", "country": "CH", "canton": "ZH", "city": "Wallisellen"}),
    ("resolve", {"concept_ids": ["{concept}"], "as_of": "{as_of}", "jurisdiction": {"city": "Zürich"}, "city": "Wallisellen"}),
    ("resolve", {"concept_ids": ["{concept}"], "as_of": "{as_of}", "jurisdiction": {"city": "Wallisellen"}, "city": "Wallisellen"}),
    ("resolve", {"concept_ids": ["{concept}"], "as_of": "{as_of}", "jurisdiction": {"municipality": "Zürich"}, "town": "Wallisellen"}),
    ("resolve", {"concept_ids": ["{concept}"], "as_of": "{as_of}", "jurisdiction": {"city": "Zürich", "town": "Wallisellen"}}),
    ("resolve", {"concept_ids": ["{concept}"], "as_of": "{as_of}", "jurisdiction": {"canton": "ZH", "region": "BE"}}),
    ("resolve", {"concept_ids": ["{concept}"], "as_of": "{as_of}", "jurisdiction": "Zurich"}),
    ("resolve", {"concept_ids": ["{concept}"], "as_of": "{as_of}", "jurisdiction": {"province": "ZH"}}),
    ("resolve", {"concept_ids": ["{concept}"], "as_of": "{as_of}", "jurisdiction": None}),
    ("resolve", {"concept_ids": ["{concept}"], "as_of": "{as_of}", "jurisdiction": {"city": 69}}),
    ("resolve", {"concept_ids": ["{concept}", "{concept}"], "as_of": "{as_of}"}),
    ("resolve", {"concept_ids": ["a", "b", "c", "d", "e", "f"], "as_of": "{as_of}"}),
    ("resolve", {"concept_ids": "{concept}", "as_of": "{as_of}"}),
    ("resolve", {"concept_ids": ["{concept}"], "as_of": "2026-13-01"}),
    ("resolve", {"concept_ids": ["{concept}"], "as_of": "{as_of}", "context": {"x": 1}}),
    ("resolve", {"concept_ids": ["{concept}"], "as_of": "{as_of}", "reviewed_only": "sometimes"}),
    ("resolve", {"concept_ids": ["{concept}"], "as_of": "{as_of}", "foo": 1}),
    ("resolve", {"as_of": "{as_of}"}),
    ("search", {"query": "{label}", "city": "Wallisellen"}),
    ("search", {"query": "{label}", "jurisdiction": {"city": "Zürich"}, "city": "Wallisellen"}),
    ("search", {"query": "{label}", "limit": 0}),
    ("search", {"query": "{label}", "limit": 11}),
    ("search", {"query": "{label}", "limit": 10}),
    ("search", {"query": "   "}),
    ("search", {"limit": 3}),
    ("search", {"query": "{label}", "jurisdiction": "Zurich"}),
    ("search", {"query": "{label}", "foo": 1}),
    ("get_evidence", {"evidence_ids": []}),
    ("get_evidence", {"evidence_ids": ["{fact}"]}),
    ("get_evidence", {"evidence_ids": ["{evidence}"], "release_id": "no-such-release"}),
    ("get_coverage", {"release_id": "no-such-release"}),
    ("get_coverage", {"parent_id": "{topic}"}),
    ("lookup", {"dataset_id": "no-such-dataset", "postal_code": "8001"}),
    ("get_coverage", None),
]

# Raw questions beyond the suites' own.
RAW_QUESTIONS = ["Jak długo trwa pozwolenie w Zurychu?", "Łódź opłata", "Łyss", "Łausanne", "Lyss", "Lausanne",
                 "Wrocław", "Kraków participatory budget", "ŁÓDŹ"]

# The concept by place matrix: every concept at these places besides its own jurisdictions.
MATRIX_PLACES = ["CH", "CH-BE", "CH-BE-351", "CH-ZH-230", "CH-GE-6621", "CH-TI-5192", "DE"]
# The attested packs the capture proves unchanged; a pack being built (mvp-poland) is captured only when named.
SWISS_PACKS = ["mvp-wallisellen", "mvp-zurich"]
QUALIFIER = re.compile(r"\s*\(([^)]*)\)\s*$")


def compact(payload) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def dump(result) -> str:
    """The exact payload text the MCP server sends for a result."""
    return compact(result.model_dump(mode="json", exclude_none=True))


def fill(value, slots: dict):
    """The value with every string that is exactly a slot name ("{concept}") replaced by the slot's value."""
    if isinstance(value, str):
        return slots.get(value, value)
    if isinstance(value, list):
        return [fill(item, slots) for item in value]
    if isinstance(value, dict):
        return {key: fill(item, slots) for key, item in value.items()}
    return value


def place_parts(code: str) -> dict:
    """A code as the request parts a caller sends: country, canton and city."""
    parts = code.split("-")
    return {"country": parts[0], **({"canton": "-".join(parts[:2])} if len(parts) > 1 else {}),
            **({"city": code} if len(parts) > 2 else {})}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(folder: Path, *args: str) -> str | None:
    try:
        done = subprocess.run(["git", "-C", str(folder), *args], capture_output=True, check=True, timeout=60)
        return done.stdout.decode("utf-8")
    except (OSError, subprocess.SubprocessError):
        return None


def code_state() -> dict:
    """The swiss-tip checkout the services were imported from: commit, changed paths and a digest of the diff."""
    folder = Path(swisstip.core.__file__).resolve().parent
    top = (git(folder, "rev-parse", "--show-toplevel") or "").strip()
    if not top:
        return dict(checkout=None)
    status = sorted(line for line in (git(Path(top), "status", "--porcelain", "--untracked-files=all") or "").splitlines() if line)
    diff = git(Path(top), "diff", "HEAD", "--binary") or ""
    digest = hashlib.sha256(diff.encode("utf-8"))
    # Untracked files are part of the code a capture ran on (a new module), so their paths and bytes count too.
    untracked = sorted(name for name in (git(Path(top), "ls-files", "--others", "--exclude-standard", "-z") or "").split("\0") if name)
    for name in untracked:
        digest.update(b"\0" + name.encode("utf-8") + b"\0" + (Path(top) / name).read_bytes())
    return dict(checkout=Path(top).name, commit=(git(Path(top), "rev-parse", "HEAD") or "").strip(), changed=status,
                diff_sha256=digest.hexdigest())


def versions() -> dict:
    found = {}
    for name in DISTRIBUTIONS:
        try:
            found[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            found[name] = None
    found["SERVER_VERSION"] = SERVER_VERSION
    return found


def header(pack_dir: Path, stdio: bool) -> dict:
    """What the capture is bound to (compared strictly) and what produced it (printed when it differs)."""
    release_path = pack_dir / "release.json"
    release_bytes = release_path.read_bytes()
    manifest = json.loads(release_bytes)["manifest"]
    suites = {}
    if (pack_dir / "acceptance.yaml").is_file():
        suites["acceptance.yaml"] = dict(file_sha256=sha256_file(pack_dir / "acceptance.yaml"),
                                         digest=load_acceptance(pack_dir / "acceptance.yaml").digest())
    if (pack_dir / "regression.yaml").is_file():
        _, regression, combined = load_regression(pack_dir)
        suites["regression.yaml"] = dict(file_sha256=sha256_file(pack_dir / "regression.yaml"), digest=regression.digest(),
                                         combined_digest=combined.digest())
    index = None
    if (pack_dir / "semantic-index.json").is_file():
        data = json.loads((pack_dir / "semantic-index.json").read_text(encoding="utf-8"))
        index = dict(file_sha256=sha256_file(pack_dir / "semantic-index.json"), content_sha256=data.get("content_sha256"),
                     model=data.get("model"), model_digest=data.get("model_digest"), release_id=data.get("release_id"))
    readiness = pack_dir / "readiness.json"
    binding = dict(pack=pack_dir.name, release_id=manifest["release_id"], schema_version=manifest["schema_version"],
                   release_sha256=hashlib.sha256(release_bytes).hexdigest(), content_sha256=manifest["content_sha256"],
                   readiness_release_sha256=json.loads(readiness.read_text(encoding="utf-8")).get("release_sha256")
                   if readiness.is_file() else None,
                   suites=suites, semantic_index=index)
    info = dict(code=code_state(), packs_commit=(git(ROOT, "rev-parse", "HEAD") or "").strip() or None,
                versions=versions(), python=sys.version.split()[0], platform=platform.platform(),
                hash_seed=os.environ.get("PYTHONHASHSEED", "random"), stdio=stdio)
    return dict(schema_version=HEADER_VERSION, binding=binding, info=info)


def suite_of(pack_dir: Path):
    """The suites of a pack: the one the cases are replayed from (the regression pack when there is one) and each
    suite whose report is recorded."""
    if not (pack_dir / "acceptance.yaml").is_file():
        return None, {}
    acceptance = load_acceptance(pack_dir / "acceptance.yaml")
    if (pack_dir / "regression.yaml").is_file():
        combined = load_regression(pack_dir)[2]
        return combined, {"acceptance": acceptance, "regression-pack": combined}
    return acceptance, {"acceptance": acceptance}


def ranking(service: ReleaseService, query: str, jurisdiction: dict | None = None) -> str:
    """The whole lexical ranking of a query with exact scores: every hit, not only the first `limit`, since hybrid
    search fuses all of them with the semantic candidates. With a jurisdiction, also the ranking among the concepts
    that apply there. With the anchored match that decides the match strength. This covers what hybrid search takes
    from the lexical side while no recorded query vectors exist."""
    record = {"everywhere": [[repr(score), concept_id, matched] for score, concept_id, matched in service.lexical_hits(query)],
              "anchored": [repr(value) for value in service.anchored_match(query)]}
    place = jurisdiction or {}
    if any(place.get(part) for part in ("country", "canton", "city")):
        try:
            scope = service.place_index.resolve(place.get("country"), place.get("canton"), place.get("city"))
        except PlaceError as exc:
            record["place_error"] = [exc.path, exc.message]
        else:
            allowed = service.applicable(scope.code)
            record["allowed"] = [[repr(score), concept_id, matched]
                                 for score, concept_id, matched in service.lexical_hits(query, allowed)]
    return compact(record)


def resolve_projection(result) -> str:
    """What of a resolve result depends on the place it was asked for: the whole payload of an error."""
    payload = result.model_dump(mode="json", exclude_none=True)
    if isinstance(result, ToolError):
        return compact(payload)
    kept = {key: payload[key] for key in ("status", "executed_scope", "guidance_for_caller") if key in payload}
    kept["results"] = [dict({key: item[key] for key in ("concept_id", "status", "answering_jurisdiction", "basis", "gaps",
                                                         "missing_context") if key in item},
                            facts=[fact["fact_id"] for fact in item.get("facts", [])])
                       for item in payload.get("results", [])]
    return compact(kept)


def place_variants(place) -> list[dict]:
    """Every way a caller can name one place of the register, as request parts."""
    parts = place.code.split("-")
    level = len(parts) - 1
    field = ("country", "canton", "city")[min(level, 2)]
    names = [place.name, *place.aliases]
    bare = []
    for name in names:
        base = QUALIFIER.sub("", name)
        bare.extend([base, *(part.strip() for part in base.split("/") if "/" in base)])
    variants = [{field: name} for name in [*names, *bare]]
    if level == 0:
        variants += [{"country": place.code}, {"country": place.code.lower()}]
    elif level == 1:
        variants += [{"canton": place.code}, {"canton": parts[1]}, {"canton": parts[1].lower()}]
    else:
        variants += [{"city": f"{name} {parts[1]}"} for name in bare]
        variants += [{"city": place.code}, {"city": f"{parts[1]}-{parts[2]}"}, {"city": f"{parts[1].lower()}-{parts[2].zfill(4)}"},
                     {"canton": parts[1], "city": parts[2]}]
    unique = {}
    for variant in variants:
        if all(value.strip() for value in variant.values()):
            unique.setdefault(compact(variant), variant)
    return list(unique.values())


def sweep_concepts(service: ReleaseService) -> list[str]:
    """The concept whose facts span the most levels and jurisdictions, and one published only at the deepest level of
    the release: resolved together, their results name the requested place at every level (an applicable fact, a
    concept "published for ..., not for <place>", "below the requested <place>")."""
    def spread(concept):
        codes = {service.facts[f].jurisdiction for f in concept.fact_ids}
        return (-len({code.count("-") for code in codes}), -len(codes), concept.concept_id)
    first = min(service.release.concepts, key=spread).concept_id
    deepest = max(code.count("-") for code in service.release.manifest.jurisdictions)
    narrow = sorted((len(concept.jurisdictions), concept.concept_id) for concept in service.release.concepts
                    if concept.concept_id != first and all(code.count("-") == deepest for code in concept.jurisdictions))
    return [first, *([narrow[0][1]] if narrow else [])]


def register_sweep(service: ReleaseService, as_of: date):
    index = service.place_index
    register = service.release.place_register
    concept_ids = sweep_concepts(service)
    yield "sweep:concepts", compact(concept_ids)
    codes = [place.code for place in register.places] if register else []
    for code in dict.fromkeys([*codes, *service.release.manifest.jurisdictions, *MATRIX_PLACES, "CH-XX", "CH-ZH-9999"]):
        yield f"label:{code}", f"{index.label(code)}\t{index.described(code)}"
    for place in register.places if register else []:
        for variant in place_variants(place):
            arguments = {"concept_ids": concept_ids, "jurisdiction": variant, "as_of": as_of.isoformat()}
            yield f"sweep:{place.code}:{compact(variant)}", resolve_projection(service.dispatch("resolve", arguments))


def probes(service: ReleaseService, hidden: ReleaseService, as_of: date):
    first_concept = next(iter(service.concepts))
    concept = service.concepts[first_concept]
    fact = service.facts[concept.fact_ids[0]]
    slots = {"{concept}": first_concept, "{as_of}": as_of.isoformat(), "{label}": concept.label, "{fact}": fact.fact_id,
             "{evidence}": fact.evidence_ids[0], "{topic}": concept.topic_id}
    for number, (tool, arguments) in enumerate(PROBES, 1):
        filled = fill(arguments, slots)
        if tool == "resolve":
            filled["as_of"] = as_of.isoformat()
        yield f"probe:{number}:{tool}:{compact(filled)}", dump(service.dispatch(tool, filled))
    for place in PLACE_PROBES:
        yield (f"place-probe:resolve:{compact(place)}",
               dump(service.dispatch("resolve", {"concept_ids": [first_concept], "jurisdiction": place, "as_of": as_of.isoformat()})))
        yield (f"place-probe:search:{compact(place)}",
               dump(service.dispatch("search", {"query": concept.label, "jurisdiction": place})))
    for name, value in ALIAS_FIELDS:
        for tool, arguments in (("resolve", {"concept_ids": [first_concept], "as_of": as_of.isoformat()}),
                                ("search", {"query": concept.label})):
            yield f"alias-probe:{tool}:nested:{name}", dump(service.dispatch(tool, {**arguments, "jurisdiction": {name: value}}))
            yield f"alias-probe:{tool}:flattened:{name}", dump(service.dispatch(tool, {**arguments, name: value}))
    for number, (tool, arguments) in enumerate(MALFORMED, 1):
        filled = fill(arguments, slots)
        yield f"malformed:{number}:{tool}:{compact(filled)}", dump(service.dispatch(tool, filled))
    yield "hidden:get_coverage", dump(hidden.dispatch("get_coverage", {}))
    yield "hidden:search", dump(hidden.dispatch("search", {"query": concept.label}))


def raw_questions(service: ReleaseService, suite, as_of: date):
    for case in suite.cases if suite else []:
        yield f"question:{case.case_id}", dump(service.dispatch("search", {"query": case.question, "limit": 10}))
        yield f"question-ranking:{case.case_id}", ranking(service, case.question)
    concept_id = next(iter(service.concepts))
    for question in RAW_QUESTIONS:
        yield f"question:extra:{question}", dump(service.dispatch("search", {"query": question, "limit": 10}))
        yield f"question-ranking:extra:{question}", ranking(service, question)
    for city in ("Łyss", "Łausanne"):
        yield (f"question:extra-resolve:{city}", dump(service.dispatch("resolve", {
            "concept_ids": [concept_id], "jurisdiction": {"city": city}, "as_of": as_of.isoformat()})))
        yield (f"question:extra-search:{city}", dump(service.dispatch("search", {
            "query": service.concepts[concept_id].label, "jurisdiction": {"city": city}})))


def contexts(service: ReleaseService, concept) -> list[dict]:
    """The contexts a concept's facts are conditioned on, each completed with the first allowed value of every other
    required field; the first allowed values alone when its facts carry no condition but it has context fields."""
    first = {name: (spec.enum or ["unspecified"])[0] for name, spec in concept.context_schema.items()}
    base = {name: first.get(name, "unspecified") for name in concept.required_context}
    conditions = sorted({compact(dict(sorted(service.facts[f].condition.items())))
                         for f in concept.fact_ids if service.facts[f].condition})
    found = [{**base, **json.loads(condition)} for condition in conditions]
    if not found and concept.context_schema:
        found = [first]
    return list({compact(dict(sorted(context.items()))): dict(sorted(context.items())) for context in found}.values())


def matrix(service: ReleaseService, as_of: date):
    stale = service.freshness.stale_from
    for concept in service.release.concepts:
        facts = [service.facts[f] for f in concept.fact_ids]
        variants = [("plain", {}), ("stale", {"as_of": stale.isoformat()}), ("reviewed-only", {"reviewed_only": True})]
        starts = [f.valid_from for f in facts if f.valid_from]
        if starts:
            variants.append(("before-valid", {"as_of": (min(starts) - timedelta(days=1)).isoformat()}))
        ends = [f.valid_through for f in facts if f.valid_through]
        if ends:
            variants.append(("after-valid", {"as_of": (max(ends) + timedelta(days=1)).isoformat()}))
        variants += [(f"context:{compact(context)}", {"context": context}) for context in contexts(service, concept)]
        for code in dict.fromkeys([*concept.jurisdictions, *MATRIX_PLACES]):
            for name, extra in variants:
                arguments = {"concept_ids": [concept.concept_id], "jurisdiction": place_parts(code),
                             "as_of": as_of.isoformat(), **extra}
                yield f"matrix:{concept.concept_id}@{code}:{name}", dump(service.dispatch("resolve", arguments))


async def stdio_session(release_path: Path, with_coverage: bool) -> tuple[dict, dict]:
    env = {"PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
    if "PYTHONHASHSEED" in os.environ:
        env["PYTHONHASHSEED"] = os.environ["PYTHONHASHSEED"]
    params = StdioServerParameters(command=sys.executable, env=env, args=[
        "-m", "swisstip.mcp_server.server", "--release", str(release_path), *(["--with-coverage"] if with_coverage else [])])
    with open(os.devnull, "w", encoding="utf-8") as errlog:
        async with stdio_client(params, errlog=errlog) as (read, write):
            async with ClientSession(read, write) as session:
                initialized = await session.initialize()
                listed = await session.list_tools()
    init = initialized.model_dump(mode="json", by_alias=True, exclude_none=True)
    init.get("serverInfo", {}).pop("version", None)
    return init, listed.model_dump(mode="json", by_alias=True, exclude_none=True)


def stdio_meta(pack_dir: Path):
    for with_coverage in (False, True):
        suffix = ":with-coverage" if with_coverage else ""
        init, listed = asyncio.run(stdio_session(pack_dir / "release.json", with_coverage))
        yield f"stdio:initialize{suffix}", compact(init)
        yield f"stdio:tools/list{suffix}", compact(listed)


def records(pack_dir: Path, stdio: bool = True):
    service = ReleaseService.from_file(pack_dir / "release.json")
    hidden = ReleaseService.from_file(pack_dir / "release.json", coverage_tool=False)
    yield "instructions", service.instructions
    yield "instructions:coverage-hidden", hidden.instructions
    for name in ALL_TOOL_CONTRACTS:
        yield f"tool:{name}:description", service.tool_description(name)
        yield f"tool:{name}:input", json.dumps(service.tool_input_schema(name), ensure_ascii=False, sort_keys=True)
    for name, (_, output) in ALL_TOOL_CONTRACTS.items():
        yield f"tool:{name}:output", json.dumps(tool_output_schema(output), ensure_ascii=False, sort_keys=True)
    yield "tools", json.dumps(service.tools())
    yield "tools:coverage-hidden", json.dumps(hidden.tools())
    yield "health", json.dumps(health(service), ensure_ascii=False, sort_keys=True)
    root = service.get_coverage(GetCoverageRequest())
    yield "get_coverage:root", dump(root)
    for topic in getattr(root, "topics", []) or []:
        yield f"get_coverage:{topic.topic_id}", dump(service.get_coverage(GetCoverageRequest(parent_id=topic.topic_id)))
    evidence: dict[str, None] = {}
    suite, reported = suite_of(pack_dir)
    as_of = policy_date(service, suite) if suite else service.freshness.snapshot_date
    for case in suite.cases if suite else []:
        for number, step in enumerate(case.steps, 1):
            key = f"case:{case.case_id}:{number}"
            if step.search is not None:
                request = step.search.request()
                yield key + ":search", dump(service.search(request))
                yield key + ":ranking", ranking(service, request.query, request.jurisdiction.model_dump(exclude_none=True))
            elif step.resolve is not None:
                result = service.resolve(step.resolve.request(as_of))
                yield key + ":resolve", dump(result)
                if not isinstance(result, ToolError):
                    for item in result.results:
                        for fact in item.facts:
                            for evidence_id in getattr(fact, "evidence_ids", []) or []:
                                evidence[evidence_id] = None
    for name, reported_suite in reported.items():
        report = check_acceptance(service, reported_suite)
        report.pop("checked_at", None)
        yield f"acceptance-report:{name}", json.dumps(report, ensure_ascii=False, sort_keys=True)
    # The excerpts those resolves serve, then every other excerpt of the release, five at a time.
    for ids in (list(evidence), [evidence_id for evidence_id in service.evidence if evidence_id not in evidence]):
        for start in range(0, len(ids), 5):
            batch = ids[start:start + 5]
            yield f"get_evidence:{','.join(batch)}", dump(service.dispatch("get_evidence", {"evidence_ids": batch}))
    yield from raw_questions(service, suite, as_of)
    yield from probes(service, hidden, as_of)
    yield from register_sweep(service, as_of)
    yield from matrix(service, as_of)
    if stdio:
        yield from stdio_meta(pack_dir)


def snapshot(packs: list[str], out: Path, stdio: bool = True) -> dict[str, Path]:
    out.mkdir(parents=True, exist_ok=True)
    written = {}
    for pack in packs:
        started = time.perf_counter()
        pack_dir = ROOT / "releases" / pack
        path = out / f"{pack}.jsonl"
        seen: set[str] = set()
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps({"header": header(pack_dir, stdio)}, ensure_ascii=False) + "\n")
            for key, value in records(pack_dir, stdio):
                if key in seen:
                    raise ValueError(f"{pack}: the key {key!r} is recorded twice")
                seen.add(key)
                handle.write(json.dumps({"key": key, "value": value}, ensure_ascii=False) + "\n")
        digest = hashlib.sha256(b"".join(path.read_bytes().split(b"\n", 1)[1:])).hexdigest()
        print(f"{pack}: {len(seen)} records in {time.perf_counter() - started:.1f} s, records sha256 {digest[:16]}")
        written[pack] = path
    return written


def read_capture(path: Path) -> tuple[dict | None, dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    first = json.loads(lines[0]) if lines else {}
    head = first.get("header")
    rows = lines[1:] if head is not None else lines
    return head, {row["key"]: row["value"] for row in map(json.loads, rows)}


def flatten(value, prefix: str = "") -> dict:
    if isinstance(value, dict):
        return {k: v for key, item in value.items() for k, v in flatten(item, f"{prefix}{key}.").items()}
    return {prefix.rstrip("."): value}


def compare_headers(before: dict | None, after: dict | None, name: str) -> bool:
    """False when the two captures are not of the same release, suites and index; informative differences printed."""
    if before is None or after is None:
        print(f"{name}: REFUSED: the {'earlier' if before is None else 'new'} capture has no header; capture it again")
        return False
    old, new = flatten(before.get("binding", {})), flatten(after.get("binding", {}))
    bound = sorted(key for key in old.keys() | new.keys() if old.get(key) != new.get(key))
    for key in bound:
        print(f"{name}: REFUSED: binding {key} is {old.get(key)!r} before and {new.get(key)!r} after")
    old, new = flatten(before.get("info", {})), flatten(after.get("info", {}))
    for key in sorted(key for key in old.keys() | new.keys() if old.get(key) != new.get(key)):
        print(f"{name}: note: {key} {old.get(key)!r} before, {new.get(key)!r} after")
    return not bound


def compare(before: Path, after: Path, limit: int = 12) -> int | None:
    """The number of differing records, or None when the headers refuse the comparison."""
    if not before.is_file():
        print(f"{after.stem}: REFUSED: the earlier capture has no {before.name}; capture it first")
        return None
    old_head, old = read_capture(before)
    new_head, new = read_capture(after)
    if not compare_headers(old_head, new_head, after.stem):
        return None
    differences = [key for key in old.keys() | new.keys() if old.get(key) != new.get(key)]
    for key in sorted(differences)[:limit]:
        a, b = old.get(key), new.get(key)
        if a is None or b is None:
            print(f"  {key}: {'added' if a is None else 'removed'}")
            continue
        at = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
        print(f"  {key}: first difference at {at}: before ...{a[max(0, at - 60):at + 60]!r}\n{' ' * (len(key) + 4)}after  ...{b[max(0, at - 60):at + 60]!r}")
    print(f"{after.stem}: {len(old)} records before, {len(new)} after, {len(differences)} differ")
    return len(differences)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, required=True, help="directory for one <pack>.jsonl per pack")
    parser.add_argument("--pack", action="append",
                        help="pack folder under releases/; repeatable; default: the attested Swiss packs, " + " and ".join(SWISS_PACKS))
    parser.add_argument("--compare", type=Path, help="an earlier --out directory to compare with")
    parser.add_argument("--skip-stdio", action="store_true", help="leave out the stdio server sessions")
    args = parser.parse_args()
    # A difference can quote any character; a console that cannot print it gets an escape instead of a crash.
    sys.stdout.reconfigure(errors="backslashreplace")
    packs = args.pack or SWISS_PACKS
    written = snapshot(packs, args.out, stdio=not args.skip_stdio)
    if args.compare is None:
        return 0
    results = [compare(args.compare / f"{pack}.jsonl", path) for pack, path in written.items()]
    if any(result is None for result in results):
        return 2
    return 1 if sum(results) else 0


if __name__ == "__main__":
    sys.exit(main())
