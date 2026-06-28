"""LangGraph shared state for CodeForge AI."""

from __future__ import annotations

from typing import Any, TypedDict


class CodeForgeState(TypedDict, total=False):
    """Strongly typed state passed between LangGraph agent nodes."""

    request: str
    persona: str
    language: str
    persona_override: str
    language_override: str
    model_override: str
    router_output: dict[str, Any]
    requirements: dict[str, Any]
    persona_instructions: dict[str, Any]
    retrieved_context: dict[str, Any]
    generated_code: str
    optimized_code: str
    optimization_report: dict[str, Any]
    reviewed_code: str
    review_report: dict[str, Any]
    security_report: dict[str, Any]
    tests: str
    test_metadata: dict[str, Any]
    execution_result: dict[str, Any]
    evaluation: dict[str, Any]
    explanation: str
    documentation: dict[str, Any]
    agent_timeline: list[dict[str, Any]]
    errors: list[dict[str, Any]]
    current_agent: str
    loop_count: int
    metadata: dict[str, Any]


def create_initial_state(
    request: str,
    persona_override: str = "",
    language_override: str = "",
    model_override: str = "",
) -> CodeForgeState:
    """Create a fresh graph state for a new workflow run."""
    return CodeForgeState(
        request=request,
        persona=persona_override or "mid_level_engineer",
        language=language_override or "python",
        persona_override=persona_override,
        language_override=language_override,
        model_override=model_override,
        router_output={},
        requirements={},
        persona_instructions={},
        retrieved_context={},
        generated_code="",
        optimized_code="",
        optimization_report={},
        reviewed_code="",
        review_report={},
        security_report={},
        tests="",
        test_metadata={},
        execution_result={},
        evaluation={},
        explanation="",
        documentation={},
        agent_timeline=[],
        errors=[],
        current_agent="",
        loop_count=0,
        metadata={},
    )
