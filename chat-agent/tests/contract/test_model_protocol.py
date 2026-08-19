"""Contract tests for application-level chat model adapters."""

from chat_agent.domain import ErrorCategory
from chat_agent.model_protocol import ChatModel, ModelResult


class FakeChatModel:
    def answer(self, question: str) -> ModelResult:
        return ModelResult.success(f"Echo: {question}")


def test_fake_adapter_matches_chat_model_contract() -> None:
    model: ChatModel = FakeChatModel()

    result = model.answer("hello")

    assert result.succeeded
    assert result.content == "Echo: hello"
    assert result.error_category is None


def test_successful_model_result_requires_content() -> None:
    result = ModelResult.success(" answer ")

    assert result.succeeded
    assert result.content == "answer"


def test_failed_model_result_contains_only_safe_category() -> None:
    result = ModelResult.failure(ErrorCategory.TIMEOUT)

    assert not result.succeeded
    assert result.content is None
    assert result.error_category is ErrorCategory.TIMEOUT
