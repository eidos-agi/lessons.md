"""Gates — CONFIRMED is earned, promotion needs a target. Same style as research.md."""

from lessons_md.gates import (
    advisory_no_origin,
    advisory_reasoned_unpromoted,
    gate_claim_present,
    gate_confirmed_earned,
    gate_promote_target,
    run_lesson_gates,
)


class TestConfirmedEarned:
    def test_low_skips(self):
        assert gate_confirmed_earned({"confidence": "LOW"})["passed"] is True

    def test_reasoned_skips(self):
        assert gate_confirmed_earned({"confidence": "REASONED"})["passed"] is True

    def test_confirmed_without_research_fails(self):
        result = gate_confirmed_earned({"confidence": "CONFIRMED"})
        assert result["passed"] is False
        assert "research.md" in result["error"]

    def test_confirmed_after_promote_passes(self):
        fm = {
            "confidence": "CONFIRMED",
            "status": "promoted-research",
            "promotes_to": {"research_id": "RES-0001"},
        }
        assert gate_confirmed_earned(fm)["passed"] is True

    def test_confirmed_with_research_id_only_passes(self):
        fm = {
            "confidence": "CONFIRMED",
            "promotes_to": {"research_id": "RES-0001"},
        }
        assert gate_confirmed_earned(fm)["passed"] is True


class TestPromoteTarget:
    def test_research_id_passes(self):
        assert gate_promote_target("RES-1", None)["passed"] is True

    def test_adr_passes(self):
        assert gate_promote_target(None, "ADR-1")["passed"] is True

    def test_neither_fails(self):
        result = gate_promote_target(None, None)
        assert result["passed"] is False
        assert "research-id" in result["error"]


class TestClaim:
    def test_empty_fails(self):
        assert gate_claim_present("")["passed"] is False

    def test_whitespace_fails(self):
        assert gate_claim_present("   ")["passed"] is False

    def test_present_passes(self):
        assert gate_claim_present("Do X before Y.")["passed"] is True

    def test_none_skips(self):
        assert gate_claim_present(None)["passed"] is True


class TestAdvisories:
    def test_missing_origin(self):
        assert advisory_no_origin(None) is not None

    def test_has_origin(self):
        assert advisory_no_origin("TASK-0001") is None

    def test_reasoned_unpromoted(self):
        assert advisory_reasoned_unpromoted({"confidence": "REASONED"}) is not None

    def test_reasoned_promoted_silent(self):
        fm = {
            "confidence": "REASONED",
            "status": "promoted-research",
            "promotes_to": {"research_id": "RES-1"},
        }
        assert advisory_reasoned_unpromoted(fm) is None


class TestRunGates:
    def test_first_failure_wins(self):
        result = run_lesson_gates({"confidence": "CONFIRMED", "claim": ""})
        assert result["passed"] is False
        assert "CONFIRMED" in result["error"] or "claim" in result["error"].lower()
