"""Application configuration constants."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Immutable application settings."""

    model: str = "LFM2.5-2.6B-Q4_K_M.gguf"
    llm_backend: str = "llama-cpp"
    ollama_url: str = "http://192.168.29.60:11434/api/generate"
    llama_cpp_url: str = "http://192.168.29.60:11434/v1/chat/completions"
    subtitle_lang: str = "en"
    transcript_prefix: str = "transcript"
    max_transcript_chars: int = 6000
    num_predict: int = 1024
    temperature: float = 0.3
    request_timeout: int = 120
    subprocess_timeout: int = 60

    @property
    def api_url(self) -> str:
        if self.llm_backend == "ollama":
            return self.ollama_url
        return self.llama_cpp_url

    @property
    def system_prompt(self) -> str:
        return (
            "You are an SEO blog writer. Given a YouTube transcript, write a structured "
            "blog post with: a Meta Description (<=160 chars), an H1 title, H2 sections, "
            "bullet points, and a Conclusion. Sound human. Don't mention the transcript."
        )


settings = Settings()

MODEL = settings.model
LLM_BACKEND = settings.llm_backend
API_URL = settings.api_url
SYSTEM_PROMPT = settings.system_prompt
SUBTITLE_LANG = settings.subtitle_lang
TRANSCRIPT_PREFIX = settings.transcript_prefix
