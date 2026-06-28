"""Agent 11: Evaluator Agent — deterministic quality gate (no LLM call)."""

from __future__ import annotations

import time

from backend.agents.base import append_timeline
from backend.models.state import CodeForgeState
from backend.services.evaluation import evaluate_execution


async def evaluator_node(state: CodeForgeState) -> CodeForgeState:
    """Evaluate execution results deterministically — drives regeneration loop without Groq calls."""
    start = time.time()
    agent_name = "evaluator"

    evaluation = evaluate_execution(state)

    result = dict(state)
    result["current_agent"] = agent_name
    result["evaluation"] = evaluation

    if evaluation.get("should_regenerate"):
        result["loop_count"] = state.get("loop_count", 0) + 1

    duration = int((time.time() - start) * 1000)
    loop_note = f" [loop {result['loop_count']}]" if evaluation.get("should_regenerate") else ""
    result["agent_timeline"] = append_timeline(
        state, agent_name, "completed",
        f"{evaluation.get('verdict', 'DONE')}: {evaluation.get('evaluation_summary', '')}{loop_note}",
        duration,
    )
    return CodeForgeState(**result)
