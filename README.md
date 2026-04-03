# ai-workflows

Portable workflow skills for AI-assisted product and engineering work.

## Layout

- `skills/` - canonical skill packages
- `docs/` - minimal overview and supporting documentation
- `README.md` - repo overview and install instructions

## Packages

- `workflow-run`
- `idea-create`
- `idea-review`
- `spec-create`
- `spec-review`
- `plan-create`
- `plan-review`
- `implement-plan`
- `final-review`

Each skill lives in `skills/<skill-name>/` and is distributed as a portable `SKILL.md`-based package. Some skills may also consult optional repo-local guidance such as `PLANS.md` when it is present.

## Canonical Workflow

The workflow has three design loops followed by implementation and a final review:

- ideate: `idea-create` and `idea-review` for high-level design
- spec: `spec-create` and `spec-review` for functional design
- plan: `plan-create` and `plan-review` for technical design
- implementation: `implement-plan`
- final review: `final-review`

Review stages should adapt the participating personas to the scope of the artifact being reviewed rather than using the exact same reviewer set every time.
`workflow-run` is the optional orchestrator skill that can drive the full lifecycle unattended from a starting prompt.

| Canonical Stage | Purpose | Primary Owner | Reviewers / Perspectives | Output |
| --- | --- | --- | --- | --- |
| `idea-create` | Create or refine a product idea before it becomes a contract. | Product owner | None by default during creation. | `docs/workflows/{slug}/idea.md` |
| `idea-review` | Pressure-test the idea for value, feasibility, and user relevance. | Review skill | Key stakeholders, power users, and technical product manager. Add or remove personas based on scope. | `docs/workflows/{slug}/reviews/idea/round-01.md` |
| `spec-create` | Turn the approved idea into a functional product contract. | Technical product manager | None by default during creation. | `docs/workflows/{slug}/spec.md` |
| `spec-review` | Review the spec for clarity, completeness, user value, and implementation readiness at the contract level. | Review skill | Product owner, architect, and scope-appropriate stakeholder or power-user personas. | `docs/workflows/{slug}/reviews/spec/round-01.md` |
| `plan-create` | Turn the approved spec into an implementation-ready engineering plan. | Architect | None by default during creation. | `docs/workflows/{slug}/plan.md` |
| `plan-review` | Perform peer review of the plan from architectural and engineering perspectives across the relevant parts of the stack. | Review skill | Engineer and technical product manager by default. Include additional architectural or domain-specific personas when the plan scope requires it. | `docs/workflows/{slug}/reviews/plan/round-01.md` |
| `implement-plan` | Implement the approved plan in bounded, validated steps. | Engineer | None during implementation beyond normal validation. | Code changes plus optional `docs/workflows/{slug}/execution.md` |
| `final-review` | Review the full workflow outcome for architectural quality, product correctness, process fit, and contract fidelity. | Review skill | Architect, product owner, and technical product manager by default. Add or remove personas based on scope. | `docs/workflows/{slug}/reviews/final/round-01.md` |

## Workflow Dossiers

Store each workflow in a single dossier under `docs/workflows/{slug}/`.

Use this structure:

- `docs/workflows/{slug}/run.md`
- `docs/workflows/{slug}/idea.md`
- `docs/workflows/{slug}/spec.md`
- `docs/workflows/{slug}/plan.md`
- `docs/workflows/{slug}/execution.md` when implementation needs a run log
- `docs/workflows/{slug}/reviews/idea/round-01.md`
- `docs/workflows/{slug}/reviews/spec/round-01.md`
- `docs/workflows/{slug}/reviews/plan/round-01.md`
- `docs/workflows/{slug}/reviews/final/round-01.md`

Keep one canonical `slug` for the whole workflow dossier by default. Fixed file names inside the dossier replace the older per-stage naming scheme.

If a workflow intentionally splits or merges scope, create or reference the related workflow dossier and explain the relationship in both dossiers and in the relevant stage artifacts.

## Orchestration

- `workflow-run` is a meta-skill, not a stage.
- It should use the stage skills in order, maintain a living lifecycle document at `docs/workflows/{slug}/run.md`, and decide when to revise or advance.
- Review stages should produce evidence and explicit recommendations. The orchestrator or a human decides whether the current stage is ready.
- The orchestrator should use `question_mode` when explicitly provided.
- If the user's wording clearly implies a mode, the orchestrator should infer it and record the inferred value in `question_mode:`.
- If the mode is still ambiguous, the orchestrator should ask one startup question:
  - fully automated: ask no questions after startup and proceed with reasonable assumptions
  - blocking questions only: ask only when a materially important decision cannot be safely assumed
  - ask many questions: ask whenever a non-obvious decision could materially improve the result
- Use this standardized fallback wording when the mode is ambiguous:
  - `Choose question_mode for workflow-run: fully automated, blocking questions only, or ask many questions.`
- Hard stop rules for orchestration:
  - stop after a bounded number of loops per stage, such as 3
  - stop when the same unresolved issue persists across 2 consecutive loops
  - stop for required approvals, missing access, or ambiguities that would materially invalidate downstream work

## Review Adaptation

- Review skills should choose reviewer personas based on artifact scope, risk, and affected surface area.
- Narrow changes can use a smaller reviewer set.
- Broad, high-risk, user-facing, or cross-functional changes should pull in more perspectives.
- The persona method is an implementation detail of the review stage, not the stage name itself.

## Traceability

- The workflow dossier slug is the default traceability anchor for all stage artifacts.
- `run.md` should keep the current artifact map, review-round paths, decisions, blockers, and resume context.
- `idea.md`, `spec.md`, `plan.md`, and `execution.md` should each identify their immediate source artifact when one exists.
- Review rounds should state the exact reviewed artifact path and link the immediately prior round when one exists.
- Later review rounds should explain what changed since the prior round before restating their recommendation.
- If work forks into a new workflow dossier, the source dossier should link to the new slug and explain why the split happened.

## Run Files

- Store orchestration ledgers at `docs/workflows/{slug}/run.md`.
- Put these top-level fields near the top of the run ledger:
  - `question_mode:`
  - `canonical_slug:`
  - `current_stage:`
  - `workflow_status:`
- Treat `run.md` as a living lifecycle document, not a thin status note.
- Keep these sections current:
  - `# Purpose / Big Picture`
  - `## Artifact Map`
  - `## Progress`
  - `## Stage Assessments`
  - `## Questions and Assumptions`
  - `## Decision Log`
  - `## Surprises & Discoveries`
  - `## Validation Evidence`
  - `## Current Blockers`
  - `## Resume Instructions`
  - `## Outcomes & Retrospective`
- Update the run ledger at every stage transition and every stopping point so another agent can resume from the run ledger plus the linked artifacts.

## Stage Files

The stage files should be richer than thin placeholders.

- `idea.md` should capture the idea in self-contained product language, including purpose, user problem, proposed direction, expected value, tradeoffs, open questions, and revision history.
- `spec.md` should act as the functional contract, with scope, flows, constraints, acceptance criteria, open questions, and revision history.
- `plan.md` should behave like a living implementation plan. It should be self-contained enough that a later agent can implement from the plan plus the repository. Keep `Progress`, `Surprises & Discoveries`, `Decision Log`, `Validation and Acceptance`, and `Outcomes & Retrospective` current as work evolves.
- `execution.md` should capture implementation evidence, including work log entries, commands run, validation results, deviations from the plan, blockers, and follow-up work.

## Review Files

- Store review rounds under the workflow dossier, grouped by stage:
  - `docs/workflows/{slug}/reviews/idea/round-01.md`
  - `docs/workflows/{slug}/reviews/spec/round-01.md`
  - `docs/workflows/{slug}/reviews/plan/round-01.md`
  - `docs/workflows/{slug}/reviews/final/round-01.md`
- Create a new round file for each new review pass. Do not overwrite earlier rounds.
- Use zero-padded numbering such as `round-01.md`, `round-02.md`, and `round-03.md`.
- Treat review rounds as structured debates among the chosen personas.
- Review rounds should include sections like:
  - `Reviewed Artifact`
  - `Prior Review Rounds` when relevant
  - `Participants`
  - `Review Scope`
  - `Opening Positions`
  - `Debate`
  - `Points of Agreement`
  - `Points of Disagreement`
  - `Suggested Revisions`
  - `Recommendation`
  - `Outstanding Dissent`
- Each review round should end with an explicit recommendation. The recommendation informs advancement, but does not control it.

## Example Prompts

Use `workflow-run` when you want the full lifecycle coordinated from a starting prompt.

```text
Use workflow-run to take this from idea through final review.
question_mode: fully automated
Prompt: Build a lightweight internal release notes tool for product and engineering teams.
```

```text
Use workflow-run to drive this workflow.
question_mode: blocking questions only
Prompt: Design and implement a customer-facing feature flag dashboard for account admins.
```

```text
Use workflow-run to coordinate the full process.
question_mode: ask many questions
Prompt: Explore and deliver a better onboarding flow for first-time users in our web app.
```

Natural-language mode inference is also valid:

```text
Use workflow-run for this feature and ask only if you have blocking questions.
Prompt: Build an internal customer feedback triage dashboard.
```

## Install for Claude

Copy any skill folder from `skills/` into your Claude skills directory:

```text
skills/workflow-run -> ~/.claude/skills/workflow-run
skills/implement-plan -> ~/.claude/skills/implement-plan
```

To install all of them, copy each folder under `skills/` into:

```text
~/.claude/skills/
```

## Install for Codex

Copy any skill folder from `skills/` into your Codex skills directory:

```text
skills/workflow-run -> ~/.codex/skills/workflow-run
skills/implement-plan -> ~/.codex/skills/implement-plan
```

To install all of them, copy each folder under `skills/` into:

```text
~/.codex/skills/
```

## Notes

- The skills are intentionally client-neutral and copy-based for now.
- `PLANS.md` is an optional repo-local extension point for planning and implementation guidance. Its absence is normal and should not block use of the canonical skills.
- This repo currently targets Claude and Codex only.
- If a future client needs extra packaging, that should be added as a thin adapter without changing the canonical skill packages in `skills/`.
