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

  This regenerates the runnable `tool/...html`. **Do not hand-edit the tool file** - it is a build
  artifact. `data/*.json` are the single source of truth.

## What is here

| Path | What it is |
|------|------------|
| `tool/` | The runnable evaluation web app (single self-contained HTML; a build output). |
| `build/` | `build.py` (the builder) + `template.html` (the shell). `legacy/` holds the old build chain. |
| `data/` | Source of truth: `competencies.json` / `.csv` and `learning-catalog.json`. |
| `Competency Matrix (simplified).xlsx` | Clean 78-row matrix + rating-scale sheet, generated from `data/`. |
| `sources/` | Originals this was built from (Career Framework PDF, competency matrix xlsm, style refs, logo). |
| `notes/` | Data model & rating scale, learning-catalog how-to, change log & decisions, roadmap. |
| `prompts/` | The old AI-review prompt (deprecated in v6). |
| `HANDOFF.md`, `issues.md` | Entry point + open issues / backlog. |

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
