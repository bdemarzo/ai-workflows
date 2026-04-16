---
name: plan-review
description: Review an engineering plan using two substantive reviewer subagents plus one skeptic before implementation. Use when the workflow needs review output in ./docs/workflows/{slug}/reviews/plan/round-01.md.
---

# Plan Review

Use this skill as the review playbook for the plan phase.

The active session should orchestrate the reviewer subagents required for the current workflow mode and write one official consolidated review round.

Input:
- the plan at `./docs/workflows/{slug}/plan.md`
- technical context or constraints that should stay in view

Reviewer roster:
- `Senior Engineer Reviewer`
- `Delivery / Systems Reviewer` or `Frontend Delivery Reviewer`
- `Skeptic`

Requirements:
- derive `slug` from the workflow dossier
- preserve the original plan file
- write the next review round to `./docs/workflows/{slug}/reviews/plan/round-XX.md`
- create a new zero-padded round file for each pass rather than overwriting earlier rounds
- state the exact reviewed artifact path in the review artifact
- link the immediately prior review round when one exists and summarize what changed since that round
- in `standard` and `heavy`, use exactly two substantive reviewers plus one skeptic
- in `light`, use one substantive reviewer plus one skeptic
- in `light`, choose the substantive reviewer by dominant risk:
  - `Senior Engineer Reviewer` by default
  - `Delivery / Systems Reviewer` for integration or operationally sensitive work
  - `Frontend Delivery Reviewer` for UI-heavy delivery risk
- keep the saved review artifact concise and findings-first
- make clear that the reviewers are subagents and the active session writes the consolidated official review round

Focus on:
- implementation sequencing
- full-stack coverage
- architectural soundness
- validation realism
- risky assumptions or missing gaps
- whether the plan is self-contained enough for a later engineer to implement safely
- the strongest reasons not to advance yet

Write the review artifact with sections like:
- reviewed artifact
- prior review rounds when relevant
- reviewer roster
- review scope
- key findings
- meaningful disagreements
- suggested revisions
- recommendation
- outstanding dissent

Compression rule:
- merge overlapping findings across reviewers
- avoid repeating the same critique reviewer by reviewer
- preserve only the disagreements that materially affect the recommendation

Finish with an explicit recommendation:
- `Recommendation: revise current stage`
- `Recommendation: ready to advance to implement-plan`

The recommendation informs the next decision, but the orchestrator and user decide whether to advance.
