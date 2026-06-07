"""Shared pytest fixtures."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Make src/ importable without installing the package
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from prompt_runner import PromptRunner
from toolbox import FakeToolbox


@pytest.fixture
def prompt_runner() -> PromptRunner:
    return PromptRunner()


@pytest.fixture
def fake_toolbox() -> FakeToolbox:
    return FakeToolbox()
