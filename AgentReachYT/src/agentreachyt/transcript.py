"""Transcript download and VTT parsing utilities."""

from __future__ import annotations

import glob

import yt_dlp

from agentreachyt.config import SUBTITLE_LANG, TRANSCRIPT_PREFIX
from agentreachyt.exceptions import TranscriptDownloadError


def _download_subtitles(url: str, auto: bool) -> None:
    mode = "writeautomaticsub" if auto else "writesub"
    ydl_opts = {
        mode: True,
        "subtitleslangs": [SUBTITLE_LANG],
        "skip_download": True,
        "subtitlesformat": "vtt",
        "outtmpl": TRANSCRIPT_PREFIX,
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url, download=True)


def get_transcript(url: str) -> str | None:
    """Download YouTube subtitles via yt-dlp.

    Args:
        url: A YouTube video URL.

    Returns:
        Path to the downloaded .vtt file, or None if unavailable.
    """
    try:
        _download_subtitles(url, auto=True)
    except Exception:
        try:
            _download_subtitles(url, auto=False)
        except Exception as exc:
            raise TranscriptDownloadError(
                f"yt-dlp failed: {exc}"
            ) from exc

    files: list[str] = glob.glob(f"{TRANSCRIPT_PREFIX}*.vtt")
    return files[0] if files else None


def parse_vtt(path: str) -> str:
    """Parse a WebVTT file and return clean transcript text.

    Removes timestamps, headers, blank lines, and simple HTML-style tags.
    Deduplicates lines while preserving order.

    Args:
        path: Absolute or relative path to the .vtt file.

    Returns:
        Cleaned transcript text as a single string.
    """
    seen: set[str] = set()
    lines: list[str] = []

    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()

            if not line or line.startswith("WEBVTT") or "-->" in line:
                continue

            clean = line.replace("<c>", "").replace("</c>", "")
            clean = clean.split("<")[0].strip()

            if clean and clean not in seen:
                seen.add(clean)
                lines.append(clean)

    return " ".join(lines)
