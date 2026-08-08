"""Streamlit user interface."""

from __future__ import annotations

import os

import streamlit as st

from agentreachyt.config import LLM_BACKEND, MODEL
from agentreachyt.exceptions import (
    LLMConnectionError,
    LLMGenerationError,
    TranscriptDownloadError,
    TranscriptParseError,
)
from agentreachyt.llm import generate_blog
from agentreachyt.transcript import get_transcript, parse_vtt


def render() -> None:
    """Render the Streamlit application UI."""
    st.set_page_config(
        page_title="YT → SEO Blog",
        page_icon="🎬",
        layout="wide",
    )
    st.title("🎬 Zero-API YouTube → SEO Blog Engine")
    st.caption(
        f"**Agent Reach** (yt-dlp) + **{LLM_BACKEND}** `{MODEL}` · No YouTube API key needed"
    )
    st.divider()

    url = st.text_input(
        "📎 Paste a YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
    )

    if not st.button(
        "🚀 Generate SEO Blog",
        type="primary",
        disabled=not url.strip(),
    ):
        return

    with st.spinner("⬇️ Downloading transcript via Agent Reach (yt-dlp)…"):
        try:
            vtt_path = get_transcript(url.strip())
        except TranscriptDownloadError as exc:
            st.error(f"Transcript download failed: {exc}")
            return

    if not vtt_path:
        st.warning(
            "No subtitles found. The video may not have auto-captions."
        )
        return

    try:
        transcript = parse_vtt(vtt_path)
    except TranscriptParseError as exc:
        st.error(f"Failed to parse transcript: {exc}")
        return
    finally:
        if os.path.exists(vtt_path):
            os.remove(vtt_path)

    if not transcript:
        st.error("Transcript was empty after parsing.")
        return

    with st.expander("📄 Transcript preview"):
        st.text(transcript[:500] + "…")

    st.subheader("✍️ Generated SEO Blog Post")

    try:
        st.write_stream(generate_blog(transcript))
    except LLMConnectionError as exc:
        st.error(str(exc))
    except LLMGenerationError as exc:
        st.error(f"Generation failed: {exc}")
