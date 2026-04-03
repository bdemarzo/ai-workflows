---
name: idea-review
description: Review a product idea for value, feasibility, and user relevance. Use when the user wants review feedback in ./docs/workflows/{slug}/reviews/idea/round-01.md before turning an idea into a spec.
---

# Idea Review

Use this skill to review an idea artifact and produce evidence and a recommendation about whether it is ready for spec creation.

Input:
- the idea artifact at `./docs/workflows/{slug}/idea.md`
- any product context or constraints that should stay in view

Requirements:
- derive `slug` from the workflow dossier
- preserve the original idea file
- write the next review round to `./docs/workflows/{slug}/reviews/idea/round-XX.md`
- create a new zero-padded round file for each pass rather than overwriting earlier rounds
- state the exact reviewed artifact path in the review artifact
- link the immediately prior review round when one exists and summarize what changed since that round
- structure the review as a stakeholder debate that still ends in an actionable recommendation

Default reviewer perspectives:
- key stakeholders
- power users
- technical product manager

Review adaptation:
- choose reviewer personas based on artifact scope, risk, and affected surface area
- use fewer perspectives for narrow or exploratory ideas
- use broader perspectives for high-risk, user-facing, or cross-functional ideas

Synthesize the result into:
- what works
- concerns about value or user relevance
- feasibility or scope concerns
- where the stakeholders disagree
- what should change before spec creation
- whether the idea is ready to advance

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
- `Recommendation: ready to advance to spec-create`

The review recommendation informs the next decision, but the human or `workflow-run` decides whether to advance.
