"""Agent 8: Security Review Agent."""

from __future__ import annotations

from backend.agents.base import run_llm_agent
from backend.models.agent_schemas import SecurityReviewOutput
from backend.models.state import CodeForgeState
from backend.utils.helpers import safe_json_dumps, validate_agent_output


async def security_review_node(state: CodeForgeState) -> CodeForgeState:
    def on_success(s: CodeForgeState, response: str) -> CodeForgeState:
        parsed = validate_agent_output(response, SecurityReviewOutput)
        result = dict(s)
        result["security_report"] = parsed.model_dump()
        if parsed.sanitized_code:
            result["reviewed_code"] = parsed.sanitized_code
        return CodeForgeState(**result)

    variables = {
        "requirements": safe_json_dumps(state.get("requirements", {})),
        "language": state.get("language", "python"),
        "reviewed_code": state.get("reviewed_code") or state.get("optimized_code", ""),
    }
    return await run_llm_agent(state, "security_review", variables, on_success)
