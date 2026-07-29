---
tags: [dq-coe, evaluation, log]
updated: 2026-07-04
---

# Change log & decisions

## Build history
- **v1** - competency matrix rating tool (dark theme), scope + 0-5 matrix, live summary,
  JSON export/import with change tracking.
- **v2** - lighter **glassmorphic** theme (aurora background, glass cards) combining the
  data-journey-map look with Syniti typography; added a learning layer.
- **v3** - real learning links (LinkedIn Learning + Coursera verified where possible);
  summary moved to the top.
- **v4** - **AI-guided review**: generate a prompt for Copilot/Claude/ChatGPT and paste the
  assistant's JSON back to auto-fill ratings; wider, multi-column tile layout for the matrix.
- **v5** - renamed to **Skills Evaluation & Enablement**; Syniti logo in header;
  header label **Syniti EMEA Data Quality**; sections consolidated to five with a hideable
  left nav and section icons; Details + Summary merged into one aligned two-column card;
  Skills + Feedback merged; **Degreed added back** alongside LinkedIn + Coursera; rating
  buttons restyled (shaded, smaller, clearer); competency areas get **collapse/expand all**.
- **v7.1 (2026-07-28)** - hosting design for POCDAPP314: host-level nginx as shared reverse
  proxy, one FQDN and internal-CA certificate per app on the shared IP 10.21.12.62, app bound
  to loopback so nginx is the only route in. Portainer CE added as the deployment mechanism
  (git-backed stacks) and management plane, itself behind nginx on its own FQDN. DEC-9 and
  DEC-10. Not yet executed on the server.
- **v7.0 (2026-07-28)** - dockerized deployable server (FastAPI plus Postgres) added
  alongside the portable files, which are unchanged offline. Leads-only authentication,
  JSONB append-only storage, and the team app brought under `build.py` (closes LIM-5).
  DEC-7 (this repo canonical again) and DEC-8 (design recorded in `CLAUDE.md`).
- **v6 (current)** - homed in Obsidian under Projects; added `Competency Matrix (simplified).xlsx`.
  **Fixed a foundational problem:** the v5 "tool" was a Python builder with `__COMPS__` placeholders,
  not a runnable HTML - replaced the fragile build chain with one clean `build/build.py` +
  `build/template.html`, emitting a real self-contained tool.
  **Removed the AI Guided-review section** (5 -> 4 sections; prompt/paste-back JS + `reviewMode` gone).
  **Restructured the AI competencies** into an **AI Enablement** area: G31 General AI Knowledge &
  Day-to-Day Use, G32 AI-Augmentation: Development Acceleration, G33 AI-Augmentation: Delivery &
  Consulting Quality; removed old G33/G34/G35 (80 -> 78). **Added a Download competencies (.csv)**
  button. **Added a Career Framework per-level HR reference** (`const FRAMEWORK`) in section 01.

## Key decisions
- **Standalone HTML** (no API key, works offline). The AI copy/paste review was **removed in v6**
  (the CoE decided the prompt path added little); the tool is now a clean manual + import workflow.
- **Build**: `data/*.json` are the single source of truth; `build/build.py` regenerates the tool.
  Do not hand-edit `tool/...html`.
- **AI Enablement** area replaces "Squad-Specialized and AI Driven"; its three competencies' expected
  values are **provisional pending CoE confirmation**.
- **Career Framework** is a per-level reference (justifies the expectation), not part of the score.
- **Degreed links** resolve inside the Syniti Degreed tenant; no public deep links exist.
- **Scale 0-5** labels (None -> Expert): CoE confirmed the convention for now (DEC-1).
- **Learning** maps at **area** level, keeping competency refs (DEC-2).
- **C7-C8** not rated (absent from the source matrix).
- Formatting preference: use "-" not the long dash; PowerPoint deliverables at 33.87 x 19.05 cm.

## Open questions
- Official wording for the 0-5 scale?
- Map learning at area level (now) or per competency ref?
- Should the framework/catalog graduate from Projects to an Areas note once stable?
