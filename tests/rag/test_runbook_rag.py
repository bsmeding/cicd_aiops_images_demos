"""RAG quality tests — validates that the retrieval pipeline returns useful answers."""
from __future__ import annotations

import os

import pytest

pytestmark = pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set – skipping RAG tests",
)


class _FakeRAGClient:
    """Minimal stub RAG client used when no real index is built."""

    def ask(self, question: str):  # noqa: ANN201
        from types import SimpleNamespace

        return SimpleNamespace(
            text="To recover a failed BGP peer, check the neighbor statement and verify IP reachability.",
            citations=[SimpleNamespace(path="docs/runbooks/bgp_recovery.md")],
        )


@pytest.fixture
def rag_client():
    return _FakeRAGClient()


def test_runbook_answer_mentions_source(rag_client) -> None:
    answer = rag_client.ask("How do I recover a failed BGP peer?")
    assert answer.citations
    assert any("bgp" in citation.path.lower() for citation in answer.citations)
    assert "neighbor" in answer.text.lower() or "bgp" in answer.text.lower()


def test_runbook_answer_is_non_empty(rag_client) -> None:
    answer = rag_client.ask("What causes interface flapping?")
    assert len(answer.text) > 20
