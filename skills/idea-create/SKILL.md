---
name: idea-create
description: Draft, revise, or refine the workflow idea artifact as the Product Strategist operator before idea-review. Use when shaping an early product opportunity, turning a rough prompt into `./docs/workflows/{slug}/idea.md`, or updating an existing idea artifact with accepted user or review feedback.
---

# Idea Create

Use this skill as the `Product Strategist` operator playbook.

The operator owns drafting and updating `./docs/workflows/{slug}/idea.md`.

Use [assets/template.md](./assets/template.md) as the default output skeleton when creating a new artifact. Adapt sections as needed, but preserve the slugged title format.

Input can be:
- a rough prompt or theme
- a specific product question
- an existing idea file at `./docs/workflows/{slug}/idea.md`

Requirements:
- derive the workflow `slug` from the prompt or existing workflow dossier
- use a short kebab-case name for the dossier
- write or update `./docs/workflows/{slug}/idea.md`
- start the artifact with the exact H1 `# Idea - {slug}`
- update an existing `idea.md` in place rather than creating duplicates
- keep the dossier slug stable unless the workflow intentionally splits into a new dossier
- keep the artifact self-contained enough that a later reader can understand the opportunity without prior thread context
- open with outcome-first framing that states what changes for the user, why it matters, and how value would be observed if the idea succeeds
- keep the permanent artifact concise and skimmable by default
- include local tracking with:
  - `Source Context` when relevant
  - `Status`
  - `Open Questions`
  - `Revision History`
- fold accepted user or review feedback into the artifact instead of leaving it chat-only
- retain useful revision history when updating an existing artifact
- include lightweight success signals without turning the idea into a metric plan
- keep the output focused on the idea itself, not on spec or plan detail

Operator responsibility:
- draft the source artifact for later review
- do not try to review or approve your own work
- leave material concerns for `idea-review`

Idea boundary:
- `idea.md` explains the opportunity, expected value, high-level direction, risks, and intentionally deferred questions
- `spec.md` owns exact user-visible behavior, scope boundaries, privacy handling, business rules, and acceptance expectations
- `plan.md` owns engineering sequencing, implementation structure, validation commands, migration mechanics, and delivery steps

Decision rule:
- if a detail is only needed to explain the opportunity, value, risk, or high-level direction, keep it in the idea
- if it changes exact user-visible behavior, correctness expectations, privacy handling, or scope boundaries, leave it for the spec
- if it exists only so engineering can estimate, sequence, or implement the work, leave it for the plan
- when unsure, bias toward less detail and capture intentional uncertainty in `Open Questions`
- use `Open Questions` for uncertainties to review or defer, not for blockers that make the idea artifact unsafe to review

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

Before finalizing `idea.md`, perform a scope check:
- remove or simplify any section that reads like `functional requirements`, `acceptance criteria`, `routes`, `privacy rules`, `business rules`, `implementation approach`, `milestones`, or `concrete steps`
- convert prematurely specific downstream detail into:
  - a higher-level product direction statement, or
  - an `Open Questions` entry for later stages
- compress repeated rationale, examples, or risk descriptions when they do not materially change the decision

The output of this stage should be ready for `idea-review`.
