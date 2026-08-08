"""LLM integration for blog generation (Ollama or llama.cpp)."""

from __future__ import annotations

import json
from collections.abc import Generator

import requests

from agentreachyt.config import API_URL, LLM_BACKEND, MODEL, SYSTEM_PROMPT, Settings
from agentreachyt.exceptions import LLMConnectionError, LLMGenerationError


def _ollama_payload(transcript: str, settings: Settings) -> dict:
    return {
        "model": MODEL,
        "system": SYSTEM_PROMPT,
        "prompt": f"Transcript:\n\n{transcript[:settings.max_transcript_chars]}",
        "stream": True,
        "options": {
            "num_predict": settings.num_predict,
            "temperature": settings.temperature,
        },
    }


def _llama_cpp_payload(transcript: str, settings: Settings) -> dict:
    return {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Transcript:\n\n{transcript[:settings.max_transcript_chars]}",
            },
        ],
        "stream": True,
        "max_tokens": settings.num_predict,
        "temperature": settings.temperature,
    }


def _stream_ollama(response: requests.Response) -> Generator[str, None, None]:
    for line in response.iter_lines():
        if not line:
            continue
        try:
            chunk = json.loads(line)
        except json.JSONDecodeError as exc:
            raise LLMGenerationError(
                f"Failed to parse LLM response: {exc}"
            ) from exc

        token = chunk.get("response", "")
        if token:
            yield token

        if chunk.get("done"):
            break


def _stream_llama_cpp(response: requests.Response) -> Generator[str, None, None]:
    for line in response.iter_lines():
        if not line:
            continue
        text = line.decode("utf-8") if isinstance(line, bytes) else line
        if not text.startswith("data:"):
            continue
        data = text[5:].strip()
        if data == "[DONE]":
            break
        try:
            chunk = json.loads(data)
        except json.JSONDecodeError as exc:
            raise LLMGenerationError(
                f"Failed to parse LLM response: {exc}"
            ) from exc

        choices = chunk.get("choices", [])
        if choices:
            delta = choices[0].get("delta", {})
            token = delta.get("content", "")
            if token:
                yield token

        if chunk.get("choices", [{}])[0].get("finish_reason") == "stop":
            break


def generate_blog(
    transcript: str,
    model: str = MODEL,
    url: str = API_URL,
    system_prompt: str = SYSTEM_PROMPT,
) -> Generator[str, None, None]:
    """Stream a blog post from the configured LLM backend.

    Args:
        transcript: Cleaned transcript text.
        model: Model identifier.
        url: LLM API endpoint.
        system_prompt: System prompt to guide generation style.

    Yields:
        Incremental text chunks from the LLM response.

    Raises:
        LLMConnectionError: If the LLM server is unreachable.
        LLMGenerationError: If the API returns an error.
    """
    settings = Settings()

    if LLM_BACKEND == "ollama":
        payload = _ollama_payload(transcript, settings)
    else:
        payload = _llama_cpp_payload(transcript, settings)

    try:
        with requests.post(
            url,
            json=payload,
            stream=True,
            timeout=settings.request_timeout,
        ) as response:
            response.raise_for_status()

            if LLM_BACKEND == "ollama":
                yield from _stream_ollama(response)
            else:
                yield from _stream_llama_cpp(response)

    except requests.exceptions.ConnectionError as exc:
        raise LLMConnectionError(
            f"{LLM_BACKEND} server is not running at {url}"
        ) from exc
    except requests.exceptions.RequestException as exc:
        raise LLMGenerationError(f"LLM API error: {exc}") from exc
