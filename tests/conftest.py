"""Shared fixtures. Clears the in-memory GUID registry between tests."""

from __future__ import annotations

import pytest

from lessons_md.config import _guid_to_path


@pytest.fixture(autouse=True)
def _clear_project_registry():
    _guid_to_path.clear()
    yield
    _guid_to_path.clear()
