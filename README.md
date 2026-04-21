# ai-workflows

Portable workflow skills for AI-assisted product and engineering work, plus a Codex adapter layer.

This repo defines a guided workflow where the active AI session is the orchestrator and subagents act as operators and reviewers. The orchestrator asks clarifying questions when needed, presents each major phase to the user, and requires approval before moving forward.

## What You Get

- `workflow-run` to orchestrate the full workflow
- operator playbooks for:
  - `idea-create`
  - `spec-create`
  - `plan-create`
  - `implement-plan`
- review playbooks for:
  - `idea-review`
  - `spec-review`
  - `plan-review`
  - `implementation-review`
  - `final-review`
- `skeptical-review` as an optional manual pressure-test outside the main workflow

## Core Model

- The active session is always the orchestrator.
- Operators and reviewers are always subagents.
- Agents define durable persona behavior.
- Skills define the stage procedure and artifact contract.
- Operators own drafting or implementation work for their phase.
- Reviewers provide findings and recommendations but do not own the source artifact.
- The orchestrator writes the official consolidated review rounds.
- The user gates progress between major phases.

## Repo Layers

This repo is organized in layers:

- `skills/`
  - the portable workflow contract
  - copy these into an agent's skills folder
- `.codex/`
  - the Codex-specific adapter layer
  - copy this into a target repository when you want Codex to execute the workflow with named subagents

## Codex Adapter Layer

The skills in [skills/](/C:/git/bdcf/ai-workflows/skills) stay portable and stage-oriented. For Codex, this repo also includes an optional project-scoped adapter layer under [.codex/](/C:/git/bdcf/ai-workflows/.codex).

This follows the OpenAI Codex subagents model: custom agents can be defined as standalone TOML files in `.codex/agents/`, while the parent session remains the orchestrator. See [OpenAI Codex Subagents](https://developers.openai.com/codex/subagents).

The Codex adapter layer in this repo has three pieces:
- [.codex/agents/](/C:/git/bdcf/ai-workflows/.codex/agents) for concrete persona agents
- [.codex/role-registry.toml](/C:/git/bdcf/ai-workflows/.codex/role-registry.toml) for mapping workflow stages to persona labels and then to concrete Codex agent names
- [.codex/config.toml](/C:/git/bdcf/ai-workflows/.codex/config.toml) for global subagent limits

The starter scaffold included here maps workflow personas to named Codex agents such as:
- `product_strategist`
- `product_manager`
- `software_architect`
- `software_engineer`
- `product_designer`
- `domain_expert`
- `stakeholder_advocate`
- `skeptic`
- `security_engineer`
- `qa_engineer`
- `documentation_maintainer`

The included [.codex/config.toml](/C:/git/bdcf/ai-workflows/.codex/config.toml) also sets conservative global subagent limits for Codex:
- `max_threads = 6`
- `max_depth = 1`

Use this layer when you want the orchestrator to call stable, named Codex subagents instead of reconstructing persona instructions every run.

The shared `Software Architect` persona in this repo is intended to drive bounded, full-stack execution planning:
- prefer the simplest viable design that satisfies the approved contract
- reuse existing patterns before introducing new abstractions, services, or dependencies
- justify each layer in present-tense terms rather than future-proofing by default
- keep recommendations concrete, defensible, and easy for the next engineer to follow

The intended split is:
- agent = persona/stable behavior
- skill = stage procedure, inputs, outputs, and boundaries
- orchestrator = stage-to-persona assignment plus gating

## Workflow

The canonical workflow is:

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

`workflow-run` is the orchestrator. It is not a stage.

## Stage Ownership

### Idea
- Operator: `Product Strategist`
- Reviewers:
  - `Stakeholder Advocate`
  - `Product Designer` or `Domain Expert`
  - `Skeptic`

### Spec
- Operator: `Product Manager`
- Reviewers:
  - `Software Architect`
  - `Stakeholder Advocate` or `Product Designer`
  - `Skeptic`

### Plan
- Operator: `Software Architect`
- Reviewers:
  - `Software Architect`
  - `Software Engineer`
  - `Skeptic`

### Implementation
- Operator: `Software Engineer`

### Implementation Review
- Reviewers:
  - `Software Architect`
  - `Security Engineer`
  - `QA Engineer`

### Final Review
- Orchestrator-led synthesis with reviewer lenses such as:
  - `Product Manager` or `Product Strategist`
  - `Software Architect`
  - `QA Engineer`

### Docs Close-Out
- Operator: `Documentation Maintainer`

## Review Rules

For `idea`, `spec`, and `plan`:
- each review uses exactly:
  - two substantive reviewers
  - one skeptic
- the second substantive reviewer may adapt to the workflow type, but the reviewer count does not change

For `implementation-review`:
- the reviewer set is fixed:
  - software architecture
  - security
  - QA
- QA should explicitly consider regressions, edge cases, and unit-test coverage expectations

Saved review rounds should stay concise and findings-first:
- keep reviewer rosters visible
- include the concrete agent id and display name when the runtime exposes one
- preserve a short synopsis of what each reviewer actually argued, not just the merged conclusion
- merge overlapping findings
- preserve only disagreements that materially affect the recommendation
- if the markdown artifacts in the repo are insufficient for the next stage to continue, record that as a key finding rather than a standalone restartability section

## Workflow Dossier

Each workflow should live under one dossier:

```text
docs/workflows/{slug}/
  run.md
  idea.md
  spec.md
  plan.md
  execution.md
  reviews/
    idea/round-01.md
    spec/round-01.md
    plan/round-01.md
    implementation/round-01.md
    final/round-01.md
```

Use one canonical `slug` per workflow. Create a new review round for each pass instead of overwriting earlier review files.

The workflow must remain resumable from the markdown artifacts in the repo alone. Reviewers should treat any gap in that handoff chain as a key finding.

Use `run.md` as the workflow ledger, not as a test report. It should include a `Decision Log` for resolved decisions, accepted feedback, and material clarifications. Validation details belong in `plan.md`, `execution.md`, or review artifacts when they are needed for that phase.

## How It Works

In normal use, `workflow-run` will:

- resolve stage-to-persona bindings through the runtime role registry when one exists
- record the actual persona-to-agent bindings used for the run
- clarify the goal, audience, constraints, and success criteria when needed
- confirm the guided workflow before the first phase starts
- re-ground on `run.md` and the current markdown artifacts at phase boundaries instead of trusting long chat history
- delegate creation work to the current phase operator subagent
- delegate formal review work to the current phase reviewer subagents
- write the official review artifact for the phase
- present the result to the user
- ask whether to proceed
- keep `docs/workflows/{slug}/run.md` current as the restartable workflow ledger

The orchestrator should ask questions whenever clarity is needed. The workflow should not rely on autonomous straight-through execution as its primary mode.

The orchestrator should treat the repo markdown artifacts as the authoritative working context. If chat history conflicts with the saved artifacts, the saved artifacts win and the discrepancy should be recorded.

Accepted user feedback and accepted review outcomes should not remain chat-only. Before the next phase begins, they should be written into `run.md` or the relevant workflow artifact, and subagent delegation should be grounded in those saved artifacts.

If a runtime-specific role registry is missing or incomplete, the orchestrator should fall back explicitly and record that fallback in `run.md` instead of silently improvising.

## Stage Outputs

| Stage | Purpose | Output |
| --- | --- | --- |
| `idea-create` | Shape the product idea and expected value. | `docs/workflows/{slug}/idea.md` |
| `idea-review` | Review the idea before spec work. | `docs/workflows/{slug}/reviews/idea/round-01.md` |
| `spec-create` | Turn the idea into a functional product contract. | `docs/workflows/{slug}/spec.md` |
| `spec-review` | Review the spec before planning. | `docs/workflows/{slug}/reviews/spec/round-01.md` |
| `plan-create` | Turn the spec into an implementation-ready plan. | `docs/workflows/{slug}/plan.md` |
| `plan-review` | Review the plan before implementation. | `docs/workflows/{slug}/reviews/plan/round-01.md` |
| `implement-plan` | Implement the approved plan. | code changes plus optional `docs/workflows/{slug}/execution.md` |
| `implementation-review` | Review implementation with architecture, security, and QA/product-correctness lenses. | `docs/workflows/{slug}/reviews/implementation/round-01.md` |
| `final-review` | Check fidelity against idea, spec, plan, and implementation evidence. | `docs/workflows/{slug}/reviews/final/round-01.md` |
| docs close-out | Update repository documentation before closure. | repo docs updates plus closure recorded in `run.md` |

## Example Prompt

```text
Use workflow-run for this feature.
Ask questions whenever clarity is needed.
Use subagents for operators and reviewers.
Gate each major phase with me before proceeding.

Build a customer-facing saved views experience for our reporting dashboard.
```

## Optional Manual Skill

`skeptical-review` is still available as an optional manual pressure-test. It is separate from the mandatory `Skeptic` reviewer already present in the normal idea/spec/plan review phases.

## Install for Codex

Copy any skill folder from `skills/` into your agent's skills directory. For Codex, that is typically:

```text
skills/workflow-run -> ~/.codex/skills/workflow-run
skills/implement-plan -> ~/.codex/skills/implement-plan
skills/implementation-review -> ~/.codex/skills/implementation-review
skills/skeptical-review -> ~/.codex/skills/skeptical-review
```

To install everything, copy each folder under `skills/` into:

```text
~/.codex/skills/
```

If you want the Codex adapter behavior in a target repository, also copy the project-scoped `.codex/` folder into that repository root:

```text
.codex/agents/
.codex/role-registry.toml
.codex/config.toml
```

That adapter layer is what makes the stage-assigned personas resolve to stable named Codex subagents.

## Repository Layout

- `skills/` - canonical skill packages
- `.codex/agents/` - optional Codex-specific subagent runtime definitions
- `.codex/role-registry.toml` - optional Codex-specific stage-to-persona-to-agent binding registry
- `.codex/config.toml` - optional Codex-specific subagent runtime settings
- `skills/<skill-name>/assets/` - optional skill-local templates and reference assets
- `docs/` - supporting docs
- `README.md` - human-facing workflow overview

## Skill Templates

Artifact-producing skills may include skill-local templates under `assets/` so the skill remains usable when copied on its own. Keep long templates in `assets/` and have `SKILL.md` point to them explicitly when they should be used.

## Notes

- The workflow skills are portable by design; the shipped adapter layer in this repo is Codex-specific.
- The repo no longer ships a runtime-neutral persona catalog; `.codex/` is the only persona binding layer included here.
- `plan.md` is the authoritative implementation document for the workflow once implementation starts.
- `execution.md` is optional and should be used as an evidence appendix rather than a second control document.
- Repo-local `PLANS.md` can be useful project context, but it should not silently override this workflow contract.
