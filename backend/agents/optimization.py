"""Agent 6: Optimization Agent (mandatory)."""

from __future__ import annotations

from backend.agents.base import get_persona_block, run_llm_agent
from backend.models.agent_schemas import OptimizationReport
from backend.models.state import CodeForgeState
from backend.utils.helpers import extract_code_block, extract_json_from_text, safe_json_dumps


async def optimization_node(state: CodeForgeState) -> CodeForgeState:
    def on_success(s: CodeForgeState, response: str) -> CodeForgeState:
        result = dict(s)
        language = s.get("language", "python")
        code = extract_code_block(response, language)
        if not code:
            sections = response.split("## Final Code")
            if len(sections) > 1:
                code = extract_code_block(sections[-1], language)
            else:
                code = extract_code_block(response)
        result["optimized_code"] = code or s.get("generated_code", "")
        try:
            report_data = extract_json_from_text(response)
            result["optimization_report"] = OptimizationReport.model_validate(report_data).model_dump()
        except Exception:
            result["optimization_report"] = {
                "selected_approach": "optimized",
                "time_complexity": "unknown",
                "space_complexity": "unknown",
                "regenerated": False,
                "improvement_over_initial": "See optimization output",
            }
        return CodeForgeState(**result)

    variables = {
        "requirements": safe_json_dumps(state.get("requirements", {})),
        "language": state.get("language", "python"),
        "persona_prompt_block": get_persona_block(state),
        "generated_code": state.get("generated_code", ""),
    }
    return await run_llm_agent(state, "optimization", variables, on_success)
