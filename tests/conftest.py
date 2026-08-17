"""Shared fixtures. Clears the in-memory GUID registry between tests."""

from __future__ import annotations

import pytest

from lessons_md import config as _cfg
from lessons_md.cli import _app as _cli_app
from lessons_md.config import _guid_to_path


@pytest.fixture(autouse=True)
def _clear_project_registry():
    _guid_to_path.clear()
    _cfg.LESSONS_DIR = ".lessons"
    _cli_app._handed_lessons = False
    yield
    _guid_to_path.clear()
    _cfg.LESSONS_DIR = ".lessons"
    _cli_app._handed_lessons = False
