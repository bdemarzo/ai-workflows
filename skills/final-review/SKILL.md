---
name: final-review
description: Run final fidelity review against implemented behavior, idea/spec/plan alignment, validation and regression gaps, unresolved implementation drift, and docs close-out readiness. Use before workflow closure, and write output to `./docs/workflows/{slug}/reviews/final/round-XX.md`.
---

# Final Review

Use this skill as the final fidelity-review playbook; the active session synthesizes reviewer critique into one official review round.

Use [assets/review-template.md](./assets/review-template.md) as the default saved review-round skeleton. Adapt sections as needed for the actual findings and recommendation.

Input:
- the implemented change, diff, or implementation summary
- the relevant `idea.md`, `spec.md`, and `plan.md`
- the latest implementation-review round
- `execution.md` when present
- validation output that should stay in view

Reviewer roster:
- `Product Manager` or `Product Strategist`
- `Software Architect`
- `QA Engineer`

Requirements:
- derive `slug` from the workflow dossier being reviewed
- write the next review round to `./docs/workflows/{slug}/reviews/final/round-XX.md`
- create a new zero-padded round file for each pass rather than overwriting earlier rounds
- do not overwrite the source artifacts
- list the exact reviewed artifact paths in the review artifact
- link the immediately prior final-review round when one exists and summarize what changed since that round
- keep the reviewer roster explicit in the saved artifact
- keep the saved review artifact concise and findings-first
- focus on fidelity, regressions, and unresolved gaps rather than rerunning all prior stage debate
- identify each reviewer with persona, concrete agent name, and display name when the runtime exposes one
- validate that each official reviewer matches the resolved role binding from `workflow-run`
- preserve a brief reviewer-by-reviewer synopsis so the saved artifact retains some color from what each subagent actually said

Focus on:
- fidelity of code and delivered behavior against `idea.md`, `spec.md`, and `plan.md`
- unresolved correctness gaps, regressions, and validation gaps
- places where implementation drifted from the approved artifact chain
- whether the delivered solution stayed simple and the repo markdown artifacts support docs close-out without chat history
- the strongest reasons not to begin docs close-out yet

Reviewer budget:
- ask each reviewer for up to three consequential findings, one explicit recommendation, and only the rationale needed to support that recommendation
- merge overlapping findings, keep synopses brief, and preserve only disagreements that materially affect closure readiness
- summarize validation or regression concerns as actionable gaps rather than long transcripts
- if the repo markdown artifacts are not sufficient to continue safely, state that as a key finding

Finish with an explicit recommendation:
- `Recommendation: loop back to implement-plan`
- `Recommendation: loop back to plan-create`
- `Recommendation: loop back to spec-create`
- `Recommendation: loop back to idea-create`
- `Recommendation: ready for docs close-out`

The recommendation informs the next decision, but the orchestrator and user decide whether to reroute, continue remediation, or begin close-out. This phase checks readiness for docs close-out; it does not perform docs close-out or close the workflow.
