---
name: plan-review
description: Perform peer review of an engineering plan from architectural and engineering perspectives across the relevant parts of the stack. Use when the user wants review feedback in ./docs/workflows/{slug}/reviews/plan/round-01.md before implementation.
---

# Plan Review

Use this skill to review an engineering plan and produce evidence and a recommendation about whether it is ready for implementation.

Input:
- the plan at `./docs/workflows/{slug}/plan.md`
- any technical context or constraints that should stay in view

Requirements:
- derive `slug` from the workflow dossier
- preserve the original plan file
- write the next review round to `./docs/workflows/{slug}/reviews/plan/round-XX.md`
- create a new zero-padded round file for each pass rather than overwriting earlier rounds
- state the exact reviewed artifact path in the review artifact
- link the immediately prior review round when one exists and summarize what changed since that round
- structure the review as a stakeholder debate that still ends in an actionable recommendation

Default reviewer perspectives:
- engineer
- technical product manager

Review adaptation:
- choose reviewer personas based on artifact scope, risk, and affected surface area
- include additional architectural or domain-specific personas when the plan scope requires it
- use a smaller reviewer set for narrow changes
- when the plan includes meaningful UI, UX, accessibility, responsive behavior, or front-end interaction work, include an explicit UX, design-system, or front-end experience perspective

Focus on:
- implementation sequencing
- full-stack coverage
- architectural soundness
- validation realism
- missing assumptions or risky gaps
- front-end interaction, accessibility, state, or responsive-delivery risks when relevant
- whether the plan is self-contained enough for a later engineer to implement it safely

Write the review artifact with sections like:
- reviewed artifact
- prior review rounds when relevant
- participants
- review scope
- opening positions
- debate
- points of agreement
- points of disagreement
- suggested revisions
- recommendation
- outstanding dissent

Finish with an explicit recommendation:
- `Recommendation: revise current stage`
- `Recommendation: ready to advance to implement-plan`

The review recommendation informs the next decision, but the human or `workflow-run` decides whether to advance.
