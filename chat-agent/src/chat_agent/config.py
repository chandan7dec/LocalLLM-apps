"""Application configuration for the local chat agent."""

from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_MODEL_ALIAS = "qwen2.5-0.5b"
MODEL_ALIAS_ENV = "CHAT_AGENT_MODEL_ALIAS"


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Runtime configuration loaded from the local environment."""

    model_alias: str = DEFAULT_MODEL_ALIAS

    @classmethod
    def from_env(cls) -> AppConfig:
        """Build configuration from environment variables with safe defaults."""
        model_alias = os.getenv(MODEL_ALIAS_ENV, DEFAULT_MODEL_ALIAS).strip()
        return cls(model_alias=model_alias or DEFAULT_MODEL_ALIAS)
