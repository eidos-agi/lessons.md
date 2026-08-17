"""CLI session boot — auto-register projects from filesystem before any tool call.

The MCP server kept a long-lived in-memory ``project_id → path`` map; a
fresh CLI subprocess does not. ``boot_from_cwd()`` walks up from CWD,
finds any directory with ``.lessons/lessons.json``, and registers it.
"""

from __future__ import annotations

from pathlib import Path

from .. import config as _cfg
from ..config import register_project


def _walk_up_for_lessons(start: Path) -> Path | None:
    """Walk up looking for a lessons.md project (``.lessons/lessons.json`` only)."""
    cur = start.resolve()
    while True:
        if (cur / _cfg.LESSONS_DIR / _cfg.CONFIG_FILENAME).is_file():
            return cur
        if cur.parent == cur:
            return None
        cur = cur.parent


def boot_from_cwd(path: str | None = None) -> None:
    """Register any lessons.md project rooted at or above CWD.

    Safe to call repeatedly. Silently no-ops if no project is found.
    """
    start = Path(path).resolve() if path else Path.cwd()
    root = _walk_up_for_lessons(start)
    if root is None:
        return
    try:
        register_project(str(root))
    except Exception:
        return
