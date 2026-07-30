---
title: Phase 2 target architecture - two-tier, hardened
type: spec
updated: 2026-07-28
tags: [dq-coe, evaluation, deployment, architecture, hardening]
---

# Phase 2: two-tier target architecture

Following IT guidance (2026-07-28) to move the reverse proxy onto its own host and
to rebuild on hardened, enterprise-grade container images.

**Phase 1 is not superseded.** The single-host deployment on POCDAPP314 is
commissioned, working, and stays as the demonstration environment on synthetic
data. Phase 2 is what makes the application usable by Capgemini staff. Nothing
built in phase 1 is discarded: the application, the stack, the git-backed
deployment and the vhost configuration all carry forward.

---

## 1. What changes

| | Phase 1 (now) | Phase 2 (target) |
|---|---|---|
| Reverse proxy | nginx on POCDAPP314 | nginx on its own host |
| App network exposure | `127.0.0.1:8001` only | Host LAN address, firewall-restricted to the proxy |
| Boundary control | Loopback binding | Firewall source restriction |
| TLS keys | On the app host | On the proxy host only |
| Base images | `python:3.12-slim`, `postgres:16-alpine` | Approved hardened base, pending IT confirmation |
| Runtime hardening | Non-root | Non-root, read-only rootfs, no capabilities, resource limits |
| Image references | Tags | Pinned digests |
| Audience | The host itself | Capgemini staff on the corporate network |

Unchanged: the application code, the data model, authentication, the append-only
storage model, the offline single-file distribution, and the shared-ingress
one-vhost-per-app pattern.

---

## 2. The control that has to be replaced

This is the most important section in this document.

Phase 1's primary network control is that **the application is not reachable from
anywhere except its own host**. `docker-compose.yml` publishes
`127.0.0.1:8001:8000`, so nginx being on the same machine is what makes it the only
route in. `CLAUDE.md` records this as an invariant.

Moving the proxy to a separate host **removes that control by definition**: the
proxy must reach the application over the network. The replacement is a firewall
rule that permits only the proxy host.

    # On POCDAPP314. Note --add-rich-rule, NOT --add-port: --add-port would
    # open 8001 to the whole network, which is exactly what we are avoiding.
    sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" \
      source address="PROXY_IP/32" port port="8001" protocol="tcp" accept'
    sudo firewall-cmd --reload
    sudo firewall-cmd --list-rich-rules

And in the stack environment, the bind address changes:

    APP_BIND=10.21.12.62      # was 127.0.0.1

**Verification changes with it.** Phase 1's check was "the app must NOT answer on
10.21.12.62:8001". In phase 2 it must answer from the proxy host and must **not**
answer from anywhere else. `deploy/verify-deployment.sh` asserts the phase 1
behaviour and will report a FAIL once this changes; that check needs rewriting at
the same time, not afterwards.

### The second-order consequence, easy to miss

`Dockerfile` currently runs uvicorn with `--forwarded-allow-ips=*`, and the comment
there states it is safe **only** because the port is loopback-bound. Once the
application is network-reachable, `*` means any client that can reach it may spoof
`X-Forwarded-For` and `X-Forwarded-Proto`, which corrupts the client addresses the
application records and trusts.

    # Phase 2
    --forwarded-allow-ips=PROXY_IP

This must change in the same release as the bind address. If only one of the two
changes lands, the deployment is worse than phase 1.

---

## 3. Encryption between proxy and application

With the proxy on another host, that hop is **plaintext HTTP across the network**
unless something is done. Four options, for IT to choose:

| Option | What it means | Assessment |
|---|---|---|
| **A. Accept plaintext** | Rely on the network segment being trusted | Simplest. Defensible only if IT considers the segment trusted for personal data |
| **B. TLS at the application** | uvicorn serves HTTPS; proxy uses `proxy_pass https://` and verifies | Pragmatic middle ground. Needs a certificate for the app host too |
| **C. Mutual TLS** | As B, plus the proxy presents a client certificate the app verifies | Strongest. Also authenticates the proxy, so the firewall rule stops being the only thing standing between the app and the network |
| **D. Network-layer encryption** | IPsec or a WireGuard tunnel between the hosts | IT's domain, transparent to both applications |

**Recommendation: B as a minimum, C if IT is willing.** The data is
named-employee performance information; encryption in transit end to end is easier
to defend than a trusted-segment argument, and the incremental work is small.

---

## 4. Hardened images

### Base images

Given the RHEL estate, **Red Hat UBI** is the natural direction: it carries a
vendor CVE feed and a support statement, which is usually what "enterprise grade"
means when IT says it.

- Application: `registry.access.redhat.com/ubi9/python-312` in place of
  `python:3.12-slim`. Straightforward: our image installs pip requirements and
  copies source; there is no OS-level dependency to port.
- Database: **not straightforward, and not a tag change.** Red Hat's
  `rhel9/postgresql-16` uses different environment variable names
  (`POSTGRESQL_USER`, `POSTGRESQL_PASSWORD`, `POSTGRESQL_DATABASE`) and a
  different data directory from `postgres:16-alpine`. **An existing `pgdata`
  volume is not compatible.** Switching means a `pg_dump` and restore, plus
  changes to `docker-compose.yml` and to the environment variables held in the
  Portainer stack.

Because of that asymmetry, do the application image first and treat the database
image as a separate, planned migration with a dump taken beforehand.

**Pending from IT:** confirmation of the approved base images and whether an
internal registry mirror should be used instead of `registry.access.redhat.com`.

### Runtime hardening

Needs no IT input and can land now. Per service in `docker-compose.yml`:

    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    read_only: true
    tmpfs:
      - /tmp
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "1.0"

Caveats found by reading our own images rather than assuming:

- `read_only: true` on the **app** needs `/tmp` as tmpfs. The application writes
  nothing else at runtime; both HTML apps are generated at build time.
- `read_only: true` on **Postgres** additionally needs `/var/run/postgresql` as
  tmpfs, and the data directory must stay a writable volume.
- `cap_drop: ALL` should be safe for both: neither binds a privileged port inside
  the container, and both already run as non-root.
- Resource limits under Compose v2 without Swarm apply through
  `deploy.resources.limits`; confirm they take effect rather than assuming.

### Pinning and scanning

Replace tags with digests so a rebuild cannot silently pull different content:

    image: registry.access.redhat.com/ubi9/python-312@sha256:<digest>

**Pending from IT:** which scanner, and what severity threshold gates a release.
Once named, it becomes a build step. Until then, pinning is the useful half and
costs nothing.

---

## 5. Either ownership model

The proxy host owner is undecided (Paul's call), so the design is stated as a
contract rather than an implementation.

**If IT owns the proxy:** hand them the backend contract in
`deploy/IT-ENGAGEMENT-BRIEF.md` section 5. Our `deploy/nginx/*.conf` files become
a reference implementation they may adopt or replace. We lose the ability to change
routing without a request, which is the trade for not owning an exposed host.

**If we own the proxy:** our vhost files transfer nearly unchanged. The only edit
is the upstream target:

    upstream skills_eval {
        server 10.21.12.62:8001 fail_timeout=10s;   # was 127.0.0.1:8001
        keepalive 16;
    }

Everything else - TLS settings, security headers, the CSP split, the catch-all
default server, the WebSocket snippet for the management UI - applies as written.
We would then own hardening and patching of an internet-adjacent host, which is
plausibly what IT is trying to avoid.

---

## 6. Migration sequence

Ordered so that nothing breaks midway and each step is verifiable.

1. **Runtime hardening only**, on the existing single-host deployment. No IT
   dependency. Verify the stack still starts and the evidence script still passes.
2. **Application image onto the approved base**, once IT confirms it. Rebuild,
   redeploy, re-run the evidence script. Database image untouched.
3. **Stand up the proxy host** (IT or us) with the vhosts, certificates and DNS.
   Do not change the app host yet.
4. **Flip the boundary in one release**: `APP_BIND` to the LAN address,
   `--forwarded-allow-ips` to the proxy IP, and the firewall rich rule, together.
   Then update `verify-deployment.sh` so its assertions match the new topology.
5. **Set `COOKIE_SECURE=true`** once TLS is genuinely in front.
6. **Database image migration**, separately, with a dump taken first.

Steps 1 and 2 are safe to do now. Step 4 is the only one with a window where a
mistake exposes the application, which is why its three changes ship together.

---

## 7. Open decisions

| # | Decision | Owner |
|---|---|---|
| 1 | Is POCLAB permitted to hold real employee personal data? | IT and the Data Privacy Officer |
| 2 | Who provides and owns the proxy host? | Paul |
| 3 | Approved base images and registry | IT |
| 4 | Scanner and severity gate | IT |
| 5 | Encryption between proxy and app: options A to D in section 3 | IT |
| 6 | Administrator subnet for the management UI allow-list | IT or network |
| 7 | Is Portainer acceptable? It holds the Docker socket and is root-equivalent on the host | IT security |

Decision 7 is worth raising explicitly rather than waiting to be asked. Portainer
is how we deploy without shell access, but a container-management UI holding the
Docker socket may not pass an enterprise review. If IT objects, the fallback is
CLI deployment (already documented as section 3b of the phase 1 runbook) and we
would revisit that decision properly rather than work around it.

---

## 8. What this does not address

- **Redundancy.** Still one application host and, in phase 2, one proxy host.
  Neither is highly available. Acceptable for an internal tool with a small user
  base; state it rather than imply otherwise.
- **The content security policy** still permits `'unsafe-inline'`, because both
  apps are single-file HTML with one large inline script. Acceptable internally;
  it should be revisited before anything internet-facing.
- **Login throttling** is still absent. With a wider audience able to reach the
  login page, this is now worth adding regardless of hosting model.
- **Authorisation is still a shared pool.** Any authenticated user reads every
  evaluation. That was agreed on the basis that accounts stay few and every
  account holder is entitled to see all evaluations. If the user list grows, that
  decision needs revisiting before it does.
