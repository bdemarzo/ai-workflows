# AGENTS.md

## Repository Purpose

This repository ships portable workflow skill packages plus a Codex adapter for guided product and engineering work.

The human-facing workflow contract lives in `README.md`.

Use this file for repo-specific operating guidance when changing the skills or docs.

## Source Of Truth

- `skills/` is the canonical source of truth for shipped skill packages.
- `README.md` is the canonical human-facing description of the workflow, stage names, and artifact paths.
- Keep skill package names, `name:` frontmatter, and README stage names aligned.

## Repo Layout

- `skills/<skill-name>/SKILL.md` - canonical skill packages
- `adapters/codex/agents/*.toml` - optional Codex-specific persona implementations
- `adapters/codex/role-registry.toml` - optional Codex-specific registry mapping workflow stages to persona labels and then to concrete agent names
- `adapters/codex/config.toml` - optional Codex-specific runtime settings for subagent orchestration
- `adapters/codex/skill-metadata/` - optional Codex app metadata overlaid onto installed skills
- `adapters/copilot/agents/*.agent.md` - optional GitHub Copilot custom agent persona implementations
- `adapters/copilot/role-registry.toml` - optional Copilot registry mapping workflow stages to persona labels and then to concrete custom agent names
- `adapters/copilot/config.toml` - optional Copilot runtime settings for subagent orchestration
- `packages/codex-plugin/` - optional Codex plugin package source template
- `marketplaces/codex-local/` - optional Codex local marketplace source template
- `skills/<skill-name>/assets/` - optional skill-local templates or output resources that support standalone use
- `skills/<skill-name>/references/` - optional skill-local reference docs loaded only when needed
- `docs/` - supporting docs only
- `README.md` - workflow model and install guidance

## Editing Rules

- The active session is the orchestrator.
- Operators and reviewers are subagents.
- Keep skill bodies client-neutral even if this repo also ships optional runtime agent definitions.
- Treat `skills/` as the portable workflow contract and `adapters/` as runtime adapter source, not as a second source of truth for stage behavior.
- Do not store install-target runtime directories such as `.codex/`, `.agents/`, `.codex-plugin/`, or `.github/` as source layout unless they are unrelated real repository infrastructure.
- If `adapters/codex/agents/` exists, treat it as the Codex implementation layer for those personas.
- If `adapters/codex/role-registry.toml` exists, treat it as the Codex binding layer from workflow stages to persona labels and then to concrete agent names.
- If `adapters/copilot/agents/` exists, treat it as the GitHub Copilot implementation layer for those personas.
- If `adapters/copilot/role-registry.toml` exists, treat it as the Copilot binding layer from workflow stages to persona labels and then to concrete custom agent names.
- `workflow-run` is a meta-skill, not a stage.
- Agents define persona behavior; skills define stage procedure.
- Official operators and reviewers must use the concrete agent resolved by the role registry; for Codex this means spawning the registry `agent` value as `agent_type`, and for Copilot this means selecting or invoking the registry `agent` value as the custom agent.
- Operators own drafting, accepted artifact revisions, implementation work, and implementation remediations for their phase.
- Reviewers provide findings and recommendations but do not own the source artifact.
- The orchestrator writes the official consolidated review rounds and owns stage advancement.
- The orchestrator should periodically re-ground on the repo markdown artifacts rather than trusting long chat history, especially at phase boundaries and after reroutes.
- The orchestrator should not rely on accepted decisions that exist only in chat; accepted user feedback and review outcomes should be written into repo markdown artifacts before more work is delegated.
- Delegate subagent work from exact artifact paths, assigned persona/lens, and saved decisions rather than broad chat-history recap.
- Keep subagent work bounded; avoid broad repo scans unless implementation evidence, source context, or a specific finding requires them.
- Before reclaiming, replacing, or aborting a stalled official operator, ask for progress, then get the user's recovery choice and record the decision, cleanup, ownership change, and evidence state in repo markdown artifacts.
- Prefer sequential reviewer execution on constrained hosts; use parallel reviewers only when host responsiveness is acceptable and faster wall-clock review matters.
- Close or release subagents after their output has been captured in markdown when the runtime supports explicit shutdown.
- Keep the dossier layout:
  - `docs/workflows/{slug}/run.md`
  - `docs/workflows/{slug}/idea.md`
  - `docs/workflows/{slug}/spec.md`
  - `docs/workflows/{slug}/plan.md`
  - `docs/workflows/{slug}/execution.md`
- Keep the review-round layout:
  - `docs/workflows/{slug}/reviews/idea/round-01.md`
  - `docs/workflows/{slug}/reviews/spec/round-01.md`
  - `docs/workflows/{slug}/reviews/plan/round-01.md`
  - `docs/workflows/{slug}/reviews/implementation/round-01.md`
  - `docs/workflows/{slug}/reviews/final/round-01.md`
- Create a new zero-padded review round for each pass. Do not overwrite older rounds.
- `idea`, `spec`, and `plan` reviews must use exactly:
  - two substantive reviewers
  - one skeptic
- For `implementation-review`, reviews must use exactly:
  - architecture
  - security
  - QA / product correctness
- QA / product correctness should explicitly consider regressions, edge cases, and unit-test coverage expectations.
- `skeptical-review` remains an optional manual pressure-test skill. It is separate from the mandatory skeptic reviewer inside the normal workflow.
- `idea.md` stays idea-level and outcome-first.
- `spec.md` stays contract-level and planning-ready.
- `plan.md` stays the authoritative implementation document once implementation starts.
- `execution.md` stays optional and should be used sparingly as an evidence appendix.
- Create-stage skills should remain concise, self-contained, and stage-bounded.
- Review rounds should remain concise, findings-first, and recommendation-driven.
- Reviewer inputs should stay compact: up to three consequential findings, one explicit recommendation, and only the rationale needed to support it.
- A person should be able to continue the workflow from the markdown artifacts in the repo alone; if not, reviewers should call that out as a key finding rather than a separate restartability section.
- Source artifacts (`idea.md`, `spec.md`, `plan.md`) are the official current-state record, not decision-history logs.
- Review artifacts may preserve decision trees, rejected options, rationale changes, and reviewer disagreement; source artifacts should fold accepted outcomes into the current truth and remove stale wording.
- Prefer replacing superseded source-artifact text over appending revision history.
- User gates are required after:
  - idea review resolution
  - spec review resolution
  - plan review resolution
  - implementation-review resolution
  - final-review gap resolution plus docs close-out
- Docs close-out is part of workflow completion.
- Repo-local `PLANS.md` and project `AGENTS.md` may be read as project context, but they should not silently override this workflow contract unless the user explicitly asks for repo-native planning mode.

## Consistency Checks

After changing the workflow or skill packages, verify:

- `skills/` contains the intended package set and no stale legacy package names
- every skill directory contains `SKILL.md`
- each skill's `name:` matches its folder name
- `README.md` and the skill package surface describe the same stage names and order
- `implementation-review` exists as a real skill and is included in the documented phase order
- if `adapters/codex/agents/` exists, the agent set covers the intended personas without changing the portable stage contract
- if `adapters/codex/role-registry.toml` exists, it covers every stage-to-persona assignment named in `workflow-run`, README, and the review skills
- role-registry allowed substitutions should include concrete substitution agent values, not persona labels alone
- if `packages/codex-plugin/` exists, its manifest template points to `./skills/`
- if `marketplaces/codex-local/marketplace.json` exists, it has valid marketplace template JSON
- if `adapters/copilot/agents/` exists, the custom agent set covers the intended personas without changing the portable stage contract
- if `adapters/copilot/role-registry.toml` exists, it covers every stage-to-persona assignment named in `workflow-run`, README, and the review skills
- artifact path references are consistent across all skills and docs
- source dossier artifacts use slugged H1 titles:
  - `# Run - {slug}`
  - `# Idea - {slug}`
  - `# Spec - {slug}`
  - `# Plan - {slug}`
  - `# Execution - {slug}` when `execution.md` is used
- review-round path references are consistent across all skills and docs
- saved review rounds record reviewer persona, concrete agent name, and display name when the runtime exposes one
- saved review rounds record only reviewers that match the resolved role binding from `workflow-run`
- saved review rounds preserve one-sentence reviewer synopses in addition to the orchestrator's merged findings
- saved review rounds reflect compact, lens-specific reviewer inputs rather than full reviewer transcripts
- `workflow-run` is documented consistently as the orchestrator rather than a workflow stage
- implementation-review specifies architecture, security, and QA / product correctness
- final-review reviewer personas are covered by each present runtime adapter layer
- implement-plan points to implementation-review as the next formal review stage
- final-review is documented as fidelity review before docs close-out, not immediate closure
- run ledger guidance records:
  - actual persona-to-agent bindings used
  - substitutions or fallbacks used
  - current orchestrator
  - current operator
  - current reviewer roster
  - current gate decision needed
  - implementation-review satisfaction state
  - documentation close-out status
- run ledger guidance uses `Decision Log` for resolved decisions and clarifications rather than implying open questions
- `Validation Evidence` is not required in `run.md`; validation belongs in the plan, execution appendix, or review artifacts when needed
- source artifacts avoid `Revision History` and other chronology sections unless the user explicitly asks for historical tracking
- docs close-out is represented consistently across README and workflow-run guidance
- skill-local templates under `skills/<skill-name>/assets/` reflect the documented artifact shape and current workflow contract
- skill-local references under `skills/<skill-name>/references/` are linked from `SKILL.md` and used for progressive disclosure rather than duplicating core instructions
- skill folders can still be copied as-is into local skill directories; Codex app metadata lives in `adapters/codex/skill-metadata/` and is overlaid only during Codex installation

## Current Limitations

- The portable workflow contract lives in `skills/`; runtime-specific persona and metadata layers live under `adapters/`.
- There is no dedicated automated test harness yet; consistency is enforced by careful doc and package alignment.
