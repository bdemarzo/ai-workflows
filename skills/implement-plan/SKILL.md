---
name: implement-plan
description: Implement an approved engineering plan in bounded, validated steps. Use when the user wants to carry out a plan from ./docs/workflows/{slug}/plan.md.
---

# Implement Plan

Use this skill to carry out an approved plan from `./docs/workflows/{slug}/plan.md`.

This is an engineer-led implementation stage.

Requirements:
- the user or upstream workflow must name the workflow dossier to implement
- read the plan file before making changes
- treat `plan.md` as the primary living implementation document
- keep the plan current as a living document when implementation decisions, discoveries, or progress change it
- keep any execution summary in `./docs/workflows/{slug}/execution.md` if a run log is needed
- if an execution summary is written, link back to the source plan artifact path
- when this workflow skill is active, follow `./docs/workflows/{slug}/plan.md` as the authoritative implementation control document for the workflow
- repo-local `PLANS.md` may be read as optional project context, but it must not replace this workflow's plan, stage contract, or execution control unless the user explicitly asks for repo-native planning mode

Treat the spec as the source of truth for user-visible behavior, privacy, and correctness.

Treat the plan as the source of truth for sequencing and implementation approach:
- follow the ordered work items
- keep changes small and bounded
- stop if the plan is no longer valid
- proceed milestone by milestone without asking for next steps unless a true blocker or explicit stage gate requires it

During implementation:
- make the minimum change required for each step
- run the repo-approved validation for the change
- record any deviation from the plan
- update the plan's living sections when implementation discoveries materially change the work
- do not invent product behavior during implementation
- if the plan needs to change for engineering reasons, update the plan
- if the user contract needs to change, update the spec first
- if implementation reveals a need for a new architectural direction, major architectural constraint, or a new third-party service, SDK, hosted platform, or external tool:
  - in fully autonomous orchestration, make the best justified choice and record it in the plan and run ledger
  - otherwise treat it as a blocking question before adopting it
- if the workflow guidelines specify a Git commit policy, follow it carefully:
  - only commit workflow-related files
  - do not include unrelated changes
  - make sure the plan and run ledger reflect the current state before the commit
- treat review rounds as historical justification and design input, not as active execution control documents

When you keep `execution.md`, use sections like:
- title
- source plan
- status
- implementation summary
- progress or work log
- validation evidence
- deviations from plan
- files changed
- current blockers
- follow-up work
- outcomes

Finish with:
- files changed
- tests or checks run
- any deviations from the plan
- remaining follow-up work, if any

The output of this stage should be ready for `final-review`.
