---
title: Exposure readiness - what must be true before this leaves POCLAB
type: register
updated: 2026-07-28
tags: [dq-coe, evaluation, deployment, readiness, governance]
---

# Exposure readiness register

The single place that answers "are we allowed to do this yet, and what is left".

Three things, in this order: a **testable definition of done**, the **constraints
we do not yet know** (our limits), and the **steps** grouped by what blocks them.

Companion documents, referenced rather than repeated:

| Document | Covers |
|---|---|
| `EVIDENCE-POCDAPP314.md` | What is built and proved today |
| `PHASE2-TARGET-ARCHITECTURE.md` | The two-tier target design |
| `IT-ENGAGEMENT-BRIEF.md` | The asks of IT, sendable as-is |
| `DEPLOY-POCDAPP314.md` | Phase 1 deployment runbook |
| `verify-deployment.sh` | Executable evidence |

---

## 1. Definition of done

"Exposed outside POCLAB" is done when **all ten** of these pass, each tested from
a Capgemini-managed laptop that is **not** inside POCLAB and **not** using an SSH
tunnel or RDP session.

| # | Criterion | How it is checked |
|---|---|---|
| E1 | The hostname resolves | `nslookup skills-eval.<zone>` returns the ingress address |
| E2 | HTTPS loads with no certificate warning | Browse to `https://skills-eval.<zone>/`, no interstitial |
| E3 | Plain HTTP redirects, bare IP does not serve | `curl -sI http://...` returns 301; `curl -skI https://<ip>/` returns 404 |
| E4 | A named user, not the bootstrap admin, completes a full cycle | Sign in, save an evaluation, reload the page, open it from the server |
| E5 | The team summary loads from the server | `/team` "Load from server" returns the stored set |
| E6 | Only 443 is reachable | `curl` to the app port and the management port both fail to connect |
| E7 | The management UI is not reachable from a normal corporate address | Refused from a standard laptop, allowed from the admin subnet |
| E8 | The session cookie is marked `Secure` | Browser devtools, and `COOKIE_SECURE=true` in the stack |
| E9 | Automated evidence passes on the new topology | `verify-deployment.sh` returns 0 with assertions updated for two-tier |
| E10 | It survives a reboot unattended | Reboot the host, re-run E1 to E6 without intervention |

**E4 is the one that fails today for a non-obvious reason:** there is no way to
create a second account. See step A4.

**E9 requires editing the script, not just running it.** It currently asserts the
application does *not* answer on the LAN address, which is correct for phase 1 and
wrong for phase 2. Changing the topology without changing the assertions produces
a false FAIL and, worse, trains people to ignore it.

---

## 2. Our limits: what we do not yet know

This is the section the exposure actually waits on. Nothing here is a task we can
complete alone; each is a constraint to discover.

**Two of these can invalidate the whole approach.** L1 and L2 are first for that
reason: if POCLAB may not hold the data, or may not be reached from the corporate
network by policy, then the answer is not "configure more" but "host this
somewhere else". Ask both before spending effort on the rest.

| # | Constraint we do not know | Owner | If the answer is unfavourable |
|---|---|---|---|
| **L1** | **Is POCLAB permitted to hold real employee personal data?** | IT + Data Privacy Officer | The application moves to a managed environment. All hosting work here becomes a rehearsal |
| **L2** | **Is POCLAB reachable from the corporate network, or jump-host-only by policy?** | Network | Exposure as described is impossible; the app must move or stay tunnel-only |
| L3 | Is a change approval, CAB or security sign-off required before an internal service is exposed? | IT | Adds lead time we have not planned for. Ask early |
| L4 | Is a security assessment or penetration test required first? | IT security | Adds lead time, and may raise findings that need code changes |
| L5 | Must the application be registered in an inventory or CMDB, with a named owner? | IT | An administrative step that can block go-live |
| L6 | Who provides and owns the reverse proxy host? | Paul | Changes who holds certificates and who deploys routing changes |
| L7 | Which base images and registry are approved? | IT | Rebuild work. Do not guess; rebuilding twice is waste |
| L8 | Which scanner, and what severity gates a release? | IT | Defines the build pipeline and possibly blocks on existing CVEs |
| L9 | Is encryption required between proxy and application? | IT | Adds a certificate for the app host, and possibly mutual TLS |
| L10 | Is Portainer acceptable, given it holds the Docker socket? | IT security | Deployment mechanism changes; DEC-10 needs revisiting properly |
| L11 | Which DNS zone do corporate machines resolve? | DNS | Determines the hostname. Every config currently carries a placeholder |
| L12 | Which CA issues the certificate? | PKI | Determines whether managed laptops trust it silently |
| L13 | What is the administrator subnet range? | Network | Needed for the management UI allow-list |
| L14 | Who owns OS patching on each host? | IT | An ownership gap is itself a finding |
| L15 | Are there central log-shipping and backup services we should use? | IT | Avoids building what already exists |
| L16 | What retention applies to evaluation records and to database backups? | DPO + IT | Drives a retention mechanism we have not built |

### Status of each

Fill this in as answers arrive. An unanswered row is a blocked step, not a
detail.

    L1  [ ]   L5  [ ]   L9  [ ]   L13 [ ]
    L2  [ ]   L6  [ ]   L10 [ ]   L14 [ ]
    L3  [ ]   L7  [ ]   L11 [ ]   L15 [ ]
    L4  [ ]   L8  [ ]   L12 [ ]   L16 [ ]

---

## 3. Two design facts that collide with wider exposure

Both are consequences of decisions taken deliberately for a small POC. Neither is
a bug. Both need a decision before real data, and both are easier to raise now
than to be asked about during a review.

### 3.1 There is no way to delete a record

Decision 8 made writes **append-only with no delete endpoint**, so a mistaken save
cannot destroy a completed review. That is a good property for data integrity.

It also means that today **an erasure or rectification request could only be
satisfied by direct database access**. Under data protection law, individuals have
rights over their personal data, and a system of record holding performance data
about named employees will eventually receive such a request.

This is a factual description of the software, not a legal opinion. The **Data
Privacy Officer should decide** what is required: a soft-delete with audit, a
supersede-and-redact mechanism, a documented manual procedure, or acceptance that
the retention period handles it. Whatever is chosen may be development work, so it
belongs in the plan rather than discovered later.

### 3.2 There is no record of who read what

`created_by` is stamped on every write, so authorship is auditable. **Reads are
not logged**, and because the visibility model is a shared pool, any authenticated
user can read every evaluation. With few accounts that was an accepted trade. As
the account list grows, "who looked at whose performance review" becomes a question
the system cannot answer.

Adding read audit is small: one insert per fetch. Worth deciding alongside 3.1
rather than separately.

---

## 4. Steps

Grouped by what blocks them, not by chronology. Track A can start immediately.

### Track A - no external dependency, start now

| # | Step | Done when |
|---|---|---|
| A1 | Add runtime hardening to the stack: `no-new-privileges`, `cap_drop: ALL`, read-only rootfs with tmpfs, resource limits | Stack starts and `verify-deployment.sh` still returns 0 |
| A2 | Pin both images by digest instead of tag | `docker-compose.yml` contains no floating tags |
| A3 | Add login throttling and account lockout | A scripted brute-force attempt is refused, and a test proves it |
| A4 | Build the user-account CLI: add, list, disable | A second named account can sign in, and `created_by` shows it |
| A5 | Run the automated test suite against a real Postgres | 27 tests pass, not skip |
| A6 | Rehearse backup and restore of `pgdata` | A dump restores into an empty volume and the app serves the data |
| A7 | Update `verify-deployment.sh` so its assertions are topology-aware | Script passes on phase 1 and is ready for phase 2 |

A3 and A4 are the two that block criterion E4. A5 matters because 27 tests have
still never executed; skipping is not passing.

### Track B - discovery, needs a conversation not a change

| # | Step | Done when |
|---|---|---|
| B1 | Send `IT-ENGAGEMENT-BRIEF.md` to Paul | Meeting held, L3 to L15 answered or scheduled |
| B2 | Ask L1 and L2 explicitly and first | A written answer on data permissibility and network reachability |
| B3 | Take 3.1 and 3.2 to the Data Privacy Officer | A decision on erasure handling, read audit and retention (L16) |
| B4 | Confirm whether change approval or a security assessment is required (L3, L4) | Either a "not required" or a submitted request with a date |

### Track C - blocked on Track B answers

| # | Step | Blocked by |
|---|---|---|
| C1 | Rebuild the application image on the approved base | L7 |
| C2 | Add the image scanning step at the required threshold | L8 |
| C3 | Plan the database image migration, with a dump first, as a separate change | L7 |
| C4 | Stand up the proxy host with vhosts and certificates | L6, L11, L12 |
| C5 | Request DNS records and the firewall paths | L2, L11, L13 |
| C6 | Decide and implement proxy-to-app encryption | L9 |
| C7 | Resolve the deployment mechanism if Portainer is rejected | L10 |
| C8 | Implement whatever the DPO requires for erasure and retention | B3 |

### Track D - the exposure release itself

These three ship **together, in one change**. Shipping any subset leaves the
application in a worse state than phase 1.

| # | Step |
|---|---|
| D1 | `APP_BIND` from `127.0.0.1` to the host LAN address |
| D2 | `--forwarded-allow-ips` from `*` to the proxy address |
| D3 | firewalld **rich rule** scoped to the proxy address, not an open port |

Then, and only then:

| # | Step |
|---|---|
| D4 | Set `COOKIE_SECURE=true` |
| D5 | Apply the management UI IP allow-list |

### Track E - verification

| # | Step |
|---|---|
| E-all | Walk criteria E1 to E10 from an off-POCLAB laptop and record the output |
| E-eng | Re-run `verify-deployment.sh`, capture with `tee`, attach to the evidence document |

---

## 5. What we are deliberately not doing

Stated so nobody assumes otherwise, and so a reviewer can challenge the choice
rather than discover the gap.

- **No high availability.** One application host, one proxy host. Acceptable for
  an internal tool with a small user base; not a claim of resilience.
- **No internet exposure.** Corporate network and VPN only. Internet-facing would
  require revisiting the CSP `'unsafe-inline'` allowance, a WAF, and formal
  security sign-off.
- **No change to the authorisation model.** Any authenticated user still reads
  every evaluation. Agreed on the basis that accounts stay few and each holder is
  entitled to see all records. **Revisit before the user list grows**, not after.
- **No single sign-on.** Local accounts with argon2 hashes. Entra ID is the right
  destination if this becomes a durable service.
- **No removal of the offline distribution.** The portable single file keeps
  working, unchanged, with no network calls.

---

## 6. The shortest honest summary

Two questions decide whether any of this is worth doing: **L1** (may POCLAB hold
real employee data) and **L2** (is POCLAB reachable from the corporate network).
Ask both first, in writing.

Meanwhile, **Track A is seven steps that need nobody's permission** and make the
application materially more deployable regardless of which hosting answer comes
back. That is where the time goes while the answers arrive.
