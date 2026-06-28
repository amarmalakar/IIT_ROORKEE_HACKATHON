"""Agent 11: Evaluator Agent."""

from __future__ import annotations

from backend.agents.base import get_sanitized_code, run_llm_agent
from backend.models.agent_schemas import EvaluatorOutput
from backend.models.state import CodeForgeState
from backend.utils.helpers import safe_json_dumps, validate_agent_output


async def evaluator_node(state: CodeForgeState) -> CodeForgeState:
    def on_success(s: CodeForgeState, response: str) -> CodeForgeState:
        parsed = validate_agent_output(response, EvaluatorOutput)
        result = dict(s)
        result["evaluation"] = parsed.model_dump()
        if parsed.should_regenerate:
            result["loop_count"] = s.get("loop_count", 0) + 1
        return CodeForgeState(**result)

    optimization = state.get("optimization_report") or {}
    variables = {
        "requirements": safe_json_dumps(state.get("requirements", {})),
        "persona": state.get("persona", ""),
        "optimized_code": get_sanitized_code(state),
        "review_feedback": safe_json_dumps(state.get("review_report", {})),
        "security_report": safe_json_dumps(state.get("security_report", {})),
        "execution_result": safe_json_dumps(state.get("execution_result", {})),
        "complexity_analysis": safe_json_dumps(optimization),
    }
    return await run_llm_agent(state, "evaluator", variables, on_success)
