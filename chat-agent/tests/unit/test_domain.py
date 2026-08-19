"""Unit tests for chat domain invariants."""

import pytest

from chat_agent.domain import (
    ChatSession,
    ErrorCategory,
    Question,
    ResponseStatus,
    normalize_question,
)


def test_question_is_trimmed() -> None:
    assert Question("  What is local inference?  ").content == "What is local inference?"


def test_empty_question_is_rejected() -> None:
    with pytest.raises(ValueError, match="non-whitespace"):
        Question("   ")


@pytest.mark.parametrize("content", ["", "   ", "\t\n"])
def test_invalid_question_content_is_normalized_to_empty(content: str) -> None:
    assert normalize_question(content) == ""


def test_valid_question_content_is_normalized_without_losing_internal_spacing() -> None:
    assert normalize_question("  two   words  ") == "two   words"


def test_exchange_transitions_to_completed() -> None:
    exchange = ChatSession().start_exchange("Question")

    exchange.complete("  Answer  ")

    assert exchange.response.status is ResponseStatus.COMPLETED
    assert exchange.response.content == "Answer"
    assert exchange.response.error_category is None


def test_exchange_transitions_to_failed() -> None:
    exchange = ChatSession().start_exchange("Question")

    exchange.fail(ErrorCategory.UNAVAILABLE)

    assert exchange.response.status is ResponseStatus.FAILED
    assert exchange.response.content is None
    assert exchange.response.error_category is ErrorCategory.UNAVAILABLE


def test_only_one_exchange_can_be_pending() -> None:
    session = ChatSession()
    session.start_exchange("First question")

    with pytest.raises(RuntimeError, match="already being processed"):
        session.start_exchange("Second question")


def test_completed_exchanges_receive_ordered_sequences() -> None:
    session = ChatSession()
    first = session.start_exchange("First")
    first.complete("Answer one")
    second = session.start_exchange("Second")
    second.complete("Answer two")

    assert [exchange.sequence for exchange in session.exchanges] == [1, 2]
