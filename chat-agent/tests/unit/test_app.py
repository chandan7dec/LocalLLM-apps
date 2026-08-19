"""Deterministic tests for Streamlit exchange rendering."""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

sys.path.insert(0, str(Path(__file__).parents[2]))

import app  # noqa: E402

from chat_agent.domain import ChatSession


@dataclass
class FakeContainer:
    recorder: list[tuple[str, Any]]
    role: str

    def __enter__(self) -> FakeContainer:
        self.recorder.append(("enter", self.role))
        return self

    def __exit__(self, *_args: object) -> None:
        self.recorder.append(("exit", self.role))


@dataclass
class FakeStreamlit:
    recorder: list[tuple[str, Any]] = field(default_factory=list)

    def chat_message(self, role: str) -> FakeContainer:
        return FakeContainer(self.recorder, role)

    def write(self, value: Any) -> None:
        self.recorder.append(("write", value))

    def error(self, value: str) -> None:
        self.recorder.append(("error", value))


def test_render_history_renders_each_exchange_once_in_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = ChatSession()
    first = session.start_exchange("First question")
    first.complete("First answer")
    second = session.start_exchange("Second question")
    second.complete("Second answer")

    fake_streamlit = FakeStreamlit()
    monkeypatch.setattr(app, "st", fake_streamlit)

    app._render_history(session)

    writes = [value for event, value in fake_streamlit.recorder if event == "write"]
    assert writes == ["First question", "First answer", "Second question", "Second answer"]
    assert [event for event, _ in fake_streamlit.recorder].count("write") == 4


def test_empty_input_gets_validation_message() -> None:
    assert app._validation_message("   ") == "Please enter a question before sending."


def test_valid_input_has_no_validation_message() -> None:
    assert app._validation_message("A valid question") is None
