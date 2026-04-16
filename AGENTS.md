# AGENTS.md

## Repository Purpose

This repository ships workflow skill packages for guided, Codex-first product and engineering work.

The human-facing workflow contract lives in `README.md`.

Use this file for repo-specific operating guidance when changing the skills or docs.

## Source Of Truth

- `skills/` is the canonical source of truth for shipped skill packages.
- `README.md` is the canonical human-facing description of the workflow, stage names, and artifact paths.
- Keep skill package names, `name:` frontmatter, and README stage names aligned.

## Repo Layout

- `skills/<skill-name>/SKILL.md` - canonical skill packages
- `.codex/agents/*.toml` - optional Codex-specific runtime subagent definitions for the abstract workflow roles
- `.codex/role-registry.toml` - optional Codex-specific registry mapping abstract workflow roles to concrete agent names and substitutions
- `.codex/config.toml` - optional Codex-specific runtime settings for subagent orchestration
- `docs/examples/` - example workflow dossiers showing the expected shape of real runs
- `docs/` - supporting docs and artifact examples only
- `README.md` - workflow model and install guidance

## Editing Rules

- The active session is the orchestrator.
- Operators and reviewers are subagents.
- Keep skill bodies client-neutral even if this repo also ships optional Codex runtime agent definitions.
- If `.codex/agents/` exists, treat it as the Codex implementation layer for the abstract workflow roles described by the skills.
- If `.codex/role-registry.toml` exists, treat it as the Codex binding layer from workflow roles to concrete agent names and substitutions.
- `workflow-run` is a meta-skill, not a stage.
- Agents define role behavior; skills define stage procedure.
- Operators own drafting or implementation work for their phase.
- Reviewers provide findings and recommendations but do not own the source artifact.
- The orchestrator writes the official consolidated review rounds and owns stage advancement.
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
- `workflow-run` should resolve one workflow mode at startup:
  - `light`
  - `standard`
  - `heavy`
- In `standard` and `heavy`, `idea`, `spec`, and `plan` reviews must use exactly:
  - two substantive reviewers
  - one skeptic
- In `light`, `idea`, `spec`, and `plan` reviews must use:
  - one substantive reviewer
  - one skeptic
- For `implementation-review`, reviews must use exactly:
  - architecture
  - security
  - QA / product correctness
- QA / product correctness should explicitly consider regressions, edge cases, and unit-test coverage expectations.
- `skeptical-review` remains an optional manual pressure-test skill. It is separate from the mandatory skeptic reviewer inside the standard workflow.
- `idea.md` stays idea-level and outcome-first.
- `spec.md` stays contract-level and planning-ready.
- `plan.md` stays the authoritative implementation document once implementation starts.
- `execution.md` stays optional and should be used sparingly as an evidence appendix.
- Create-stage skills should remain concise, self-contained, and stage-bounded.
- Review rounds should remain concise, findings-first, and recommendation-driven.
- User gates are required after:
  - idea review resolution in `standard` and `heavy`
  - spec review resolution
  - plan review resolution
  - implementation-review resolution
  - final-review gap resolution plus docs close-out
- In `light`, the first user gate may happen after a compressed idea/spec cycle, but both `idea.md` and `spec.md` should still exist in the dossier.
- Docs close-out is part of workflow completion.
- Repo-local `PLANS.md` and project `AGENTS.md` may be read as project context, but they should not silently override this workflow contract unless the user explicitly asks for repo-native planning mode.

## Consistency Checks

After changing the workflow or skill packages, verify:

- `skills/` contains the intended package set and no stale legacy package names
- every skill directory contains `SKILL.md`
- each skill's `name:` matches its folder name
- `README.md` and the skill package surface describe the same stage names and order
- `implementation-review` exists as a real skill and is included in the documented phase order
- if `.codex/agents/` exists, the agent set covers the intended operator and reviewer roles without changing the portable stage contract
- if `.codex/role-registry.toml` exists, it covers every role named in `workflow-run`, README, and the review skills
- artifact path references are consistent across all skills and docs
- review-round path references are consistent across all skills and docs
- `workflow-run` is documented consistently as the orchestrator rather than a workflow stage
- workflow modes are described consistently across README, AGENTS, and `workflow-run`
- idea/spec/plan review skills describe the correct reviewer count for `light` versus `standard`/`heavy`
- implementation-review specifies architecture, security, and QA / product correctness
- final-review reviewer roles are covered by the Codex runtime layer when `.codex/agents/` is present
- implement-plan points to implementation-review as the next formal review stage
- final-review is documented as fidelity review before docs close-out, not immediate closure
- run ledger guidance records:
  - workflow mode
  - actual role-to-agent bindings used
  - substitutions or fallbacks used
  - current orchestrator
  - current operator
  - current reviewer roster
  - current gate decision needed
  - implementation-review satisfaction state
  - documentation close-out status
- docs close-out is represented consistently across README and workflow-run guidance
- example dossiers under `docs/examples/` reflect the documented workflow modes and dossier shape
- skill folders can still be copied as-is into local Codex skill directories

## Current Limitations

- This repo now prioritizes Codex-first orchestration with subagents.
- There is no dedicated automated test harness yet; consistency is enforced by careful doc and package alignment.
