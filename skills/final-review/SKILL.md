---
name: final-review
description: Run an orchestrator-led fidelity review against the idea, spec, plan, implementation, and validation chain before docs close-out and workflow closure.
---

# Final Review

Use this skill as the final fidelity-review playbook.

The active session owns the final synthesis. Reviewer subagents provide critique, but the active session writes the official review round and coordinates gap resolution with the user.

Use [assets/review-template.md](./assets/review-template.md) as the default saved review-round skeleton. Adapt sections as needed for the actual findings and recommendation.

Input:
- the implemented change, diff, or implementation summary
- the relevant `idea.md`, `spec.md`, and `plan.md`
- the latest implementation-review round
- `execution.md` when present
- validation output that should stay in view

Expected reviewer roster:
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
- identify each reviewer in the roster with persona, concrete agent name, and subagent display name when the runtime exposes one
- validate that each official reviewer matches the resolved role binding from `workflow-run`
- preserve a brief reviewer-by-reviewer synopsis so the saved artifact retains some color from what each subagent actually said

Focus on:
- fidelity of code and delivered behavior against `idea.md`, `spec.md`, and `plan.md`
- unresolved correctness gaps
- regressions and validation gaps
- places where implementation drifted from the approved artifact chain
- whether the delivered solution stayed appropriately simple and avoided unjustified architectural expansion during execution
- what must still be fixed before docs close-out and closure

Write the review artifact with sections like:
- reviewed artifacts
- prior review rounds when relevant
- reviewer roster
- review scope
- reviewer synopses
- key findings
- meaningful disagreements
- suggested revisions
- recommendation
- outstanding dissent

Compression rule:
- merge overlapping findings across reviewer lenses
- avoid repeating the same critique in multiple voices
- keep only the disagreements that materially affect closure readiness
- keep each reviewer synopsis brief and high-signal rather than turning the artifact into a transcript
- keep reviewer inputs compact: ask each reviewer for up to three consequential findings, one explicit recommendation, and only the rationale needed to support that recommendation
- keep each reviewer within their assigned lens and avoid duplicating another lens unless the disagreement changes the recommendation

Finish with an explicit recommendation:
- `Recommendation: loop back to implement-plan`
- `Recommendation: loop back to plan-create`
- `Recommendation: loop back to spec-create`
- `Recommendation: loop back to idea-create`
- `Recommendation: ready for docs close-out`

The recommendation informs the next decision, but the orchestrator and user decide whether to reroute, continue remediation, or begin close-out.
