---
tags: [dq-coe, enablement, learning, howto]
updated: 2026-07-02
---

# Learning catalog - how to update

The learning suggestions are a **curatable repo**. Master copy: `data/learning-catalog.json`.

## Structure
Keyed by competency **area**; each entry is one learning item:

```json
"DQ-Specific Functional": [
  { "p": "linkedin", "t": "Learning Data Governance",
    "m": "Course - 1h 24m - Beginner",
    "u": "https://www.linkedin.com/learning/learning-data-governance-14224082", "d": 1 }
]
```

| field | meaning |
|-------|---------|
| `p` | provider: `linkedin`, `coursera`, or `degreed` |
| `t` | title shown on the card |
| `m` | meta line (duration / level / type) |
| `u` | link. `linkedin`/`coursera` are public URLs; `degreed` resolves inside your Degreed tenant |
| `d` | `1` = verified deep link to a specific course; `0` = provider search/topic entry point |

## Provider notes
- **LinkedIn Learning / Coursera** - public course pages exist; verified links have `d:1`,
  topic/search entry points have `d:0`. Curate `d:0` items to specific courses over time.
- **Degreed** - enterprise LXP; course URLs sit behind SSO, so there are no public deep links.
  Point `u` at your Degreed tenant's course/pathway URLs when you have them.

## To update the live tool
The tool embeds its own copy of this catalog. To change what the tool shows:
1. Edit `data/learning-catalog.json` (the master).
2. Open `tool/Syniti_Skills_Evaluation_and_Enablement.html`, find the line beginning
   `const LEARNING = {...};` and replace the object with the new JSON (minified is fine).
3. Save. (Ask the build owner to regenerate if you would rather not hand-edit.)

## Future: pin learning to a specific competency
Today the catalog maps to **areas**. To map to an individual competency `ref`
(e.g. a course pinned to `A3 - DQ Dev: SQL View`), add ref-keyed entries and extend the tool's
`renderLearning()` to prefer a `ref` match before falling back to the area. Logged in [[Roadmap]].
