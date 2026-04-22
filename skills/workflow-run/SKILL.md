---
name: workflow-run
description: Coordinate the full workflow from idea through close-out using the active session as orchestrator, subagents as operators and reviewers, and explicit user gates between major phases. Use when the user wants guided orchestration rather than a one-shot stage run.
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
- `implementation-review`
- `final-review`

Use [assets/run-template.md](./assets/run-template.md) as the default `run.md` skeleton when creating a workflow dossier.

Read [references/run-ledger.md](./references/run-ledger.md) only when creating or updating `run.md`, resuming a workflow, resolving a user gate, or handling a reroute/remediation loop.

This skill is the orchestrator. It stays in the active session, asks clarifying questions, delegates work to subagents, consolidates outputs, and asks the user when it is time to proceed.

## Core Model

- agents define durable persona behavior
- skills define stage procedure and artifact contract
- the active session is always the orchestrator
- operators and reviewers are always subagents
- the orchestrator owns clarifying questions, stage transitions, user gates, official review-round files, run-ledger updates, and reroute decisions
- operators own source-artifact drafting, accepted source-artifact revisions, implementation work, and implementation remediations for their phase
- reviewers provide findings and recommendations but do not own the source artifact
- if the runtime does not support subagents well enough to run this model, stop and tell the user instead of silently degrading into a different workflow

## Workflow Contract

Canonical phase order:
1. `idea-create`
2. `idea-review`
3. user gate
4. `spec-create`
5. `spec-review`
6. user gate
7. `plan-create`
8. `plan-review`
9. user gate
10. `implement-plan`
11. `implementation-review`
12. user gate
13. `final-review`
14. resolve final gaps with the user
15. docs close-out
16. final user approval and workflow closure

Requirements:
- derive one canonical `slug` from the starting prompt and keep the workflow dossier under `./docs/workflows/{slug}/`
- treat `./docs/workflows/{slug}/run.md` as the source of truth for workflow state, artifact paths, role bindings, approvals, blockers, and resume context
- start `run.md` with the exact H1 `# Run - {slug}`
- keep `run.md` as a compact restart ledger, not a chronology, validation log, or implementation journal
- do not add `Validation Evidence` to `run.md`; point to `plan.md`, `execution.md`, or review artifacts instead
- keep fixed dossier file names: `idea.md`, `spec.md`, `plan.md`, and optional `execution.md`
- create new zero-padded review rounds under:
  - `reviews/idea/round-XX.md`
  - `reviews/spec/round-XX.md`
  - `reviews/plan/round-XX.md`
  - `reviews/implementation/round-XX.md`
  - `reviews/final/round-XX.md`
- keep repo markdown artifacts sufficient for another operator or orchestrator session to resume the workflow without prior chat history
- if a runtime-specific role registry exists, resolve stage-to-persona bindings through it and record the actual bindings used
- if a required concrete binding is missing and there is no valid substitute, stop and tell the user instead of silently inventing a replacement

## Phase Ownership

- `idea-create`: operator `Product Strategist`; reviewers `Stakeholder Advocate`, `Product Designer` or `Domain Expert`, and `Skeptic`
- `spec-create`: operator `Product Manager`; reviewers `Software Architect`, `Stakeholder Advocate` or `Product Designer`, and `Skeptic`
- `plan-create`: operator `Software Architect`; reviewers `Software Architect`, `Software Engineer`, and `Skeptic`
- `implement-plan`: operator `Software Engineer`
- `implementation-review`: reviewers `Software Architect`, `Security Engineer`, and `QA Engineer`
- `final-review`: reviewers `Product Manager` or `Product Strategist`, `Software Architect`, and `QA Engineer`
- docs close-out: operator `Documentation Maintainer`

Reviewer-count rule:
- idea, spec, and plan reviews always use exactly two substantive reviewers plus one skeptic
- the second substantive reviewer may adapt to the workflow type, but the count does not change
- implementation review always uses exactly software architecture, security, and QA

## Role Binding

- when a runtime-specific registry exists, resolve each stage to the assigned personas, default concrete agent names, and allowed substitutions
- record stage-to-persona and persona-to-agent bindings in `run.md`
- if a preferred agent is unavailable but an allowed substitute exists, record the substitution and continue
- if a required persona has no usable binding, stop and ask the user instead of silently weakening the review
- official operators and reviewers must be spawned as the resolved concrete persona agent, or an explicitly allowed substitute, and the spawned agent type must match before the output is treated as official workflow work
- for Codex, use the registry `agent` value as the spawned subagent `agent_type`; prompt text such as "you are {Persona}" does not turn `worker`, `explorer`, or `default` into an official workflow persona
- generic helper agents may be used only for sidecar discovery or bounded support work; record them separately from official operator/reviewer rosters

## Startup

- treat startup as guided preflight, not as the beginning of stage execution
- derive the slug, clarify goal/audience/constraints/success criteria whenever needed, and resolve role bindings
- explain that the active session will orchestrate subagents through idea, spec, plan, implementation, implementation review, final review, and docs close-out
- explain that user approval is required after idea review resolution, spec review resolution, plan review resolution, implementation-review resolution, and final-review gap resolution plus docs close-out
- present one concise start confirmation before the first stage begins
- do not begin `idea-create` until the user confirms the startup summary

Use a plain-language startup confirmation such as:
- `Here is how I will run this workflow:`
- `- Workflow ask: Build a lightweight internal release notes tool for product and engineering teams.`
- `- Canonical slug: release-notes-tool`
- `- Orchestrator: active session`
- `- Bound product strategist persona: product_strategist`
- `- Idea operator: Product Strategist`
- `- Spec operator: Product Manager`
- `- Plan operator: Software Architect`
- `- Implementation operator: Software Engineer`
- `- User approvals required after idea, spec, plan, implementation review, and close-out`
- `Reply 'start' to begin, or tell me what to change.`

## Grounding And Clarification

- ask questions whenever clarity is needed for correctness, scope, contract fidelity, or implementation safety
- do not defer material ambiguity simply to stay moving
- record resolved decisions and material clarifications in `run.md`
- treat repo markdown artifacts as authoritative and long chat history as convenience context only
- before each stage transition, re-read `run.md` and the source artifacts for the next stage
- after each user gate, reroute, or remediation loop, explicitly re-ground on the current markdown artifacts before making the next stage decision
- if chat context conflicts with repo markdown artifacts, prefer the artifacts and record the discrepancy in `run.md`
- do not carry accepted decisions, constraints, or clarifications forward as chat-only context; write them into `run.md` or the relevant source artifact before relying on them
- do not duplicate the same accepted decision across every artifact; write it to the artifact that owns it and point other artifacts to that source when needed

## Delegation And Context Budget

- delegate with exact artifact paths, the assigned persona/lens, and the specific decision or artifact needed next
- instruct subagents to read named markdown artifacts first and treat them as primary context
- delegate with artifact paths instead of pasted artifact contents whenever files are available in the workspace
- do not include long chat-history summaries when `run.md` and source artifacts contain the needed context
- ask subagents to return only decisions, findings, edits made, and unresolved blockers
- prohibit long restatements of artifacts, chat history, or reviewer transcripts
- for focused re-reviews, ask reviewers to inspect only the prior finding, current artifact, and changed area
- target saved review rounds at roughly 250-500 words unless material findings require more
- idea, spec, and plan reviews should normally inspect only `run.md` plus the relevant workflow artifacts
- codebase inspection should be targeted and usually reserved for implementation, implementation-review, final-review fidelity checks, or a specific blocking question
- generic helper agents may be used only for narrow blocking questions with named paths, symbols, or terms
- start with the required operator or reviewer set for the current phase
- do not spawn sidecar agents unless a specific blocker or unknown must be resolved
- if token or host pressure is high, run reviewers sequentially and avoid optional sidecars
- expand the reviewer or helper set only when the added agent has a distinct question that materially affects the next gate
- after a subagent's output has been captured in the relevant markdown artifact, close or release that subagent when the runtime supports it
- do not keep completed reviewers or operators alive across user gates unless they are actively needed for the next delegated task

## Execution Loop

1. Confirm the workflow ask, slug, constraints, and guided phase order.
2. Resolve concrete subagent bindings for every stage persona and record them in `run.md`.
3. Re-ground on `run.md` plus source artifacts for the current stage and restate the artifact-based truth before delegating work.
4. Delegate the current create stage to the owning operator using artifact paths and saved decisions as primary task context.
5. Verify the created or updated source artifact before launching review.
6. Delegate the formal review stage to the resolved reviewer agents.
7. Write the consolidated official review round.
8. Delegate accepted source-artifact revisions or implementation remediations back to the owning operator subagent.
9. Verify the updated artifact or implementation diff, then update `run.md` with the accepted decision and revision outcome.
10. Present the result to the user at the required gate.
11. After the user gate, record feedback, ensure accepted feedback is written into repo markdown artifacts through the owning operator when edits are needed, and re-ground before advancing, looping, or rerouting.
12. After implementation, run `implementation-review`; if any implementation reviewer requires material changes, route remediation back to the implementation operator and repeat.
13. After implementation-review approval, run `final-review`; if it finds fidelity gaps, route fixes back to the owning operator and rerun review as needed.
14. Before docs close-out, run a drift sweep across `idea.md`, `spec.md`, `plan.md`, `execution.md` when present, and latest reviews to catch stale wording after later decisions.
15. Delegate docs close-out to the documentation maintainer.
16. Verify docs close-out, re-ground on final markdown artifacts, ask for final approval, and close the workflow.

## Advancement And Reroute Rules

- do not advance from idea until the idea is specific enough to support spec creation
- do not advance from spec until the contract is specific enough to support planning
- do not advance from plan until the implementation approach is specific enough to support engineering execution
- do not advance when repo markdown artifacts are insufficient for the next stage to continue without chat history
- do not advance when accepted user feedback or accepted review outcomes still live only in chat context
- do not leave implementation review until architecture, security, and QA all recommend proceeding
- do not close the workflow until final-review gaps are resolved, required repo documentation is updated, and the user gives final approval
- prefer revising the current phase over advancing with unresolved material defects
- if a later phase exposes an earlier-phase contract problem, reroute to the earliest broken phase
- if implementation reveals a needed contract change, update the spec before resuming implementation
- if implementation review fails, rerun `implement-plan` and then rerun `implementation-review`
- if final review finds fidelity gaps, route fixes back to the operator who owns the affected work
- after any reroute, remediation cycle, or direction-changing user feedback, update the relevant repo markdown artifacts before delegating more work
- if later accepted decisions make earlier artifacts stale, route a concise correction to that artifact's owning operator before closure

Finish the workflow with:
- final artifact paths
- final workflow status
- final operator / reviewer outcome where relevant
- assumptions that materially shaped the result
- blockers or follow-up work that prevented full closure, if any
