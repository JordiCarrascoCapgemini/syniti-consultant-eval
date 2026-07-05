---
tags: [dq-coe, evaluation, reference]
updated: 2026-07-04
---

# Data model & rating scale

## Source of truth
- Competencies + per-level expectations come from the **EMEA DQ Common Competency Matrix**
  (`sources/EMEA_DQ_Common_Competency_Matrix.xlsm`, sheet *REF - Compencies Master Data*).
- Career levels and progression context come from the **Global Consulting Career Framework**
  (`sources/Syniti_Career_Framework_2024.pdf`).
- Extracted machine-readable copies live in `data/competencies.json` and `data/competencies.csv`.

## Competency record
Each of the **78** competencies (was 80 before the v6 AI restructure) is:

```json
{ "ref": "A1", "area": "Syniti Platform: Technical (ADM)",
  "t": "Data Prep: Collect", "d": "short description",
  "e": { "C1":1, "C2":2, "C3":3, "C4-S":3, "C4-M":3, "C5-S":4, "C5-M":4, "C6-S":5, "C6-M":5 } }
```

- `e` holds the **expected rating (0-5) per C-level**. The matrix covers C1-C6, split into
  Solution (`-S`) and Managing (`-M`) tracks at C4-C6. C7-C8 are not rated in the source.

## Competency areas (13)
Core (on by default): DQ-Specific Technical, DQ-Specific Functional, SAP Data Functional,
Delivery & Consulting.
Squads / specialist (optional): Delivery Excellence, dqOps, Harmonization, Source Cleansing,
Cloud Data Quality, Dashboarding & Analytics, **AI Enablement**, plus the two
Syniti Platform (ADM / ADM-M) technical areas.

### AI Enablement (v6, was "Squad-Specialized and AI Driven")
Three competencies, **expected values provisional - confirm with the CoE** (DEC-5):
- `G31` General AI Knowledge & Day-to-Day Use
- `G32` AI-Augmentation: Development Acceleration
- `G33` AI-Augmentation: Delivery & Consulting Quality

Removed in v6: old `G33` Syniti AI-Generated Rule Content, `G34` Syniti Vision, `G35` Syniti Classify.

### Career Framework reference
`const FRAMEWORK` (in the tool) maps each C-level to its role headline, expectation narrative, and
Data Quality / track focus, extracted from `sources/Syniti_Career_Framework_2024.pdf`. It is a
**reference** shown in section 01 to justify the level expectation - not part of the score. Note the
framework splits tracks at C5/C6 (Managing vs Solution); the tool's C4-S and C4-M both map to the
single "Lead Consultant (C4)".

## Rating scale (0-5)
| 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| None | Awareness | Working | Competent | Proficient | Expert |

The matrix stores expectations as 0-5 numbers with no written legend; the labels above are the
convention used by the tool. If the CoE adopts official wording, update it in the tool and here.

## Derived metrics
- **Delta to level** = rating - expected. `>=0` met, `<=-2` material gap, otherwise slightly under.
- **Classification** suggested from average delta: exceeds (>= +0.5), meets (>= -0.25 and no gaps),
  partially meets (>= -1), else below. The lead can override.
