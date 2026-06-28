"""Prompt template loading and variable injection."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from backend.config.settings import PROMPTS_DIR

AGENT_TEMPLATE_MAP: dict[str, str] = {
    "router": "router_agent.md",
    "requirement_extraction": "requirement_extraction_agent.md",
    "persona": "persona_agent.md",
    "context_retrieval": "context_retrieval_agent.md",
    "language_specialist": "language_specialist_agent.md",
    "optimization": "optimization_agent.md",
    "code_review": "code_review_agent.md",
    "security_review": "security_review_agent.md",
    "unit_test_generator": "unit_test_generator_agent.md",
    "execution": "execution_agent.md",
    "evaluator": "evaluator_agent.md",
    "explanation": "explanation_agent.md",
    "documentation": "documentation_agent.md",
}

AGENT_VARIABLES: dict[str, list[str]] = {
    "router": ["user_request", "persona_override", "language_override"],
    "requirement_extraction": ["user_request", "router_output", "language", "persona"],
    "persona": ["persona", "requirements", "user_request"],
    "context_retrieval": ["user_request", "requirements", "language", "persona", "retrieved_chunks"],
    "language_specialist": [
        "user_request", "requirements", "language", "persona_prompt_block", "context_prompt_block",
    ],
    "optimization": ["requirements", "language", "persona_prompt_block", "generated_code"],
    "code_review": ["requirements", "language", "persona_prompt_block", "optimized_code"],
    "security_review": ["requirements", "language", "reviewed_code"],
    "unit_test_generator": ["requirements", "language", "persona_prompt_block", "sanitized_code"],
    "execution": ["language", "sanitized_code", "tests", "environment_info"],
    "evaluator": [
        "requirements", "persona", "optimized_code", "review_feedback",
        "security_report", "execution_result", "complexity_analysis",
    ],
    "explanation": [
        "user_request", "requirements", "persona_prompt_block", "sanitized_code",
        "optimization_output", "evaluation",
    ],
    "documentation": [
        "user_request", "requirements", "persona", "sanitized_code",
        "tests", "explanation", "evaluation", "workflow",
    ],
}


class PromptLoader:
    """Load Markdown prompt templates and inject runtime variables."""

    def __init__(self, prompts_dir: Path | None = None) -> None:
        self.prompts_dir = prompts_dir or PROMPTS_DIR
        self._cache: dict[str, str] = {}

    def load_template(self, filename: str) -> str:
        if filename not in self._cache:
            path = self.prompts_dir / filename
            if not path.exists():
                raise FileNotFoundError(f"Prompt template not found: {path}")
            self._cache[filename] = path.read_text(encoding="utf-8")
        return self._cache[filename]

    def load_system_prompt(self) -> str:
        return self.load_template("system_prompt.md")

    def load_agent_template(self, agent_name: str) -> str:
        filename = AGENT_TEMPLATE_MAP.get(agent_name)
        if not filename:
            raise ValueError(f"Unknown agent: {agent_name}")
        return self.load_template(filename)

    def load_persona_modifiers(self) -> str:
        return self.load_template("personas/persona_modifiers.md")

    def inject_variables(self, template: str, variables: dict[str, Any]) -> str:
        result = template
        for key, value in variables.items():
            placeholder = "{" + key + "}"
            if isinstance(value, (dict, list)):
                text = _format_complex(value)
            else:
                text = str(value) if value is not None else ""
            result = result.replace(placeholder, text)
        return result

    def build_system_message(self, agent_name: str, extra_vars: dict[str, Any] | None = None) -> str:
        system = self.load_system_prompt()
        agent_template = self.load_agent_template(agent_name)
        combined = f"{system}\n\n---\n\n{agent_template}"
        vars_ = {
            "agent_name": agent_name.replace("_", " ").title(),
            **(extra_vars or {}),
        }
        return self.inject_variables(combined, vars_)

    def build_user_message(self, agent_name: str, variables: dict[str, Any]) -> str:
        """Build user message from agent input section variables."""
        lines = [f"## Agent Input: {agent_name}", ""]
        for var_name in AGENT_VARIABLES.get(agent_name, variables.keys()):
            if var_name in variables:
                value = variables[var_name]
                if isinstance(value, (dict, list)):
                    value = _format_complex(value)
                lines.append(f"**{var_name}:**\n{value}")
                lines.append("")
        return "\n".join(lines)

    def build_messages(
        self,
        agent_name: str,
        variables: dict[str, Any],
        language: str = "",
        persona: str = "",
    ) -> list[dict[str, str]]:
        system = self.build_system_message(
            agent_name,
            {"language": language, "persona": persona},
        )
        user = self.build_user_message(agent_name, variables)
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

    def build_retry_message(self, validation_error: str, expected_schema: str, previous: str) -> str:
        return (
            f"Your previous response failed validation.\n\n"
            f"Error: {validation_error}\n"
            f"Expected format: {expected_schema}\n\n"
            f"Please regenerate your response following the exact output format specified.\n"
            f"Previous response (truncated): {previous[:500]}"
        )


def _format_complex(value: Any) -> str:
    import json
    if isinstance(value, str):
        return value
    return json.dumps(value, indent=2, default=str)


_loader: PromptLoader | None = None


def get_prompt_loader() -> PromptLoader:
    global _loader
    if _loader is None:
        _loader = PromptLoader()
    return _loader
