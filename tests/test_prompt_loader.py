"""Tests for prompt template loader."""

import pytest

from backend.prompts.loader import PromptLoader, AGENT_TEMPLATE_MAP


@pytest.fixture
def loader():
    return PromptLoader()


def test_all_agent_templates_exist(loader):
    for agent, filename in AGENT_TEMPLATE_MAP.items():
        content = loader.load_template(filename)
        assert len(content) > 100, f"Template for {agent} is too short"


def test_system_prompt_loads(loader):
    content = loader.load_system_prompt()
    assert "CodeForge AI" in content


def test_variable_injection(loader):
    template = "User Request: {user_request}\nLanguage: {language}"
    result = loader.inject_variables(template, {
        "user_request": "build a REST API",
        "language": "python",
    })
    assert "build a REST API" in result
    assert "python" in result


def test_build_messages(loader):
    messages = loader.build_messages(
        "router",
        {"user_request": "hello", "persona_override": "", "language_override": ""},
        language="python",
        persona="mid_level_engineer",
    )
    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert "hello" in messages[1]["content"]


def test_persona_modifiers_load(loader):
    content = loader.load_persona_modifiers()
    assert "Interview Preparation" in content
