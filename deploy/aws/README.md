# Swiss TIP on AWS

**Last update:** 24 September 2026

One CloudFormation template, [swiss-tip.yaml](swiss-tip.yaml), creates one
EC2 instance that serves the Swiss TIP MCP server to the internet: the
pack's release image from `ghcr.io`, the one `docker run` of the quick start
serves, which carries the server, its embedding model and the pack's calendar
connector in one container, behind [Caddy](https://caddyserver.com), which
obtains the HTTPS certificate. With a
second domain the instance also runs the OpenCode web interface
([docker/opencode](https://github.com/swisstip/swiss-tip/blob/main/docker/opencode/README.md)) behind a name and a
password. The MCP endpoint is open unless it is given a name and a password
too. The stack is created in the AWS console from that one file; nothing is
installed on your machine and no repository access is needed on the host.

[Tested and not tested](#tested-and-not-tested) says what has been run where.

## What the stack creates

| Resource | What for |
| --- | --- |
| EC2 instance, Amazon Linux 2023, x86_64, `t3.small` by default | Docker with three containers at most: the server (with its embedding model and, with `Calendar` `yes`, the pack's calendar connector inside), Caddy and, with a demo domain, the web interface |
| Elastic IP | a public address that survives a stop and start; the A records point at it |
| Security group | ports 80 and 443 in (443 also over UDP, for HTTP/3); no SSH port |
| IAM role and instance profile | Session Manager for a shell without SSH, and reading the secrets below |
| Secrets Manager secret, only with a demo domain | the web interface's password: the one given, or else one the stack generates |
| Secrets Manager secret, only with `McpUsername` | the MCP endpoint's password, in the same way |
| Route 53 A records, only with a hosted zone ID | the domains, pointed at the Elastic IP |

The root volume is an encrypted gp3 volume of 20 GiB. The instance metadata
service takes session tokens only and answers one hop, so a container cannot
read the instance's credentials.

## Parameters

| Parameter | Default | Meaning |
| --- | --- | --- |
| `Pack` | `mvp-zurich` | the knowledge pack; the image is `<Registry>/swiss-tip:<Pack>` |
| `WelcomeUrl` | the pack's `welcome.json` on the `main` branch of this repository | the web interface's welcome panel, the coverage text and sample questions of `docker/demo-opencode/welcome.json`, downloaded at the first start; empty, or a failed download, gives the generic panel without questions. Until the branch that carries the file is merged, give its raw URL on that branch |
| `Calendar` | `yes` | the calendar connector the pack image carries, started beside the server in the same container ([dataset connectors](https://github.com/swisstip/swiss-tip/blob/main/docs/architecture/dataset-connectors.md); `mvp-zurich` has one, the waste-collection calendars of Zurich, Basel and St. Gallen). The server registers it on the container's loopback and offers the fifth tool `lookup`. `no` writes an empty `SWISSTIP_CONNECTORS=` into `.env`: four tools. A pack without datasets serves four tools either way |
| `SslipNames` | `none` | HTTPS without a domain of your own: `mcp` serves the MCP endpoint on `https://<ip>.sslip.io/mcp`, `mcp-and-demo` runs the web interface too, on `demo.<ip>.sslip.io`. `<ip>` is the Elastic IP with hyphens, for example `51-96-83-1`; [sslip.io](https://sslip.io) resolves it to the address and Caddy obtains the certificate. Needs `McpDomain` and `DemoDomain` empty |
| `McpDomain` | empty | for example `mcp.example.ai`; then `https://<domain>/mcp`. Empty (and `SslipNames` `none`): plain HTTP on port 80 of the Elastic IP |
| `DemoDomain` | empty | for example `demo.example.ai`; then the web interface runs on the instance too, over HTTPS and behind the password. Empty (and `SslipNames` other than `mcp-and-demo`): no web interface on this host |
| `HostedZoneId` | empty | only when the domains are in Route 53: the zone in which the A records are created |
| `McpUsername`, `McpPassword` | empty | empty: the MCP endpoint is open. A name: every path of the endpoint, `/health` too, asks for it and the password (basic credentials); the password is the one given, or else generated. Needs `McpDomain` or `SslipNames`, so that they travel over HTTPS only |
| `DemoUsername`, `DemoPassword` | `opencode`, empty | the web interface's name, and its password: the one given, or else generated. A hosted web interface always has a password |
| `Registry` | `ghcr.io/swisstip` | the image prefix; the packages must be public, the host logs in nowhere |
| `InstanceType` | `t3.small` | `t3.small`, `t3.medium`, `t3.large`, `c7i-flex.large` or `m7i-flex.large`; x86 only, because the images are built for x86 |
| `CpuCredits` | `unlimited` | T3 only: `unlimited` keeps the latency under sustained load and bills the surplus, `standard` throttles to the baseline |
| `VolumeGiB`, `SwapGiB` | 20, 2 | the root volume, and a swap file as headroom while the model loads |
| `LatestAmi` | the current Amazon Linux 2023 | leave as it is |

The embedding model takes 1.2 GiB of memory
([measured](https://github.com/swisstip/swiss-tip/blob/main/docker/README.md#measured)), so 2 GiB is the least that
serves hybrid search, and the web interface wants `t3.medium` or more beside
it. The calendar connector is one small Python process on a few hundred
kilobytes of rows, a few dozen MB; the model the web interface needs runs at
the provider, not here. On `t3.small` the server, its model, the connector,
Caddy and the web interface did run together
([tested](#tested-and-not-tested)), with little memory to spare. The
Free plan refuses to change an instance's type, so a stack that started small
stays small; a bigger host is a new stack. The web interface does not have to
run here: the same image runs on a
laptop against the hosted endpoint
([docker/opencode](https://github.com/swisstip/swiss-tip/blob/main/docker/opencode/README.md#against-a-hosted-server)),
and the instance then carries the server alone.

A password is 8 to 64 letters, digits, dots, underscores, tildes or hyphens,
so that it survives the host's `.env` file unquoted; a name is up to 32 of
the same without the tilde. Both password parameters are `NoEcho`. A
password reaches the host through its secret, which the instance reads at
its first start, never through the instance's user data, which the account
can read back. Leave `McpUsername` empty for an endpoint a test harness must
reach without credentials.

## Before you start

- An AWS account and a region, for example `eu-central-1` (Frankfurt). The
  region needs its default VPC, which every new account has; the template
  names no network.
- The images on `ghcr.io` must be public and current. The workflow
  [Container images](../../.github/workflows/container-images.yml) pushes
  the release image; the code repository's
  [workflow of the same name](https://github.com/swisstip/swiss-tip/blob/main/.github/workflows/container-images.yml)
  pushes `swiss-tip-opencode` with `images: opencode` or `all`. A new package starts private
  ([container images](https://github.com/swisstip/swiss-tip/blob/main/docker/README.md#build-on-github)).
- For HTTPS, a domain whose DNS you can edit.

## Create the stack

In the console: CloudFormation, "Create stack", "With new resources",
"Upload a template file", this directory's `swiss-tip.yaml`. Name the stack,
fill in the parameters, and on the last page acknowledge that the stack
creates IAM resources. The stack is complete after about three minutes; the
host then installs Docker and pulls the images, so the endpoint answers some
minutes later. The "Outputs" tab has the addresses:

| Output | Meaning |
| --- | --- |
| `PublicIp` | the Elastic IP for the A records |
| `McpEndpoint`, `Health` | the MCP endpoint for a client, and `/health` beside it |
| `McpPasswordSecret` | with `McpUsername`: the secret that holds the endpoint's password (Secrets Manager console, the secret, "Retrieve secret value") |
| `DemoUrl`, `DemoPasswordSecret` | with a demo domain: the web interface, and the secret that holds its password, read in the same way |
| `Shell` | a shell on the instance with Session Manager |

With the AWS CLI instead:

```shell
aws cloudformation deploy --stack-name swiss-tip --template-file deploy/aws/swiss-tip.yaml \
  --capabilities CAPABILITY_IAM --parameter-overrides McpDomain=mcp.example.ai
aws cloudformation describe-stacks --stack-name swiss-tip --query "Stacks[0].Outputs"
```

## Point the domains at it

Unless `HostedZoneId` did it, create an A record for each domain with the
value of `PublicIp` where the domain is registered. Caddy asks for the
certificate as soon as the name resolves to the instance and retries until
then; `sudo docker compose restart caddy` in `/opt/swiss-tip` makes it ask at
once. Every new stack asks for a new certificate, and Let's Encrypt issues
five a week for the same name.

With `SslipNames` there is nothing to point: the names contain the address.
A public name is logged with its certificate, and scanners were fetching the
open MCP endpoint seconds after it was issued; the web interface is behind
its password. The names are the address's, so a new stack has new ones.

A host that was created without them takes them by hand, because the host
script runs once and a changed stack parameter does not reach it. In
`/opt/swiss-tip/.env` set `SWISSTIP_MCP_SITE=<ip>.sslip.io`, and for the web
interface `SWISSTIP_DEMO_SITE=demo.<ip>.sslip.io`, `COMPOSE_PROFILES=demo`,
`OPENCODE_SERVER_USERNAME` and an `OPENCODE_SERVER_PASSWORD`, then `sudo
docker compose up -d`. The plain `http://<PublicIp>/mcp` then stops
answering, because Caddy serves that site on its name only.

## Check it

```shell
curl https://mcp.example.ai/health
python scripts/test/mcp/check_server.py --url https://mcp.example.ai/mcp --require-hybrid
python <code>/docker/opencode/check_interface.py --url https://demo.example.ai --password <password>
```

Behind a name and a password the first two take them as `curl -u
<name>:<password>` and `--username <name> --password <password>`, and the
third takes `--username` when the name is not `opencode`.

`/health` names the release and `search.configured_mode: hybrid`; with
`Calendar` `yes` its `connectors` list names the connector with `status:
ok` and the 15 datasets under `registered`. The round
trip is the one the image workflow runs, and `--require-hybrid` fails on any
search that fell back to lexical; it is written for the `mvp-zurich` release
of the same commit. The interface check expects 401 without credentials, then
a project, `swiss_tip` connected, a default model and the welcome panel. A
client connects with `claude mcp add --transport http swiss-tip
https://mcp.example.ai/mcp`, or as the
[image README](../../releases/mvp-zurich/README.md) shows for other clients.

With `McpUsername` the client sends basic credentials with every request:
the header `Authorization: Basic <token>`, where the token is the base64 of
`<name>:<password>` (`printf '%s' '<name>:<password>' | base64`).

```shell
claude mcp add --transport http swiss-tip https://mcp.example.ai/mcp --header "Authorization: Basic <token>"
```

In an OpenCode configuration it is `"headers": {"Authorization": "Basic
<token>"}` in the `swiss_tip` entry. The OpenCode image builds that entry
itself from `SWISSTIP_MCP_USERNAME` and `SWISSTIP_MCP_PASSWORD`
([docker/opencode](https://github.com/swisstip/swiss-tip/blob/main/docker/opencode/README.md#against-a-hosted-server)).
The web interface on this host needs none of it: it reaches the server on
the Compose network, not through Caddy.

## Operate

A shell opens from the `Shell` output (Session Manager); the files are in
`/opt/swiss-tip`, and `.env` is readable by root only, so Compose runs with
`sudo`.

```shell
sudo tail -n 40 /var/log/cloud-init-output.log   # the host setup, once, at the first start
cd /opt/swiss-tip
sudo docker compose ps
sudo docker compose logs -f swiss-tip            # one line per tool call
sudo docker compose logs caddy                   # certificates, and one line per request to the MCP site
sudo systemctl restart swiss-tip                 # pull the moving tags and recreate what changed: a new release
```

- **A new release.** The workflow moves `swiss-tip:<pack>`; then
  `sudo systemctl restart swiss-tip`. The same happens at every boot. New
  calendars come with the release image, so the same restart takes them.
- **Another setting.** The host script runs once, so a changed stack
  parameter does not reach a running host. Edit `/opt/swiss-tip/.env` and
  restart the service, or delete the stack and create it again, which also
  changes the Elastic IP.
- **A fresh host with the same address.** Update the stack with a change
  set that replaces the instance: the address and its attachment are
  resources of their own, so a replaced instance gets the same Elastic IP
  and runs the current host script at its first boot, with the stack's
  parameters. CloudFormation replaces the instance only when its image
  changes; when no newer Amazon Linux 2023 image has appeared since the
  last one, set `LatestAmi` to the other kernel flavour of the same
  distribution, `/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-6.12-x86_64`,
  and check in the change set that `Instance` changes `ImageId` before
  executing. A change set whose `Instance` row changes `UserData` alone
  would stop and start the same instance without running the script.
  Every hand edit of `.env` goes with the old instance, sslip.io names and
  the web interface included, and is made again afterwards.
- **The registry parameter.** `Registry` reaches the host once too. A stack
  created with an earlier image owner keeps pulling from it after a
  replacement, and an image that exists only under the current owner is
  `denied`; `SWISSTIP_REGISTRY` in `.env` is the line to correct, then
  `sudo systemctl restart swiss-tip`.
- **The web interface on and off.** `COMPOSE_PROFILES=demo` in `.env` starts
  it with the service; `sudo docker compose stop demo` stops it and leaves
  the server alone. Hosted, it refuses to start without a password.
- **The welcome panel.** `/opt/swiss-tip/welcome.json`, mounted into the
  web interface read-only; the container reads it at its start. New
  questions: replace the file (`sudo curl -fsSL -o welcome.json <raw URL>`,
  or edit it) and `sudo docker compose up -d --force-recreate --no-deps
  demo`, which leaves the server alone.
- **The calendar connector on and off.** Without `SWISSTIP_CONNECTORS` in
  `.env` the pack image starts the connector it carries; the line
  `SWISSTIP_CONNECTORS=` (empty) turns it off, and the server lists four
  tools and `connectors: []`. Then `sudo systemctl restart swiss-tip`: the
  server reads its connectors at startup, so this one restarts it.
- **A host set up with the slim image.** A host created before 24
  September 2026 runs the slim image, the embedding sidecar and, with the
  profile `calendar`, the calendar image. To move it to the one release
  image: replace `/opt/swiss-tip/compose.yaml` with this directory's file;
  in `.env`, delete the line `SWISSTIP_CONNECTORS=http://127.0.0.1:8100`
  (it would point the server at a connector the image then does not start)
  and take `calendar` out of `COMPOSE_PROFILES` (`demo,calendar` becomes
  `demo`); replace the last line of `watchdog.sh` with `docker compose
  restart swiss-tip`; then `sudo docker compose pull` and `sudo docker
  compose up -d --remove-orphans`, which removes the sidecar and the
  calendar container.
- **Names and passwords.** They are `SWISSTIP_MCP_USERNAME`,
  `SWISSTIP_MCP_PASSWORD`, `OPENCODE_SERVER_USERNAME` and
  `OPENCODE_SERVER_PASSWORD` in `.env`. Change them there and run `sudo
  docker compose up -d`, which recreates Caddy or the web interface and
  leaves the server alone; removing both MCP lines opens the endpoint. The
  secrets of the stack keep the first values.
- **The model after a crash.** Ollama runs beside the server in its
  container and is started once, with it; should it end, every search falls
  back to lexical, saying so. A timer runs `/opt/swiss-tip/watchdog.sh`
  every two minutes: it asks for the model from inside the server's
  container and restarts the server when there is no answer.
- **Stop and start.** A stopped instance costs its volume and its address
  only; started again, the service brings everything up.
- **Delete.** Deleting the stack removes every resource it created.

## Cost

Rough figures for Frankfurt; [AWS pricing](https://aws.amazon.com/ec2/pricing/on-demand/)
has the current ones. `t3.small` is about 0.02 USD an hour, the public IPv4
address 0.005 USD an hour, the 20 GiB volume about 2 USD a month and each
secret 0.40 USD a month: about 20 USD a month in all. With `CpuCredits:
unlimited`, sustained load above the baseline of 20 % a vCPU is billed at
0.05 USD a vCPU-hour, at most about 0.08 USD an hour on `t3.small`. An
account created since 15 July 2025 starts on the Free plan with up to 200 USD
of credits for six months, which these charges draw on; `t3.small`,
`c7i-flex.large` and `m7i-flex.large` are among its eligible instance types.
Set a budget with an alert in the Billing console either way.

## How the host is set up

The instance's user data is one script, run once by cloud-init. It makes the
swap file, installs Docker from the distribution and Docker Compose from its
GitHub release by digest, writes `/opt/swiss-tip/compose.yaml`, `Caddyfile`,
`caddy-start.sh` and `.env`, downloads `welcome.json` from `WelcomeUrl` (or
writes the generic panel), reads each password from its secret into `.env`,
and enables three systemd units: `swiss-tip.service` (pull, then
`docker compose up -d`, at every boot, retried on failure),
and `swiss-tip-watchdog.service` with its timer.

[compose.yaml](compose.yaml), [Caddyfile](Caddyfile) and
[caddy-start.sh](caddy-start.sh) in this directory are the files the host
gets: a stack is created from one file, so the template carries them in its
own text. [inline_files.py](inline_files.py) writes them into it after a
change, and [test_template.py](test_template.py) fails when the two differ
by a byte. Only Caddy publishes ports.

The MCP endpoint's name and password are Caddy's to ask for, not the
server's: the server, its package and its images are the same with and
without them. `caddy-start.sh` is Caddy's entry point. With both variables
set it hashes the password and writes the `basic_auth` block that the MCP
site of the `Caddyfile` imports; without them it writes nothing, the import
matches no file and the site is open; with one of the two it ends with an
error. Caddy keeps the hash only. Its bcrypt cost is low on purpose: every
request is checked against it, the hash never leaves the host, and the
password itself is in `.env` beside it. The server and the web interface
are reachable from Caddy alone; the web
interface's site defaults to a port nobody publishes, so without a demo
domain it is not served even if its container runs.

```shell
./.venv/Scripts/python.exe -m unittest discover -s deploy/aws
```

## The same files without AWS

On any host with Docker, from this directory; `.localhost` names get a
certificate of Caddy's own authority, so `curl` needs `-k`:

```shell
SWISSTIP_MCP_SITE=mcp.localhost SWISSTIP_DEMO_SITE=demo.localhost COMPOSE_PROFILES=demo \
  OPENCODE_SERVER_PASSWORD=... SWISSTIP_HTTP_PORT=8080 SWISSTIP_HTTPS_PORT=8443 docker compose up -d --wait
curl -k --resolve mcp.localhost:8443:127.0.0.1 https://mcp.localhost:8443/health
```

`SWISSTIP_MCP_USERNAME` and `SWISSTIP_MCP_PASSWORD` beside them put the MCP
site behind a name and a password, and `OPENCODE_SERVER_USERNAME` names the
web interface's user. On a trusted network, `SWISSTIP_MCP_SITE=:80` serves
plain HTTP on every name, where a password travels unprotected.

## Tested and not tested

Tested on 18 September 2026 on one Windows laptop with Docker Desktop, with
the images of `ghcr.io` and a local build of the OpenCode image:

- `cfn-lint` 1.57.0 reports nothing for the template in `eu-central-1`,
  `eu-central-2` and `us-east-1`, and `bash -n` accepts the host script.
- `compose.yaml` and the `Caddyfile` as above, with `.localhost` names: all
  four containers healthy; over HTTPS through Caddy, `/health` with
  `search.configured_mode: hybrid` and an MCP `initialize` under a host name
  the server does not know; the web interface 401 without credentials and
  200 with them, its project and `swiss_tip connected` routes, and its event
  stream arriving at once. Only Caddy had published ports.
- With `SWISSTIP_MCP_USERNAME` and `SWISSTIP_MCP_PASSWORD`: the MCP site
  answered 401 without credentials and with a wrong password, on `/health`
  and on `/mcp`, and 200 with them, over HTTPS and over plain HTTP; an MCP
  `initialize` with them succeeded; five requests took 4 to 30 ms each with
  the password and 4 to 14 ms without. Setting the two variables
  recreated Caddy and not the server. The round trip (`check_server.py
  --username --password --require-hybrid`) ran through the protected site
  with every search hybrid and one failure, the one it also has against the
  open site: the check of the coverage root is written for a newer release
  than the published image served. Without credentials, and with wrong
  ones, it ended with one line that says so. The OpenCode image, started with
  `docker run` against that site, ended with one error line without
  credentials, with a wrong password and with a name alone, and with both
  reported `swiss_tip connected`; Caddy logged its `/mcp` requests as the
  user's, with status 200. With `OPENCODE_SERVER_USERNAME=visitor` the web
  interface accepted that name with its password and refused `opencode` and
  the MCP site's credentials. A name with a space ended Caddy's start with
  one error line.
- The watchdog's check and remedy by hand: after `docker restart` of the
  server the check from inside its container failed, recreating the sidecar
  alone made it pass, and the server was not restarted by it.

Tested in an AWS account on 20 September 2026, in `eu-central-2` (Zurich),
with `McpDomain` and `DemoDomain` empty and the published images public: the
console flow of [Create the stack](#create-the-stack) end to end, including
the IAM capability acknowledgement; `CREATE_COMPLETE` in about three minutes;
`/health` on the Elastic IP over plain HTTP answering `mvp-zurich-2026-09-19-v15`
with `search.configured_mode: hybrid` a few minutes after; and
`check_server.py --require-hybrid` against the endpoint, `0 failure(s)`,
every search hybrid. The host script ran to completion on Amazon Linux 2023
and the `Shell` output opened a working Session Manager session.

The same host was then given sslip.io names and the web interface by hand, as
[Point the domains at it](#point-the-domains-at-it) describes, on `t3.small`
and the Free plan: Let's Encrypt issued certificates for `<ip>.sslip.io` and
`demo.<ip>.sslip.io`, the four containers ran (`demo` healthy), `check_server.py
--require-hybrid` passed over HTTPS with 0 failures on its second run (on the
first, the first search fell back to lexical while the embedding model loaded,
with 235 MB of memory available and 403 MB of swap in use), and the web
interface answered a sample question through the hosted server. A change of
the instance type to `t3.medium` in a stack update was refused: "This
operation is not available for free plan accounts".

The `SslipNames` parameter, the split of the Elastic IP into an address and its
attachment, and the outputs that follow are checked by `cfn-lint` 1.57.0 (no
findings in `eu-central-1`, `eu-central-2` and `us-east-1`) and by
`test_template.py`, and have not been run in an AWS account.

The `Calendar` parameter, the `calendar` service of `compose.yaml`, the
`SWISSTIP_CONNECTORS` line of `.env` and the watchdog's recreation of the
connector were run on 23 September 2026 on the stack of 20 September: a
change set with the new template and `LatestAmi` set to the kernel 6.12
flavour replaced the instance and kept the Elastic IP, the first change set
without it had shown `UserData` as the only change of `Instance` and was
deleted. The new host pulled from the stack's old image owner and was
denied the calendar image, which exists under `swisstip` only;
`SWISSTIP_REGISTRY` corrected in `.env` and the service restarted, the
four containers came up healthy, `/health` named release
`mvp-zurich-2026-09-22-v7` with the connector `ok` and the five Zurich
datasets registered, the sslip.io names and the web interface were set by
hand again, Let's Encrypt issued both certificates, the interface answered
401 without credentials, and it answered the next organic-waste collection
day for 8001 from the connector. The same three containers, server,
sidecar and connector, had run together on a laptop before through the
code repository's `compose.yaml` with the profiles `calendar` and `demo`.

The single release image in place of the slim image, the sidecar and the
calendar image was run on 24 September 2026 on one Windows laptop, with this
directory's `compose.yaml` and the published `swiss-tip:mvp-zurich` (release
`mvp-zurich-2026-09-24-v5`, server 0.3.2) behind Caddy on plain HTTP: the
server healthy in about ten seconds, `/health` with `search.configured_mode:
hybrid` and the connector `ok` with 15 datasets, and `check_server.py
--require-hybrid --require-lookup` with 0 failures (lookup for 8001: 28
September). With `SWISSTIP_CONNECTORS=` in `.env` the server came up with
`connectors: []`. With Ollama killed inside the container, the watchdog's
check failed, its restart brought the model back, and the next check passed.
`cfn-lint` 1.57.0 reports nothing for the template in `eu-central-1`,
`eu-central-2` and `us-east-1`. The same evening the running host of 23
September (`t3.small`, Free plan) was moved by hand as
[Operate](#operate) describes for a host set up with the slim image: three
containers (server, web interface, Caddy), the server healthy with the
connector, Ollama and the server started in that order and the model loaded
in 5.7 s; `/health` over HTTPS named release `mvp-zurich-2026-09-24-v5`
ready, `search.configured_mode: hybrid` and the connector `ok` with 15
datasets; `check_server.py --require-hybrid --require-lookup` passed with 0
failures, every search hybrid and the lookup for 8001 answered 28
September. The host then had 311 MB of memory available and 758 MB of swap
in use. A new stack created from the template has not been run.

Not tested: `SslipNames` and a stack created with it, the certificate from
Let's Encrypt for a domain of one's own, the Route 53 records,
`McpDomain`/`McpUsername`/`DemoDomain` and the secrets they create (given or
generated password), the two rules on those parameters, and the watchdog and
restart behaviour over a longer run. The Free plan's eligibility of every
resource is not verified either.
