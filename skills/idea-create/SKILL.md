---
name: idea-create
description: Draft, revise, or refine the workflow idea artifact as the Product Strategist operator before idea-review. Use when shaping an early product opportunity, turning a rough prompt into `./docs/workflows/{slug}/idea.md`, or updating an existing idea artifact with accepted user or review feedback.
---

# Idea Create

Use this skill as the `Product Strategist` operator playbook.

The operator owns drafting and updating `./docs/workflows/{slug}/idea.md`.

Use [assets/template.md](./assets/template.md) as the default output skeleton when creating a new artifact. Adapt sections as needed, preserve the slugged title format, and omit any section that does not carry a decision or material uncertainty.

Input can be:
- a rough prompt or theme
- a specific product question
- a requested enhancement to an existing product surface or workflow
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
- when the work enhances existing behavior, make the idea delta-first: state what exists today, what should change, what must be preserved, and why the change is worth doing
- keep the permanent artifact concise and skimmable by default
- include local tracking only when it carries signal; `Status` should stay visible, but `Source Context` and `Open Questions` are optional
- fold accepted user or review feedback into the artifact instead of leaving it chat-only
- replace superseded wording when updating an existing artifact; source artifacts should show current state, not revision history
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
- `execution.md` owns implementation evidence, checks run, remediation history, and deviations after implementation starts

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
- for enhancement work, the gap between current behavior and the desired outcome

Do not:
- write a functional spec
- write an implementation plan
- describe existing functionality as if it is new
- broaden an enhancement request into a full feature redesign unless the user explicitly asked for that
- settle engineering details that belong later
- include detailed acceptance criteria, route inventories, API contracts, data models, migration mechanics, file/module breakdowns, or task sequencing
- repeat the same framing in multiple sections when one short summary is enough

Before finalizing `idea.md`, perform a scope check:
- remove or simplify any section that reads like `functional requirements`, `acceptance criteria`, `routes`, `privacy rules`, `business rules`, `implementation approach`, `milestones`, or `concrete steps`
- convert prematurely specific downstream detail into:
  - a higher-level product direction statement, or
  - an `Open Questions` entry for later stages
- delete optional sections that contain only generic background, duplicated rationale, placeholders, or weak `None` / `TBD` style content
- merge overlapping bullets so each retained line changes the reader's decision or next action
- compress repeated rationale, examples, or risk descriptions when they do not materially change the decision
- for enhancement work, remove abstract feature descriptions that do not distinguish current behavior from the desired change
- when revising after later-stage decisions, remove stale idea-level wording that now contradicts the accepted spec or delivered behavior

The output of this stage should be ready for `idea-review`.
