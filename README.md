# ai-workflows

Portable workflow skills for AI-assisted product and engineering work.

This repo packages a structured workflow you can run inside skill-capable agent apps such as Codex or Claude. The default flow moves from idea, to spec, to plan, to implementation, to final review, while keeping a workflow dossier under `docs/workflows/{slug}/`.

## What You Get

- `workflow-run` to coordinate the full workflow from a starting prompt
- creation skills for idea, spec, and plan stages
- review skills for idea, spec, plan, and final outcome
- `implement-plan` for execution
- `skeptical-review` for optional adversarial feedback outside the main stage sequence

## Workflow

The canonical workflow is:

1. `idea-create`
2. `idea-review`
3. `spec-create`
4. `spec-review`
5. `plan-create`
6. `plan-review`
7. `implement-plan`
8. `final-review`

`workflow-run` is the orchestrator. It is not a stage.

## Stage Outputs

| Stage | Purpose | Output |
| --- | --- | --- |
| `idea-create` | Shape the product idea and expected value. | `docs/workflows/{slug}/idea.md` |
| `idea-review` | Pressure-test the idea before spec work. | `docs/workflows/{slug}/reviews/idea/round-01.md` |
| `spec-create` | Turn the idea into a functional product contract. | `docs/workflows/{slug}/spec.md` |
| `spec-review` | Review the spec for clarity, completeness, and readiness for planning. | `docs/workflows/{slug}/reviews/spec/round-01.md` |
| `plan-create` | Turn the spec into an implementation-ready engineering plan. | `docs/workflows/{slug}/plan.md` |
| `plan-review` | Review the plan before implementation begins. | `docs/workflows/{slug}/reviews/plan/round-01.md` |
| `implement-plan` | Implement the approved plan. | Code changes plus optional `docs/workflows/{slug}/execution.md` |
| `final-review` | Review the finished outcome against the artifact chain. | `docs/workflows/{slug}/reviews/final/round-01.md` |

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
    final/round-01.md
```

Use one canonical `slug` per workflow. Create a new review round for each pass instead of overwriting earlier review files.

## How It Works

Use `workflow-run` when you want the full lifecycle coordinated from a starting prompt.

In normal use, `workflow-run` will:

- run the stages in order
- maintain `docs/workflows/{slug}/run.md`
- ask plain-language startup questions if your preferred level of autonomy or review pauses is unclear
- ask blocking questions for materially important decisions
- pause at major stage boundaries when you ask for review gates

Blocking questions should include decisions such as:

- new architectural directions or major architectural constraints
- new third-party services, SDKs, hosted platforms, or external tools
- material security, privacy, cost, operational, or vendor-lock-in tradeoffs

If the target repo requires `PLANS.md`, or its `AGENTS.md` says planning and implementation must use `PLANS.md`, the workflow should treat `plan.md` as the authoritative execution document once implementation starts.

## Review Style

Review skills are meant to do more than rubber-stamp artifacts.

They should:

- adapt reviewer personas to scope and risk
- include an explicit UX or product-design perspective for meaningful UI or interaction work
- include a skeptical or risk-focused perspective
- preserve meaningful dissent when important weaknesses remain
- compare non-trivial or user-facing work against industry-standard practice and strong comparable products

## Optional Manual Skill

`skeptical-review` is an optional manual pressure-test skill. It is not part of the canonical stage sequence.

Use it when you want a harsher reality check on:

- an idea
- a spec
- a plan
- an implementation summary
- a product or architecture decision

It should respond directly in chat and should not create new files.

## Example Prompts

Structured prompt:

```text
Use workflow-run to take this from idea through final review.
question_mode: fully automated
stage_gate_mode: none
Prompt: Build a lightweight internal release notes tool for product and engineering teams.
```

Natural-language prompt:

```text
Implement the following feature concept. Ask blocking questions. Stop at major steps or milestones so I can review progress.
Use workflow-run for this feature.
Prompt: Build a customer-facing saved views experience for our reporting dashboard.
```

Another natural-language prompt:

```text
Use workflow-run for this feature and ask only if you have blocking questions.
Prompt: Build an internal customer feedback triage dashboard.
```

Manual adversarial review:

```text
Use skeptical-review on this spec and tell me why it should not advance yet.
```

## Install for Claude

Copy any skill folder from `skills/` into your Claude skills directory:

```text
skills/workflow-run -> ~/.claude/skills/workflow-run
skills/implement-plan -> ~/.claude/skills/implement-plan
skills/skeptical-review -> ~/.claude/skills/skeptical-review
```

To install everything, copy each folder under `skills/` into:

```text
~/.claude/skills/
```

## Install for Codex

Copy any skill folder from `skills/` into your Codex skills directory:

```text
skills/workflow-run -> ~/.codex/skills/workflow-run
skills/implement-plan -> ~/.codex/skills/implement-plan
skills/skeptical-review -> ~/.codex/skills/skeptical-review
```

To install everything, copy each folder under `skills/` into:

```text
~/.codex/skills/
```

## Repository Layout

- `skills/` - canonical skill packages
- `docs/` - supporting docs and artifact examples
- `README.md` - human-facing workflow overview

## Notes

- The skills are intentionally client-neutral.
- This repo currently targets Claude and Codex.
- Repo-local `PLANS.md` and project `AGENTS.md` can override portable planning and implementation defaults.
