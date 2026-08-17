"""Integrity: recorded status vs files on disk."""

from pathlib import Path

from lessons_md._logic.lesson import lesson_create, lesson_promote, lesson_supersede
from lessons_md.config import init_project, register_project
from lessons_md.files import find_lesson_file, read_markdown, write_markdown
from lessons_md.integrity import check_integrity


def _setup(tmp_path) -> str:
    config = init_project(str(tmp_path))
    register_project(str(tmp_path))
    return config.id


def test_clean_project_has_no_issues(tmp_path):
    pid = _setup(tmp_path)
    lesson_create(pid, "Register first", "Call project-set first.")
    assert check_integrity(str(tmp_path)) == []


def test_confirmed_without_research_is_error(tmp_path):
    pid = _setup(tmp_path)
    lesson_create(pid, "Too sure", "This claim is not earned.")
    fp = find_lesson_file(str(tmp_path), "LESSON-0001")
    parsed = read_markdown(fp)
    parsed.frontmatter["confidence"] = "CONFIRMED"
    write_markdown(fp, parsed.frontmatter, parsed.content)
    issues = check_integrity(str(tmp_path))
    assert any(i["severity"] == "error" and "CONFIRMED" in i["message"] for i in issues)


def test_supersede_stays_clean(tmp_path):
    pid = _setup(tmp_path)
    lesson_create(pid, "First", "First claim.")
    lesson_supersede(pid, "LESSON-0001", "Second", "Replacement claim.")
    assert check_integrity(str(tmp_path)) == []


def test_promoted_without_research_id_is_error(tmp_path):
    pid = _setup(tmp_path)
    lesson_create(pid, "Needs research", "Promote me.")
    lesson_promote(pid, "LESSON-0001", research_id="RES-0099", use_research=False)
    fp = find_lesson_file(str(tmp_path), "LESSON-0001")
    parsed = read_markdown(fp)
    parsed.frontmatter["promotes_to"] = {"research_id": None, "adr": None}
    write_markdown(fp, parsed.frontmatter, parsed.content)
    issues = check_integrity(str(tmp_path))
    assert any("research_id" in i["message"] for i in issues)


def test_empty_claim_is_warning(tmp_path):
    _setup(tmp_path)
    dest = Path(tmp_path) / ".lessons" / "lessons" / "LESSON-0001 - empty.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        "---\nid: LESSON-0001\ntype: lesson\ntitle: Empty\nstatus: open\n"
        "confidence: LOW\nclaim: ''\n---\n\nbody\n"
    )
    issues = check_integrity(str(tmp_path))
    assert any(
        i["severity"] == "warning" and "empty claim" in i["message"] for i in issues
    )
