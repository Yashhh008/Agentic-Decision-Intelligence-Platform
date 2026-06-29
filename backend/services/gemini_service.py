"""
ADIP — Gemini Service

Central LLM abstraction layer.
All agents and engines use this service — nothing communicates with Gemini directly.

Uses the current google-genai SDK (replaces the deprecated google-generativeai).

Responsibilities:
- Send prompts to Gemini
- Handle retries and timeouts
- Return structured JSON responses
- Provide fallback on repeated failure
- Skip retries immediately on 429 quota errors
"""
from __future__ import annotations

import asyncio
from typing import Any

from google import genai
from google.genai import types as genai_types

from backend.config.settings import settings
from backend.utils.helpers import extract_json_from_text
from backend.utils.logger import get_logger

logger = get_logger(__name__)

# Error codes that should NOT be retried
_NO_RETRY_CODES = {"429", "RESOURCE_EXHAUSTED", "QUOTA_EXCEEDED"}


def _is_quota_error(exc: Exception) -> bool:
    """Returns True if the exception is a quota/rate-limit error."""
    msg = str(exc).upper()
    return any(code in msg for code in _NO_RETRY_CODES)


class GeminiService:
    """
    Wrapper around the Google Gemini API (google-genai SDK).

    Usage:
        service = GeminiService()
        result = await service.generate_json(prompt)
        text   = await service.generate_text(prompt)
    """

    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not set in environment variables.")
        self._client = genai.Client(api_key=settings.gemini_api_key)
        self._model = settings.gemini_model
        logger.info(f"GeminiService initialized with model: {self._model}")

    async def generate_json(
        self, prompt: str, fallback: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Generates a JSON response from Gemini.

        Args:
            prompt: The full prompt including schema instructions.
            fallback: Returned if all retries fail.

        Returns:
            Parsed JSON dict.
        """
        try:
            raw = await self._call_with_retry(prompt)
            return extract_json_from_text(raw)
        except Exception as exc:
            logger.error(f"GeminiService.generate_json failed after retries: {exc}")
            if fallback is not None:
                return fallback
            raise

    async def generate_text(self, prompt: str, fallback: str | None = None) -> str:
        """
        Generates a plain-text response from Gemini.

        Args:
            prompt: The full prompt.
            fallback: Returned if all retries fail. If None, a generic message is used.

        Returns:
            Raw text string.
        """
        try:
            return await self._call_with_retry(prompt)
        except Exception as exc:
            logger.error(f"GeminiService.generate_text failed: {exc}")
            if fallback is not None:
                return fallback
            return "Analysis complete. Review the signals and retrieved knowledge for context."

    async def _call_with_retry(self, prompt: str) -> str:
        """Calls Gemini with exponential backoff retry. Skips retries on quota errors."""
        for attempt in range(1, settings.llm_max_retries + 1):
            try:
                # Run synchronous Gemini call in thread pool to avoid blocking event loop
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: self._client.models.generate_content(
                        model=self._model,
                        contents=prompt,
                        config=genai_types.GenerateContentConfig(
                            temperature=0.2,
                            max_output_tokens=2048,
                        ),
                    )
                )
                # SDK may return text via .text or via candidates
                text = None
                if response:
                    if response.text:
                        text = response.text
                    elif response.candidates:
                        try:
                            text = response.candidates[0].content.parts[0].text
                        except (IndexError, AttributeError):
                            pass
                if text:
                    return text
                raise ValueError("Empty response from Gemini")
            except Exception as exc:
                if _is_quota_error(exc):
                    logger.warning(f"Gemini quota/rate-limit hit — skipping retries: {exc}")
                    raise  # Don't retry quota errors, go straight to fallback
                logger.warning(f"Gemini attempt {attempt}/{settings.llm_max_retries} failed: {exc}")
                if attempt < settings.llm_max_retries:
                    await asyncio.sleep(2 ** attempt)  # exponential backoff
                else:
                    raise
        raise RuntimeError("All Gemini retries exhausted")
