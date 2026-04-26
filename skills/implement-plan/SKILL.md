---
name: implement-plan
description: Implement or remediate an approved `./docs/workflows/{slug}/plan.md` as the Software Engineer operator using bounded validated code changes, optional execution evidence, and handoff to implementation-review.
---

# Implement Plan

Use this skill as the `Software Engineer` operator playbook.

The operator owns implementation work after the plan has been approved.

When `execution.md` is useful, use [assets/execution-template.md](./assets/execution-template.md) as the default output skeleton. Adapt sections as needed, but preserve the slugged title format.

## Inputs And Source Of Truth

- Work from an identified workflow dossier.
- Read `./docs/workflows/{slug}/plan.md` before changing code.
- Treat `plan.md` as the authoritative implementation control document.
- Treat `spec.md` as the source of truth for user-visible behavior, privacy, and correctness.
- Treat review rounds as historical design input, not active execution control documents.

## Implementation Boundary

- follow the ordered work in `plan.md`
- keep changes small and bounded
- do not invent product behavior during implementation
- stop if the plan is no longer valid or a contract ambiguity materially affects correctness
- ask the orchestrator to get user clarification when blocked
- if user-visible behavior must change, send the change back through the spec before continuing
- if engineering realities require an implementation change but the product contract still holds, update `plan.md`

## Execution Discipline

- make the minimum change required for the current approved step
- run repo-appropriate validation for the change
- keep `plan.md` current when material discoveries, decisions, or deviations change the work
- route new architectural direction, major constraints, or third-party dependencies back through the orchestrator unless already authorized by the approved plan
- if a Git commit policy exists in the workflow guidelines, follow it carefully

## Evidence And Handoff

- use `./docs/workflows/{slug}/execution.md` when implementation has more than one approved step, multiple validation commands, remediation rounds, material validation, deviations, blockers, or follow-up evidence
- when `execution.md` is used, start it with the exact H1 `# Execution - {slug}`
- keep evidence concise; do not paste long logs, transcripts, or repeated plan/spec content
- record changed areas, checks run, failures fixed, deviations from the plan, and the next handoff
- keep `plan.md` as the implementation control document, not a detailed execution journal
- when implementation review sends remediation back, the same Software Engineer operator owns the fix pass and hands off again to `implementation-review`

## Progress Checks

When the orchestrator asks for implementation progress, respond with a compact status instead of continuing silently:
- current task/file or subsystem
- completed changes
- active blocker, if any
- expected time to handoff
- whether a partial handoff is available now

If blocked or unable to finish within the expected window, say so directly and identify the cleanest handoff point.

The output of this stage should be ready for `implementation-review`, not directly for `final-review`.
