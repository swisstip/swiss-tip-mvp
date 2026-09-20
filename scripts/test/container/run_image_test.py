"""Test a published Swiss TIP image, pulled from its registry, with OpenCode as the caller.

    python scripts/test/container/run_image_test.py
    python scripts/test/container/run_image_test.py --live
    python scripts/test/container/run_image_test.py --live --case german-work-permit
    python scripts/test/container/run_image_test.py --image ghcr.io/<owner>/swiss-tip:<tag> --require-public

The server under test is the image alone: the script pulls it (unless
--no-pull), starts it as a container on a free loopback port and talks to it
only over HTTP. Nothing of the checkout is served; the checkout supplies the
test clients, run as subprocesses:

1. Anonymous registry access: whether the tag can be pulled without a login,
   as the jury would pull it (a failure only with --require-public).
2. The pulled image: its registry digest and the release ID and content digest
   labels.
3. /health of the running container names the release of the labels and
   reports it as ready (a matching readiness.json in the image).
4. scripts/test/mcp/check_server.py --url against the container (every check of
   the round trip; the step reports how many).
5. The container's own log shows the tool calls of step 4, so the answers
   came from the container.
6. OpenCode connects to the endpoint (run_opencode_test.py --check-connection
   with --url).
7. With --live, the standing cases through OpenCode against the container, one
   harness run per --case (default zurich-registration and
   german-work-permit), with the harness's heuristic assessment. The answers
   are graded by hand against docs/product/user-acceptance-tests.md; the
   assessment does not fail the run.

The container log, the steps and the harness run folders are written to
.local/container-image-test/run-<timestamp>/summary.json. The exit code is 1
when a step of 1 to 6 fails (1 only with --require-public) or a live session
made no MCP call, and 0 otherwise.
"""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_IMAGE = "ghcr.io/swisstip/swiss-tip:mvp-zurich"  # the pack's moving tag; --image names a release
DEFAULT_CASES = ["zurich-registration", "german-work-permit"]
RELEASE_LABEL = "swiss-tip.release.id"
DIGEST_LABEL = "swiss-tip.release.content-sha256"


def python() -> str:
    candidate = ROOT / (".venv/Scripts/python.exe" if os.name == "nt" else ".venv/bin/python")
    return str(candidate) if candidate.is_file() else sys.executable


def run(command: list[str], timeout=None) -> subprocess.CompletedProcess:
    return subprocess.run(command, cwd=ROOT, text=True, encoding="utf-8", errors="replace",
                          capture_output=True, timeout=timeout)


def free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


def split_image(image: str) -> tuple[str, str, str]:
    """ghcr.io/owner/name:tag -> (registry, repository, tag)."""
    registry, _, rest = image.partition("/")
    repository, _, tag = rest.rpartition(":") if ":" in rest else (rest, "", "latest")
    return registry, repository, tag or "latest"


def anonymous_pull_status(image: str) -> tuple[bool, str]:
    """Ask the registry for the tag's manifest with an anonymous token, as a client without a login does."""
    registry, repository, tag = split_image(image)
    if registry != "ghcr.io":
        return False, f"not checked: {image} is not a ghcr.io reference"
    try:
        with urllib.request.urlopen(f"https://ghcr.io/token?scope=repository:{repository}:pull&service=ghcr.io",
                                    timeout=20) as response:
            token = json.load(response).get("token", "")
        request = urllib.request.Request(f"https://ghcr.io/v2/{repository}/manifests/{tag}", method="HEAD", headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.oci.image.index.v1+json, application/vnd.oci.image.manifest.v1+json, "
                      "application/vnd.docker.distribution.manifest.list.v2+json"})
        with urllib.request.urlopen(request, timeout=20) as response:
            return True, f"HTTP {response.status}"
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code}; the package is private or the tag does not exist"
    except (OSError, ValueError) as exc:
        return False, str(exc)


def wait_for_health(url: str, seconds: int = 60) -> dict | None:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=3) as response:
                return json.load(response)
        except (OSError, ValueError):
            time.sleep(1)
    return None


def harness_folder(output: str) -> Path | None:
    match = re.search(r"^Config: (.+)$", output, re.MULTILINE)
    return Path(match.group(1).strip()).parent if match else None


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--image", default=DEFAULT_IMAGE, help=f"image reference to pull and test; default {DEFAULT_IMAGE}")
    parser.add_argument("--no-pull", action="store_true", help="test the local copy of --image without pulling")
    parser.add_argument("--require-public", action="store_true", help="fail when the tag cannot be pulled anonymously")
    parser.add_argument("--live", action="store_true", help="run the standing cases through OpenCode with the model")
    parser.add_argument("--case", action="append", help="harness case for --live, repeatable; default: both standing cases")
    parser.add_argument("--model", help="OpenCode model for --live; default: the harness's model")
    parser.add_argument("--port", type=int, help="loopback port for the container; default: a free port")
    parser.add_argument("--keep", action="store_true", help="leave the container running after the test")
    parser.add_argument("--output", type=Path, default=ROOT / ".local/container-image-test")
    args = parser.parse_args(argv)
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    folder = args.output / f"run-{stamp}"
    folder.mkdir(parents=True, exist_ok=False)
    port = args.port or free_port()
    endpoint = f"http://127.0.0.1:{port}/mcp"
    name = f"swiss-tip-image-test-{stamp}"
    summary = {"image": args.image, "endpoint": endpoint, "container": name,
               "started_at": datetime.now(timezone.utc).isoformat(), "steps": [], "harness_runs": {}}
    failures = []

    def step(label, ok, detail="", required=True):
        print(f"{'ok  ' if ok else 'FAIL' if required else 'warn'} {label}" + (f": {detail}" if detail else ""), flush=True)
        summary["steps"].append({"step": label, "ok": ok, "required": required, "detail": detail})
        if required and not ok:
            failures.append(label)
        return ok

    def finish() -> int:
        summary["finished_at"] = datetime.now(timezone.utc).isoformat()
        summary["failures"] = failures
        (folder / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\n{len(failures)} failure(s); saved {folder}")
        return 1 if failures else 0

    public, detail = anonymous_pull_status(args.image)
    step("the tag can be pulled without a login", public, detail, required=args.require_public)

    if not args.no_pull:
        pulled = run(["docker", "pull", args.image], timeout=900)
        last_line = ((pulled.stdout + pulled.stderr).strip().splitlines() or [""])[-1]
        if not step("docker pull", pulled.returncode == 0, last_line):
            return finish()
    inspected = run(["docker", "image", "inspect", args.image])
    if not step("image present locally", inspected.returncode == 0, inspected.stderr.strip()):
        return finish()
    config = json.loads(inspected.stdout)[0]
    labels = config.get("Config", {}).get("Labels") or {}
    summary.update(image_id=config.get("Id"), repo_digests=config.get("RepoDigests"), labels=labels)
    step("release labels present", bool(labels.get(RELEASE_LABEL) and labels.get(DIGEST_LABEL)),
         f"{labels.get(RELEASE_LABEL)} content {labels.get(DIGEST_LABEL)}; digest {(config.get('RepoDigests') or ['none'])[0]}")

    started = run(["docker", "run", "-d", "--name", name, "-p", f"127.0.0.1:{port}:8000", args.image])
    if not step("container started", started.returncode == 0, started.stderr.strip() or started.stdout.strip()[:12]):
        return finish()
    try:
        health = wait_for_health(f"http://127.0.0.1:{port}/health")
        summary["health"] = health
        step("/health answers and names the labelled release",
             bool(health) and health.get("status") == "ok" and health.get("release_id") == labels.get(RELEASE_LABEL),
             f"{(health or {}).get('release_id')}, {(health or {}).get('facts')} facts, search {((health or {}).get('search') or {}).get('configured_mode')}")
        readiness = (health or {}).get("readiness") or {}
        step("/health reports the release as ready", readiness.get("status") == "ready",
             f"attested by {readiness.get('attested_by')} at {readiness.get('attested_at')}" if readiness.get("status") == "ready"
             else readiness.get("reason", "no readiness field"))
        if health is None:
            return finish()

        checked = run([python(), "scripts/test/mcp/check_server.py", "--url", endpoint], timeout=300)
        (folder / "check-server.txt").write_text(checked.stdout + checked.stderr, encoding="utf-8")
        counts = re.findall(r"^(ok  |FAIL) ", checked.stdout, re.MULTILINE)
        step("check_server.py --url against the container", checked.returncode == 0 and counts and "FAIL" not in counts,
             f"{counts.count('ok  ')} of {len(counts)} checks passed")
        # The container is fresh, so every per-call line in its log is a call of the check above.
        served = run(["docker", "logs", name]).stderr.count(" tool=")
        step("the container's log records the check's tool calls", served > 0, f"{served} tool call lines")

        # The licence files come from the basic image, outside the release mount point; the README is the pack's.
        documents = run(["docker", "exec", name, "ls", "/usr/share/doc/swiss-tip"])
        carried = documents.stdout.split()
        step("the image carries LICENSE and NOTICE", {"LICENSE", "NOTICE"} <= set(carried),
             ", ".join(carried) or documents.stderr.strip())
        served_files = run(["docker", "exec", name, "ls", "/srv/swiss-tip"])
        step("the image carries the pack README beside the release", "README.md" in served_files.stdout.split(),
             " ".join(served_files.stdout.split()) or served_files.stderr.strip())

        harness = [python(), "scripts/test/mock-mcp/run_opencode_test.py", "--server", "real", "--url", endpoint]
        if args.model:
            harness += ["--model", args.model]
        connection = run([*harness, "--check-connection"], timeout=300)
        run_folder = harness_folder(connection.stdout)
        listing = (run_folder / "mcp-list.txt").read_text(encoding="utf-8", errors="replace") if run_folder else ""
        listing = " ".join(re.sub(r"\x1b\[[0-9;]*m", "", listing).split())
        summary["harness_runs"]["check-connection"] = str(run_folder)
        step("OpenCode connects to the container",
             bool(re.search(r"\bswiss_tip connected\b", listing)) and endpoint in listing, listing[:160])

        for case in (args.case or DEFAULT_CASES) if args.live else []:
            print(f"\n##### OpenCode live: {case}", flush=True)
            live = run([*harness, "--live", "--case", case], timeout=1800)
            run_folder = harness_folder(live.stdout)
            (folder / f"opencode-{case}.txt").write_text(live.stdout + live.stderr, encoding="utf-8")
            summary["harness_runs"][case] = str(run_folder)
            scenarios = {}
            if run_folder and (run_folder / "summary.json").is_file():
                scenarios = json.loads((run_folder / "summary.json").read_text(encoding="utf-8")).get("scenarios", {})
            for scenario, record in scenarios.items():
                verdict = record.get("assessment", {})
                called = verdict.get("turn1_called_mcp", verdict.get("called_mcp"))
                shown = {key: value for key, value in verdict.items() if isinstance(value, (bool, int))}
                step(f"OpenCode {scenario} called the container", bool(called), json.dumps(shown))
            step(f"OpenCode {case} completed", live.returncode == 0 and bool(scenarios), str(run_folder))
    finally:
        logs = run(["docker", "logs", name])
        (folder / "container.log").write_text(logs.stdout + logs.stderr, encoding="utf-8")
        if args.keep:
            print(f"container {name} left running on {endpoint}")
        else:
            run(["docker", "rm", "-f", name])
    return finish()


if __name__ == "__main__":
    raise SystemExit(main())
