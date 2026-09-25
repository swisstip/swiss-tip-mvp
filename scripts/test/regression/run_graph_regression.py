"""Replay a pack's acceptance and regression questions against the knowledge graph in its release (no LLM).

    ./.venv/Scripts/python.exe scripts/test/regression/run_graph_regression.py [--pack mvp-zurich] [--no-write]
    ./.venv/Scripts/python.exe scripts/test/regression/run_graph_regression.py --hybrid [--ollama-url URL]

Every question is asked of `get_knowledge_graph` in-process, as a caller following the server's instructions would,
and judged against what the suites already expect (`swisstip.runtime.graph_regression`): a question whose search
expects a concept must reach a domain its topic bridges to, among the first three, with the topic in
covered_topics; a question the release declines must not be pointed at a covered topic with a strong match. The
outcome is written to releases/<pack>/graph-regression-report.json (graph-regression-report-hybrid.json with
--hybrid). Domains are matched by words, or with --hybrid also with the local Ollama embedding model the pack's
semantic index names, as a server started with --semantic-index matches them. The report is a measurement, not a gate: the
exit code is 0 unless the release carries no graph (2) or the hybrid run fell back to words (2).
"""

import argparse
import json
import sys
from pathlib import Path

from swisstip.build.acceptance import load_regression
from swisstip.runtime.graph_regression import graph_regression
from swisstip.runtime.semantic import OllamaEmbedder
from swisstip.runtime.service import ReleaseService

ROOT = Path(__file__).resolve().parents[3]
REPORT_FILE = "graph-regression-report.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pack", default="mvp-zurich")
    parser.add_argument("--no-write", action="store_true", help="print the outcome without writing the report")
    parser.add_argument("--hybrid", action="store_true", help="match domains with the local embedding model as well")
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    parser.add_argument("--timeout", type=float, default=60, help="seconds per embedding request")
    args = parser.parse_args()

    pack_dir = ROOT / "releases" / args.pack
    _, _, combined = load_regression(pack_dir)
    service = ReleaseService.from_file(pack_dir / "release.json")
    if service.graph_index is None:
        print(f"{args.pack}: the release carries no knowledge graph")
        return 2
    if args.hybrid:
        # The model of the pack's semantic index; the graph embeds its own domains, so the index itself is not read.
        model = json.loads((pack_dir / "semantic-index.json").read_text(encoding="utf-8"))["model"]
        service.graph_embedder = OllamaEmbedder(model=model, base_url=args.ollama_url, timeout_seconds=args.timeout)
    report = graph_regression(service, combined)
    subject, decline = report["subject"], report["decline"]
    print(f"{args.pack} ({report['modes']}): subject {subject['passed']} of {subject['cases']} reach a domain of their "
          f"topic ({subject['first']} as the first); decline {decline['passed']} of {decline['cases']} not pointed at a "
          f"covered topic; unbridged topics {report['unbridged'] or 'none'}; largest answer {report['max_bytes']} bytes")
    if args.hybrid and set(report["modes"]) != {"hybrid"}:
        print("hybrid: some questions fell back to words; the run is not a hybrid replay")
        return 2
    if not args.no_write:
        path = pack_dir / (REPORT_FILE.replace(".json", "-hybrid.json") if args.hybrid else REPORT_FILE)
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
