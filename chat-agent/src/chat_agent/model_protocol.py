"""Application-level model contract independent of Foundry Local SDK details."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .domain import ErrorCategory


@dataclass(frozen=True, slots=True)
class ModelResult:
    """Safe result returned by any local chat model adapter."""

    content: str | None = None
    error_category: ErrorCategory | None = None

    @property
    def succeeded(self) -> bool:
        """Whether this result contains a usable model response."""
        return self.content is not None and self.error_category is None

    @classmethod
    def success(cls, content: str) -> ModelResult:
        normalized = content.strip()
        if not normalized:
            raise ValueError("Successful model result must contain non-whitespace text")
        return cls(content=normalized)

    @classmethod
    def failure(cls, error_category: ErrorCategory) -> ModelResult:
        return cls(error_category=error_category)


class ChatModel(Protocol):
    """Boundary consumed by chat orchestration."""

    def answer(self, question: str) -> ModelResult:
        """Return a safe result for one validated question."""
        ...
