"""Tests for the agentreachyt package."""

from __future__ import annotations

import tempfile
from pathlib import Path

from agentreachyt.config import Settings
from agentreachyt.transcript import parse_vtt


class TestParseVtt:
    def test_removes_timestamps(self) -> None:
        vtt_content = (
            "WEBVTT\n\n"
            "00:00:01.000 --> 00:00:04.000\n"
            "Hello world\n\n"
            "00:00:05.000 --> 00:00:08.000\n"
            "This is a test\n"
        )

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".vtt", delete=False, encoding="utf-8"
        ) as fh:
            fh.write(vtt_content)
            temp_path = fh.name

        try:
            result = parse_vtt(temp_path)
            assert "Hello world" in result
            assert "This is a test" in result
            assert "-->" not in result
            assert "WEBVTT" not in result
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_deduplicates_lines(self) -> None:
        vtt_content = (
            "WEBVTT\n\n"
            "00:00:01.000 --> 00:00:04.000\n"
            "Repeat line\n\n"
            "00:00:05.000 --> 00:00:08.000\n"
            "Repeat line\n"
        )

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".vtt", delete=False, encoding="utf-8"
        ) as fh:
            fh.write(vtt_content)
            temp_path = fh.name

        try:
            result = parse_vtt(temp_path)
            assert result.count("Repeat line") == 1
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_strips_html_tags(self) -> None:
        vtt_content = (
            "WEBVTT\n\n"
            "00:00:01.000 --> 00:00:04.000\n"
            "<c>Tagged text</c>\n"
        )

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".vtt", delete=False, encoding="utf-8"
        ) as fh:
            fh.write(vtt_content)
            temp_path = fh.name

        try:
            result = parse_vtt(temp_path)
            assert "<c>" not in result
            assert "</c>" not in result
            assert "Tagged text" in result
        finally:
            Path(temp_path).unlink(missing_ok=True)


class TestSettings:
    def test_defaults(self) -> None:
        s = Settings()
        assert s.model == "qwen2.5-coder:1.5b"
        assert s.temperature == 0.3
        assert s.num_predict == 1024
        assert s.max_transcript_chars == 6000
