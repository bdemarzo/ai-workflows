# Run - {slug}

## Purpose / Big Picture
[What the workflow is delivering, for whom, and what success looks like.]

### Workflow Guidelines
- Orchestrator: [active session or concrete orchestrator]
- Current phase: [phase]
- Workflow status: [in-progress | awaiting-user-approval | awaiting-clarification | blocked | complete]
- Current gate decision needed: [exact approval or revision decision]
- Important constraints: [constraint]
- Implementation-review satisfaction: [not-started | architecture/security/QA status]
- Documentation close-out status: [not-started | in-progress | complete]

## Artifact Map
- `./docs/workflows/{slug}/idea.md`
- `./docs/workflows/{slug}/spec.md`
- `./docs/workflows/{slug}/plan.md`
- `./docs/workflows/{slug}/execution.md` when present
- Latest review rounds:
  - `./docs/workflows/{slug}/reviews/idea/round-XX.md`
  - `./docs/workflows/{slug}/reviews/spec/round-XX.md`
  - `./docs/workflows/{slug}/reviews/plan/round-XX.md`
  - `./docs/workflows/{slug}/reviews/implementation/round-XX.md`
  - `./docs/workflows/{slug}/reviews/final/round-XX.md`

## Progress
- [Current workflow progress summary.]

## Phase Ownership
- Current operator: [Persona -> Agent]
- Official reviewers:
  - [Persona -> Agent]
- Sidecar/helper agents:
  - [Helper purpose -> Agent/display name, or none]
- Substitutions or fallbacks:
  - [Persona -> substituted persona/agent and reason, or none]

## Stage Assessments
- [Phase] -> [Readiness, recommendation, and orchestrator rationale.]

## Decision Log
- [Decision or accepted clarification] -> [What changed in the workflow artifacts]

## Current Blockers
- [Blocker and whether the workflow is waiting on the user or remediation.]

## Resume Instructions
- [Exact next action.]
- [Exact gate or approval decision needed when paused.]

## Outcomes & Retrospective
- [What was delivered, deferred, learned, and documented.]
