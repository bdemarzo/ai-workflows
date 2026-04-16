---
name: idea-create
description: Draft or refine the idea artifact as the Product Strategist operator before idea-review. Use when the workflow needs `./docs/workflows/{slug}/idea.md`.
---

# Idea Create

Use this skill as the `Product Strategist` operator playbook.

The operator owns drafting and updating `./docs/workflows/{slug}/idea.md`.

Input can be:
- a rough prompt or theme
- a specific product question
- an existing idea file at `./docs/workflows/{slug}/idea.md`

Requirements:
- derive the workflow `slug` from the prompt or existing workflow dossier
- use a short kebab-case name for the dossier
- write or update `./docs/workflows/{slug}/idea.md`
- keep the artifact self-contained enough that a later reader can understand the opportunity without prior thread context
- open with outcome-first framing that states what changes for the user, why it matters, and how value would be observed if the idea succeeds
- keep the dossier slug stable unless the workflow intentionally splits into a new dossier
- keep the permanent artifact concise and skimmable by default
- include local tracking with:
  - `Source Context` when relevant
  - `Status`
  - `Open Questions`
  - `Revision History`
- include lightweight success signals without turning the idea into a metric plan
- keep the output focused on the idea itself, not on spec or plan detail

Operator responsibility:
- draft the source artifact for later review
- do not try to review or approve your own work
- leave material concerns for `idea-review`

Stage boundary rule:
- `idea.md` explains why the idea matters and what direction is worth exploring
- it does not fully define exact user-visible behavior; that belongs in `spec.md`
- it does not define engineering delivery; that belongs in `plan.md`
- when a detail starts to read like product contract language, route definition, privacy policy, business-rule detail, acceptance behavior, implementation breakdown, or technical design, move that detail out of the idea

Decision rule:
- if a detail is only needed to explain the opportunity, value, risk, or high-level direction, keep it in the idea
- if it changes exact user-visible behavior, correctness expectations, privacy handling, or scope boundaries, leave it for the spec
- if it exists only so engineering can estimate, sequence, or implement the work, leave it for the plan
- when unsure, bias toward less detail and capture the uncertainty in `Open Questions`

Focus on:
- user problem or opportunity
- proposed product direction
- expected value and tradeoffs
- how success would be recognized at a high level
- why the idea is worth pursuing or rejecting
- open questions that should be reviewed next

Do not:
- write a functional spec
- write an implementation plan
- settle engineering details that belong later
- include detailed acceptance criteria, route inventories, API contracts, data models, migration mechanics, file/module breakdowns, or task sequencing
- repeat the same framing in multiple sections when one short summary is enough

Write the idea artifact with sections like:
- title
- purpose / big picture
- context and orientation when needed
- source context when relevant
- user problem or opportunity
- proposed direction
- expected value
- success signals or evidence of value
- tradeoffs and risks
- status
- open questions
- revision history
- reasons not to do this

Before finalizing `idea.md`, perform a scope check:
- remove or simplify any section that reads like `functional requirements`, `acceptance criteria`, `routes`, `privacy rules`, `business rules`, `implementation approach`, `milestones`, or `concrete steps`
- convert prematurely specific downstream detail into:
  - a higher-level product direction statement, or
  - an `Open Questions` entry for later stages
- compress repeated rationale, examples, or risk descriptions when they do not materially change the decision

The output of this stage should be ready for `idea-review`.
