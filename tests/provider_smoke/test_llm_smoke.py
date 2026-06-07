"""Provider smoke tests — live API calls, manual dispatch only."""
from __future__ import annotations

import os

import pytest
from litellm import completion

pytestmark = pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set – skipping provider smoke tests",
)

_MSG = [
    {"role": "system", "content": "Answer in one sentence."},
    {"role": "user", "content": "What is NetDevOps?"},
]


def test_openai_gpt4o_mini_responds() -> None:
    response = completion(model="gpt-4o-mini", messages=_MSG)
    content = response.choices[0].message.content
    assert content and len(content) > 5


@pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)
def test_anthropic_haiku_responds() -> None:
    response = completion(model="claude-haiku-4-5-20251001", messages=_MSG)
    content = response.choices[0].message.content
    assert content and len(content) > 5
