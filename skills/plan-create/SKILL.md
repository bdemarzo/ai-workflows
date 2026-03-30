---
name: plan-create
description: Turn an approved spec into an implementation-ready engineering plan. Use when the user wants to create or refine a plan in ./docs/plans/{planname}.md.
---

# Plan Create

Before planning, read the repository root `PLANS.md` if it exists and follow its instructions for how plans should be created and structured. Treat `PLANS.md` as supplementary repo-local guidance only. Its absence is normal and must not block planning.

Use this skill to produce an implementation-ready plan in `./docs/plans/{planname}.md`.

This is an architect-led creation stage.

Requirements:
- derive `planname` from `featurename` by default
- use a short kebab-case name
- only choose a different `planname` when the workflow intentionally splits or merges scope, and explain that divergence in the plan body
- update an existing plan instead of creating a duplicate when appropriate
- link to the source spec artifact path in the plan body

Use the spec to define what must be true for users. Use the plan to define how engineering will achieve it.

Decision rule:
- if a missing detail affects user-visible behavior, privacy, or correctness, stop and send it back to the spec
- if a missing detail is only needed for implementation, decide it in the plan

Include:
- source spec artifact
- implementation approach
- ordered work items
- impacted files or modules
- dependencies and assumptions
- validation steps and test cases
- rollout or fallback notes if relevant

Do not:
- restate product policy unless the spec is ambiguous
- mix in brainstorming
- begin implementation

The output of this stage should be ready for `plan-review`.
