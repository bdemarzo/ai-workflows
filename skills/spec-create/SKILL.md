---
name: spec-create
description: Draft, revise, or update the functional product contract as the Product Manager operator before spec-review. Use when turning an approved idea into `./docs/workflows/{slug}/spec.md`, updating an existing spec, or incorporating accepted spec-review feedback before planning.
---

# Spec Create

Use this skill as the `Product Manager` operator playbook.

The operator owns drafting and updating `./docs/workflows/{slug}/spec.md`.

Use [assets/template.md](./assets/template.md) as the default output skeleton when creating a new artifact. Adapt sections as needed, but preserve the slugged title format.

Write a functional product contract, not an execution plan.

Input can be:
- an approved idea from the prompt
- an existing spec file that should be refined in place
- an idea artifact at `./docs/workflows/{slug}/idea.md`

Requirements:
- derive `slug` from the prompt or workflow dossier
- create the file if it does not exist
- update the file in place if it already exists
- preserve the dossier slug unless the workflow intentionally splits into a new dossier
- start the artifact with the exact H1 `# Spec - {slug}`
- keep the spec self-contained enough for planning without relying on prior thread context
- make the spec concrete enough that planning can proceed from `spec.md` alone
- keep the permanent artifact concise and skimmable by default
- avoid copying idea rationale into the spec when a short source link or summary is enough
- link back to the source idea artifact path when the spec was created from one
- if a workflow split created this dossier, explain that relationship in the spec body
- include local tracking with:
  - `Source Idea`
  - `Status`
  - `Open Questions`
  - `Revision History`
- incorporate accepted review outcomes into the spec so `spec.md` remains the current contract
- retain useful revision history when updating an existing artifact
- keep the spec as the source of truth for user-visible behavior, scope, and correctness

Operator responsibility:
- draft the source artifact for later review
- do not try to review or approve your own work
- leave material objections for `spec-review`

Spec boundary:
- `spec.md` defines the user-visible contract: behavior, scope, constraints, privacy and business rules, routes or URLs when relevant, acceptance criteria, scenarios, edge cases, and observable acceptance behavior
- `plan.md` owns sequencing, task breakdown, code structure, file/module lists, implementation mechanics, migration steps, detailed execution logs, and validation commands
- `execution.md` owns implementation evidence and validation results after work begins
- when a detail reads like implementation mechanics, move it out of the spec unless it changes user-visible outcomes, privacy, or correctness

Decision rule:
- if a detail is only needed so engineering can implement it, leave it for the plan
- if it changes user expectations, privacy, or correctness, keep it in the spec
- when unsure, preserve the user-facing contract and leave engineering mechanics unresolved
- if a short requirement list, example list, or table is enough, do not expand it into long prose

Before finalizing `spec.md`, perform a scope check:
- remove or simplify sections that read like `plan of work`, `milestones`, `concrete steps`, `module ownership`, `file lists`, `dependency rollout`, `migration sequence`, or `validation commands`
- convert prematurely specific implementation detail into:
  - a product-facing constraint or requirement if it truly affects user expectations, privacy, or correctness, or
  - an `Open Questions` item to be decided in planning
- compress repeated examples, requirement restatements, or rationale when one clear statement is sufficient
- keep acceptance criteria observable but compact; do not duplicate every functional requirement as a second full list unless that improves planning safety

The output of this stage should be ready for `spec-review`.
