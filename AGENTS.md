# AGENTS.md

## Repository Purpose

This repository ships portable workflow skill packages for AI-assisted product and engineering work.

The human-facing workflow contract lives in `README.md`.

Use this file for repo-specific operating guidance when changing the skills or docs.

## Source Of Truth

- `skills/` is the canonical source of truth for shipped skill packages.
- `README.md` is the canonical human-facing description of the workflow, stage names, and artifact paths.
- Keep skill package names, `name:` frontmatter, and README stage names aligned.

## Repo Layout

- `skills/<skill-name>/SKILL.md` - canonical skill packages
- `docs/` - supporting docs and artifact examples only; do not duplicate the full workflow contract here unless there is a clear need
- `README.md` - workflow model and install guidance

## Editing Rules

- Keep skill instructions client-neutral. Do not add Codex-only or Claude-only behavior to the skill bodies.
- If you rename, add, or remove a stage, update all of these together:
  - the skill folder name
  - the `name:` field in that skill's frontmatter
  - `README.md`
  - install examples in `README.md`
- Preserve the per-workflow dossier layout:
  - `docs/workflows/{slug}/run.md`
  - `docs/workflows/{slug}/idea.md`
  - `docs/workflows/{slug}/spec.md`
  - `docs/workflows/{slug}/plan.md`
  - `docs/workflows/{slug}/execution.md`
- Preserve the per-workflow review-round layout:
  - `docs/workflows/{slug}/reviews/idea/round-01.md`
  - `docs/workflows/{slug}/reviews/spec/round-01.md`
  - `docs/workflows/{slug}/reviews/plan/round-01.md`
  - `docs/workflows/{slug}/reviews/final/round-01.md`
- Create a new review round for each review pass. Do not overwrite older rounds.
- Use zero-padded review round names such as `round-01.md`, `round-02.md`, and `round-03.md`.
- Review stages should stay artifact-specific and should adapt reviewer personas based on scope, risk, and affected surface area.
- Review rounds should be written as structured stakeholder debates that still end in actionable suggestions and an explicit recommendation.
- The persona method belongs in the skill body, not in the stage name.
- `workflow-run` is a meta-skill, not a stage. It may coordinate the stage skills, keep a run ledger, and decide when to advance.
- Review stages should produce explicit recommendations and evidence. They should not be written as the final authority on stage advancement.
- Optional repo-local guidance such as `PLANS.md` is supplementary. The canonical workflow and copied skill packages must still be usable when that guidance file is absent.
- The workflow dossier slug is the default traceability anchor. Avoid reintroducing separate stage-level naming schemes unless there is a strong reason.
- If a workflow intentionally splits or merges scope, create or reference the related workflow dossier and explain the relationship in the run ledger and affected stage files.
- Create artifacts should be self-contained enough for a later contributor to understand the stage without reopening the entire conversation.
- `plan.md` should behave like a living implementation plan and keep sections such as `Progress`, `Surprises & Discoveries`, `Decision Log`, `Validation and Acceptance`, and `Outcomes & Retrospective` current as work evolves.
- `execution.md` should capture implementation evidence, deviations, validation, blockers, and follow-up work.
- Orchestration should support a startup question gate with three modes: fully automated, blocking questions only, and ask many questions.
- Orchestration may infer `question_mode` from clear natural-language instructions. If the mode is ambiguous, it should ask the standardized fallback question once.
- The run ledger should include a top-level `question_mode:` field near the top so resumed orchestration behaves consistently.
- The run ledger should be maintained as a living lifecycle document with required sections for progress, decisions, discoveries, validation, blockers, and resume instructions.
- Another agent should be able to resume an in-progress workflow from `docs/workflows/{slug}/run.md` plus the linked artifacts without needing prior thread context.
- Orchestration should enforce hard stop rules for repeated unresolved issues, bounded loop counts, required approvals, missing access, or materially blocking ambiguity.

## Consistency Checks

After changing the workflow or skill packages, verify:

- `skills/` contains the intended package set and no stale legacy package names
- every skill directory contains `SKILL.md`
- each skill's `name:` matches its folder name
- `README.md` and the skill package surface describe the same stage names and order
- artifact path references are consistent across all skills and docs
- dossier path references are consistent across all skills and docs
- review-round path references are consistent across all skills and docs
- `workflow-run` is documented consistently as an orchestrator rather than a workflow stage
- traceability expectations are consistent across the create, review, implementation, and final review stages
- run ledger path references are consistent across the orchestrator skill and docs
- run ledger examples and guidance consistently use a top-level `question_mode:` field
- `question_mode` inference and fallback-question behavior are described consistently across the orchestrator skill and docs
- run ledger lifecycle sections and update rules are described consistently across the orchestrator skill and docs
- optional repo-local guidance such as `PLANS.md` is documented as optional rather than assumed
- review rounds preserve history instead of instructing in-place overwrite
- skill folders can still be copied as-is into local Claude and Codex skill directories

## Current Limitations

- This repo currently targets Claude and Codex only.
- There is no dedicated automated test harness yet; consistency is enforced by careful doc and package alignment.
