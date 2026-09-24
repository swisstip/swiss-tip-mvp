# syntax=docker/dockerfile:1
#
# Test image, not a release image: the mvp-zurich pack image plus the
# OpenCode agent with its web interface, so that a browser is enough to ask
# the knowledge base a question and watch the tool calls. The pack image
# serves MCP on the container's loopback; OpenCode runs in the same
# container with a baked configuration whose only tool source is that
# server, and its web interface is the one port the image publishes.
#
#   docker build -f docker/demo-opencode/Dockerfile \
#     --build-context shared=<code>/docker/opencode \
#     -t swiss-tip-demo:mvp-zurich docker/demo-opencode
#   docker run --rm -p 127.0.0.1:4096:4096 swiss-tip-demo:mvp-zurich      GUI on http://127.0.0.1:4096
#
# The image carries no credentials. Without an API key OpenCode uses the
# public OpenCode Zen key, which leaves only the free models enabled; the
# default model is one of them. A key in OPENCODE_API_KEY, if given at run
# time, enables the paid models of that account.
#
# Unlike the pack images, this one needs the network at run time: the model
# is called over the internet. Only the knowledge base is local.
#
# Two build contexts. This directory holds what belongs to the pack: the
# welcome panel with its coverage text and sample questions, and the image
# README. The named context "shared" is the code repository's
# docker/opencode (swisstip/swiss-tip), which holds the agent configuration,
# the plugin, the start script, the proxy shim and the panel script that this
# image shares with the swiss-tip-opencode image; they live there once and
# are not copied into this repository. The OpenCode binary is the platform
# package of the npm release, downloaded by digest; no Node.js is installed.

ARG BASE_IMAGE=swiss-tip:mvp-zurich
ARG PYTHON_IMAGE=python:3.14-slim
# Declared before the first FROM, so that every stage that names them gets these values: an ARG with its default
# inside a stage is empty in the next one, which left the version label, and the image tag taken from it, empty.
ARG OPENCODE_VERSION=1.18.31
ARG OPENCODE_PACKAGE=opencode-linux-x64
ARG OPENCODE_SHA256=6d89da252a8b030d923e728396dc34465cf6095101b78222b0ee337b68140dea

# The download stage keeps curl and the tarball out of the final image.
FROM ${PYTHON_IMAGE} AS opencode
ARG OPENCODE_VERSION
ARG OPENCODE_PACKAGE
ARG OPENCODE_SHA256
ADD https://registry.npmjs.org/${OPENCODE_PACKAGE}/-/${OPENCODE_PACKAGE}-${OPENCODE_VERSION}.tgz /tmp/opencode.tgz
RUN echo "${OPENCODE_SHA256}  /tmp/opencode.tgz" | sha256sum -c - \
 && mkdir -p /out \
 && tar -xzf /tmp/opencode.tgz -C /out --strip-components=2 package/bin/opencode \
 && chmod 755 /out/opencode

FROM ${BASE_IMAGE}
ARG OPENCODE_VERSION
ARG OPENCODE_PACKAGE
ARG DEMO_MODEL=opencode/ling-3.0-flash-fin-free
LABEL org.opencontainers.image.title="Swiss TIP demo: OpenCode with the mvp-zurich knowledge release" \
      org.opencontainers.image.description="Test image. The mvp-zurich pack image (MCP server, human-reviewed facts on foreign nationals in Switzerland, hybrid search on a bundled embedding model) with the OpenCode agent and its web interface on port 4096. OpenCode is configured with the loopback MCP server as its only tool source, with a plugin that refuses every built-in tool; the browser is the whole interface. It carries no credentials and defaults to a free OpenCode Zen model, and it needs the network to reach that model." \
      org.opencontainers.image.licenses="Apache-2.0" \
      swiss-tip.demo.opencode.version="${OPENCODE_VERSION}" \
      swiss-tip.demo.opencode.package="${OPENCODE_PACKAGE}" \
      swiss-tip.demo.model="${DEMO_MODEL}"

# OPENCODE_PORT is the published one, served by the shim; the agent itself
# listens on OPENCODE_INTERNAL_PORT and PORT stays the MCP server's, both on
# the loopback, and the base image's health check keeps watching PORT.
ENV OPENCODE_PORT=4096 \
    OPENCODE_INTERNAL_PORT=4099 \
    SWISSTIP_DEMO_MODEL=${DEMO_MODEL} \
    SWISSTIP_WORKSPACE=/home/swisstip/workspace \
    SWISSTIP_WELCOME=/etc/swiss-tip/welcome.json \
    OPENCODE_DISABLE_AUTOUPDATE=1 \
    OPENCODE_DISABLE_LSP_DOWNLOAD=1 \
    OPENCODE_DISABLE_PROJECT_CONFIG=1 \
    OPENCODE_DISABLE_SHARE=1 \
    OPENCODE_CONFIG=/etc/swiss-tip/opencode.json

USER root
# The directories are made here, because a COPY --chmod=644 creates the
# directories it needs with that mode too, and an unreadable /etc/swiss-tip or
# /usr/local/lib/swiss-tip stops the runtime user from reading what is in it,
# as the slim MCP image notes for its documents directory. The base image
# happens to carry /usr/local/lib/swiss-tip already; naming it here means the
# build does not depend on that.
# There is no browser in the container, and opencode web starts one; the
# link makes that a silent success instead of a logged stack trace. Git is
# for the workspace below, not for the agent, which has no shell.
RUN apt-get update \
 && apt-get install -y --no-install-recommends git \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir -p /etc/swiss-tip /usr/local/lib/swiss-tip /home/swisstip/workspace \
 && chown -R swisstip /home/swisstip \
 && ln -s /bin/true /usr/local/bin/xdg-open

COPY --from=opencode /out/opencode /usr/local/bin/opencode
COPY --from=shared --chmod=644 opencode.json /etc/swiss-tip/opencode.json
COPY --chmod=644 README.md /usr/share/doc/swiss-tip/demo-opencode.md
COPY --from=shared --chmod=755 with-opencode.sh /usr/local/bin/with-opencode
COPY --from=shared --chmod=644 opencode_web_shim.py opencode_health.py welcome.js swiss-tip-tools-only.js /usr/local/lib/swiss-tip/
COPY --chmod=644 welcome.json /etc/swiss-tip/welcome.json

USER 10001
# The web interface is project-based, and a project is a version-controlled
# directory. Without one, the agent's directory belongs to the "global"
# project, whose worktree is the root of the file system, and the interface
# has no project of its own to open a session in. One empty commit in the
# workspace makes it that project.
RUN git -c init.defaultBranch=main init -q /home/swisstip/workspace \
 && git -C /home/swisstip/workspace \
      -c user.name="Swiss TIP demo" -c user.email="demo@swiss-tip.invalid" \
      commit -q --allow-empty -m "Swiss TIP demo workspace"

# The agent talks to the knowledge base and to nothing else: the build fails
# unless the configuration loads the plugin that refuses every built-in tool
# and names the loopback MCP server, and unless the binary runs. The welcome
# panel must have a title and questions that are plain strings.
RUN opencode --version \
 && python -c "import ast, pathlib; ast.parse(pathlib.Path('/usr/local/lib/swiss-tip/opencode_web_shim.py').read_text(encoding='utf-8'))" \
 && test -s /usr/local/lib/swiss-tip/welcome.js \
 && python -c "import json, sys; w = json.load(open('/etc/swiss-tip/welcome.json', encoding='utf-8')); sys.exit(None if w.get('title') and all(isinstance(q, str) and q for q in w.get('questions', [])) else 'welcome.json needs a title and non-empty question strings')" \
 && python -c "import httpx, starlette, uvicorn" \
 && python -c "import json, sys; c = json.load(open('/etc/swiss-tip/opencode.json', encoding='utf-8')); s = c['mcp']['swiss_tip']; sys.exit(None if s['type'] == 'remote' and s['url'].startswith('http://127.0.0.1:') and c['plugin'] == ['file:///usr/local/lib/swiss-tip/swiss-tip-tools-only.js'] else 'the baked configuration does not restrict the agent to the loopback MCP server')" \
 && grep -q 'startsWith("swiss_tip_")' /usr/local/lib/swiss-tip/swiss-tip-tools-only.js

EXPOSE 4096
# The knowledge base on PORT and the web interface on OPENCODE_PORT. With
# OPENCODE_SERVER_PASSWORD the interface answers 401, which is an answer.
HEALTHCHECK --interval=30s --timeout=5s --start-period=90s --retries=3 \
  CMD python /usr/local/lib/swiss-tip/opencode_health.py

ENTRYPOINT ["tini", "--", "with-opencode"]
CMD []
