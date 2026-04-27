# Run Ledger Reference

Read this reference when creating or updating `docs/workflows/{slug}/run.md`, resuming a workflow, resolving a user gate, or handling a reroute/remediation loop.

Use [../assets/run-template.md](../assets/run-template.md) as the output skeleton.

## Required Sections

Maintain these sections:
- `# Run - {slug}`
- `## Purpose / Big Picture`
- `### Workflow Guidelines`
- `## Artifact Map`
- `## Progress`
- `## Phase Ownership`
- `## Stage Assessments`
- `## Decision Log`
- `## Current Blockers`
- `## Resume Instructions`
- `## Outcomes & Retrospective`

Do not add `## Validation Evidence` to `run.md`. Validation belongs in `plan.md`, `execution.md`, or review artifacts when needed.

Keep `run.md` under roughly 120 lines. It is a restart ledger, not a chronology, test report, or implementation journal.

## Update Timing

After startup confirmation, record:
- original workflow ask
- canonical slug
- current orchestrator
- concrete persona-to-agent bindings used
- substitutions or fallbacks used
- initial user constraints and clarifications
- confirmation that the user approved the guided workflow start

Before each create stage, record:
- current operator
- current reviewer roster
- current phase objective
- artifact-based restatement of current truth used to start the phase

After each create stage, update:
- `Artifact Map`
- `Progress`
- `Resume Instructions`
Do not append every minor step to `Progress`; replace it with the current state.

After each review stage, record:
- reviewed artifact path
- official review round path
- operator for the phase
- reviewer roster for the phase
- reviewer display names when the runtime exposes them
- brief reviewer synopses preserved in the official review artifact
- recommendation
- one-sentence orchestrator consolidation rationale

After each user gate, record:
- what the user reviewed
- approval or revision decision
- any conditions the user attached to proceeding
- artifact-based re-grounding summary used before the next step when needed
- where accepted feedback was written in repo markdown artifacts

During implementation review, record:
- satisfaction status for architecture
- satisfaction status for security
- satisfaction status for QA / product correctness
- remediation cycle count

During operator progress checks or stalled-operator recovery, record:
- progress check sent, response or timeout, blocker or partial handoff, user recovery decision, cleanup, replacement or takeover, and evidence location

During final-review and close-out, record:
- unresolved fidelity gaps
- how they were resolved
- documentation updates required
- documentation updates completed
- final closure approval

After any material clarification or blocker, record:
- what was asked
- why it mattered
- the answer
- what changed because of it
- any correction where repo markdown artifacts overrode stale chat context

## Section Guidance

- `Purpose / Big Picture`: explain what the workflow is delivering, for whom, and what success looks like in one short paragraph.
- `Workflow Guidelines`: record the current orchestrator, current phase, workflow status, current gate decision needed when paused, and important constraints.
- `Artifact Map`: list the current source artifact paths and latest review-round paths in a compact table.
- `Progress`: use a compact current-state table, not a dated checklist.
- `Phase Ownership`: record the current operator, official reviewer roster, and sidecar/helper agents separately.
- `Phase Ownership`: when an operator is replaced or the orchestrator takes over, record the prior operator, replacement or takeover, and reason under substitutions or fallbacks.
- `Stage Assessments`: keep only the latest stage assessment plus unresolved prior warnings that still matter.
- `Decision Log`: record resolved decisions, accepted user feedback, material clarifications, and what changed because of them.
- `Current Blockers`: list active blockers and whether the workflow is waiting on the user, operator recovery, or remediation.
- `Resume Instructions`: state the exact next action and exact approval decision needed when paused.
- `Outcomes & Retrospective`: summarize what was delivered, deferred, learned, and documented only at completion.

When useful after long or messy threads, add a concise artifact-based restatement of current truth to `Resume Instructions` or `Decision Log`.

When delegating, prefer artifact paths and saved decision summaries in `Decision Log` over chat-history recap.

## Status Values

Use only these `workflow_status` values:
- `in-progress`
- `awaiting-user-approval`
- `awaiting-clarification`
- `blocked`
- `complete`

## Evidence Placement

- Put planned validation commands in `plan.md`.
- Put command results, changed areas, remediation evidence, and implementation deviations in `execution.md` when implementation has multiple steps, multiple validation commands, or remediation rounds.
- Put reviewer conclusions in review-round files.
- Record only pointers and current readiness in `run.md`.

## Example

```text
# Run - release-notes-tool

## Purpose / Big Picture
Build a lightweight internal release notes tool for product and engineering teams.

### Workflow Guidelines
- Orchestrator: active session
- Current phase: spec-review
- Workflow status: awaiting-user-approval
- Current gate decision needed: approve spec review resolution before plan-create

## Phase Ownership
- Current operator: Product Manager -> product_manager
- Official reviewers:
  - Software Architect -> software_architect
  - Stakeholder Advocate -> stakeholder_advocate
  - Skeptic -> skeptic
- Sidecar/helper agents: none
```
