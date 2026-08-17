"""Project lifecycle: init, set, list, info."""

from __future__ import annotations

import os

from ..config import (
    init_project,
    list_registered,
    load_config,
    register_project,
    resolve_project,
)
from ..files import list_lessons

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
    """Register an existing lessons.md project for this session."""
    result = register_project(path)
    return (
        f"Project registered: **{result['project']}**\nproject_id: `{result['id']}`\n\n"
        "Use this project_id in all subsequent calls."
    )


def project_list() -> str:
    """List all projects registered in this session."""
    projects = list_registered()
    if not projects:
        return (
            "No projects registered this session. Call project_set with a project path."
        )
    return "\n".join(f"- `{p['id']}` → {p['path']}" for p in projects)


def project_info(project_id: str) -> str:
    """Show project stats — lesson counts by status."""
    project_root = resolve_project(project_id)
    config = load_config(project_root)
    name = config.project if config else os.path.basename(project_root)
    lessons = list_lessons(project_root, include_superseded=True)
    counts = {status: 0 for status in _LESSON_STATUSES}
    for lesson in lessons:
        status = lesson.frontmatter.get("status")
        if status in counts:
            counts[status] += 1
        elif status:
            counts[status] = counts.get(status, 0) + 1
    status_line = " · ".join(f"{s}: {n}" for s, n in counts.items())
    lines = [
        f"## {name}",
        f"project_id: `{project_id}`",
        f"Path: {project_root}",
        "",
        f"**Lessons:** {status_line}",
    ]
    return "\n".join(lines)
