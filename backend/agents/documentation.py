"""Agent 13: Documentation Agent."""

from __future__ import annotations

from backend.agents.base import get_sanitized_code, run_llm_agent
from backend.models.agent_schemas import DocumentationOutput
from backend.models.state import CodeForgeState
from backend.utils.helpers import safe_json_dumps, validate_agent_output


async def documentation_node(state: CodeForgeState) -> CodeForgeState:
    def on_success(s: CodeForgeState, response: str) -> CodeForgeState:
        parsed = validate_agent_output(response, DocumentationOutput)
        result = dict(s)
        result["documentation"] = parsed.model_dump()
        return CodeForgeState(**result)

    router = state.get("router_output") or {}
    variables = {
        "user_request": state.get("request", ""),
        "requirements": safe_json_dumps(state.get("requirements", {})),
        "persona": state.get("persona", ""),
        "sanitized_code": get_sanitized_code(state),
        "tests": state.get("tests", ""),
        "explanation": state.get("explanation", ""),
        "evaluation": safe_json_dumps(state.get("evaluation", {})),
        "workflow": safe_json_dumps(router.get("workflow", [])),
    }
    return await run_llm_agent(state, "documentation", variables, on_success)
