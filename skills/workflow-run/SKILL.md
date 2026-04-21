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

Use [assets/run-template.md](./assets/run-template.md) as the default `run.md` skeleton when creating a new workflow dossier. Keep the section names aligned with the run-ledger contract in this skill.

This skill is the orchestrator. It stays in the active session, asks clarifying questions, delegates work to subagents, consolidates outputs, and asks the user when it is time to proceed.

Role model:
- agents define durable persona behavior
- skills define stage procedure and artifact contract
- the orchestrator assigns personas to stage skills and manages gating

Core model:
- the active session is always the orchestrator
- operators and reviewers are always subagents
- the orchestrator owns:
  - clarifying questions
  - stage transitions
  - user gates
  - official review-round files
  - run-ledger updates
  - reroute decisions
- operators own source-artifact drafting or implementation work for their phase
- reviewers provide findings and recommendations but do not own the source artifact

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
- treat `./docs/workflows/{slug}/run.md` as the source of truth for workflow state, current phase, artifact paths, reviewer rosters, approvals, blockers, and resume context
- start `run.md` with the exact H1 `# Run - {slug}`
- keep workflow guidance in plain text under a `### Workflow Guidelines` subsection inside `## Purpose / Big Picture`
- keep fixed dossier file names for:
  - `idea.md`
  - `spec.md`
  - `plan.md`
  - `execution.md`
- create new review rounds under:
  - `reviews/idea/round-XX.md`
  - `reviews/spec/round-XX.md`
  - `reviews/plan/round-XX.md`
  - `reviews/implementation/round-XX.md`
  - `reviews/final/round-XX.md`
- treat this workflow dossier contract as authoritative when this skill is active
- keep the repo markdown artifacts sufficient for another operator or orchestrator session to resume the workflow without prior chat history
- if the runtime does not support subagents well enough to run this model, stop and tell the user instead of silently degrading into a different workflow
- if a runtime-specific role registry exists, resolve stage-to-persona bindings through it and record the actual bindings used
- if a required concrete binding is missing and there is no valid substitute, stop and tell the user instead of silently inventing a replacement

Default phase ownership:
- `idea-create`
  - operator: `Product Strategist`
  - reviewers:
    - `Stakeholder Advocate`
    - `Product Designer` or `Domain Expert`
    - `Skeptic`
- `spec-create`
  - operator: `Product Manager`
  - reviewers:
    - `Software Architect`
    - `Stakeholder Advocate` or `Product Designer`
    - `Skeptic`
- `plan-create`
  - operator: `Software Architect`
  - reviewers:
    - `Software Architect`
    - `Software Engineer`
    - `Skeptic`
- `implement-plan`
  - operator: `Software Engineer`
- `implementation-review`
  - reviewers:
    - `Software Architect`
    - `Security Engineer`
    - `QA Engineer`
- `final-review`
  - reviewers:
    - `Product Manager` or `Product Strategist`
    - `Software Architect`
    - `QA Engineer`
- `docs close-out`
  - operator: `Documentation Maintainer`

Reviewer-count rule:
- idea, spec, and plan reviews always use exactly:
  - two substantive reviewers
  - one skeptic
- the second substantive reviewer may adapt to the workflow type, but the count does not change
- implementation review always uses exactly:
  - software architecture
  - security
  - QA

Role binding:
- when a runtime-specific registry exists, resolve each stage to:
  - the assigned personas
  - the default concrete agent name for each persona
  - any allowed substitutions for that assignment
- record the stage-to-persona and persona-to-agent bindings in `run.md`
- if a preferred agent is unavailable but an allowed substitute exists, record the substitution and continue
- if a required persona has no usable binding, stop and ask the user instead of silently weakening the review

At startup:
- treat startup as guided preflight, not as the beginning of stage execution
- derive the slug
- clarify the workflow goal, audience, constraints, and success criteria whenever needed
- resolve stage-to-persona bindings when a runtime registry exists
- explain that the active session will orchestrate subagents through:
  - idea
  - spec
  - plan
  - implementation
  - implementation review
  - final review
  - docs close-out
- explain that user approval is required after:
  - idea review resolution
  - spec review resolution
  - plan review resolution
  - implementation-review resolution
  - final-review gap resolution plus docs close-out
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

Clarification rule:
- ask questions whenever clarity is needed for correctness, scope, contract fidelity, or implementation safety
- do not defer material ambiguity simply to stay moving
- record resolved decisions and material clarifications in `run.md`

Re-grounding rule:
- treat repo markdown artifacts as the authoritative working context and treat long chat history as convenience context only
- before each stage transition, re-read `run.md` and the source artifacts for the next stage and continue from those files rather than from memory alone
- after each user gate, reroute, or remediation loop, explicitly re-ground on the current markdown artifacts before making the next stage decision
- if chat context conflicts with the current repo markdown artifacts, prefer the markdown artifacts and record the discrepancy in `run.md`
- when the thread has become long, repetitive, or contradictory, perform a concise artifact-based restatement of the current truth before proceeding
- do not carry accepted decisions, constraints, or clarifications forward as chat-only context; write them into `run.md` or the relevant source artifact before relying on them
- before starting a new phase, confirm that accepted user feedback and accepted review outcomes are reflected in the repo markdown artifacts
- when delegating to subagents, ground the task in artifact paths and saved decisions rather than relying on conversational recap alone

Delegation scope rule:
- delegate with exact artifact paths, the assigned persona/lens, and the specific decision or artifact needed next
- instruct subagents to read the named markdown artifacts first and treat them as the primary context
- avoid broad repo scans unless the task requires implementation evidence, unresolved source context, or a finding depends on code-level detail
- when broader inspection is necessary, keep it targeted to named paths, symbols, or terms and ask the subagent to report what it inspected
- prefer compact subagent outputs: the conclusion, the reasoning needed to support it, and the smallest useful set of findings or edits

Execution model:
1. confirm the workflow ask, slug, constraints, and guided phase order
2. resolve the concrete subagent binding for every stage persona
3. record the chosen stage-to-persona and persona-to-agent bindings in `run.md`
4. re-ground on `run.md` plus the source artifacts for the current stage and restate the current artifact-based truth before delegating work
5. delegate the current create stage and the matching formal review stage using artifact paths and saved decisions as the primary task context
6. write the consolidated official review round
7. fold accepted review decisions back into the source artifact
8. present the result to the user at the required gate
9. after the user gate, record the user's feedback, ensure accepted feedback is written into repo markdown artifacts, and then re-ground on the updated artifacts before advancing, looping, or rerouting
10. after implementation, run `implementation-review`
11. if any implementation reviewer requires material changes, route work back to `implement-plan`, re-ground on the updated artifacts, and repeat
12. after implementation review approval, run `final-review`
13. if final review finds fidelity gaps, route fixes back to the owning operator, re-ground on the updated artifacts, and rerun review as needed
14. delegate docs close-out to the documentation maintainer
15. verify docs close-out, re-ground on the final markdown artifacts, ask for final approval, and then close the workflow

Advancement rules:
- do not advance from idea until the idea is specific enough to support spec creation
- do not advance from spec until the contract is specific enough to support planning
- do not advance from plan until the implementation approach is specific enough to support engineering execution
- do not advance when the markdown artifacts in the repo are insufficient for the next stage to continue without chat history
- do not advance when accepted user feedback or accepted review outcomes still live only in chat context
- do not leave implementation review until architecture, security, and QA all recommend proceeding
- do not close the workflow until:
  - final-review gaps are resolved
  - required repo documentation is updated
  - the user gives final approval

Looping and reroute rules:
- prefer revising the current phase over advancing with unresolved material defects
- if a later phase exposes an earlier-phase contract problem, reroute to the earliest broken phase
- if implementation reveals a needed contract change, update the spec before resuming implementation
- if implementation review fails:
  - rerun `implement-plan`
  - then rerun `implementation-review`
- if final review finds fidelity gaps, route the fixes back to the operator who owns the affected work
- after any reroute or remediation cycle, re-ground on `run.md` plus the updated markdown artifacts before resuming orchestration
- after any user feedback that changes the direction, ensure the accepted change is written into repo markdown artifacts before delegating more work

Run ledger structure:
- maintain these required sections:
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

Run ledger update rules:
- after startup confirmation, record:
  - the original workflow ask
  - the canonical slug
  - the current orchestrator
  - the concrete persona-to-agent bindings used
  - any substitutions or fallbacks used
  - the initial user constraints and clarifications
  - the fact that the user approved the guided workflow start
- before each create stage, record:
  - current operator
  - current reviewer roster
  - current phase objective
  - the artifact-based restatement of current truth used to start the phase
- after each create stage, update:
  - `Artifact Map`
  - `Progress`
  - `Resume Instructions`
- after each review stage, record:
  - reviewed artifact path
  - official review round path
  - operator for the phase
  - reviewer roster for the phase
  - reviewer display names when the runtime exposes them
  - brief reviewer synopses preserved in the official review artifact
  - recommendation
  - orchestrator consolidation rationale
- after each user gate, record:
  - what the user reviewed
  - approval or revision decision
  - any conditions the user attached to proceeding
  - the artifact-based re-grounding summary used before the next step when one was needed
  - where accepted feedback was written in the repo markdown artifacts
- during implementation review, record:
  - satisfaction status for architecture
  - satisfaction status for security
  - satisfaction status for QA / product correctness
  - the remediation cycle count
- during final-review and close-out, record:
  - unresolved fidelity gaps
  - how they were resolved
  - documentation updates required
  - documentation updates completed
  - final closure approval
- after any material clarification or blocker, record:
  - what was asked
  - why it mattered
  - the answer
  - what changed because of it
  - any correction where repo markdown artifacts overrode stale chat context

Section guidance:
- `Purpose / Big Picture`: explain what the workflow is delivering, for whom, and what success looks like
- `Workflow Guidelines`: record the current orchestrator, current phase, workflow status, current gate decision needed when paused, and any important constraints
- `Artifact Map`: list the current paths for:
  - `idea.md`
  - latest idea review round
  - `spec.md`
  - latest spec review round
  - `plan.md`
  - latest plan review round
  - `execution.md` when present
  - latest implementation review round
  - latest final review round
- `Phase Ownership`: record the current operator subagent and the reviewer roster for the phase
- `Stage Assessments`: summarize phase readiness, recommendations, and why the orchestrator advanced or looped
- `Decision Log`: record resolved decisions, accepted user feedback, material clarifications, and what changed because of them
- `Current Blockers`: list active blockers and whether the workflow is waiting on the user or on remediation
- `Resume Instructions`: state the exact next action and the exact approval decision needed when paused
- `Outcomes & Retrospective`: summarize what was delivered, deferred, learned, and documented
- when useful after long or messy threads, add a concise artifact-based restatement of current truth to `Resume Instructions` or `Decision Log`
- when delegating, prefer artifact paths and saved decision summaries in `Decision Log` over chat-history recap

Use `workflow_status` values such as:
- `in-progress`
- `awaiting-user-approval`
- `awaiting-clarification`
- `blocked`
- `complete`

Run ledger example:
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
- Current operator: Product Manager
- Reviewers:
  - Software Architect
  - Stakeholder Advocate
  - Skeptic
```

Finish the workflow with:
- final artifact paths
- final workflow status
- final operator / reviewer outcome where relevant
- assumptions that materially shaped the result
- blockers or follow-up work that prevented full closure, if any
