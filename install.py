#!/usr/bin/env python3
"""Install ai-workflows skills and a selected runtime adapter into another repository."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List


CODEX_PROJECT_ADAPTER_ENTRIES = ("role-registry.toml", "config.toml")
COPILOT_PROJECT_ADAPTER_ENTRIES = ("role-registry.toml", "config.toml")


@dataclass
class InstallResult:
    installed: List[Path]
    skipped: List[Path]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Install ai-workflows skills and the selected runtime adapter into "
            "the current repository."
        )
    )
    parser.add_argument(
        "--runtime",
        choices=("codex", "copilot"),
        required=True,
        help="Runtime adapter to install. Must be either 'codex' or 'copilot'.",
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=Path.cwd(),
        help="Target repository root. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace existing managed skill and adapter files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned changes without writing files.",
    )
    parser.add_argument(
        "--no-skills",
        action="store_true",
        help="Do not install skill packages.",
    )
    parser.add_argument(
        "--no-adapter",
        action="store_true",
        help="Do not install the selected runtime adapter layer.",
    )
    parser.add_argument(
        "--global-skills",
        action="store_true",
        help="For --runtime codex only: install skills to ~/.codex/skills instead of the target repo's .codex/skills.",
    )
    return parser.parse_args()


def ensure_source_layout(source_root: Path, runtime: str, needs_skills: bool, needs_adapter: bool) -> None:
    if needs_skills:
        skills_root = source_root / "skills"
        if not skills_root.is_dir():
            raise FileNotFoundError(f"Missing source skills directory: {skills_root}")

    if not needs_adapter:
        return

    if runtime == "codex":
        adapter_root = source_root / ".codex"
        if not adapter_root.is_dir():
            raise FileNotFoundError(f"Missing source Codex adapter directory: {adapter_root}")
        return

    adapter_root = source_root / ".github"
    if not adapter_root.is_dir():
        raise FileNotFoundError(f"Missing source Copilot adapter directory: {adapter_root}")


def remove_destination(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def is_same_or_child(path: Path, parent: Path) -> bool:
    try:
        common = os.path.commonpath([str(path.resolve()), str(parent.resolve())])
    except ValueError:
        return False
    return os.path.normcase(common) == os.path.normcase(str(parent.resolve()))


def copy_path(src: Path, dest: Path, force: bool, dry_run: bool, result: InstallResult) -> None:
    if dest.exists():
        if not force:
            result.skipped.append(dest)
            return
        if dry_run:
            result.installed.append(dest)
            return
        remove_destination(dest)

    result.installed.append(dest)
    if dry_run:
        return

    dest.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)


def install_skills(source_root: Path, target_root: Path, args: argparse.Namespace, result: InstallResult) -> None:
    source_skills = source_root / "skills"
    if args.runtime == "codex" and args.global_skills:
        dest_skills = Path.home() / ".codex" / "skills"
    elif args.runtime == "codex":
        dest_skills = target_root / ".codex" / "skills"
    else:
        dest_skills = target_root / ".github" / "skills"

    for skill_dir in sorted(path for path in source_skills.iterdir() if path.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            raise FileNotFoundError(f"Skill directory is missing SKILL.md: {skill_dir}")
        copy_path(skill_dir, dest_skills / skill_dir.name, args.force, args.dry_run, result)


def install_codex_adapter(source_root: Path, target_root: Path, args: argparse.Namespace, result: InstallResult) -> None:
    source_adapter = source_root / ".codex"
    dest_project_adapter = target_root / ".codex"
    dest_user_agents = Path.home() / ".codex" / "agents"

    source_agents = source_adapter / "agents"
    if not source_agents.is_dir():
        raise FileNotFoundError(f"Missing source adapter entry: {source_agents}")

    for child in sorted(source_agents.iterdir()):
        copy_path(child, dest_user_agents / child.name, args.force, args.dry_run, result)

    for entry_name in CODEX_PROJECT_ADAPTER_ENTRIES:
        source_entry = source_adapter / entry_name
        if not source_entry.exists():
            raise FileNotFoundError(f"Missing source adapter entry: {source_entry}")
        copy_path(source_entry, dest_project_adapter / entry_name, args.force, args.dry_run, result)


def install_copilot_adapter(source_root: Path, target_root: Path, args: argparse.Namespace, result: InstallResult) -> None:
    source_adapter = source_root / ".github"
    dest_adapter = target_root / ".github"

    source_agents = source_adapter / "agents"
    if not source_agents.is_dir():
        raise FileNotFoundError(f"Missing source Copilot adapter entry: {source_agents}")

    for child in sorted(source_agents.iterdir()):
        copy_path(child, dest_adapter / "agents" / child.name, args.force, args.dry_run, result)

    source_workflow_config = source_adapter / "ai-workflows"
    if not source_workflow_config.is_dir():
        raise FileNotFoundError(f"Missing source Copilot adapter entry: {source_workflow_config}")

    for entry_name in COPILOT_PROJECT_ADAPTER_ENTRIES:
        source_entry = source_workflow_config / entry_name
        if not source_entry.exists():
            raise FileNotFoundError(f"Missing source Copilot adapter entry: {source_entry}")
        copy_path(source_entry, dest_adapter / "ai-workflows" / entry_name, args.force, args.dry_run, result)

    instructions = source_adapter / "copilot-instructions.md"
    if instructions.exists():
        copy_path(instructions, dest_adapter / instructions.name, args.force, args.dry_run, result)


def install_adapter(source_root: Path, target_root: Path, args: argparse.Namespace, result: InstallResult) -> None:
    if args.runtime == "codex":
        install_codex_adapter(source_root, target_root, args, result)
    else:
        install_copilot_adapter(source_root, target_root, args, result)


def print_summary(result: InstallResult, dry_run: bool) -> None:
    verb = "Would install" if dry_run else "Installed"
    skip_verb = "Would skip existing" if dry_run else "Skipped existing"

    print(f"{verb}: {len(result.installed)} item(s)")
    for path in result.installed:
        print(f"  + {path}")

    if result.skipped:
        print(f"{skip_verb}: {len(result.skipped)} item(s)")
        for path in result.skipped:
            print(f"  = {path}")
        print("Use --force to replace skipped managed files.")


def main() -> int:
    args = parse_args()
    source_root = Path(__file__).resolve().parent
    target_root = args.target.resolve()

    try:
        if args.no_skills and args.no_adapter:
            raise ValueError("Nothing to install: both --no-skills and --no-adapter were passed.")
        if args.runtime == "copilot" and args.global_skills:
            raise ValueError("--global-skills is only supported with --runtime codex.")

        ensure_source_layout(source_root, args.runtime, not args.no_skills, not args.no_adapter)
        if not target_root.is_dir():
            raise FileNotFoundError(f"Target repository root does not exist: {target_root}")

        writes_target_skills = not args.no_skills and not args.global_skills
        writes_target_adapter = not args.no_adapter
        writes_to_source_repo = is_same_or_child(target_root, source_root) and (
            writes_target_skills or writes_target_adapter
        )
        if writes_to_source_repo and not args.dry_run:
            raise ValueError(
                "Target is the ai-workflows source repo or one of its subdirectories. Run this from a target repo, "
                "pass --target, or use --dry-run to inspect planned changes."
            )

        result = InstallResult(installed=[], skipped=[])
        if not args.no_skills:
            install_skills(source_root, target_root, args, result)
        if not args.no_adapter:
            install_adapter(source_root, target_root, args, result)

        print_summary(result, args.dry_run)
        return 0
    except Exception as exc:
        print(f"install.py: error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
