"""Microsoft Foundry Local implementation of the application model contract."""

from __future__ import annotations

from functools import lru_cache

from foundry_local_sdk import Configuration, FoundryLocalManager
from foundry_local_sdk.exception import FoundryLocalException

from .config import AppConfig
from .domain import ErrorCategory
from .model_protocol import ModelResult

_APP_NAME = "local_chat_agent"


class FoundryLocalAdapter:
    """Answer questions with a locally loaded Microsoft Foundry Local model."""

    def __init__(self, config: AppConfig) -> None:
        self._manager = self._get_manager()
        model = self._manager.catalog.get_model(config.model_alias)
        if model is None:
            raise FoundryLocalException(
                f"Configured model alias is unavailable: {config.model_alias}"
            )

        if not model.is_cached:
            model.download()
        if not model.is_loaded:
            model.load()

        self._model = model
        self._client = model.get_chat_client()

    @staticmethod
    def _get_manager() -> FoundryLocalManager:
        if FoundryLocalManager.instance is None:
            FoundryLocalManager.initialize(Configuration(app_name=_APP_NAME))
        return FoundryLocalManager.instance

    def answer(self, question: str) -> ModelResult:
        """Request one non-streaming answer and translate SDK outcomes safely."""
        try:
            completion = self._client.complete_chat([{"role": "user", "content": question}])
            content = completion.choices[0].message.content
            if not content or not content.strip():
                return ModelResult.failure(ErrorCategory.INVALID_RESPONSE)
            return ModelResult.success(content)
        except TimeoutError:
            return ModelResult.failure(ErrorCategory.TIMEOUT)
        except (ConnectionError, OSError, FoundryLocalException):
            return ModelResult.failure(ErrorCategory.UNAVAILABLE)
        except (IndexError, AttributeError, TypeError, ValueError):
            return ModelResult.failure(ErrorCategory.INVALID_RESPONSE)


@lru_cache(maxsize=4)
def get_cached_adapter(model_alias: str) -> FoundryLocalAdapter:
    """Cache one adapter per model alias for the application process."""
    return FoundryLocalAdapter(AppConfig(model_alias=model_alias))
