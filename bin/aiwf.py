#!/usr/bin/env python3
"""aiwf: minimal workflow run controller for ai-workflows artifacts.

This helper intentionally manages workflow dossier state only.
Artifact generation remains the responsibility of skill execution in Codex.
"""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
import sys
import textwrap
from typing import Dict, Iterable, Tuple

QUESTION_MODE_ALIASES = {
    "fully automated": {"fully automated", "fully-automated"},
    "blocking questions only": {
        "blocking questions only",
        "blocking-questions-only",
        "blocking",
    },
    "ask many questions": {
        "ask many questions",
        "ask-many-questions",
        "ask-many",
    },
}

STAGE_GATE_MODE_ALIASES = {
    "none": {"none"},
    "loop boundaries": {"loop boundaries", "loop-boundaries"},
}

EXECUTION_PLAN_MODE_CHOICES = {"auto", "standard", "execplan"}

STAGE_SEQUENCE = [
    "idea-create",
    "idea-review",
    "spec-create",
    "spec-review",
    "plan-create",
    "plan-review",
    "implement-plan",
    "final-review",
]

GATE_TRANSITIONS = {
    "idea-to-spec": {
        "from": "idea-review",
        "to": "spec-create",
        "revise": "idea-create",
    },
    "spec-to-plan": {
        "from": "spec-review",
        "to": "plan-create",
        "revise": "spec-create",
    },
    "plan-to-implement": {
        "from": "plan-review",
        "to": "implement-plan",
        "revise": "plan-create",
    },
    "implement-to-final": {
        "from": "implement-plan",
        "to": "final-review",
        "revise": "implement-plan",
    },
}


def _utc_now() -> str:
    return dt.datetime.now(tz=dt.timezone.utc).replace(microsecond=0).isoformat()


def _resolve_repo(repo: str | None) -> Path:
    base = Path(repo).expanduser().resolve() if repo else Path.cwd().resolve()
    if not base.exists() or not base.is_dir():
        raise SystemExit(f"Repository path does not exist or is not a directory: {base}")
    return base


def _normalize_choice(raw: str, aliases: Dict[str, Iterable[str]], kind: str) -> str:
    value = raw.strip().lower()
    for canonical, accepted in aliases.items():
        if value in {alias.lower() for alias in accepted}:
            return canonical
    raise SystemExit(f"Unsupported {kind}: {raw}")


def _infer_execution_plan_mode(repo: Path) -> str:
    if (repo / "PLANS.md").exists():
        return "execplan"

    agents = repo / "AGENTS.md"
    if not agents.exists():
        return "standard"

    content = agents.read_text(encoding="utf-8").lower()
    if "plans.md" in content and (
        "planning and implementation must use" in content
        or "must use `plans.md`" in content
        or "must use plans.md" in content
    ):
        return "execplan"
    return "standard"


def _workflow_dir(repo: Path, slug: str) -> Path:
    return repo / "docs" / "workflows" / slug


def _run_path(repo: Path, slug: str) -> Path:
    return _workflow_dir(repo, slug) / "run.md"


def _pending_transition_for_gate(gate: str) -> str:
    transition = GATE_TRANSITIONS[gate]
    return f"{transition['from']} -> {transition['to']}"


def _gate_for_pending_transition(pending_transition: str) -> str | None:
    for gate in GATE_TRANSITIONS:
        if pending_transition == _pending_transition_for_gate(gate):
            return gate
    return None


def _artifact_map(slug: str) -> Dict[str, str]:
    base = f"docs/workflows/{slug}"
    return {
        "dossier": f"{base}/",
        "run": f"{base}/run.md",
        "idea": f"{base}/idea.md",
        "idea_review": f"{base}/reviews/idea/round-01.md",
        "spec": f"{base}/spec.md",
        "spec_review": f"{base}/reviews/spec/round-01.md",
        "plan": f"{base}/plan.md",
        "plan_review": f"{base}/reviews/plan/round-01.md",
        "execution": f"{base}/execution.md",
        "final_review": f"{base}/reviews/final/round-01.md",
    }


def _next_stage(current_stage: str) -> str | None:
    try:
        index = STAGE_SEQUENCE.index(current_stage)
    except ValueError:
        return None
    if index + 1 >= len(STAGE_SEQUENCE):
        return None
    return STAGE_SEQUENCE[index + 1]


def _header_lines(fields: Dict[str, str]) -> list[str]:
    ordered_keys = [
        "question_mode",
        "stage_gate_mode",
        "execution_plan_mode",
        "canonical_slug",
        "current_stage",
        "workflow_status",
        "pending_transition",
        "repo_root",
        "last_transition_at",
    ]
    lines: list[str] = []
    for key in ordered_keys:
        value = fields.get(key)
        if value:
            lines.append(f"{key}: {value}")
    lines.append("")
    return lines


def _read_ledger(path: Path) -> Tuple[Dict[str, str], str]:
    fields: Dict[str, str] = {}
    body_lines: list[str] = []
    in_header = True

    for line in path.read_text(encoding="utf-8").splitlines():
        if in_header and line.strip():
            if ":" in line:
                key, val = line.split(":", 1)
                fields[key.strip()] = val.strip()
                continue
        if in_header:
            in_header = False
            if not line.strip():
                continue
        body_lines.append(line)

    body = ""
    if body_lines:
        body = "\n".join(body_lines).rstrip() + "\n"
    return fields, body


def _write_ledger(path: Path, fields: Dict[str, str], body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized_body = body if body.endswith("\n") else f"{body}\n"
    path.write_text("\n".join(_header_lines(fields)) + normalized_body, encoding="utf-8")


def _replace_section(body: str, heading: str, new_lines: list[str]) -> str:
    lines = body.rstrip("\n").splitlines()
    if not lines:
        lines = []

    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == heading)
    except StopIteration:
        if lines:
            lines.append("")
        lines.append(heading)
        lines.extend(new_lines)
        return "\n".join(lines) + "\n"

    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break

    updated = lines[: start + 1] + new_lines + lines[end:]
    return "\n".join(updated) + "\n"


def _append_section_bullet(body: str, heading: str, bullet: str) -> str:
    lines = body.rstrip("\n").splitlines()
    if not lines:
        lines = []

    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == heading)
    except StopIteration:
        if lines:
            lines.append("")
        lines.append(heading)
        lines.append(bullet)
        return "\n".join(lines) + "\n"

    insert_at = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            insert_at = i
            break

    updated = lines[:insert_at] + [bullet] + lines[insert_at:]
    return "\n".join(updated) + "\n"


def _resume_instruction(stage: str, slug: str, gate: str | None = None) -> list[str]:
    dossier = f"docs/workflows/{slug}"
    if stage == "idea-create":
        return [
            f"- Next: run `idea-create` against `{dossier}/idea.md`, then `idea-review`.",
        ]
    if stage == "idea-review":
        return [
            f"- Next: run `idea-review` against `{dossier}/idea.md`. If approval is required afterward, use `aiwf run pause --gate idea-to-spec`.",
        ]
    if stage == "spec-create":
        return [
            f"- Next: run `spec-create` against `{dossier}/spec.md`, then `spec-review`.",
        ]
    if stage == "spec-review":
        return [
            f"- Next: run `spec-review` against `{dossier}/spec.md`. If approval is required afterward, use `aiwf run pause --gate spec-to-plan`.",
        ]
    if stage == "plan-create":
        return [
            f"- Next: run `plan-create` against `{dossier}/plan.md`, then `plan-review`.",
        ]
    if stage == "plan-review":
        return [
            f"- Next: run `plan-review` against `{dossier}/plan.md`. If approval is required afterward, use `aiwf run pause --gate plan-to-implement`.",
        ]
    if stage == "implement-plan":
        return [
            f"- Next: run `implement-plan` from `{dossier}/plan.md` and keep `{dossier}/plan.md` current during execution. If approval is required afterward, use `aiwf run pause --gate implement-to-final`.",
        ]
    if stage == "final-review":
        return [
            f"- Next: run `final-review` using the artifact chain under `{dossier}/`.",
        ]
    if gate:
        return [
            f"- Review the current dossier under `{dossier}/` and decide whether to `approve` or `revise current stage` for `{gate}`.",
        ]
    return ["- Next action: inspect the run ledger and continue from the current stage."]


def _build_initial_body(
    slug: str,
    prompt: str,
    question_mode: str,
    stage_gate_mode: str,
    execution_plan_mode: str,
    created_at: str,
    notes: str | None,
) -> str:
    artifacts = _artifact_map(slug)
    notes_line = f"- Startup note: {notes}" if notes else "- Startup note: none"
    return textwrap.dedent(
        f"""\
        # Purpose / Big Picture
        - Original prompt: {prompt}
        - Success depends on keeping the workflow dossier under `{artifacts["dossier"]}` aligned with the stage skills.

        ## Artifact Map
        - Dossier: `{artifacts["dossier"]}`
        - Run ledger: `{artifacts["run"]}`
        - Idea: `{artifacts["idea"]}`
        - Latest idea review: `{artifacts["idea_review"]}` once created
        - Spec: `{artifacts["spec"]}`
        - Latest spec review: `{artifacts["spec_review"]}` once created
        - Plan: `{artifacts["plan"]}`
        - Latest plan review: `{artifacts["plan_review"]}` once created
        - Execution evidence: `{artifacts["execution"]}` when needed
        - Latest final review: `{artifacts["final_review"]}` once created

        ## Progress
        - [x] Workflow started at {created_at}
        - [ ] idea-create
        - [ ] idea-review
        - [ ] spec-create
        - [ ] spec-review
        - [ ] plan-create
        - [ ] plan-review
        - [ ] implement-plan
        - [ ] final-review

        ## Stage Assessments
        - idea: pending
        - spec: pending
        - plan: pending
        - implementation: pending
        - final review: pending

        ## Questions and Assumptions
        - question_mode: {question_mode}
        - stage_gate_mode: {stage_gate_mode}
        - execution_plan_mode: {execution_plan_mode}
        {notes_line}

        ## Decision Log
        - {created_at}: Created the workflow dossier and initialized the run ledger.

        ## Surprises & Discoveries
        - None yet.

        ## Validation Evidence
        - `{created_at}`: `aiwf run start` initialized the dossier ledger without generating artifacts.

        ## Current Blockers
        - None.

        ## Resume Instructions
        - Next: run `idea-create` against `{artifacts["idea"]}`, then `idea-review`.

        ## Outcomes & Retrospective
        - Pending.
        """
    )


def _update_for_pause(
    body: str,
    slug: str,
    gate: str,
    timestamp: str,
    notes: str | None,
) -> str:
    pending = _pending_transition_for_gate(gate)
    updated = _append_section_bullet(
        body,
        "## Decision Log",
        f"- {timestamp}: Paused for stage approval at `{pending}`.",
    )
    if notes:
        updated = _append_section_bullet(
            updated,
            "## Decision Log",
            f"- {timestamp}: Approval note: {notes}",
        )
    updated = _append_section_bullet(
        updated,
        "## Progress",
        f"- [x] {timestamp}: paused for `{gate}` approval",
    )
    updated = _replace_section(
        updated,
        "## Current Blockers",
        [f"- Waiting on stage approval for `{pending}`."],
    )
    updated = _replace_section(
        updated,
        "## Resume Instructions",
        _resume_instruction(GATE_TRANSITIONS[gate]["from"], slug, gate=gate),
    )
    return updated


def _update_for_resume(
    body: str,
    slug: str,
    stage: str,
    timestamp: str,
    summary: str,
    notes: str | None,
) -> str:
    updated = _append_section_bullet(
        body,
        "## Decision Log",
        f"- {timestamp}: {summary}",
    )
    if notes:
        updated = _append_section_bullet(
            updated,
            "## Decision Log",
            f"- {timestamp}: Resume note: {notes}",
        )
    updated = _append_section_bullet(
        updated,
        "## Progress",
        f"- [x] {timestamp}: controller moved workflow to `{stage}`",
    )
    updated = _replace_section(updated, "## Current Blockers", ["- None."])
    updated = _replace_section(
        updated,
        "## Resume Instructions",
        _resume_instruction(stage, slug),
    )
    return updated


def cmd_start(args: argparse.Namespace) -> int:
    repo = _resolve_repo(args.repo)
    ledger = _run_path(repo, args.slug)
    if ledger.exists() and not args.force:
        raise SystemExit(f"Run ledger already exists: {ledger}. Use --force to overwrite.")

    question_mode = _normalize_choice(args.question_mode, QUESTION_MODE_ALIASES, "question mode")
    stage_gate_mode = _normalize_choice(
        args.stage_gate_mode,
        STAGE_GATE_MODE_ALIASES,
        "stage gate mode",
    )
    execution_plan_mode = (
        _infer_execution_plan_mode(repo)
        if args.execution_plan_mode == "auto"
        else args.execution_plan_mode
    )
    timestamp = _utc_now()

    fields = {
        "question_mode": question_mode,
        "stage_gate_mode": stage_gate_mode,
        "execution_plan_mode": execution_plan_mode,
        "canonical_slug": args.slug,
        "current_stage": STAGE_SEQUENCE[0],
        "workflow_status": "in-progress",
        "repo_root": str(repo),
        "last_transition_at": timestamp,
    }
    body = _build_initial_body(
        slug=args.slug,
        prompt=args.prompt,
        question_mode=question_mode,
        stage_gate_mode=stage_gate_mode,
        execution_plan_mode=execution_plan_mode,
        created_at=timestamp,
        notes=args.notes,
    )
    _write_ledger(ledger, fields, body)

    print(f"Resolved runtime repo: {repo}")
    print(f"Workflow dossier: {_workflow_dir(repo, args.slug)}")
    print(f"Run ledger: {ledger}")
    print(f"Question mode: {question_mode}")
    print(f"Stage gate mode: {stage_gate_mode}")
    print(f"Execution plan mode: {execution_plan_mode}")
    print(f"Current stage: {fields['current_stage']}")
    print("Next: run idea-create, then idea-review in Codex for this repository.")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    repo = _resolve_repo(args.repo)
    ledger = _run_path(repo, args.slug)
    if not ledger.exists():
        raise SystemExit(f"Run ledger does not exist: {ledger}")

    fields, _ = _read_ledger(ledger)
    print(f"Resolved runtime repo: {repo}")
    print(f"Workflow dossier: {_workflow_dir(repo, args.slug)}")
    print(f"Run ledger: {ledger}")
    print(f"Question mode: {fields.get('question_mode', 'unknown')}")
    print(f"Stage gate mode: {fields.get('stage_gate_mode', 'unknown')}")
    print(f"Execution plan mode: {fields.get('execution_plan_mode', 'unknown')}")
    print(f"Workflow status: {fields.get('workflow_status', 'unknown')}")
    print(f"Current stage: {fields.get('current_stage', 'unknown')}")
    if fields.get("pending_transition"):
        print(f"Pending transition: {fields['pending_transition']}")
    print(f"Last transition: {fields.get('last_transition_at', 'unknown')}")
    return 0


def cmd_pause(args: argparse.Namespace) -> int:
    repo = _resolve_repo(args.repo)
    ledger = _run_path(repo, args.slug)
    if not ledger.exists():
        raise SystemExit(f"Run ledger does not exist: {ledger}")

    fields, body = _read_ledger(ledger)
    transition = GATE_TRANSITIONS[args.gate]
    current_stage = fields.get("current_stage")
    expected_stage = transition["from"]
    if current_stage and current_stage != expected_stage:
        raise SystemExit(
            f"Cannot pause gate {args.gate} from stage {current_stage}. Expected {expected_stage}."
        )

    timestamp = _utc_now()
    fields["current_stage"] = expected_stage
    fields["workflow_status"] = "awaiting-stage-approval"
    fields["pending_transition"] = _pending_transition_for_gate(args.gate)
    fields["last_transition_at"] = timestamp
    body = _update_for_pause(body, args.slug, args.gate, timestamp, args.notes)
    _write_ledger(ledger, fields, body)

    print(f"Resolved runtime repo: {repo}")
    print(f"Run ledger: {ledger}")
    print(f"Paused at gate: {args.gate}")
    print(f"Pending transition: {fields['pending_transition']}")
    print("Decision needed: approve or revise current stage.")
    return 0


def cmd_advance(args: argparse.Namespace) -> int:
    repo = _resolve_repo(args.repo)
    ledger = _run_path(repo, args.slug)
    if not ledger.exists():
        raise SystemExit(f"Run ledger does not exist: {ledger}")

    fields, body = _read_ledger(ledger)
    if fields.get("pending_transition"):
        raise SystemExit("Run ledger is paused at a stage gate. Resume or revise it before advancing.")

    current_stage = fields.get("current_stage")
    if not current_stage:
        raise SystemExit("Run ledger is missing current_stage.")

    expected_next = _next_stage(current_stage)
    if args.to != expected_next:
        raise SystemExit(f"Cannot advance from {current_stage} to {args.to}. Expected {expected_next}.")

    timestamp = _utc_now()
    fields["current_stage"] = args.to
    fields["workflow_status"] = "in-progress"
    fields["last_transition_at"] = timestamp
    body = _update_for_resume(
        body,
        args.slug,
        args.to,
        timestamp,
        f"Advanced workflow from `{current_stage}` to `{args.to}`.",
        args.notes,
    )
    _write_ledger(ledger, fields, body)

    print(f"Resolved runtime repo: {repo}")
    print(f"Run ledger: {ledger}")
    print(f"Advanced from {current_stage} to {args.to}")
    print("Next: continue the workflow from the new current stage.")
    return 0


def cmd_resume(args: argparse.Namespace) -> int:
    repo = _resolve_repo(args.repo)
    ledger = _run_path(repo, args.slug)
    if not ledger.exists():
        raise SystemExit(f"Run ledger does not exist: {ledger}")

    fields, body = _read_ledger(ledger)
    pending_transition = fields.get("pending_transition")
    if not pending_transition:
        raise SystemExit("Run ledger is not paused at a stage gate.")

    gate = _gate_for_pending_transition(pending_transition)
    if gate is None:
        raise SystemExit(f"Unsupported pending transition in run ledger: {pending_transition}")

    if args.approve:
        if args.approve != gate:
            raise SystemExit(
                f"Approval gate {args.approve} does not match pending transition {pending_transition}."
            )
        next_stage = GATE_TRANSITIONS[gate]["to"]
        summary = f"Approved `{gate}` and advanced to `{next_stage}`."
    else:
        next_stage = GATE_TRANSITIONS[gate]["revise"]
        summary = f"Rejected `{gate}` advancement and routed back to `{next_stage}`."

    timestamp = _utc_now()
    fields["workflow_status"] = "in-progress"
    fields["current_stage"] = next_stage
    fields["last_transition_at"] = timestamp
    fields.pop("pending_transition", None)
    body = _update_for_resume(body, args.slug, next_stage, timestamp, summary, args.notes)
    _write_ledger(ledger, fields, body)

    print(f"Resolved runtime repo: {repo}")
    print(f"Run ledger: {ledger}")
    print(summary)
    print(f"New stage: {next_stage}")
    print("Next: execute the new stage in Codex and update artifacts in this repo.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aiwf", description="Minimal ai-workflows run controller")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run workflow commands")
    run_sub = run.add_subparsers(dest="run_command", required=True)

    start = run_sub.add_parser("start", help="Start a workflow run")
    start.add_argument("--repo", help="Target repository directory. Defaults to current working directory.")
    start.add_argument("--slug", required=True, help="Canonical workflow slug")
    start.add_argument(
        "--question-mode",
        required=True,
        help="Question mode token. Recommended values: fully-automated, blocking-questions-only, ask-many-questions.",
    )
    start.add_argument(
        "--stage-gate-mode",
        default="none",
        help="Stage gate mode token. Supported values: none, loop-boundaries.",
    )
    start.add_argument(
        "--execution-plan-mode",
        default="auto",
        choices=sorted(EXECUTION_PLAN_MODE_CHOICES),
        help="Use auto to infer standard vs execplan from the runtime repository.",
    )
    start.add_argument("--prompt", required=True, help="Original user prompt")
    start.add_argument("--notes", help="Optional startup notes")
    start.add_argument("--force", action="store_true", help="Overwrite existing run ledger")
    start.set_defaults(func=cmd_start)

    status = run_sub.add_parser("status", help="Show workflow run status")
    status.add_argument("--repo", help="Target repository directory. Defaults to current working directory.")
    status.add_argument("--slug", required=True, help="Canonical workflow slug")
    status.set_defaults(func=cmd_status)

    advance = run_sub.add_parser("advance", help="Advance to the next stage in the canonical sequence")
    advance.add_argument("--repo", help="Target repository directory. Defaults to current working directory.")
    advance.add_argument("--slug", required=True, help="Canonical workflow slug")
    advance.add_argument(
        "--to",
        required=True,
        choices=STAGE_SEQUENCE[1:],
        help="The next stage to enter.",
    )
    advance.add_argument("--notes", help="Optional transition notes")
    advance.set_defaults(func=cmd_advance)

    pause = run_sub.add_parser("pause", help="Pause at a supported stage gate")
    pause.add_argument("--repo", help="Target repository directory. Defaults to current working directory.")
    pause.add_argument("--slug", required=True, help="Canonical workflow slug")
    pause.add_argument(
        "--gate",
        required=True,
        choices=sorted(GATE_TRANSITIONS.keys()),
        help="Major transition gate to pause on.",
    )
    pause.add_argument("--notes", help="Optional pause notes")
    pause.set_defaults(func=cmd_pause)

    resume = run_sub.add_parser("resume", help="Approve or revise a paused major gate")
    resume.add_argument("--repo", help="Target repository directory. Defaults to current working directory.")
    resume.add_argument("--slug", required=True, help="Canonical workflow slug")
    decision = resume.add_mutually_exclusive_group(required=True)
    decision.add_argument(
        "--approve",
        choices=sorted(GATE_TRANSITIONS.keys()),
        help="Approve the currently pending major transition gate.",
    )
    decision.add_argument(
        "--revise-current-stage",
        action="store_true",
        help="Route back to the create or implementation stage associated with the pending gate.",
    )
    resume.add_argument("--notes", help="Optional approval or revision notes")
    resume.set_defaults(func=cmd_resume)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
