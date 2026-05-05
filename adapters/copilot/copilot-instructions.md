# ai-workflows Copilot Instructions

This repository ships portable workflow skill packages plus runtime adapters.

- Treat `skills/` as the canonical source of truth for workflow skills.
- Treat `adapters/codex/` as the Codex adapter source and `adapters/copilot/` as the GitHub Copilot adapter source.
- Treat `.codex/`, `.agents/`, and `.github/` as installer output paths in target repositories, not as source layout for this repository.
- Keep adapter role registries aligned with README stage names and skill package names.
- Do not duplicate or fork skill behavior into adapter files; adapter files should bind personas and runtime mechanics only.
- When running the installer, require an explicit runtime: `--runtime codex` or `--runtime copilot`.
- After changing skills, docs, or adapters, run `python scripts/check_workflow_artifacts.py --root .`.
