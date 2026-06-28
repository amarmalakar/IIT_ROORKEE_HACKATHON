"""Pydantic request/response schemas for API."""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    request: str = Field(..., min_length=1, description="Natural language code request")
    persona: str = Field(default="", description="Optional persona override")
    language: str = Field(default="", description="Optional language override")
    model: str = Field(default="", description="Optional model override")


class ReviewRequest(BaseModel):
    request: str = Field(..., min_length=1)
    code: str = Field(..., min_length=1)
    language: str = Field(default="python")
    persona: str = Field(default="")


class TestRequest(BaseModel):
    request: str = Field(default="")
    code: str = Field(..., min_length=1)
    language: str = Field(default="python")
    persona: str = Field(default="")


class EvaluateRequest(BaseModel):
    request: str = Field(default="")
    code: str = Field(..., min_length=1)
    tests: str = Field(default="")
    language: str = Field(default="python")
    persona: str = Field(default="")


class WorkflowResponse(BaseModel):
    nodes: list[dict[str, Any]]
    edges: list[dict[str, str]]


class GenerateResponse(BaseModel):
    success: bool
    state: dict[str, Any]
    message: str = ""
