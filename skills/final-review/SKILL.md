---
name: final-review
description: Review the full workflow outcome for architectural quality, product correctness, process fit, and contract fidelity. Use when the user wants review output in ./docs/reviews/finals/{artifactname}.md after implementation.
---

# Final Review

Use this skill to review the full workflow outcome after implementation and write the review artifact to `./docs/reviews/finals/{artifactname}.md`.

Input:
- the implemented change, diff, or implementation summary
- the relevant idea, spec, and plan files
- the execution summary when present
- any validation output that should stay in view

Requirements:
- derive `artifactname` from the canonical slug or `planname` being reviewed rather than inventing a freeform name
- write the review artifact to `./docs/reviews/finals/{artifactname}.md`
- update the current review file in place by default rather than creating numbered copies
- do not overwrite the source artifacts
- list the exact reviewed artifact paths in the review artifact

Default reviewer perspectives:
- architect
- product owner
- technical product manager

Review adaptation:
- choose reviewer personas based on artifact scope, risk, and affected surface area
- use fewer perspectives for narrow, low-risk changes
- use broader perspectives for high-risk, user-facing, cross-functional, or process-sensitive changes

Focus on:
- fidelity across the idea, spec, plan, implementation, and validation chain
- architectural quality
- product correctness
- fit against the intended contract
- process fit and traceability gaps
- regressions and edge cases
- insufficient validation

Finish with an explicit recommendation:
- `Recommendation: loop back to idea-create`
- `Recommendation: loop back to spec-create`
- `Recommendation: loop back to plan-create`
- `Recommendation: loop back to implement-plan`
- `Recommendation: workflow outcome ready`

The review recommendation informs the next decision, but the human or `workflow-run` decides whether to advance, reroute, or stop.
