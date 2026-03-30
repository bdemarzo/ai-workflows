---
name: idea-review
description: Review a product idea for value, feasibility, and user relevance. Use when the user wants review feedback in ./docs/reviews/ideas/{topic}.md before turning an idea into a spec.
---

# Idea Review

Use this skill to review an idea artifact and produce evidence and a recommendation about whether it is ready for spec creation.

Input:
- the idea artifact at `./docs/ideas/{topic}.md`
- any product context or constraints that should stay in view

Requirements:
- derive `topic` from the idea file name
- preserve the original idea file
- write the review artifact to `./docs/reviews/ideas/{topic}.md`
- update the current review file in place by default rather than creating numbered copies
- state the exact reviewed artifact path in the review artifact

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
- what should change before spec creation
- whether the idea is ready to advance

Finish with an explicit recommendation:
- `Recommendation: revise current stage`
- `Recommendation: ready to advance to spec-create`

The review recommendation informs the next decision, but the human or `workflow-run` decides whether to advance.
