---
title: issues - Skills Evaluation & Enablement
type: issues
tags: [dq-coe, evaluation, issues, backlog]
updated: 2026-07-17
---

# issues.md

Open questions, decisions to make, known limitations, and the enhancement backlog.
Paired with [[HANDOFF]]. Status legend: OPEN / DECISION NEEDED / LIMITATION (by design) / DONE.

---

## Decisions needed (from the CoE / lead)

- **DEC-1 - Official 0-5 scale wording.** DONE (2026-07-04). CoE confirmed: **keep the current
  convention** (0 None, 1 Awareness, 2 Working, 3 Competent, 4 Proficient, 5 Expert).
- **DEC-2 - Learning granularity: area vs competency ref.** DONE (2026-07-04). Decision: **map at
  area level**, keep competency refs. No `renderLearning()` change needed.
- **DEC-3 - Projects vs Areas home.** OPEN (revisit later). Now homed under **Projects** at
  `Work/10 Projects/syniti-dq-consultant-evaluation`. Candidate to graduate `data/` + `sources/` to an
  **Areas** note once stable.
- **DEC-4 - Degreed tenant URLs.** CLOSED (2026-07-17, deferred). Decision: the learning catalog
  (incl. Degreed deep links) will be **curated as a later batch exercise** - Degreed items stay as
  tenant search until then. ENH-1/ENH-2 are folded into that future curation pass.
- **DEC-5 - AI Enablement expected values.** DECIDED (2026-07-17). The G31-G33 expected ratings are
  **confirmed as shipped** - the provisional values are now official. No data change needed.
- **DEC-6 - Degreed provider color.** DECIDED (2026-07-17). Degreed's provider color moves from the
  retired `#E08A0B` to the brand kit's slate-blue `#6F8BD9` (part of the kit retheme). `#E08A0B` was
  never Degreed's real brand color, and Degreed links resolve inside the Syniti tenant (LIM-1), so
  there is no external-brand reason to keep it. LinkedIn `#0A66C2` / Coursera `#0056D2` unchanged.

---

## Known limitations (by design / external constraint)

- **LIM-1 - Degreed has no public deep links.** Degreed is an enterprise LXP; course URLs are behind
  the org's SSO. Degreed items resolve inside the Syniti tenant only. (This is why Coursera was
  briefly substituted; Degreed is back with tenant-resolving links.)
- **LIM-2 - Some learning links are search entry points, not specific courses.** Items with `d:0`
  open a provider topic/search page; `d:1` items are verified course pages. Curating `d:0 -> d:1`
  is a backlog item (ENH-1).
- **LIM-3 - No live AI in the tool.** By design (standalone, no API key). AI assistance is
  copy-paste ("bring your own assistant"). A live-rating variant is only possible if the tool runs
  inside an environment that can call a model (e.g. Claude / Claude Code).
- **LIM-4 - C7-C8 not rated.** The source competency matrix does not define expectations for C7-C8,
  so those levels have no expected values.
- **LIM-5 - Multiple copies of COMPS / LEARNING.** The eval tool embeds both consts (rebuilt from
  `data/*.json` by `build/build.py`, so for that tool the JSON is the master). The **team summary
  app** also embeds its own copy of `COMPS` (exports do not carry expectations) and is hand-edited -
  when the competency matrix changes, update `data/competencies.json`, run the builder, and re-embed
  the team app's `const COMPS` (same short-key conversion as build.py).
- **LIM-6 - Clipboard in `file://`.** Copy-prompt uses the async clipboard API with an
  `execCommand('copy')` fallback so it works when the file is opened directly from disk.
- **LIM-7 - No browser storage.** The tool intentionally keeps all state in memory and persists via
  the downloadable JSON (not localStorage), so it works as a portable file and in sandboxed embeds.

---

## Enhancement backlog

- **ENH-1 - Curate `d:0` learning links to verified course pages.** Priority: high.
- **ENH-2 - Add Degreed tenant deep links** (depends on DEC-4). Priority: high.
- **ENH-3 - Pin learning to competency refs** (depends on DEC-2; `renderLearning()` change). Medium.
- **ENH-4 - Per-rating evidence note.** Have the AI prompt return a one-line justification per
  competency; surface as a tooltip on each matrix tile. Medium.
- **ENH-5 - Single source for the catalog.** Add a tiny build step (or in-tool loader) so
  `data/learning-catalog.json` is the only place to edit. Medium.
- **ENH-6 - Management report (team / heatmap roll-up).** DONE (2026-07-17) - shipped as
  `tool/Syniti_Team_Skills_Summary.html` (see HANDOFF section 4.7): team KPIs + Insights, C-grade
  filter, roster, heatmap, growth-by-area chart, drill-down, team export.
- **ENH-7 - Clean single builder.** DONE (v6) - `build/build.py` + `build/template.html`.
- **ENH-8 - Live AI variant.** DROPPED. The AI copy/paste path was removed in v6 at the CoE's request;
  a live variant is not planned.

---

## Notes / risks

- The `build/build-scripts/` chain (`build2 -> build3 -> build4 -> build_final`) is fragile and
  chat-specific. Do not extend it further; edit the HTML or make a clean builder (ENH-7).
- Keep the "-" hyphen (no long dash) and the PowerPoint size 33.87 x 19.05 cm as standing rules
  (see [[HANDOFF]] section 10).
- **Reconciliation (2026-07-17).** The project briefly had two homes: this monorepo folder (stale at
  v5) and a standalone repo `github.com/truwaynegordon/syniti-consultant-eval` (v6) cloned inside
  the Obsidian vault. Resolved: monorepo is canonical; v6 folded in; the standalone clone moved to
  `~/repos/syniti-consultant-eval` and its repo is archive-only; the vault folder is git-free (a
  plain mirror synced at /vala). Registry follow-up still open: fix `vaultFolder`/`handoffVault`
  paths in `~/repos/claude-project-tg/.vala/projects.json` (old TGORDON home + old vault name) and
  note the archived standalone repo.

---

## Resolved

- **DONE (v6) - Runnable build fixed.** v5 shipped a Python builder with placeholders, not a tool;
  now emitted by `build/build.py` as real HTML. (See HANDOFF v6 note + section 9.)
- **DONE (v6) - AI Guided-review removed** (5 -> 4 sections; prompt/paste-back + `reviewMode` gone).
- **DONE (v6) - AI competencies restructured** into AI Enablement (G31-G33; old G33/G34/G35 removed).
- **DONE (v6) - Download competencies (.csv)** button added.
- **DONE (v6) - Career Framework** surfaced as a per-level HR reference.
- **DONE (v6) - Simplified Excel matrix** generated (`Competency Matrix (simplified).xlsx`).
- **DONE - Real learning links** (LinkedIn + Coursera verified where available).
- **DONE - Summary moved up** (merged into the top overview card).
- **DONE - Wider, less-vertical layout** (multi-column matrix tiles; full-width rating).
- **DONE - Ten-point overhaul** (legend shrink + align, collapse-all, button restyle, left nav,
  five sections, section icons, official logo, rename, EMEA label, Degreed re-added).
- **DONE - Official "Syniti - Part of Capgemini" logo** embedded.
- **SUPERSEDED - AI-assisted review** (v4/v5 prompt generation + paste-back) - removed in v6.
- **DONE (2026-07-17) - Syniti brand-kit retheme** applied to `build/template.html` (tool rebuilt)
  and the team app: pure system font stack (fixes the offline Courier fallback), kit tokens, aurora
  underlay, semantic status registers.
- **DONE (2026-07-17) - Team Skills Summary app** shipped (ENH-6) with test-data/ harness.
- **DONE (2026-07-17) - Competency ladder + explicit framework linkage** (maturity phase): section
  05 ladder (78 x 9 matrix with Career Framework roles) and the section 01 expected-profile panel.
