---
name: spec-create
description: Turn an approved idea into a functional product contract. Use when the user wants to create or refine the feature spec in ./docs/specs/{featurename}.md.
---

# Spec Create

Use this skill to create or update the feature spec at `./docs/specs/{featurename}.md`.

This is a technical-product-manager-led creation stage.

Write a functional product contract, not an execution plan.

The input can be either:
- an approved idea from the prompt
- an existing feature spec file that should be refined in place
- an idea artifact at `./docs/ideas/{topic}.md`

Requirements:
- derive `featurename` from the prompt or the existing feature file
- when starting from an idea artifact, reuse the idea slug as `featurename` by default unless the workflow intentionally splits scope
- use a short kebab-case name
- create the file if it does not exist
- update the file in place if it already exists
- when created from an idea, link back to the source idea artifact path and explain any slug divergence
- keep the spec as the source of truth for user-visible behavior, scope, and correctness

Keep these details in the spec:
- user-visible behavior
- scope
- constraints
- privacy rules
- business rules
- user-facing routes or URLs
- acceptance criteria

Do not put these details in the spec:
- implementation sequencing
- task breakdown
- file or module lists
- test matrices
- migration mechanics unless they change user-visible outcomes

Decision rule:
- if a detail is only needed so engineering can implement it, leave it for the plan
- if it changes user expectations, privacy, or correctness, keep it in the spec

Write the feature file with these sections:
- source idea artifact when relevant
- summary
- problem statement
- goals
- non-goals
- target users
- core user flows
- constraints
- privacy rules, business rules, and user-facing routes or URLs when relevant
- open questions
- acceptance criteria

The output of this stage should be ready for `spec-review`.
