---
title: Deployment spec - POCDAPP314 with nginx reverse proxy
type: spec
updated: 2026-07-28
tags: [dq-coe, evaluation, deployment, nginx, infrastructure]
---

# Deployment spec: POCDAPP314 + nginx reverse proxy

## 1. Executive summary

The Skills Evaluation app is deployed to a single Linux host, **POCDAPP314
(10.21.12.62)** in POCLAB, as a Docker Compose stack. A **host-level nginx**
terminates TLS and reverse-proxies to it.

The pattern is deliberately built for reuse: nginx runs as a **shared ingress**
independent of any single application, each app gets **its own hostname and its
own certificate on the shared IP**, and onboarding the next app (dq-studio) is
**one new file in `/etc/nginx/conf.d/` plus one DNS record**. No existing app is
touched.

Application stacks are deployed and operated through **Portainer**, using
git-backed stacks, so the deployment method is the same for every application and
does not depend on someone having shell access.

Four decisions were confirmed before writing this:

- **Addressing:** shared IP, one FQDN per app, routed by `Host` header and TLS
  SNI. Per-app IPs were considered and rejected as unnecessary - see §3.2.
- **Certificates:** issued by the internal CA, one per hostname.
- **Deployment mechanism:** Portainer git-backed stacks. Secrets are entered as
  stack environment variables in Portainer, not as a `.env` file on disk.
- **Portainer access:** behind nginx on its own FQDN, like any other vhost.

**Portainer is an admin plane, not an application.** It mounts the Docker socket,
which makes it root-equivalent on this host: anyone who reaches that UI and
authenticates can start a privileged container and take the box. It is therefore
published on loopback only, reached through nginx, and its vhost should carry an
IP allow-list. See §9.

**Status: designed, not yet executed.** Nothing in this document has been run
against POCDAPP314. Every command is written to be run by a human with sudo on
the box. Items needing another team are marked **ACTION**.

---

## 2. Component inventory

| Layer | Component | Where it runs | Listens on |
|---|---|---|---|
| Ingress | nginx | Host, as a systemd service | `10.21.12.62:80`, `10.21.12.62:443` |
| Management | Portainer CE | Docker, CLI-deployed stack | `127.0.0.1:9000` only |
| TLS | Internal CA certificate per FQDN | `/etc/nginx/certs/` | n/a |
| Application | `app` container (FastAPI + uvicorn) | Docker Compose | `127.0.0.1:8001` only |
| Database | `db` container (Postgres 16) | Docker Compose | container network only, no published port |
| Storage | `pgdata` named volume | Docker | n/a |
| Storage | `portainer_data` named volume | Docker | n/a |

Two properties do the security work here:

1. **The app publishes on loopback only.** `docker-compose.yml` binds
   `127.0.0.1:8001:8000`. The app is not reachable from the network at all;
   nginx is the only route in. A plain `8001:8000` would have published it on
   `0.0.0.0` and exposed it over unencrypted HTTP on the lab network, bypassing
   TLS, the security headers and the redirect.
2. **Postgres publishes nothing.** It is reachable only by the app container
   over the compose network.
3. **Portainer publishes on loopback only too.** Its own HTTPS listener on 9443
   is deliberately not published: nginx terminates TLS, so there is one
   certificate story and no TLS inside TLS.

### 2.1 Port registry

Each app takes one loopback port. **Register it here before using it.**

| Port | Component | Status |
|---|---|---|
| 8001 | Skills Evaluation & Enablement | this deployment |
| 8002 | dq-studio | reserved, not yet deployed |
| 8003+ | unallocated | - |
| 9000 | Portainer CE UI (HTTP, behind nginx) | management plane |

Two Portainer ports are intentionally **not** published: `9443` (its own HTTPS
listener, unnecessary because nginx terminates TLS) and `8000` (the Edge agent
tunnel, not used in a single-host deployment). Leaving them unpublished keeps the
admin plane reachable only through nginx.

---

## 3. Network and naming

### 3.1 What is being requested

**ACTION (DNS team):** one A record per application, all pointing at the same
address.

| Hostname | Type | Value |
|---|---|---|
| `skills-eval.<POCLAB zone>` | A | 10.21.12.62 |
| `portainer.<POCLAB zone>` | A | 10.21.12.62 |
| `dq-studio.<POCLAB zone>` | A | 10.21.12.62 |

**ACTION (you):** confirm the real POCLAB DNS zone. Every config file in
`deploy/nginx/` currently uses the placeholder **`skills-eval.poclab.local`**,
which is a guess. It appears in `server_name`, both certificate paths and the log
paths, and must be replaced before use.

**ACTION (firewall/network team):** allow inbound TCP 443 and 80 to 10.21.12.62
from the user population. Nothing else needs opening. Port 8001 must **not** be
opened; the loopback binding already prevents external access, and an explicit
deny is a useful second line.

### 3.2 Why one IP and not one IP per app

The original ask was an IP *and* a domain per app. On a single host with a single
NIC, nginx distinguishes applications by the `Host` header (and by SNI during the
TLS handshake), so each app gets its own hostname and its own certificate while
sharing 10.21.12.62. This is standard virtual hosting and is what the confirmed
decision selected.

Per-app IPs remain available if network or security policy later requires
addressing separation: request additional addresses, add them as secondary
addresses on the interface, and change each vhost's `listen` to
`listen 10.21.12.63:443 ssl;`. It is a small change to the same config files.

Worth being clear about what that would and would not buy. It **would** let
firewall rules target an application by destination IP, and would serve clients
too old to send SNI. It would **not** provide isolation: it is still one nginx
process, one kernel, one host, one Docker daemon. If genuine isolation is the
goal, separate hosts or per-app VMs are the answer, not extra IPs.

---

## 4. Prerequisites on POCDAPP314

Host preparation has its own runbook: **`deploy/HOST-PREP-POCDAPP314.md`**. It
installs and configures Docker, nginx, SELinux, firewalld and Portainer for
RHEL 10.2, and ends with a 12-line checklist. Complete that first; this document
assumes every check in it passes.

Access is via PuTTY (SSH); RDP is also available but not needed for this.

The items below are the ones that most often block a deployment. All are covered
in the host-prep runbook.

**RHEL 10 note:** Red Hat ships Podman, not Docker. Docker Engine comes from
Docker's own repository, and whether an `el10` build exists must be verified
before starting - see section 1 of the host-prep runbook. Everything here assumes
Docker Engine plus the Compose plugin.

- Docker Engine and the Compose v2 plugin installed, `docker` usable by your
  account, and the daemon enabled at boot (`systemctl is-enabled docker`).
- nginx installed and enabled at boot.
- nginx version. `deploy/nginx/skills-eval.conf` uses the modern `http2 on;`
  directive, which needs **nginx >= 1.25.1**. On anything older the config will
  fail to load; the fix is in a comment at that line (use
  `listen 443 ssl http2;` and delete the `http2 on;` line).
- Outbound access to pull `python:3.12-slim` and `postgres:16-alpine`, or a
  mirror. **If the lab has no egress, this is a blocker** and the images must be
  side-loaded with `docker save` / `docker load`.
- SELinux is enforcing on RHEL. nginx cannot proxy to a loopback port until
  `setsebool -P httpd_can_network_connect 1` is set; without it every request
  returns 502. This is the most commonly missed step on this platform.
- firewalld allows only 80 and 443 inbound. 8001 and 9000 must stay closed.
- Whether **Portainer is already installed** on this host. If it is, skip Step 1
  and reuse it; do not stand up a second instance, because two Portainers sharing
  one Docker socket will both claim the same containers and stacks.
- Whether the host can reach the **git remote**. Git-backed stacks require
  Portainer itself to clone the repository, including credentials for a private
  remote. If it cannot, use the CLI fallback in Step 3b.

---

## 5. Deployment steps

Order matters: Portainer first, because it deploys everything after it, then the
application stack, then nginx and the certificates.

### Step 1 - install Portainer (once per host)

Portainer cannot deploy itself, so this is the one stack deployed from the shell.
Skip this step entirely if Portainer is already running on the host.

    cd /opt
    sudo mkdir -p syniti && cd syniti
    git clone <repo-url> syniti-consultant-eval
    cd syniti-consultant-eval/deploy/portainer
    docker compose up -d
    docker compose ps

Then **immediately** open the UI and create the admin account. Portainer locks
initial setup if no admin is created within a few minutes of first start, and
recovering means restarting the container. Until nginx is configured (Step 5),
reach it over an SSH local forward from your workstation rather than opening a
port:

    # in PuTTY: Connection > SSH > Tunnels, source 9000, destination 127.0.0.1:9000
    # then browse to http://127.0.0.1:9000

Treat that admin password as equivalent to root on this host, because it is.

Note this clone of the repository is only needed to bootstrap Portainer and to
hold the nginx files for Step 5. The application stack itself is deployed from
git by Portainer, not from this directory.

### Step 2 - register the stack in Portainer

In Portainer: **Stacks > Add stack > Repository**.

| Field | Value |
|---|---|
| Name | `skills-eval` |
| Repository URL | the repo remote |
| Reference | `refs/heads/main` |
| Compose path | `docker-compose.yml` |
| Authentication | required if the remote is private |

Add these as **environment variables** in the stack definition. On this host they
replace the `.env` file entirely; `.env.example` documents the same names.

| Variable | Value |
|---|---|
| `POSTGRES_PASSWORD` | generated, unique to this environment |
| `ADMIN_PASSWORD` | generated, unique to this environment |
| `APP_PORT` | `8001` |
| `APP_BIND` | `127.0.0.1` |
| `COOKIE_SECURE` | `true` |

`COOKIE_SECURE=true` is required here: nginx terminates TLS, so the session
cookie must be marked `Secure`. It is the exact string `true`, case-sensitive.

Generate the two passwords with a password manager or `openssl rand -base64 24`.
Do not reuse a password from another environment, and do not paste them into
chat, tickets or this file. Once entered they live in Portainer's own database on
the `portainer_data` volume, which is one more reason that volume matters.

`docker-compose.yml` declares both passwords with no default, so a missing one
fails the stack deployment with a readable error rather than starting something
half-configured.

### Step 3 - deploy and verify the stack

Deploy the stack. Portainer clones the repository, builds the image (the
Dockerfile rebuilds both apps from `data/*.json` as part of the build) and starts
`db` then `app`.

Expect `db` healthy, then `app` healthy. The app applies `db/schema.sql` and
creates the first lead account on first boot. Check the `app` container logs in
Portainer for `Created bootstrap admin account.`

Then confirm from a shell, because this is the check that proves the security
boundary and Portainer will not tell you:

    curl -fsS http://127.0.0.1:8001/api/health      # must return {"status":"ok"}
    curl -m 3  http://10.21.12.62:8001/api/health   # MUST fail to connect

The second command failing is the point. If it succeeds, the app is exposed on
the lab network over plain HTTP and `APP_BIND` is wrong.

#### Step 3b - CLI fallback

If Portainer cannot reach the git remote, deploy the stack from the shell
instead. The result is identical; only the mechanism differs.

    cd /opt/syniti/syniti-consultant-eval
    cp .env.example .env && chmod 600 .env && vi .env    # same variables as above
    docker compose up -d --build

Portainer will still show, monitor and manage the stack, but as an external one:
it cannot redeploy from git a stack it did not create that way.

### Step 4 - certificates

**ACTION (PKI/CA team):** request a server certificate for the application
hostname.

    openssl req -new -newkey rsa:2048 -nodes \
      -keyout /tmp/skills-eval.key \
      -out    /tmp/skills-eval.csr \
      -subj "/CN=skills-eval.<POCLAB zone>"

Submit the CSR, receive the certificate, then install the certificate plus its
issuing chain as one file:

    sudo install -d -m 750 /etc/nginx/certs
    sudo install -m 644 skills-eval.crt /etc/nginx/certs/skills-eval.<zone>.crt
    sudo install -m 600 /tmp/skills-eval.key /etc/nginx/certs/skills-eval.<zone>.key
    shred -u /tmp/skills-eval.key

The `.crt` must contain the server certificate **followed by the intermediate
chain**. A missing chain is the most common cause of "works in Chrome on my
machine, fails elsewhere".

Also create the throwaway self-signed cert for the catch-all default server -
the command is in the header of `deploy/nginx/00-default.conf`.

### Step 5 - install the nginx configuration

    sudo install -d -m 755 /etc/nginx/snippets
    sudo install -m 644 deploy/nginx/snippets/*.conf /etc/nginx/snippets/
    sudo install -m 644 deploy/nginx/00-default.conf  /etc/nginx/conf.d/
    sudo install -m 644 deploy/nginx/skills-eval.conf /etc/nginx/conf.d/
    sudo install -m 644 deploy/nginx/portainer.conf   /etc/nginx/conf.d/

`00-default.conf` also defines the `$connection_upgrade` map that the Portainer
vhost needs for WebSockets, so install it even if you skip the catch-all servers.

Before enabling the Portainer vhost, set the IP allow-list in it. The directives
are present but commented, with an ACTION note explaining why they matter for an
admin plane.

Replace the placeholder hostname in the installed file, then validate **before**
reloading:

    sudo sed -i 's/skills-eval\.poclab\.local/skills-eval.<real zone>/g' \
      /etc/nginx/conf.d/skills-eval.conf
    sudo nginx -t
    sudo systemctl reload nginx

`nginx -t` failing is normal on the first pass - usually a wrong cert path or the
`http2 on;` version issue from §4. Never reload without a clean `-t`; a reload
with a broken config leaves the previous config running but a restart would take
every app on the host down.

### Step 6 - verify end to end

    curl -fsS https://skills-eval.<zone>/api/health
    curl -sI  http://skills-eval.<zone>/            # expect 301 to https
    curl -sI  https://skills-eval.<zone>/           # expect 200 + HSTS header
    curl -skI https://10.21.12.62/                  # expect 404 from default server

Then in a browser on a managed machine: no certificate warning, the eval app at
`/`, the team summary at `/team`, the server-only buttons visible, sign-in works,
and save-then-reload-then-open-from-server returns the same evaluation.

### Step 7 - seeding for the demo (optional)

    docker compose exec app python -m server.seed

This loads the 34 synthetic evaluations. It is safe for a POC and the data is
fictional. It never runs automatically.

---

## 6. Operations

**Autostart.** `restart: unless-stopped` plus an enabled Docker daemon brings the
stack back after a reboot. Verify with an actual reboot rather than assuming it -
`systemctl is-enabled docker` and then `docker compose ps` after restart.

**Logs.**

| What | Where |
|---|---|
| nginx access/error, per app | `/var/log/nginx/skills-eval.*.log` |
| Application | `docker compose logs app` |
| Postgres | `docker compose logs db` |

nginx logs rotate via the distribution's existing logrotate config. Container
logs do not rotate by default; set `max-size`/`max-file` in
`/etc/docker/daemon.json` or the stack will eventually fill the disk. **Open
action.**

**Backup.** The `pgdata` volume is the only stateful thing on the host.

    docker compose exec -T db pg_dump -U syniti syniti_eval | gzip > eval-$(date +%F).sql.gz

No schedule exists yet. **Open action** - agree a retention period, and note that
once real evaluations are loaded these dumps contain personal data and inherit
the same handling requirements as the database.

The `portainer_data` volume is also stateful and worth backing up: it holds the
stack definitions, the entered environment variables including both passwords, and
the Portainer user accounts. Losing it means re-registering every stack.

**Upgrade.** For a git-backed stack, in Portainer: **Stacks > skills-eval >
Pull and redeploy**. Portainer re-clones at the configured reference, rebuilds and
restarts. Then verify:

    curl -fsS https://skills-eval.<zone>/api/health

Rollback is the same action pointed at a previous tag or commit: change the stack
reference and redeploy. Because writes are append-only, rolling the application
back does not lose stored evaluations.

nginx is untouched by an application upgrade, and upgrading Portainer itself is a
separate CLI action against `deploy/portainer/docker-compose.yml` with the image
tag bumped on purpose.

If the stack was created by the Step 3b fallback, upgrade it the same way it was
created (`git pull && docker compose up -d --build`); Portainer cannot redeploy
from git a stack it did not create that way.

**Monitoring.** Point whatever the lab uses at
`https://skills-eval.<zone>/api/health`. It is unauthenticated by design and
excluded from the access log.

---

## 7. Onboarding the next application (dq-studio)

The whole point of the shared-ingress pattern. Nothing below touches this app.

1. Allocate the next loopback port in the §2.1 registry (8002).
2. **ACTION (DNS):** A record `dq-studio.<zone>` to 10.21.12.62.
3. **ACTION (CA):** certificate for that hostname.
4. Copy `skills-eval.conf` to `dq-studio.conf` and change the four marked items:
   `server_name`, both cert paths, the upstream name and port, and the log paths.
5. Register a second git-backed stack in Portainer for that app, publishing on
   `127.0.0.1:8002`, with its own environment variables.
6. `sudo nginx -t && sudo systemctl reload nginx`.

Only step 4 and step 6 need shell access. Everything about the application itself
is done in Portainer, which is the main practical benefit of adding it: the person
deploying the next app does not need to be the person with sudo.

A reload is graceful: existing connections to this app are not dropped.

---

## 8. Risks and open items

| # | Item | Impact | Owner |
|---|---|---|---|
| 1 | Nothing here has been executed against POCDAPP314 | Unknown-unknowns on first run | you |
| 2 | Real DNS zone unconfirmed; configs carry a placeholder | nginx serves the wrong name or fails `-t` | you |
| 3 | nginx version on the box unknown (`http2 on;` needs >= 1.25.1) | Config fails to load | you |
| 4 | Lab egress for image pulls unconfirmed | Cannot build; needs side-loaded images | platform |
| 5 | SELinux may block nginx proxying to loopback | 502 on every request | platform |
| 6 | CSP allows `'unsafe-inline'` | Weaker XSS defence than ideal | accepted |
| 7 | Container log rotation not configured | Disk fills over time | you |
| 8 | No backup schedule | Data loss on volume loss | you |
| 9 | No login throttling or account lockout | Brute-force exposure | decision needed |
| 10 | Single host, no redundancy | Total outage on host failure | accepted for POC |
| 11 | Portainer holds the Docker socket: root-equivalent on the host | Full host compromise if the UI is reached | mitigations in §9 |
| 12 | Admin plane and app plane share one nginx | An nginx outage removes the management path too | accepted, see §9 |
| 13 | Stack secrets live in `portainer_data` | Volume loss or theft exposes both passwords | you |
| 14 | Portainer image tag must be bumped deliberately | Pinned at 2.21.4; no automatic security patching | you |

### On the CSP trade-off (#6)

Both apps are single-file HTML with one large inline `<script>`, inline `<style>`
and a base64 logo. A strict `script-src 'self'` breaks them completely. The
shipped policy therefore allows `'unsafe-inline'`. Removing it means either
per-deploy script hashes or extracting the script to a served `.js` file - and
the latter ends the portable-single-file property that the whole design protects.
This is a knowing trade-off for an internal POC, and it should be revisited
before this pattern is used for anything internet-facing.

---

## 9. Portainer: the admin plane

Portainer is the most privileged thing on this host and deserves its own section.

**Why it is privileged.** It mounts `/var/run/docker.sock`. The socket cannot be
mounted read-only, because creating and managing containers is the entire
function. Anyone who authenticates to the UI can start a container that mounts the
host filesystem, which is a root shell in two clicks. The Portainer admin
password is therefore equivalent to root on POCDAPP314.

**Mitigations applied in this design.**

- The UI is published on `127.0.0.1:9000` only. It is not reachable from the
  network except through nginx.
- Portainer's own 9443 listener and the 8000 Edge tunnel are not published.
- The vhost carries commented `allow`/`deny` directives. **ACTION:** set the real
  administrator subnet before enabling that vhost. This is the single highest-value
  control here and it costs one line.
- The image is pinned rather than tracking `latest`, so an unreviewed image cannot
  arrive during an unrelated redeploy.
- Baseline security headers only. The application CSP is deliberately not applied
  to Portainer, because a policy written for our single-file apps breaks a bundled
  Angular front end.

**Accepted consequence.** Putting Portainer behind the same nginx as the
applications means a broken nginx config removes the management path at the same
moment you need it. The mitigation is process, not architecture: never
`systemctl reload nginx` without a clean `nginx -t`, and keep SSH access working
as the out-of-band path. An SSH local forward to `127.0.0.1:9000` reaches
Portainer with nginx entirely out of the picture, which is also how Step 1 works
before nginx exists.

**Not addressed.** Portainer has its own users, roles and teams. This POC assumes
a small number of administrators sharing appropriate access. If Portainer becomes
the control plane for several applications with different owners, its own access
model needs designing, and that is out of scope here.

---

### Before any real evaluation data

Two gates, unchanged by this deployment work and both recorded in `CLAUDE.md`:

1. **TLS must be in place with `COOKIE_SECURE=true`.** This deployment satisfies
   that, and step 6 verifies it.
2. **Data privacy review.** The database becomes a shared system of record for
   named-employee performance data on EU staff, including performance
   classification and promotion recommendation. The **Data Privacy Officer should
   review the design before real evaluations are loaded.** Running the POC on
   `test-data/` is fine; that data is synthetic.
