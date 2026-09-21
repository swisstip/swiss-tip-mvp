# Swiss TIP demo image: OpenCode with the Zurich knowledge base

**Last update:** 21 September 2026

A test image, not a release image. It is the `mvp-zurich` pack image with
the [OpenCode](https://opencode.ai) agent and its web interface on top, so
that a browser is enough to ask the knowledge base a question and watch the
tool calls it answers from. Nothing in the knowledge base changes: the same
release, the same readiness record, the same semantic index and the same
MCP server as the pack image, which alone is the product.

The agent, its configuration, the plugin, the start script, the proxy and
the welcome panel of this directory are also built into the
[OpenCode image](https://github.com/swisstip/swiss-tip/blob/main/docker/opencode/README.md), without a server, a release or a
model: there `SWISSTIP_MCP_URL` names a Swiss TIP MCP server that runs
elsewhere, for example the slim image beside the embedding sidecar, where
the profile `demo` of the code repository's [compose.yaml](https://github.com/swisstip/swiss-tip/blob/main/compose.yaml) starts it.

```shell
docker run --rm -p 4096:4096 swiss-tip-demo:mvp-zurich
```

Then open `http://127.0.0.1:4096`, open a new session and click one of the
sample questions, or ask your own, for example:

> Ich bin tschechischer Staatsbuerger und beginne naechste Woche in Zuerich
> zu arbeiten. Bis wann muss ich mich anmelden?

## What runs in the container

| Process | Address | Role |
| --- | --- | --- |
| Ollama with `qwen3-embedding:0.6b` | `127.0.0.1:11434` | embeddings for hybrid search |
| `swisstip-mcp` with the `mvp-zurich` release | `127.0.0.1:8000` | the knowledge base, MCP on `/mcp`, `/health` beside it |
| `opencode web` | `127.0.0.1:4099` | the agent and its web interface |
| `opencode_web_shim.py` | `0.0.0.0:4096` | serves that interface, the routes it needs and the server does not answer, and the welcome panel |

Everything but the shim is bound to the loopback interface, so the web
interface is the only published port. The start script
([with-opencode.sh](https://github.com/swisstip/swiss-tip/blob/main/docker/opencode/with-opencode.sh)) starts the knowledge base first and
waits until it answers `/health`, then the agent, then the shim. With
`SWISSTIP_MCP_URL` set, as in the OpenCode image, it starts no knowledge
base and waits for the `/health` beside that address instead. OpenCode's start banner names its own port, `Web interface:
http://127.0.0.1:4099/`, which is not reachable from outside the container;
the shim's last log line names the container port to publish, 4096.

## Why the shim

The web interface is the desktop client's, and it asks its server for the
project list, the connected MCP servers, the default model and the state of
the working tree over paths under `/api`. The standalone server of
`opencode web` 1.18.31 answers only some of them. The rest fall through to
the single-page application, and the interface, reading the application
shell where it expects JSON, leaves its project list empty and its "New
session" control disabled, shows no model and no MCP server, and raises
"Failed to reload <project>: Unexpected token".

The same information is served on the paths without the `/api` prefix, so
`opencode_web_shim.py` answers those requests from them, in the
`{"data": ...}` envelope the `/api` routes use, and passes everything else
through, streaming, including the event stream. What it passes through it
decodes: the server compresses most answers when the browser asks it to, and
a proxy that forwards those bytes without saying they are compressed turns
every one of them into "Unexpected token" on the way in. The rule is
general - any `/api/<path>` answered with the application shell is answered
from `/<path>` when the server has it - and three paths need more:

| Path | Answered with |
| --- | --- |
| `/api/project` | `/project` without the `global` project, whose worktree is the container's root directory |
| `/api/mcp` | `/mcp` turned from an object of server name to state into the list of objects the interface reads |
| `/api/model/default` | the configured model's entry in `/api/model`; the server has no route of its own |

A path with no answer at all is logged once and answered `{"data": null}`,
so that a feature of the interface stays inert instead of breaking the page.
On this release those are `/api/server`, `/api/plugin`,
`/api/debug/location`, `/api/mcp/resource` and
`/api/experimental/integration/wellknown`; none of them is needed to ask a
question. Every one of these decisions is in the container's log, once per
path, so a route that starts to matter is named there rather than showing as
a dead control.

The workspace is also a Git repository with one empty commit, made in the
build: a directory outside a version-controlled tree has no project of its
own, and the interface would again have none to open a session in.

If a later OpenCode version serves these paths itself, the route fixes can
go; the welcome panel below still needs the shim.

## The welcome panel

OpenCode has no setting for a welcome text, so the shim adds one. Every HTML
page it passes through loads `/swiss-tip/welcome.js`, which the shim serves
from [welcome.js](https://github.com/swisstip/swiss-tip/blob/main/docker/opencode/welcome.js), preceded by the content of
[welcome.json](welcome.json) and the agent's worktree. The interface's
content security policy allows scripts from its own origin only, not inline
ones, so the configuration travels inside that script. The script:

- registers the workspace as the project in a browser that has none yet.
  The interface keeps its project list in the browser's local storage, not
  on the server, so a first visit would otherwise show an empty list and
  would need "Add project" before a session can be opened;
- shows the title, the coverage and the sample questions of `welcome.json`
  on the home screen while the server has no sessions, and on every
  new-session screen, where they replace the OpenCode logo. Under the note
  it names the release in small print, the one the server's `/health`
  reports, so the panel always shows the release that answers;
- types a clicked question into the prompt and sends it, after opening a
  new session when the click was on the home screen. It waits for the model
  selector first: a prompt sent before that selector is shown goes to
  another free model than the configured one.

The sample questions are the questions of acceptance cases of the release,
some slightly shortened (UAT-34, UAT-24, UAT-25, UAT-1, UAT-3, UAT-14 and
UAT-11), so each of them is known to be covered. The first three are plain
lookups (office hours, a registration duty, rubbish bags) from the Zurich
office and daily-life topics. To change the
text or the questions, edit `welcome.json` and rebuild, or mount another
file on `/etc/swiss-tip/welcome.json`. Its `pack` names the pack it was
written for. The start script reads the server's pack from `/health`; when
the two differ, which only a server elsewhere can bring about, the panel
keeps its note and the registration of the workspace, takes the pack as its
title and leaves out the coverage text and the questions. A file without
`pack` is shown on every server. The script finds the interface's
elements by their `data-component` and `data-action` attributes in OpenCode
1.18.31; if a later version renames them, the panel does not appear and the
interface works as before. `SWISSTIP_WELCOME=` (empty) turns the panel off.

## The tools

The agent answers from the knowledge base only: the baked configuration
`/etc/swiss-tip/opencode.json` names the loopback MCP server `swiss_tip` as
its only tool source, and the plugin
[swiss-tip-tools-only.js](https://github.com/swisstip/swiss-tip/blob/main/docker/opencode/swiss-tip-tools-only.js) refuses every tool call
that is not one of `swiss_tip`'s, before it runs, with an error that sends
the model back to `swiss_tip`. So there is no shell, no file access and no
web fetch.

The built-in tools are refused, not turned off. Since 17 September 2026 the
OpenCode Zen free tier rejects a request that does not offer them, with
"Error from provider (Console): OpenCode's free tier can only be used from
within OpenCode", and both `tools: false` and `permission: deny` leave them
out of the request. The model therefore sees them and, rarely, calls one;
the call fails and the answer goes on with `swiss_tip`. The build fails if
the configuration stops loading the plugin or stops naming a loopback MCP
server.

## Credentials, cost and the network

The image carries no credentials. Without an API key, OpenCode uses the
public OpenCode Zen key, which leaves only the free models enabled; the
default `opencode/ling-3.0-flash-fin-free` is one of them. Free models are
rate-limited, and a limit reached mid-answer ends the turn with a provider
error - the acceptance records of 13 and 15 September show the same
behaviour.

| Variable | Effect |
| --- | --- |
| `SWISSTIP_DEMO_MODEL` | the model, as `<provider>/<model>`; default `opencode/ling-3.0-flash-fin-free` |
| `OPENCODE_API_KEY` | an OpenCode Zen key; with it the account's paid models are enabled too |
| `OPENCODE_SERVER_PASSWORD` | HTTP basic authentication on port 4096; the user name is `opencode`, or `OPENCODE_SERVER_USERNAME` |
| `SWISSTIP_REQUIRE_PASSWORD` | when set, the container ends with an error instead of starting without `OPENCODE_SERVER_PASSWORD`; a hosted setup sets it |
| `SWISSTIP_MCP_USERNAME`, `SWISSTIP_MCP_PASSWORD` | only with `SWISSTIP_MCP_URL`, in the [OpenCode image](https://github.com/swisstip/swiss-tip/blob/main/docker/opencode/README.md): basic credentials for a server that asks for them |
| `SWISSTIP_WELCOME` | the welcome panel's `welcome.json`; default `/etc/swiss-tip/welcome.json`, empty for no panel |
| `OPENCODE_PORT` | the published port, served by the shim; default 4096 |
| `OPENCODE_INTERNAL_PORT` | the agent's own port on the loopback; default 4099 |
| `PORT` | the loopback MCP port; default 8000 |

Unlike the pack images, this one needs the network at run time: the model is
called over the internet, and the agent fetches its model catalogue at
start. Only the knowledge base is local. Without a password anyone who
reaches port 4096 can spend the model budget, so publish the port on
`127.0.0.1` unless the network is trusted:

```shell
docker run --rm -p 127.0.0.1:4096:4096 -e OPENCODE_SERVER_PASSWORD=... swiss-tip-demo:mvp-zurich
```

With a password the agent answers every request without credentials with
401, its own health route included. The start script takes that answer as
the agent being up. The shim passes a browser's request on with the
credentials the browser sent, or none, so the agent itself refuses a visitor
without the password; only the shim's two calls at start, for the route list
and the worktree, carry the password themselves. The image's health check
([opencode_health.py](https://github.com/swisstip/swiss-tip/blob/main/docker/opencode/opencode_health.py)) sends no credentials and takes
401 as alive.

[check_interface.py](https://github.com/swisstip/swiss-tip/blob/main/docker/opencode/check_interface.py) checks a running interface from
outside, with the standard library only: with `--password` first 401 without
credentials, then one project to open a session in, `swiss_tip` connected, a
default model, and the welcome panel with the workspace it registers. It asks
no question. The image workflow runs it, and it serves a hosted interface as
well:

```shell
python <code>/docker/opencode/check_interface.py --url http://127.0.0.1:4096 --password ...
```

## Build

The pack image must exist first; see [../README.md](https://github.com/swisstip/swiss-tip/blob/main/docker/README.md). On
GitHub, the workflow [Container images](../../.github/workflows/container-images.yml)
of this repository builds, tests and pushes this image with the input `images: all`, on the
Zurich pack image of the same run, or `images: demo`, on the one of `ghcr.io`, as
`ghcr.io/<owner>/swiss-tip-demo:<release_id>`, `:mvp-zurich` and `:latest`. The release image has no `latest`, because it is built for more than one pack; this image is built on `mvp-zurich` only, so `latest` is unambiguous.

```shell
docker build -f docker/demo-opencode/Dockerfile \
  --build-context shared=<code>/docker/opencode \
  -t swiss-tip-demo:mvp-zurich docker/demo-opencode
```

| Build argument | Meaning |
| --- | --- |
| `BASE_IMAGE` | the pack image; default `swiss-tip:mvp-zurich` |
| `OPENCODE_VERSION`, `OPENCODE_PACKAGE`, `OPENCODE_SHA256` | the OpenCode release, its platform package (`opencode-linux-x64`, or `-baseline` for a CPU without AVX2, or `opencode-linux-arm64`) and the digest of its tarball |
| `DEMO_MODEL` | the default model |

The binary is the platform package of the npm release, downloaded by digest
in a separate stage; no Node.js is installed. Changing `OPENCODE_VERSION` or
`OPENCODE_PACKAGE` means changing `OPENCODE_SHA256` with it.

## Licences

OpenCode is MIT-licensed and is not part of the Swiss TIP release. The
licence of the server and the notices of the sources are in
`/usr/share/doc/swiss-tip/`, and this file is
`/usr/share/doc/swiss-tip/demo-opencode.md` in the image.
