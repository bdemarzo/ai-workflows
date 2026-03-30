---
name: workflow-run
description: Run the full idea, spec, plan, implementation, and final review workflow from a starting prompt by coordinating the existing stage skills, keeping a ledger in ./docs/runs/{slug}.md, and deciding when to revise or advance. Use when the user wants unattended execution of the workflow with configurable question gates.
---

# Workflow Run

Use this skill to coordinate the full workflow from a starting prompt by using these stage skills:
- `idea-create`
- `idea-review`
- `spec-create`
- `spec-review`
- `plan-create`
- `plan-review`
- `implement-plan`
- `final-review`

This skill is the orchestrator. It decides when to revise or advance.

Requirements:
- derive one canonical `slug` from the starting prompt and keep it in `./docs/runs/{slug}.md`
- treat the run ledger as the source of truth for current stage, artifact paths, loop counts, assumptions, recommendations, decisions, and blockers
- keep a top-level `question_mode:` field near the top of the run ledger
- reuse the canonical slug for downstream artifacts by default unless the workflow intentionally splits or merges scope
- when downstream names diverge, log the reason and source links in both the artifact and the run ledger
- consult the stage skills for artifact-specific instructions instead of rewriting their responsibilities here

At startup:
- if the user already specified a question mode, use it
- if the user's prompt clearly implies a question mode in natural language, infer it, write the inferred value into `question_mode:`, and continue without asking
- otherwise ask one startup question and require one of these modes before proceeding:
  - fully automated
  - blocking questions only
  - ask many questions
- use this exact fallback question when the mode is still ambiguous:
  - `Choose question_mode for workflow-run: fully automated, blocking questions only, or ask many questions.`

Question modes:
- fully automated:
  - ask no further questions after startup
  - make reasonable assumptions and log them in the run ledger
- blocking questions only:
  - ask only when the missing decision is substantively material to the idea, spec, plan, implementation, or final review
  - prefer reasonable assumptions for lower-impact ambiguity
- ask many questions:
  - ask whenever a non-obvious decision could materially improve correctness, clarity, fit, or implementation quality

Inference examples:
- infer `fully automated` from prompts such as `fully automate this`, `run this unattended`, or `do not ask questions`
- infer `blocking questions only` from prompts such as `ask only if you have blocking questions` or `only ask if something materially blocks progress`
- infer `ask many questions` from prompts such as `check in with me on unclear decisions` or `ask questions as you go`
- if the wording does not clearly map to one mode, do not guess; ask the fallback question once

Execution model:
1. establish the question mode, canonical slug, initial context, and run ledger
2. run `idea-create`, then run `idea-review`
3. read the current idea and its review artifact, decide whether to revise `idea-create` or advance to `spec-create`
4. run `spec-create`, then run `spec-review`
5. read the current spec and its review artifact, decide whether to revise `spec-create` or advance to `plan-create`
6. run `plan-create`, then run `plan-review`
7. read the current plan and its review artifact, decide whether to revise `plan-create` or advance to `implement-plan`
8. run `implement-plan`
9. run `final-review`
10. read the full artifact chain and the final review artifact, decide whether to reroute to the earliest broken stage or mark the workflow outcome ready

Advancement gates:
- advance from idea only when the idea is specific enough to support functional design without major unresolved value, feasibility, or scope confusion
- advance from spec only when user-visible behavior, constraints, acceptance criteria, and contract boundaries are specific enough for technical planning
- advance from plan only when sequencing, technical coverage, assumptions, and validation are specific enough for implementation
- mark the workflow outcome ready only when the delivered result is faithful enough to the idea, spec, plan, implementation, and validation chain

Decision rules:
- treat review artifacts as evidence and recommendations, not as the final authority on progression
- prefer revising the current stage over advancing with unresolved material defects
- if a later stage exposes an earlier-stage contract problem, route back to the earliest broken stage
- when implementation reveals contract drift, update the spec before resuming implementation

Hard stop rules:
- stop after 3 loops in the same stage unless the user explicitly allows more
- stop when the same unresolved issue persists across 2 consecutive loops
- stop for required approvals, missing repository access, or ambiguities that would materially invalidate downstream work
- when stopped, record the blocker, affected stage, recommended next action, and open questions in the run ledger

Run ledger contents:
- run summary
- question_mode
- canonical slug
- current stage
- artifact paths
- loop counts by stage
- recommendations received
- orchestrator decisions and rationale
- assumptions made
- blockers and required follow-up

Run ledger header example:
```text
question_mode: blocking questions only
canonical_slug: customer-flag-dashboard
current_stage: spec-create
```

Finish with:
- the final artifact paths
- the final workflow status
- any assumptions that materially shaped the result
- any blockers or follow-up work that prevented completion
