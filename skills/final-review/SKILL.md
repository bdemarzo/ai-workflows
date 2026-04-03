---
name: final-review
description: Review the full workflow outcome for architectural quality, product correctness, process fit, and contract fidelity. Use when the user wants review output in ./docs/workflows/{slug}/reviews/final/round-01.md after implementation.
---

# Final Review

Use this skill to review the full workflow outcome after implementation and write the next review round to `./docs/workflows/{slug}/reviews/final/round-XX.md`.

Input:
- the implemented change, diff, or implementation summary
- the relevant idea, spec, and plan files
- the execution summary when present
- the run ledger when present
- any validation output that should stay in view

Requirements:
- derive `slug` from the workflow dossier being reviewed
- write the next review round to `./docs/workflows/{slug}/reviews/final/round-XX.md`
- create a new zero-padded round file for each pass rather than overwriting earlier rounds
- do not overwrite the source artifacts
- list the exact reviewed artifact paths in the review artifact
- link the immediately prior final-review round when one exists and summarize what changed since that round
- structure the review as a stakeholder debate that still ends in an actionable recommendation

Default reviewer perspectives:
- architect
- product owner
- technical product manager

Review adaptation:
- choose reviewer personas based on artifact scope, risk, and affected surface area
- use fewer perspectives for narrow, low-risk changes
- use broader perspectives for high-risk, user-facing, cross-functional, or process-sensitive changes

Focus on:
- fidelity across the idea, spec, plan, implementation, execution, and validation chain
- architectural quality
- product correctness
- fit against the intended contract
- process fit and traceability gaps
- regressions and edge cases
- insufficient validation

Write the review artifact with sections like:
- reviewed artifacts
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
- `Recommendation: loop back to idea-create`
- `Recommendation: loop back to spec-create`
- `Recommendation: loop back to plan-create`
- `Recommendation: loop back to implement-plan`
- `Recommendation: workflow outcome ready`

The review recommendation informs the next decision, but the human or `workflow-run` decides whether to advance, reroute, or stop.
