"""Call the research-md CLI when a lesson is promoted.

CONFIRMED is earned by a real research.md finding, not a typed string.
This hook is the docket.md → shipr pattern applied to the other neighbor:
subprocess, not a cloned module.

Unlike shipr-on-close (best-effort memory), a failed research-md call
blocks promotion. A missing binary or missing .research/ is a gate fail
unless the caller passed ``enabled=False``.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)
_FINDING_RE = re.compile(r"^\d{1,4}$")
_ID_LINE = re.compile(r"^ID:\s*(\S+)", re.MULTILINE)


@dataclass
class ResearchHookResult:
    ok: bool
    skipped: bool
    message: str
    research_id: str | None = None
    finding_id: str | None = None


def research_bin(command: str | None = None) -> str | None:
    name = (
        command.strip()
        if isinstance(command, str) and command.strip()
        else "research-md"
    )
    return shutil.which(name)


def find_research_root(start: str, explicit: str | None = None) -> str | None:
    if explicit:
        root = Path(explicit).resolve()
        if (root / ".research" / "research.json").is_file():
            return str(root)
        return None
    cur = Path(start).resolve()
    while True:
        if (cur / ".research" / "research.json").is_file():
            return str(cur)
        if cur.parent == cur:
            return None
        cur = cur.parent


def looks_like_uuid(value: str) -> bool:
    return bool(_UUID_RE.match(value))


def looks_like_finding_id(value: str) -> bool:
    return bool(_FINDING_RE.match(value))


def _run(
    argv: list[str],
    cwd: str,
    runner,
    timeout: int = 30,
) -> subprocess.CompletedProcess:
    run = runner or subprocess.run
    return run(
        argv,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=cwd,
        env=os.environ.copy(),
    )


def _parse_id(stdout: str) -> str | None:
    match = _ID_LINE.search(stdout or "")
    if not match:
        return None
    return match.group(1).rstrip("|").strip()


def _fail(message: str) -> ResearchHookResult:
    return ResearchHookResult(ok=False, skipped=False, message=message)


def promote_via_research_md(
    project_root: str,
    lesson_id: str,
    title: str,
    claim: str,
    research_ref: str | None = None,
    *,
    research_path: str | None = None,
    enabled: bool = True,
    command: str | None = None,
    runner=None,
) -> ResearchHookResult:
    """Create or verify a research-md finding for this lesson."""
    if not enabled:
        return ResearchHookResult(
            ok=True,
            skipped=True,
            message="research-md: skipped (disabled)",
            research_id=research_ref
            if research_ref and looks_like_uuid(research_ref)
            else None,
            finding_id=research_ref
            if research_ref and looks_like_finding_id(research_ref)
            else None,
        )

    bin_path = research_bin(command)
    if not bin_path:
        return _fail(
            "research-md is not on PATH. Install research-md or pass --no-research."
        )

    root = find_research_root(project_root, research_path)
    if not root:
        return _fail(
            "No .research/research.json above this project. "
            "Run `research-md project-init` or pass --research-path."
        )

    try:
        set_result = _run([bin_path, "project-set", root], root, runner)
    except subprocess.TimeoutExpired:
        return _fail("research-md project-set timed out")
    except OSError as e:
        return _fail(f"research-md project-set failed ({e})")

    if set_result.returncode != 0:
        detail = (set_result.stderr or set_result.stdout or "").strip().splitlines()
        return _fail(
            f"research-md project-set failed ({detail[-1] if detail else set_result.returncode})"
        )

    guid = _parse_id(set_result.stdout)
    if not guid:
        return _fail("research-md project-set did not return an ID")

    if research_ref and looks_like_finding_id(research_ref):
        return _verify_finding(bin_path, root, guid, research_ref.zfill(4), runner)

    if research_ref and not looks_like_uuid(research_ref):
        # Placeholder like RES-0099 is not a research.md id.
        return _fail(
            f"{research_ref!r} is not a research-md project GUID or finding id "
            f"(finding ids are 0001-style). Create a finding with research-md "
            f"or omit --research-id to create one from this lesson."
        )

    if research_ref and looks_like_uuid(research_ref) and research_ref != guid:
        return _fail(
            f"--research-id {research_ref} does not match .research/ at {root} ({guid})."
        )

    return _create_finding(bin_path, root, guid, lesson_id, title, claim, runner)


def _verify_finding(
    bin_path: str,
    root: str,
    guid: str,
    finding_id: str,
    runner,
) -> ResearchHookResult:
    try:
        listed = _run([bin_path, "finding-list", "--research-id", guid], root, runner)
    except (subprocess.TimeoutExpired, OSError) as e:
        return _fail(f"research-md finding-list failed ({e})")
    if listed.returncode != 0:
        detail = (listed.stderr or listed.stdout or "").strip().splitlines()
        return _fail(
            f"research-md finding-list failed ({detail[-1] if detail else listed.returncode})"
        )
    if finding_id not in (listed.stdout or ""):
        return _fail(
            f"research-md has no finding {finding_id} in {root}. "
            "Use finding-create first or omit --research-id to create one."
        )
    return ResearchHookResult(
        ok=True,
        skipped=False,
        message=f"research-md: verified finding {finding_id} in {guid}",
        research_id=guid,
        finding_id=finding_id,
    )


def _create_finding(
    bin_path: str,
    root: str,
    guid: str,
    lesson_id: str,
    title: str,
    claim: str,
    runner,
) -> ResearchHookResult:
    argv = [
        bin_path,
        "finding-create",
        "--research-id",
        guid,
        "--title",
        title,
        "--claim",
        claim,
        "--evidence",
        "LOW",
        "--source",
        f"lessons-md {lesson_id}",
    ]
    try:
        created = _run(argv, root, runner)
    except subprocess.TimeoutExpired:
        return _fail("research-md finding-create timed out")
    except OSError as e:
        return _fail(f"research-md finding-create failed ({e})")
    if created.returncode != 0:
        detail = (created.stderr or created.stdout or "").strip().splitlines()
        return _fail(
            f"research-md finding-create failed ({detail[-1] if detail else created.returncode})"
        )
    finding_id = _parse_id(created.stdout)
    if not finding_id:
        return _fail("research-md finding-create did not return an ID")
    return ResearchHookResult(
        ok=True,
        skipped=False,
        message=f"research-md: created finding {finding_id} from {lesson_id}",
        research_id=guid,
        finding_id=finding_id,
    )


def hook_result_as_dict(result: ResearchHookResult) -> dict[str, Any]:
    return {
        "ok": result.ok,
        "skipped": result.skipped,
        "message": result.message,
        "research_id": result.research_id,
        "finding_id": result.finding_id,
    }
