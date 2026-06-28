"""Agent 9: Unit Test Generator Agent."""

from __future__ import annotations

from backend.agents.base import get_persona_block, get_sanitized_code, run_llm_agent
from backend.models.agent_schemas import UnitTestOutput
from backend.models.state import CodeForgeState
from backend.utils.helpers import extract_code_block, extract_json_from_text, safe_json_dumps


async def unit_test_generator_node(state: CodeForgeState) -> CodeForgeState:
    def on_success(s: CodeForgeState, response: str) -> CodeForgeState:
        result = dict(s)
        language = s.get("language", "python")
        tests = extract_code_block(response, language)
        if not tests:
            tests = extract_code_block(response)
        result["tests"] = tests or response
        try:
            meta = extract_json_from_text(response)
            result["test_metadata"] = UnitTestOutput.model_validate(meta).model_dump()
        except Exception:
            result["test_metadata"] = {"framework": "pytest", "total_tests": 0, "runnable": True}
        return CodeForgeState(**result)

    variables = {
        "requirements": safe_json_dumps(state.get("requirements", {})),
        "language": state.get("language", "python"),
        "persona_prompt_block": get_persona_block(state),
        "sanitized_code": get_sanitized_code(state),
    }
    return await run_llm_agent(state, "unit_test_generator", variables, on_success)
