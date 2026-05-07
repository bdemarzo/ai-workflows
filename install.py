#!/usr/bin/env python3
"""Install ai-workflows skills and a selected runtime adapter into another repository."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, List


CODEX_PROJECT_ADAPTER_ENTRIES = ("role-registry.toml", "config.toml")
COPILOT_PROJECT_ADAPTER_ENTRIES = ("role-registry.toml", "config.toml")
CODEX_ADAPTER_ROOT = Path("adapters") / "codex"
COPILOT_ADAPTER_ROOT = Path("adapters") / "copilot"
LIBRARY_NAME = "ai-workflows"
MANIFEST_SCHEMA_VERSION = 1
MANAGED_HEADER = "Managed by ai-workflows. Source files live in the ai-workflows library."


@dataclass
class InstallResult:
    installed: List[Path]
    skipped: List[Path]
    removed: List[Path]


@dataclass
class ManifestEntry:
    kind: str
    source: str | None
    path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Install ai-workflows skills and the selected runtime adapter into "
            "a target repository or user profile."
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
        "--scope",
        choices=("project", "user"),
        default="project",
        help="Install into the target repository or the current user's profile. Defaults to project.",
    )
    parser.add_argument(
        "--legacy-codex-skills",
        action="store_true",
        help="For --runtime codex only: use the legacy .codex/skills destination for the selected scope.",
    )
    parser.add_argument(
        "--namespace",
        default=LIBRARY_NAME,
        help=(
            "Prefix deployed skills and agents with this namespace. Defaults to 'ai-workflows'. "
            "Use --legacy-names to preserve the old flat deployed names."
        ),
    )
    parser.add_argument(
        "--legacy-names",
        action="store_true",
        help="Deploy skills and agents with their historical flat names instead of namespace-prefixed names.",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Remove files recorded in the ai-workflows manifest for the selected runtime and scope.",
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
        adapter_root = source_root / CODEX_ADAPTER_ROOT
        if not adapter_root.is_dir():
            raise FileNotFoundError(f"Missing source Codex adapter directory: {adapter_root}")
        return

    adapter_root = source_root / COPILOT_ADAPTER_ROOT
    if not adapter_root.is_dir():
        raise FileNotFoundError(f"Missing source Copilot adapter directory: {adapter_root}")


def validate_namespace(namespace: str) -> str:
    namespace = namespace.strip()
    if not namespace:
        raise ValueError("--namespace must not be empty unless --legacy-names is used.")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", namespace):
        raise ValueError("--namespace may contain only letters, numbers, hyphens, and underscores.")
    return namespace


def deployed_skill_name(skill_name: str, args: argparse.Namespace) -> str:
    if args.legacy_names:
        return skill_name
    return f"{args.namespace}-{skill_name}"


def deployed_agent_file_name(filename: str, args: argparse.Namespace) -> str:
    if args.legacy_names:
        return filename
    return f"{args.namespace}-{filename}"


def deployed_agent_id(agent_id: str, runtime: str, args: argparse.Namespace) -> str:
    if args.legacy_names:
        return agent_id
    if runtime == "codex":
        return f"{args.namespace.replace('-', '_')}_{agent_id}"
    return f"{args.namespace}-{agent_id}"


def scope_root_for(runtime: str, target_root: Path, args: argparse.Namespace) -> Path:
    if runtime == "codex":
        return Path.home() if args.scope == "user" else target_root
    return copilot_scope_root(target_root, args)


def manifest_path_for(runtime: str, target_root: Path, args: argparse.Namespace) -> Path:
    scope_root = scope_root_for(runtime, target_root, args)
    if runtime == "codex":
        return scope_root / ".codex" / LIBRARY_NAME / "manifest.json"
    return scope_root / ".github" / LIBRARY_NAME / "manifest.json"


def relative_to_scope(path: Path, scope_root: Path) -> str:
    try:
        return path.resolve().relative_to(scope_root.resolve()).as_posix()
    except ValueError:
        return str(path)


def manifest_entry_to_dict(entry: ManifestEntry, scope_root: Path) -> dict[str, str | None]:
    return {
        "kind": entry.kind,
        "source": entry.source,
        "path": relative_to_scope(entry.path, scope_root),
    }


def load_manifest(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(data, dict) or data.get("library") != LIBRARY_NAME:
        return None
    return data


def manifest_managed_paths(manifest: dict | None, scope_root: Path) -> set[Path]:
    if not manifest:
        return set()
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        return set()

    paths: set[Path] = set()
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            continue
        path = Path(entry["path"])
        if not path.is_absolute():
            path = scope_root / path
        paths.add(path.resolve())
    return paths


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


def copy_path(
    src: Path,
    dest: Path,
    force: bool,
    dry_run: bool,
    result: InstallResult,
    previous_managed_paths: set[Path] | None = None,
    transform: Callable[[str], str] | None = None,
) -> bool:
    previous_managed_paths = previous_managed_paths or set()
    if dest.exists():
        if not force and dest.resolve() not in previous_managed_paths:
            result.skipped.append(dest)
            return False
        if dry_run:
            result.installed.append(dest)
            return True
        remove_destination(dest)

    result.installed.append(dest)
    if dry_run:
        return True

    dest.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dest)
    else:
        if transform:
            dest.write_text(transform(src.read_text(encoding="utf-8")), encoding="utf-8")
        else:
            shutil.copy2(src, dest)
    return True


def prepend_once(text: str, header: str, comment_prefix: str) -> str:
    marker = f"{comment_prefix} {header}"
    if marker in text:
        return text
    return f"{marker}\n{text}"


def transform_skill_text(text: str, source_name: str, dest_name: str) -> str:
    text = re.sub(
        rf"^name:\s*{re.escape(source_name)}\s*$",
        f"name: {dest_name}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    return prepend_markdown_marker(text)


def prepend_markdown_marker(text: str) -> str:
    marker = f"<!-- {MANAGED_HEADER} -->"
    if marker in text:
        return text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            insert_at = end + len("\n---")
            return f"{text[:insert_at]}\n\n{marker}{text[insert_at:]}"
    return f"{marker}\n{text}"


def transform_codex_agent_text(text: str, source_id: str, dest_id: str) -> str:
    text = re.sub(
        rf'^name\s*=\s*"{re.escape(source_id)}"\s*$',
        f'name = "{dest_id}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    return prepend_once(text, MANAGED_HEADER, "#")


def transform_copilot_agent_text(text: str, source_id: str, dest_id: str) -> str:
    text = re.sub(
        rf"^name:\s*{re.escape(source_id)}\s*$",
        f"name: {dest_id}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    return prepend_markdown_marker(text)


def transform_role_registry_text(text: str, runtime: str, args: argparse.Namespace) -> str:
    def replace_agent(match: re.Match[str]) -> str:
        return f'agent = "{deployed_agent_id(match.group(1), runtime, args)}"'

    def replace_agent_list(match: re.Match[str]) -> str:
        values = [value.strip().strip('"') for value in match.group(1).split(",") if value.strip()]
        deployed = [f'"{deployed_agent_id(value, runtime, args)}"' for value in values]
        return f"allowed_substitution_agents = [{', '.join(deployed)}]"

    text = re.sub(r'^agent\s*=\s*"([^"]+)"\s*$', replace_agent, text, flags=re.MULTILINE)
    text = re.sub(
        r"^allowed_substitution_agents\s*=\s*\[(.*?)\]\s*$",
        replace_agent_list,
        text,
        flags=re.MULTILINE,
    )
    return prepend_once(text, MANAGED_HEADER, "#")


def copy_codex_skill_metadata(
    source_root: Path,
    skill_name: str,
    dest_skill_dir: Path,
    args: argparse.Namespace,
    result: InstallResult,
    previous_managed_paths: set[Path],
    manifest_entries: list[ManifestEntry],
) -> None:
    metadata_dir = source_root / CODEX_ADAPTER_ROOT / "skill-metadata" / skill_name
    if not metadata_dir.is_dir():
        return

    for child in sorted(metadata_dir.iterdir()):
        dest = dest_skill_dir / child.name
        if copy_path(child, dest, True, args.dry_run, result, previous_managed_paths):
            manifest_entries.append(ManifestEntry("skill-metadata", str(child.relative_to(source_root)), dest))


def codex_skills_dest(target_root: Path, args: argparse.Namespace) -> Path:
    scope_root = Path.home() if args.scope == "user" else target_root
    if args.legacy_codex_skills:
        return scope_root / ".codex" / "skills"
    return scope_root / ".agents" / "skills"


def copilot_scope_root(target_root: Path, args: argparse.Namespace) -> Path:
    return Path.home() if args.scope == "user" else target_root


def install_skills(
    source_root: Path,
    target_root: Path,
    args: argparse.Namespace,
    result: InstallResult,
    previous_managed_paths: set[Path],
    manifest_entries: list[ManifestEntry],
) -> None:
    source_skills = source_root / "skills"
    if args.runtime == "codex":
        dest_skills = codex_skills_dest(target_root, args)
    else:
        dest_skills = copilot_scope_root(target_root, args) / ".github" / "skills"

    for skill_dir in sorted(path for path in source_skills.iterdir() if path.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            raise FileNotFoundError(f"Skill directory is missing SKILL.md: {skill_dir}")
        dest_skill_name = deployed_skill_name(skill_dir.name, args)
        dest_skill_dir = dest_skills / dest_skill_name
        installed_skill = copy_path(skill_dir, dest_skill_dir, args.force, args.dry_run, result, previous_managed_paths)
        if installed_skill:
            manifest_entries.append(ManifestEntry("skill", str(skill_dir.relative_to(source_root)), dest_skill_dir))
            if not args.dry_run:
                deployed_skill_file = dest_skill_dir / "SKILL.md"
                deployed_skill_file.write_text(
                    transform_skill_text(deployed_skill_file.read_text(encoding="utf-8"), skill_dir.name, dest_skill_name),
                    encoding="utf-8",
                )
        if installed_skill and args.runtime == "codex":
            copy_codex_skill_metadata(
                source_root,
                skill_dir.name,
                dest_skill_dir,
                args,
                result,
                previous_managed_paths,
                manifest_entries,
            )


def install_codex_adapter(
    source_root: Path,
    target_root: Path,
    args: argparse.Namespace,
    result: InstallResult,
    previous_managed_paths: set[Path],
    manifest_entries: list[ManifestEntry],
) -> None:
    source_adapter = source_root / CODEX_ADAPTER_ROOT
    dest_adapter = (Path.home() if args.scope == "user" else target_root) / ".codex"
    dest_library = dest_adapter / LIBRARY_NAME

    source_agents = source_adapter / "agents"
    if not source_agents.is_dir():
        raise FileNotFoundError(f"Missing source adapter entry: {source_agents}")

    for child in sorted(source_agents.iterdir()):
        source_id = child.stem.replace("-", "_")
        dest = dest_adapter / "agents" / deployed_agent_file_name(child.name, args)
        dest_id = deployed_agent_id(source_id, "codex", args)
        if copy_path(
            child,
            dest,
            args.force,
            args.dry_run,
            result,
            previous_managed_paths,
            transform=lambda text, source_id=source_id, dest_id=dest_id: transform_codex_agent_text(text, source_id, dest_id),
        ):
            manifest_entries.append(ManifestEntry("agent", str(child.relative_to(source_root)), dest))

    for entry_name in CODEX_PROJECT_ADAPTER_ENTRIES:
        source_entry = source_adapter / entry_name
        if not source_entry.exists():
            raise FileNotFoundError(f"Missing source adapter entry: {source_entry}")
        dest = dest_library / entry_name
        transform: Callable[[str], str] | None = None
        kind = "config"
        if entry_name == "role-registry.toml":
            transform = lambda text: transform_role_registry_text(text, "codex", args)
            kind = "role-registry"
        elif entry_name.endswith(".toml"):
            transform = lambda text: prepend_once(text, MANAGED_HEADER, "#")
        if copy_path(source_entry, dest, args.force, args.dry_run, result, previous_managed_paths, transform=transform):
            manifest_entries.append(ManifestEntry(kind, str(source_entry.relative_to(source_root)), dest))


def install_copilot_adapter(
    source_root: Path,
    target_root: Path,
    args: argparse.Namespace,
    result: InstallResult,
    previous_managed_paths: set[Path],
    manifest_entries: list[ManifestEntry],
) -> None:
    source_adapter = source_root / COPILOT_ADAPTER_ROOT
    dest_adapter = copilot_scope_root(target_root, args) / ".github"

    source_agents = source_adapter / "agents"
    if not source_agents.is_dir():
        raise FileNotFoundError(f"Missing source Copilot adapter entry: {source_agents}")

    for child in sorted(source_agents.iterdir()):
        source_id = child.name.removesuffix(".agent.md")
        dest = dest_adapter / "agents" / deployed_agent_file_name(child.name, args)
        dest_id = deployed_agent_id(source_id, "copilot", args)
        if copy_path(
            child,
            dest,
            args.force,
            args.dry_run,
            result,
            previous_managed_paths,
            transform=lambda text, source_id=source_id, dest_id=dest_id: transform_copilot_agent_text(text, source_id, dest_id),
        ):
            manifest_entries.append(ManifestEntry("agent", str(child.relative_to(source_root)), dest))

    for entry_name in COPILOT_PROJECT_ADAPTER_ENTRIES:
        source_entry = source_adapter / entry_name
        if not source_entry.exists():
            raise FileNotFoundError(f"Missing source Copilot adapter entry: {source_entry}")
        dest = dest_adapter / LIBRARY_NAME / entry_name
        transform: Callable[[str], str] | None = None
        kind = "config"
        if entry_name == "role-registry.toml":
            transform = lambda text: transform_role_registry_text(text, "copilot", args)
            kind = "role-registry"
        elif entry_name.endswith(".toml"):
            transform = lambda text: prepend_once(text, MANAGED_HEADER, "#")
        if copy_path(source_entry, dest, args.force, args.dry_run, result, previous_managed_paths, transform=transform):
            manifest_entries.append(ManifestEntry(kind, str(source_entry.relative_to(source_root)), dest))

    instructions = source_adapter / "copilot-instructions.md"
    if instructions.exists():
        dest = dest_adapter / instructions.name if args.legacy_names else dest_adapter / LIBRARY_NAME / instructions.name
        if copy_path(
            instructions,
            dest,
            args.force,
            args.dry_run,
            result,
            previous_managed_paths,
            transform=prepend_markdown_marker,
        ):
            manifest_entries.append(ManifestEntry("instructions", str(instructions.relative_to(source_root)), dest))


def install_adapter(
    source_root: Path,
    target_root: Path,
    args: argparse.Namespace,
    result: InstallResult,
    previous_managed_paths: set[Path],
    manifest_entries: list[ManifestEntry],
) -> None:
    if args.runtime == "codex":
        install_codex_adapter(source_root, target_root, args, result, previous_managed_paths, manifest_entries)
    else:
        install_copilot_adapter(source_root, target_root, args, result, previous_managed_paths, manifest_entries)


def write_manifest(
    manifest_path: Path,
    source_root: Path,
    target_root: Path,
    args: argparse.Namespace,
    manifest_entries: list[ManifestEntry],
) -> None:
    scope_root = scope_root_for(args.runtime, target_root, args)
    manifest = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "library": LIBRARY_NAME,
        "runtime": args.runtime,
        "scope": args.scope,
        "namespace": None if args.legacy_names else args.namespace,
        "legacy_names": bool(args.legacy_names),
        "installed_at": datetime.now(timezone.utc).isoformat(),
        "source_root": str(source_root),
        "entries": [
            manifest_entry_to_dict(entry, scope_root)
            for entry in sorted(manifest_entries, key=lambda item: str(item.path))
        ],
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def remove_empty_parents(path: Path, stop_at: Path) -> None:
    current = path.parent
    stop_at = stop_at.resolve()
    while current.exists() and current.resolve() != stop_at:
        try:
            current.rmdir()
        except OSError:
            return
        current = current.parent


def uninstall_from_manifest(manifest_path: Path, target_root: Path, args: argparse.Namespace, result: InstallResult) -> None:
    manifest = load_manifest(manifest_path)
    if manifest is None:
        raise FileNotFoundError(f"No ai-workflows manifest found: {manifest_path}")

    scope_root = scope_root_for(args.runtime, target_root, args)
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        raise ValueError(f"Invalid manifest entries in: {manifest_path}")

    for entry in sorted(entries, key=lambda item: str(item.get("path", "")), reverse=True):
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            continue
        path = Path(entry["path"])
        if not path.is_absolute():
            path = scope_root / path
        if not is_same_or_child(path, scope_root):
            raise ValueError(f"Refusing to uninstall path outside selected scope: {path}")
        if not path.exists():
            continue
        if not args.dry_run:
            remove_destination(path)
            remove_empty_parents(path, scope_root)
        result.removed.append(path)

    if manifest_path.exists():
        if not args.dry_run:
            manifest_path.unlink()
            remove_empty_parents(manifest_path, scope_root)
        result.removed.append(manifest_path)


def print_summary(result: InstallResult, dry_run: bool) -> None:
    verb = "Would install" if dry_run else "Installed"
    skip_verb = "Would skip existing" if dry_run else "Skipped existing"
    remove_verb = "Would remove" if dry_run else "Removed"

    print(f"{verb}: {len(result.installed)} item(s)")
    for path in result.installed:
        print(f"  + {path}")

    if result.removed:
        print(f"{remove_verb}: {len(result.removed)} item(s)")
        for path in result.removed:
            print(f"  - {path}")

    if result.skipped:
        print(f"{skip_verb}: {len(result.skipped)} item(s)")
        for path in result.skipped:
            print(f"  = {path}")
        print("Use --force to replace skipped unmanaged files.")


def main() -> int:
    args = parse_args()
    source_root = Path(__file__).resolve().parent
    target_root = args.target.resolve()

    try:
        if not args.legacy_names:
            args.namespace = validate_namespace(args.namespace)
        if args.no_skills and args.no_adapter:
            raise ValueError("Nothing to install: both --no-skills and --no-adapter were passed.")
        if args.runtime == "copilot" and args.legacy_codex_skills:
            raise ValueError("--legacy-codex-skills is only supported with --runtime codex.")

        if args.uninstall and (args.no_skills or args.no_adapter):
            raise ValueError("--uninstall removes the manifest-managed deployment; do not combine it with --no-skills or --no-adapter.")

        if not args.uninstall:
            ensure_source_layout(source_root, args.runtime, not args.no_skills, not args.no_adapter)
        if args.scope == "project" and not target_root.is_dir():
            raise FileNotFoundError(f"Target repository root does not exist: {target_root}")

        writes_target_skills = args.scope == "project" and not args.no_skills
        writes_target_adapter = args.scope == "project" and not args.no_adapter
        writes_target_manifest = args.scope == "project"
        writes_to_source_repo = is_same_or_child(target_root, source_root) and (
            writes_target_skills or writes_target_adapter or writes_target_manifest
        )
        if writes_to_source_repo and not args.dry_run:
            raise ValueError(
                "Target is the ai-workflows source repo or one of its subdirectories. Run this from a target repo, "
                "pass --target, use --scope user, or use --dry-run to inspect planned changes."
            )

        result = InstallResult(installed=[], skipped=[], removed=[])
        manifest_path = manifest_path_for(args.runtime, target_root, args)

        if args.uninstall:
            uninstall_from_manifest(manifest_path, target_root, args, result)
            print_summary(result, args.dry_run)
            return 0

        scope_root = scope_root_for(args.runtime, target_root, args)
        previous_manifest = load_manifest(manifest_path)
        previous_managed_paths = manifest_managed_paths(previous_manifest, scope_root)
        manifest_entries: list[ManifestEntry] = []

        if not args.no_skills:
            install_skills(source_root, target_root, args, result, previous_managed_paths, manifest_entries)
        if not args.no_adapter:
            install_adapter(source_root, target_root, args, result, previous_managed_paths, manifest_entries)

        if not args.dry_run:
            write_manifest(manifest_path, source_root, target_root, args, manifest_entries)
        result.installed.append(manifest_path)

        print_summary(result, args.dry_run)
        return 0
    except Exception as exc:
        print(f"install.py: error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
