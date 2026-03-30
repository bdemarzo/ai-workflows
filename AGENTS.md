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
- Preserve the folder-by-type artifact path layout for primary artifacts:
  - `docs/runs/{slug}.md`
  - `docs/ideas/{topic}.md`
  - `docs/specs/{featurename}.md`
  - `docs/plans/{planname}.md`
  - `docs/executions/{planname}.md`
- Preserve the typed review path layout for review artifacts:
  - `docs/reviews/ideas/{topic}.md`
  - `docs/reviews/specs/{featurename}.md`
  - `docs/reviews/plans/{planname}.md`
  - `docs/reviews/finals/{artifactname}.md`
- Update current review files in place by default.
- Do not create numbered review files like `-1` or `-2`; if a historical review snapshot must be kept separately, use an explicit dated archive copy instead.
- Review stages should stay artifact-specific and should adapt reviewer personas based on scope, risk, and affected surface area.
- The persona method belongs in the skill body, not in the stage name.
- `workflow-run` is a meta-skill, not a stage. It may coordinate the stage skills, keep a run ledger, and decide when to advance.
- Review stages should produce explicit recommendations and evidence. They should not be written as the final authority on stage advancement.
- Optional repo-local guidance such as `PLANS.md` is supplementary. The canonical workflow and copied skill packages must still be usable when that guidance file is absent.
- After ideation, downstream artifacts should reuse one canonical slug by default. If a workflow intentionally splits or merges scope, the artifact body should explain the divergence and link to the source artifact.
- Orchestration should support a startup question gate with three modes: fully automated, blocking questions only, and ask many questions.
- Orchestration may infer `question_mode` from clear natural-language instructions. If the mode is ambiguous, it should ask the standardized fallback question once.
- The run ledger should include a top-level `question_mode:` field near the top so resumed orchestration behaves consistently.
- Orchestration should enforce hard stop rules for repeated unresolved issues, bounded loop counts, required approvals, missing access, or materially blocking ambiguity.

## Consistency Checks

After changing the workflow or skill packages, verify:

- `skills/` contains the intended package set and no stale legacy package names
- every skill directory contains `SKILL.md`
- each skill's `name:` matches its folder name
- `README.md` and the skill package surface describe the same stage names and order
- artifact path references are consistent across all skills and docs
- `workflow-run` is documented consistently as an orchestrator rather than a workflow stage
- traceability expectations are consistent across the create, review, implementation, and final review stages
- run ledger path references are consistent across the orchestrator skill and docs
- run ledger examples and guidance consistently use a top-level `question_mode:` field
- `question_mode` inference and fallback-question behavior are described consistently across the orchestrator skill and docs
- optional repo-local guidance such as `PLANS.md` is documented as optional rather than assumed
- skill folders can still be copied as-is into local Claude and Codex skill directories

## Current Limitations

- This repo currently targets Claude and Codex only.
- There is no dedicated automated test harness yet; consistency is enforced by careful doc and package alignment.
