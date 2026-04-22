---
name: idea-review
description: Review an idea artifact using two substantive reviewer subagents plus one skeptic before spec creation. Use when the workflow needs review output in ./docs/workflows/{slug}/reviews/idea/round-01.md.
---

# Idea Review

Use this skill as the review playbook for the idea phase.

The active session should orchestrate the required reviewer subagents and write one official consolidated review round.

Use [assets/review-template.md](./assets/review-template.md) as the default saved review-round skeleton. Adapt sections as needed for the actual findings and recommendation.

Input:
- the idea artifact at `./docs/workflows/{slug}/idea.md`
- product context or constraints that should stay in view

Reviewer roster:
- `Stakeholder Advocate`
- `Product Designer` or `Domain Expert`
- `Skeptic`

Requirements:
- derive `slug` from the workflow dossier
- preserve the original idea file
- write the next review round to `./docs/workflows/{slug}/reviews/idea/round-XX.md`
- create a new zero-padded round file for each pass rather than overwriting earlier rounds
- state the exact reviewed artifact path in the review artifact
- link the immediately prior review round when one exists and summarize what changed since that round
- use exactly two substantive reviewers plus one skeptic
- keep the saved review artifact concise and findings-first
- make clear that the reviewers are subagents and the active session writes the consolidated official review round
- identify each reviewer in the roster with persona, concrete agent name, and subagent display name when the runtime exposes one
- validate that each official reviewer matches the resolved role binding from `workflow-run`
- preserve a brief reviewer-by-reviewer synopsis so the saved artifact retains some color from what each subagent actually said

Focus on:
- value and user relevance
- whether the idea is worth pursuing
- whether success signals are observable enough to justify advancing
- whether the markdown artifacts in the repo are sufficient for a later operator to continue to `spec-create` without chat history
- major UX / workflow risks when relevant
- the strongest reasons not to advance yet

Write the review artifact with sections like:
- reviewed artifact
- prior review rounds when relevant
- reviewer roster
- review scope
- reviewer synopses
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
- keep each reviewer synopsis brief and high-signal rather than turning the artifact into a transcript
- keep reviewer inputs compact: ask each reviewer for up to three consequential findings, one explicit recommendation, and only the rationale needed to support that recommendation
- keep each reviewer within their assigned lens and avoid duplicating another lens unless the disagreement changes the recommendation
- if the repo markdown artifacts are not sufficient to continue safely, state that as a key finding rather than creating a separate restartability section

Finish with an explicit recommendation:
- `Recommendation: revise current stage`
- `Recommendation: ready to advance to spec-create`

The recommendation informs the next decision, but the orchestrator and user decide whether to advance.
