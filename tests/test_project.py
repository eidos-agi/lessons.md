"""Project init, set, info, GUID stability."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from lessons_md._logic.project import project_info, project_set
from lessons_md.config import init_project, resolve_project


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
    with pytest.raises(ValueError, match="project_set"):
        resolve_project("00000000-0000-0000-0000-000000000000")


def test_reinit_same_path_keeps_id(tmp_path):
    first = init_project(str(tmp_path))
    second = init_project(str(tmp_path))
    assert first.id == second.id

    data = json.loads((tmp_path / ".lessons" / "lessons.json").read_text())
    assert data["id"] == first.id
