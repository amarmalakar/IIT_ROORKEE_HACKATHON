"""Agent 5: Language Specialist Agent."""

from __future__ import annotations

from backend.agents.base import get_persona_block, run_llm_agent
from backend.models.state import CodeForgeState
from backend.utils.helpers import extract_code_block, safe_json_dumps


async def language_specialist_node(state: CodeForgeState) -> CodeForgeState:
    def on_success(s: CodeForgeState, response: str) -> CodeForgeState:
        result = dict(s)
        language = s.get("language", "python")
        code = extract_code_block(response, language)
        if not code:
            code = extract_code_block(response)
        code = code or response
        result["generated_code"] = code
        result["optimized_code"] = code
        return CodeForgeState(**result)

    variables = {
        "user_request": state.get("request", ""),
        "requirements": safe_json_dumps(state.get("requirements", {})),
        "language": state.get("language", "python"),
        "persona_prompt_block": get_persona_block(state),
        "context_prompt_block": "",
    }
    return await run_llm_agent(state, "language_specialist", variables, on_success)
