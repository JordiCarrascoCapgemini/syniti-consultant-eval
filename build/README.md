---
tags: [dq-coe, evaluation, build, reference]
updated: 2026-07-04
---

# build/ - how the tool is produced

## The build (v6, current)

The runnable tool `tool/Syniti_Skills_Evaluation_and_Enablement.html` is **generated** by one clean
builder. To change the tool:

1. Edit content in `../data/competencies.json` and/or `../data/learning-catalog.json`, and/or the
   shell in `template.html`.
2. Run:

       python3 build/build.py        # from the project root

`build.py` reads:
- `../data/competencies.json`  -> `const COMPS` (converted to short keys `ref, area, t, d, e`)
- `../data/learning-catalog.json` -> `const LEARNING`
- `template.html` - the HTML/CSS/JS shell (logo already embedded; placeholders `__COMPS__`,
  `__LEARNING__`)

...substitutes, guards against leftover placeholders and the long dash, and writes `../tool/...html`.
**`../data/*.json` are the single source of truth. Do not hand-edit `../tool/...html`** - it is a
build artifact and will be overwritten. The `const FRAMEWORK` (Career Framework reference) currently
lives inline in `template.html`.

If you change competencies, also regenerate `../data/competencies.csv` and the root
`Competency Matrix (simplified).xlsx` from `competencies.json`.

## legacy/ and build-scripts/ (reference only - do NOT use)

The v5 tool was built by a fragile in-chat chain:

    build2.py  ->  build3.py  ->  build4.py  ->  build_final.py

Each read the previous builder's *source* and applied `str_replace` edits. `build_final.py` wrote the
*builder's* source to a `.html` name, which is why the v5 "tool" still contained `__COMPS__`
placeholders and would not open in a browser. The chain is kept in `build-scripts/`, and a copy of the
v5 builder-as-html in `legacy/`, purely as history. **Do not extend the chain; use `build.py`.**

## inputs/ (superseded)
`comps.json`, `comps_min.json`, `learning.json`, `logo_b64.txt` were the v5 build inputs. They are now
superseded by `../data/*.json` (content) and the logo embedded in `template.html`. Kept for reference.
