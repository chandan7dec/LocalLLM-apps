"""Streamlit entry point for the local chat agent."""

from __future__ import annotations

import streamlit as st

from chat_agent.chat_service import ChatService
from chat_agent.config import AppConfig
from chat_agent.domain import (
    ChatExchange,
    ChatSession,
    ErrorCategory,
    ResponseStatus,
    normalize_question,
)
from chat_agent.foundry_adapter import get_cached_adapter


def _get_chat_session() -> ChatSession:
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = ChatSession()
    return st.session_state.chat_session


def _render_exchange(exchange: ChatExchange) -> None:
    with st.chat_message("user"):
        st.write(exchange.question.content)

    with st.chat_message("assistant"):
        if exchange.response.status is ResponseStatus.COMPLETED:
            st.write(exchange.response.content)
        elif exchange.response.status is ResponseStatus.FAILED:
            st.error(_safe_error_message(exchange.response.error_category))


def _render_history(session: ChatSession) -> None:
    """Render each in-memory exchange exactly once in sequence order."""
    for exchange in session.exchanges:
        _render_exchange(exchange)


def _safe_error_message(category: ErrorCategory | None) -> str:
    messages = {
        ErrorCategory.UNAVAILABLE: (
            "The local model is unavailable. Check Foundry Local and try again."
        ),
        ErrorCategory.TIMEOUT: "The local model took too long to respond. Try again.",
        ErrorCategory.INVALID_RESPONSE: "The local model returned an invalid answer. Try again.",
    }
    if category is not None and category in messages:
        return messages[category]
    return "The local model could not answer. Try again."


def _validation_message(question: str) -> str | None:
    """Return correction feedback for empty input without invoking the model."""
    if not normalize_question(question):
        return "Please enter a question before sending."
    return None


def main() -> None:
    """Render the single-question local chat experience."""
    st.set_page_config(page_title="Local Chat Agent", page_icon="💬")
    st.title("Local Chat Agent")
    st.caption("Ask a question and receive an answer from your local model.")

    session = _get_chat_session()
    _render_history(session)

    question = st.chat_input(
        "Ask a question",
        disabled=session.pending_exchange is not None,
    )
    if question is None:
        return

    validation_message = _validation_message(question)
    if validation_message:
        st.warning(validation_message)
        return

    with st.chat_message("user"):
        st.write(question.strip())

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                config = AppConfig.from_env()
                model = get_cached_adapter(config.model_alias)
                exchange = ChatService(model, session).submit(question)
            except (ConnectionError, OSError, TimeoutError):
                st.error(_safe_error_message(ErrorCategory.UNAVAILABLE))
                return
            except Exception:
                st.error("The local model could not be started. Check Foundry Local and try again.")
                return

        if exchange.response.status is ResponseStatus.COMPLETED:
            st.write(exchange.response.content)
        else:
            st.error(_safe_error_message(exchange.response.error_category))


if __name__ == "__main__":
    main()
