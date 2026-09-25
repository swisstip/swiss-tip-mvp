# syntax=docker/dockerfile:1
#
# Swiss TIP MCP server with semantic search on the mvp-zurich release (KB1):
# foreign nationals in Switzerland, from residence permits and registration
# to social insurance, tax at source, the driving licence, health insurance
# and naturalisation, federal rules with Canton and City of Zurich. The base
# image (docker/mcp) plus the release, its readiness record and its
# semantic index, the image README the pack publishes, and the pack's
# waste-collection calendars behind the calendar connector. The build
# context is the pack directory, a checkout's releases/mvp-zurich or the
# same four files downloaded from a GitHub release; the second context
# "datasets" is the pack's dataset bundles, a checkout's datasets/mvp-zurich.
# Published as ghcr.io/<owner>/swiss-tip:<release_id> by the workflow
# container-images.yml.
#
#   docker build -t swiss-tip-mcp:0.3.2 docker/mcp
#   docker build -f docker/mvp-zurich/Dockerfile --build-context datasets=datasets/mvp-zurich -t swiss-tip:mvp-zurich releases/mvp-zurich
#   docker run --rm -p 8000:8000 swiss-tip:mvp-zurich          MCP on http://127.0.0.1:8000/mcp
#   docker run --rm -i swiss-tip:mvp-zurich --transport stdio
#   docker run --rm -p 8000:8000 -e SWISSTIP_CONNECTORS= swiss-tip:mvp-zurich   without the calendar
#
# The calendar connector runs in this container beside the server and
# Ollama, on the loopback address only: with-calendar starts it, waits for
# it and registers it through SWISSTIP_CONNECTORS, so the server lists the
# fifth tool lookup from the first request. The connector stays a process
# of its own that the server reaches over HTTP, as in the two-container
# setup; SWISSTIP_CONNECTORS set to anything, even empty, leaves it out.
#
# The build fails when the release does not validate or is not ready, when
# a search on the bundled model does not run hybrid (an index for another
# release or another model digest), and when a dataset bundle does not
# validate or does not bind to a concept of the release.
#
# The workflow builds it for linux/amd64 and linux/arm64. The platform that
# is not the runner's runs these checks under emulation, where one embedding
# takes several seconds, so its check search waits 120 seconds per call
# instead of the 10 the server waits.

ARG BASE_IMAGE=swiss-tip-mcp:0.3.2
FROM ${BASE_IMAGE}
ARG RELEASE_ID=""
ARG RELEASE_CONTENT_SHA256=""
ARG REVISION=""
# Empty is PyPI. Another index is used with PyPI behind it, as for the base images.
ARG PACKAGE_INDEX=""
ARG BUILDPLATFORM
ARG TARGETPLATFORM
LABEL org.opencontainers.image.title="Swiss TIP MCP server with the mvp-zurich knowledge release" \
      org.opencontainers.image.description="MCP server for foreign nationals in Switzerland: residence permits and registration, social insurance on arrival and departure, tax at source, the foreign driving licence, health insurance and premium reduction, and naturalisation (federal rules, Canton and City of Zurich), every fact human-reviewed and cited to an official page, with hybrid lexical and semantic concept search on a bundled local embedding model and the waste-collection calendars of Zurich, Basel and St. Gallen behind the lookup tool. Streamable HTTP on port 8000 at /mcp, or stdio with --transport stdio. The image README is /srv/swiss-tip/README.md, the licence and notices are in /usr/share/doc/swiss-tip/, and the labels swiss-tip.release.id and swiss-tip.release.content-sha256 name the bundled release." \
      org.opencontainers.image.licenses="Apache-2.0" \
      org.opencontainers.image.version="${RELEASE_ID}" \
      org.opencontainers.image.revision="${REVISION}" \
      swiss-tip.release.id="${RELEASE_ID}" \
      swiss-tip.release.content-sha256="${RELEASE_CONTENT_SHA256}"

USER root
# The connector of the same version as the server the base image carries; its dependencies are the server's already.
RUN pip install --no-cache-dir \
      ${PACKAGE_INDEX:+--index-url "${PACKAGE_INDEX}" --extra-index-url https://pypi.org/simple/} \
      "swisstip-calendar-connector==$(python -c "from importlib.metadata import version; print(version('swisstip-core'))")"

COPY --chmod=755 <<'EOF' /usr/local/bin/with-calendar
#!/bin/sh
# Start the calendar connector on loopback when the image carries dataset
# bundles, wait until it answers, register it with the server through
# SWISSTIP_CONNECTORS, then run the given command in its place. Standard
# output belongs to the command, because MCP over stdio uses it; the
# connector writes to standard error only. When the connector does not
# start, the command still runs, without the lookup tool.
set -eu
datasets=/srv/swiss-tip/datasets
port=8100
if [ -z "${SWISSTIP_CONNECTORS+set}" ] && ls "$datasets"/*/dataset.json > /dev/null 2>&1; then
    swisstip-calendar-connector --datasets-dir "$datasets" --host 127.0.0.1 --port "$port" 1>&2 &
    if python -c "import sys, time, urllib.request
for attempt in range(100):
    try:
        urllib.request.urlopen(sys.argv[1], timeout=2)
        sys.exit(0)
    except OSError:
        time.sleep(0.2)
sys.exit(1)" "http://127.0.0.1:$port/health"; then
        export SWISSTIP_CONNECTORS="http://127.0.0.1:$port"
    else
        echo "with-calendar: the calendar connector did not start; the server runs without lookup" >&2
    fi
fi
exec "$@"
EOF

USER 10001
COPY release.json readiness.json semantic-index.json README.md /srv/swiss-tip/
COPY --from=datasets --chown=10001:10001 . /srv/swiss-tip/datasets/

RUN swisstip-mcp --release /srv/swiss-tip/release.json --require-ready --health > /dev/null \
 && python -c "import json, sys; m = json.load(open(sys.argv[1], encoding='utf-8'))['manifest']; got = (m['release_id'], m['content_sha256']); sys.exit(0 if all(w in ('', g) for w, g in zip(sys.argv[2:], got)) else 'release.json is %s %s, the build arguments name %s %s' % (*got, *sys.argv[2:]))" \
      /srv/swiss-tip/release.json "${RELEASE_ID}" "${RELEASE_CONTENT_SHA256}" \
 && if [ "${TARGETPLATFORM}" = "${BUILDPLATFORM}" ]; then check_timeout=10; else check_timeout=120; fi  && SWISSTIP_REQUIRE_SEMANTIC=1 SWISSTIP_CHECK_TIMEOUT="$check_timeout" with-ollama python /usr/local/lib/swiss-tip/check_semantic.py \
      /srv/swiss-tip/release.json /srv/swiss-tip/semantic-index.json \
      "Ich bin tschechischer Staatsbürger und beginne nächste Woche in Zürich zu arbeiten. Bis wann muss ich mich anmelden?" \
      "Je suis citoyen tchèque et je commence à travailler à Zurich. Quand dois-je m'annoncer?" \
      "Can my wife join me in Switzerland if I have a B permit?" \
      "weak:Wie wird das Wetter morgen in Zürich?" \
 && with-calendar swisstip-mcp --release /srv/swiss-tip/release.json --require-ready --health \
    | python -c "import glob, json, sys; c = json.load(sys.stdin)['connectors']; n = len(glob.glob('/srv/swiss-tip/datasets/*/dataset.json')); got = [(e['status'], len(e['registered'])) for e in c]; print('calendar connector: %d of %d datasets registered' % (sum(r for _, r in got), n)); sys.exit(0 if n and got == [('ok', n)] else 'the calendar connector registered %s of %d datasets: %s' % (got, n, c))"

ENTRYPOINT ["tini", "--", "with-calendar", "with-ollama", "swisstip-mcp", "--release", "/srv/swiss-tip/release.json", "--require-ready", "--semantic-index", "/srv/swiss-tip/semantic-index.json", "--transport", "streamable-http", "--host", "0.0.0.0"]
CMD []
