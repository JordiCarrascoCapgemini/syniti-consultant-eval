---
title: syniti-dq-consultant-evaluation — Project Brief
tags: [project, consultant-eval, brief]
created: 2026-07-06
status: active
---

# Project · Skills Evaluation & Enablement (Consultant Evaluation)

**Repo:** [truwaynegordon/syniti-consultant-eval](https://github.com/truwaynegordon/syniti-consultant-eval) · **Local:** this folder is the live clone (`.git` present, in sync with `origin/main`)

A standalone single-file HTML tool for EMEA DQ CoE delivery leads to evaluate a consultant against competency expectations for their C-level, classify performance, capture feedback, and map targeted learning to close gaps. Works fully offline — no server, no network, no API key.

Full detail lives in this same folder — **read [`HANDOFF.md`](HANDOFF.md) first**, then [`issues.md`](issues.md). Vault-side binding: [[Binding — Consultant Evaluation]].

## Installation

There isn't one — that's the point. Open [`tool/Syniti_Skills_Evaluation_and_Enablement.html`](tool/Syniti_Skills_Evaluation_and_Enablement.html) directly in any browser. To change it, edit `data/*.json` or `build/template.html`, then run `python3 build/build.py` to regenerate the tool file (see `README.md`).

**Checked 2026-07-06** against the sibling apps' portable-Windows-bundle work: this app is **exempt** for the same reason as [[Binding — Business Outcomes Activation|BOA]] — it's already a zero-install single-file artifact. See [[Portable Distribution]].

## Backlog

Source of truth is [`issues.md`](issues.md) in this folder (decisions needed, known limitations, enhancement backlog) — not duplicated here.

## Related

- [[Binding — Consultant Evaluation]] · [[Portable Distribution]]
- [[App Bindings MOC]]
