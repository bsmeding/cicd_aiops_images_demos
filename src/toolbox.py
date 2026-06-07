"""Fake toolbox for agent tool-call tests — records calls without hitting real APIs."""
from __future__ import annotations

from collections import defaultdict
from typing import Any


class FakeToolbox:
    """Drop-in stub that records tool invocations made by the agent under test."""

    def __init__(self) -> None:
        self._calls: dict[str, list[dict[str, Any]]] = defaultdict(list)

    # ── Nautobot stubs ────────────────────────────────────────────────────────

    def nautobot_get_device(self, name: str) -> dict[str, Any]:
        self._record("nautobot_get_device", {"name": name})
        return {
            "name": name,
            "site": "AMS1",
            "role": "edge-router",
            "status": "active",
            "primary_ip": "10.0.0.1",
        }

    def nautobot_get_interfaces(self, device: str) -> list[dict[str, Any]]:
        self._record("nautobot_get_interfaces", {"device": device})
        return [
            {"name": "GigabitEthernet0/0", "status": "active"},
            {"name": "GigabitEthernet0/1", "status": "down"},
        ]

    # ── Generic call recorder ─────────────────────────────────────────────────

    def called(self, tool_name: str) -> bool:
        return len(self._calls[tool_name]) > 0

    def call_count(self, tool_name: str) -> int:
        return len(self._calls[tool_name])

    def last_args(self, tool_name: str) -> dict[str, Any]:
        return self._calls[tool_name][-1] if self._calls[tool_name] else {}

    def _record(self, tool_name: str, args: dict[str, Any]) -> None:
        self._calls[tool_name].append(args)
