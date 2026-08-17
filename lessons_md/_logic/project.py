"""Project lifecycle: init, set, list, info."""

from __future__ import annotations

import os

from .. import config as _cfg
from ..config import (
    init_project,
    list_registered,
    load_config,
    register_project,
    resolve_project,
)
from ..files import list_lessons
from ..integrity import check_integrity

_LESSON_STATUSES = (
    "open",
    "promoted-research",
    "promoted-adr",
    "superseded",
    "retired",
)


def project_init(path: str, name: str | None = None) -> str:
    """Initialize a new lessons.md project."""
    config = init_project(path, name)
    try:
        register_project(os.path.abspath(path))
    except Exception:
        pass
    return (
        f"Project initialized: **{config.project}**\nproject_id: `{config.id}`\n"
        f"Path: {path}\n\nUse this project_id in all subsequent calls."
    )


def project_set(path: str) -> str:
    """Register an existing lessons.md project for this session.

    Always hands the caller the active lessons. LOOK-0001: do not swallow
    retrieval failures.
    """
    from .lesson import lesson_relevant

    result = register_project(path)
    lines = [
        f"Project registered: **{result['project']}**",
        f"project_id: `{result['id']}`",
        "",
        "Use this project_id in all subsequent calls.",
        "",
        lesson_relevant(result["id"]),
    ]
    return "\n".join(lines)


def project_list() -> str:
    """List all projects registered in this session."""
    projects = list_registered()
    if not projects:
        return (
            "No projects registered this session. Call project_set with a project path."
        )
    return "\n".join(f"- `{p['id']}` → {p['path']}" for p in projects)


def _counts(project_root: str) -> dict[str, int]:
    lessons = list_lessons(project_root, include_superseded=True)
    counts = {status: 0 for status in _LESSON_STATUSES}
    for lesson in lessons:
        status = lesson.frontmatter.get("status")
        if status in counts:
            counts[status] += 1
        elif status:
            counts[status] = counts.get(status, 0) + 1
    return counts


def project_info(project_id: str) -> str:
    """Show project stats — lesson counts by status plus an integrity line."""
    project_root = resolve_project(project_id)
    config = load_config(project_root)
    name = config.project if config else os.path.basename(project_root)
    counts = _counts(project_root)
    status_line = " · ".join(f"{s}: {n}" for s, n in counts.items())
    issues = check_integrity(project_root)
    errors = sum(1 for i in issues if i["severity"] == "error")
    warnings = sum(1 for i in issues if i["severity"] != "error")
    if issues:
        integrity = (
            f"Integrity: {errors} error(s), {warnings} warning(s) — run `status`"
        )
    else:
        integrity = "Integrity: All checks passed."
    lines = [
        f"## {name}",
        f"project_id: `{project_id}`",
        f"Path: {project_root}",
        f"Layout: {_cfg.LESSONS_DIR}/",
        "",
        f"**Lessons:** {status_line}",
        f"**{integrity}**",
    ]
    return "\n".join(lines)


def status(project_id: str) -> str:
    """Show project health: each lesson, promotions, integrity vs disk."""
    project_root = resolve_project(project_id)
    config = load_config(project_root)
    name = config.project if config else os.path.basename(project_root)
    lessons = list_lessons(project_root, include_superseded=True)
    counts = _counts(project_root)
    status_line = " · ".join(f"{s}: {n}" for s, n in counts.items())
    lines = [
        f"## {name} — Lessons Status",
        "",
        f"project_id: `{project_id}`",
        f"Path: {project_root}",
        f"Layout: {_cfg.LESSONS_DIR}/",
        "",
        f"**Lessons:** {status_line}",
        "",
    ]
    if not lessons:
        lines.append("No lessons.")
    else:
        for lesson in lessons:
            fm = lesson.frontmatter
            line = (
                f"**{fm.get('id', '?')}** "
                f"[{fm.get('status', '?')}/{fm.get('confidence', '?')}] — "
                f"{fm.get('title', '')}"
            )
            promotes = fm.get("promotes_to") or {}
            if isinstance(promotes, dict) and promotes.get("research_id"):
                line += f" → {promotes['research_id']}"
            if fm.get("supersedes"):
                line += f" (supersedes {fm['supersedes']})"
            lines.append(line)

    issues = check_integrity(project_root)
    if issues:
        lines.extend(["", "**Integrity issues:**"])
        for issue in issues:
            icon = "ERROR" if issue["severity"] == "error" else "WARNING"
            lines.append(f"  [{icon}] {issue['message']}")
    else:
        lines.extend(["", "**Integrity:** All checks passed."])
    return "\n".join(lines)
