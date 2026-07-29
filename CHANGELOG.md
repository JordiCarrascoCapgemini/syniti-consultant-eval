# Changelog

Concise version history. Full decisions and rationale live in
[notes/Change log & decisions.md](notes/Change%20log%20&%20decisions.md).

## v7.1 (2026-07-28)
- **Hosting and ingress design added** for POCDAPP314 (10.21.12.62): host-level nginx as a
  shared reverse proxy, one hostname and one internal-CA certificate per application on the
  shared IP, routed by Host header and TLS SNI. `deploy/DEPLOY-POCDAPP314.md` is the runbook,
  `deploy/architecture.html` the architecture document, `deploy/nginx/` the configuration.
- **The app now publishes on loopback only.** `docker-compose.yml` binds
  `127.0.0.1:8001:8000`, so nginx is the only route in and the app is not reachable from the
  lab network. Previously it published on all interfaces.
- **uvicorn runs with `--proxy-headers`** so the app sees the client's real scheme and address
  through the proxy hop.
- Added a catch-all nginx default server, so the bare IP and unknown hostnames return 404
  rather than falling through to whichever vhost loaded first.
- **Portainer CE added as the deployment mechanism and management plane.** Application stacks
  are deployed from git through Portainer, so deploying does not require shell access and
  secrets live as stack environment variables rather than an on-disk `.env`. Portainer itself
  is CLI-deployed (`deploy/portainer/docker-compose.yml`) and reached through nginx on its own
  FQDN, published on loopback only. It mounts the Docker socket and is root-equivalent on the
  host, so its vhost carries an IP allow-list and a pinned image.
- Split the nginx header snippet into `security-baseline.conf` and `csp-apps.conf`: the app
  content-security-policy breaks Portainer's bundled UI, so only our own vhosts include it.
- Added `snippets/proxy-ws.conf` for WebSocket upstreams. `proxy-app.conf` sets
  `Connection ""` for upstream keepalive, which silently breaks the upgrade handshake that
  Portainer needs for container consoles and live logs.
- **Added `deploy/HOST-PREP-POCDAPP314.md`**: the RHEL 10.2 host-preparation runbook - Docker
  Engine from Docker's repo (with the dnf5 syntax difference and the Podman shim conflict
  called out), daemon log rotation, the `httpd_can_network_connect` SELinux boolean, firewalld,
  nginx, and Portainer, ending in a 12-point checklist including reboot survival.
- DEC-9 records the hosting decisions, DEC-10 the deployment mechanism. Nothing in this release
  has been executed on the server.

## v7.0 (2026-07-28)
- **Dockerized, deployable server** (`server/`, `db/schema.sql`, `Dockerfile`,
  `docker-compose.yml`): FastAPI plus Postgres, serving the two existing apps and adding
  optional save/load. Basic authentication for leads (server-side sessions, argon2 hashes,
  first admin from a mandatory env var). Evaluations stored as JSONB, append-only, read
  latest per consultant and date. All scoring stays in the apps' JS - none is reimplemented
  server-side.
- **Additive, not replacing.** Opened from `file://` both apps behave exactly as before and
  make no network call; the server-only controls appear only when an API answers.
- **The team app is now generated** from `build/template-team.html`, so `build.py` emits both
  apps from `data/competencies.json`. This closes LIM-5.
- **New:** `refdata.py` (one shared loader for the reference data), `GET /api/reference`,
  an evaluation restore path in the eval app (the file importer only ever compared),
  `python -m server.seed`, and a pytest suite including an end-to-end check against
  `test-data/EXPECTED_RESULTS.md`.
- **Fixed:** `build.py` read and wrote without an explicit encoding or newline policy, so it
  produced different bytes on Windows and Linux. Both are now explicit.
- DEC-7 decided: this repo is canonical again (see issues.md). DEC-8 records the design.

## v6.2 (2026-07-17)
- **Maturity phase: the skill <-> C-level <-> Career Framework relationship made explicit.**
  Section 01 now renders a linkage sentence (framework role + headline -> matrix expectations) and
  an "Expected profile at this level" panel (per-area expected-rating bars, updating with the level
  selector), with a provenance note (matrix = data/competencies.json; narrative = Career Framework
  2024 PDF; joined by C-level).
- **New section 05 "Competency ladder"**: the full 78-competency expected-rating matrix across all
  nine C-levels, columns headed by level code + Career Framework role, ordinal intensity ramp,
  selected level highlighted, print-friendly. The requirements-by-level reference.
- DEC-5 decided: AI Enablement (G31-G33) expected values confirmed as shipped.
- DEC-4 closed (deferred): learning-catalog curation (incl. Degreed links) is a later batch exercise.

## v6.1 (2026-07-17)
- **Reconciliation**: the project's two homes (standalone repo `syniti-consultant-eval` at v6;
  monorepo folder stale at v5) merged - the **monorepo folder is canonical**; the standalone clone
  moved to `~/repos/syniti-consultant-eval` and its GitHub repo is archive-only; the Obsidian vault
  folder is git-free again (plain mirror, Obsidian Sync only).
- **Syniti brand-kit retheme** applied to `build/template.html` (tool rebuilt via `build/build.py`):
  pure system font stack (no Google Fonts - fixes the offline Courier fallback), kit tokens
  (#365EB9 / #5B30EE / #232F63, good/warn/critical registers), `body::before` aurora, glass +
  navy-tinted shadows, tabular-nums. Degreed provider color -> kit slate-blue #6F8BD9 (DEC-6).
- **Team Skills Summary app** (`tool/Syniti_Team_Skills_Summary.html`, ENH-6): imports many
  evaluation JSONs; team KPIs + Insights (top improvement areas, severest gap, cohort watch),
  global C-grade filter, roster with trends, 13-area heatmap, growth-by-area dumbbell chart,
  drill-down, whole-team JSON export. Runs on the 78-comp AI Enablement model.
- **test-data/**: 34 deterministic synthetic evaluations (20 consultants, all 9 C-levels, all 13
  areas, 14 with priors and per-area trends) + `EXPECTED_RESULTS.md` truth sheet.

## v6 (2026-07-04)
- Homed in Obsidian under Projects; added `Competency Matrix (simplified).xlsx`.
- Replaced the fragile `str_replace` build chain with one clean builder (`build/build.py` +
  `build/template.html`). The v5 "tool" had shipped as an unrunnable Python builder with
  `__COMPS__`/`__LEARNING__` placeholders; the output is now a real self-contained HTML.
- Removed the AI Guided-review section (5 -> 4 sections; prompt/paste-back JS and `reviewMode` gone).
- Restructured the AI competencies into an **AI Enablement** area (`G31` General AI Knowledge &
  Day-to-Day Use, `G32` AI-Augmentation: Development Acceleration, `G33` AI-Augmentation: Delivery &
  Consulting Quality). Removed old `G33`/`G34`/`G35`. 80 -> 78 competencies. Expected values for the
  three are provisional pending CoE confirmation.
- Added a **Download competencies (.csv)** button.
- Added a per-level **Career Framework** HR reference (`const FRAMEWORK`) in section 01.

## v5
- Renamed to **Skills Evaluation & Enablement**; official "Syniti - Part of Capgemini" logo; five
  sections + hideable left nav + section icons; Details + Summary merged into one aligned card;
  Skills + Feedback merged; Degreed re-added alongside LinkedIn + Coursera; rating buttons restyled;
  competency areas get collapse/expand-all.

## v4
- AI-guided review: generate a prompt for Copilot/Claude/ChatGPT and paste the JSON back to auto-fill
  ratings; wider multi-column matrix layout.

## v3
- Real learning links (LinkedIn Learning + Coursera verified where possible); summary moved to the top.

## v2
- Lighter glassmorphic theme (aurora background, glass cards); added a learning layer.

## v1
- Competency matrix rating tool (dark theme); scope + 0-5 matrix; live summary; JSON export/import
  with change tracking.
