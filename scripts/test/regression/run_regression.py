"""Replay a pack's regression pack (acceptance.yaml plus regression.yaml) lexically and with hybrid search (no LLM).

    ./.venv/Scripts/python.exe scripts/test/regression/run_regression.py [--pack mvp-zurich]
    ./.venv/Scripts/python.exe scripts/test/regression/run_regression.py --lexical-only --no-write
    ./.venv/Scripts/python.exe scripts/test/regression/run_regression.py --render-only

Every case is answered in-process by the ReleaseService the server uses, once with lexical search only and once
with the release's semantic index and the local Ollama embedding model it names (the retrieval the container
serves). Search steps send the query of the case: a question in a query language of the release as asked, any other
question as the German or English key terms the suite's author prepared (`translated: true`). The outcome is
written to releases/<pack>/regression-report.json, and every case with its latest results to
releases/<pack>/test-cases.md (`swisstip.build.case_catalogue`); --render-only rewrites that page from the committed
suites and reports without a replay, for example after acceptance-answers.json changed. Exit code 1 when a blocking
case fails in a mode, 2 when the hybrid run is not possible or a query fell back to lexical search, unless
--lexical-only is given.
"""

import argparse
import json
import sys
from pathlib import Path

from swisstip.build.acceptance import load_regression
from swisstip.build.case_catalogue import CATALOGUE_FILE, load_case_catalogue
from swisstip.runtime.acceptance import check_acceptance, issues_of, regression_report
from swisstip.runtime.semantic import (OllamaEmbedder, SemanticError, SemanticSearch, load_index,
                                       semantic_index_binding)
from swisstip.runtime.service import ReleaseService

ROOT = Path(__file__).resolve().parents[3]


def hybrid_service(pack_dir: Path, ollama_url: str, timeout: float) -> tuple[ReleaseService, dict]:
    """The service with hybrid search, and the identity of the index bytes and settings it used.

    The binding is returned alongside the service because `regression_report` refuses a hybrid run that cannot say
    which index bytes and retrieval settings produced it - a report that only says "hybrid" is not reproducible.
    """
    service = ReleaseService.from_file(pack_dir / "release.json")
    index_path = pack_dir / "semantic-index.json"
    index = load_index(index_path, service.release)
    embedder = OllamaEmbedder(model=index.model, base_url=ollama_url, timeout_seconds=timeout)
    semantic = SemanticSearch(index, embedder)
    service.semantic_search = semantic
    binding = semantic_index_binding(index_path, index, min_score=semantic.min_score,
                                     candidate_limit=semantic.candidate_limit)
    return service, binding


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pack", default="mvp-zurich")
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    parser.add_argument("--timeout", type=float, default=60, help="seconds per embedding request")
    parser.add_argument("--lexical-only", action="store_true", help="skip the hybrid run and record why")
    parser.add_argument("--no-write", action="store_true", help="print the outcome without writing the report")
    parser.add_argument("--render-only", action="store_true",
                        help=f"rewrite {CATALOGUE_FILE} from the committed suites and reports without a replay")
    args = parser.parse_args()

    pack_dir = ROOT / "releases" / args.pack
    if args.render_only:
        write_catalogue(pack_dir)
        return 0
    acceptance, regression, combined = load_regression(pack_dir)
    reports: dict[str, dict | str] = {"lexical": check_acceptance(ReleaseService.from_file(pack_dir / "release.json"), combined)}
    exit_code = 0
    binding: dict | None = None
    if args.lexical_only:
        reports["hybrid"] = "not run (--lexical-only)"
    else:
        try:
            service, binding = hybrid_service(pack_dir, args.ollama_url, args.timeout)
            reports["hybrid"] = check_acceptance(service, combined)
        except (OSError, ValueError, SemanticError) as exc:
            reports["hybrid"] = f"semantic search unavailable: {exc}"
            binding = None
            exit_code = 2
    report = regression_report(reports, acceptance.digest(), regression.digest(), semantic_index=binding)

    for mode, run in report["runs"].items():
        if "skipped" in run:
            print(f"{mode}: skipped, {run['skipped']}")
            continue
        print(f"{mode} ({run['retrieval_mode']}): {run['passed']} of {run['cases']} cases pass; blocking failed "
              f"{run['failed'] or 'none'}; quarantined {len(run['quarantined'])}, still failing "
              f"{len(run['quarantined_failed'])}, now passing {run['quarantined_passing'] or 'none'}; "
              f"{run['unjudged_steps']} hybrid-only step(s) not judged")
        for issue in issues_of(reports[mode]):
            print("   ", issue)
        if run["failed"]:
            exit_code = max(exit_code, 1)
        if mode == "hybrid" and run["retrieval_mode"] != "hybrid":
            print("hybrid: some queries fell back to lexical search; the run is not a hybrid replay")
            exit_code = 2
    if not args.no_write:
        path = pack_dir / "regression-report.json"
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"wrote {path.relative_to(ROOT)}")
        write_catalogue(pack_dir)
    return exit_code


def write_catalogue(pack_dir: Path) -> None:
    path = pack_dir / CATALOGUE_FILE
    path.write_text(load_case_catalogue(pack_dir), encoding="utf-8", newline="\n")
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    sys.exit(main())
