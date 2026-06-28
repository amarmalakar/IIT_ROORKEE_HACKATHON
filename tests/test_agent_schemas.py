"""Tests for Pydantic agent schemas."""

import pytest
from pydantic import ValidationError

from backend.models.agent_schemas import (
    RouterOutput,
    EvaluatorOutput,
    SecurityReviewOutput,
    CodeReviewOutput,
    RequirementExtractionOutput,
)
from backend.models.state import create_initial_state


def test_router_output_valid():
    data = RouterOutput(
        language="python",
        language_confidence=0.95,
        intent="full_pipeline",
        persona="mid_level_engineer",
        persona_confidence=0.88,
        routing_rationale="test",
    )
    assert data.language == "python"


def test_router_output_invalid_confidence():
    with pytest.raises(ValidationError):
        RouterOutput(
            language="python",
            language_confidence=1.5,
            intent="generate",
            persona="beginner",
        )


def test_evaluator_output():
    ev = EvaluatorOutput(
        verdict="PASS",
        confidence_score=0.91,
        evaluation_summary="All good",
    )
    assert ev.verdict == "PASS"
    assert not ev.should_regenerate


def test_security_review_output():
    sr = SecurityReviewOutput(
        security_score=95,
        verdict="PASS",
        security_report_summary="No issues",
    )
    assert sr.verdict == "PASS"


def test_code_review_output():
    cr = CodeReviewOutput(
        overall_score=85,
        verdict="APPROVE",
        summary="Looks good",
    )
    assert cr.verdict == "APPROVE"


def test_requirement_extraction_output():
    req = RequirementExtractionOutput(
        title="Two Sum",
        summary="Find two numbers",
        language="python",
        functional_requirements=["Find indices"],
    )
    assert req.title == "Two Sum"


def test_create_initial_state():
    state = create_initial_state("hello world", persona_override="senior_engineer")
    assert state["request"] == "hello world"
    assert state["persona"] == "senior_engineer"
    assert state["loop_count"] == 0
    assert state["agent_timeline"] == []
