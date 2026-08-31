"""
Small LLM provider abstraction.

`get_llm_client()` returns a `GeminiClient`, `AnthropicClient`, or
`OpenAIClient` depending on `settings.LLM_PROVIDER`. Provider SDKs are
imported lazily inside each client's `__init__` (not at module import time)
so the app can start even if one of the SDKs / API keys isn't configured --
the error only surfaces when that provider is actually selected and used, as
a clear HTTPException rather than a crash at import time.
"""
from abc import ABC, abstractmethod

from fastapi import HTTPException

from app.config import get_settings

SYSTEM_PROMPT = (
    "You are ContextOS, a personal knowledge assistant. Answer the user's "
    "question using ONLY the provided context chunks. If the context does not "
    "contain enough information to answer, say so clearly instead of "
    "guessing. Be concise."
)


class LLMClient(ABC):
    @abstractmethod
    def complete(self, question: str, context: str) -> str:
        """Return a grounded answer to `question` given `context`."""
        raise NotImplementedError


class AnthropicClient(LLMClient):
    def __init__(self) -> None:
        settings = get_settings()
        if not settings.ANTHROPIC_API_KEY:
            raise HTTPException(
                status_code=400,
                detail=(
                    "ANTHROPIC_API_KEY is not set. Add it to your .env file "
                    "(see .env.example) to use the Anthropic LLM provider."
                ),
            )
        import anthropic

        self._client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self._model = settings.ANTHROPIC_MODEL

    def complete(self, question: str, context: str) -> str:
        response = self._client.messages.create(
            model=self._model,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {question}",
                }
            ],
        )
        text_blocks = [block.text for block in response.content if block.type == "text"]
        return "".join(text_blocks)


class OpenAIClient(LLMClient):
    def __init__(self) -> None:
        settings = get_settings()
        if not settings.OPENAI_API_KEY:
            raise HTTPException(
                status_code=400,
                detail=(
                    "OPENAI_API_KEY is not set. Add it to your .env file "
                    "(see .env.example) to use the OpenAI LLM provider."
                ),
            )
        import openai

        self._client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self._model = settings.OPENAI_MODEL

    def complete(self, question: str, context: str) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {question}",
                },
            ],
        )
        return response.choices[0].message.content or ""


class GeminiClient(LLMClient):
    def __init__(self) -> None:
        settings = get_settings()
        if not settings.GEMINI_API_KEY:
            raise HTTPException(
                status_code=400,
                detail=(
                    "GEMINI_API_KEY is not set. Add it to your .env file "
                    "(see .env.example) to use the Gemini LLM provider."
                ),
            )
        import google.generativeai as genai

        genai.configure(api_key=settings.GEMINI_API_KEY)
        self._model = genai.GenerativeModel(
            settings.GEMINI_MODEL, system_instruction=SYSTEM_PROMPT
        )

    def complete(self, question: str, context: str) -> str:
        response = self._model.generate_content(
            f"Context:\n{context}\n\nQuestion: {question}"
        )
        return response.text or ""


def get_llm_client() -> LLMClient:
    settings = get_settings()
    if settings.LLM_PROVIDER == "gemini":
        return GeminiClient()
    if settings.LLM_PROVIDER == "anthropic":
        return AnthropicClient()
    if settings.LLM_PROVIDER == "openai":
        return OpenAIClient()
    raise HTTPException(
        status_code=400,
        detail=(
            f"Unknown LLM_PROVIDER '{settings.LLM_PROVIDER}'. "
            "Use 'gemini', 'anthropic', or 'openai'."
        ),
    )
