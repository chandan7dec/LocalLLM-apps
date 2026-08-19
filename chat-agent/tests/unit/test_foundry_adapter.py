"""Unit tests for safe Foundry Local adapter result translation."""

from types import SimpleNamespace
from typing import Any

import pytest

from chat_agent.domain import ErrorCategory
from chat_agent.foundry_adapter import FoundryLocalAdapter


class FakeClient:
    def __init__(self, completion: Any = None, error: Exception | None = None) -> None:
        self.completion = completion
        self.error = error

    def complete_chat(self, _messages: list[dict[str, str]]) -> Any:
        if self.error:
            raise self.error
        return self.completion


def adapter_with_client(client: FakeClient) -> FoundryLocalAdapter:
    adapter = object.__new__(FoundryLocalAdapter)
    adapter._client = client
    return adapter


def test_empty_model_response_becomes_invalid_response() -> None:
    completion = SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content="  "))])

    result = adapter_with_client(FakeClient(completion=completion)).answer("Question")

    assert not result.succeeded
    assert result.error_category is ErrorCategory.INVALID_RESPONSE


@pytest.mark.parametrize(
    ("error", "category"),
    [
        (TimeoutError(), ErrorCategory.TIMEOUT),
        (ConnectionError(), ErrorCategory.UNAVAILABLE),
    ],
)
def test_runtime_failures_become_safe_categories(error: Exception, category: ErrorCategory) -> None:
    result = adapter_with_client(FakeClient(error=error)).answer("Question")

    assert not result.succeeded
    assert result.error_category is category
