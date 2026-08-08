"""Custom exceptions for the YouTube-to-Blog engine."""



class AgentReachYTError(Exception):
    """Base exception for all application errors."""


class TranscriptDownloadError(AgentReachYTError):
    """Raised when transcript download fails."""

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.cause = cause


class TranscriptParseError(AgentReachYTError):
    """Raised when transcript parsing fails."""


class LLMConnectionError(AgentReachYTError):
    """Raised when the LLM service is unreachable."""


class LLMGenerationError(AgentReachYTError):
    """Raised when the LLM returns an error during generation."""
