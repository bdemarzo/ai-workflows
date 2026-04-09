---
name: skeptical-review
description: Apply an adversarial, high-skepticism review lens to an idea, spec, plan, implementation summary, or shipped change. Use when the user wants a harsh reality check, wants someone to find meaningful flaws, wants stronger dissent than a normal review stage provides, or wants to pressure-test whether something is under-specified, risky, overbuilt, solving the wrong problem, or weaker than industry-standard practice.
---

# Skeptical Review

Use this skill to pressure-test an artifact with an intentionally skeptical stance.

This is not a balanced peer review. It is a targeted search for consequential weaknesses.

Use it on:
- an idea artifact
- a spec
- a plan
- an implementation summary or diff
- a product decision, architecture choice, or workflow proposal

Default posture:
- assume the artifact is not ready until it proves otherwise
- look for meaningful flaws, not nits
- prefer a short list of consequential criticisms over a long list of minor comments
- compare against strong products, standard practices, and realistic delivery constraints when relevant
- do not soften the conclusion to preserve team harmony

Requirements:
- identify the exact artifact or decision being challenged
- preserve the source artifact; do not overwrite it
- do not create new files for this skill
- ground criticism in the actual artifact rather than inventing hypothetical failures with no connection to the text
- distinguish between:
  - fatal flaws
  - likely failure modes
  - missing evidence
  - optional improvements
- explicitly state what evidence or change would change the conclusion
- prefer direct language over diplomatic filler
- recommend kill, narrow, defer, revise, or proceed despite risk when appropriate

Review method:
- start by identifying the strongest claim the artifact is making
- attack the hidden assumptions behind that claim
- ask what breaks first in real usage, delivery, operations, or adoption
- look for vague language hiding unresolved decisions
- look for complexity that is not paying for itself
- look for missing constraints, edge cases, rollout risks, and validation gaps
- compare the approach against industry-standard practice and how strong comparable products or teams usually solve the same problem
- when the artifact is user-facing, question usability, discoverability, trust, defaults, failure states, and accessibility
- when the artifact depends on new architecture or third-party services, question whether the tradeoff is really justified

Do not:
- pad the response with generic negativity
- nitpick wording unless wording hides a material ambiguity
- pretend certainty where the artifact only supports a risk judgment
- collapse into a normal balanced review voice

Write the output with sections like:
- artifact under review
- core claim being challenged
- fatal flaws
- likely failure modes
- benchmark and best-practice gaps
- missing evidence
- what would change my mind
- recommendation

Recommendation styles:
- `Recommendation: kill this approach`
- `Recommendation: narrow and retry`
- `Recommendation: revise before advancing`
- `Recommendation: proceed only if the stated risks are accepted`

Return the critique directly in the response. This skill is interactive by default and should not create workflow artifacts or standalone review files unless the skill is explicitly revised later to do so.
