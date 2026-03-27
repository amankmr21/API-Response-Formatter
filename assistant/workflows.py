"""Formatting workflow for unstructured API responses."""

from __future__ import annotations

import json

from assistant.llm_client import LLMClientError, generate_text

SYSTEM_PROMPT = """
You are a backend data normalization assistant.

Your job:
1) Convert messy API response content into clean, valid JSON.
2) Normalize inconsistent key names to snake_case.
3) Preserve important information and avoid dropping fields.
4) Standardize structure:
   - If response has record items, return:
     {
       "status": "...",
       "message": "...",
       "data": [ ...normalized objects... ],
       "meta": { ...optional metadata... }
     }
   - If response has a single object, "data" can still be a list with one object.
5) Fix data types where obvious (e.g., numeric strings -> numbers, "true"/"false" -> booleans).
6) Ensure output is strict JSON only.
7) Do not include markdown fences, notes, or explanations.

Return only JSON.
""".strip()


def _extract_json(text: str) -> str:
    """Extract JSON content even if model adds accidental wrappers."""
    candidate = text.strip()
    if candidate.startswith("```"):
        candidate = candidate.strip("`")
        if candidate.lower().startswith("json"):
            candidate = candidate[4:].strip()
    return candidate


def format_api_response(raw_payload: str) -> str:
    """Normalize and clean raw API response into standard JSON."""
    response_text = generate_text(SYSTEM_PROMPT, raw_payload)
    candidate = _extract_json(response_text)

    try:
        parsed = json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise LLMClientError(
            "Model output was not valid JSON. Try a simpler payload input."
        ) from exc

    return json.dumps(parsed, indent=2, ensure_ascii=True)
