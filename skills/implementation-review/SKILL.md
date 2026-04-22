---
name: implementation-review
description: Review implemented code, diffs, execution evidence, and validation sufficiency with architecture, security, and QA/product-correctness reviewer lenses. Use when deciding whether implementation can advance to final-review, and write output to `./docs/workflows/{slug}/reviews/implementation/round-XX.md`.
---

# Implementation Review

Use this skill to review the implemented change after `implement-plan`; the active orchestrator gathers reviewer findings and writes one official round to `./docs/workflows/{slug}/reviews/implementation/round-XX.md`.

Use [assets/review-template.md](./assets/review-template.md) as the default saved review-round skeleton. Adapt sections as needed for the actual findings and recommendation.

Input:
- the implemented change, diff, or implementation summary
- `./docs/workflows/{slug}/plan.md`
- `./docs/workflows/{slug}/spec.md`
- `./docs/workflows/{slug}/idea.md` when needed for fidelity context
- `./docs/workflows/{slug}/execution.md` when present
- validation output that should stay in view

Reviewer roster:
- `Software Architect`
- `Security Engineer`
- `QA Engineer`

Requirements:
- derive `slug` from the workflow dossier
- preserve the source artifacts
- write the next review round to `./docs/workflows/{slug}/reviews/implementation/round-XX.md`
- create a new zero-padded round file for each pass rather than overwriting earlier rounds
- list the exact reviewed artifact paths in the review artifact
- link the immediately prior implementation-review round when one exists and summarize what changed since that round
- use exactly the three reviewer personas in the roster
- treat QA as responsible for user-visible correctness, regressions, edge cases, test realism, and unit-test coverage expectations
- keep the saved review artifact concise, findings-first, and clear about meaningful disagreement
- identify each reviewer with persona, concrete agent name, and display name when the runtime exposes one
- validate that each official reviewer matches the resolved role binding from `workflow-run`
- preserve a brief reviewer-by-reviewer synopsis so the saved artifact retains some color from what each subagent actually said
- omit empty boilerplate sections from the saved artifact when they would only say `None`
- keep normal saved rounds around 250-500 words unless material findings require more

Focus on:
- architectural soundness against the approved plan
- security risks, trust boundaries, unsafe defaults, secrets handling, authz/authn issues, and abuse paths when relevant
- product correctness against spec and plan
- regressions, edge-case coverage, validation sufficiency, and unit tests
- accidental complexity or implementation drift that added layers, abstractions, or dependencies beyond the approved need
- whether the delivered shape and repo markdown artifacts are easy for a later operator to continue without chat history
- the strongest reasons not to proceed to final-review yet

Reviewer budget:
- ask each reviewer for up to three consequential findings, one explicit recommendation, and only the rationale needed to support that recommendation
- merge overlapping findings, keep synopses brief, and preserve only disagreements that materially affect the recommendation
- summarize validation or test concerns as actionable gaps rather than long transcripts
- if the repo markdown artifacts are not sufficient to continue safely, state that as a key finding
- group reviewed code paths by subsystem when many files were touched; rely on `execution.md` for exact changed-file evidence
- for focused re-reviews, ask reviewers to inspect only the prior finding, current diff/evidence, and changed area

Finish with an explicit recommendation:
- `Recommendation: revise implement-plan`
- `Recommendation: implementation ready for final-review`

Do not exit this phase as ready until architecture, security, and QA / product correctness all support proceeding; this phase does not perform final fidelity review or documentation close-out.
