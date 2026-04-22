---
name: spec-review
description: Review `./docs/workflows/{slug}/spec.md` using two substantive reviewer subagents plus one skeptic before plan creation. Use when validating the functional product contract, observable acceptance, readiness for `plan-create`, or whether the workflow can advance, and write output to `./docs/workflows/{slug}/reviews/spec/round-XX.md`.
---

# Spec Review

Use this skill as the review playbook for the spec phase.

The active session should orchestrate the required reviewer subagents and write one official consolidated review round.

Use [assets/review-template.md](./assets/review-template.md) as the default saved review-round skeleton. Adapt sections as needed for the actual findings and recommendation.

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
- explicitly check whether accepted review outcomes have been incorporated into the latest `spec.md`
- keep the saved review artifact concise and findings-first
- validate that each official reviewer matches the resolved role binding from `workflow-run`
- identify each reviewer with persona, concrete agent name, and display name when the runtime exposes one
- preserve a brief reviewer-by-reviewer synopsis so the saved artifact retains some color from what each subagent actually said

Focus on:
- completeness of the user-facing contract
- missing behavior, states, constraints, or edge cases
- whether acceptance criteria are observable enough to drive planning
- whether the markdown artifacts in the repo are sufficient for a later operator to continue to `plan-create` without chat history
- whether the spec is shaping the smallest sufficient solution rather than quietly requiring speculative architecture
- whether the spec is accidentally prescribing implementation detail that belongs in the plan
- what should stay out of the spec and move to the plan
- the strongest reasons not to advance yet

Reviewer budget:
- ask each reviewer for up to three consequential findings, one explicit recommendation, and only the rationale needed to support that recommendation
- merge overlapping findings, keep synopses brief, and preserve only disagreements that materially affect the recommendation
- if the repo markdown artifacts are not sufficient to continue safely, state that as a key finding

Finish with an explicit recommendation:
- `Recommendation: revise current stage`
- `Recommendation: ready to advance to plan-create`

The recommendation informs the next decision, but the orchestrator and user decide whether to advance.
