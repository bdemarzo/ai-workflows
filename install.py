#!/usr/bin/env python3
"""Install ai-workflows skills and Codex adapter into another repository."""

from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List


ADAPTER_ENTRIES = ("agents", "role-registry.toml", "config.toml")


@dataclass
class InstallResult:
    installed: List[Path]
    skipped: List[Path]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Install ai-workflows skills and the optional Codex adapter into "
            "the current repository."
        )
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
        help="Do not install the project-scoped .codex adapter layer.",
    )
    parser.add_argument(
        "--global-skills",
        action="store_true",
        help="Install skills to ~/.codex/skills instead of the target repo's .codex/skills.",
    )
    return parser.parse_args()


def ensure_source_layout(source_root: Path) -> None:
    skills_root = source_root / "skills"
    adapter_root = source_root / ".codex"
    if not skills_root.is_dir():
        raise FileNotFoundError(f"Missing source skills directory: {skills_root}")
    if not adapter_root.is_dir():
        raise FileNotFoundError(f"Missing source adapter directory: {adapter_root}")


def remove_destination(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


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
    if args.global_skills:
        dest_skills = Path.home() / ".codex" / "skills"
    else:
        dest_skills = target_root / ".codex" / "skills"

    for skill_dir in sorted(path for path in source_skills.iterdir() if path.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            raise FileNotFoundError(f"Skill directory is missing SKILL.md: {skill_dir}")
        copy_path(skill_dir, dest_skills / skill_dir.name, args.force, args.dry_run, result)


def install_adapter(source_root: Path, target_root: Path, args: argparse.Namespace, result: InstallResult) -> None:
    source_adapter = source_root / ".codex"
    dest_adapter = target_root / ".codex"

    for entry_name in ADAPTER_ENTRIES:
        source_entry = source_adapter / entry_name
        if not source_entry.exists():
            raise FileNotFoundError(f"Missing source adapter entry: {source_entry}")

        if source_entry.is_dir():
            for child in sorted(source_entry.iterdir()):
                copy_path(child, dest_adapter / entry_name / child.name, args.force, args.dry_run, result)
        else:
            copy_path(source_entry, dest_adapter / entry_name, args.force, args.dry_run, result)


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
        ensure_source_layout(source_root)
        if not target_root.is_dir():
            raise FileNotFoundError(f"Target repository root does not exist: {target_root}")

        writes_target_skills = not args.no_skills and not args.global_skills
        writes_target_adapter = not args.no_adapter
        writes_to_source_repo = target_root == source_root and (writes_target_skills or writes_target_adapter)
        if writes_to_source_repo and not args.dry_run:
            raise ValueError(
                "Target is the ai-workflows source repo. Run this from a target repo, "
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
