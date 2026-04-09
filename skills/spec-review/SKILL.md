---
name: spec-review
description: Review a functional spec for clarity, completeness, user value, and implementation readiness at the contract level. Use when the user wants review feedback in ./docs/workflows/{slug}/reviews/spec/round-01.md before planning.
---

# Spec Review

Use this skill to review an existing spec and write the coordinating result to `./docs/workflows/{slug}/reviews/spec/round-XX.md`.

Review the document as a functional product contract, not as an implementation plan.

Input:
- the feature spec at `./docs/workflows/{slug}/spec.md`
- any product context or constraints that should stay in view

Requirements:
- derive `slug` from the workflow dossier
- preserve the original spec file
- write the next review round to `./docs/workflows/{slug}/reviews/spec/round-XX.md`
- create a new zero-padded round file for each pass rather than overwriting earlier rounds
- state the exact reviewed artifact path in the review artifact
- link the immediately prior review round when one exists and summarize what changed since that round
- structure the review as a stakeholder debate that still ends in an actionable recommendation
- have reviewers form independent opening positions before converging on a recommendation
- include at least one explicitly skeptical or risk-focused perspective that tries to find reasons the current spec should not advance
- when the spec is non-trivial or user-facing, include at least one perspective that compares it against industry-standard patterns and how similar successful products or applications handle comparable requirements
- explicitly check whether planning can proceed from the current `spec.md` alone without relying on prior review rounds
- explicitly check whether accepted prior review feedback appears to have been folded back into the latest `spec.md`

Default reviewer perspectives:
- product owner
- architect
- scope-appropriate stakeholder or power-user personas

Review adaptation:
- choose reviewer personas based on artifact scope, risk, and affected surface area
- use fewer perspectives for narrow changes
- use broader perspectives for high-risk, user-facing, or cross-functional changes
- when the workflow includes meaningful UI, UX, navigation, or interaction behavior, include an explicit UX or product-design perspective
- for user-facing features, treat that UX or product-design perspective as expected rather than optional
- do not optimize for reviewer consensus; preserve strong dissent when important contract risks remain
- when using comparable products or best-practice references, use them to identify missing behavior, states, constraints, or acceptance expectations

Synthesize the result into:
- what works
- what is unclear or incomplete
- missing user-facing behavior
- missing interaction detail, interface states, navigation clarity, accessibility expectations, or UX edge cases when relevant
- missing boundary conditions or edge cases that affect correctness
- where the contract falls short of industry-standard patterns or comparable successful products when relevant
- the strongest reasons not to advance yet
- whether acceptance criteria are observable enough to drive planning
- whether the current spec is restartable enough for `plan-create` from the artifact alone
- details that should stay out of the spec and move to planning
- where the reviewers disagree
- what should change before planning
- whether the spec is ready to advance

Write the review artifact with sections like:
- reviewed artifact
- prior review rounds when relevant
- participants
- review scope
- contract restartability
- observable acceptance assessment
- incorporation of prior accepted feedback
- opening positions
- benchmark and best-practice comparison when relevant
- debate
- points of agreement
- points of disagreement
- suggested revisions
- recommendation
- outstanding dissent

Finish with an explicit recommendation:
- `Recommendation: revise current stage`
- `Recommendation: ready to advance to plan-create`

The review recommendation informs the next decision, but the human or `workflow-run` decides whether to advance. The recommendation should make clear whether `plan-create` can proceed from the current `spec.md` without rereading historical review rounds.
