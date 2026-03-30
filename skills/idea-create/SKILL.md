---
name: idea-create
description: Create or refine a product idea before it becomes a functional product contract. Use when the user wants to shape an idea in ./docs/ideas/{topic}.md before moving to spec creation.
---

# Idea Create

Use this skill to create or refine a product idea before it becomes a spec.

This is a product-owner-led creation stage.

The input can be either:
- a rough prompt or theme
- a specific product question
- an existing idea file at `./docs/ideas/{topic}.md`

Requirements:
- derive `topic` from the prompt or existing idea file
- use a short kebab-case name
- write or update `./docs/ideas/{topic}.md`
- when this idea is likely to advance, treat `topic` as the default canonical slug for downstream artifacts unless scope intentionally forks later
- keep the output focused on the idea itself, not on implementation planning

Focus on:
- the user problem or opportunity
- the proposed product direction
- expected value and tradeoffs
- open questions that still need review

Do not:
- write a functional spec
- write an implementation plan
- settle engineering details that belong later in the workflow

Write the idea artifact with sections like:
- topic
- user problem or opportunity
- proposed direction
- tradeoffs
- open questions
- reasons not to do this

The output of this stage should be ready for `idea-review`.
