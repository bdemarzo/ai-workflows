# ai-workflows

Portable workflow skills for AI-assisted product and engineering work, plus optional runtime adapter layers for named subagents.

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
- `adapters/codex/`: source files for the optional Codex adapter.
- `adapters/copilot/`: source files for the optional GitHub Copilot adapter.
- `packages/codex-plugin/` and `marketplaces/codex-local/`: source templates for Codex plugin packaging and local marketplace metadata.
- `scripts/check_workflow_artifacts.py`: lightweight consistency checker for skill packages and concise workflow dossiers.

## Core Model

- The active session is always the orchestrator.
- Operators and reviewers are always subagents.
- Agents define durable persona behavior.
- Skills define stage procedure, inputs, outputs, and artifact boundaries.
- Operators own source artifacts, accepted revisions, implementation work, and remediation work.
- Reviewers provide findings and recommendations; they do not own source artifacts.
- The orchestrator writes official consolidated review rounds and owns stage advancement.
- If an official operator appears stalled, the orchestrator asks that subagent for progress before changing ownership.
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
| docs close-out (`docs-closeout` binding) | Documentation Maintainer | n/a |

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

- `run.md` is the compact restart ledger. Use current-state summaries instead of chronology, and do not add `Validation Evidence`.
- `idea.md` owns the current opportunity, value, risks, and intentionally deferred questions.
- `spec.md` owns the current user-visible contract, acceptance behavior, privacy/business rules, and scope boundaries.
- `plan.md` owns the current implementation decisions, sequencing, interfaces, validation plan, idempotence, and recovery.
- `execution.md` owns concise implementation evidence, checks run, changed areas, remediation history, and deviations during multi-step work.
- Review rounds own reviewer findings, recommendations, brief reviewer synopses, decision branches, and what changed between rounds.

The repo markdown artifacts must be sufficient for another operator or orchestrator to resume without chat history. Accepted decisions and review outcomes should be folded into the owning source artifact as the official current state before later work depends on them. Do not preserve stale alternatives, dated revision history, or superseded rationale in `idea.md`, `spec.md`, or `plan.md`; that history belongs in review rounds, `run.md` decision pointers, or `execution.md` evidence when relevant.

## Stalled Operator Recovery

When an official operator subagent appears stalled, blocked, or materially slower than expected, the orchestrator first asks the subagent for a bounded progress report. If the operator is unresponsive or cannot provide a useful handoff, the orchestrator asks the user whether to wait and check again, replace the operator, take over directly, or follow custom direction. The decision, cleanup, substitution, takeover, and implementation evidence state are recorded in `run.md` and `execution.md` when applicable.

## Stalled Operator Recovery

When an official operator subagent appears stalled, blocked, or materially slower than expected, the orchestrator first asks the subagent for a bounded progress report. If the operator is unresponsive or cannot provide a useful handoff, the orchestrator asks the user whether to wait and check again, replace the operator, take over directly, or follow custom direction. The decision, cleanup, substitution, takeover, and implementation evidence state are recorded in `run.md` and `execution.md` when applicable.

## Review Output Rules

Saved review rounds should be concise and findings-first:

- keep reviewer rosters visible
- record concrete agent id and display name when the runtime exposes them
- keep reviewer inputs to up to three consequential findings, one recommendation, and only necessary rationale
- preserve one-sentence reviewer synopses without transcript-style detail
- merge overlapping findings
- omit empty boilerplate sections such as `Meaningful Disagreements`, `Suggested Revisions`, or `Outstanding Dissent`
- keep review rounds compact unless material findings require more
- for focused re-reviews, inspect only the prior finding, current artifact, and changed area
- record markdown-artifact handoff gaps as findings when they would block restartability
- use review rounds for meaningful decision trees, rejected options, and changes since the prior round; do not copy that history into the source artifacts after a decision is accepted

Before docs close-out, run a drift sweep across the idea, spec, plan, execution evidence when present, and latest review rounds. Fix stale wording where later accepted decisions superseded earlier artifact language.

## Runtime Adapters

The portable workflow contract lives in `skills/`. Runtime adapter source files live under `adapters/` so this repository does not accidentally behave like an already-installed Codex or Copilot target. The installer is responsible for writing real runtime directories such as `.codex/`, `.agents/`, and `.github/` into a target repository or user profile.

Registry `allowed_substitutions` entries are persona labels; paired `allowed_substitution_agents` entries are the concrete runtime agent IDs to use when that substitution is selected.

### Codex

Codex adapter source:

- `adapters/codex/agents/`: concrete persona agent definitions
- `adapters/codex/role-registry.toml`: stage-to-persona-to-agent bindings
- `adapters/codex/config.toml`: subagent runtime settings
- `adapters/codex/skill-metadata/`: optional Codex app metadata overlaid onto installed skills

Codex project-scope install destinations:

- target `.agents/skills/`: default repo-local Codex skill install location
- target `.codex/agents/*.toml`: persona agent definitions
- target `.codex/role-registry.toml` and `.codex/config.toml`: runtime binding/config

Codex user-scope install destinations:

- user `~/.agents/skills/`: default user Codex skill install location
- user `~/.codex/agents/*.toml`: persona agent definitions
- user `~/.codex/role-registry.toml` and `~/.codex/config.toml`: runtime binding/config

Official Codex workflow delegation must use the concrete `agent` value resolved from `.codex/role-registry.toml`. Generic helpers such as `worker`, `explorer`, or `default` may support sidecar discovery, but prompt text alone does not make them official workflow operators or reviewers.

Codex persona agents generally inherit the current session model so newer models such as GPT-5.5 are used when selected and available. The documentation maintainer remains pinned to a smaller model for concise docs work.

Current Codex runtime note: repo-scoped `.codex/agents/*.toml` discovery can vary by surface and version. Project scope remains the default because it keeps the workflow package portable with the target repository. Use `--scope user` when your Codex surface only discovers user-profile agents.

Optional Codex settings:

```toml
approval_policy = "on-request"
approvals_reviewer = "auto_review"
```

Use automatic approval reviews when your Codex workspace supports them and you want eligible approval prompts pre-reviewed by Codex before you decide. This does not replace the workflow's product/user gates.

Hooks are also supported by recent Codex versions, but this package does not enable them by default. Teams that want a repo-local quality gate can configure a `Stop` or `PostToolUse` hook to run:

```powershell
python scripts/check_workflow_artifacts.py --root .
```

### GitHub Copilot

Copilot adapter source:

- `adapters/copilot/agents/*.agent.md`: concrete Copilot custom agent profiles for workflow personas
- `adapters/copilot/role-registry.toml`: stage-to-persona-to-agent bindings
- `adapters/copilot/config.toml`: runtime orchestration settings
- `adapters/copilot/copilot-instructions.md`: concise repository instructions for Copilot

Copilot project-scope install destinations:

- target `.github/skills/`: installed copies of canonical skill packages from `skills/`
- target `.github/agents/*.agent.md`: concrete Copilot custom agent profiles
- target `.github/ai-workflows/role-registry.toml` and `.github/ai-workflows/config.toml`: project runtime binding/config
- target `.github/copilot-instructions.md`: repository instructions

Copilot user-scope install destinations:

- user `~/.github/skills/`: installed copies of canonical skill packages from `skills/`
- user `~/.github/agents/*.agent.md`: concrete Copilot custom agent profiles
- user `~/.github/ai-workflows/role-registry.toml` and `~/.github/ai-workflows/config.toml`: runtime binding/config
- user `~/.github/copilot-instructions.md`: user-profile instructions

Official Copilot workflow delegation must use the concrete `agent` value resolved from `.github/ai-workflows/role-registry.toml`. The Copilot adapter defaults to project-local skill and custom-agent locations so it can travel with the target repository.

### Codex Plugin Templates

Plugin packaging source lives under `packages/codex-plugin/`, and local marketplace source lives under `marketplaces/codex-local/`. These are source templates, not active root-level Codex plugin installation files. Build or copy them into an actual marketplace root when testing plugin installation.

## Install

From a target repository root:

```powershell
python C:\path\to\ai-workflows\install.py --runtime codex
python C:\path\to\ai-workflows\install.py --runtime copilot
```

For Codex, this installs:

- skill packages into `.agents/skills/`
- persona agents into `.codex/agents/`
- role registry and runtime config into the target repo's `.codex/`

For Copilot, this installs:

- skill packages into `.github/skills/`
- custom agent profiles into `.github/agents/`
- role registry and runtime config into `.github/ai-workflows/`
- repository instructions into `.github/copilot-instructions.md`

Useful installer options:

- `--runtime codex`: install the Codex adapter
- `--runtime copilot`: install the GitHub Copilot adapter
- `--scope project`: install into the target repository; this is the default
- `--scope user`: install into the current user's profile for the selected runtime
- `--dry-run`: show planned changes without writing files
- `--force`: overwrite existing managed files
- `--legacy-codex-skills`: for Codex only, install skills to `.codex/skills` for project scope or `~/.codex/skills` for user scope
- `--no-adapter`: install only skills
- `--no-skills`: install only the adapter
- `--target <path>`: install into a specific existing directory

Manual install is also supported. For project-scoped Codex use, copy folders from `skills/` into target `.agents/skills/`, overlay any matching `adapters/codex/skill-metadata/<skill>/` files into the installed skill folder, copy `adapters/codex/agents/*.toml` into target `.codex/agents/`, then copy `adapters/codex/role-registry.toml` and `adapters/codex/config.toml` into target `.codex/`. For user-scoped Codex use, make the same copies under `~/.agents/skills/` and `~/.codex/`. For older Codex versions that still expect legacy locations, use `.codex/skills/` under the selected scope root.

To test this package as a local Codex plugin, build or copy the plugin template from `packages/codex-plugin/ai-workflows/` into an actual marketplace root that matches `marketplaces/codex-local/marketplace.json`. Do not add root-level `.codex-plugin/` or `.agents/plugins/` files to this source repository.

For project-scoped Copilot use, copy folders from `skills/` into target `.github/skills/`, copy `adapters/copilot/agents/*.agent.md` into target `.github/agents/`, copy `adapters/copilot/role-registry.toml` and `adapters/copilot/config.toml` into target `.github/ai-workflows/`, and copy `adapters/copilot/copilot-instructions.md` into target `.github/`. For user-scoped Copilot use, make the same copies under `~/.github/`.

## Consistency Checker

Run the checker from this repository root:

```powershell
python scripts/check_workflow_artifacts.py --root .
```

Check a workflow dossier:

```powershell
python scripts/check_workflow_artifacts.py --root . --dossier C:\path\to\repo\docs\workflows\my-slug --stale-term per-band
```

The checker fails on structural errors such as missing skill files, mismatched skill names, invalid plugin templates, adapter registries that reference missing agents, Copilot custom agents with missing frontmatter, or invalid artifact H1s. It reports warnings for source-artifact history sections, forbidden `run.md` sections, missing latest-review references, and configured stale terms.

## Repository Layout

- `skills/`: canonical portable skill packages
- `adapters/`: optional runtime adapter source files
- `packages/`: optional package source templates
- `marketplaces/`: optional marketplace source templates
- `scripts/`: lightweight repository and workflow checks
- `README.md`: human-facing workflow overview and install guidance
