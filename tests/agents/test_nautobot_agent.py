"""Agent tool-call tests — verify the agent invokes the right Nautobot tools."""
from __future__ import annotations

import os

import pytest

pytestmark = pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set – skipping live agent tests",
)


def _make_agent(toolbox):
    """Build a minimal LangChain agent backed by the fake toolbox."""
    from langchain_core.tools import tool
    from langchain_openai import ChatOpenAI
    from langgraph.prebuilt import create_react_agent

    @tool
    def nautobot_get_device(name: str) -> dict:  # type: ignore[return]
        """Look up a device by name in Nautobot."""
        return toolbox.nautobot_get_device(name)

    @tool
    def nautobot_get_interfaces(device: str) -> list:  # type: ignore[return]
        """Return interface list for a device."""
        return toolbox.nautobot_get_interfaces(device)

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return create_react_agent(llm, tools=[nautobot_get_device, nautobot_get_interfaces])


def test_agent_calls_nautobot_lookup(fake_toolbox):
    agent = _make_agent(fake_toolbox)
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "Find the site and role for device edge-ams1."}]}
    )
    last_msg = response["messages"][-1].content
    assert fake_toolbox.called("nautobot_get_device")
    assert "edge-ams1" in fake_toolbox.last_args("nautobot_get_device").get("name", "")
    assert last_msg  # agent produced a non-empty answer


def test_agent_includes_site_in_response(fake_toolbox):
    agent = _make_agent(fake_toolbox)
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "What site is edge-ams1 in?"}]}
    )
    last_msg = response["messages"][-1].content.lower()
    assert "ams1" in last_msg or "site" in last_msg
