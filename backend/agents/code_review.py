"""Agent 7: Code Review Agent."""

from __future__ import annotations

from backend.agents.base import get_persona_block, run_llm_agent
from backend.models.agent_schemas import CodeReviewOutput
from backend.models.state import CodeForgeState
from backend.utils.helpers import safe_json_dumps, validate_agent_output


def _code_for_review(state: CodeForgeState) -> str:
    return state.get("optimized_code") or state.get("generated_code") or ""


async def code_review_node(state: CodeForgeState) -> CodeForgeState:
    def on_success(s: CodeForgeState, response: str) -> CodeForgeState:
        parsed = validate_agent_output(response, CodeReviewOutput)
        result = dict(s)
        result["review_report"] = parsed.model_dump()
        result["reviewed_code"] = parsed.reviewed_code or _code_for_review(s)
        return CodeForgeState(**result)

    variables = {
        "requirements": safe_json_dumps(state.get("requirements", {})),
        "language": state.get("language", "python"),
        "persona_prompt_block": get_persona_block(state),
        "optimized_code": _code_for_review(state),
    }
    result = await run_llm_agent(state, "code_review", variables, on_success)
    if result.get("reviewed_code"):
        return result

    code = _code_for_review(state)
    recovered = dict(result)
    recovered["reviewed_code"] = code
    recovered["optimized_code"] = code
    return CodeForgeState(**recovered)
