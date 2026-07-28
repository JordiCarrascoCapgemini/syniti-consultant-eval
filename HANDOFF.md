---
title: HANDOFF - Skills Evaluation & Enablement
type: handoff
area: "[[Syniti Data Quality CoE]]"
status: active
tags: [dq-coe, evaluation, enablement, handoff, claude-code]
updated: 2026-07-17
---

> **Reconciliation + v6.1 note (2026-07-17).** Two Claude Code sessions had diverged: v6 lived in a
> standalone repo (`github.com/truwaynegordon/syniti-consultant-eval`) cloned inside the Obsidian
> vault, while the monorepo copy was stale at v5. Resolved 2026-07-17: **this monorepo folder is
> canonical again**; v6 content was folded in wholesale; the standalone clone moved to
> `~/repos/syniti-consultant-eval` (archive) and the vault folder is git-free again (Obsidian Sync
> only). On top of v6, this session added: **Syniti brand-kit retheme** (system font stack - fixes
> the offline Courier fallback - kit tokens, aurora underlay; applied to `build/template.html` and
> rebuilt), the **Team Skills Summary sibling app** (`tool/Syniti_Team_Skills_Summary.html`: imports
> many evaluation JSONs; team KPIs, Insights, roster, heatmap with C-grade filter, growth-by-area
> chart, drill-down, team export - ENH-6 done), and **test-data/** (34 deterministic synthetic
> evaluations + expected-results truth sheet, built on the 78-comp AI Enablement model).

> **v6 note (2026-07-04).** Two things changed materially since v5:
> 1. **The v5 bundle never shipped a runnable tool.** `tool/...html` was actually a *Python builder*
>    with `__COMPS__`/`__LEARNING__` placeholders (it would not open in a browser). It is now a real,
>    self-contained HTML, produced by one clean builder - see **section 9**.
> 2. **Four changes landed:** the AI "Guided review" section was removed (5 -> 4 sections); the AI
>    competencies were restructured into an **AI Enablement** area (3 items; expectations confirmed 2026-07-17);
>    a **Download competencies (.csv)** button was added; and the **Career Framework** is now surfaced
>    as a per-level HR reference. Details in sections 2, 4 and the change log.

# HANDOFF - Skills Evaluation & Enablement

Single entry point for picking this up in a Claude Code project. It captures what the tool is,
its current state, how it is built, how to change it, every design decision, and the open issues.
Read this first, then [[issues|issues.md]], then the notes in `notes/`.

Companion notes: [[Skills Evaluation & Enablement|Index/MOC]] - [[Data model & rating scale]] -
[[Learning catalog - how to update]] - [[Change log & decisions]] - [[Roadmap]] - [[Guided review prompt]].

---

## 1. What this is

A **standalone, single-file HTML tool** that lets a Syniti delivery lead evaluate a consultant
against the competency expectations for their C-level, classify performance, capture narrative
feedback, and map targeted learning (LinkedIn Learning, Coursera, Degreed) to close each gap.

- Audience: Syniti **EMEA Data Quality** CoE delivery leads.
- Constraints from the outset: **standalone HTML**, works offline, **downloads its own form**
  (JSON) and can **re-import a prior evaluation to show change** over time.
- Look: light **glassmorphic** theme, combining the `data-journey-map` reference aesthetic with
  Syniti brand typography and the official Syniti logo.

### Requirement history (verbatim intent, in order)
1. Capture consultant performance by C-level + expectation + skills matrix; short assessment that
   gathers answers, classifies, rates, gives project feedback; standalone HTML; download the form;
   fields for name / project / lead; import a previous performance and show change; style of the
   attached reference HTML.
2. Combine styles with the second reference - lighter, glassmorphic. Add learning options for
   Degreed or LinkedIn Learning; deconstruct/curate later; sample for now.
3. Move the summary to the top (or show it another way). Make the development-plan links **real**
   (actual LinkedIn/Degreed courses; another catalog allowed).
4. Add an **AI-assisted** path: generate a prompt to paste into Copilot/Claude/ChatGPT (Q&A or
   from notes) and rate from the result. Make the layout **less vertical, more horizontal**.
5. Ten-point overhaul: shrink the rating legend so the top two blocks line up; collapse-all on the
   matrix; more button-like rating buttons (shaded, smaller); hideable **left section nav**;
   restructure to **five sections**; add **section icons**; **Syniti logo** top-left; rename to
   **Skills Evaluation & Enablement**; rename the label to **Syniti EMEA Data Quality**; **add
   Degreed back** (was replaced by Coursera) and keep the learning repo updatable.
6. Use the **official** "Syniti - Part of Capgemini" logo (uploaded).
7. Produce this handoff + issues, add to the Obsidian bundle; continue in Claude Code.
8. (v6, in Claude Code) Home the project in Obsidian under Projects; add a simplified Excel matrix;
   **remove the AI Guided-review path**; **restructure the AI competencies** into an AI Enablement
   area; add a **competency download**; surface the **Career Framework** as a per-level HR reference;
   and replace the broken build chain with **one clean builder** that emits a genuinely runnable HTML.

---

## 2. Current status (v6) - what is done and validated

**Canonical home:** `Obsidian/.../Work/10 Projects/syniti-dq-consultant-evaluation` (this bundle).
Deliverable: `tool/Syniti_Skills_Evaluation_and_Enablement.html` - now a **real, self-contained,
runnable HTML** (~107 KB), generated by `build/build.py` from `data/*.json` + `build/template.html`.

v6 changes (all applied):
- **AI Guided-review section removed.** All prompt/paste-back JS and the `reviewMode` state are
  gone. `prompts/Guided review prompt.md` is deprecated. The tool is now **five sections**
  (01 Details & summary, 02 Scope, 03 Skills evaluation, 04 Learning plan, 05 Competency ladder -
  the ladder added 2026-07-17, see below).
- **AI competencies restructured** into a new **AI Enablement** area (was "Squad-Specialized and AI
  Driven"): `G31` General AI Knowledge & Day-to-Day Use, `G32` AI-Augmentation: Development
  Acceleration, `G33` AI-Augmentation: Delivery & Consulting Quality. Old `G33/G34/G35`
  (AI-Generated Rule Content, Syniti Vision, Syniti Classify) removed. **80 -> 78 competencies.**
  Expected values for the three were confirmed by the CoE lead on 2026-07-17 (DEC-5 decided).
- **Download competencies (.csv)** button (header) exports every competency with its per-C-level
  expected rating.
- **Career Framework reference** (`const FRAMEWORK`) shows, per selected C-level, the role headline,
  the expectation narrative, and the Data Quality / track focus - a reference footnote in section 01
  that justifies the level expectation. Reference only, not scored.

Validated (v6): builder emits HTML with **no placeholders**; embedded `COMPS` (78) and `LEARNING`
parse as JSON; full `<script>` parses (esprima); every DOM id the script references exists in markup;
`{}`/`()`/`[]` balanced; **no "-" long dash** (build guard). Live browser render not re-checked in
this environment (Chrome extension offline; open the file directly to view).

**Data validation still open (v5 claim was overstated):** the shipped v5 file was a *builder*, not a
runnable tool - see the v6 note at the top and section 9.

---

## 3. Repository map (this folder)

```
syniti-dq-consultant-evaluation/
  HANDOFF.md                     <- you are here
  issues.md                      <- open issues, questions, limitations, roadmap
  Skills Evaluation & Enablement.md   <- Obsidian index / MOC
  Competency Matrix (simplified).xlsx <- clean 78-row matrix + rating scale (generated from data/)
  tool/
    Syniti_Skills_Evaluation_and_Enablement.html   <- the RUNNABLE app (build output; do not hand-edit)
    Syniti_Team_Skills_Summary.html                <- sibling app: team roll-up (ENH-6; hand-edited, no build step)
  test-data/
    Evaluation_*.json (34) + EXPECTED_RESULTS.md   <- deterministic synthetic evals + truth sheet for testing the team app
  build/
    build.py                     <- the one clean builder: data/*.json + template.html -> tool/*.html
    template.html                <- HTML/CSS/JS shell with logo embedded + __COMPS__/__LEARNING__
    legacy/                      <- the old fragile str_replace chain, kept for reference only
  sources/
    Syniti_Career_Framework_2024.pdf               <- levels C1-C8, Managing + Solution tracks
    EMEA_DQ_Common_Competency_Matrix.xlsm          <- 80 competencies x expected ratings per level
    syniti-ai-acceleration (style ref).html        <- dark style reference (typography)
    data-journey-map (style ref).html              <- light glassmorphic style reference
    syniti-logo (official).png                     <- official transparent logo asset
  data/
    competencies.json / competencies.csv           <- extracted competency data + expectations
    learning-catalog.json                          <- the curatable learning repo
  prompts/
    Guided review prompt.md                        <- DEPRECATED (v6): the old AI prompt template
  notes/
    Data model & rating scale.md
    Learning catalog - how to update.md
    Change log & decisions.md
    Roadmap.md
  build/
    README.md                                      <- build history + go-forward guidance
    build-scripts/  build2.py build3.py build4.py build_final.py   <- historical builders (reference)
    inputs/         comps.json comps_min.json learning.json logo_b64.txt   <- reusable build inputs
```

---

## 4. The tool - internal architecture (for editing directly in Claude Code)

The output HTML is self-contained: one `<style>` block, the markup, one `<script>` block - open it
in a browser, no runtime build needed. **To change it, edit `build/template.html` (shell/CSS/JS) or
`data/*.json` (content), then run `python3 build/build.py`.** Do not hand-edit `tool/...html` - it is
a build artifact and will be overwritten. See section 9.

### 4.1 Design tokens (CSS variables, in `:root`) - Syniti brand kit (2026-07-17 retheme)
```
--navy #232F63  --blue #365EB9  --violet #5B30EE (lone accent, primary actions only)
--ink #20242E   --muted #6B7492 --slate #64748B  --dim #8FA1C8  --canvas #F6F8FE
--good #0E9F6E  --warn #B45309 (+ --warn-bg #FEF3E2, --warn-line #F5D9A8)  --critical #DC2626
--glass-fill / --glass-hairline / --glass-blur / --glass-shadow (kit glass material)
--grad linear-gradient(120deg,#365EB9,#5B30EE)  --li #0A66C2  --co #0056D2  --dg #6F8BD9 (DEC-6)
--r-card 22px --r-panel 16px --r-control 11px --r-chip 8px --r-button 10px  --maxw 1360px
```
Fonts: **pure system stack** (`-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,...`) - no web
fonts, no mono family; labels are 11px/700/uppercase/.04em, figures use `tabular-nums`. This fixed
the offline Courier fallback (v5/v6 loaded Google Fonts that fail offline). Aurora is a
`body::before` underlay (kit pattern), not blob divs. Source of truth: `~/repos/syniti-brand-kit`
(`tokens/tokens.css`, `patterns/patterns.css`). The retheme lives in `build/template.html`; the tool
is rebuilt from it.

### 4.2 Data layer (embedded JS consts - the crown jewels)
- `const COMPS = [...]` - the **78** competencies. Each: `{ref, area, t (title), d (desc),
  e:{C1,C2,C3,"C4-S","C4-M","C5-S","C5-M","C6-S","C6-M"}}` where `e` = expected 0-5 per level.
  (Injected by `build.py` from `data/competencies.json`, whose keys are `title/desc/exp`.)
- `const FRAMEWORK = {level: {role, headline, summary, dq, dqlab}}` - Career Framework reference
  text per C-level (from `sources/Syniti_Career_Framework_2024.pdf`). Reference only, not scored.
- `const LEARNING = {area: [ {p,t,m,u,d}, ... ], _meta:{...}}` - the learning repo.
  `p` = linkedin|coursera|degreed, `t` title, `m` meta, `u` url, `d` 1=verified course / 0=search.
- `const SCALE = [{lv:0,nm:"None"}...{lv:5,nm:"Expert"}]` - the 0-5 labels (convention).
- `const LEVELS = [...]` and `const LEVEL_LABEL = {...}` - C-levels and display names.
- `const AREAS = [...]` - ordered competency areas; core areas default-on, squads optional.
- Logo: a base64 PNG in `<img class="brandlogo" src="data:image/png;base64,...">`.

The `data/competencies.json` and `data/learning-catalog.json` mirror the embedded copies. To change
what the tool shows, edit the embedded consts (or edit the JSON and paste it over the const).

### 4.3 State
```
let state = { level, ratings:{ref:0-5}, na:{ref:bool}, scope:{area:bool},
              cmp:null (imported comparison), prov:"both", onlyGaps:true, plan:{} }
```
(`reviewMode` was removed with the AI section.)

### 4.4 JS function reference
- `renderScope()` - draws the area toggles (section 02).
- `renderMatrix()` - draws the competency tile grid grouped by area (section 04).
- `paintRow(c)` - repaints one competency's rating buttons + delta pill after a change.
- `recompute()` - recalculates stats, summary, classification suggestion; calls `renderLearning()`
  and `refreshPrompt()`. Central "on change" hub.
- `stats()` / `band()` / `deltaClass()` / `belowAreas()` - scoring + classification helpers.
- `expFor(c)` - expected rating for the selected level.
- `renderLearning()` - draws learning cards filtered by provider + gap toggle (section 04).
- `renderPlan()` - draws the development plan (items ticked "Add to plan").
- `renderFramework()` - fills the Career Framework reference panel for the selected level (section
  01), incl. the framework-to-matrix linkage sentence and `renderFwProfile()` (per-area expected-
  rating bars - the explicit skill <-> C-level expectation <-> Career Framework chain).
- `renderLadder()` / `ladderCellInfo()` - draws the section 05 Competency ladder and its ramp.
- `collect()` / `doExport()` - build and download the JSON evaluation form.
- `downloadComps()` - builds and downloads the competency list + per-level expectations as CSV.

(Removed with the AI section: `scopedComps`, `buildPrompt`, `refreshPrompt`, `copyPrompt`,
`applyAI`, `applyObj`, and the mode/notes handlers.)
- import handler - reads a prior JSON, accepts schema `syniti-skills-eval` **and** legacy
  `syniti-perf-assessment`, and shows per-row change.
- `setNav(open)` - toggles the left nav; IntersectionObserver highlights the active section.
- `card()` / `el()` / `toast()` - small DOM helpers.

### 4.5 Sections & DOM ids
**Five** cards, ids used by the nav + IntersectionObserver:
`#sec-overview` (01 Evaluation details & summary; hosts the Career Framework reference `#fwRef`
with the linkage sentence `#fwLink` and the per-area "Expected profile at this level" `#fwProfile`) -
`#sec-scope` (02 Scope) - `#sec-skills` (03 Skills evaluation + feedback) -
`#sec-learning` (04 Learning plan) - `#sec-ladder` (05 Competency ladder: the full 78 x 9 expected-
rating matrix grouped by area, columns headed by level code + Career Framework role, ordinal blue
intensity ramp, selected level's column highlighted; `renderLadder()` + `ladderCellInfo()`;
recomputed on level change). (`#sec-ai` was removed in v6.)

### 4.6 Export / import schema
`{ schema:"syniti-skills-eval", version:3, meta:{name,project,lead,level,type,date},
   ratings, na, feedback:{band,reco,proj,strengths,dev,pf}, plan, scope }`
Filename prefix on download: `Evaluation_`. Import is tolerant of the older schema name.

---

### 4.7 The Team Skills Summary sibling app (2026-07-17)

`tool/Syniti_Team_Skills_Summary.html` is a **standalone sibling file** - same skeleton, kit tokens
and system-font stack, its own script and state; hand-edited directly (no build step). It imports
many exported evaluation JSONs (schema `syniti-skills-eval`, legacy `syniti-perf-assessment`
accepted) and aggregates them.

Six sections: 01 Import (multi-select + drag-drop, per-file OK/error/duplicate rows; the section
auto-minimizes to a "N files - M consultants" chip after a successful import), 02 Team KPI summary
(a global **Filter by grade** tab row - C4-S/C4-M merge into "C4" - scopes the KPI tiles, band
chips, roster, heatmap, growth and the first two insights, with a "<grade> cohort" chip on every
filtered header; an **Insights** row: Top areas for improvement, Most severe skill gap, Cohort
watch - the last always whole-team), 03 Consultant roster (band badge, KPIs, trend arrow, "level
changed" chip), 04 Skills heatmap (consultants x 13 areas, cell = avg rating minus avg
expectation), 05 Team growth by area (dumbbell chart comparing each consultant's earliest vs
latest evaluation, averaged across the team; fair across promotions), 06 Drill-down (per-area
bars, material gaps, feedback, learning plan).

Aggregation: consultants keyed by normalized name; latest eval by date = current, prior feeds
trends. Team avg score / avg delta = equal-weight means over rated consultants; at/above = pooled;
gaps summed. `exportTeam()` downloads a whole-team `syniti-team-summary` v1 JSON incl. the growth
table. It embeds its **own copy of COMPS** (78, from `data/competencies.json`) because exports do
not carry expectations - keep in sync when the matrix changes (LIM-5). Test with `test-data/`
(import all 34; compare against `EXPECTED_RESULTS.md`).

---

## 5. How to make common changes (recipes)

- **Update the learning catalog** - edit `const LEARNING` (or `data/learning-catalog.json` then
  paste over the const). Provider `p`, title `t`, meta `m`, url `u`, verified flag `d`. See
  [[Learning catalog - how to update]].
- **Change the 0-5 scale wording** - edit `const SCALE`; also update `notes/Data model & rating scale`.
- **Add / edit competencies** - edit `const COMPS` (keep `e` expectations per level); regenerate
  `data/competencies.*` if you want the mirrors in sync.
- **Pin learning to a specific competency ref** (not just area) - add ref-keyed entries and extend
  `renderLearning()` to prefer a `ref` match before the area fallback. (Roadmap item.)
- **Re-theme** - change the CSS variables in `:root`; the gradient is `--grad`.
- **Add a section** - add a card with an `id="sec-..."`, add a `.navlink` in the sidenav, add the
  id to the IntersectionObserver `secIds` array.
- **Swap the logo** - replace the base64 in `<img class="brandlogo">`; keep it transparent PNG.

---

## 6. Data model & rating scale (summary)

**78** competencies across 13 areas (was 80; the AI area was restructured - see v6 note);
expectations are 0-5 per C-level, from the matrix sheet *REF - Compencies Master Data* (AI Enablement
values are provisional). Levels C1-C6 (Solution `-S` / Managing `-M` split at C4-C6);
**C7-C8 are not rated** (absent from the source). Scale: 0 None, 1 Awareness, 2 Working,
3 Competent, 4 Proficient, 5 Expert (labels are a **convention** the CoE confirmed for now; source
has numbers only). Full detail in [[Data model & rating scale]].

---

## 7. Design system & style references

Two references shaped the look: `sources/data-journey-map (style ref).html` (light glassmorphic
base - `#F6F8FE` field, aurora blobs, glass cards, blue->violet gradient, teal/amber accents) and
`sources/syniti-ai-acceleration (style ref).html` (Syniti typography: Space Grotesk / Inter /
JetBrains Mono). The tool merges the light glass base with Syniti type and the official logo.

---

## 8. Key decisions & rationale

- **Standalone HTML, no API key** - so it runs anywhere offline. Therefore the AI step is
  **"bring your own assistant"** (generate prompt -> paste into Copilot/Claude/ChatGPT -> paste JSON
  back), not a live API call. If this ever runs inside Claude/Claude Code, it could rate live.
- **Learning links must be real** - LinkedIn Learning and Coursera have public course pages
  (verified links carry `d:1`; topic/search entry points carry `d:0`). **Degreed is an enterprise
  LXP**: course URLs sit behind the org's SSO, so there are **no public deep links** - Degreed items
  resolve inside the Syniti Degreed tenant. This is why Coursera was briefly used in place of
  Degreed; Degreed is now back with tenant-resolving links.
- **Sections + hideable nav + icons** for scannability; Details+Summary merged so the top two
  blocks align (this also fixed the "line up" request directly). v5 had five sections; **v6 has four**
  (the AI Guided-review section was removed).
- **Formatting**: "-" hyphen, never the long dash; captured as a standing preference (section 10).
- Scale is a convention; C7-C8 unrated; the learning catalog is a single structured object so it can
  be deconstructed and curated later.

---

## 9. Build tooling (history + go-forward)

**Go-forward (v6):** one clean builder.
```
python3 build/build.py
```
It reads `data/competencies.json` (-> `const COMPS`, short keys), `data/learning-catalog.json`
(-> `const LEARNING`), and `build/template.html` (the shell, with the logo already embedded and two
placeholders `__COMPS__`/`__LEARNING__`), substitutes, guards against leftover placeholders and the
long dash, and writes `tool/Syniti_Skills_Evaluation_and_Enablement.html`. `data/*.json` are the
**single source of truth**; regenerate `data/competencies.csv` and `Competency Matrix (simplified).xlsx`
from `competencies.json` if you change competencies.

**History / why this exists:** v5 was built by a fragile chain `build2 -> build3 -> build4 ->
build_final.py` that applied `str_replace` edits to each other's *source*. `build_final.py` wrote the
*builder's* source to a `.html` name - which is why the v5 "tool" still had `__COMPS__` placeholders
and would not run. The whole chain (and the old `build/inputs/*`) is preserved under `build/legacy/`
and `build/build-scripts/` for reference only. **Do not extend it; use `build.py`.**

---

## 10. Formatting & deliverable preferences (standing)

- **Never use the long dash "-"**; use a plain hyphen "-".
- **PowerPoint deliverables**: slide size **33.87 cm wide x 19.05 cm high** (= 13.333 in x 7.5 in,
  standard 16:9). For python-pptx: `prs.slide_width = Cm(33.87); prs.slide_height = Cm(19.05)`.

---

## 11. Open issues

Tracked in [[issues|issues.md]]. Headlines: curate `d:0` links to verified courses; add Degreed
**tenant** URLs; optionally pin learning to competency refs; confirm official 0-5 scale wording;
decide the Projects-vs-Areas home for the data + catalog; optional team/heatmap roll-up and
per-rating evidence tooltips.

---

## 12. Suggested first tasks in Claude Code

1. Open `tool/...html`; confirm it runs; skim the `<script>` block against section 4.4.
2. Decide the data workflow: treat `data/*.json` as master and add a tiny re-embed step, or edit
   the embedded consts directly.
3. Knock out the highest-value issues: Degreed tenant links + curating `d:0` -> `d:1`.
4. If team-level reporting is wanted, design the multi-evaluation roll-up (issues.md).
