"""LLM querying using local llama.cpp server (OpenAI-compatible API)."""

import requests


LLM_URL = "http://192.168.29.60:11434/v1/chat/completions"
MODEL_NAME = "llama-3.2-3b-instruct.Q4_K_M"


def query_llm(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful document analysis assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "stream": False
    }
    try:
        res = requests.post(LLM_URL, json=payload, timeout=300)
        res.raise_for_status()
        data = res.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Local LLM Processing Error: {e}"
