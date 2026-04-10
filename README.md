# ai-workflows

Portable workflow skills for AI-assisted product and engineering work.

This repo packages a structured workflow you can run inside skill-capable agent apps such as Codex or Claude. The default flow moves from idea, to spec, to plan, to implementation, to final review, while keeping a workflow dossier under `docs/workflows/{slug}/`.

The intended output style is concise by default: permanent workflow artifacts should read like working documents, not transcripts of everything the model thought about.

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

- resolve run and execution options before stage work begins
- run the stages in order
- maintain `docs/workflows/{slug}/run.md`
- keep workflow guidance in plain text under `Purpose / Big Picture` rather than as top-of-file metadata
- ask plain-language startup questions with short labeled choices if your preferred level of autonomy or review pauses is unclear
- ask about Git commit cadence when the repo is under Git and the workflow is likely to change files, unless your preference is already clear
- once startup options are clear, show you the resolved workflow setup and ask you to confirm before it starts the first stage
- ask blocking questions for materially important decisions
- record those important questions, answers, clarifications, and resulting decisions in `run.md` as part of the workflow history
- pause at major stage boundaries when you ask for review gates

Permanent artifacts should stay skimmable:

- deep questioning and internal reasoning may happen during a stage, but the saved document should keep only the decisions, evidence, and open issues needed to move forward safely
- review rounds are findings-first by default, not full stakeholder-debate transcripts
- when a short summary, bullet list, or table is enough, prefer that over long prose

Blocking questions should include decisions such as:

- new architectural directions or major architectural constraints
- new third-party services, SDKs, hosted platforms, or external tools
- material security, privacy, cost, operational, or vendor-lock-in tradeoffs

When these workflow skills are active, the workflow dossier remains authoritative. Repo-local `PLANS.md` can be read as project context, but it should not silently override this workflow's stage structure, artifact structure, or execution control unless the user explicitly asks for repo-native planning mode.

## Review Style

Review skills are meant to do more than rubber-stamp artifacts.

They should:

- adapt reviewer personas to scope and risk
- include an explicit UX or product-design perspective for meaningful UI or interaction work
- include a skeptical or risk-focused perspective
- preserve meaningful dissent when important weaknesses remain
- compare non-trivial or user-facing work against industry-standard practice and strong comparable products

But the saved review artifact should stay compact:

- keep named reviewer lenses without transcribing the whole debate
- merge overlapping critiques instead of repeating them persona by persona
- preserve only the disagreements that materially affect the recommendation

## Optional Manual Skill

`skeptical-review` is an optional manual pressure-test skill. It is not part of the canonical stage sequence.

Use it when you want a harsher reality check on:

- an idea
- a spec
- a plan
- an implementation summary
- a product or architecture decision

It should respond directly in chat and should not create new files.

## Multi-Client Handoffs

You can split a workflow across clients manually. For example:

- use Claude for `idea-create`, `idea-review`, `spec-create`, and `spec-review`
- use Codex for `plan-create`, `plan-review`, and `implement-plan`
- use both Claude and Codex for selected review stages

The workflow model already supports this well because `idea.md`, `spec.md`, `plan.md`, review rounds, and `run.md` are meant to be self-contained and restartable.

When handing off between clients:

- use the artifact boundary as the handoff boundary
- update `run.md` to name the current owner, next recommended owner, and exact artifact path the next client should start from
- keep the rationale for the handoff in `run.md`
- if both clients review the same artifact, create sequential review rounds rather than overwriting:
  - for example, `round-01.md` from one client and `round-02.md` from the other
- summarize the combined outcome in `run.md` before advancing

This repo does not currently automate client switching. Use `run.md` as the handoff contract.

## Example Prompts

Structured prompt:

```text
Use workflow-run to take this from idea through final review.
question_mode: fully automated
stage_gate_mode: none
Build a lightweight internal release notes tool for product and engineering teams.
```

Natural-language prompt:

```text
Implement the following feature concept. Ask blocking questions. Stop at major steps or milestones so I can review progress.
Use workflow-run for this feature.
Build a customer-facing saved views experience for our reporting dashboard.
```

Multi-client handoff prompt:

```text
Use workflow-run for this feature.
Use Claude for idea and spec work.
Use Codex for plan creation and implementation.
Use both Claude and Codex for review stages when useful.
Ask blocking questions.
Stop at major stage boundaries so I can review and approve handoffs.
Build a Portable Markdown Format app with a cross-platform .NET CLI creator and a cross-platform rich reader application.
```

If `workflow-run` needs a startup clarification, it should prefer a concise numbered-choice question such as:

```text
How should I handle decisions as I run this workflow?
1. Make reasonable assumptions and only stop for review gates
2. Ask only when something would materially block good work
3. Check in often on non-obvious choices
Reply with 1, 2, 3, or answer in your own words.
```

After startup options are resolved, it should present a short start confirmation such as:

```text
Here is how I will run this workflow:
- Workflow ask: Build a customer-facing saved views experience for our reporting dashboard.
- Canonical slug: saved-views-dashboard
- Decision handling: ask only when something would materially block good work
- Review pauses: stop for approval after idea review, spec review, plan review, and implementation
- Git commits: do not create commits automatically
- Execution plan mode: standard
Reply 'start' to begin, or tell me what to change.
```

Git commit preference is also a good startup policy to make explicit. For example:

```text
How do you want me to handle Git commits for workflow changes?
1. Do not create commits automatically
2. Create commits at major approved stage boundaries when files changed
3. Create a commit after each file-changing stage
Reply with 1, 2, 3, or answer in your own words.
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
- Repo-local `PLANS.md` can be useful project context, but it should not silently override this workflow contract.
