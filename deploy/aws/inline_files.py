"""Write compose.yaml, the Caddyfile and caddy-start.sh of this directory into the template.

    ./.venv/Scripts/python.exe deploy/aws/inline_files.py

A stack is created from one file, so swiss-tip.yaml carries the three files
in the host script of its user data, each between a `cat > file <<'MARKER'`
line and its MARKER. Edit and test the files here, then run this script;
test_template.py fails while the template and the files differ. The standard
library is all it needs.
"""

from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "swiss-tip.yaml"
FILES = {"SWISSTIP_COMPOSE": "compose.yaml", "SWISSTIP_CADDYFILE": "Caddyfile", "SWISSTIP_CADDY_START": "caddy-start.sh"}
# The indentation of the literal block the host script is written in.
INDENT = " " * 16


def inlined(content: str) -> str:
    """The file as lines of that block; a line without text stays empty, so no line ends in spaces."""
    return "".join((INDENT + line if line.strip() else "") + "\n" for line in content.splitlines())


def main() -> int:
    template = TEMPLATE.read_text(encoding="utf-8").replace("\r\n", "\n")
    updated = template
    for marker, name in FILES.items():
        opening = "<<'%s'\n" % marker
        if updated.count(opening) != 1:
            sys.exit(f"{TEMPLATE.name} has no single heredoc {marker}")
        begin = updated.index(opening) + len(opening)
        end = updated.index(INDENT + marker + "\n", begin)
        content = (HERE / name).read_text(encoding="utf-8").replace("\r\n", "\n")
        updated = updated[:begin] + inlined(content) + updated[end:]
    if updated == template:
        print(f"{TEMPLATE.name} already carries the files")
        return 0
    TEMPLATE.write_bytes(updated.encode("utf-8"))
    print(f"{TEMPLATE.name} updated; run the tests of this directory and cfn-lint")
    return 0


if __name__ == "__main__":
    sys.exit(main())
