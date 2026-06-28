"""Agent 5: Language Specialist Agent."""

from __future__ import annotations

from backend.agents.base import append_timeline, build_regeneration_feedback, get_persona_block, run_llm_agent
from backend.models.state import CodeForgeState
from backend.utils.helpers import extract_code_block, safe_json_dumps


async def language_specialist_node(state: CodeForgeState) -> CodeForgeState:
    loop_count = state.get("loop_count", 0)
    is_retry = loop_count > 0

    def on_success(s: CodeForgeState, response: str) -> CodeForgeState:
        result = dict(s)
        language = s.get("language", "python")
        code = extract_code_block(response, language)
        if not code:
            code = extract_code_block(response)
        result["generated_code"] = code or response
        return CodeForgeState(**result)

    feedback = build_regeneration_feedback(state)
    user_request = state.get("request", "")
    if feedback:
        user_request = f"{user_request}\n\n---\n\n{feedback}"

    retrieved = state.get("retrieved_context") or {}
    context_block = retrieved.get("context_prompt_block", "") if not is_retry else feedback

    variables = {
        "user_request": user_request,
        "requirements": safe_json_dumps(state.get("requirements", {})),
        "language": state.get("language", "python"),
        "persona_prompt_block": get_persona_block(state),
        "context_prompt_block": context_block,
    }

    result = await run_llm_agent(state, "language_specialist", variables, on_success)

    if is_retry:
        result["agent_timeline"] = append_timeline(
            state, "language_specialist", "completed",
            f"Regenerated code — loop {loop_count}",
        )

    return result
