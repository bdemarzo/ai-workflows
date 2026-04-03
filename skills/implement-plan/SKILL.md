---
name: implement-plan
description: Implement an approved engineering plan in bounded, validated steps. Use when the user wants to carry out a plan from ./docs/workflows/{slug}/plan.md.
---

# Implement Plan

Before implementing, read the repository root `PLANS.md` if it exists and follow its instructions for how plans should be used and implemented. Treat `PLANS.md` as supplementary repo-local guidance only. Its absence is normal and must not block implementation.

Use this skill to carry out an approved plan from `./docs/workflows/{slug}/plan.md`.

This is an engineer-led implementation stage.

Requirements:
- the user or upstream workflow must name the workflow dossier to implement
- read the plan file before making changes
- keep the plan current as a living document when implementation decisions, discoveries, or progress change it
- keep any execution summary in `./docs/workflows/{slug}/execution.md` if a run log is needed
- if an execution summary is written, link back to the source plan artifact path

Treat the spec as the source of truth for user-visible behavior, privacy, and correctness.

Treat the plan as the source of truth for sequencing and implementation approach:
- follow the ordered work items
- keep changes small and bounded
- stop if the plan is no longer valid

During implementation:
- make the minimum change required for each step
- run the repo-approved validation for the change
- record any deviation from the plan
- update the plan's living sections when implementation discoveries materially change the work
- do not invent product behavior during implementation
- if the plan needs to change for engineering reasons, update the plan
- if the user contract needs to change, update the spec first

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
