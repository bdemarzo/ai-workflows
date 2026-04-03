---
name: plan-create
description: Turn an approved spec into an implementation-ready engineering plan. Use when the user wants to create or refine a plan in ./docs/workflows/{slug}/plan.md.
---

# Plan Create

Before planning, inspect the repository root for `PLANS.md` and `AGENTS.md`.

Execution-plan mode:
- if the repository root contains `PLANS.md`, or if the repository's `AGENTS.md` says planning and implementation must use `PLANS.md`, treat that guidance as authoritative
- when that guidance is authoritative, operate in `execplan` mode
- when neither file requires `PLANS.md`, operate in `standard` mode
- `PLANS.md` is optional only when the project does not require it

Use this skill to produce an implementation-ready plan in `./docs/workflows/{slug}/plan.md`.

This is an architect-led creation stage.

Requirements:
- derive `slug` from the workflow dossier or source spec
- update the existing plan in the dossier instead of creating duplicates
- link to the source spec artifact path in the plan body
- keep the plan self-contained enough that a later engineer can resume from the plan plus the repository without needing `run.md`
- make clear near the top what changes for the user or system and how successful delivery will be observed
- treat the plan as a living document and keep these sections current as the plan changes:
  - `Progress`
  - `Surprises & Discoveries`
  - `Decision Log`
  - `Outcomes & Retrospective`
- define non-obvious terms in plain language instead of assuming prior repo knowledge
- in `execplan` mode, treat `./docs/workflows/{slug}/plan.md` as the repository's executable plan for this workflow, not just a supporting artifact
- in `execplan` mode, ensure the plan is strong enough to serve as the primary implementation control document once implementation starts
- when revising after `plan-review`, fold accepted review decisions back into `plan.md` so implementation-critical details do not remain stranded in review rounds
- when the plan is ready for execution, mark that state clearly in the plan body

Use the spec to define what must be true for users. Use the plan to define how engineering will achieve it.

Decision rule:
- if a missing detail affects user-visible behavior, privacy, or correctness, stop and send it back to the spec
- if a missing detail is only needed for implementation, decide it in the plan

Write the plan in prose-first form with sections like:
- title
- source spec
- execution plan mode
- status
- purpose / big picture
- observable success framing
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

In `execplan` mode, require these expectations:
- the plan must be restartable from `plan.md` plus the repository alone
- treat restartability from `plan.md` plus the repository alone as a hard requirement, not a nice-to-have
- `Progress`, `Decision Log`, `Surprises & Discoveries`, `Validation and Acceptance`, and `Outcomes & Retrospective` must be treated as mandatory living sections
- validation must include concrete commands or checks with expected observable outcomes when the project permits them
- accepted review outcomes must be incorporated into the plan before implementation begins

Do not:
- restate product policy unless the spec is ambiguous
- mix in brainstorming
- begin implementation

The output of this stage should be ready for `plan-review`.
