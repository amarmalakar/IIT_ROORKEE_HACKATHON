"""Tests for utility helpers."""

import pytest

from backend.utils.helpers import extract_json_from_text, extract_code_block, get_persona_fallback, validate_agent_output
from backend.models.agent_schemas import RouterOutput


def test_extract_json_from_fenced_block():
    text = '```json\n{"language": "python", "intent": "generate"}\n```'
    result = extract_json_from_text(text)
    assert result["language"] == "python"


def test_extract_json_raw():
    text = '{"language": "java", "intent": "review"}'
    result = extract_json_from_text(text)
    assert result["intent"] == "review"


def test_extract_code_block():
    text = '## Code\n```python\ndef hello():\n    return "world"\n```'
    code = extract_code_block(text, "python")
    assert "def hello" in code


def test_validate_agent_output():
    text = """{
        "language": "python",
        "language_confidence": 0.9,
        "intent": "full_pipeline",
        "persona": "mid_level_engineer",
        "routing_rationale": "test"
    }"""
    result = validate_agent_output(text, RouterOutput)
    assert result.language == "python"


def test_extract_json_strips_control_chars():
    text = '{"language": "python", "intent": "generate\x0b"}'
    result = extract_json_from_text(text)
    assert result["language"] == "python"


def test_get_persona_fallback():
    block = get_persona_fallback("interview_preparation")
    assert block["persona"] == "interview_preparation"
    assert "Interview Preparation" in block["persona_prompt_block"]
