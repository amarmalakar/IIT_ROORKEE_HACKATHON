"""Agent 2: Requirement Extraction Agent."""

from __future__ import annotations

from backend.agents.base import format_router_output, run_llm_agent
from backend.models.agent_schemas import RequirementExtractionOutput
from backend.models.state import CodeForgeState
from backend.utils.helpers import validate_agent_output


async def requirement_extraction_node(state: CodeForgeState) -> CodeForgeState:
    def on_success(s: CodeForgeState, response: str) -> CodeForgeState:
        parsed = validate_agent_output(response, RequirementExtractionOutput)
        result = dict(s)
        result["requirements"] = parsed.model_dump()
        return CodeForgeState(**result)

    variables = {
        "user_request": state.get("request", ""),
        "router_output": format_router_output(state.get("router_output", {})),
        "language": state.get("language", "python"),
        "persona": state.get("persona", ""),
    }
    return await run_llm_agent(state, "requirement_extraction", variables, on_success)
