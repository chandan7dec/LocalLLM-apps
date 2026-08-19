"""Opt-in integration test for the installed Microsoft Foundry Local runtime."""

import os

import pytest

from chat_agent.config import AppConfig
from chat_agent.foundry_adapter import FoundryLocalAdapter

pytestmark = pytest.mark.foundry_integration


@pytest.mark.skipif(
    os.getenv("RUN_FOUNDRY_INTEGRATION") != "1",
    reason="Set RUN_FOUNDRY_INTEGRATION=1 to run against Foundry Local",
)
def test_foundry_local_returns_non_empty_response() -> None:
    adapter = FoundryLocalAdapter(AppConfig.from_env())

    result = adapter.answer("Reply with one short sentence about local AI.")

    assert result.succeeded
    assert result.content
