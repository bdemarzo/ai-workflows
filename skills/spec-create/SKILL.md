---
name: spec-create
description: Turn an approved idea into a functional product contract. Use when the user wants to create or refine the feature spec in ./docs/workflows/{slug}/spec.md.
---

# Spec Create

Use this skill to create or update the feature spec at `./docs/workflows/{slug}/spec.md`.

This is a technical-product-manager-led creation stage.

Write a functional product contract, not an execution plan.

The input can be either:
- an approved idea from the prompt
- an existing feature spec file that should be refined in place
- an idea artifact at `./docs/workflows/{slug}/idea.md`

Requirements:
- derive `slug` from the prompt or workflow dossier
- create the file if it does not exist
- update the file in place if it already exists
- keep the spec self-contained enough for planning without relying on prior thread context
- make the spec concrete enough that planning can proceed from `spec.md` alone without mining prior review rounds
- keep the permanent artifact concise and skimmable by default; preserve extra detail only when it materially changes the product contract, a constraint, or restartability
- link back to the source idea artifact path when the spec was created from one
- if a workflow split created this dossier, explain that relationship in the spec body
- include rich local tracking in the artifact with:
  - `Source Idea`
  - `Status`
  - `Open Questions`
  - `Revision History`
- fold accepted review decisions back into the spec so the latest `spec.md` is the current contract
- keep the spec as the source of truth for user-visible behavior, scope, and correctness
- prefer leaving engineering implementation detail unresolved rather than prematurely turning the spec into a plan

Stage boundary rule:
- `spec.md` should define what must be true for the user and product, not how engineering will implement it
- the spec should be concrete about behavior, correctness, scope, and constraints, but should stop short of execution design
- when a detail starts to read like sequencing, work packages, code structure, architecture decision records, integration mechanics, migration steps, or validation command lists, stop and move that detail out of the spec

Keep these details in the spec:
- user-visible behavior
- scope
- constraints
- privacy rules
- business rules
- user-facing routes or URLs
- acceptance criteria
- concrete user-facing scenarios or examples
- boundary conditions and edge cases that affect correctness
- observable acceptance behavior, not only abstract acceptance language
- compact structure over essay-style explanation; prefer bullets or tables when they communicate the contract more clearly

Do not put these details in the spec:
- implementation sequencing
- task breakdown
- file or module lists
- detailed execution logs
- migration mechanics unless they change user-visible outcomes

Decision rule:
- if a detail is only needed so engineering can implement it, leave it for the plan
- if it changes user expectations, privacy, or correctness, keep it in the spec
- when unsure, bias toward preserving the user-facing contract and leave engineering mechanics unresolved
- if a short requirement, example list, or table is enough, do not expand it into long prose

Write the spec with sections like:
- title
- source idea
- status
- summary
- context and orientation when needed
- problem statement
- goals
- non-goals
- target users
- key scenarios or user flows
- functional requirements
- constraints and guardrails
- boundary conditions and edge cases
- privacy rules, business rules, and user-facing routes or URLs when relevant
- acceptance criteria
- observable acceptance behavior or examples
- open questions
- revision history

Before finalizing `spec.md`, perform a scope check:
- remove or simplify sections that read like `plan of work`, `milestones`, `concrete steps`, `module ownership`, `file lists`, `dependency rollout`, `migration sequence`, or `validation commands`
- convert prematurely specific implementation detail into either:
  - a product-facing constraint or requirement if it truly affects user expectations, privacy, or correctness, or
  - an `Open Questions` item to be decided in planning
- compress repeated examples, requirement restatements, or rationale when one clear statement is sufficient

The output of this stage should be ready for `spec-review`.
