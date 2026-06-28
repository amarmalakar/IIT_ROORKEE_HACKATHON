"""Agent 3: Persona Agent."""

from __future__ import annotations

from backend.agents.base import run_llm_agent
from backend.models.agent_schemas import PersonaOutput
from backend.models.state import CodeForgeState
from backend.utils.helpers import get_persona_fallback, safe_json_dumps, validate_agent_output


async def persona_node(state: CodeForgeState) -> CodeForgeState:
    def on_success(s: CodeForgeState, response: str) -> CodeForgeState:
        parsed = validate_agent_output(response, PersonaOutput)
        result = dict(s)
        result["persona_instructions"] = parsed.model_dump()
        result["persona"] = parsed.persona
        return CodeForgeState(**result)

    variables = {
        "persona": state.get("persona", "mid_level_engineer"),
        "requirements": safe_json_dumps(state.get("requirements", {})),
        "user_request": state.get("request", ""),
    }
    result = await run_llm_agent(state, "persona", variables, on_success)
    if result.get("persona_instructions"):
        return result

    persona_id = state.get("persona", "mid_level_engineer")
    fallback = get_persona_fallback(persona_id)
    recovered = dict(result)
    recovered["persona"] = persona_id
    recovered["persona_instructions"] = fallback
    timeline = list(recovered.get("agent_timeline", []))
    if timeline and timeline[-1].get("agent") == "persona":
        timeline[-1] = {
            **timeline[-1],
            "status": "completed",
            "summary": f"Using built-in {persona_id} persona",
        }
    recovered["agent_timeline"] = timeline
    return CodeForgeState(**recovered)
