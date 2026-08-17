"""research-md subprocess hook — docket.md → shipr, but for findings."""

from __future__ import annotations

import shutil
import subprocess
from unittest.mock import MagicMock, patch

import pytest

from lessons_md._logic.lesson import lesson_create, lesson_promote
from lessons_md.config import init_project, register_project
from lessons_md.errors import LessonGateError
from lessons_md.files import find_lesson_file, read_markdown
from lessons_md.hooks.research_hook import (
    find_research_root,
    looks_like_finding_id,
    looks_like_uuid,
    promote_via_research_md,
)


def _setup(tmp_path) -> tuple[str, str]:
    root = str(tmp_path)
    config = init_project(root)
    register_project(root)
    return root, config.id


class TestIdShapes:
    def test_uuid(self):
        assert looks_like_uuid("742887c1-3a10-47c7-b19f-93357e45e04b")
        assert not looks_like_uuid("RES-0099")
        assert not looks_like_uuid("0001")

    def test_finding(self):
        assert looks_like_finding_id("0001")
        assert looks_like_finding_id("1")
        assert not looks_like_finding_id("RES-0099")


class TestFindRoot:
    def test_missing(self, tmp_path):
        assert find_research_root(str(tmp_path)) is None

    def test_finds_dot_research(self, tmp_path):
        (tmp_path / ".research").mkdir()
        (tmp_path / ".research" / "research.json").write_text("{}")
        assert find_research_root(str(tmp_path)) == str(tmp_path.resolve())


class TestHook:
    def test_disabled_skips(self):
        runner = MagicMock()
        out = promote_via_research_md(
            "/proj", "LESSON-0001", "T", "C", enabled=False, runner=runner
        )
        assert out.skipped is True
        runner.assert_not_called()

    def test_missing_binary_fails(self):
        runner = MagicMock()
        with patch("lessons_md.hooks.research_hook.shutil.which", return_value=None):
            out = promote_via_research_md(
                "/proj", "LESSON-0001", "T", "C", runner=runner
            )
        assert out.ok is False
        assert "not on PATH" in out.message
        runner.assert_not_called()

    def test_creates_finding(self, tmp_path):
        (tmp_path / ".research").mkdir()
        (tmp_path / ".research" / "research.json").write_text(
            '{"id": "742887c1-3a10-47c7-b19f-93357e45e04b"}'
        )
        runner = MagicMock()
        runner.side_effect = [
            MagicMock(
                returncode=0,
                stdout="Registered: .\nID: 742887c1-3a10-47c7-b19f-93357e45e04b\n",
                stderr="",
            ),
            MagicMock(
                returncode=0,
                stdout="Finding created: findings/0001-t.md\nID: 0001 | Evidence: LOW\n",
                stderr="",
            ),
        ]
        with patch(
            "lessons_md.hooks.research_hook.shutil.which",
            return_value="/bin/research-md",
        ):
            out = promote_via_research_md(
                str(tmp_path),
                "LESSON-0001",
                "Needs research",
                "This should become a finding.",
                runner=runner,
            )
        assert out.ok is True
        assert out.finding_id == "0001"
        assert out.research_id == "742887c1-3a10-47c7-b19f-93357e45e04b"
        create_argv = runner.call_args_list[1].args[0]
        assert create_argv[1] == "finding-create"
        assert "Needs research" in create_argv

    def test_placeholder_id_fails(self, tmp_path):
        (tmp_path / ".research").mkdir()
        (tmp_path / ".research" / "research.json").write_text(
            '{"id": "742887c1-3a10-47c7-b19f-93357e45e04b"}'
        )
        runner = MagicMock()
        runner.return_value = MagicMock(
            returncode=0,
            stdout="ID: 742887c1-3a10-47c7-b19f-93357e45e04b\n",
            stderr="",
        )
        with patch(
            "lessons_md.hooks.research_hook.shutil.which",
            return_value="/bin/research-md",
        ):
            out = promote_via_research_md(
                str(tmp_path),
                "LESSON-0001",
                "T",
                "C",
                "RES-0099",
                runner=runner,
            )
        assert out.ok is False
        assert "RES-0099" in out.message


class TestPromoteWiresHook:
    def test_promote_calls_hook_and_stores_finding(self, tmp_path):
        root, pid = _setup(tmp_path)
        lesson_create(pid, "Needs research", "This should become a finding.")
        hook = MagicMock()
        hook.ok = True
        hook.skipped = False
        hook.message = "research-md: created finding 0001 from LESSON-0001"
        hook.research_id = "742887c1-3a10-47c7-b19f-93357e45e04b"
        hook.finding_id = "0001"
        with patch(
            "lessons_md._logic.lesson.promote_via_research_md", return_value=hook
        ) as called:
            # Force the research path even without .research/ by passing a ref
            # and a fake discover? Hook is patched; need want_research True.
            # Passing research_id makes want_research True.
            out = lesson_promote(pid, "LESSON-0001", research_id="0001")
        called.assert_called_once()
        assert "finding_id=0001" in out
        fm = read_markdown(find_lesson_file(root, "LESSON-0001")).frontmatter
        assert fm["promotes_to"]["finding_id"] == "0001"
        assert fm["status"] == "promoted-research"

    def test_hook_failure_blocks_promote(self, tmp_path):
        _, pid = _setup(tmp_path)
        lesson_create(pid, "Needs research", "This should become a finding.")
        hook = MagicMock()
        hook.ok = False
        hook.message = "research-md is not on PATH"
        with patch(
            "lessons_md._logic.lesson.promote_via_research_md", return_value=hook
        ):
            with pytest.raises(LessonGateError, match="not on PATH"):
                lesson_promote(pid, "LESSON-0001", research_id="0001")


@pytest.mark.skipif(
    shutil.which("research-md") is None, reason="research-md not on PATH"
)
def test_live_promote_creates_a_real_finding(tmp_path):
    root, pid = _setup(tmp_path)
    lesson_create(pid, "Live hook", "research-md must actually run.")
    init = subprocess.run(
        [
            "research-md",
            "project-init",
            str(tmp_path),
            "--name",
            "live",
            "--question",
            "Does the hook create a finding?",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert init.returncode == 0, init.stderr
    out = lesson_promote(pid, "LESSON-0001")
    assert "finding_id=" in out
    findings = list((tmp_path / ".research" / "findings").glob("*.md"))
    assert findings, out
    fm = read_markdown(find_lesson_file(root, "LESSON-0001")).frontmatter
    assert fm["promotes_to"]["finding_id"]
    assert fm["status"] == "promoted-research"
