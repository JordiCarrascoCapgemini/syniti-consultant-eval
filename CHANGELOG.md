# Changelog

Concise version history. Full decisions and rationale live in
[notes/Change log & decisions.md](notes/Change%20log%20&%20decisions.md).

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
