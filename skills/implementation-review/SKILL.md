---
name: implementation-review
description: Review implemented code and execution evidence using architecture, security, and QA/product-correctness reviewer lenses before final-review. Use when the user wants review output in ./docs/workflows/{slug}/reviews/implementation/round-01.md after implementation.
---

# Implementation Review

Use this skill to review the implemented change after `implement-plan` and write the next review round to `./docs/workflows/{slug}/reviews/implementation/round-XX.md`.

This is a consolidated implementation review. The active orchestrator should gather findings from the required reviewer subagents and write one official review round.

Use [assets/review-template.md](./assets/review-template.md) as the default saved review-round skeleton. Adapt sections as needed for the actual findings and recommendation.

Input:
- the implemented change, diff, or implementation summary
- `./docs/workflows/{slug}/plan.md`
- `./docs/workflows/{slug}/spec.md`
- `./docs/workflows/{slug}/idea.md` when needed for fidelity context
- `./docs/workflows/{slug}/execution.md` when present
- validation output that should stay in view

Requirements:
- derive `slug` from the workflow dossier
- preserve the source artifacts
- write the next review round to `./docs/workflows/{slug}/reviews/implementation/round-XX.md`
- create a new zero-padded round file for each pass rather than overwriting earlier rounds
- list the exact reviewed artifact paths in the review artifact
- link the immediately prior implementation-review round when one exists and summarize what changed since that round
- use exactly these three reviewer personas:
  - `Software Architect`
  - `Security Engineer`
  - `QA Engineer`
- treat the QA Engineer as responsible for:
  - user-visible correctness
  - regressions
  - edge cases
  - test realism
  - unit-test coverage expectations
- keep the saved review artifact concise and findings-first
- preserve meaningful disagreement when one or more of the three reviewer lenses is not satisfied

Focus on:
- architectural soundness against the approved plan
- security risks, trust boundaries, unsafe defaults, secrets handling, authz/authn issues, and abuse paths when relevant
- product correctness against spec and plan
- regressions and missing edge-case coverage
- sufficiency of validation and unit tests
- accidental complexity or implementation drift that added layers, abstractions, or dependencies beyond the approved need
- whether the delivered shape remains easy for the next engineer to follow and change safely
- the strongest reasons not to proceed to final-review yet

Write the review artifact with sections like:
- reviewed artifacts
- prior implementation review rounds when relevant
- reviewer lenses
- review scope
- key findings
- meaningful disagreements
- suggested revisions
- recommendation
- outstanding dissent

Compression rule:
- merge overlapping findings when multiple reviewer lenses point to the same underlying issue
- avoid repeating the same critique across lenses
- summarize validation or test concerns into clear actionable gaps rather than long transcripts

Finish with an explicit recommendation:
- `Recommendation: revise implement-plan`
- `Recommendation: implementation ready for final-review`

Do not exit this phase as ready until architecture, security, and QA / product correctness all support proceeding.
