# Skills Evaluation & Enablement

A standalone, single-file HTML tool for Syniti EMEA Data Quality CoE delivery leads to evaluate a
consultant against the competency expectations for their C-level, classify performance, capture
narrative feedback, and map targeted learning (LinkedIn Learning, Coursera, Degreed) to close each gap.
Works offline, downloads its own JSON form, and can re-import a prior evaluation to show change over time.

> Full details, architecture, and every design decision are in **[HANDOFF.md](HANDOFF.md)** - read that first.

## Quick start

- **Use it:** open [`tool/Syniti_Skills_Evaluation_and_Enablement.html`](tool/Syniti_Skills_Evaluation_and_Enablement.html)
  directly in a browser. No install, no server, no network.
- **Change it:** edit `data/*.json` (content) or `build/template.html` (shell/CSS/JS), then run:

  ```bash
  python3 build/build.py
  ```

  This regenerates **both** runnable apps in `tool/`. **Do not hand-edit either tool file** -
  they are build artifacts. `data/*.json` are the single source of truth.

- Run the server (optional, adds login and shared storage):

  ```
  cp .env.example .env    # then fill in POSTGRES_PASSWORD and ADMIN_PASSWORD
  docker compose up --build
  ```

  The eval app is served at `/` and the team summary at `/team`. The single files keep
  working offline exactly as before; the server-only buttons appear only when an API answers.
  This must not hold real evaluation data until it is fronted with TLS and started with
  `COOKIE_SECURE=true` - see `CLAUDE.md`.

- Prepare the POCLAB server (RHEL 10.2) before first deployment: install Docker, nginx,
  SELinux and firewall rules, and Portainer by following
  **`deploy/HOST-PREP-POCDAPP314.md`**.

- Deploy to the POCLAB server (POCDAPP314 / 10.21.12.62) behind nginx, via Portainer:
  follow **`deploy/DEPLOY-POCDAPP314.md`**. The architecture, including how users reach the app
  and how the next application is onboarded, is in **`deploy/architecture.html`** (open in a
  browser).

## What is here

| Path | What it is |
|------|------------|
| `tool/` | The two runnable web apps (self-contained HTML; both build outputs). |
| `build/` | `build.py` (the builder) + `template.html` and `template-team.html` (the shells). `legacy/` holds the old build chain. |
| `refdata.py` | The one loader for `data/*.json`, shared by the builder and the server. |
| `server/` | FastAPI app: auth, evaluations API, reference data, seed command. |
| `db/` | `schema.sql` - three tables, applied idempotently at startup. |
| `tests/` | pytest suite, including an end-to-end check against `test-data/EXPECTED_RESULTS.md`. |
| `Dockerfile`, `docker-compose.yml`, `.env.example` | The deployable stack (app plus Postgres). |
| `deploy/` | Hosting: nginx vhosts + snippets, the Portainer stack, host-prep and deployment runbooks, the architecture document, and `EXPOSURE-READINESS.md` (what must be true before this leaves POCLAB). |
| `data/` | Source of truth: `competencies.json` / `.csv` and `learning-catalog.json`. |
| `Competency Matrix (simplified).xlsx` | Clean 78-row matrix + rating-scale sheet, generated from `data/`. |
| `sources/` | Originals this was built from (Career Framework PDF, competency matrix xlsm, style refs, logo). |
| `notes/` | Data model & rating scale, learning-catalog how-to, change log & decisions, roadmap. |
| `prompts/` | The old AI-review prompt (deprecated in v6). |
| `test-data/` | 34 synthetic evaluations + expected results. Safe to delete. |
| `HANDOFF.md`, `issues.md` | Entry point + open issues / backlog. |
| `CLAUDE.md` | Guidance for agents: build invariants and the deployment design decisions. |

## Current state (v6)

78 competencies across 13 areas; four sections (Details & summary, Scope, Skills evaluation,
Learning plan). Highlights of v6: a clean single builder replacing the old fragile chain; the AI
Guided-review section removed; an **AI Enablement** competency area; a competency CSV download; and a
per-level **Career Framework** HR reference. See `notes/Change log & decisions.md`.

## Data model (summary)

Expectations are 0-5 per C-level (C1-C6, split into Solution `-S` / Managing `-M` tracks at C4-C6;
C7-C8 are not rated in the source). Scale: 0 None, 1 Awareness, 2 Working, 3 Competent, 4 Proficient,
5 Expert. Full detail in `notes/Data model & rating scale.md`.

---

Internal Syniti Data Quality CoE material. Private repository.
