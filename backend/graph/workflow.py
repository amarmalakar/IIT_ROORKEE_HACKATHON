"""LangGraph workflow compilation and routing."""

from __future__ import annotations

from langgraph.graph import END, StateGraph

from backend.agents import (
    code_review_node,
    context_retrieval_node,
    documentation_node,
    evaluator_node,
    execution_node,
    explanation_node,
    language_specialist_node,
    optimization_node,
    persona_node,
    requirement_extraction_node,
    router_node,
    security_review_node,
    unit_test_generator_node,
)
from backend.models.state import CodeForgeState


def route_by_intent(state: CodeForgeState) -> str:
    """Conditional routing from Router based on detected intent."""
    intent = (state.get("router_output") or {}).get("intent", "full_pipeline")
    if intent == "explain":
        return "explanation"
    if intent == "review":
        return "code_review"
    if intent == "document":
        return "documentation"
    if intent == "unsupported":
        return "documentation"
    return "requirement_extraction"


def route_after_evaluation(state: CodeForgeState) -> str:
    """Regeneration loop — route back to codegen or optimization on FAIL (max 2 loops)."""
    evaluation = state.get("evaluation") or {}
    loop_count = state.get("loop_count", 0)
    if evaluation.get("should_regenerate") and loop_count < 2:
        agent = evaluation.get("regenerate_agent") or "language_specialist"
        if agent not in ("language_specialist", "optimization", "requirement_extraction"):
            agent = "language_specialist"
        return agent
    return "explanation"


def build_workflow() -> StateGraph:
    """Full 13-agent CodeForge AI pipeline with evaluator regeneration loop.

    START → router → requirement_extraction → persona → context_retrieval
      → language_specialist → optimization → code_review → security_review
      → unit_test_generator → execution → evaluator
      → [FAIL: loop back to language_specialist | optimization] (max 2 loops)
      → explanation → documentation → END
    """
    graph = StateGraph(CodeForgeState)

    graph.add_node("router", router_node)
    graph.add_node("requirement_extraction", requirement_extraction_node)
    graph.add_node("persona", persona_node)
    graph.add_node("context_retrieval", context_retrieval_node)
    graph.add_node("language_specialist", language_specialist_node)
    graph.add_node("optimization", optimization_node)
    graph.add_node("code_review", code_review_node)
    graph.add_node("security_review", security_review_node)
    graph.add_node("unit_test_generator", unit_test_generator_node)
    graph.add_node("execution", execution_node)
    graph.add_node("evaluator", evaluator_node)
    graph.add_node("explanation", explanation_node)
    graph.add_node("documentation", documentation_node)

    graph.set_entry_point("router")

    graph.add_conditional_edges(
        "router",
        route_by_intent,
        {
            "requirement_extraction": "requirement_extraction",
            "explanation": "explanation",
            "code_review": "code_review",
            "documentation": "documentation",
        },
    )

    graph.add_edge("requirement_extraction", "persona")
    graph.add_edge("persona", "context_retrieval")
    graph.add_edge("context_retrieval", "language_specialist")
    graph.add_edge("language_specialist", "optimization")
    graph.add_edge("optimization", "code_review")
    graph.add_edge("code_review", "security_review")
    graph.add_edge("security_review", "unit_test_generator")
    graph.add_edge("unit_test_generator", "execution")
    graph.add_edge("execution", "evaluator")

    graph.add_conditional_edges(
        "evaluator",
        route_after_evaluation,
        {
            "language_specialist": "language_specialist",
            "optimization": "optimization",
            "requirement_extraction": "requirement_extraction",
            "explanation": "explanation",
        },
    )

    graph.add_edge("explanation", "documentation")
    graph.add_edge("documentation", END)

    return graph


_compiled_graph = None


def get_compiled_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_workflow().compile()
    return _compiled_graph


async def run_workflow(
    request: str,
    persona_override: str = "",
    language_override: str = "",
    model_override: str = "",
) -> CodeForgeState:
    """Execute the full workflow and return final state."""
    from backend.models.state import create_initial_state

    graph = get_compiled_graph()
    initial = create_initial_state(request, persona_override, language_override, model_override)
    result = await graph.ainvoke(initial)
    return CodeForgeState(**result)
