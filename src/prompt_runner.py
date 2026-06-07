"""Thin wrapper around LiteLLM used by prompt regression tests."""
from __future__ import annotations

import os
from typing import Any

from litellm import completion


class PromptRunner:
    """Run a named prompt template against a configured model."""

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        prompts_dir: str = "prompts",
    ) -> None:
        self.model = model
        self.prompts_dir = prompts_dir

    def run(self, prompt_name: str, input_text: str, **kwargs: Any) -> dict[str, Any]:
        """Execute *prompt_name* with *input_text* and return the parsed response."""
        system_prompt = self._load_prompt(prompt_name)
        response = completion(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_text},
            ],
            response_format={"type": "json_object"},
            **kwargs,
        )
        import json

        content = response.choices[0].message.content
        return json.loads(content)  # type: ignore[arg-type]

    def _load_prompt(self, name: str) -> str:
        import pathlib

        path = pathlib.Path(self.prompts_dir) / f"{name}.txt"
        if path.exists():
            return path.read_text()
        # Fallback inline prompt used when no file is present (demo/test mode)
        return (
            "You are a network incident triage assistant. "
            "Respond with a JSON object containing: severity, summary, recommended_action."
        )
