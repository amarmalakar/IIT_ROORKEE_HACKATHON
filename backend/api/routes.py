"""FastAPI REST routes."""

from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from backend.config.settings import LANGUAGES, PERSONAS, WORKFLOW_EDGES, WORKFLOW_NODES
from backend.graph.workflow import run_workflow
from backend.models.api_schemas import (
    EvaluateRequest,
    GenerateRequest,
    GenerateResponse,
    ReviewRequest,
    TestRequest,
    WorkflowResponse,
)
from backend.models.state import create_initial_state
from backend.services.llm import list_models
from backend.tools.repl import execute_code

router = APIRouter()


@router.post("/generate", response_model=GenerateResponse)
async def generate_code(body: GenerateRequest) -> GenerateResponse:
    """Run the full multi-agent code generation pipeline."""
    try:
        state = await run_workflow(
            request=body.request,
            persona_override=body.persona,
            language_override=body.language,
            model_override=body.model,
        )
        return GenerateResponse(success=True, state=dict(state), message="Pipeline completed")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/review")
async def review_code(body: ReviewRequest) -> dict[str, Any]:
    """Run code review and security review on provided code."""
    from backend.agents.code_review import code_review_node
    from backend.agents.security_review import security_review_node

    state = create_initial_state(body.request, body.persona, body.language)
    state["optimized_code"] = body.code
    state["reviewed_code"] = body.code
    state["requirements"] = {"title": "Code Review", "summary": body.request, "language": body.language}
    state = await code_review_node(state)
    state = await security_review_node(state)
    return {
        "review_report": state.get("review_report", {}),
        "security_report": state.get("security_report", {}),
        "reviewed_code": state.get("reviewed_code", body.code),
    }


@router.post("/test")
async def generate_and_run_tests(body: TestRequest) -> dict[str, Any]:
    """Generate tests and execute code."""
    from backend.agents.unit_test_generator import unit_test_generator_node
    from backend.agents.execution import execution_node

    state = create_initial_state(body.request, body.persona, body.language)
    state["optimized_code"] = body.code
    state["reviewed_code"] = body.code
    state["requirements"] = {"title": "Test Generation", "summary": body.request, "language": body.language}
    state = await unit_test_generator_node(state)
    state = await execution_node(state)
    return {
        "tests": state.get("tests", ""),
        "test_metadata": state.get("test_metadata", {}),
        "execution_result": state.get("execution_result", {}),
    }


@router.post("/evaluate")
async def evaluate_solution(body: EvaluateRequest) -> dict[str, Any]:
    """Evaluate provided code and optional tests."""
    from backend.agents.evaluator import evaluator_node
    from backend.agents.execution import execution_node

    state = create_initial_state(body.request, body.persona, body.language)
    state["optimized_code"] = body.code
    state["reviewed_code"] = body.code
    state["tests"] = body.tests
    state["requirements"] = {"title": "Evaluation", "summary": body.request, "language": body.language}
    if body.tests:
        state = await execution_node(state)
    else:
        state["execution_result"] = execute_code(body.language, body.code)
    state = await evaluator_node(state)
    return {"evaluation": state.get("evaluation", {})}


@router.get("/persona")
async def list_personas() -> list[dict[str, str]]:
    return PERSONAS


@router.get("/workflow", response_model=WorkflowResponse)
async def get_workflow() -> WorkflowResponse:
    return WorkflowResponse(nodes=WORKFLOW_NODES, edges=WORKFLOW_EDGES)


@router.get("/models")
async def get_models() -> list[dict[str, object]]:
    return list_models()


@router.get("/languages")
async def get_languages() -> list[dict[str, str]]:
    return LANGUAGES


@router.get("/download/{artifact}")
async def download_artifact(artifact: str, request: str = "") -> PlainTextResponse:
    """Download generated artifacts. Requires prior /generate call stored in session — returns template for demo."""
    templates: dict[str, str] = {
        "code": "# Run POST /generate first to get code\n",
        "tests": "# Run POST /generate first to get tests\n",
        "readme": "# CodeForge AI\n\nRun the generation pipeline to produce README content.\n",
    }
    content = templates.get(artifact, f"Unknown artifact: {artifact}")
    filename = {"code": "solution.py", "tests": "test_solution.py", "readme": "README.md"}.get(
        artifact, f"{artifact}.txt"
    )
    return PlainTextResponse(
        content=content,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/download/state")
async def download_from_state(body: dict[str, Any]) -> PlainTextResponse:
    """Download artifact from a completed workflow state."""
    artifact = body.get("artifact", "code")
    state = body.get("state", {})
    mapping = {
        "code": state.get("optimized_code") or state.get("generated_code", ""),
        "tests": state.get("tests", ""),
        "readme": (state.get("documentation") or {}).get("readme", ""),
        "explanation": state.get("explanation", ""),
    }
    content = mapping.get(artifact, "")
    if not content:
        raise HTTPException(status_code=404, detail=f"Artifact '{artifact}' not found in state")
    filename = {"code": "solution.py", "tests": "test_solution.py", "readme": "README.md"}.get(
        artifact, f"{artifact}.md"
    )
    return PlainTextResponse(
        content=content,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
