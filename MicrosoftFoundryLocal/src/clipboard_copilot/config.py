"""Runtime configuration and shared constants.

Centralises all tunable settings and UTF-8 terminal handling so the rest of
the package can import them without re-running side-effectful setup code.
"""

from __future__ import annotations

import io
import sys

# Reconfigure stdout for UTF-8 compatibility on the Windows terminal.
if isinstance(sys.stdout, io.TextIOWrapper) and sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Model configuration
MODEL_NAME = "llama3.2:3b"
LOCAL_OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = (
    "Fix all spelling, grammar, punctuation, and phrasing errors in the "
    "provided text. Output ONLY the corrected text directly, without any "
    "intro, explanation, quotes, or preamble."
)
