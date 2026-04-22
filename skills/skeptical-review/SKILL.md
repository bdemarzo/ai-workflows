---
name: skeptical-review
description: Apply an optional manual pressure-test outside the formal workflow to ideas, specs, plans, implementation summaries or diffs, architecture choices, product decisions, and workflow proposals. This is separate from the mandatory Skeptic reviewer used inside idea/spec/plan review.
---

# Skeptical Review

Use this skill to pressure-test an artifact with an intentionally skeptical stance. This skill remains optional and manual; it does not replace the mandatory `Skeptic` reviewer in normal idea, spec, and plan review phases.

Use for idea artifacts, specs, plans, implementation summaries or diffs, product decisions, architecture choices, and workflow proposals.

## Skeptical Posture

- assume the artifact is not ready until it proves otherwise
- prefer a short set of consequential critiques over comprehensive commentary or nits
- compare against strong products, standard practices, and realistic delivery constraints when relevant
- ground criticism in the actual artifact; do not invent disconnected hypothetical failures or soften direct conclusions

Requirements:
- identify the exact artifact or decision being challenged
- preserve the source artifact; do not overwrite it
- do not create new files for this skill
- distinguish fatal flaws, likely failure modes, missing evidence, and optional improvements
- explicitly state what evidence or change would change the conclusion

## Review Focus

- identify the strongest claim the artifact is making
- attack the hidden assumptions behind that claim
- ask what breaks first in real usage, delivery, operations, or adoption
- look for vague language, unpaid complexity, missing constraints, edge cases, rollout risks, and validation gaps
- compare the approach against industry-standard practice and how strong comparable products or teams usually solve the same problem
- when the artifact is user-facing, question usability, discoverability, trust, defaults, failure states, and accessibility
- when the artifact depends on new architecture or third-party services, question whether the tradeoff is really justified

## Output

- return the critique directly in the response
- identify the artifact or decision under review
- challenge the core claim
- group consequential findings by severity or type
- state what would change the conclusion
- finish with one allowed recommendation:
- `Recommendation: kill this approach`
- `Recommendation: narrow and retry`
- `Recommendation: revise before advancing`
- `Recommendation: proceed only if the stated risks are accepted`
- do not create workflow artifacts or standalone review files
