#!/usr/bin/env python3
"""Lightweight consistency checks for ai-workflows skills and workflow dossiers."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11 fallback
    tomllib = None


FORBIDDEN_RUN_HEADINGS = {
    "## Validation Evidence",
}

FORBIDDEN_SOURCE_HEADINGS = {
    "idea.md": {
        "## Revision History",
        "## Change Log",
        "## Changelog",
        "## Prior Decisions",
        "## Previous Decisions",
    },
    "spec.md": {
        "## Revision History",
        "## Change Log",
        "## Changelog",
        "## Prior Decisions",
        "## Previous Decisions",
    },
    "plan.md": {
        "## Revision History",
        "## Change Log",
        "## Changelog",
        "## Prior Decisions",
        "## Previous Decisions",
        "## Progress",
        "## Surprises & Discoveries",
        "## Outcomes & Retrospective",
    },
}

SOURCE_ARTIFACTS = {
    "run.md": "Run",
    "idea.md": "Idea",
    "spec.md": "Spec",
    "plan.md": "Plan",
    "execution.md": "Execution",
}

REVIEW_DIRS = {
    "idea",
    "spec",
    "plan",
    "implementation",
    "final",
}

CODEX_ADAPTER_ROOT = Path("adapters") / "codex"
COPILOT_ADAPTER_ROOT = Path("adapters") / "copilot"
CODEX_PLUGIN_TEMPLATE = Path("packages") / "codex-plugin" / "ai-workflows" / ".codex-plugin" / "plugin.json"
CODEX_MARKETPLACE_TEMPLATE = Path("marketplaces") / "codex-local" / "marketplace.json"


@dataclass
class Finding:
    level: str
    path: Path
    message: str

    def format(self, root: Path | None = None) -> str:
        display = self.path
        if root:
            try:
                display = self.path.resolve().relative_to(root.resolve())
            except ValueError:
                display = self.path
        return f"{self.level}: {display}: {self.message}"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def find_frontmatter_name(text: str) -> str | None:
    if not text.startswith("---"):
        return None

    end = text.find("\n---", 3)
    if end == -1:
        return None

    for line in text[3:end].splitlines():
        match = re.match(r"\s*name:\s*(.+?)\s*$", line)
        if match:
            return match.group(1).strip().strip('"').strip("'")
    return None


def find_frontmatter_value(text: str, key: str) -> str | None:
    if not text.startswith("---"):
        return None

    end = text.find("\n---", 3)
    if end == -1:
        return None

    for line in text[3:end].splitlines():
        match = re.match(rf"\s*{re.escape(key)}:\s*(.+?)\s*$", line)
        if match:
            return match.group(1).strip().strip('"').strip("'")
    return None


def parse_minimal_toml_value(raw: str) -> Any:
    raw = raw.strip()
    if raw.startswith('"') and raw.endswith('"'):
        return raw[1:-1]
    if raw.startswith("'") and raw.endswith("'"):
        return raw[1:-1]
    if raw.startswith("[") and raw.endswith("]"):
        values: list[str] = []
        for item in raw[1:-1].split(","):
            value = parse_minimal_toml_value(item)
            if isinstance(value, str):
                values.append(value)
        return values
    if raw.isdigit():
        return int(raw)
    return raw


def load_minimal_toml(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_stage: dict[str, Any] | None = None
    current_assignment: dict[str, Any] | None = None

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped == "[[stages]]":
            current_stage = {"assignments": []}
            current_assignment = None
            data.setdefault("stages", []).append(current_stage)
            continue

        if stripped == "[[stages.assignments]]":
            if current_stage is None:
                raise ValueError("assignment declared before stage")
            current_assignment = {}
            current_stage.setdefault("assignments", []).append(current_assignment)
            continue

        match = re.match(r"([A-Za-z0-9_-]+)\s*=\s*(.+)$", stripped)
        if not match:
            raise ValueError(f"unsupported TOML line: {stripped}")

        key, raw_value = match.groups()
        if current_assignment is not None:
            target = current_assignment
        elif current_stage is not None:
            target = current_stage
        else:
            target = data
        target[key] = parse_minimal_toml_value(raw_value)

    return data


def load_toml(path: Path, findings: list[Finding]) -> dict[str, Any] | None:
    try:
        text = read_text(path)
        if tomllib is not None:
            return tomllib.loads(text)
        return load_minimal_toml(text)
    except Exception as exc:
        findings.append(Finding("ERROR", path, f"invalid TOML: {exc}"))
        return None


def check_skills(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    skills_dir = root / "skills"

    if not skills_dir.exists():
        findings.append(Finding("ERROR", skills_dir, "skills directory is missing"))
        return findings

    for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            findings.append(Finding("ERROR", skill_dir, "missing SKILL.md"))
            continue

        text = read_text(skill_file)
        name = find_frontmatter_name(text)
        if name != skill_dir.name:
            findings.append(
                Finding(
                    "ERROR",
                    skill_file,
                    f"frontmatter name {name!r} does not match folder {skill_dir.name!r}",
                )
            )

    return findings


def check_registry_assignments(
    registry_path: Path,
    agent_names: set[str],
    adapter_label: str,
    findings: list[Finding],
) -> None:
    registry = load_toml(registry_path, findings)
    if registry is None:
        return

    stages = registry.get("stages")
    if not isinstance(stages, list):
        findings.append(Finding("ERROR", registry_path, "missing or invalid stages list"))
        return

    for stage in stages:
        stage_name = stage.get("name") if isinstance(stage, dict) else None
        assignments = stage.get("assignments") if isinstance(stage, dict) else None
        if not isinstance(stage_name, str) or not isinstance(assignments, list):
            findings.append(Finding("ERROR", registry_path, "stage is missing name or assignments"))
            continue

        for assignment in assignments:
            agent = assignment.get("agent") if isinstance(assignment, dict) else None
            if not isinstance(agent, str):
                findings.append(Finding("ERROR", registry_path, f"{stage_name} has an assignment without agent"))
            elif agent not in agent_names:
                findings.append(
                    Finding(
                        "ERROR",
                        registry_path,
                        f"{adapter_label} stage {stage_name!r} references missing agent {agent!r}",
                    )
                )


def check_codex_adapter(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    adapter_dir = root / CODEX_ADAPTER_ROOT
    if not adapter_dir.exists():
        return findings

    agents_dir = adapter_dir / "agents"
    registry_path = adapter_dir / "role-registry.toml"

    if not agents_dir.exists() and not registry_path.exists():
        return findings
    if not agents_dir.is_dir():
        findings.append(Finding("ERROR", agents_dir, "Codex agents directory is missing"))
        return findings
    if not registry_path.is_file():
        findings.append(Finding("ERROR", registry_path, "Codex role registry is missing"))
        return findings

    agent_names: set[str] = set()
    for agent_path in sorted(agents_dir.glob("*.toml")):
        agent_config = load_toml(agent_path, findings)
        if agent_config is None:
            continue
        name = agent_config.get("name")
        if not isinstance(name, str) or not name:
            findings.append(Finding("ERROR", agent_path, "Codex agent is missing string name"))
            continue
        agent_names.add(name)

    check_registry_assignments(registry_path, agent_names, "Codex", findings)
    return findings


def check_copilot_adapter(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    adapter_dir = root / COPILOT_ADAPTER_ROOT
    if not adapter_dir.exists():
        return findings

    agents_dir = adapter_dir / "agents"
    registry_path = adapter_dir / "role-registry.toml"

    if not agents_dir.exists() and not registry_path.exists():
        return findings
    if not agents_dir.is_dir():
        findings.append(Finding("ERROR", agents_dir, "Copilot agents directory is missing"))
        return findings
    if not registry_path.is_file():
        findings.append(Finding("ERROR", registry_path, "Copilot role registry is missing"))
        return findings

    agent_names: set[str] = set()
    for agent_path in sorted(agents_dir.glob("*.agent.md")):
        text = read_text(agent_path)
        name = find_frontmatter_value(text, "name")
        description = find_frontmatter_value(text, "description")
        if not name:
            findings.append(Finding("ERROR", agent_path, "Copilot agent is missing frontmatter name"))
            continue
        if not description:
            findings.append(Finding("ERROR", agent_path, "Copilot agent is missing frontmatter description"))
        agent_names.add(name)

    check_registry_assignments(registry_path, agent_names, "Copilot", findings)
    return findings


def check_adapters(root: Path) -> list[Finding]:
    return [*check_codex_adapter(root), *check_copilot_adapter(root)]


def check_plugin_packaging(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    manifest_path = root / CODEX_PLUGIN_TEMPLATE
    marketplace_path = root / CODEX_MARKETPLACE_TEMPLATE

    if manifest_path.exists():
        try:
            manifest = json.loads(read_text(manifest_path))
        except Exception as exc:
            findings.append(Finding("ERROR", manifest_path, f"invalid JSON: {exc}"))
            manifest = None

        if isinstance(manifest, dict):
            name = manifest.get("name")
            skills = manifest.get("skills")
            if not isinstance(name, str) or not name:
                findings.append(Finding("ERROR", manifest_path, "plugin manifest is missing string name"))
            if skills != "./skills/":
                findings.append(Finding("ERROR", manifest_path, "plugin manifest template must point skills to ./skills/"))

    if marketplace_path.exists():
        try:
            marketplace = json.loads(read_text(marketplace_path))
        except Exception as exc:
            findings.append(Finding("ERROR", marketplace_path, f"invalid JSON: {exc}"))
            marketplace = None

        if isinstance(marketplace, dict):
            plugins = marketplace.get("plugins")
            if not isinstance(plugins, list) or not plugins:
                findings.append(Finding("ERROR", marketplace_path, "marketplace must contain at least one plugin"))
            else:
                for plugin in plugins:
                    if not isinstance(plugin, dict):
                        findings.append(Finding("ERROR", marketplace_path, "marketplace plugin entry must be an object"))
                        continue
                    source = plugin.get("source")
                    source_path: str | None = None
                    if isinstance(source, str):
                        source_path = source
                    elif isinstance(source, dict) and isinstance(source.get("path"), str):
                        source_path = source["path"]
                    if not source_path:
                        findings.append(Finding("ERROR", marketplace_path, "marketplace plugin entry is missing source path"))
                        continue
                    if Path(source_path).is_absolute() or not source_path.startswith("./"):
                        findings.append(
                            Finding("ERROR", marketplace_path, "marketplace source path must be ./-relative")
                        )
                        continue
                    policy = plugin.get("policy")
                    if not isinstance(policy, dict):
                        findings.append(Finding("ERROR", marketplace_path, "marketplace plugin entry is missing policy"))

    return findings


def check_runtime_source_leakage(root: Path) -> list[Finding]:
    findings: list[Finding] = []

    for path in [
        root / ".codex",
        root / ".codex-plugin",
        root / ".agents",
    ]:
        if path.exists():
            findings.append(
                Finding("ERROR", path, "runtime install path should not be present in the source repository")
            )

    for path in [
        root / ".github" / "agents",
        root / ".github" / "ai-workflows",
        root / ".github" / "copilot-instructions.md",
    ]:
        if path.exists():
            findings.append(
                Finding("ERROR", path, "Copilot adapter source belongs under adapters/copilot")
            )

    return findings


def check_h1(path: Path, expected: str) -> list[Finding]:
    text = read_text(path)
    first_line = text.splitlines()[0] if text.splitlines() else ""
    if first_line != expected:
        return [Finding("ERROR", path, f"expected H1 {expected!r}, found {first_line!r}")]
    return []


def latest_rounds(dossier: Path, stage: str) -> list[Path]:
    review_dir = dossier / "reviews" / stage
    if not review_dir.exists():
        return []
    return sorted(review_dir.glob("round-*.md"))


def check_dossier(dossier: Path, stale_terms: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    slug = dossier.name

    if not dossier.exists():
        return [Finding("ERROR", dossier, "workflow dossier does not exist")]

    for filename, label in SOURCE_ARTIFACTS.items():
        path = dossier / filename
        if not path.exists():
            if filename == "execution.md":
                continue
            findings.append(Finding("ERROR", path, "required source artifact is missing"))
            continue

        findings.extend(check_h1(path, f"# {label} - {slug}"))
        text = read_text(path)

        if filename == "run.md":
            for heading in FORBIDDEN_RUN_HEADINGS:
                if re.search(rf"^{re.escape(heading)}\s*$", text, flags=re.MULTILINE):
                    findings.append(
                        Finding("WARN", path, f"forbidden run ledger section present: {heading}")
                    )
            for stage in sorted(REVIEW_DIRS):
                rounds = latest_rounds(dossier, stage)
                if rounds:
                    latest = rounds[-1]
                    expected_ref = f"./docs/workflows/{slug}/reviews/{stage}/{latest.name}"
                    alternate_ref = f"docs/workflows/{slug}/reviews/{stage}/{latest.name}"
                    if expected_ref not in text and alternate_ref not in text:
                        findings.append(
                            Finding(
                                "WARN",
                                path,
                                f"latest {stage} review {latest.name} is not referenced explicitly",
                            )
                        )

        for heading in FORBIDDEN_SOURCE_HEADINGS.get(filename, set()):
            if re.search(rf"^{re.escape(heading)}\s*$", text, flags=re.MULTILINE):
                findings.append(
                    Finding(
                        "WARN",
                        path,
                        f"source artifact history section should move to review rounds or execution evidence: {heading}",
                    )
                )

        for term in stale_terms:
            if re.search(re.escape(term), text, flags=re.IGNORECASE):
                findings.append(Finding("WARN", path, f"possible stale legacy term found: {term!r}"))

    for stage in sorted(REVIEW_DIRS):
        for path in latest_rounds(dossier, stage):
            text = read_text(path)
            expected = f"# {stage.title().replace('-', ' ')} Review Round {path.stem[-2:]} - {slug}"
            if stage == "implementation":
                expected = f"# Implementation Review Round {path.stem[-2:]} - {slug}"
            if stage == "final":
                expected = f"# Final Review Round {path.stem[-2:]} - {slug}"
            findings.extend(check_h1(path, expected))

    return findings


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root containing skills/ (default: current directory).",
    )
    parser.add_argument(
        "--dossier",
        type=Path,
        action="append",
        default=[],
        help="Workflow dossier path to inspect. May be provided multiple times.",
    )
    parser.add_argument(
        "--stale-term",
        action="append",
        default=[],
        help="Term to report as possible stale legacy wording in source artifacts.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    findings = check_skills(root)
    findings.extend(check_runtime_source_leakage(root))
    findings.extend(check_plugin_packaging(root))
    findings.extend(check_adapters(root))

    stale_terms = args.stale_term
    for dossier in args.dossier:
        findings.extend(check_dossier(dossier.resolve(), stale_terms))

    for finding in findings:
        print(finding.format(root))

    errors = [finding for finding in findings if finding.level == "ERROR"]
    if errors:
        print(f"\n{len(errors)} error(s), {len(findings) - len(errors)} warning(s)")
        return 1

    print(f"{len(findings)} warning(s), 0 error(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
