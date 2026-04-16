---
name: plan-create
description: Draft or refine the implementation-ready engineering plan as the Architect / Implementation Planner operator before plan-review. Use when the workflow needs `./docs/workflows/{slug}/plan.md`.
---

# Plan Create

Use this skill as the `Architect / Implementation Planner` operator playbook.

The operator owns drafting and updating `./docs/workflows/{slug}/plan.md`.

Requirements:
- derive `slug` from the workflow dossier or source spec
- update the existing plan in the dossier instead of creating duplicates
- link to the source spec artifact path in the plan body
- keep the plan self-contained enough that a later engineer can resume from the plan plus the repository without needing `run.md`
- make clear near the top what changes for the user or system and how successful delivery will be observed
- keep the permanent artifact concise and skimmable by default
- treat `./docs/workflows/{slug}/plan.md` as the authoritative execution plan for the workflow
- repo-local `PLANS.md` may be read as optional project context, but it must not replace this workflow's plan structure, stage contract, or execution control unless the user explicitly asks for repo-native planning mode
- treat the plan as a living document and keep these sections current:
  - `Progress`
  - `Surprises & Discoveries`
  - `Decision Log`
  - `Outcomes & Retrospective`
- define non-obvious terms in plain language instead of assuming prior repo knowledge
- when revising after `plan-review`, fold accepted review decisions back into `plan.md`
- when the plan is ready for execution, mark that state clearly in the plan body

Operator responsibility:
- draft the source artifact for later review
- do not try to review or approve your own work
- leave material objections for `plan-review`

Use the spec to define what must be true for users. Use the plan to define how engineering will achieve it.

Decision rule:
- if a missing detail affects user-visible behavior, privacy, or correctness, stop and send it back to the spec
- if a missing detail is only needed for implementation, decide it in the plan
- if the plan would introduce a new architectural direction, major architectural constraint, or a new third-party service, SDK, hosted platform, or external tool, treat that as materially important and route it back through the orchestrator for clarification or approval when needed
- when unsure, do not backfill product discovery into the plan; push unclear user-facing contract questions back to the spec

Write the plan with sections like:
- title
- source spec
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

Style rule:
- focus on decisions, sequencing, interfaces, validation, and recovery
- prefer compact bullets or short prose blocks over long explanatory narrative
- avoid restating the same intent, dependency, or risk in multiple sections unless the repetition materially improves implementation safety

Require these expectations:
- the plan must be restartable from `plan.md` plus the repository alone
- treat restartability as a hard requirement
- `Progress`, `Decision Log`, `Surprises & Discoveries`, `Validation and Acceptance`, and `Outcomes & Retrospective` are mandatory living sections
- validation should include concrete commands or checks with expected observable outcomes when the project permits them
- accepted review outcomes must be incorporated into the plan before implementation begins

Do not:
- restate product policy unless the spec is ambiguous
- mix in brainstorming
- begin implementation
- silently repair product-contract gaps that should have been clarified in the spec
- expand straightforward decisions into essay-style rationale unless the tradeoff is non-obvious or high risk

The output of this stage should be ready for `plan-review`.
