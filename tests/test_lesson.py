"""Lesson create, list, view, update, supersede, promote."""

from __future__ import annotations

from pathlib import Path

from lessons_md._logic.lesson import (
    lesson_create,
    lesson_list,
    lesson_promote,
    lesson_relevant,
    lesson_supersede,
    lesson_update,
    lesson_view,
)
from lessons_md.config import init_project, register_project
from lessons_md.errors import LessonError, LessonNotFoundError
from lessons_md.files import find_lesson_file, read_markdown


def _setup_project(tmp_path) -> str:
    project_root = str(tmp_path)
    config = init_project(project_root)
    register_project(project_root)
    return config.id


def _frontmatter(tmp_path, lesson_id: str) -> dict:
    fp = find_lesson_file(str(tmp_path), lesson_id)
    assert fp is not None, f"{lesson_id} file not found"
    return read_markdown(fp).frontmatter


def _assert_rejected(fn, *args, needle: str, **kwargs) -> None:
    """Accept LessonError/ValueError or an error string containing needle."""
    try:
        result = fn(*args, **kwargs)
    except (LessonError, ValueError) as exc:
        assert needle in str(exc)
        return
    assert isinstance(result, str), (
        f"expected error or error string, got {type(result)}"
    )
    assert needle in result


class TestCreateAndRead:
    def test_create_writes_open_low_lesson(self, tmp_path):
        pid = _setup_project(tmp_path)
        out = lesson_create(
            pid,
            "Always register the project",
            "Call project-set before any lesson write.",
        )
        assert "LESSON-0001" in out
        assert "origin_task" in out  # advisory: no origin_task

        fp = find_lesson_file(str(tmp_path), "LESSON-0001")
        assert fp is not None
        path = Path(fp)
        assert path.parent.name == "lessons"
        assert path.parent.parent.name == ".lessons"

        fm = read_markdown(fp).frontmatter
        assert fm["id"] == "LESSON-0001"
        assert fm["status"] == "open"
        assert fm["confidence"] == "LOW"

    def test_confirmed_on_create_rejected(self, tmp_path):
        pid = _setup_project(tmp_path)
        _assert_rejected(
            lesson_create,
            pid,
            "Too sure too soon",
            "This claim is not earned yet.",
            confidence="CONFIRMED",
            needle="CONFIRMED",
        )

    def test_list_shows_the_lesson(self, tmp_path):
        pid = _setup_project(tmp_path)
        lesson_create(pid, "Register first", "Call project-set first.")
        listed = lesson_list(pid)
        assert "LESSON-0001" in listed

    def test_view_includes_claim(self, tmp_path):
        pid = _setup_project(tmp_path)
        claim = "Call project-set before any lesson write."
        lesson_create(pid, "Register first", claim)
        view = lesson_view(pid, "LESSON-0001")
        assert claim in view


class TestUpdate:
    def test_update_claim_and_append_content(self, tmp_path):
        pid = _setup_project(tmp_path)
        lesson_create(pid, "Register first", "Original claim.")
        lesson_update(
            pid,
            "LESSON-0001",
            claim="Revised claim another agent can act on.",
            append_content="Extra body from the update.",
        )
        view = lesson_view(pid, "LESSON-0001")
        assert "Revised claim another agent can act on." in view
        assert "Extra body from the update." in view
        assert _frontmatter(tmp_path, "LESSON-0001")["claim"] == (
            "Revised claim another agent can act on."
        )


class TestSupersede:
    def test_supersede_moves_old_and_links_new(self, tmp_path):
        pid = _setup_project(tmp_path)
        lesson_create(pid, "First take", "The first claim.")
        out = lesson_supersede(
            pid,
            "LESSON-0001",
            "Second take",
            "The replacement claim.",
        )
        assert "LESSON-0001" in out
        assert "LESSON-0002" in out

        old_fp = find_lesson_file(str(tmp_path), "LESSON-0001")
        assert old_fp is not None
        old_path = Path(old_fp)
        assert old_path.parent.name == "superseded"
        assert old_path.parent.parent.name == ".lessons"
        assert read_markdown(old_fp).frontmatter["status"] == "superseded"

        new_fm = _frontmatter(tmp_path, "LESSON-0002")
        assert new_fm["supersedes"] == "LESSON-0001"


class TestPromote:
    def test_promote_research_id_sets_status_and_link(self, tmp_path):
        pid = _setup_project(tmp_path)
        lesson_create(pid, "Needs research", "This should become a finding.")
        lesson_promote(pid, "LESSON-0001", research_id="RES-0099", use_research=False)
        fm = _frontmatter(tmp_path, "LESSON-0001")
        assert fm["status"] == "promoted-research"
        assert fm["promotes_to"]["research_id"] == "RES-0099"

    def test_confirmed_allowed_after_research_promote(self, tmp_path):
        pid = _setup_project(tmp_path)
        lesson_create(pid, "Needs research", "This should become a finding.")
        lesson_promote(pid, "LESSON-0001", research_id="RES-0099", use_research=False)
        lesson_update(pid, "LESSON-0001", confidence="CONFIRMED")
        assert _frontmatter(tmp_path, "LESSON-0001")["confidence"] == "CONFIRMED"

    def test_promote_requires_research_id_or_adr(self, tmp_path):
        pid = _setup_project(tmp_path)
        lesson_create(pid, "Needs a target", "Promotion needs a destination.")
        _assert_rejected(lesson_promote, pid, "LESSON-0001", needle="research")

    def test_relevant_lists_open_and_matches_applies_when(self, tmp_path):
        pid = _setup_project(tmp_path)
        lesson_create(
            pid,
            "Promote by running research-md",
            "Shell out to research-md on promote.",
            applies_when="improving lessons.md after a session",
        )
        all_open = lesson_relevant(pid)
        assert "LESSON-0001" in all_open
        assert "read these before acting" in all_open
        matched = lesson_relevant(pid, "improving lessons.md")
        assert "LESSON-0001" in matched
        assert "when:" in matched
        missed = lesson_relevant(pid, "railway deploy")
        assert "No open lessons match" in missed

    def test_project_set_hands_open_lessons(self, tmp_path):
        from lessons_md._logic.project import project_set

        pid = _setup_project(tmp_path)
        lesson_create(pid, "Force retrieval", "project-set must print open lessons.")
        out = project_set(str(tmp_path))
        assert "LESSON-0001" in out
        assert "Force retrieval" in out

    def test_view_missing_raises(self, tmp_path):
        pid = _setup_project(tmp_path)
        try:
            lesson_view(pid, "LESSON-9999")
        except LessonNotFoundError as exc:
            assert "LESSON-9999" in str(exc)
        else:
            raise AssertionError("expected LessonNotFoundError")
