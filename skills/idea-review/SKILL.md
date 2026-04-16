---
name: idea-review
description: Review an idea artifact using two substantive reviewer subagents plus one skeptic before spec creation. Use when the workflow needs review output in ./docs/workflows/{slug}/reviews/idea/round-01.md.
---

# Idea Review

Use this skill as the review playbook for the idea phase.

The active session should orchestrate the reviewer subagents required for the current workflow mode and write one official consolidated review round.

Input:
- the idea artifact at `./docs/workflows/{slug}/idea.md`
- product context or constraints that should stay in view

Reviewer roster:
- `Stakeholder Value Reviewer`
- `UX / Product Design Reviewer` or `Domain Reviewer`
- `Skeptic`

Requirements:
- derive `slug` from the workflow dossier
- preserve the original idea file
- write the next review round to `./docs/workflows/{slug}/reviews/idea/round-XX.md`
- create a new zero-padded round file for each pass rather than overwriting earlier rounds
- state the exact reviewed artifact path in the review artifact
- link the immediately prior review round when one exists and summarize what changed since that round
- in `standard` and `heavy`, use exactly two substantive reviewers plus one skeptic
- in `light`, use one substantive reviewer plus one skeptic
- in `light`, choose the substantive reviewer by dominant risk:
  - `Stakeholder Value Reviewer` by default
  - `UX / Product Design Reviewer` when the idea is meaningfully user-facing and interaction-heavy
  - `Domain Reviewer` when domain constraints dominate
- keep the saved review artifact concise and findings-first
- make clear that the reviewers are subagents and the active session writes the consolidated official review round

Focus on:
- value and user relevance
- whether the idea is worth pursuing
- whether success signals are observable enough to justify advancing
- whether the artifact is self-contained enough for spec creation
- major UX / workflow risks when relevant
- the strongest reasons not to advance yet

Write the review artifact with sections like:
- reviewed artifact
- prior review rounds when relevant
- reviewer roster
- review scope
- self-containment assessment
- observability of value
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
- `Recommendation: ready to advance to spec-create`

The recommendation informs the next decision, but the orchestrator and user decide whether to advance.
