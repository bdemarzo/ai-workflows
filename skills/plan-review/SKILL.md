---
name: plan-review
description: Perform peer review of an engineering plan from architectural and engineering perspectives across the relevant parts of the stack. Use when the user wants review feedback in ./docs/reviews/plans/{planname}.md before implementation.
---

# Plan Review

Use this skill to review an engineering plan and produce evidence and a recommendation about whether it is ready for implementation.

Input:
- the plan at `./docs/plans/{planname}.md`
- any technical context or constraints that should stay in view

Requirements:
- derive `planname` from the plan file name
- preserve the original plan file
- write the review artifact to `./docs/reviews/plans/{planname}.md`
- update the current review file in place by default rather than creating numbered copies
- state the exact reviewed artifact path in the review artifact

Default reviewer perspectives:
- engineer
- technical product manager

Review adaptation:
- choose reviewer personas based on artifact scope, risk, and affected surface area
- include additional architectural or domain-specific personas when the plan scope requires it
- use a smaller reviewer set for narrow changes

Focus on:
- implementation sequencing
- full-stack coverage
- architectural soundness
- validation realism
- missing assumptions or risky gaps

Finish with an explicit recommendation:
- `Recommendation: revise current stage`
- `Recommendation: ready to advance to implement-plan`

The review recommendation informs the next decision, but the human or `workflow-run` decides whether to advance.
