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
- When a workflow has meaningful UI, UX, navigation, or interaction surface area, idea-review and spec-review should include an explicit UX or product-design perspective, and plan-review should include one when delivery risk depends on interface behavior.
- Review methods should require independent opening positions, an explicitly skeptical or risk-focused perspective, and preservation of meaningful dissent when important weaknesses remain.
- For non-trivial or user-facing work, review stages should benchmark against industry-standard practices and how comparable successful products or applications solve similar problems.
- Review rounds should be written as structured stakeholder debates that still end in actionable suggestions and an explicit recommendation.
- The persona method belongs in the skill body, not in the stage name.
- `workflow-run` is a meta-skill, not a stage. It may coordinate the stage skills, keep a run ledger, and decide when to advance.
- `skeptical-review` is an optional manual pressure-test skill, not a workflow stage, not part of the canonical dossier layout, and should return feedback directly instead of creating new files.
- Review stages should produce explicit recommendations and evidence. They should not be written as the final authority on stage advancement.
- Repo-local `PLANS.md` and project `AGENTS.md` may be authoritative for planning and implementation behavior. When a project requires `PLANS.md`, that requirement should outrank portable defaults.
- The workflow dossier slug is the default traceability anchor. Avoid reintroducing separate stage-level naming schemes unless there is a strong reason.
- If a workflow intentionally splits or merges scope, create or reference the related workflow dossier and explain the relationship in the run ledger and affected stage files.
- Create artifacts should be self-contained enough for a later contributor to understand the stage without reopening the entire conversation.
- `idea.md` should stay idea-level, but should be outcome-first, self-contained, and clear about how value would be recognized.
- `spec.md` should stay contract-level, but should be self-contained enough for planning from the artifact alone and should capture observable acceptance behavior and important boundary conditions.
- `plan.md` should behave like a living implementation plan and keep sections such as `Progress`, `Surprises & Discoveries`, `Decision Log`, `Validation and Acceptance`, and `Outcomes & Retrospective` current as work evolves.
- In `execplan` environments, `plan.md` is the authoritative implementation document once implementation starts and should be restartable without relying on `run.md`.
- `execution.md` should capture implementation evidence, deviations, validation, blockers, and follow-up work.
- In `execplan` environments, use `execution.md` sparingly as an optional evidence appendix rather than a second control document.
- Orchestration should support a startup question gate with three modes: fully automated, blocking questions only, and ask many questions.
- Orchestration may infer `question_mode` from clear natural-language instructions. If the mode is ambiguous, it should ask one plain-language startup question about how autonomous it should be, not a CLI-style option prompt.
- New architectural directions, major architectural constraints, and new third-party services, SDKs, hosted platforms, or external tools should count as materially important decisions for orchestration.
- In `blocking questions only`, those decisions should be surfaced as blocking questions before they are locked in.
- In `fully automated`, those decisions should be self-answered and documented in the run ledger and affected source artifact.
- Orchestration should also support an optional `stage_gate_mode` that controls whether the workflow pauses for human approval before major stage transitions.
- If the user's stage-gate preference is ambiguous, orchestration should ask one plain-language startup question about whether to pause at major stage boundaries or run straight through.
- In v1, support only `none` and `loop boundaries`.
- `loop boundaries` should pause only after `idea-review`, `spec-review`, `plan-review`, and `implement-plan`, and should not add a completion gate after `final-review`.
- Stage gates are transition checkpoints, not clarification questions.
- The run ledger should record question mode, stage gate mode, execution plan mode, current stage, workflow status, and pending transition when relevant in plain text under a `Workflow Guidelines` subsection inside `Purpose / Big Picture`.
- The run ledger should also preserve materially important interaction history: key questions asked, answers received, clarifications, unresolved threads, and the decisions those interactions caused.
- The run ledger should be maintained as a living lifecycle document with required sections for progress, decisions, discoveries, validation, blockers, and resume instructions.
- Another agent should be able to resume an in-progress workflow from `docs/workflows/{slug}/run.md` plus the linked artifacts without needing prior thread context.
- Orchestration should enforce hard stop rules for repeated unresolved issues, bounded loop counts, required approvals, missing access, or materially blocking ambiguity.
- When paused at a stage gate, `workflow_status` should be `awaiting-stage-approval` and `Resume Instructions` should state the approval decision needed.
- In `execplan` environments, `workflow-run` should determine `execution_plan_mode` automatically from root `PLANS.md` or project `AGENTS.md`.
- In `execplan` environments, `run.md` should be reduced during implementation to orchestration data rather than duplicating detailed execution progress.
- Accepted idea-review decisions should be consolidated back into `idea.md` before spec creation advances.
- Accepted spec-review decisions should be consolidated back into `spec.md` before planning advances.
- Accepted plan-review decisions should be consolidated back into `plan.md` before implementation starts.
- Review rounds should remain design and review evidence, not alternative execution sources of truth.

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
- idea and spec guidance clearly require self-containment, observable outcomes, and consolidation of accepted review decisions back into the source artifact
- run ledger path references are consistent across the orchestrator skill and docs
- run ledger examples and guidance consistently place workflow guidance under `Purpose / Big Picture` instead of as top-of-file header fields
- run ledger guidance consistently requires materially important question and answer history to be recorded in enough detail for restartability
- `question_mode` inference and plain-language startup-question behavior are described consistently across the orchestrator skill and docs
- `stage_gate_mode` startup-question behavior, inference behavior, and gated transitions are described consistently across the orchestrator skill and docs
- `execution_plan_mode` resolution and `execplan` behavior are described consistently across the orchestrator skill and docs
- run ledger lifecycle sections and update rules are described consistently across the orchestrator skill and docs
- repo-local `PLANS.md` and project `AGENTS.md` precedence are documented consistently
- review rounds preserve history instead of instructing in-place overwrite
- review skills consistently require independent opening positions, a skeptical perspective, and preservation of meaningful dissent
- review skills consistently require benchmark or best-practice comparison for non-trivial or user-facing work
- no review skill is described as owning stage-gate decisions; gates remain owned by `workflow-run`
- idea-review and spec-review outputs are documented as inputs to source-artifact consolidation rather than alternative truth sources
- plan-review outputs are documented as inputs to plan consolidation rather than alternative execution control docs
- skill folders can still be copied as-is into local Claude and Codex skill directories

## Current Limitations

- This repo currently targets Claude and Codex only.
- There is no dedicated automated test harness yet; consistency is enforced by careful doc and package alignment.
