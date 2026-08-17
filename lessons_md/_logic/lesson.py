"""Lesson CRUD: create, list, view, update, supersede, promote."""

from __future__ import annotations

import os

from ..errors import LessonGateError, LessonNotFoundError
from ..files import (
    find_lesson_file,
    lesson_path,
    list_lessons,
    next_lesson_id,
    read_markdown,
    write_markdown,
)
from ..gates import (
    advisory_no_origin,
    advisory_reasoned_unpromoted,
    gate_claim_present,
    gate_confirmed_earned,
    gate_promote_target,
)
from ._common import get_project, today

_DEFAULT_BODY = """## Claim

## What happened

## Do differently

## Caveats

## Promotion
"""

_FM_ORDER = (
    "id",
    "type",
    "title",
    "status",
    "date",
    "confidence",
    "claim",
    "origin_task",
    "promotes_to",
    "supersedes",
    "concerns",
)


def _reject_confirmed(confidence: str | None, fm: dict | None = None) -> None:
    preview = dict(fm or {})
    if confidence is not None:
        preview["confidence"] = confidence
    result = gate_confirmed_earned(preview)
    if not result["passed"]:
        raise LessonGateError(result["error"])


def _require_lesson(project_root: str, lesson_id: str) -> tuple[str, object]:
    fp = find_lesson_file(project_root, lesson_id)
    if not fp:
        raise LessonNotFoundError("Lesson", lesson_id)
    return fp, read_markdown(fp)


def _default_promotes_to() -> dict:
    return {"research_id": None, "adr": None}


def _body(content: str) -> str:
    return content if content else _DEFAULT_BODY


def _write_lesson(
    project_root: str,
    fm: dict,
    content: str,
    *,
    superseded: bool = False,
    old_path: str | None = None,
) -> str:
    dest = lesson_path(project_root, fm["id"], fm["title"], superseded=superseded)
    write_markdown(dest, fm, content)
    if old_path and old_path != dest and os.path.exists(old_path):
        os.unlink(old_path)
    return dest


def _format_scalar(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str) and (
        value == ""
        or value[0] in "0123456789"
        or any(ch in value for ch in ":#{}[],&*?|>!%@`")
        or value.lower() in {"true", "false", "null", "yes", "no"}
    ):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return str(value)


def _format_lesson(fm: dict, content: str) -> str:
    keys = [k for k in _FM_ORDER if k in fm]
    keys.extend(k for k in fm if k not in _FM_ORDER)
    lines = ["---"]
    for key in keys:
        value = fm[key]
        if isinstance(value, dict):
            lines.append(f"{key}:")
            for nested_key, nested_val in value.items():
                lines.append(f"  {nested_key}: {_format_scalar(nested_val)}")
        elif isinstance(value, list):
            if not value:
                lines.append(f"{key}: []")
            else:
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {_format_scalar(item)}")
        else:
            lines.append(f"{key}: {_format_scalar(value)}")
    lines.append("---")
    rendered = "\n".join(lines)
    if content:
        return rendered + "\n" + content.rstrip("\n")
    return rendered


def lesson_create(
    project_id: str,
    title: str,
    claim: str,
    content: str = "",
    confidence: str = "LOW",
    concerns: list[str] | None = None,
    origin_task: str | None = None,
) -> str:
    """Create a lesson. CONFIRMED is illegal until research earns it."""
    claim_gate = gate_claim_present(claim)
    if not claim_gate["passed"]:
        raise LessonGateError(claim_gate["error"])
    _reject_confirmed(confidence)
    project_root = get_project(project_id)
    id = next_lesson_id(project_root)
    fm: dict = {
        "id": id,
        "type": "lesson",
        "title": title,
        "status": "open",
        "date": today(),
        "confidence": confidence,
        "claim": claim,
        "origin_task": origin_task,
        "promotes_to": _default_promotes_to(),
        "supersedes": None,
        "concerns": concerns if concerns is not None else ["paseo"],
    }
    _write_lesson(project_root, fm, _body(content))
    result = f"Created lesson **{id}** — {title}"
    advisories = [
        a
        for a in (advisory_no_origin(origin_task), advisory_reasoned_unpromoted(fm))
        if a
    ]
    if advisories:
        result += "\n\n" + "\n".join(f"⚠ {a}" for a in advisories)
    return result


def lesson_list(project_id: str, include_superseded: bool = False) -> str:
    """List lessons as ``**LESSON-0001** [open/LOW] — title``."""
    project_root = get_project(project_id)
    lessons = list_lessons(project_root, include_superseded=include_superseded)
    if not lessons:
        return "No lessons."
    return "\n".join(
        f"**{lesson.frontmatter['id']}** "
        f"[{lesson.frontmatter.get('status', '?')}/"
        f"{lesson.frontmatter.get('confidence', '?')}] — "
        f"{lesson.frontmatter.get('title', '')}"
        for lesson in lessons
    )


def lesson_view(project_id: str, lesson_id: str) -> str:
    """View a lesson's full frontmatter and body."""
    project_root = get_project(project_id)
    _fp, lesson = _require_lesson(project_root, lesson_id)
    return _format_lesson(lesson.frontmatter, lesson.content)


def lesson_update(
    project_id: str,
    lesson_id: str,
    title: str | None = None,
    claim: str | None = None,
    content: str | None = None,
    append_content: str | None = None,
    confidence: str | None = None,
    concerns: list[str] | None = None,
    status: str | None = None,
) -> str:
    """Update a lesson. Renames the file when the title changes."""
    project_root = get_project(project_id)
    fp, lesson = _require_lesson(project_root, lesson_id)
    fm = {**lesson.frontmatter}
    if claim is not None:
        claim_gate = gate_claim_present(claim)
        if not claim_gate["passed"]:
            raise LessonGateError(claim_gate["error"])
    _reject_confirmed(confidence, fm)
    if title is not None:
        fm["title"] = title
    if claim is not None:
        fm["claim"] = claim
    if confidence is not None:
        fm["confidence"] = confidence
    if concerns is not None:
        fm["concerns"] = concerns
    if status is not None:
        fm["status"] = status
    if append_content:
        new_content = f"{lesson.content}\n\n{append_content}".strip()
    elif content is not None:
        new_content = content
    else:
        new_content = lesson.content
    _write_lesson(
        project_root,
        fm,
        new_content,
        superseded=fm.get("status") == "superseded",
        old_path=fp,
    )
    return f"Updated **{fm['id']}** — {fm['title']}"


def lesson_supersede(
    project_id: str,
    old_id: str,
    new_title: str,
    claim: str,
    content: str = "",
    confidence: str = "LOW",
) -> str:
    """Create a new lesson that supersedes ``old_id`` and archive the old file."""
    _reject_confirmed(confidence)
    project_root = get_project(project_id)
    fp, old = _require_lesson(project_root, old_id)
    old_fm = {**old.frontmatter, "status": "superseded"}
    _write_lesson(
        project_root,
        old_fm,
        old.content,
        superseded=True,
        old_path=fp,
    )
    new_id = next_lesson_id(project_root)
    new_fm: dict = {
        "id": new_id,
        "type": "lesson",
        "title": new_title,
        "status": "open",
        "date": today(),
        "confidence": confidence,
        "claim": claim,
        "origin_task": None,
        "promotes_to": _default_promotes_to(),
        "supersedes": old_id,
        "concerns": ["paseo"],
    }
    _write_lesson(project_root, new_fm, _body(content))
    return f"Superseded **{old_id}** with **{new_id}** — {new_title}"


def lesson_promote(
    project_id: str,
    lesson_id: str,
    research_id: str | None = None,
    adr: str | None = None,
) -> str:
    """Link a lesson to research and/or an ADR. Does not create either."""
    target = gate_promote_target(research_id, adr)
    if not target["passed"]:
        raise LessonGateError(target["error"])
    project_root = get_project(project_id)
    fp, lesson = _require_lesson(project_root, lesson_id)
    fm = {**lesson.frontmatter}
    promotes_to = dict(fm.get("promotes_to") or _default_promotes_to())
    if research_id:
        promotes_to["research_id"] = research_id
    if adr:
        promotes_to["adr"] = adr
    fm["promotes_to"] = promotes_to
    if research_id:
        fm["status"] = "promoted-research"
    else:
        fm["status"] = "promoted-adr"
    _write_lesson(
        project_root,
        fm,
        lesson.content,
        superseded=False,
        old_path=fp,
    )
    parts = []
    if research_id:
        parts.append(f"research_id={research_id}")
    if adr:
        parts.append(f"adr={adr}")
    return f"Promoted **{fm['id']}** → {fm['status']} ({', '.join(parts)})"
