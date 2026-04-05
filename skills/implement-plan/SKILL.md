---
name: implement-plan
description: Implement an approved engineering plan in bounded, validated steps. Use when the user wants to carry out a plan from ./docs/workflows/{slug}/plan.md.
---

# Implement Plan

Before implementing, inspect the repository root for `PLANS.md` and `AGENTS.md`.

Execution-plan mode:
- if the repository root contains `PLANS.md`, or if the repository's `AGENTS.md` says planning and implementation must use `PLANS.md`, treat that guidance as authoritative
- when that guidance is authoritative, operate in `execplan` mode
- when neither file requires `PLANS.md`, operate in `standard` mode
- `PLANS.md` is optional only when the project does not require it

Use this skill to carry out an approved plan from `./docs/workflows/{slug}/plan.md`.

This is an engineer-led implementation stage.

Requirements:
- the user or upstream workflow must name the workflow dossier to implement
- read the plan file before making changes
- treat `plan.md` as the primary living implementation document
- keep the plan current as a living document when implementation decisions, discoveries, or progress change it
- keep any execution summary in `./docs/workflows/{slug}/execution.md` if a run log is needed
- if an execution summary is written, link back to the source plan artifact path
- in `execplan` mode, do not require `run.md` to reconstruct implementation state
- in `execplan` mode, prefer recording substantive progress, decisions, discoveries, and validation in `plan.md`
- in `execplan` mode, use `execution.md` only as an optional evidence appendix when a separate run log is genuinely useful

Treat the spec as the source of truth for user-visible behavior, privacy, and correctness.

Treat the plan as the source of truth for sequencing and implementation approach:
- follow the ordered work items
- keep changes small and bounded
- stop if the plan is no longer valid
- once implementation starts in `execplan` mode, proceed milestone by milestone without asking for next steps unless a true blocker or explicit stage gate requires it

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
