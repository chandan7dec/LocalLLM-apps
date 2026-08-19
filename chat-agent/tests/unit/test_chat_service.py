"""Unit tests for the User Story 1 chat service flow."""

import pytest

from chat_agent.chat_service import ChatService
from chat_agent.domain import ErrorCategory, ResponseStatus
from chat_agent.model_protocol import ModelResult


class FakeModel:
    def __init__(self, result: ModelResult | None = None, error: Exception | None = None) -> None:
        self.calls: list[str] = []
        self.result = result or ModelResult.success("A local answer")
        self.error = error

    def answer(self, question: str) -> ModelResult:
        self.calls.append(question)
        if self.error:
            raise self.error
        return self.result


def test_valid_submission_completes_exchange_and_calls_model_once() -> None:
    model = FakeModel()
    service = ChatService(model)

    exchange = service.submit("  What is local inference?  ")

    assert model.calls == ["What is local inference?"]
    assert exchange.response.status is ResponseStatus.COMPLETED
    assert exchange.response.content == "A local answer"


def test_pending_exchange_resolves_to_model_answer() -> None:
    model = FakeModel(result=ModelResult.success("Finished answer"))
    service = ChatService(model)

    exchange = service.submit("Question")

    assert exchange.response.status is ResponseStatus.COMPLETED
    assert exchange.response.content == "Finished answer"
    assert service.session.pending_exchange is None


def test_ten_sequential_submissions_preserve_order_and_content() -> None:
    model = FakeModel()
    service = ChatService(model)

    for index in range(10):
        service.submit(f"Question {index}")

    assert [exchange.sequence for exchange in service.session.exchanges] == list(range(1, 11))
    assert [exchange.question.content for exchange in service.session.exchanges] == [
        f"Question {index}" for index in range(10)
    ]
    assert [exchange.response.content for exchange in service.session.exchanges] == [
        "A local answer" for _ in range(10)
    ]
    assert model.calls == [f"Question {index}" for index in range(10)]


def test_model_failure_becomes_safe_failed_exchange() -> None:
    model = FakeModel(result=ModelResult.failure(ErrorCategory.UNAVAILABLE))
    service = ChatService(model)

    exchange = service.submit("Question")

    assert exchange.response.status is ResponseStatus.FAILED
    assert exchange.response.error_category is ErrorCategory.UNAVAILABLE
    assert exchange.response.content is None


def test_failed_exchange_can_be_followed_by_a_retry() -> None:
    model = FakeModel(result=ModelResult.failure(ErrorCategory.UNAVAILABLE))
    service = ChatService(model)

    failed = service.submit("First question")
    model.result = ModelResult.success("Retry answer")
    retried = service.submit("Second question")

    assert failed.response.error_category is ErrorCategory.UNAVAILABLE
    assert retried.response.status is ResponseStatus.COMPLETED
    assert retried.response.content == "Retry answer"
    assert model.calls == ["First question", "Second question"]


@pytest.mark.parametrize(
    ("error", "category"),
    [
        (TimeoutError(), ErrorCategory.TIMEOUT),
        (ConnectionError(), ErrorCategory.UNAVAILABLE),
        (ValueError(), ErrorCategory.INVALID_RESPONSE),
    ],
)
def test_expected_model_exceptions_are_translated(
    error: Exception,
    category: ErrorCategory,
) -> None:
    service = ChatService(FakeModel(error=error))

    exchange = service.submit("Question")

    assert exchange.response.status is ResponseStatus.FAILED
    assert exchange.response.error_category is category
