"""Reusable Groq API client wrapper."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from groq import APIConnectionError, APIStatusError, Groq, RateLimitError

load_dotenv()

DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


class LLMClientError(Exception):
    """Raised when the LLM client fails to generate a response."""


def _build_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise LLMClientError(
            "Missing GROQ_API_KEY. Set it in your environment or .env file."
        )
    return Groq(api_key=api_key)


def generate_text(task_prompt: str, user_text: str) -> str:
    """Generate text from Groq using a system prompt and user content."""
    if not user_text.strip():
        raise LLMClientError("Input payload is empty. Provide data to format.")

    client = _build_client()

    try:
        completion = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": task_prompt},
                {"role": "user", "content": user_text.strip()},
            ],
            temperature=0.1,
        )
        content = completion.choices[0].message.content
        if not content:
            raise LLMClientError("The model returned an empty response.")
        return content.strip()
    except RateLimitError as exc:
        raise LLMClientError(
            "Rate limit reached on Groq API. Please wait and try again."
        ) from exc
    except APIConnectionError as exc:
        raise LLMClientError(
            "Unable to connect to Groq API. Check your internet connection."
        ) from exc
    except APIStatusError as exc:
        raise LLMClientError(
            f"Groq API error ({exc.status_code}): {exc.message}"
        ) from exc
