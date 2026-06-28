"""LangGraph workflow compilation and routing."""

from __future__ import annotations

from langgraph.graph import END, StateGraph

from backend.agents import (
    code_review_node,
    execution_node,
    explanation_node,
    language_specialist_node,
    persona_node,
    requirement_extraction_node,
    router_node,
)
from backend.models.state import CodeForgeState


def route_by_intent(state: CodeForgeState) -> str:
    """Conditional routing from Router based on detected intent."""
    intent = (state.get("router_output") or {}).get("intent", "full_pipeline")
    if intent == "explain":
        return "explanation"
    if intent == "review":
        return "code_review"
    if intent in ("document", "unsupported"):
        return "explanation"
    return "requirement_extraction"


def build_workflow() -> StateGraph:
    """Compile the streamlined CodeForge AI LangGraph workflow.

    Fast path (7 agents): router → requirements → persona → codegen → review
    → execution → explanation. Skips context retrieval (embeddings), optimization,
    security review, test generation, evaluator loop, and documentation agents.
    """
    graph = StateGraph(CodeForgeState)

    graph.add_node("router", router_node)
    graph.add_node("requirement_extraction", requirement_extraction_node)
    graph.add_node("persona", persona_node)
    graph.add_node("language_specialist", language_specialist_node)
    graph.add_node("code_review", code_review_node)
    graph.add_node("execution", execution_node)
    graph.add_node("explanation", explanation_node)

    graph.set_entry_point("router")

    graph.add_conditional_edges(
        "router",
        route_by_intent,
        {
            "requirement_extraction": "requirement_extraction",
            "explanation": "explanation",
            "code_review": "code_review",
        },
    )

    graph.add_edge("requirement_extraction", "persona")
    graph.add_edge("persona", "language_specialist")
    graph.add_edge("language_specialist", "code_review")
    graph.add_edge("code_review", "execution")
    graph.add_edge("execution", "explanation")
    graph.add_edge("explanation", END)

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
