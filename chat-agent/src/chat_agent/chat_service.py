"""Application orchestration for serialized local-model chat requests."""

from __future__ import annotations

import logging
from time import perf_counter

from .domain import ChatExchange, ChatSession, ErrorCategory
from .model_protocol import ChatModel, ModelResult

logger = logging.getLogger(__name__)


class ChatService:
    """Coordinate validated questions, model calls, and safe exchange state."""

    def __init__(self, model: ChatModel, session: ChatSession | None = None) -> None:
        self._model = model
        self.session = session or ChatSession()

    def submit(self, content: str) -> ChatExchange:
        """Submit one question and resolve its exchange without leaking sensitive data."""
        exchange = self.session.start_exchange(content)
        started = perf_counter()

        try:
            result = self._model.answer(exchange.question.content)
        except TimeoutError:
            result = ModelResult.failure(ErrorCategory.TIMEOUT)
        except (ConnectionError, OSError):
            result = ModelResult.failure(ErrorCategory.UNAVAILABLE)
        except ValueError:
            result = ModelResult.failure(ErrorCategory.INVALID_RESPONSE)

        if result.succeeded:
            exchange.complete(result.content or "")
        else:
            exchange.fail(result.error_category or ErrorCategory.INVALID_RESPONSE)

        self._log_result(exchange, started)
        return exchange

    @staticmethod
    def _log_result(exchange: ChatExchange, started: float) -> None:
        """Log request metadata only; never include question or response text."""
        duration_ms = round((perf_counter() - started) * 1000, 2)
        logger.info(
            "chat_request_completed",
            extra={
                "status": exchange.response.status.value,
                "error_category": (
                    exchange.response.error_category.value
                    if exchange.response.error_category
                    else None
                ),
                "duration_ms": duration_ms,
            },
        )
