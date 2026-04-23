# ai-workflows

Portable workflow skills for AI-assisted product and engineering work, plus an optional Codex adapter layer for named subagents.

This repository defines a guided workflow where the active AI session is the orchestrator and subagents act as operators and reviewers. The workflow moves through idea, spec, plan, implementation, implementation review, final review, and docs close-out with explicit user gates between major phases.

## What Ships

- `workflow-run`: orchestrates the full workflow.
- Create-stage skills:
  - `idea-create`
  - `spec-create`
  - `plan-create`
  - `implement-plan`
- Review-stage skills:
  - `idea-review`
  - `spec-review`
  - `plan-review`
  - `implementation-review`
  - `final-review`
- `skeptical-review`: optional manual pressure-test outside the main workflow.
- `.codex/`: optional Codex adapter with persona agents, role registry, and runtime settings.
- `scripts/check_workflow_artifacts.py`: lightweight consistency checker for skill packages and workflow dossiers.

## Core Model

- The active session is always the orchestrator.
- Operators and reviewers are always subagents.
- Agents define durable persona behavior.
- Skills define stage procedure, inputs, outputs, and artifact boundaries.
- Operators own source artifacts, accepted revisions, implementation work, and remediation work.
- Reviewers provide findings and recommendations; they do not own source artifacts.
- The orchestrator writes official consolidated review rounds and owns stage advancement.
- User approval is required after idea review resolution, spec review resolution, plan review resolution, implementation-review resolution, and final-review gap resolution plus docs close-out.

## Workflow

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

`workflow-run` is the orchestrator, not a stage.

## Stage Ownership

| Stage | Operator | Reviewers |
| --- | --- | --- |
| `idea-create` / `idea-review` | Product Strategist | Stakeholder Advocate, Product Designer or Domain Expert, Skeptic |
| `spec-create` / `spec-review` | Product Manager | Software Architect, Stakeholder Advocate or Product Designer, Skeptic |
| `plan-create` / `plan-review` | Software Architect | Software Architect, Software Engineer, Skeptic |
| `implement-plan` | Software Engineer | n/a |
| `implementation-review` | n/a | Software Architect, Security Engineer, QA Engineer |
| `final-review` | Orchestrator synthesis | Product Manager or Product Strategist, Software Architect, QA Engineer |
| docs close-out | Documentation Maintainer | n/a |

For `idea`, `spec`, and `plan`, reviews use exactly two substantive reviewers plus one skeptic. `implementation-review` always uses architecture, security, and QA / product correctness.

## Workflow Dossier

Each workflow lives under one dossier:

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

Create a new zero-padded review round for each pass. Do not overwrite older review files.

Source artifacts use slugged H1 titles:

- `# Run - {slug}`
- `# Idea - {slug}`
- `# Spec - {slug}`
- `# Plan - {slug}`
- `# Execution - {slug}` when `execution.md` is used

## Artifact Ownership

- `run.md` is the compact restart ledger. Keep it under roughly 120 lines, use a current-state summary instead of a long chronology, and do not add `Validation Evidence`.
- `idea.md` owns opportunity, value, risks, and intentionally deferred questions. Keep it under roughly 1,000 words unless deeper discovery is requested.
- `spec.md` owns the user-visible contract, acceptance behavior, privacy/business rules, and scope boundaries.
- `plan.md` owns implementation decisions, sequencing, interfaces, validation plan, idempotence, and recovery.
- `execution.md` owns implementation evidence, checks run, changed areas, remediation history, and deviations during multi-step work.
- Review rounds own reviewer findings, recommendation, and brief reviewer synopses.

The repo markdown artifacts must be sufficient for another operator or orchestrator to resume without chat history. Accepted decisions and review outcomes should be written into the owning artifact before later work depends on them.

## Review Output Rules

Saved review rounds should be concise and findings-first:

- keep reviewer rosters visible
- record concrete agent id and display name when the runtime exposes them
- keep reviewer inputs to up to three consequential findings, one recommendation, and only necessary rationale
- preserve brief reviewer synopses without transcript-style detail
- merge overlapping findings
- omit empty boilerplate sections such as `Meaningful Disagreements`, `Suggested Revisions`, or `Outstanding Dissent`
- keep normal review rounds around 250-500 words unless material findings require more
- for focused re-reviews, inspect only the prior finding, current artifact, and changed area
- record markdown-artifact handoff gaps as findings when they would block restartability

Before docs close-out, run a drift sweep across the idea, spec, plan, execution evidence when present, and latest review rounds. Fix stale wording where later accepted decisions superseded earlier artifact language.

## Codex Adapter

The portable workflow contract lives in `skills/`. The optional Codex adapter lives in `.codex/`:

- `.codex/agents/`: concrete persona agent definitions
- `.codex/role-registry.toml`: stage-to-persona-to-agent bindings
- `.codex/config.toml`: subagent runtime settings

Official Codex workflow delegation must use the concrete `agent` value resolved from `.codex/role-registry.toml`. Generic helpers such as `worker`, `explorer`, or `default` may support sidecar discovery, but prompt text alone does not make them official workflow operators or reviewers.

Current Codex runtime limitation: repo-scoped `.codex/agents/*.toml` discovery appears unreliable in some sessions. This package keeps the project-scoped role registry and runtime config in the target repository, but installs persona agent files to `~/.codex/agents/` by default so the named workflow personas are consistently spawnable.

## Install

From a target repository root:

```powershell
python C:\path\to\ai-workflows\install.py
```

By default this installs:

- skill packages into `.codex/skills/`
- persona agents into `~/.codex/agents/`
- role registry and runtime config into the target repo's `.codex/`

Useful installer options:

- `--dry-run`: show planned changes without writing files
- `--force`: overwrite existing managed files
- `--global-skills`: install skills to `~/.codex/skills`
- `--no-adapter`: install only skills
- `--no-skills`: install only the adapter
- `--target <path>`: install into a specific existing directory

Manual install is also supported. Copy folders from `skills/` into your agent's skills directory. For Codex use, copy `.codex/agents/*.toml` into `~/.codex/agents/`, then copy `.codex/role-registry.toml` and `.codex/config.toml` into the target repository root under `.codex/`.

## Consistency Checker

Run the checker from this repository root:

```powershell
python scripts/check_workflow_artifacts.py --root .
```

Check a workflow dossier:

```powershell
python scripts/check_workflow_artifacts.py --root . --dossier C:\path\to\repo\docs\workflows\my-slug --stale-term per-band
```

The checker fails on structural errors such as missing skill files, mismatched skill names, or invalid artifact H1s. It reports warnings for budget drift, forbidden `run.md` sections, missing latest-review references, oversized review rounds, and configured stale terms.

## Repository Layout

- `skills/`: canonical portable skill packages
- `.codex/`: optional Codex adapter layer
- `scripts/`: lightweight repository and workflow checks
- `README.md`: human-facing workflow overview and install guidance
