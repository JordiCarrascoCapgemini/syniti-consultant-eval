---
title: issues - Skills Evaluation & Enablement
type: issues
tags: [dq-coe, evaluation, issues, backlog]
updated: 2026-07-04
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
- **DEC-4 - Degreed tenant URLs.** OPEN (input). Still needed. The profile link supplied
  (`degreed.com/profile/dguser9rqx/skills`) is a personal skills page behind SSO, not a public
  course/pathway deep link - so Degreed items stay as tenant search until real pathway URLs are given.
- **DEC-5 - AI Enablement expected values.** OPEN (input). The three AI competencies (G31-G33) carry
  **provisional** expected ratings; confirm/adjust with the CoE.

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
- **LIM-5 - Two copies of the learning catalog.** The tool embeds `const LEARNING`; `data/
  learning-catalog.json` is the mirror/master. Editing one does not update the other automatically.
  Keep them in sync (or add a small re-embed step - ENH-5).
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
- **ENH-6 - Management report (team / heatmap roll-up).** NEXT PLANNED BUILD. A **separate standalone
  HTML tool** that imports several individual `Evaluation_*.json` files and aggregates them into a
  team-by-competency heatmap + gap view. Medium/large.
- **ENH-7 - Clean single builder.** DONE (v6) - `build/build.py` + `build/template.html`.
- **ENH-8 - Live AI variant.** DROPPED. The AI copy/paste path was removed in v6 at the CoE's request;
  a live variant is not planned.

---

## Notes / risks

- The `build/build-scripts/` chain (`build2 -> build3 -> build4 -> build_final`) is fragile and
  chat-specific. Do not extend it further; edit the HTML or make a clean builder (ENH-7).
- Keep the "-" hyphen (no long dash) and the PowerPoint size 33.87 x 19.05 cm as standing rules
  (see [[HANDOFF]] section 10).

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
