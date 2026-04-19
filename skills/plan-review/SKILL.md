---
name: plan-review
description: Review an engineering plan using two substantive reviewer subagents plus one skeptic before implementation. Use when the workflow needs review output in ./docs/workflows/{slug}/reviews/plan/round-01.md.
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
- make clear that the reviewers are subagents and the active session writes the consolidated official review round
- identify each reviewer in the roster with persona, concrete agent name, and subagent display name when the runtime exposes one
- preserve a brief reviewer-by-reviewer synopsis so the saved artifact retains some color from what each subagent actually said

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

Write the review artifact with sections like:
- reviewed artifact
- prior review rounds when relevant
- reviewer roster
- review scope
- reviewer synopses
- key findings
- meaningful disagreements
- suggested revisions
- recommendation
- outstanding dissent

Compression rule:
- merge overlapping findings across reviewers
- avoid repeating the same critique reviewer by reviewer
- preserve only the disagreements that materially affect the recommendation
- keep each reviewer synopsis brief and high-signal rather than turning the artifact into a transcript
- if the repo markdown artifacts are not sufficient to continue safely, state that as a key finding rather than creating a separate restartability section

Finish with an explicit recommendation:
- `Recommendation: revise current stage`
- `Recommendation: ready to advance to implement-plan`

The recommendation informs the next decision, but the orchestrator and user decide whether to advance.
