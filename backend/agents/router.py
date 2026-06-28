"""Agent 1: Router Agent."""

from __future__ import annotations

from backend.agents.base import append_timeline, run_llm_agent
from backend.models.agent_schemas import RouterOutput
from backend.models.state import CodeForgeState
from backend.utils.helpers import validate_agent_output


async def router_node(state: CodeForgeState) -> CodeForgeState:
    def on_success(s: CodeForgeState, response: str) -> CodeForgeState:
        parsed = validate_agent_output(response, RouterOutput)
        output = parsed.model_dump()
        result = dict(s)
        result["router_output"] = output
        result["language"] = s.get("language_override") or output["language"]
        result["persona"] = s.get("persona_override") or output["persona"]
        return CodeForgeState(**result)

    variables = {
        "user_request": state.get("request", ""),
        "persona_override": state.get("persona_override", ""),
        "language_override": state.get("language_override", ""),
    }
    result = await run_llm_agent(state, "router", variables, on_success)
    if result.get("router_output"):
        result["agent_timeline"] = append_timeline(
            result, "router", "completed",
            f"Routed: {result['router_output'].get('intent')} / {result['language']}"
        )
    return result
