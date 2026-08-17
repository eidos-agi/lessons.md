"""Project init, set, info, GUID stability."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from lessons_md._logic.project import project_info, project_set, status
from lessons_md.config import init_project, resolve_project
from lessons_md.errors import LessonValidationError


def test_init_writes_config_and_dirs(tmp_path):
    config = init_project(str(tmp_path))

    lessons_json = tmp_path / ".lessons" / "lessons.json"
    assert lessons_json.is_file()
    data = json.loads(lessons_json.read_text())
    assert data["id"] == config.id
    assert data["id"]
    assert (tmp_path / ".lessons" / "lessons").is_dir()
    assert (tmp_path / ".lessons" / "superseded").is_dir()


def test_project_set_registers_and_info_works(tmp_path):
    config = init_project(str(tmp_path))
    out = project_set(str(tmp_path))
    assert config.id in out

    info = project_info(config.id)
    assert config.id in info
    assert str(tmp_path) in info or Path(tmp_path).name in info


def test_resolve_project_unknown_guid_mentions_project_set():
    with pytest.raises(LessonValidationError, match="project_set"):
        resolve_project("00000000-0000-0000-0000-000000000000")


def test_mcp_help_lists_status():
    from lessons_md.mcp_server import _build_top_level_help

    help_text = _build_top_level_help()
    assert "status --project-id" in help_text
    assert "CONFIRMED" in help_text


def test_status_reports_integrity_pass(tmp_path):
    config = init_project(str(tmp_path))
    project_set(str(tmp_path))
    out = status(config.id)
    assert "Lessons Status" in out
    assert "Integrity:** All checks passed" in out
    info = project_info(config.id)
    assert "Integrity: All checks passed" in info


def test_reinit_same_path_keeps_id(tmp_path):
    first = init_project(str(tmp_path))
    second = init_project(str(tmp_path))
    assert first.id == second.id

    data = json.loads((tmp_path / ".lessons" / "lessons.json").read_text())
    assert data["id"] == first.id
