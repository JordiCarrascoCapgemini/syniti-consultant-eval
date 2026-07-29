---
title: Commissioning evidence - POCDAPP314
type: evidence
updated: 2026-07-28
tags: [dq-coe, evaluation, deployment, evidence, poc]
---

# Commissioning evidence: Skills Evaluation on POCDAPP314

What was achieved, how it was proved, and what remains. Pair this with the output
of `deploy/verify-deployment.sh`, which produces the machine-readable evidence.

- **Host:** POCDAPP314, 10.21.12.62, POCLAB
- **OS:** Red Hat Enterprise Linux 10.2 (Coughlan)
- **Date commissioned:** 2026-07-28
- **Repository:** `github.com/JordiCarrascoCapgemini/syniti-consultant-eval`

---

## 1. Executive summary

The Skills Evaluation tool now runs as a containerised service on POCDAPP314,
with leads-only authentication and shared storage in Postgres, deployed and
managed through Portainer from a git-backed stack. The evaluation app and the team
summary both serve, and both were reached and exercised end to end.

The offline single-file distribution is **unchanged**. Both apps still work opened
straight from disk with no network access, so nothing existing users depend on has
been altered.

**Status: working, and not yet exposed.** The application is reachable only from
the host itself. TLS, DNS and the reverse proxy are the remaining work, and the
two hard gates below are not yet satisfied.

---

## 2. What was achieved

| # | Outcome | How it was proved |
|---|---|---|
| 1 | Container platform installed on RHEL 10.2 | `docker.service` active and enabled; `docker compose version` returns; `hello-world` runs |
| 2 | Container networking functional | `hello-world` completes, after loading the netfilter modules (see section 4) |
| 3 | Log rotation configured | `docker info` reports `json-file` with size and file limits |
| 4 | Reboot survival | Host rebooted; Docker, nginx, the modules, the sysctls and the SELinux boolean all returned unaided |
| 5 | nginx installed | 1.26.3, active and enabled, satisfying the `http2 on` requirement |
| 6 | Firewall minimal | Only `http` and `https` opened; 8001 and 9000 deliberately closed |
| 7 | SELinux prepared | `httpd_can_network_connect` set persistently, ahead of nginx needing it |
| 8 | Portainer running as control plane | Container up, bound to `127.0.0.1:9000`, unreachable from the network |
| 9 | Application stack deployed from git | Portainer git-backed stack `skills-eval`; image built on the host from `data/*.json` |
| 10 | Database running, unexposed | Postgres container publishes no port at all |
| 11 | Schema created automatically | `users`, `sessions`, `evaluations` present after first boot |
| 12 | First lead account created | App log line `Created bootstrap admin account.` |
| 13 | Both apps serve | `GET /` returns the evaluation app, `GET /team` the team summary |
| 14 | Server mode detected by the apps | Save and open controls present in the served HTML, absent in the offline file |
| 15 | Authentication enforced | `/api/evaluations` and `/api/reference` return 401 without a session |
| 16 | Loopback boundary holds | App and Portainer answer on 127.0.0.1 and fail from 10.21.12.62 |

---

## 3. Security properties demonstrated

These are the ones worth stating because they were designed in, not incidental.

- **Nothing application-related is on the network.** The app publishes on
  `127.0.0.1:8001` and Portainer on `127.0.0.1:9000`. Both were confirmed to
  refuse connections on 10.21.12.62. Access during commissioning was by SSH local
  forward, not by opening ports.
- **The database publishes no port**, and is reachable only by the app container
  over the Compose network.
- **Authentication is enforced server-side**, not by hiding UI. Unauthenticated
  API calls return 401.
- **Writes are append-only.** There is no update and no delete endpoint, so a
  mistaken save cannot destroy a completed review.
- **The firewall was not widened** to make anything work. 8001 and 9000 remain
  closed; the loopback binding is the control, not the firewall.

---

## 4. Deviations from the runbook, and why

Recorded because the next host will hit the same things.

| Finding | Impact | Resolution |
|---|---|---|
| **Netfilter kernel modules absent.** RHEL 10 minimal did not load `iptable_nat`, so there was no `nat` table and dockerd died with `RULE_APPEND failed (No such file or directory): rule in chain PREROUTING` | Docker would not start at all | Modules loaded and persisted in `/etc/modules-load.d/docker.conf`, plus two sysctls. Now section 4.4 of the host-prep runbook, marked required |
| **`systemctl status docker` hides the cause.** It shows only "Failed to start Docker Application Container Engine" | Several diagnostic rounds lost | `sudo dockerd --debug` prints the fatal line immediately. Added to the runbook |
| **dnf5 changed `config-manager` syntax.** The widely published `--add-repo` form is dnf4 and fails on RHEL 10 | Docker repo could not be added | `dnf config-manager addrepo --from-repofile=...`, documented |
| **Portainer disables initial setup** minutes after first start | Locked out; container restart needed | Compose now passes `--admin-password-file`, so the account exists before a browser is opened. Committed as `dd4e292` |
| **Host is not directly routable.** Access is RDP to a POCLAB box, then PuTTY from there | Tunnel guidance was initially wrong | The forward must be **Local** and lives on the machine running the SSH client; `echo $SSH_CLIENT` identifies it. Documented |
| **The remote had none of the work.** 42 files existed only in a local working tree, and the server had cloned a different repository | The git-backed stack cloned an empty repo | Committed and pushed as `7e415e4`; the server was repointed at the correct remote |
| **Docker packages are `el10`** native, not the el9 fallback | None - this is the supported combination | Recorded so no one assumes an unsupported mix |

---

## 5. How to reproduce the evidence

```
sudo bash deploy/verify-deployment.sh | tee evidence-$(date +%F).txt
```

Read-only: it reads service state, queries loopback endpoints and counts rows. It
changes nothing and is safe to run at any time.

It reports PASS, FAIL and SKIP per check, and exits non-zero if anything FAILed.
**SKIP is not a failure** - it marks checks that are not applicable yet, such as
the nginx vhosts before certificates exist.

Optional, to demonstrate the full analytics path:

```
sudo docker exec <app-container> python -m server.seed
```

That loads 34 synthetic evaluations. The team summary should then reproduce the
figures in `test-data/EXPECTED_RESULTS.md`: team average **3.01**, average delta
**-0.18**, **46** material gaps, bands **4 below / 3 exceeds / 9 meets /
4 partially**. Those numbers agreeing exercises storage, retrieval, the
latest-revision dedupe and the client-side analytics in one action.

That data is synthetic and safe to delete.

---

## 6. What is NOT yet done

| # | Item | Owner | Blocks |
|---|---|---|---|
| 1 | Internal CA certificates for `skills-eval.<zone>` and `portainer.<zone>` | PKI team | TLS, and therefore real data |
| 2 | DNS A records for both names to 10.21.12.62 | DNS team | Named access |
| 3 | Confirm the real POCLAB DNS zone | you | Every nginx config carries the `poclab.local` placeholder |
| 4 | Install the nginx vhosts and reload | you | Named access over TLS |
| 5 | Set the IP allow-list in `deploy/nginx/portainer.conf` | you, needs the admin subnet | Admin plane exposure once nginx fronts it |
| 6 | Set `COOKIE_SECURE=true` | you, after TLS | Real data |
| 7 | Data privacy review | Data Privacy Officer | Real data |
| 8 | Backup schedule for `pgdata` and `portainer_data` | you | Data durability |
| 9 | Decide on login throttling and account lockout | you | Scoped out, not overlooked |
| 10 | Automated tests against a real Postgres | you | 27 tests have never executed |

### The two hard gates

**No real evaluation data until both are satisfied.**

1. **TLS in front, with `COOKIE_SECURE=true`.** Today the session cookie is not
   marked `Secure` because the deployment is plain HTTP on loopback. That is
   correct for commissioning and wrong for real use.
2. **Data privacy review.** Once real evaluations are loaded this database becomes
   a shared system of record for named-employee performance data on EU staff,
   including performance classification and promotion recommendation. The Data
   Privacy Officer should review the design before that happens, and database
   backups inherit the same handling requirements.

Commissioning against `test-data/` raises neither concern: that data is synthetic
by construction.

---

## 7. Honest limits of this evidence

- **The 27 automated tests have never run.** They need a real Postgres and skip
  without `TEST_DATABASE_URL`. Skipping is not passing. The application was
  verified by direct use and by the API checks in the script, not by the suite.
- **The verification script has not been executed by its author.** It was written
  on a Windows machine with no shell available, so it was checked structurally
  rather than run. Expect the possibility of a rough edge on first execution.
- **nginx has never served this application.** The vhost configuration is written
  but `nginx -t` has never validated it against a real certificate, and the
  SELinux boolean has never actually been exercised by a proxy request.
- **Reboot survival was tested once.** That is enough to prove persistence was
  configured, not enough to characterise behaviour under load or over time.
