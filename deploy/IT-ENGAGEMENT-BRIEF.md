---
title: IT engagement brief - Skills Evaluation application
type: brief
updated: 2026-07-28
tags: [dq-coe, evaluation, deployment, it, infrastructure]
---

# IT engagement brief: Skills Evaluation application

**For:** Paul, Capgemini IT
**From:** Jordi Carrasco, Syniti EMEA Data Quality CoE
**Subject:** exposing an internal web application to Capgemini staff, and the
infrastructure decisions we need from IT

---

## 1. Executive summary

We have built and commissioned an internal web application that supports the
Syniti EMEA Data Quality competency evaluation process. It currently runs on a
single POCLAB host, **POCDAPP314 (10.21.12.62)**, reachable only from that host
itself. It is working and verified.

To make it usable by Capgemini staff we need a network path, DNS, a certificate,
and a reverse-proxy tier. Following IT's guidance we plan to move the reverse
proxy onto **its own host**, and to rebuild our containers on an
**approved hardened base image**.

**What we are asking for:** eleven items in section 4, of which four are
decisions only IT can make. We are not asking IT to take on the application
itself; we own the application, its data model and its deployment.

**One question worth answering early**, because it may change everything below:
is POCLAB sanctioned to hold **real employee personal data**? The application
holds performance ratings, classifications and promotion recommendations for named
EU staff. If a POC lab environment is not permitted to hold that, we would rather
learn it now and plan a move to a managed environment than discover it after the
network work is done. We are running on synthetic test data today, which raises no
such question.

---

## 2. What exists today

| Layer | Detail |
|---|---|
| Application | Python FastAPI, containerised, serves two internal web pages plus a JSON API |
| Authentication | Username and password, argon2 hashes, server-side sessions, HttpOnly and SameSite cookies. Unauthenticated API calls are rejected |
| Database | PostgreSQL 16, containerised, publishes no network port |
| Orchestration | Docker Compose, deployed from a git repository through Portainer |
| Reverse proxy | nginx on the same host, configured but not yet serving |
| Host OS | RHEL 10.2, SELinux enforcing, firewalld with only 80 and 443 permitted |

Both containers run as non-root. Neither the application nor the database is
reachable from the network: the application is bound to `127.0.0.1` and the
database to the container network only. Access during commissioning was by SSH
local port forward, not by opening ports.

Evidence of commissioning, including the verification script and its results, is
in `deploy/EVIDENCE-POCDAPP314.md` in our repository. We can share it.

---

## 3. What we plan to change, per IT's guidance

1. **Move the reverse proxy to its own host.** We accept the reasoning: a shared
   ingress fronting several applications should not sit on an application host,
   and TLS private keys should not live on the application box.
2. **Rebuild on an approved hardened base image** and add runtime hardening
   (read-only root filesystem, all Linux capabilities dropped, no new privileges,
   resource limits, images pinned by digest rather than tag).
3. **Add container image scanning** to our build, gated at whatever severity
   threshold IT requires.

### A consequence we want to flag rather than discover later

Today the application is protected by being bound to loopback: nothing outside the
host can reach it. **Moving the proxy to a separate host removes that control**,
because the proxy must then reach the application over the network. Our
replacement is a firewall rule permitting **only the proxy host's address** to
reach the application port. We would like IT to confirm that is acceptable, or to
propose their preferred equivalent.

Related: with a proxy on a different host, the hop between proxy and application
is **plaintext HTTP across the network** unless we encrypt it. For
named-employee performance data IT may prefer encryption in transit end to end. We
can terminate TLS at the application as well; we would rather be told than assume.

---

## 4. What we need from IT

### Decisions only IT can make

| # | Decision | Why it blocks us |
|---|---|---|
| 1 | **Is POCLAB permitted to hold real employee personal data?** If not, what is the correct target environment? | Determines whether this work continues here or moves |
| 2 | **Who provides and owns the reverse-proxy host?** IT builds and owns it, or IT provides a VM and we own nginx on it | Changes who holds certificates and who deploys vhost changes |
| 3 | **Which base images and registry are approved?** Our assumption is Red Hat UBI, given the RHEL estate. Please confirm, including whether an internal registry mirror should be used | We will not guess; rebuilding twice is wasted effort |
| 4 | **Which scanner, and what severity gates a release?** Trivy, Grype, Prisma or other | Determines our build pipeline |

### Requests

| # | Request | Detail |
|---|---|---|
| 5 | Network path | Corporate network to the proxy host, TCP 443 inbound. **443 only** |
| 6 | Network path | Proxy host to POCDAPP314, TCP 8001 inbound, **source-restricted to the proxy host** |
| 7 | DNS | An A record per application, in a zone that corporate machines resolve. Initially `skills-eval.<zone>`; `dq-studio.<zone>` to follow |
| 8 | Certificate | One per hostname, from the corporate PKI so managed laptops trust the chain without warnings. Full chain including intermediates |
| 9 | Administrative access | A separate hostname for our container management UI, restricted by IP allow-list to the administrator subnet. Please provide that subnet range |
| 10 | Patching ownership | Confirm who owns OS patching on POCDAPP314 and on the proxy host |
| 11 | Platform services | Whether central log shipping and volume backup services exist that we should use rather than build |

### What we provide

- **The backend contract** for the proxy (section 5), so the vhosts can be built
  by whoever owns them.
- Working nginx vhost configuration, already written and reviewed, which IT can
  adopt, adapt or discard.
- The application, its deployment, its data model and its own authentication. We
  are not asking IT to operate the application.

---

## 5. Backend contract for the reverse proxy

Stated explicitly so it works whether IT owns the proxy or we do.

| Property | Value |
|---|---|
| Backend address | POCDAPP314, 10.21.12.62 |
| Backend port | TCP 8001, plain HTTP |
| Protocol to backend | HTTP/1.1 |
| Health check | `GET /api/health`, unauthenticated by design, expects `{"status":"ok"}` |
| Public hostname | `skills-eval.<zone>`, TLS terminated at the proxy |
| Port 80 | Redirect to HTTPS only, never serves |
| Required headers to backend | `Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`, `X-Forwarded-Host`, `X-Forwarded-Port` |
| WebSockets | **Not** required by the application |
| Max request body | 2 MB is sufficient |
| Timeouts | 5s connect, 60s read and send |
| Sticky sessions | Not required; sessions are held server-side in PostgreSQL |
| Paths | All paths to the same backend. `/` and `/team` are pages, `/api/*` is the API |

The management UI, if exposed, additionally **requires WebSocket upgrade** and a
much larger body limit, and should carry an IP allow-list. We recommend treating
it as a separate vhost with different rules, not as a path on the application
hostname.

---

## 6. What we will do regardless of the decisions above

- Keep the current single-host deployment working as the demonstration
  environment, on synthetic data.
- Add runtime hardening flags that need no IT input.
- Add the image scanning step, adjusting the gate once IT names the tool.
- Not put real evaluation data into the application until there is TLS in front,
  and until the data privacy review is complete.

---

## 7. Data protection note

The application will hold performance ratings, narrative feedback, performance
classifications and promotion recommendations for named employees, most of them EU
based. We are treating this as personal data requiring review by the **Data
Privacy Officer** before any real records are entered, and we would welcome IT's
view on the correct hosting environment for it. This brief does not constitute a
data protection assessment and is not intended as legal or regulatory advice.

---

*Prepared with AI assistance. Please review the technical details against your own
environment before acting on them, and confirm anything marked as an assumption.*
