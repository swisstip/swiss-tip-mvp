# syntax=docker/dockerfile:1
#
# Swiss TIP MCP server with semantic search on the mvp-wallisellen release:
# official Stadt Wallisellen information for residents and visitors. The base
# image (docker/semantic) plus the release, its readiness record and its
# semantic index. The build context is the pack directory, a checkout's
# releases/mvp-wallisellen or the same three files downloaded from a GitHub
# release.
#
#   docker build -t swiss-tip-semantic:0.2.5 docker/semantic
#   docker build -f docker/mvp-wallisellen/Dockerfile -t swiss-tip:mvp-wallisellen releases/mvp-wallisellen
#   docker run --rm -p 8000:8000 swiss-tip:mvp-wallisellen     MCP on http://127.0.0.1:8000/mcp
#   docker run --rm -i swiss-tip:mvp-wallisellen --transport stdio
#
# The build fails when the release does not validate or is not ready, and
# when a search on the bundled model does not run hybrid (an index for
# another release or another model digest).

ARG BASE_IMAGE=swiss-tip-semantic:0.2.5
FROM ${BASE_IMAGE}
ARG RELEASE_ID=""
ARG RELEASE_CONTENT_SHA256=""
ARG REVISION=""
LABEL org.opencontainers.image.title="Swiss TIP MCP server - mvp-wallisellen with semantic search" \
      org.opencontainers.image.description="MCP server for official Stadt Wallisellen information (city services, moving, waste, building, taxes, politics, schools, families, health, leisure), every fact cited to an official page, with hybrid lexical and semantic concept search on a bundled local embedding model. Streamable HTTP on port 8000 at /mcp, or stdio with --transport stdio." \
      org.opencontainers.image.version="${RELEASE_ID}" \
      org.opencontainers.image.revision="${REVISION}" \
      swiss-tip.release.id="${RELEASE_ID}" \
      swiss-tip.release.content-sha256="${RELEASE_CONTENT_SHA256}"

COPY release.json readiness.json semantic-index.json /srv/swiss-tip/

RUN swisstip-mcp --release /srv/swiss-tip/release.json --require-ready --health > /dev/null \
 && python -c "import json, sys; m = json.load(open(sys.argv[1], encoding='utf-8'))['manifest']; got = (m['release_id'], m['content_sha256']); sys.exit(0 if all(w in ('', g) for w, g in zip(sys.argv[2:], got)) else 'release.json is %s %s, the build arguments name %s %s' % (*got, *sys.argv[2:]))" \
      /srv/swiss-tip/release.json "${RELEASE_ID}" "${RELEASE_CONTENT_SHA256}" \
 && SWISSTIP_REQUIRE_SEMANTIC=1 with-ollama python /usr/local/lib/swiss-tip/check_semantic.py \
      /srv/swiss-tip/release.json /srv/swiss-tip/semantic-index.json \
      "Wann ist die Stadtverwaltung Wallisellen geöffnet?" \
      "Ich ziehe nach Wallisellen um, wo melde ich mich an?" \
      "Where can I dispose of old electronic devices?"

ENTRYPOINT ["tini", "--", "with-ollama", "swisstip-mcp", "--release", "/srv/swiss-tip/release.json", "--require-ready", "--semantic-index", "/srv/swiss-tip/semantic-index.json", "--transport", "streamable-http", "--host", "0.0.0.0"]
CMD []
