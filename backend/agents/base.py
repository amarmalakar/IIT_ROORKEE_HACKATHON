"""Base utilities for LangGraph agent nodes."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable

from backend.models.state import CodeForgeState
from backend.services.llm import get_llm_service
from backend.utils.helpers import safe_json_dumps


def append_timeline(
    state: CodeForgeState,
    agent: str,
    status: str,
    summary: str = "",
    duration_ms: int = 0,
) -> list[dict[str, Any]]:
    timeline = list(state.get("agent_timeline", []))
    timeline.append({
        "agent": agent,
        "status": status,
        "summary": summary,
        "duration_ms": duration_ms,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    return timeline


def append_error(state: CodeForgeState, agent: str, error: str) -> list[dict[str, Any]]:
    errors = list(state.get("errors", []))
    errors.append({
        "agent": agent,
        "error": error,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    return errors


def get_persona_block(state: CodeForgeState) -> str:
    instructions = state.get("persona_instructions") or {}
    return instructions.get("persona_prompt_block", "")


def get_sanitized_code(state: CodeForgeState) -> str:
    security = state.get("security_report") or {}
    if security.get("sanitized_code"):
        return security["sanitized_code"]
    reviewed = state.get("reviewed_code") or ""
    if reviewed:
        return reviewed
    return state.get("optimized_code") or state.get("generated_code") or ""


async def run_llm_agent(
    state: CodeForgeState,
    agent_name: str,
    variables: dict[str, Any],
    on_success: Callable[[CodeForgeState, str], CodeForgeState],
) -> CodeForgeState:
    """Generic LLM agent runner with timeline and error tracking."""
    import time

    start = time.time()
    llm = get_llm_service()
    try:
        response = await llm.invoke_with_retry(
            agent_name,
            variables,
            language=state.get("language", ""),
            persona=state.get("persona", ""),
            model_override=state.get("model_override", ""),
        )
        duration = int((time.time() - start) * 1000)
        result = on_success(state, response)
        result["current_agent"] = agent_name
        result["agent_timeline"] = append_timeline(
            state, agent_name, "completed", f"{agent_name} finished", duration
        )
        return result
    except Exception as exc:
        result = dict(state)
        result["current_agent"] = agent_name
        result["errors"] = append_error(state, agent_name, str(exc))
        result["agent_timeline"] = append_timeline(
            state, agent_name, "error", str(exc)
        )
        return CodeForgeState(**result)


def format_router_output(router_output: dict) -> str:
    return safe_json_dumps(router_output)
