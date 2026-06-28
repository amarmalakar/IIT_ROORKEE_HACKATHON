"""Tests for the test-failure regeneration loop."""

from backend.graph.workflow import route_after_evaluation
from backend.models.state import create_initial_state
from backend.services.evaluation import evaluate_execution, MAX_REGENERATION_LOOPS


def test_evaluate_passes_on_success():
    state = create_initial_state("test")
    state["execution_result"] = {
        "execution_status": "success",
        "tests_summary": {"total": 3, "passed": 3, "failed": 0, "errors": 0},
        "test_results": [],
    }
    ev = evaluate_execution(state)
    assert ev["verdict"] == "PASS"
    assert ev["should_regenerate"] is False


def test_evaluate_triggers_regeneration_on_test_failure():
    state = create_initial_state("test")
    state["loop_count"] = 0
    state["execution_result"] = {
        "execution_status": "failed",
        "stderr": "AssertionError",
        "tests_summary": {"total": 2, "passed": 1, "failed": 1, "errors": 0},
        "test_results": [
            {"test_name": "test_ok", "status": "passed", "message": ""},
            {"test_name": "test_fail", "status": "failed", "message": "assert 1 == 2"},
        ],
    }
    ev = evaluate_execution(state)
    assert ev["verdict"] == "FAIL"
    assert ev["should_regenerate"] is True
    assert ev["regenerate_agent"] == "language_specialist"


def test_evaluate_stops_after_max_loops():
    state = create_initial_state("test")
    state["loop_count"] = MAX_REGENERATION_LOOPS
    state["execution_result"] = {
        "execution_status": "failed",
        "tests_summary": {"total": 1, "passed": 0, "failed": 1, "errors": 0},
        "test_results": [],
    }
    ev = evaluate_execution(state)
    assert ev["should_regenerate"] is False


def test_route_after_evaluation_regenerates():
    state = create_initial_state("test")
    state["loop_count"] = 1
    state["evaluation"] = {"should_regenerate": True, "regenerate_agent": "language_specialist"}
    assert route_after_evaluation(state) == "language_specialist"


def test_route_after_evaluation_stops_at_max_loops():
    state = create_initial_state("test")
    state["loop_count"] = 2
    state["evaluation"] = {"should_regenerate": True, "regenerate_agent": "language_specialist"}
    assert route_after_evaluation(state) == "explanation"


def test_route_after_evaluation_proceeds():
    state = create_initial_state("test")
    state["evaluation"] = {"should_regenerate": False}
    assert route_after_evaluation(state) == "explanation"


def test_build_regeneration_feedback_includes_failures():
    from backend.agents.base import build_regeneration_feedback

    state = create_initial_state("fix two sum")
    state["loop_count"] = 1
    state["optimized_code"] = "def broken(): pass"
    state["execution_result"] = {
        "stderr": "AssertionError: expected [0,1]",
        "test_results": [{"test_name": "test_two_sum", "status": "failed", "message": "assert"}],
    }
    state["evaluation"] = {"failed_tests": state["execution_result"]["test_results"]}
    feedback = build_regeneration_feedback(state)
    assert "REGENERATION ATTEMPT" in feedback
    assert "test_two_sum" in feedback
    assert "AssertionError" in feedback
