# syntax=docker/dockerfile:1
#
# Swiss TIP MCP server with semantic search on the mvp-zurich release (KB1):
# foreign nationals in Switzerland, from residence permits and registration
# to social insurance, tax at source, the driving licence, health insurance
# and naturalisation, federal rules with Canton and City of Zurich. The base
# image (docker/mcp) plus the release, its readiness record and its
# semantic index, and the image README the pack publishes. The build context
# is the pack directory, a checkout's releases/mvp-zurich or the same four
# files downloaded from a GitHub release. Published as ghcr.io/<owner>/swiss-tip:<release_id> by the
# workflow container-images.yml.
#
#   docker build -t swiss-tip-mcp:0.3.0 docker/mcp
#   docker build -f docker/mvp-zurich/Dockerfile -t swiss-tip:mvp-zurich releases/mvp-zurich
#   docker run --rm -p 8000:8000 swiss-tip:mvp-zurich          MCP on http://127.0.0.1:8000/mcp
#   docker run --rm -i swiss-tip:mvp-zurich --transport stdio
#
# The build fails when the release does not validate or is not ready, and
# when a search on the bundled model does not run hybrid (an index for
# another release or another model digest).

ARG BASE_IMAGE=swiss-tip-mcp:0.3.0
FROM ${BASE_IMAGE}
ARG RELEASE_ID=""
ARG RELEASE_CONTENT_SHA256=""
ARG REVISION=""
LABEL org.opencontainers.image.title="Swiss TIP MCP server with the mvp-zurich knowledge release" \
      org.opencontainers.image.description="MCP server for foreign nationals in Switzerland: residence permits and registration, social insurance on arrival and departure, tax at source, the foreign driving licence, health insurance and premium reduction, and naturalisation (federal rules, Canton and City of Zurich), every fact human-reviewed and cited to an official page, with hybrid lexical and semantic concept search on a bundled local embedding model. Streamable HTTP on port 8000 at /mcp, or stdio with --transport stdio. The image README is /srv/swiss-tip/README.md, the licence and notices are in /usr/share/doc/swiss-tip/, and the labels swiss-tip.release.id and swiss-tip.release.content-sha256 name the bundled release." \
      org.opencontainers.image.licenses="Apache-2.0" \
      org.opencontainers.image.version="${RELEASE_ID}" \
      org.opencontainers.image.revision="${REVISION}" \
      swiss-tip.release.id="${RELEASE_ID}" \
      swiss-tip.release.content-sha256="${RELEASE_CONTENT_SHA256}"

COPY release.json readiness.json semantic-index.json README.md /srv/swiss-tip/

RUN swisstip-mcp --release /srv/swiss-tip/release.json --require-ready --health > /dev/null \
 && python -c "import json, sys; m = json.load(open(sys.argv[1], encoding='utf-8'))['manifest']; got = (m['release_id'], m['content_sha256']); sys.exit(0 if all(w in ('', g) for w, g in zip(sys.argv[2:], got)) else 'release.json is %s %s, the build arguments name %s %s' % (*got, *sys.argv[2:]))" \
      /srv/swiss-tip/release.json "${RELEASE_ID}" "${RELEASE_CONTENT_SHA256}" \
 && SWISSTIP_REQUIRE_SEMANTIC=1 with-ollama python /usr/local/lib/swiss-tip/check_semantic.py \
      /srv/swiss-tip/release.json /srv/swiss-tip/semantic-index.json \
      "Ich bin tschechischer Staatsbürger und beginne nächste Woche in Zürich zu arbeiten. Bis wann muss ich mich anmelden?" \
      "Je suis citoyen tchèque et je commence à travailler à Zurich. Quand dois-je m'annoncer?" \
      "Can my wife join me in Switzerland if I have a B permit?" \
      "weak:Wie hoch ist die Mehrwertsteuer in der Schweiz?"

ENTRYPOINT ["tini", "--", "with-ollama", "swisstip-mcp", "--release", "/srv/swiss-tip/release.json", "--require-ready", "--semantic-index", "/srv/swiss-tip/semantic-index.json", "--transport", "streamable-http", "--host", "0.0.0.0"]
CMD []
