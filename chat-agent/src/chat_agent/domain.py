"""Domain entities and state transitions for a browser chat session."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ResponseStatus(StrEnum):
    """Lifecycle states for a model response."""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class ErrorCategory(StrEnum):
    """Safe categories exposed by the model boundary."""

    UNAVAILABLE = "unavailable"
    TIMEOUT = "timeout"
    INVALID_RESPONSE = "invalid_response"


@dataclass(frozen=True, slots=True)
class Question:
    """A validated, normalized question submitted by a user."""

    content: str

    def __post_init__(self) -> None:
        normalized = normalize_question(self.content)
        if not normalized:
            raise ValueError("Question must contain non-whitespace text")
        object.__setattr__(self, "content", normalized)


def normalize_question(content: str) -> str:
    """Trim user input without changing meaningful internal whitespace."""
    return content.strip()


@dataclass(slots=True)
class ModelResponse:
    """The current response state associated with a question."""

    status: ResponseStatus = ResponseStatus.PENDING
    content: str | None = None
    error_category: ErrorCategory | None = None

    @classmethod
    def completed(cls, content: str) -> ModelResponse:
        normalized = content.strip()
        if not normalized:
            raise ValueError("Completed response must contain non-whitespace text")
        return cls(status=ResponseStatus.COMPLETED, content=normalized)

    @classmethod
    def failed(cls, error_category: ErrorCategory) -> ModelResponse:
        return cls(status=ResponseStatus.FAILED, error_category=error_category)


@dataclass(slots=True)
class ChatExchange:
    """An ordered question and its mutable response state."""

    sequence: int
    question: Question
    response: ModelResponse = field(default_factory=ModelResponse)

    def complete(self, content: str) -> None:
        self.response = ModelResponse.completed(content)

    def fail(self, error_category: ErrorCategory) -> None:
        self.response = ModelResponse.failed(error_category)


@dataclass(slots=True)
class ChatSession:
    """In-memory ordered exchanges for one browser session."""

    exchanges: list[ChatExchange] = field(default_factory=list)

    @property
    def pending_exchange(self) -> ChatExchange | None:
        return next(
            (
                exchange
                for exchange in self.exchanges
                if exchange.response.status is ResponseStatus.PENDING
            ),
            None,
        )

    def start_exchange(self, content: str) -> ChatExchange:
        if self.pending_exchange is not None:
            raise RuntimeError("Another question is already being processed")
        exchange = ChatExchange(
            sequence=len(self.exchanges) + 1,
            question=Question(content),
        )
        self.exchanges.append(exchange)
        return exchange
