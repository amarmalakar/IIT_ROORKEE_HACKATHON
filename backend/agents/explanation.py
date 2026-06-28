"""Agent 12: Explanation Agent."""

from __future__ import annotations

from backend.agents.base import get_persona_block, get_sanitized_code, run_llm_agent
from backend.models.state import CodeForgeState
from backend.utils.helpers import safe_json_dumps


async def explanation_node(state: CodeForgeState) -> CodeForgeState:
    def on_success(s: CodeForgeState, response: str) -> CodeForgeState:
        result = dict(s)
        result["explanation"] = response
        return CodeForgeState(**result)

    variables = {
        "user_request": state.get("request", ""),
        "requirements": safe_json_dumps(state.get("requirements", {})),
        "persona_prompt_block": get_persona_block(state),
        "sanitized_code": get_sanitized_code(state),
        "optimization_output": safe_json_dumps(state.get("optimization_report", {})),
        "evaluation": safe_json_dumps(state.get("evaluation", {})),
    }
    return await run_llm_agent(state, "explanation", variables, on_success)
