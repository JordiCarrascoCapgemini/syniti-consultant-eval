---
title: Skills Evaluation & Enablement
type: project
area: "[[Syniti Data Quality CoE]]"
status: active
owner: 
tags: [dq-coe, evaluation, enablement, competency, tool]
updated: 2026-07-04
---

# Skills Evaluation & Enablement

A standalone, self-contained web tool that evaluates a Syniti consultant against the
competency expectations for their C-level, classifies performance, captures feedback,
and maps targeted learning (LinkedIn Learning, Coursera, Degreed) to close each gap.

> [!tip] Open the tool
> [[Syniti_Skills_Evaluation_and_Enablement.html|Open the evaluation tool]] (in `tool/`).
> It is a single HTML file - no install, works offline, downloads/imports its own JSON.

## What is here
- `tool/` - the evaluation web app (single HTML file; a build output - regenerate with `build/build.py`).
- `Competency Matrix (simplified).xlsx` - clean 78-row matrix + rating-scale sheet.
- `build/` - `build.py` (the builder) + `template.html` (the shell); `legacy/` is the old chain.
- `sources/` - the originals this was built from (career framework PDF, competency matrix xlsm, style references).
- `data/` - extracted, curatable data (single source of truth): [[competencies.json]] / competencies.csv and the [[learning-catalog.json]].
- `prompts/` - the [[Guided review prompt]] (DEPRECATED - the AI flow was removed in v6).
- `notes/` - documentation: [[Data model & rating scale]], [[Learning catalog - how to update]], [[Change log & decisions]], [[Roadmap]].

## Project vs Area
This folder sits under **Projects** because the tool is an active deliverable with iterations.
The underlying **competency framework and learning catalog** are an ongoing CoE capability -
if you prefer, move `data/` and `sources/` into an **Areas** note (e.g. `Areas/DQ Competency Framework`)
and keep only the tool + notes here in Projects. Recommendation: keep it all together here while
actively building; graduate the data + catalog to Areas once they stabilise.

## How the tool works (one paragraph)
Pick the consultant's C-level (a **Career Framework** reference shows what that level means), scope
the relevant competency areas, then rate each competency 0-5. The tool computes delta-to-level, an
overall classification, per-area bars, and a learning plan. Everything exports to a JSON file that can
be re-imported later to show change over time; you can also download the competency list with its
per-level expectations as CSV.

## Related
- [[Data model & rating scale]]
- [[Learning catalog - how to update]]
- [[Change log & decisions]]
- [[Roadmap]]
