"""Utility helpers for CodeForge AI."""

import json
import logging
import re
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)

logger = logging.getLogger("codeforge")


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def extract_json_from_text(text: str) -> dict[str, Any]:
    """Extract JSON object from LLM response, handling markdown fences."""
    text = text.strip()
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fence_match:
        text = fence_match.group(1).strip()
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", " ", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        brace_match = re.search(r"\{[\s\S]*\}", text)
        if brace_match:
            cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", " ", brace_match.group())
            return json.loads(cleaned)
        raise


def extract_code_block(text: str, language: str = "") -> str:
    """Extract the primary code block from markdown response."""
    if not text or not text.strip():
        return ""
    pattern = rf"```(?:{language})?\s*([\s\S]*?)```" if language else r"```(?:\w+)?\s*([\s\S]*?)```"
    matches = re.findall(pattern, text)
    if not matches:
        return _strip_stray_fences(text.strip())
    return max(matches, key=len).strip()


def sanitize_executable_code(text: str, language: str = "python") -> str:
    """Prepare LLM output for subprocess execution by stripping markdown wrappers."""
    if not text or not text.strip():
        return ""
    cleaned = extract_code_block(text, language)
    if not cleaned:
        cleaned = extract_code_block(text)
    return _strip_stray_fences(cleaned)


def _strip_stray_fences(text: str) -> str:
    """Remove leftover markdown fence lines from code text."""
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def validate_agent_output(text: str, schema: type[T]) -> T:
    """Parse and validate LLM output against a Pydantic schema."""
    data = extract_json_from_text(text)
    return schema.model_validate(data)


def safe_json_dumps(obj: Any) -> str:
    return json.dumps(obj, indent=2, default=str)


def truncate_text(text: str, max_len: int = 10000) -> str:
    if len(text) <= max_len:
        return text
    return text[:max_len] + "\n[truncated]"


PERSONA_FALLBACK_BLOCKS: dict[str, str] = {
    "interview_preparation": (
        "ACTIVE PERSONA: Interview Preparation\n"
        "- Present brute force then optimal solution\n"
        "- Include complexity analysis and dry run"
    ),
    "product_ready_engineer": (
        "ACTIVE PERSONA: Product Ready Engineer\n"
        "- Production-grade code with error handling and logging\n"
        "- SOLID principles and input validation"
    ),
    "beginner_developer": (
        "ACTIVE PERSONA: Beginner Developer\n"
        "- Simple readable code with clear variable names\n"
        "- Step-by-step comments"
    ),
    "mid_level_engineer": (
        "ACTIVE PERSONA: Mid-Level Engineer\n"
        "- Clean code with type hints\n"
        "- Handle edge cases and include brief docstrings"
    ),
    "senior_engineer": (
        "ACTIVE PERSONA: Senior Engineer\n"
        "- Maintainable design with clear abstractions\n"
        "- Performance-conscious implementation"
    ),
    "principal_engineer": (
        "ACTIVE PERSONA: Principal Engineer\n"
        "- Scalable architecture and extensibility\n"
        "- Document trade-offs"
    ),
    "competitive_programmer": (
        "ACTIVE PERSONA: Competitive Programmer\n"
        "- Fastest algorithm with minimal memory\n"
        "- Concise implementation"
    ),
    "data_engineer": (
        "ACTIVE PERSONA: Data Engineer\n"
        "- Efficient data pipelines and SQL best practices\n"
        "- Handle large-scale data patterns"
    ),
    "ai_engineer": (
        "ACTIVE PERSONA: AI Engineer\n"
        "- Clean ML/LLM integration patterns\n"
        "- Reproducible and testable code"
    ),
    "code_mentor": (
        "ACTIVE PERSONA: Code Mentor\n"
        "- Educational explanations alongside code\n"
        "- Highlight learning points"
    ),
}


def get_persona_fallback(persona_id: str) -> dict[str, str]:
    block = PERSONA_FALLBACK_BLOCKS.get(
        persona_id, PERSONA_FALLBACK_BLOCKS["mid_level_engineer"]
    )
    return {
        "persona": persona_id,
        "persona_prompt_block": block,
        "code_style_notes": block,
        "review_standards": "Standard quality checks",
        "testing_strategy": "Cover main cases and edge cases",
        "explanation_style": "Clear and concise",
        "documentation_level": "standard",
    }
