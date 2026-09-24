"""Replay a pack's acceptance and regression questions against the knowledge graph in its release (no LLM).

    ./.venv/Scripts/python.exe scripts/test/regression/run_graph_regression.py [--pack mvp-zurich] [--no-write]

Every question is asked of `get_knowledge_graph` in-process, as a caller following the server's instructions would,
and judged against what the suites already expect (`swisstip.runtime.graph_regression`): a question whose search
expects a concept must reach a domain its topic bridges to, among the first three, with the topic in
covered_topics; a question the release declines must not be pointed at a covered topic with a strong match. The
outcome is written to releases/<pack>/graph-regression-report.json. The report is a measurement, not a gate: the exit
code is 0 unless the release carries no graph.
"""

import argparse
import json
import sys
from pathlib import Path

from swisstip.build.acceptance import load_regression
from swisstip.runtime.graph_regression import graph_regression
from swisstip.runtime.service import ReleaseService

ROOT = Path(__file__).resolve().parents[3]
REPORT_FILE = "graph-regression-report.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pack", default="mvp-zurich")
    parser.add_argument("--no-write", action="store_true", help="print the outcome without writing the report")
    args = parser.parse_args()

    pack_dir = ROOT / "releases" / args.pack
    _, _, combined = load_regression(pack_dir)
    service = ReleaseService.from_file(pack_dir / "release.json")
    if service.graph_index is None:
        print(f"{args.pack}: the release carries no knowledge graph")
        return 2
    report = graph_regression(service, combined)
    subject, decline = report["subject"], report["decline"]
    print(f"{args.pack} ({report['method']}): subject {subject['passed']} of {subject['cases']} reach a domain of their "
          f"topic ({subject['first']} as the first); decline {decline['passed']} of {decline['cases']} not pointed at a "
          f"covered topic; unbridged topics {report['unbridged'] or 'none'}; largest answer {report['max_bytes']} bytes")
    if not args.no_write:
        path = pack_dir / REPORT_FILE
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
