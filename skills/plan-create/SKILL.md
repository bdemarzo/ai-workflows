---
name: plan-create
description: Turn an approved spec into an implementation-ready engineering plan. Use when the user wants to create or refine a plan in ./docs/workflows/{slug}/plan.md.
---

# Plan Create

Before planning, read the repository root `PLANS.md` if it exists and follow its instructions for how plans should be created and structured. Treat `PLANS.md` as supplementary repo-local guidance only. Its absence is normal and must not block planning.

Use this skill to produce an implementation-ready plan in `./docs/workflows/{slug}/plan.md`.

This is an architect-led creation stage.

Requirements:
- derive `slug` from the workflow dossier or source spec
- update the existing plan in the dossier instead of creating duplicates
- link to the source spec artifact path in the plan body
- keep the plan self-contained enough that a later engineer can resume from the plan plus the repository
- treat the plan as a living document and keep these sections current as the plan changes:
  - `Progress`
  - `Surprises & Discoveries`
  - `Decision Log`
  - `Outcomes & Retrospective`
- define non-obvious terms in plain language instead of assuming prior repo knowledge

Use the spec to define what must be true for users. Use the plan to define how engineering will achieve it.

Decision rule:
- if a missing detail affects user-visible behavior, privacy, or correctness, stop and send it back to the spec
- if a missing detail is only needed for implementation, decide it in the plan

Write the plan in prose-first form with sections like:
- title
- source spec
- status
- purpose / big picture
- progress
- surprises & discoveries
- decision log
- outcomes & retrospective
- context and orientation
- plan of work
- milestones when useful
- concrete steps
- validation and acceptance
- idempotence and recovery
- interfaces and dependencies
- open questions
- revision history

Do not:
- restate product policy unless the spec is ambiguous
- mix in brainstorming
- begin implementation

The output of this stage should be ready for `plan-review`.
