"""Prompt regression tests for the incident_router prompt.

These tests call the real LLM and validate that the response satisfies the
IncidentTriage contract. Requires OPENAI_API_KEY in the environment.
Mark with @pytest.mark.llm if you want to skip them without that variable.
"""
from __future__ import annotations

import os

import pytest
from pydantic import BaseModel, field_validator

pytestmark = pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set – skipping live LLM tests",
)


class IncidentTriage(BaseModel):
    severity: str
    summary: str
    recommended_action: str

    @field_validator("severity", mode="before")
    @classmethod
    def normalize_severity(cls, v: str) -> str:
        return v.lower()


def test_router_prompt_returns_required_fields(prompt_runner):
    result = prompt_runner.run(
        prompt_name="incident_router",
        input_text="BGP sessions down on edge routers in site AMS1",
    )
    parsed = IncidentTriage.model_validate(result)
    assert parsed.severity in {"low", "medium", "high", "critical"}
    assert len(parsed.summary) > 10
    assert len(parsed.recommended_action) > 10


def test_router_prompt_mentions_bgp(prompt_runner):
    result = prompt_runner.run(
        prompt_name="incident_router",
        input_text="BGP neighbor 10.0.0.2 went down on core-ams1",
    )
    parsed = IncidentTriage.model_validate(result)
    assert "BGP" in parsed.summary or "bgp" in parsed.summary.lower()


def test_router_prompt_classifies_critical(prompt_runner):
    result = prompt_runner.run(
        prompt_name="incident_router",
        input_text=(
            "All BGP sessions down across all edge routers. "
            "Full network outage in AMS1 and FRA1."
        ),
    )
    parsed = IncidentTriage.model_validate(result)
    assert parsed.severity in {"high", "critical"}
