---
name: implement-plan
description: Carry out an approved engineering plan as the expert engineer operator, in bounded validated steps, before handing the result to implementation-review. Use when the user wants to implement `./docs/workflows/{slug}/plan.md`.
---

# Implement Plan

Use this skill as the `Expert Engineer` operator playbook.

The operator owns implementation work after the plan has been approved.

Requirements:
- the workflow dossier to implement must already be identified
- read `./docs/workflows/{slug}/plan.md` before making changes
- treat `plan.md` as the authoritative implementation control document for the workflow
- keep the plan current as a living document when implementation discoveries or decisions materially change the work
- use `./docs/workflows/{slug}/execution.md` only when an evidence appendix or work log is genuinely useful
- treat `spec.md` as the source of truth for user-visible behavior, privacy, and correctness
- treat review rounds as historical design input, not as active execution control documents
- when implementation review sends remediation back, the same expert engineer operator owns the fix pass

Operator responsibilities:
- follow the ordered work in `plan.md`
- keep changes small and bounded
- stop if the plan is no longer valid
- ask the orchestrator to get user clarification when a blocker or contract ambiguity materially affects correctness
- do not invent product behavior during implementation
- if engineering realities require a plan change, update `plan.md`
- if user-visible behavior must change, send the change back through the spec before continuing

During implementation:
- make the minimum change required for the current step
- run repo-appropriate validation
- record deviations from the plan
- update the plan's living sections when discoveries materially change the work
- if implementation reveals a new architectural direction, major architectural constraint, or new third-party dependency:
  - treat that as materially important
  - route it back through the orchestrator for clarification or approval unless it is already clearly authorized by the approved plan
- if a Git commit policy exists in the workflow guidelines, follow it carefully

When you keep `execution.md`, use sections like:
- title
- source plan
- status
- implementation summary
- validation evidence
- deviations from plan
- files changed
- blockers
- follow-up work

Finish with:
- files changed
- tests or checks run
- deviations from the plan
- remaining follow-up work

The output of this stage should be ready for `implementation-review`, not directly for `final-review`.
