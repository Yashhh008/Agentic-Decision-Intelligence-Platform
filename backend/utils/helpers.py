"""
ADIP — General Helpers

Utility functions that do not belong to any specific domain.
"""
import json
import re
from datetime import datetime
from typing import Any


def utc_now_iso() -> str:
    """Returns the current UTC timestamp in ISO 8601 format."""
    return datetime.utcnow().isoformat() + "Z"


def extract_json_from_text(text: str) -> dict[str, Any]:
    """
    Attempts to extract a JSON object from a raw LLM text response.

    Handles cases where the model wraps JSON in markdown fences.

    Args:
        text: Raw LLM output string.

    Returns:
        Parsed dictionary.

    Raises:
        ValueError: If no valid JSON can be extracted.
    """
    # Strip markdown code fences if present
    match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", text)
    if match:
        json_str = match.group(1)
    else:
        # Try to find the first { ... } block
        match = re.search(r"\{[\s\S]+\}", text)
        if match:
            json_str = match.group(0)
        else:
            raise ValueError(f"No JSON found in LLM response: {text[:200]}")

    return json.loads(json_str)


def truncate_text(text: str, max_length: int = 300) -> str:
    """Truncates a string to max_length, appending ellipsis if needed."""
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + "..."
