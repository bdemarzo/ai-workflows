---
name: idea-review
description: Review a product idea for value, feasibility, and user relevance. Use when the user wants review feedback in ./docs/workflows/{slug}/reviews/idea/round-01.md before turning an idea into a spec.
---

# Idea Review

Use this skill to review an idea artifact and produce evidence and a recommendation about whether it is ready for spec creation.

Input:
- the idea artifact at `./docs/workflows/{slug}/idea.md`
- any product context or constraints that should stay in view

Requirements:
- derive `slug` from the workflow dossier
- preserve the original idea file
- write the next review round to `./docs/workflows/{slug}/reviews/idea/round-XX.md`
- create a new zero-padded round file for each pass rather than overwriting earlier rounds
- state the exact reviewed artifact path in the review artifact
- link the immediately prior review round when one exists and summarize what changed since that round
- have reviewers form independent opening positions before converging on a recommendation
- use persona diversity and independent opening positions as an analysis method, not as a requirement to save a long transcript of the debate
- include at least one explicitly skeptical or risk-focused perspective that tries to find reasons the current artifact should not advance
- when the artifact is non-trivial or user-facing, include at least one perspective that compares the idea against industry-standard patterns and how similar successful products or applications solve comparable problems
- explicitly check whether the current `idea.md` is understandable without prior chat context or prior review rounds
- explicitly check whether accepted prior review feedback appears to have been folded back into the latest `idea.md`
- keep the saved review artifact concise and findings-first by default

Default reviewer perspectives:
- key stakeholders
- power users
- technical product manager

Review adaptation:
- choose reviewer personas based on artifact scope, risk, and affected surface area
- use fewer perspectives for narrow or exploratory ideas
- use broader perspectives for high-risk, user-facing, or cross-functional ideas
- when the workflow includes meaningful UI, UX, navigation, or interaction design, include an explicit UX or product-design perspective
- for user-facing workflow changes, have that UX or product-design reviewer challenge clarity of flow, user expectations, friction, and success from the interface point of view
- do not optimize for reviewer consensus; preserve strong dissent when the artifact still has meaningful weaknesses
- when using comparable products or best-practice references, treat them as inputs for critique rather than as permission to hand-wave missing details
- preserve only consequential disagreements in the saved artifact; do not transcribe the full back-and-forth when a short summary will do

Synthesize the result into:
- what works
- concerns about value or user relevance
- whether the idea's success signals are observable enough to justify advancing
- feasibility or scope concerns
- UI or UX concerns about discoverability, flow clarity, interaction friction, or user comprehension when relevant
- where the idea falls short of industry-standard patterns or comparable successful products when relevant
- the strongest reasons not to advance yet
- whether the artifact is self-contained enough for spec creation from the artifact alone
- where the stakeholders disagree
- what should change before spec creation
- whether the idea is ready to advance

Write the review artifact as a compact findings-first review with sections like:
- reviewed artifact
- prior review rounds when relevant
- reviewer lenses
- review scope
- self-containment assessment
- observability of value
- incorporation of prior accepted feedback
- benchmark and best-practice comparison when relevant
- key findings
- meaningful disagreements
- suggested revisions
- recommendation
- outstanding dissent

Compression rule:
- merge overlapping findings when multiple reviewer lenses point to the same underlying issue
- avoid repeating the same critique from multiple personas
- summarize benchmark or comparable-product analysis into a short conclusion unless it materially changes the recommendation
- keep persona names short and use them as reviewer lenses, not as a reason to expand the artifact into a transcript

Finish with an explicit recommendation:
- `Recommendation: revise current stage`
- `Recommendation: ready to advance to spec-create`

The review recommendation informs the next decision, but the human or `workflow-run` decides whether to advance. The recommendation should make clear whether the idea is ready for spec creation from the current artifact alone.
