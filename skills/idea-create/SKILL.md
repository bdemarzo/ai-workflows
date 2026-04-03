---
name: idea-create
description: Create or refine a product idea before it becomes a functional product contract. Use when the user wants to shape an idea in ./docs/workflows/{slug}/idea.md before moving to spec creation.
---

# Idea Create

Use this skill to create or refine a product idea before it becomes a spec.

This is a product-owner-led creation stage.

The input can be either:
- a rough prompt or theme
- a specific product question
- an existing idea file at `./docs/workflows/{slug}/idea.md`

Requirements:
- derive the workflow `slug` from the prompt or existing workflow dossier
- use a short kebab-case name for the dossier
- write or update `./docs/workflows/{slug}/idea.md`
- keep the idea self-contained enough that a later reader can understand the opportunity without prior thread context
- open with outcome-first framing that states what changes for the user, why it matters, and how value would be observed if the idea succeeds
- keep the dossier slug stable unless the workflow intentionally splits into a new dossier
- include rich local tracking in the artifact with:
  - `Source Context` when relevant
  - `Status`
  - `Open Questions`
  - `Revision History`
- include lightweight evidence-of-value guidance or success signals without turning the idea into a metric plan
- keep the output focused on the idea itself, not on implementation planning

Focus on:
- the user problem or opportunity
- the proposed product direction
- expected value and tradeoffs
- how success would be recognized at a high level
- why the idea is worth pursuing or rejecting
- open questions that still need review

Do not:
- write a functional spec
- write an implementation plan
- settle engineering details that belong later in the workflow

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

The output of this stage should be ready for `idea-review`.
