"""Agent 4: Context Retrieval Agent."""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone

from backend.agents.base import append_error, append_timeline
from backend.models.agent_schemas import ContextRetrievalOutput
from backend.models.state import CodeForgeState
from backend.services.llm import get_llm_service
from backend.tools.retriever import get_retriever
from backend.utils.helpers import safe_json_dumps, validate_agent_output


async def context_retrieval_node(state: CodeForgeState) -> CodeForgeState:
    start = time.time()
    agent_name = "context_retrieval"
    result = dict(state)
    result["current_agent"] = agent_name

    try:
        requirements = state.get("requirements", {})
        query = f"{requirements.get('title', '')} {requirements.get('summary', '')} {state.get('request', '')}"
        retriever = get_retriever()
        chunks = retriever.retrieve(query, language=state.get("language", ""), top_k=3)

        llm = get_llm_service()
        variables = {
            "user_request": state.get("request", ""),
            "requirements": safe_json_dumps(requirements),
            "language": state.get("language", ""),
            "persona": state.get("persona", ""),
            "retrieved_chunks": json.dumps(chunks, indent=2),
        }
        response = await llm.invoke_with_retry(
            agent_name, variables,
            language=state.get("language", ""),
            persona=state.get("persona", ""),
            model_override=state.get("model_override", ""),
        )
        parsed = validate_agent_output(response, ContextRetrievalOutput)
        result["retrieved_context"] = parsed.model_dump()
        duration = int((time.time() - start) * 1000)
        result["agent_timeline"] = append_timeline(
            state, agent_name, "completed",
            f"Retrieved {parsed.num_results} snippets", duration
        )
    except Exception as exc:
        result["retrieved_context"] = {
            "retrieval_performed": False,
            "context_summary": "Retrieval skipped due to error",
            "context_prompt_block": "",
            "context_snippets": [],
        }
        result["errors"] = append_error(state, agent_name, str(exc))
        result["agent_timeline"] = append_timeline(state, agent_name, "error", str(exc))

    return CodeForgeState(**result)
