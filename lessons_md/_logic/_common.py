"""Helpers shared across logic modules — date, GUID resolution."""

from __future__ import annotations

from datetime import date

from ..config import resolve_project


def today() -> str:
    return date.today().isoformat()


def get_project(project_id: object) -> str:
    """Resolve a registered project_id to its root path. Typed errors."""
    return resolve_project(project_id)
