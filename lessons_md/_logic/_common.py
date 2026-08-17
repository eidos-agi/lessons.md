"""Shared helpers."""

from __future__ import annotations

from datetime import date


def today() -> str:
    return date.today().isoformat()
