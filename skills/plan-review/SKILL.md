---
name: plan-review
description: Perform peer review of an engineering plan from architectural and engineering perspectives across the relevant parts of the stack. Use when the user wants review feedback in ./docs/workflows/{slug}/reviews/plan/round-01.md before implementation.
---

# Plan Review

Use this skill to review an engineering plan and produce evidence and a recommendation about whether it is ready for implementation.

Input:
- the plan at `./docs/workflows/{slug}/plan.md`
- any technical context or constraints that should stay in view

Requirements:
- derive `slug` from the workflow dossier
- preserve the original plan file
- write the next review round to `./docs/workflows/{slug}/reviews/plan/round-XX.md`
- create a new zero-padded round file for each pass rather than overwriting earlier rounds
- state the exact reviewed artifact path in the review artifact
- link the immediately prior review round when one exists and summarize what changed since that round
- have reviewers form independent opening positions before converging on a recommendation
- use persona diversity and independent opening positions as an analysis method, not as a requirement to save a long transcript of the debate
- include at least one explicitly skeptical or risk-focused perspective that tries to find reasons the current plan should not advance
- when the plan touches established platform, frontend, architecture, or delivery patterns, include at least one perspective that compares it against industry-standard implementation practices and strong comparable products or applications
- keep the saved review artifact concise and findings-first by default

Default reviewer perspectives:
- engineer
- technical product manager

Review adaptation:
- choose reviewer personas based on artifact scope, risk, and affected surface area
- include additional architectural or domain-specific personas when the plan scope requires it
- use a smaller reviewer set for narrow changes
- when the plan includes meaningful UI, UX, accessibility, responsive behavior, or front-end interaction work, include an explicit UX, design-system, or front-end experience perspective
- do not optimize for reviewer consensus; preserve strong dissent when material implementation or rollout risks remain
- preserve only consequential disagreements in the saved artifact; do not transcribe the full back-and-forth when a short summary will do

Focus on:
- implementation sequencing
- full-stack coverage
- architectural soundness
- validation realism
- missing assumptions or risky gaps
- front-end interaction, accessibility, state, or responsive-delivery risks when relevant
- where the plan falls short of industry-standard implementation practices or comparable successful applications when relevant
- the strongest reasons not to advance yet
- whether the plan is self-contained enough for a later engineer to implement it safely

Write the review artifact as a compact findings-first review with sections like:
- reviewed artifact
- prior review rounds when relevant
- reviewer lenses
- review scope
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
- `Recommendation: ready to advance to implement-plan`

The review recommendation informs the next decision, but the human or `workflow-run` decides whether to advance.
