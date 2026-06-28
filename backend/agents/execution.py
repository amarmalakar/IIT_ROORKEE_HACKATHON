"""Agent 10: Execution Agent."""

from __future__ import annotations

import time

from backend.agents.base import append_error, append_timeline, get_sanitized_code
from backend.models.state import CodeForgeState
from backend.tools.repl import execute_code


async def execution_node(state: CodeForgeState) -> CodeForgeState:
    start = time.time()
    agent_name = "execution"
    result = dict(state)
    result["current_agent"] = agent_name

    try:
        code = get_sanitized_code(state)
        tests = state.get("tests", "")
        language = state.get("language", "python")
        exec_result = execute_code(language, code, tests)
        result["execution_result"] = exec_result
        duration = int((time.time() - start) * 1000)
        result["agent_timeline"] = append_timeline(
            state, agent_name, "completed",
            f"Status: {exec_result.get('execution_status')}", duration
        )
    except Exception as exc:
        result["execution_result"] = {
            "execution_status": "error",
            "language": state.get("language", ""),
            "sandbox_notes": str(exc),
        }
        result["errors"] = append_error(state, agent_name, str(exc))
        result["agent_timeline"] = append_timeline(state, agent_name, "error", str(exc))

    return CodeForgeState(**result)
