"""CLI session boot — auto-register projects from filesystem before any tool call.

The MCP server kept a long-lived in-memory ``project_id → path`` map; a
fresh CLI subprocess does not. ``boot_from_cwd()`` walks up from CWD,
finds ``.lessons/lessons.json`` or ``.eidos/lessons/lessons.json``, and
registers it. Same eidos-aware-but-not-required property as research.md.
"""

from __future__ import annotations

from pathlib import Path

from .. import config as _cfg
from ..config import register_project


def _walk_up_for_lessons(start: Path) -> Path | None:
    """Walk up looking for a lessons.md project, eidos-aware or legacy."""
    cur = start.resolve()
    while True:
        if (cur / _cfg.LESSONS_DIR / _cfg.CONFIG_FILENAME).is_file():
            return cur
        if (cur / ".eidos" / "lessons" / _cfg.CONFIG_FILENAME).is_file():
            _cfg.LESSONS_DIR = _cfg.EIDOS_LESSONS_DIR
            return cur
        if cur.parent == cur:
            return None
        cur = cur.parent


def boot_from_cwd(path: str | None = None) -> str | None:
    """Register any lessons.md project rooted at or above CWD.

    Returns the project_id when a project was registered. No-ops if none found.
    """
    start = Path(path).resolve() if path else Path.cwd()
    root = _walk_up_for_lessons(start)
    if root is None:
        return None
    try:
        info = register_project(str(root))
    except Exception:
        return None
    return info.get("id")
