# Changelog

Concise version history. Full decisions and rationale live in
[notes/Change log & decisions.md](notes/Change%20log%20&%20decisions.md).

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
