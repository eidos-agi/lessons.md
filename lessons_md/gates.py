"""Lesson gates — CONFIRMED is illegal until research.md earns it.

Mirrors research.md's evidence-gate module: hard fails return
``{"passed": False, "error": ...}``; advisories are soft strings.
"""

from __future__ import annotations

_CONFIRMED_ERROR = (
    "CONFIRMED is illegal until a research.md finding earned it. "
    "Use lesson-promote after research."
)


def _promoted_by_research(fm: dict) -> bool:
    if fm.get("status") == "promoted-research":
        return True
    promotes_to = fm.get("promotes_to") or {}
    return isinstance(promotes_to, dict) and bool(promotes_to.get("research_id"))


def gate_confirmed_earned(fm: dict) -> dict:
    """CONFIRMED requires a research.md promotion. Same rule as research's
    triangulation gate: the top grade is earned, not declared."""
    if str(fm.get("confidence", "")).upper() != "CONFIRMED":
        return {"passed": True}
    if _promoted_by_research(fm):
        return {"passed": True}
    return {"passed": False, "error": _CONFIRMED_ERROR}


def gate_promote_target(research_id: str | None, adr: str | None) -> dict:
    """Promotion must point at research.md and/or an ADR."""
    if research_id or adr:
        return {"passed": True}
    return {
        "passed": False,
        "error": "lesson-promote requires --research-id and/or --adr.",
    }


def gate_claim_present(claim: str | None) -> dict:
    if claim is not None and not str(claim).strip():
        return {
            "passed": False,
            "error": "A lesson claim cannot be empty. One sentence another agent can act on.",
        }
    return {"passed": True}


def advisory_no_origin(origin_task: str | None) -> str | None:
    if origin_task:
        return None
    return (
        "This lesson has no origin_task. If it came from a docket.md task, "
        "pass --origin-task so the next agent can find the execution that taught it."
    )


def advisory_reasoned_unpromoted(fm: dict) -> str | None:
    if str(fm.get("confidence", "")).upper() != "REASONED":
        return None
    if _promoted_by_research(fm):
        return None
    return (
        "REASONED is still un-binding. Promote to a research.md finding "
        "(lesson-promote --research-id) before treating this as earned."
    )


def run_lesson_gates(fm: dict) -> dict:
    """Run hard gates. Returns the first failure."""
    for check in (
        gate_confirmed_earned(fm),
        gate_claim_present(fm.get("claim")),
    ):
        if not check["passed"]:
            return check
    return {"passed": True}
