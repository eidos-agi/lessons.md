"""Integrity checks — lesson status vs files on disk.

Same job as research.md's integrity module: the recorded state and the
filesystem must agree, or `status` says so.
"""

from __future__ import annotations

import os

from .files import find_lesson_file, list_lessons
from .gates import gate_confirmed_earned


def _in_superseded_dir(file_path: str) -> bool:
    parent = os.path.basename(os.path.dirname(os.path.abspath(file_path)))
    return parent == "superseded"


def check_integrity(project_root: str) -> list[dict]:
    issues: list[dict] = []
    lessons = list_lessons(project_root, include_superseded=True)
    for lesson in lessons:
        fm = lesson.frontmatter
        lid = fm.get("id", os.path.basename(lesson.file_path))
        status = fm.get("status")
        archived = _in_superseded_dir(lesson.file_path)

        if status == "superseded" and not archived:
            issues.append(
                {
                    "severity": "error",
                    "message": (
                        f"{lid} status is superseded but the file is still in "
                        "lessons/. Move it with lesson-supersede."
                    ),
                }
            )
        if status != "superseded" and archived:
            issues.append(
                {
                    "severity": "error",
                    "message": (
                        f"{lid} sits in superseded/ but status is {status!r}. "
                        "Status and directory disagree."
                    ),
                }
            )

        gate = gate_confirmed_earned(fm)
        if not gate["passed"]:
            issues.append({"severity": "error", "message": f"{lid}: {gate['error']}"})

        if status == "promoted-research":
            promotes = fm.get("promotes_to") or {}
            if not (isinstance(promotes, dict) and promotes.get("research_id")):
                issues.append(
                    {
                        "severity": "error",
                        "message": (
                            f"{lid} is promoted-research but promotes_to.research_id "
                            "is missing."
                        ),
                    }
                )

        if not str(fm.get("claim") or "").strip():
            issues.append(
                {
                    "severity": "warning",
                    "message": f"{lid} has an empty claim.",
                }
            )

        supersedes = fm.get("supersedes")
        if supersedes and not find_lesson_file(project_root, str(supersedes)):
            issues.append(
                {
                    "severity": "warning",
                    "message": (
                        f"{lid} supersedes {supersedes} but that lesson file "
                        "was not found."
                    ),
                }
            )

    return issues
