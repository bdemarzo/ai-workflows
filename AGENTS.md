# AGENTS.md

## Purpose

This repository ships portable workflow skill packages plus optional Codex and Copilot adapter source for guided product and engineering work.

Use this file for repo-specific operating rules when changing skills, adapters, installer behavior, or docs. `README.md` remains the human-facing workflow contract.

## Source Of Truth

- `skills/` is the canonical portable workflow contract.
- `README.md` is the canonical human-facing description of stages, artifact paths, install behavior, and adapter shape.
- `adapters/` contains runtime-specific persona/config/metadata source only; it must not become a second source of truth for stage behavior.
- Keep skill folder names, `name:` frontmatter, README stage names, and role registries aligned.

## Layout

- `skills/<skill>/SKILL.md` - canonical skill body
- `skills/<skill>/assets/` - skill-local templates
- `skills/<skill>/references/` - progressive-disclosure reference docs linked from `SKILL.md`
- `adapters/codex/` - Codex agents, config, role registry, and skill metadata overlays
- `adapters/copilot/` - Copilot custom agents, config, role registry, and instructions
- `packages/codex-plugin/` - Codex plugin package source template
- `marketplaces/codex-local/` - local marketplace source template
- `docs/` - supporting docs only

Do not store install-target runtime directories such as root `.codex/`, `.agents/`, `.codex-plugin/`, or adapter-style `.github/` as source layout unless they are unrelated real repository infrastructure.

## Workflow Rules

- The active session is the orchestrator; operators and reviewers are subagents.
- `workflow-run` is a meta-skill, not a stage.
- Agents define persona behavior; skills define stage procedure.
- Official operators/reviewers must use the concrete agent resolved by the runtime role registry.
- For Codex, spawn the registry `agent` value as `agent_type`.
- For Copilot, select or invoke the registry `agent` value as the custom agent.
- Prompt text alone does not turn a generic agent into an official workflow persona.
- Operators own source-artifact drafting, accepted revisions, implementation work, and implementation remediations.
- Reviewers provide findings and recommendations; they do not own source artifacts.
- The orchestrator writes consolidated review rounds and owns stage advancement.
- Re-ground on repo markdown artifacts at phase boundaries, after user gates, and after reroutes. Do not rely on chat-only accepted decisions.
- Delegate from exact artifact paths, assigned persona/lens, and saved decisions. Avoid broad repo scans unless a specific finding or implementation need requires them.
- Before reclaiming, replacing, or aborting a stalled official operator, ask for progress, get the user's recovery choice, and record the decision/evidence in repo markdown artifacts.
- Prefer sequential reviewers on constrained hosts; use parallel reviewers only when responsiveness is acceptable.

## Artifact Contract

Dossier layout:
- `docs/workflows/{slug}/run.md`
- `docs/workflows/{slug}/idea.md`
- `docs/workflows/{slug}/spec.md`
- `docs/workflows/{slug}/plan.md`
- `docs/workflows/{slug}/execution.md` when useful

Review-round layout:
- `docs/workflows/{slug}/reviews/idea/round-XX.md`
- `docs/workflows/{slug}/reviews/spec/round-XX.md`
- `docs/workflows/{slug}/reviews/plan/round-XX.md`
- `docs/workflows/{slug}/reviews/implementation/round-XX.md`
- `docs/workflows/{slug}/reviews/final/round-XX.md`

Create a new zero-padded review round for each pass. Do not overwrite older rounds.

Source artifact responsibilities:
- `run.md`: compact restart ledger; no `Validation Evidence`
- `idea.md`: idea-level, outcome-first current opportunity
- `spec.md`: contract-level user-visible behavior and scope
- `plan.md`: authoritative implementation control document once implementation starts
- `execution.md`: optional concise evidence appendix for implementation steps, validation, deviations, and remediation
- review rounds: findings, recommendations, reviewer synopses, decision branches, rejected options, and meaningful disagreement

Source artifacts are current-state records, not chronology. Replace superseded text instead of appending revision history. A person should be able to resume the workflow from markdown artifacts alone.

## Stage And Review Rules

Required phase order: `idea-create`, `idea-review`, user gate, `spec-create`, `spec-review`, user gate, `plan-create`, `plan-review`, user gate, `implement-plan`, `implementation-review`, user gate, `final-review`, final gap resolution, docs close-out, final user approval.

- `idea`, `spec`, and `plan` reviews use exactly two substantive reviewers plus one skeptic.
- `implementation-review` uses architecture, security, and QA / product correctness.
- QA / product correctness considers regressions, edge cases, and unit-test coverage expectations.
- `skeptical-review` is optional manual pressure testing and is separate from mandatory workflow skeptic review.
- `final-review` is fidelity review before docs close-out, not immediate closure.
- Docs close-out is part of workflow completion.
- Required user gates follow idea review resolution, spec review resolution, plan review resolution, implementation-review resolution, and final-review gap resolution plus docs close-out.

## Token Discipline

- Keep skill bodies concise and stage-bounded.
- Put rarely needed detail in linked `references/` files and load it only when needed.
- Keep templates in `assets/`; do not duplicate template content in `SKILL.md`.
- Keep reviewer inputs compact: up to three consequential findings, one explicit recommendation, and only necessary rationale.
- Keep review rounds findings-first; omit empty boilerplate sections.
- Store validation in `plan.md`, `execution.md`, or review artifacts, not `run.md`.
- Store accepted decisions in the artifact that owns them; point elsewhere instead of duplicating the same decision across artifacts.

## Verification

After changing workflow, skill, adapter, installer, or package metadata, run:

```powershell
python scripts/check_workflow_artifacts.py --root .
```

Also spot-check the change for:
- skill names/frontmatter matching folder names
- README, skill order, and role registries agreeing on stage names and reviewer personas
- adapter registries referencing existing concrete agents and allowed substitution agents
- `implementation-review` and `final-review` remaining in the documented phase order
- run-ledger guidance preserving current operator/reviewer/gate/close-out status
- skill-local references being linked from `SKILL.md`
- skill folders remaining copyable as standalone local skills

Repo-local `PLANS.md` or project `AGENTS.md` may be read as project context, but they do not silently override this workflow contract unless the user explicitly asks for repo-native planning mode.
