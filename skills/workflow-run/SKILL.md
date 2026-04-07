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
- keep workflow guidance in plain text under a `### Workflow Guidelines` subsection inside `# Purpose / Big Picture` rather than as top-of-file header fields
- when the workflow is intentionally split across clients or agents, record that plan in plain text under a `### Client Handoff Plan` subsection inside `# Purpose / Big Picture`
- treat user interaction history as critical workflow state: important questions asked, answers received, clarifications, unresolved threads, and resulting decisions must be recorded in `run.md`, not left only in chat history
- when the repo is under Git and the workflow is expected to change files, record the chosen Git commit policy in the workflow guidelines subsection
- keep fixed dossier file names for `idea.md`, `spec.md`, `plan.md`, and `execution.md`
- create new review rounds under `reviews/<stage>/round-XX.md` instead of overwriting prior reviews
- consult the stage skills for artifact-specific instructions instead of rewriting their responsibilities here
- keep the run ledger self-contained enough that another agent can resume from the run ledger plus the linked artifacts without needing prior conversation context

At startup:
- treat startup as a preflight step, not as the beginning of stage execution
- resolve run and execution options before creating stage artifacts or starting `idea-create`
- if more than one startup option is ambiguous, ask all required startup-option questions first and finish that clarification pass before asking for start confirmation
- if the user already specified a question mode, use it
- if the user's prompt clearly implies a question mode in natural language, infer it, record it in the workflow guidelines subsection, and continue without asking
- otherwise ask one plain-language startup question about how autonomous the workflow should be and map the answer into one of these modes:
  - fully automated
  - blocking questions only
  - ask many questions
- format startup questions as short labeled choices rather than only as open-ended prose:
  - prefer a numbered list such as `1.`, `2.`, `3.` when the client does not provide richer choice UI
  - keep the labels user-facing and descriptive rather than exposing internal field names
  - tell the user they can reply with the number or answer in their own words
- use this exact fallback question structure when the mode is still ambiguous:
  - `How should I handle decisions as I run this workflow?`
  - `1. Make reasonable assumptions and only stop for review gates`
  - `2. Ask only when something would materially block good work`
  - `3. Check in often on non-obvious choices`
  - `Reply with 1, 2, 3, or answer in your own words.`
- if the user already specified a stage gate mode, use it
- if the user's prompt clearly implies a stage gate mode in natural language, infer it, record it in the workflow guidelines subsection, and continue without asking
- otherwise ask one plain-language startup question about review pauses and map the answer into a supported stage gate mode
- use this exact fallback question structure when the stage-gate preference is still ambiguous:
  - `How do you want me to handle major stage reviews?`
  - `1. Stop for my approval after idea review, spec review, plan review, and implementation`
  - `2. Run straight through unless something is blocked`
  - `Reply with 1, 2, or answer in your own words.`
- if the repository is under Git and the workflow is likely to create or change files:
  - if the user already specified commit behavior, use it
  - if the user's prompt clearly implies commit behavior in natural language, infer it, record it in the workflow guidelines subsection, and continue without asking
  - otherwise ask one plain-language startup question about commit cadence and map the answer into a Git commit policy
  - use this exact fallback question structure when the commit preference is still ambiguous:
    - `How do you want me to handle Git commits for workflow changes?`
    - `1. Do not create commits automatically`
    - `2. Create commits at major approved stage boundaries when files changed`
    - `3. Create a commit after each file-changing stage`
    - `Reply with 1, 2, 3, or answer in your own words.`
- determine `execution_plan_mode` before planning:
  - if the repository root contains `PLANS.md`, use `execplan`
  - if the repository root `AGENTS.md` says planning and implementation must use `PLANS.md`, use `execplan`
  - otherwise use `standard`
- once all startup options are clear, present one concise startup confirmation summary before beginning the workflow:
  - restate the workflow ask or prompt in plain language
  - show the canonical slug
  - show the resolved question mode
  - show the resolved stage gate mode
  - show the resolved Git commit policy when relevant
  - show the resolved execution plan mode
  - show any explicit client handoff plan when relevant
  - ask the user to confirm before stage execution begins
- use a plain-language confirmation prompt rather than internal field names or raw config dumps
- prefer a short confirmation structure such as:
  - `Here is how I will run this workflow:`
  - `- Workflow ask: Build a lightweight internal release notes tool for product and engineering teams.`
  - `- Canonical slug: release-notes-tool`
  - `- Decision handling: ask only when something would materially block good work`
  - `- Review pauses: stop for approval after idea review, spec review, plan review, and implementation`
  - `- Git commits: create commits at major approved stage boundaries when files changed`
  - `- Execution plan mode: standard`
  - `Reply 'start' to begin, or tell me what to change.`
- do not begin `idea-create` until the user confirms the startup summary
- after confirmation, create or update `run.md` and record the final startup choices plus the fact that the user approved the workflow start

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
- when asking the fallback question, preserve the numbered-choice format rather than collapsing it into a single open-ended sentence

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
- when asking the fallback question, preserve the numbered-choice format rather than collapsing it into a single open-ended sentence

Git commit policy options:
- `manual only`:
  - do not create commits automatically
- `approved stage boundaries`:
  - create commits only after file-changing stages that have reached a user-approved boundary
- `each file-changing stage`:
  - create a commit after each stage that changed files

Git commit inference examples:
- infer `manual only` from prompts such as `do not commit`, `I will handle commits`, or `leave git alone`
- infer `approved stage boundaries` from prompts such as `commit after each approved step`, `commit at review gates`, or `commit when I approve a stage`
- infer `each file-changing stage` from prompts such as `commit after each step` or `commit every stage`
- if the wording does not clearly express a commit preference, do not guess; ask the plain-language fallback question once
- when asking the fallback question, preserve the numbered-choice format rather than collapsing it into a single open-ended sentence

Execution-plan modes:
- `standard`:
  - use the portable workflow defaults in this repo
  - `run.md` may continue carrying fuller workflow lifecycle tracking
- `execplan`:
  - treat `plan.md` as the authoritative execution control document once implementation starts
  - treat repository `PLANS.md` and repo `AGENTS.md` planning rules as authoritative
  - keep `run.md` focused on orchestration, approvals, blockers, and high-level reroute decisions during implementation

Execution model:
1. resolve startup options, ask any needed startup-option questions, and prepare the workflow ask for confirmation
2. present one startup confirmation summary and wait for explicit user approval to begin
3. after approval, establish the canonical slug, initial context, and run ledger
4. run `idea-create`, then run `idea-review`
5. read the current idea and the latest idea review round, decide whether to revise `idea-create` or advance to `spec-create`
6. if `stage_gate_mode` is `loop boundaries`, pause after `idea-review` and before `spec-create`
7. run `spec-create`, then run `spec-review`
8. read the current spec and the latest spec review round, decide whether to revise `spec-create` or advance to `plan-create`
9. if `stage_gate_mode` is `loop boundaries`, pause after `spec-review` and before `plan-create`
10. run `plan-create`, then run `plan-review`
11. read the current plan and the latest plan review round, decide whether to revise `plan-create` or advance to `implement-plan`
12. before implementation, consolidate accepted plan-review decisions into `plan.md` so execution-critical decisions are captured in the plan itself
13. if `stage_gate_mode` is `loop boundaries`, pause after `plan-review` and before `implement-plan`
14. run `implement-plan`
15. if `stage_gate_mode` is `loop boundaries`, pause after `implement-plan` and before `final-review`
16. run `final-review`
17. read the full artifact chain and the latest final-review round, decide whether to reroute to the earliest broken stage or mark the workflow outcome ready

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
- if the workflow intentionally splits ownership across clients or agents, record:
  - which client or agent is preferred for which stages
  - which client or agent should act next
  - why that handoff exists
  - what artifact the next client should pick up from
- do not assume automatic client switching; use the run ledger to make the handoff explicit and restartable
- if a Git commit policy is enabled:
  - only commit files that belong to the workflow change set
  - do not include unrelated user changes
  - do not create empty commits
  - update `run.md` before committing so the commit reflects the actual workflow state
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
- record `pending_transition` in the workflow guidelines subsection when paused
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
- maintain these required sections in the body:
  - `# Purpose / Big Picture`
  - `### Workflow Guidelines`
  - `### Client Handoff Plan` when relevant
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
- after startup options are resolved and the user confirms the start, record:
  - the original workflow ask
  - the resolved startup options
  - any startup-option questions that were asked
  - the answers that resolved them
  - the explicit user confirmation to begin
- update the run ledger at every stopping point and every stage transition
- update the run ledger after every materially important user interaction, not only at stage boundaries
- after each `*-create`, update `Artifact Map`, `Progress`, and `Resume Instructions`
- after each `*-review`, update `Artifact Map`, `Stage Assessments`, `Decision Log`, and `Questions and Assumptions`
- after each advancement or loop-back decision, record:
  - the reviewed artifact path
  - the review round path
  - the review recommendation received
  - the orchestrator decision
  - the rationale for that decision
- after each blocking or materially useful user exchange, record:
  - what the agent asked
  - why it asked
  - the user's answer or clarification
  - what changed because of that answer
  - any still-open questions or follow-up needed
- before each stage-gate pause, record:
  - the completed stage
  - the pending transition
  - the latest artifact path
  - the latest review-round path when one exists
  - the decision requested from the user
- before any intentional client or agent handoff, record:
  - the current owner
  - the next recommended owner
  - the stage or artifact boundary where the handoff happens
  - the exact artifact path the next owner should start from
  - any open questions or review rounds the next owner must consider
- when multiple clients or agents review the same artifact, record each review as its own review round in sequence and summarize the combined outcome in `Decision Log`
- when a Git commit is created as part of the workflow policy, record:
  - why the commit happened
  - which stage or boundary it corresponds to
  - the commit identifier or summary when available
- after each user question or inferred assumption, record:
  - the question or assumption
  - the answer if one was received
  - the impacted stage or artifact
- do not summarize a multi-question conversation into a single vague bullet when the individual answers materially shaped the workflow; keep enough detail that another agent can reconstruct why the workflow took its current path
- after each validation step, add concise evidence showing what was run and what it proved
- when blocked, update `workflow_status`, `Current Blockers`, and `Resume Instructions`
- when complete, write `Outcomes & Retrospective` before exiting
- in `execplan` mode, once `implement-plan` starts:
  - keep `run.md` focused on current stage, artifact map, approval state, blockers, and high-level reroute decisions
  - avoid duplicating detailed execution progress, decision logs, or discoveries that should live in `plan.md`

Section guidance:
- `Purpose / Big Picture`: explain what the workflow is trying to deliver, for whom, and what a successful outcome looks like
- `Workflow Guidelines`: record the current question mode, stage gate mode, Git commit policy when relevant, execution plan mode, canonical slug, current stage, workflow status, and pending transition when paused, using plain text bullets or short prose rather than frontmatter-like header lines
- `Client Handoff Plan`: when relevant, record the preferred client or agent for each stage group, the current owner, the next recommended owner, and how dual-review stages should be sequenced
- `Artifact Map`: list the current paths for `idea.md`, the latest `idea` review round, `spec.md`, the latest `spec` review round, `plan.md`, the latest `plan` review round, `execution.md` when present, and the latest `final` review round when present
- `Progress`: use timestamped checkboxes and keep the list current at every stopping point
- `Stage Assessments`: summarize the current state of each stage, the latest recommendation, and why the orchestrator advanced or looped
- `Questions and Assumptions`: record each materially important question, the answer given, why it mattered, any unresolved follow-up, and any inferred assumption used when no answer was available
- `Decision Log`: record every startup confirmation, stage-advancement, loop-back, reroute, or user-driven decision with rationale and note which question, answer, or discovery triggered it when relevant
- `Surprises & Discoveries`: capture unexpected constraints, failed assumptions, implementation discoveries, or user clarifications that materially changed the workflow
- `Validation Evidence`: record commands, observed outputs, and what those results proved
- `Current Blockers`: list active blockers, why they block progress, and whether the workflow is waiting or stopped
- `Resume Instructions`: state the exact next action for the next agent or resumed run, including the approval decision needed when paused at a stage gate
- `Outcomes & Retrospective`: summarize what was delivered, what was deferred, and lessons learned
- in `execplan` mode, `run.md` should support orchestration and handoff, while `plan.md` should remain sufficient for implementation restart

Use the run ledger as a lifecycle document, not a thin status note. It should explain what happened, why it happened, and what should happen next.

Run ledger metadata example:
```text
# Purpose / Big Picture
Build a lightweight internal release notes tool for product and engineering teams.

### Workflow Guidelines
- Question mode: blocking questions only
- Stage gate mode: loop boundaries
- Git commit policy: approved stage boundaries
- Execution plan mode: execplan
- Canonical slug: customer-flag-dashboard
- Current stage: spec-create
- Workflow status: in-progress
```

Paused run-ledger metadata example:
```text
# Purpose / Big Picture
Build a lightweight internal release notes tool for product and engineering teams.

### Workflow Guidelines
- Question mode: blocking questions only
- Stage gate mode: loop boundaries
- Git commit policy: approved stage boundaries
- Execution plan mode: execplan
- Canonical slug: customer-flag-dashboard
- Current stage: spec-review
- Workflow status: awaiting-stage-approval
- Pending transition: spec-review -> plan-create

### Client Handoff Plan
- Preferred owner for idea and spec: Claude
- Preferred owner for plan and implementation: Codex
- Dual-review policy: when both clients review the same artifact, create sequential review rounds and summarize the combined decision in `Decision Log`
- Next recommended owner: Codex
```

Finish with:
- the final artifact paths
- the final workflow status
- the current or final owner when multi-client handoffs were used
- any assumptions that materially shaped the result
- any blockers or follow-up work that prevented completion
