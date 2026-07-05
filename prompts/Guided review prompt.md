---
tags: [dq-coe, evaluation, ai, prompt, deprecated]
updated: 2026-07-04
---

> **DEPRECATED (v6, 2026-07-04).** The AI "Guided review" section was removed from the tool at the
> CoE's request. The tool no longer generates or accepts this prompt. Kept only as a historical
> record of the v4/v5 copy-paste review flow.

# Guided review prompt (historical)

In v4/v5 the tool **generated this prompt dynamically** from the scoped competencies and the selected
C-level. It is reproduced here for reference only. It is no longer wired into the tool.

## Template (interview mode)
```
You are helping a Syniti delivery lead assess a consultant for a project performance review.

CONSULTANT LEVEL: <C-level> (<label>). Judge performance against the expectation for THIS
level, not against perfection.

RATING SCALE (integers 0-5):
  0 = None
  1 = Awareness
  2 = Working
  3 = Competent
  4 = Proficient
  5 = Expert

COMPETENCIES TO ASSESS  (ref | competency | expected level | meaning):
  <ref> | <competency> | expected <n> | <description>
  ...   (only the areas the lead scoped)

TASK: Interview me to gather evidence. Ask a short, focused set of questions (about 6-10,
grouped by theme) covering the competencies above - keep it a quick back-and-forth. When you
have enough to judge, produce the assessment.

OUTPUT: when ready, reply with ONLY this JSON inside a single code block, no other text:
```
```json
{
  "ratings": { "<ref>": 3 },
  "na": [],
  "classification": "meets",
  "recommendation": "On track at level",
  "strengths": "",
  "development": "",
  "projectFeedback": ""
}
```
```
Rules: use ONLY the refs listed; ratings are integers 0-5; be evidence-based and do not inflate;
when writing development, compare each rating to its expected level.
```

## Notes mode
Same as above, but instead of interviewing, the prompt includes the lead's free-text notes and
asks the assistant to rate from those, listing any un-evidenced competency in `na`.

## Paste-back
The tool tolerantly extracts the JSON (handles code fences and surrounding text), applies only
valid competency refs, clamps ratings to 0-5, fills classification + narrative, and auto-enables
any area that received ratings.
