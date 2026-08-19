"""Local LLM inference backends.

Provides grammar correction through either:

- **Microsoft Foundry Local SDK** — in-process C++ ONNX inference with
  automatic NPU (Snapdragon / Intel Core Ultra) and DirectML GPU detection.
- **Ollama** — fallback local HTTP REST API endpoint when the Foundry Local
  SDK is unavailable.

Both backends are optional; the module auto-detects them at import time and
degrades gracefully when a dependency is missing.
"""

from __future__ import annotations

import requests

from clipboard_copilot.config import LOCAL_OLLAMA_URL, MODEL_NAME, SYSTEM_PROMPT

# ---------------------------------------------------------------------------
# Foundry Local SDK discovery
# ---------------------------------------------------------------------------
FOUNDRY_MANAGER = None
HAS_FOUNDRY_SDK = False

try:
    from foundry_local_sdk import Configuration, FoundryLocalManager

    _config = Configuration(app_name="clipboard_copilot")
    FoundryLocalManager.initialize(_config)
    FOUNDRY_MANAGER = FoundryLocalManager.instance
    HAS_FOUNDRY_SDK = True
except Exception:
    HAS_FOUNDRY_SDK = False


def correct_text_with_foundry_sdk(text: str) -> str:
    """Correct ``text`` using the Foundry Local SDK in-process engine.

    Key advantages over Ollama:

    1. In-process C++ ONNX bindings (zero HTTP socket serialization latency).
    2. Automatic NPU (Snapdragon / Intel Core Ultra) & DirectML GPU detection.
    3. Standalone ~20MB runtime embeddable in end-user apps without external
       daemon installers.
    """
    try:
        if FOUNDRY_MANAGER is None:
            return correct_text_with_ollama(text)
        model = FOUNDRY_MANAGER.catalog.get_model(MODEL_NAME)
        if not model.is_downloaded:
            print(f"\U0001f4e5 Downloading model ({MODEL_NAME}) via Foundry Catalog...")
            model.download()
        if not model.is_loaded:
            print("\u2699\ufe0f Loading model into hardware accelerator (NPU/GPU/CPU)...")
            model.load()

        client = model.get_chat_client()
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text.strip()},
        ]
        response = client.complete_chat(messages)
        content = response.choices[0].message.content
        if isinstance(content, str):
            return content.strip()
        return correct_text_with_ollama(text)
    except Exception:
        # Fallback to the local HTTP endpoint if the catalog model is
        # uninitialized on the local machine.
        return correct_text_with_ollama(text)


def correct_text_with_ollama(text: str) -> str:
    """Correct ``text`` via the local Ollama HTTP REST API endpoint."""
    full_prompt = f"{SYSTEM_PROMPT}\n\nInput text:\n{text.strip()}\n\nCorrected text:"
    try:
        response = requests.post(
            LOCAL_OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "num_predict": 128,
                },
            },
            timeout=10,
        )
        if response.status_code == 200:
            result = response.json().get("response", "")
            if isinstance(result, str):
                result = result.strip()
                if result.startswith('"') and result.endswith('"'):
                    result = result[1:-1]
                return result
            return text
        return text
    except Exception as e:
        print(f"\u26a0\ufe0f Local inference error: {e}")
        return text


def correct_text(text: str) -> str:
    """Route ``text`` to the best available grammar-correction backend."""
    if not text or not text.strip():
        return text

    if HAS_FOUNDRY_SDK and FOUNDRY_MANAGER is not None:
        try:
            return correct_text_with_foundry_sdk(text)
        except Exception:
            return correct_text_with_ollama(text)
    return correct_text_with_ollama(text)
