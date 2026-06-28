"""Tests for LangGraph workflow routing."""

from backend.graph.workflow import route_by_intent, build_workflow
from backend.models.state import create_initial_state


def test_route_by_intent_full_pipeline():
    state = create_initial_state("build me an API")
    state["router_output"] = {"intent": "full_pipeline"}
    assert route_by_intent(state) == "requirement_extraction"


def test_route_by_intent_explain():
    state = create_initial_state("explain this code")
    state["router_output"] = {"intent": "explain"}
    assert route_by_intent(state) == "explanation"


def test_route_by_intent_review():
    state = create_initial_state("review my code")
    state["router_output"] = {"intent": "review"}
    assert route_by_intent(state) == "code_review"


def test_route_by_intent_document_goes_to_explanation():
    state = create_initial_state("document this")
    state["router_output"] = {"intent": "document"}
    assert route_by_intent(state) == "explanation"


def test_build_workflow_compiles():
    graph = build_workflow()
    assert graph is not None
