"""Pydantic schemas for agent JSON outputs."""

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class RouterOutput(BaseModel):
    language: str
    language_confidence: float = Field(ge=0.0, le=1.0)
    intent: str
    persona: str
    persona_confidence: float = Field(ge=0.0, le=1.0, default=0.8)
    ambiguity_detected: bool = False
    ambiguity_details: list[str] = Field(default_factory=list)
    clarifying_questions: list[str] = Field(default_factory=list)
    workflow: list[str] = Field(default_factory=list)
    skip_agents: list[str] = Field(default_factory=list)
    routing_rationale: str = ""


class RequirementIO(BaseModel):
    name: str
    type: str
    description: str = ""
    constraints: str = ""


class RequirementExtractionOutput(BaseModel):
    title: str
    summary: str
    language: str
    inputs: list[RequirementIO] = Field(default_factory=list)
    outputs: list[RequirementIO] = Field(default_factory=list)
    functional_requirements: list[str] = Field(default_factory=list)
    non_functional_requirements: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    edge_cases: list[str] = Field(default_factory=list)
    suggested_libraries: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)


class PersonaOutput(BaseModel):
    persona: str
    persona_display_name: str
    code_style_instructions: str = ""
    review_standards: str = ""
    testing_strategy: str = ""
    explanation_style: str = ""
    documentation_level: str = "standard"
    complexity_priority: str = "balanced"
    required_sections: list[str] = Field(default_factory=list)
    persona_prompt_block: str = ""


class ContextSnippet(BaseModel):
    source: str
    language: str
    relevance_score: float
    snippet: str
    usage_note: str = ""


class ContextRetrievalOutput(BaseModel):
    retrieval_performed: bool = False
    query_used: str = ""
    num_results: int = 0
    context_snippets: list[ContextSnippet] = Field(default_factory=list)
    patterns_identified: list[str] = Field(default_factory=list)
    context_summary: str = ""
    context_prompt_block: str = ""


class ReviewIssue(BaseModel):
    severity: str
    category: str
    line_reference: str = ""
    description: str
    suggestion: str = ""


class CodeReviewOutput(BaseModel):
    overall_score: int = Field(ge=0, le=100)
    verdict: Literal["APPROVE", "REQUEST_CHANGES", "REJECT"]
    summary: str
    issues: list[ReviewIssue] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    reviewed_code: str = ""
    checklist: dict[str, str] = Field(default_factory=dict)


class SecurityFinding(BaseModel):
    severity: str
    category: str
    location: str = ""
    description: str
    cwe_id: str = ""
    remediation: str = ""
    fixed_code_snippet: str = ""


class SecurityReviewOutput(BaseModel):
    security_score: int = Field(ge=0, le=100)
    verdict: Literal["PASS", "WARN", "FAIL"]
    risk_level: str = "none"
    findings: list[SecurityFinding] = Field(default_factory=list)
    passed_checks: list[str] = Field(default_factory=list)
    security_report_summary: str = ""
    sanitized_code: str = ""


class UnitTestOutput(BaseModel):
    framework: str
    total_tests: int = 0
    categories: dict[str, int] = Field(default_factory=dict)
    test_file_name: str = ""
    runnable: bool = True


class TestResult(BaseModel):
    test_name: str
    status: str
    duration_ms: int = 0
    message: str = ""


class ExecutionOutput(BaseModel):
    execution_status: str
    language: str
    runtime_ms: int = 0
    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0
    test_results: list[TestResult] = Field(default_factory=list)
    tests_summary: dict[str, int] = Field(default_factory=dict)
    traceback: Optional[str] = None
    execution_logs: list[dict[str, str]] = Field(default_factory=list)
    sandbox_notes: str = ""


class ImprovementSuggestion(BaseModel):
    priority: str
    area: str
    suggestion: str


class EvaluatorOutput(BaseModel):
    verdict: Literal["PASS", "FAIL"]
    confidence_score: float = Field(ge=0.0, le=1.0)
    scores: dict[str, int] = Field(default_factory=dict)
    requirements_met: list[str] = Field(default_factory=list)
    requirements_missing: list[str] = Field(default_factory=list)
    test_pass_rate: float = 0.0
    improvement_suggestions: list[ImprovementSuggestion] = Field(default_factory=list)
    evaluation_summary: str = ""
    should_regenerate: bool = False
    regenerate_agent: Optional[str] = None


class OptimizationReport(BaseModel):
    selected_approach: str = "optimized"
    time_complexity: str = ""
    space_complexity: str = ""
    regenerated: bool = False
    improvement_over_initial: str = ""


class DocumentationOutput(BaseModel):
    readme: str = ""
    api_docs: str = ""
    architecture_doc: str = ""
    deployment_guide: str = ""
    presentation_notes: str = ""


AGENT_SCHEMA_MAP: dict[str, type[BaseModel]] = {
    "router": RouterOutput,
    "requirement_extraction": RequirementExtractionOutput,
    "persona": PersonaOutput,
    "context_retrieval": ContextRetrievalOutput,
    "code_review": CodeReviewOutput,
    "security_review": SecurityReviewOutput,
    "unit_test_generator": UnitTestOutput,
    "execution": ExecutionOutput,
    "evaluator": EvaluatorOutput,
    "documentation": DocumentationOutput,
}
