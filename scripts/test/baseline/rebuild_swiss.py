"""Rebuild the attested Swiss releases in memory and require the committed bytes.

    ./.venv/Scripts/python.exe scripts/test/baseline/rebuild_swiss.py
    ./.venv/Scripts/python.exe scripts/test/baseline/rebuild_swiss.py --pack mvp-zurich --text mvp-zurich=<dir>

For each pack (default: mvp-zurich and mvp-wallisellen) the release is built from its curation.yaml, the place files
the curation names and the pack's text dataset, exactly as the knowledge builder builds it, with the three values a
build cannot know pinned from the committed manifest: created_at, acceptance_suite_sha256 and schema_version. Nothing
is written. The proof passes when, for every pack:

- the committed release.json loads and dumps back to its own bytes (dump_release(load_release(p)) == bytes);
- the rebuilt release dumps to exactly the bytes of the committed release.json;
- the sha256 of those bytes is the release_sha256 of the pack's readiness.json.

The text datasets are Git-ignored, so the proof runs locally only. A pack's dataset is the first of
<packs checkout>/.local/<pack>/text and <folder holding both checkouts>/.local/<pack>/text that has an index.json;
--text overrides it. The exit code is 1 when a pack fails, 2 when an input is missing.
"""

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

from swisstip.build.curation import load_curation
from swisstip.build.places import place_register_for
from swisstip.build.release_build import BuildError, build_release
from swisstip.core.release import Manifest, dump_release, load_release

ROOT = Path(__file__).resolve().parents[3]
PACKS = ["mvp-zurich", "mvp-wallisellen"]


def text_dataset(pack: str, override: dict[str, Path]) -> Path | None:
    candidates = [override[pack]] if pack in override else [ROOT / ".local" / pack / "text",
                                                               ROOT.parent / ".local" / pack / "text"]
    return next((path for path in candidates if (path / "index.json").is_file()), None)


def readiness_sha(pack_dir: Path) -> str:
    return json.loads((pack_dir / "readiness.json").read_text(encoding="utf-8"))["release_sha256"]


def first_difference(a: str, b: str) -> str:
    at = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
    line = a.count("\n", 0, at) + 1
    return (f"first difference at character {at} (line {line}): committed ...{a[max(0, at - 80):at + 80]!r}\n"
            f"    rebuilt   ...{b[max(0, at - 80):at + 80]!r}")


def rebuild(pack: str, text_dir: Path) -> list[str]:
    """The failures of one pack; empty when the rebuild is byte-identical and the readiness hash matches."""
    pack_dir = ROOT / "releases" / pack
    release_path = pack_dir / "release.json"
    committed_bytes = release_path.read_bytes()
    committed_text = committed_bytes.decode("utf-8")
    committed = load_release(release_path)
    failures = []
    if dump_release(committed) != committed_text:
        failures.append("dump_release(load_release(release.json)) differs from the file: "
                        + first_difference(committed_text, dump_release(committed)))
    sha = hashlib.sha256(committed_bytes).hexdigest()
    if sha != readiness_sha(pack_dir):
        failures.append(f"release.json hashes to {sha}, readiness.json names {readiness_sha(pack_dir)}")
    curation_path = pack_dir / "curation.yaml"
    curation = load_curation(curation_path)
    manifest = committed.manifest
    release, report = build_release(curation, text_dir, manifest.release_id, created_at=manifest.created_at,
                                    place_register=place_register_for(curation, curation_path),
                                    acceptance_suite_sha256=manifest.acceptance_suite_sha256)
    if report["dropped"]:
        failures.append(f"the rebuild dropped {len(report['dropped'])} fact(s) or concept(s)")
    # The build writes the current schema version; the committed one is pinned. It lies outside the content digest.
    release.manifest = Manifest.model_validate({**release.manifest.model_dump(), "schema_version": manifest.schema_version})
    rebuilt_text = dump_release(release)
    rebuilt_sha = hashlib.sha256(rebuilt_text.encode("utf-8")).hexdigest()
    if release.manifest.content_sha256 != manifest.content_sha256:
        failures.append(f"content_sha256 {release.manifest.content_sha256} rebuilt, {manifest.content_sha256} committed")
    if rebuilt_text != committed_text:
        failures.append("the rebuilt release differs from release.json: " + first_difference(committed_text, rebuilt_text))
    elif rebuilt_sha != readiness_sha(pack_dir):
        failures.append(f"the rebuilt release hashes to {rebuilt_sha}, readiness.json names {readiness_sha(pack_dir)}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pack", action="append", help="pack folder under releases/; repeatable; default: " + ", ".join(PACKS))
    parser.add_argument("--text", action="append", default=[], metavar="PACK=DIR",
                        help="the text dataset of a pack, overriding the .local lookup; repeatable")
    args = parser.parse_args()
    # A difference can quote any character; a console that cannot print it gets an escape instead of a crash.
    sys.stdout.reconfigure(errors="backslashreplace")
    override = {}
    for item in args.text:
        pack, _, path = item.partition("=")
        override[pack] = Path(path)
    failed = missing = 0
    for pack in args.pack or PACKS:
        text_dir = text_dataset(pack, override)
        if not (ROOT / "releases" / pack / "release.json").is_file() or text_dir is None:
            print(f"{pack}: MISSING release.json or text dataset (.local/{pack}/text)")
            missing += 1
            continue
        started = time.perf_counter()
        try:
            failures = rebuild(pack, text_dir)
        except (BuildError, OSError, ValueError) as exc:
            failures = [f"the rebuild failed: {exc}"]
        elapsed = time.perf_counter() - started
        if failures:
            failed += 1
            print(f"{pack}: FAILED in {elapsed:.1f} s (text dataset {text_dir})")
            for failure in failures:
                print(f"  {failure}")
        else:
            print(f"{pack}: byte-identical, sha256 {readiness_sha(ROOT / 'releases' / pack)} as attested, "
                  f"in {elapsed:.1f} s (text dataset {text_dir})")
    return 2 if missing else 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
