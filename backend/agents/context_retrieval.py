"""Agent 4: Context Retrieval Agent — local FAISS, no LLM call."""

from __future__ import annotations

import time

from backend.agents.base import append_timeline
from backend.models.state import CodeForgeState
from backend.tools.retriever import get_retriever


def _format_chunks_locally(chunks: list[dict]) -> dict:
    """Build context retrieval output from FAISS chunks without an LLM call."""
    if not chunks:
        return {
            "retrieval_performed": False,
            "query_used": "",
            "num_results": 0,
            "context_snippets": [],
            "patterns_identified": [],
            "context_summary": "No relevant context found in vector store.",
            "context_prompt_block": "",
        }

    patterns = []
    for c in chunks:
        tags = c.get("usage_note", "")
        if tags and tags not in patterns:
            patterns.append(tags)

    summary_parts = [f"{c.get('source', 'snippet')} (score {c.get('relevance_score', 0)})" for c in chunks]
    context_summary = "Retrieved reference patterns: " + ", ".join(summary_parts)

    snippet_lines = []
    for c in chunks:
        snippet_lines.append(
            f"--- {c.get('source')} [{c.get('language')}] ---\n{c.get('snippet', '')}\n"
        )

    context_prompt_block = (
        "RETRIEVED CONTEXT (optional reference — adapt, do not copy blindly):\n\n"
        f"{context_summary}\n\n"
        "REFERENCE SNIPPETS:\n" + "\n".join(snippet_lines)
    )

    return {
        "retrieval_performed": True,
        "query_used": "semantic + keyword",
        "num_results": len(chunks),
        "context_snippets": chunks,
        "patterns_identified": patterns,
        "context_summary": context_summary,
        "context_prompt_block": context_prompt_block,
    }


async def context_retrieval_node(state: CodeForgeState) -> CodeForgeState:
    """Retrieve context from FAISS locally — skips LLM to save rate limit budget."""
    start = time.time()
    agent_name = "context_retrieval"
    result = dict(state)
    result["current_agent"] = agent_name

    requirements = state.get("requirements", {})
    query = f"{requirements.get('title', '')} {requirements.get('summary', '')} {state.get('request', '')}"
    retriever = get_retriever()
    chunks = retriever.retrieve(query, language=state.get("language", ""), top_k=3)
    result["retrieved_context"] = _format_chunks_locally(chunks)

    duration = int((time.time() - start) * 1000)
    result["agent_timeline"] = append_timeline(
        state, agent_name, "completed",
        f"Retrieved {result['retrieved_context']['num_results']} snippets (local)",
        duration,
    )
    return CodeForgeState(**result)
