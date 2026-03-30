---
name: spec-review
description: Review a functional spec for clarity, completeness, user value, and implementation readiness at the contract level. Use when the user wants review feedback in ./docs/reviews/specs/{featurename}.md before planning.
---

# Spec Review

Use this skill to review an existing spec and write the coordinating result to `./docs/reviews/specs/{featurename}.md`.

Review the document as a functional product contract, not as an implementation plan.

Input:
- the feature spec at `./docs/specs/{featurename}.md`
- any product context or constraints that should stay in view

Requirements:
- derive `featurename` from the feature file name
- preserve the original spec file
- write the review artifact to `./docs/reviews/specs/{featurename}.md`
- update the current review file in place by default rather than creating numbered copies
- state the exact reviewed artifact path in the review artifact

Default reviewer perspectives:
- product owner
- architect
- scope-appropriate stakeholder or power-user personas

Review adaptation:
- choose reviewer personas based on artifact scope, risk, and affected surface area
- use fewer perspectives for narrow changes
- use broader perspectives for high-risk, user-facing, or cross-functional changes

Synthesize the result into:
- what works
- what is unclear or incomplete
- missing user-facing behavior
- details that should stay out of the spec and move to planning
- what should change before planning
- whether the spec is ready to advance

Finish with an explicit recommendation:
- `Recommendation: revise current stage`
- `Recommendation: ready to advance to plan-create`

The review recommendation informs the next decision, but the human or `workflow-run` decides whether to advance.
