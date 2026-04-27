---
name: plan-review
description: Review `./docs/workflows/{slug}/plan.md` before implementation using two substantive reviewer subagents plus one skeptic. Use when validating implementation readiness, architecture simplicity, restartability, or whether the workflow can advance to `implement-plan`, and write output to `./docs/workflows/{slug}/reviews/plan/round-XX.md`.
---

# Plan Review

Use this skill as the review playbook for the plan phase.

The active session should orchestrate the required reviewer subagents and write one official consolidated review round.

Use [assets/review-template.md](./assets/review-template.md) as the default saved review-round skeleton. Adapt sections as needed for the actual findings and recommendation.

Input:
- the plan at `./docs/workflows/{slug}/plan.md`
- technical context or constraints that should stay in view

Reviewer roster:
- `Software Architect`
- `Software Engineer`
- `Skeptic`

Requirements:
- derive `slug` from the workflow dossier
- preserve the original plan file
- write the next review round to `./docs/workflows/{slug}/reviews/plan/round-XX.md`
- create a new zero-padded round file for each pass rather than overwriting earlier rounds
- state the exact reviewed artifact path in the review artifact
- link the immediately prior review round when one exists and summarize what changed since that round
- use exactly two substantive reviewers plus one skeptic
- keep the saved review artifact concise and findings-first
- validate that each official reviewer matches the resolved role binding from `workflow-run`
- identify each reviewer with persona, concrete agent name, and display name when the runtime exposes one
- preserve a one-sentence reviewer-by-reviewer synopsis of each subagent's main point
- omit empty boilerplate sections from the saved artifact when they would only say `None`
- keep saved rounds compact unless material findings require more

Focus on:
- implementation sequencing
- full-stack coverage
- architectural soundness
- validation realism
- risky assumptions or missing gaps
- whether the markdown artifacts in the repo are sufficient for a later operator to continue to `implement-plan` without chat history
- whether the plan chooses the simplest viable architecture that satisfies the spec
- whether every proposed layer, service, abstraction, dependency, and integration is justified by the current need
- whether the plan reuses existing repository patterns before inventing new architecture
- whether the plan introduces repetition, split responsibility, or indirection that could be collapsed without losing clarity
- the strongest reasons not to advance yet

Reviewer input:
- ask each reviewer for up to three consequential findings, one explicit recommendation, and only the rationale needed to support that recommendation
- merge overlapping findings, keep synopses brief, and preserve only disagreements that materially affect the recommendation
- if the repo markdown artifacts are not sufficient to continue safely, state that as a key finding
- for focused re-reviews, ask reviewers to inspect only the prior finding, current artifact, and changed area

Finish with an explicit recommendation:
- `Recommendation: revise current stage`
- `Recommendation: ready to advance to implement-plan`

The recommendation informs the next decision, but the orchestrator and user decide whether to advance.
