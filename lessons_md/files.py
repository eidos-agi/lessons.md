"""Markdown file I/O, ID generation, lesson path helpers.

Lesson CRUD lives in _logic/lesson.py later. This module is I/O + paths only.
"""

import os
import re
from dataclasses import dataclass
from typing import Any

import yaml

from . import config as _cfg
from .config import DIRECTORIES
from .security import safe_path


def _lessons_dir() -> str:
    """Dereference LESSONS_DIR at call time so monkey-patches take effect after import."""
    return _cfg.LESSONS_DIR


# ── Types ─────────────────────────────────────────────────────────────────────


@dataclass
class ParsedFile:
    frontmatter: dict[str, Any]
    content: str
    file_path: str


# ── YAML formatting to match gray-matter ──────────────────────────────────────


class _GrayMatterDumper(yaml.SafeDumper):
    """Custom YAML dumper that matches gray-matter (js-yaml) output.

    Key differences from default PyYAML:
    - Strings that look like dates get single-quoted: '2026-03-22'
    - List items are indented 2 spaces under their key (default_flow_style=False
      + best_width handling doesn't do this, we need indent+offset config)
    """

    pass


def _str_representer(dumper: yaml.Dumper, data: str) -> yaml.ScalarNode:
    # Quote strings that look like dates (YYYY-MM-DD)
    if re.match(r"^\d{4}-\d{2}-\d{2}$", data):
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="'")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


_GrayMatterDumper.add_representer(str, _str_representer)


# ── Read / Write ──────────────────────────────────────────────────────────────


def read_markdown(file_path: str) -> ParsedFile:
    with open(file_path) as f:
        raw = f.read()

    # Parse YAML frontmatter
    if raw.startswith("---\n"):
        end = raw.index("\n---\n", 4)
        fm_str = raw[4:end]
        content = raw[end + 5 :].strip()
        frontmatter = yaml.safe_load(fm_str) or {}
        # Convert date objects back to strings (yaml.safe_load parses dates)
        for k, v in frontmatter.items():
            if hasattr(v, "isoformat"):
                frontmatter[k] = v.isoformat()
    else:
        frontmatter = {}
        content = raw.strip()

    return ParsedFile(frontmatter=frontmatter, content=content, file_path=file_path)


def write_markdown(file_path: str, frontmatter: dict[str, Any], content: str) -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Filter out None values
    fm = {k: v for k, v in frontmatter.items() if v is not None}

    fm_str = yaml.dump(
        fm,
        Dumper=_GrayMatterDumper,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=True,
        indent=2,  # base indent
        width=4096,
    )
    # gray-matter (js-yaml) indents list items under their key with 2 spaces.
    # PyYAML puts them at the same level. Fix by adding 2-space indent to list items
    # that follow a key line.
    lines = fm_str.split("\n")
    fixed = []
    for line in lines:
        if line.startswith("- "):
            # This is a list item at root level — indent it
            fixed.append("  " + line)
        else:
            fixed.append(line)
    fm_str = "\n".join(fixed)

    with open(file_path, "w") as f:
        f.write("---\n")
        f.write(fm_str)
        f.write("---\n")
        if content:
            f.write(content)
            if not content.endswith("\n"):
                f.write("\n")
        else:
            f.write("\n")


# ── ID generation ─────────────────────────────────────────────────────────────


def _next_id(prefix: str, existing: list[str]) -> str:
    max_n = 0
    pattern = re.compile(rf"^{prefix}-(\d+)$", re.IGNORECASE)
    for id_str in existing:
        m = pattern.match(id_str)
        if m:
            n = int(m.group(1))
            max_n = max(max_n, n)
    return f"{prefix}-{str(max_n + 1).zfill(4)}"


def _slugify(title: str, max_len: int = 50) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower())
    slug = slug.strip("-")
    return slug[:max_len]


# ── Lessons ───────────────────────────────────────────────────────────────────


def _lesson_dir(project_root: str, superseded: bool = False) -> str:
    subdir = DIRECTORIES["SUPERSEDED"] if superseded else DIRECTORIES["LESSONS"]
    return safe_path(project_root, _lessons_dir(), subdir)


def list_lessons(
    project_root: str, include_superseded: bool = False
) -> list[ParsedFile]:
    results = []
    dirs = [_lesson_dir(project_root)]
    if include_superseded:
        dirs.append(_lesson_dir(project_root, superseded=True))

    for d in dirs:
        if not os.path.exists(d):
            continue
        for f in sorted(os.listdir(d)):
            if f.endswith(".md"):
                try:
                    results.append(read_markdown(os.path.join(d, f)))
                except Exception:
                    pass
    return results


def next_lesson_id(project_root: str) -> str:
    existing = [
        lesson.frontmatter["id"]
        for lesson in list_lessons(project_root, include_superseded=True)
        if lesson.frontmatter.get("id")
    ]
    return _next_id("LESSON", existing)


def lesson_path(
    project_root: str, id: str, title: str, superseded: bool = False
) -> str:
    slug = _slugify(title)
    subdir = DIRECTORIES["SUPERSEDED"] if superseded else DIRECTORIES["LESSONS"]
    return safe_path(project_root, _lessons_dir(), subdir, f"{id} - {slug}.md")


def find_lesson_file(project_root: str, id: str) -> str | None:
    dirs = [
        safe_path(project_root, _lessons_dir(), DIRECTORIES["LESSONS"]),
        safe_path(project_root, _lessons_dir(), DIRECTORIES["SUPERSEDED"]),
    ]
    for d in dirs:
        if not os.path.exists(d):
            continue
        for f in os.listdir(d):
            if f.startswith(id):
                return os.path.join(d, f)
    return None
