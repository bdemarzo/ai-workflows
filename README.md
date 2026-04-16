# ai-workflows

Codex-first workflow skills for AI-assisted product and engineering work.

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
- Agents define durable role behavior.
- Skills define the stage procedure and artifact contract.
- Operators own drafting or implementation work for their phase.
- Reviewers provide findings and recommendations but do not own the source artifact.
- The orchestrator writes the official consolidated review rounds.
- The user gates progress between major phases.

## Codex Runtime Layer

The skills in [skills/](/C:/git/bdcf/ai-workflows/skills) stay portable and role-based. For Codex, this repo now also includes an optional project-scoped runtime layer under [.codex/agents/](/C:/git/bdcf/ai-workflows/.codex/agents).

This follows the OpenAI Codex subagents model: custom agents can be defined as standalone TOML files in `.codex/agents/`, while the parent session remains the orchestrator. See [OpenAI Codex Subagents](https://developers.openai.com/codex/subagents).

The Codex runtime layer in this repo now has three pieces:
- [.codex/agents/](/C:/git/bdcf/ai-workflows/.codex/agents) for concrete role agents
- [.codex/role-registry.toml](/C:/git/bdcf/ai-workflows/.codex/role-registry.toml) for mapping abstract workflow roles to concrete agent names and substitutions
- [.codex/config.toml](/C:/git/bdcf/ai-workflows/.codex/config.toml) for global subagent limits

The starter scaffold included here maps the workflow roles to named Codex agents such as:
- `product_strategist`
- `technical_product_manager`
- `implementation_planner`
- `skeptic`
- `expert_engineer`
- `architecture_reviewer`
- `security_reviewer`
- `qa_product_correctness_reviewer`
- `product_fidelity_reviewer`
- `plan_fidelity_reviewer`
- `qa_regression_reviewer`
- `documentation_maintainer`

The included [.codex/config.toml](/C:/git/bdcf/ai-workflows/.codex/config.toml) also sets conservative global subagent limits for Codex:
- `max_threads = 6`
- `max_depth = 1`

Use this layer when you want the orchestrator to call stable, named Codex subagents instead of reconstructing role instructions every run.

The intended split is:
- agent = role/persona/stable behavior
- skill = stage procedure, inputs, outputs, and boundaries
- orchestrator = role-to-skill assignment plus gating

## Workflow Modes

`workflow-run` should resolve one workflow mode at startup:
- `light`
- `standard`
- `heavy`

`light`
- for small, localized, low-risk work
- may compress `idea-create` and `spec-create` into one discovery cycle before the first user gate
- still leaves both `idea.md` and `spec.md` in the dossier
- early reviews use one substantive reviewer plus one skeptic
- `implementation-review`, `final-review`, and docs close-out remain mandatory

`standard`
- default mode
- full `idea -> spec -> plan -> implement -> implementation-review -> final-review -> docs close-out`
- early reviews use two substantive reviewers plus one skeptic
- user gates remain between major phases

`heavy`
- for high-risk, cross-cutting, security-sensitive, or high-blast-radius work
- same stage order as `standard`
- early reviews use two substantive reviewers plus one skeptic
- the orchestrator should ask more clarifying questions, preserve more dissent, and require stronger validation before advancing

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
  - `Stakeholder Value Reviewer`
  - `UX / Product Design Reviewer` or `Domain Reviewer`
  - `Skeptic`

### Spec
- Operator: `Technical Product Manager`
- Reviewers:
  - `Architect Reviewer`
  - `Stakeholder / Power User Reviewer` or `UX / Product Design Reviewer`
  - `Skeptic`

### Plan
- Operator: `Architect / Implementation Planner`
- Reviewers:
  - `Senior Engineer Reviewer`
  - `Delivery / Systems Reviewer` or `Frontend Delivery Reviewer`
  - `Skeptic`

### Implementation
- Operator: `Expert Engineer`

### Implementation Review
- Reviewers:
  - `Architecture Reviewer`
  - `Security Reviewer`
  - `QA / Product Correctness Reviewer`

### Final Review
- Orchestrator-led synthesis with reviewer lenses such as:
  - `Product Fidelity Reviewer`
  - `Plan Fidelity Reviewer`
  - `QA / Regression Reviewer`

### Docs Close-Out
- Operator: `Documentation Maintainer`

## Review Rules

For `idea`, `spec`, and `plan` in `standard` and `heavy` mode:
- each review uses exactly:
  - two substantive reviewers
  - one skeptic
- the second substantive reviewer may adapt to the workflow type, but the reviewer count does not change

For `idea`, `spec`, and `plan` in `light` mode:
- each review uses:
  - one substantive reviewer
  - one skeptic
- the substantive reviewer should be chosen by dominant risk for the phase

For `implementation-review`:
- the reviewer set is fixed:
  - architecture
  - security
  - QA / product correctness
- QA / product correctness should explicitly consider regressions, edge cases, and unit-test coverage expectations

Saved review rounds should stay concise and findings-first:
- keep reviewer rosters visible
- merge overlapping findings
- preserve only disagreements that materially affect the recommendation

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

## How It Works

In normal use, `workflow-run` will:

- resolve `light`, `standard`, or `heavy` mode
- resolve workflow roles through the runtime role registry when one exists
- record the actual role-to-agent bindings used for the run
- clarify the goal, audience, constraints, and success criteria when needed
- confirm the guided workflow before the first phase starts
- delegate creation work to the current phase operator subagent
- delegate review work to the current phase reviewer subagents
- write the official review artifact for the phase
- present the result to the user
- ask whether to proceed
- keep `docs/workflows/{slug}/run.md` current as the restartable workflow ledger

The orchestrator should ask questions whenever clarity is needed. The workflow should not rely on autonomous straight-through execution as its primary mode.

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
Use standard mode unless the task is clearly small enough for light mode.

Build a customer-facing saved views experience for our reporting dashboard.
```

## Optional Manual Skill

`skeptical-review` is still available as an optional manual pressure-test. It is separate from the mandatory `Skeptic` reviewer already present in the standard idea/spec/plan review phases.

## Install for Codex

Copy any skill folder from `skills/` into your Codex skills directory:

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

If you want the Codex-first runtime behavior in a target repository, also copy the project-scoped Codex runtime layer into that repository root:

```text
.codex/agents/
.codex/role-registry.toml
.codex/config.toml
```

That runtime layer is what makes the abstract workflow roles resolve to stable named Codex subagents.

## Repository Layout

- `skills/` - canonical skill packages
- `.codex/agents/` - optional Codex-specific subagent runtime definitions
- `.codex/role-registry.toml` - optional Codex-specific role-to-agent binding registry
- `.codex/config.toml` - optional Codex-specific subagent runtime settings
- `docs/examples/` - example workflow dossiers
- `docs/` - supporting docs and artifact examples
- `README.md` - human-facing workflow overview

## Examples

The repo includes example dossiers under [docs/examples/](/C:/git/bdcf/ai-workflows/docs/examples):
- [standard-saved-views](/C:/git/bdcf/ai-workflows/docs/examples/standard-saved-views) for a `standard` workflow
- [light-profile-copy-refresh](/C:/git/bdcf/ai-workflows/docs/examples/light-profile-copy-refresh) for a `light` workflow

Each example shows the expected dossier shape, review rounds, and run-ledger recording style.

## Notes

- This repo now prioritizes Codex-first orchestration with subagents.
- `plan.md` is the authoritative implementation document for the workflow once implementation starts.
- `execution.md` is optional and should be used as an evidence appendix rather than a second control document.
- Repo-local `PLANS.md` can be useful project context, but it should not silently override this workflow contract.
