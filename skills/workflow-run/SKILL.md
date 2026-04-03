---
name: workflow-run
description: Run the full idea, spec, plan, implementation, and final review workflow from a starting prompt by coordinating the existing stage skills, keeping a living lifecycle document in ./docs/workflows/{slug}/run.md, and deciding when to revise or advance. Use when the user wants unattended execution of the workflow with configurable question gates.
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
- derive one canonical `slug` from the starting prompt and keep the workflow dossier under `./docs/workflows/{slug}/`
- treat `./docs/workflows/{slug}/run.md` as the source of truth for lifecycle status, current stage, artifact paths, review-round paths, loop counts, assumptions, recommendations, decisions, blockers, and resume context
- keep a top-level `question_mode:` field near the top of the run ledger
- keep fixed dossier file names for `idea.md`, `spec.md`, `plan.md`, and `execution.md`
- create new review rounds under `reviews/<stage>/round-XX.md` instead of overwriting prior reviews
- consult the stage skills for artifact-specific instructions instead of rewriting their responsibilities here
- keep the run ledger self-contained enough that another agent can resume from the run ledger plus the linked artifacts without needing prior conversation context

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
3. read the current idea and the latest idea review round, decide whether to revise `idea-create` or advance to `spec-create`
4. run `spec-create`, then run `spec-review`
5. read the current spec and the latest spec review round, decide whether to revise `spec-create` or advance to `plan-create`
6. run `plan-create`, then run `plan-review`
7. read the current plan and the latest plan review round, decide whether to revise `plan-create` or advance to `implement-plan`
8. run `implement-plan`
9. run `final-review`
10. read the full artifact chain and the latest final-review round, decide whether to reroute to the earliest broken stage or mark the workflow outcome ready

Advancement gates:
- advance from idea only when the idea is specific enough to support functional design without major unresolved value, feasibility, or scope confusion
- advance from spec only when user-visible behavior, constraints, acceptance criteria, and contract boundaries are specific enough for technical planning
- advance from plan only when sequencing, technical coverage, assumptions, validation, and self-containment are specific enough for implementation
- mark the workflow outcome ready only when the delivered result is faithful enough to the idea, spec, plan, implementation, execution evidence, and validation chain

Decision rules:
- treat review artifacts as evidence and recommendations, not as the final authority on progression
- prefer revising the current stage over advancing with unresolved material defects
- if a later stage exposes an earlier-stage contract problem, route back to the earliest broken stage
- when implementation reveals contract drift, update the spec before resuming implementation
- if a workflow intentionally splits scope, create or reference the related workflow dossier and log the relationship in both run ledgers

Hard stop rules:
- stop after 3 loops in the same stage unless the user explicitly allows more
- stop when the same unresolved issue persists across 2 consecutive loops
- stop for required approvals, missing repository access, or ambiguities that would materially invalidate downstream work
- when stopped, record the blocker, affected stage, recommended next action, and open questions in the run ledger

Run ledger structure:
- maintain these top-level header fields near the top:
  - `question_mode`
  - `canonical_slug`
  - `current_stage`
  - `workflow_status`
- maintain these required sections in the body:
  - `# Purpose / Big Picture`
  - `## Artifact Map`
  - `## Progress`
  - `## Stage Assessments`
  - `## Questions and Assumptions`
  - `## Decision Log`
  - `## Surprises & Discoveries`
  - `## Validation Evidence`
  - `## Current Blockers`
  - `## Resume Instructions`
  - `## Outcomes & Retrospective`

Run ledger update rules:
- update the run ledger at every stopping point and every stage transition
- after each `*-create`, update `Artifact Map`, `Progress`, and `Resume Instructions`
- after each `*-review`, update `Artifact Map`, `Stage Assessments`, `Decision Log`, and `Questions and Assumptions`
- after each advancement or loop-back decision, record:
  - the reviewed artifact path
  - the review round path
  - the review recommendation received
  - the orchestrator decision
  - the rationale for that decision
- after each user question or inferred assumption, record:
  - the question or assumption
  - the answer if one was received
  - the impacted stage or artifact
- after each validation step, add concise evidence showing what was run and what it proved
- when blocked, update `workflow_status`, `Current Blockers`, and `Resume Instructions`
- when complete, write `Outcomes & Retrospective` before exiting

Section guidance:
- `Purpose / Big Picture`: explain what the workflow is trying to deliver, for whom, and what a successful outcome looks like
- `Artifact Map`: list the current paths for `idea.md`, the latest `idea` review round, `spec.md`, the latest `spec` review round, `plan.md`, the latest `plan` review round, `execution.md` when present, and the latest `final` review round when present
- `Progress`: use timestamped checkboxes and keep the list current at every stopping point
- `Stage Assessments`: summarize the current state of each stage, the latest recommendation, and why the orchestrator advanced or looped
- `Questions and Assumptions`: record every answered question, inferred answer, and assumption that materially shaped an artifact or decision
- `Decision Log`: record every stage-advancement, loop-back, or reroute decision with rationale
- `Surprises & Discoveries`: capture unexpected constraints, failed assumptions, or implementation discoveries that changed the workflow
- `Validation Evidence`: record commands, observed outputs, and what those results proved
- `Current Blockers`: list active blockers, why they block progress, and whether the workflow is waiting or stopped
- `Resume Instructions`: state the exact next action for the next agent or resumed run
- `Outcomes & Retrospective`: summarize what was delivered, what was deferred, and lessons learned

Use the run ledger as a lifecycle document, not a thin status note. It should explain what happened, why it happened, and what should happen next.

Run ledger header example:
```text
question_mode: blocking questions only
canonical_slug: customer-flag-dashboard
current_stage: spec-create
workflow_status: in-progress
```

Finish with:
- the final artifact paths
- the final workflow status
- any assumptions that materially shaped the result
- any blockers or follow-up work that prevented completion
