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
| `idea-create` | Create or refine a product idea before it becomes a contract. | Product owner | None by default during creation. | `docs/ideas/{topic}.md` |
| `idea-review` | Pressure-test the idea for value, feasibility, and user relevance. | Review skill | Key stakeholders, power users, and technical product manager. Add or remove personas based on scope. | `docs/reviews/ideas/{topic}.md` |
| `spec-create` | Turn the approved idea into a functional product contract. | Technical product manager | None by default during creation. | `docs/specs/{featurename}.md` |
| `spec-review` | Review the spec for clarity, completeness, user value, and implementation readiness at the contract level. | Review skill | Product owner, architect, and scope-appropriate stakeholder or power-user personas. | `docs/reviews/specs/{featurename}.md` |
| `plan-create` | Turn the approved spec into an implementation-ready engineering plan. | Architect | None by default during creation. | `docs/plans/{planname}.md` |
| `plan-review` | Perform peer review of the plan from architectural and engineering perspectives across the relevant parts of the stack. | Review skill | Engineer and technical product manager by default. Include additional architectural or domain-specific personas when the plan scope requires it. | `docs/reviews/plans/{planname}.md` |
| `implement-plan` | Implement the approved plan in bounded, validated steps. | Engineer | None during implementation beyond normal validation. | Code changes plus optional `docs/executions/{planname}.md` |
| `final-review` | Review the full workflow outcome for architectural quality, product correctness, process fit, and contract fidelity. | Review skill | Architect, product owner, and technical product manager by default. Add or remove personas based on scope. | `docs/reviews/finals/{artifactname}.md` |

## Orchestration

- `workflow-run` is a meta-skill, not a stage.
- It should use the stage skills in order, maintain a run ledger at `docs/runs/{slug}.md`, and decide when to revise or advance.
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

- After ideation, reuse one canonical slug by default for the spec, plan, execution log, and final review.
- Allow a different downstream slug only when the workflow intentionally splits or merges scope.
- When names diverge, the artifact body should explain why and link to the source artifact it came from.
- Workflow runs should keep the canonical slug and current artifact paths in `docs/runs/{slug}.md`.
- Review artifacts should state the exact reviewed artifact path.
- Specs created from ideas should link back to the source idea artifact.
- Plans should link to the source spec artifact.
- Execution summaries should link to the source plan artifact.
- Final reviews should list all reviewed artifact paths.

## Run Files

- Store orchestration ledgers under `docs/runs/{slug}.md`.
- Put a top-level `question_mode:` field near the top of the run ledger so resumed runs stay deterministic.
- Use the run ledger to record question mode, current stage, artifact paths, loop counts, assumptions, recommendations, decisions, and blockers.

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

## Review Files

- Store review artifacts under `docs/reviews/<artifact-type>/`.
- Use one current review file per reviewed artifact:
  - `docs/reviews/ideas/{topic}.md`
  - `docs/reviews/specs/{featurename}.md`
  - `docs/reviews/plans/{planname}.md`
  - `docs/reviews/finals/{artifactname}.md`
- Update the current review file in place on subsequent review rounds by default.
- Do not create numbered review files like `{featurename}-1.md` or `{featurename}-2.md`.
- If a past review snapshot must be preserved separately, create an explicit dated archive copy instead of using numeric suffixes.
- Review artifacts should end with an explicit recommendation. The recommendation informs advancement, but does not control it.

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
