# Run - {slug}

## Purpose / Big Picture
[What the workflow is delivering, for whom, and what success looks like.]

### Workflow Guidelines
- Orchestrator: [active session or concrete orchestrator]
- Current phase: [phase]
- Workflow status: [in-progress | awaiting-user-approval | awaiting-clarification | blocked | complete]
- Current gate decision needed: [exact approval or revision decision]
- Implementation-review satisfaction: [not-started | architecture/security/QA status]
- Documentation close-out status: [not-started | in-progress | complete]

## Artifact Map
| Artifact | Current path |
| --- | --- |
| Idea | `./docs/workflows/{slug}/idea.md` |
| Spec | `./docs/workflows/{slug}/spec.md` |
| Plan | `./docs/workflows/{slug}/plan.md` |
| Execution evidence | `./docs/workflows/{slug}/execution.md` when present |
| Latest idea review | `./docs/workflows/{slug}/reviews/idea/round-XX.md` |
| Latest spec review | `./docs/workflows/{slug}/reviews/spec/round-XX.md` |
| Latest plan review | `./docs/workflows/{slug}/reviews/plan/round-XX.md` |
| Latest implementation review | `./docs/workflows/{slug}/reviews/implementation/round-XX.md` |
| Latest final review | `./docs/workflows/{slug}/reviews/final/round-XX.md` |

## Progress
| Field | Value |
| --- | --- |
| Current stage | [stage] |
| Latest completed stage | [stage or none] |
| Next action | [exact next action] |
| Gate needed | [approval / clarification / none] |

## Phase Ownership
- Current operator: [Persona -> Agent]
- Official reviewers:
  - [Persona -> Agent]
- Sidecar/helper agents:
  - [Helper purpose -> Agent/display name, or none]
- Substitutions or fallbacks:
  - [Persona -> substituted persona/agent and reason, or none]

## Stage Assessments
- [Latest stage only] -> [Readiness, recommendation, and brief orchestrator rationale.]

## Decision Log
- [Material decision or accepted clarification] -> [Where it was written in the source artifacts.]

## Current Blockers
- [Blocker and whether the workflow is waiting on the user or remediation.]

## Resume Instructions
- [Exact next action.]
- [Exact gate or approval decision needed when paused.]

## Outcomes & Retrospective
- [Final delivery/deferred summary only when complete; otherwise `Not complete yet.`]
