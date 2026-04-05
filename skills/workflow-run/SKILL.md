---
name: workflow-run
description: Run the full idea, spec, plan, implementation, and final review workflow from a starting prompt by coordinating the existing stage skills, keeping a living lifecycle document in ./docs/workflows/{slug}/run.md, and deciding when to revise or advance. Use when the user wants unattended execution of the workflow with configurable question and stage gates.
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
- treat `./docs/workflows/{slug}/run.md` as the source of truth for orchestration state, current stage, artifact paths, review-round paths, loop counts, approvals, blockers, and resume context
- keep a top-level `question_mode:` field near the top of the run ledger
- keep a top-level `stage_gate_mode:` field near the top of the run ledger
- keep a top-level `execution_plan_mode:` field near the top of the run ledger
- keep fixed dossier file names for `idea.md`, `spec.md`, `plan.md`, and `execution.md`
- create new review rounds under `reviews/<stage>/round-XX.md` instead of overwriting prior reviews
- consult the stage skills for artifact-specific instructions instead of rewriting their responsibilities here
- keep the run ledger self-contained enough that another agent can resume from the run ledger plus the linked artifacts without needing prior conversation context

At startup:
- if the user already specified a question mode, use it
- if the user's prompt clearly implies a question mode in natural language, infer it, write the inferred value into `question_mode:`, and continue without asking
- otherwise ask one plain-language startup question about how autonomous the workflow should be and map the answer into one of these modes:
  - fully automated
  - blocking questions only
  - ask many questions
- use this exact fallback question when the mode is still ambiguous:
  - `How should I handle decisions as I run this workflow: make reasonable assumptions and only stop for review gates, ask only when something would materially block good work, or check in often on non-obvious choices?`
- if the user already specified a stage gate mode, use it
- if the user's prompt clearly implies a stage gate mode in natural language, infer it, write the inferred value into `stage_gate_mode:`, and continue without asking
- otherwise ask one plain-language startup question about review pauses and map the answer into a supported stage gate mode
- use this exact fallback question when the stage-gate preference is still ambiguous:
  - `Do you want me to pause for your approval at the major stage boundaries after idea review, spec review, plan review, and implementation, or should I run straight through unless something is blocked?`
- determine `execution_plan_mode` before planning:
  - if the repository root contains `PLANS.md`, use `execplan`
  - if the repository root `AGENTS.md` says planning and implementation must use `PLANS.md`, use `execplan`
  - otherwise use `standard`
- write the resolved mode into `execution_plan_mode:`

Question modes:
- fully automated:
  - ask no further questions after startup
  - make reasonable assumptions and log them in the run ledger
  - if the workflow needs a new architectural direction, a major architectural constraint, or a new third-party service, SDK, hosted platform, or external tool, choose the best justified option and record the reasoning, tradeoffs, and affected artifacts in the run ledger
- blocking questions only:
  - ask only when the missing decision is substantively material to the idea, spec, plan, implementation, or final review
  - treat these as substantively material by default:
    - introducing a new architectural pattern, boundary, or major technical constraint
    - adding a new third-party service, SDK, hosted platform, or external tool
    - accepting a new security, privacy, cost, operational, or vendor-lock-in tradeoff
  - prefer reasonable assumptions for lower-impact ambiguity
- ask many questions:
  - ask whenever a non-obvious decision could materially improve correctness, clarity, fit, or implementation quality

Inference examples:
- infer `fully automated` from prompts such as `fully automate this`, `run this unattended`, or `do not ask questions`
- infer `blocking questions only` from prompts such as `ask only if you have blocking questions` or `only ask if something materially blocks progress`
- infer `ask many questions` from prompts such as `check in with me on unclear decisions` or `ask questions as you go`
- if the wording does not clearly map to one mode, do not guess; ask the plain-language fallback question once

Stage gate modes:
- `none`:
  - do not pause for human approval between stages unless a normal blocker requires it
- `loop boundaries`:
  - pause at major stage transitions so a human can review the current artifacts before the next stage starts
  - treat these pauses as approval checkpoints, not clarification questions

Stage gate inference examples:
- infer `loop boundaries` from prompts such as `pause before moving from idea to spec`, `let me review each stage before continuing`, or `gate the workflow at each step`
- infer `none` from prompts such as `run straight through`, `do not stop between stages`, or `only stop for real blockers`
- if the wording does not clearly express a review-pause preference, do not guess; ask the plain-language fallback question once

Execution-plan modes:
- `standard`:
  - use the portable workflow defaults in this repo
  - `run.md` may continue carrying fuller workflow lifecycle tracking
- `execplan`:
  - treat `plan.md` as the authoritative execution control document once implementation starts
  - treat repository `PLANS.md` and repo `AGENTS.md` planning rules as authoritative
  - keep `run.md` focused on orchestration, approvals, blockers, and high-level reroute decisions during implementation

Execution model:
1. establish the question mode, canonical slug, initial context, and run ledger
2. run `idea-create`, then run `idea-review`
3. read the current idea and the latest idea review round, decide whether to revise `idea-create` or advance to `spec-create`
4. if `stage_gate_mode` is `loop boundaries`, pause after `idea-review` and before `spec-create`
4. run `spec-create`, then run `spec-review`
5. read the current spec and the latest spec review round, decide whether to revise `spec-create` or advance to `plan-create`
6. if `stage_gate_mode` is `loop boundaries`, pause after `spec-review` and before `plan-create`
6. run `plan-create`, then run `plan-review`
7. read the current plan and the latest plan review round, decide whether to revise `plan-create` or advance to `implement-plan`
8. before implementation, consolidate accepted plan-review decisions into `plan.md` so execution-critical decisions are captured in the plan itself
8. if `stage_gate_mode` is `loop boundaries`, pause after `plan-review` and before `implement-plan`
8. run `implement-plan`
9. if `stage_gate_mode` is `loop boundaries`, pause after `implement-plan` and before `final-review`
10. run `final-review`
11. read the full artifact chain and the latest final-review round, decide whether to reroute to the earliest broken stage or mark the workflow outcome ready

Advancement gates:
- advance from idea only when the idea is specific enough to support functional design without major unresolved value, feasibility, or scope confusion
- advance from spec only when user-visible behavior, constraints, acceptance criteria, and contract boundaries are specific enough for technical planning
- advance from plan only when sequencing, technical coverage, assumptions, validation, and self-containment are specific enough for implementation
- mark the workflow outcome ready only when the delivered result is faithful enough to the idea, spec, plan, implementation, execution evidence, and validation chain
- do not add a completion gate after `final-review`; use the final review recommendation and normal reroute logic instead

Decision rules:
- treat review artifacts as evidence and recommendations, not as the final authority on progression
- prefer revising the current stage over advancing with unresolved material defects
- if a later stage exposes an earlier-stage contract problem, route back to the earliest broken stage
- when implementation reveals contract drift, update the spec before resuming implementation
- when a new architectural direction or new external dependency becomes necessary, treat that decision as materially important:
  - in `blocking questions only`, ask before locking it in
  - in `fully automated`, make the best justified choice and record the reasoning in `run.md` plus the affected source artifact
- if a workflow intentionally splits scope, create or reference the related workflow dossier and log the relationship in both run ledgers
- in `execplan` mode, treat repo `PLANS.md` and repo `AGENTS.md` execution rules as higher priority than portable defaults in this workflow
- in `execplan` mode, do not let `run.md` compete with `plan.md` as a second implementation source of truth

Hard stop rules:
- stop after 3 loops in the same stage unless the user explicitly allows more
- stop when the same unresolved issue persists across 2 consecutive loops
- stop for required approvals, missing repository access, or ambiguities that would materially invalidate downstream work
- when stopped, record the blocker, affected stage, recommended next action, and open questions in the run ledger

Stage gate behavior:
- when `stage_gate_mode` is `loop boundaries`, pause only at these transitions:
  - after `idea-review`, before `spec-create`
  - after `spec-review`, before `plan-create`
  - after `plan-review`, before `implement-plan`
  - after `implement-plan`, before `final-review`
- before pausing, update `run.md` with:
  - the completed stage
  - the pending transition
  - the latest artifact path
  - the latest review-round path when one exists
  - the orchestrator's rationale for recommending advancement
- set `workflow_status:` to `awaiting-stage-approval` while paused
- add `pending_transition:` near the top of the run ledger when paused
- use a plain-text gate prompt that includes:
  - current completed stage
  - pending next stage
  - artifact paths to review
  - the latest review recommendation
  - the orchestrator assessment
  - the explicit decision needed: `approve` or `revise current stage`
- if the user responds `approve`, continue into the pending stage
- if the user responds `revise current stage`:
  - at the idea, spec, or plan gates, rerun the matching `*-create` stage and then the matching `*-review` stage again
  - at the implementation gate, rerun `implement-plan` before moving to `final-review`
  - revisit the same gate after the revision pass before advancing
- in `execplan` mode, keep stage gates and questions fully available before implementation
- once `implement-plan` starts in `execplan` mode:
  - ask no more clarification questions unless a true blocker requires them
  - do not introduce milestone-by-milestone approval pauses unless the user explicitly requested that behavior
  - if `stage_gate_mode` is `loop boundaries`, the existing gate before `final-review` may still be used

Run ledger structure:
- maintain these top-level header fields near the top:
  - `question_mode`
  - `stage_gate_mode`
  - `execution_plan_mode`
  - `canonical_slug`
  - `current_stage`
  - `workflow_status`
  - `pending_transition` when paused for approval
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
- before each stage-gate pause, record:
  - the completed stage
  - the pending transition
  - the latest artifact path
  - the latest review-round path when one exists
  - the decision requested from the user
- after each user question or inferred assumption, record:
  - the question or assumption
  - the answer if one was received
  - the impacted stage or artifact
- after each validation step, add concise evidence showing what was run and what it proved
- when blocked, update `workflow_status`, `Current Blockers`, and `Resume Instructions`
- when complete, write `Outcomes & Retrospective` before exiting
- in `execplan` mode, once `implement-plan` starts:
  - keep `run.md` focused on current stage, artifact map, approval state, blockers, and high-level reroute decisions
  - avoid duplicating detailed execution progress, decision logs, or discoveries that should live in `plan.md`

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
- `Resume Instructions`: state the exact next action for the next agent or resumed run, including the approval decision needed when paused at a stage gate
- `Outcomes & Retrospective`: summarize what was delivered, what was deferred, and lessons learned
- in `execplan` mode, `run.md` should support orchestration and handoff, while `plan.md` should remain sufficient for implementation restart

Use the run ledger as a lifecycle document, not a thin status note. It should explain what happened, why it happened, and what should happen next.

Run ledger header example:
```text
question_mode: blocking questions only
stage_gate_mode: loop boundaries
execution_plan_mode: execplan
canonical_slug: customer-flag-dashboard
current_stage: spec-create
workflow_status: in-progress
```

Paused run-ledger header example:
```text
question_mode: blocking questions only
stage_gate_mode: loop boundaries
execution_plan_mode: execplan
canonical_slug: customer-flag-dashboard
current_stage: spec-review
workflow_status: awaiting-stage-approval
pending_transition: spec-review -> plan-create
```

Finish with:
- the final artifact paths
- the final workflow status
- any assumptions that materially shaped the result
- any blockers or follow-up work that prevented completion
