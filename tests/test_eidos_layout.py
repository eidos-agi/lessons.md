"""Eidos-aware boot — `.eidos/lessons/` is found the way research.md finds `.eidos/research/`."""

import json
from pathlib import Path

from lessons_md import config as _cfg
from lessons_md._logic._session import boot_from_cwd
from lessons_md.config import _guid_to_path, load_config


def test_boot_finds_eidos_layout(tmp_path, monkeypatch):
    eidos = tmp_path / ".eidos" / "lessons"
    eidos.mkdir(parents=True)
    payload = {
        "id": "11111111-1111-1111-1111-111111111111",
        "version": "0.1.0",
        "project": "eidos-demo",
        "created": "2026-08-17",
        "lessons_path": ".eidos/lessons",
    }
    (eidos / "lessons.json").write_text(json.dumps(payload))
    (eidos / "lessons").mkdir()
    (eidos / "superseded").mkdir()

    monkeypatch.setattr(_cfg, "LESSONS_DIR", ".lessons")
    monkeypatch.chdir(tmp_path)
    boot_from_cwd()

    assert _cfg.LESSONS_DIR == ".eidos/lessons"
    assert payload["id"] in _guid_to_path
    loaded = load_config(str(tmp_path))
    assert loaded is not None
    assert loaded.id == payload["id"]


def test_legacy_layout_still_wins_when_present(tmp_path, monkeypatch):
    from lessons_md.config import init_project, register_project

    monkeypatch.setattr(_cfg, "LESSONS_DIR", ".lessons")
    init_project(str(tmp_path), "legacy")
    register_project(str(tmp_path))
    monkeypatch.chdir(tmp_path)
    boot_from_cwd()
    assert _cfg.LESSONS_DIR == ".lessons"
    assert (Path(tmp_path) / ".lessons" / "lessons.json").is_file()
