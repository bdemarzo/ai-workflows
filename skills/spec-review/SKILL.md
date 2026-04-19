---
name: spec-review
description: Review a spec artifact using two substantive reviewer subagents plus one skeptic before plan creation. Use when the workflow needs review output in ./docs/workflows/{slug}/reviews/spec/round-01.md.
---

# Spec Review

Use this skill as the review playbook for the spec phase.

The active session should orchestrate the required reviewer subagents and write one official consolidated review round.

Input:
- the spec artifact at `./docs/workflows/{slug}/spec.md`
- product context or constraints that should stay in view

Reviewer roster:
- `Software Architect`
- `Stakeholder Advocate` or `Product Designer`
- `Skeptic`

Requirements:
- derive `slug` from the workflow dossier
- preserve the original spec file
- write the next review round to `./docs/workflows/{slug}/reviews/spec/round-XX.md`
- create a new zero-padded round file for each pass rather than overwriting earlier rounds
- state the exact reviewed artifact path in the review artifact
- link the immediately prior review round when one exists and summarize what changed since that round
- use exactly two substantive reviewers plus one skeptic
- explicitly check whether planning can proceed from the current `spec.md` alone
- explicitly check whether accepted review feedback has been folded back into the latest `spec.md`
- keep the saved review artifact concise and findings-first
- make clear that the reviewers are subagents and the active session writes the consolidated official review round

Focus on:
- completeness of the user-facing contract
- missing behavior, states, constraints, or edge cases
- whether acceptance criteria are observable enough to drive planning
- whether the current spec is restartable enough for `plan-create`
- whether the spec is shaping the smallest sufficient solution rather than quietly requiring speculative architecture
- whether the spec is accidentally prescribing implementation detail that belongs in the plan
- what should stay out of the spec and move to the plan
- the strongest reasons not to advance yet

Write the review artifact with sections like:
- reviewed artifact
- prior review rounds when relevant
- reviewer roster
- review scope
- contract restartability
- observable acceptance assessment
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
- `Recommendation: ready to advance to plan-create`

The recommendation informs the next decision, but the orchestrator and user decide whether to advance.
