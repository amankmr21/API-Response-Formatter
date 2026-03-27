"""Input/output helpers for API response formatter."""

from __future__ import annotations

from pathlib import Path


def read_input_payload(raw_json: str | None, file_path: str | None) -> str:
    """Read raw payload from direct input or file."""
    if not raw_json and not file_path:
        raise ValueError("Provide input using --json or --file.")

    if raw_json and file_path:
        raise ValueError("Use one input source only: --json or --file.")

    if raw_json:
        payload = raw_json.strip()
    else:
        path = Path(file_path or "")
        if not path.exists():
            raise ValueError(f"Input file not found: {file_path}")
        payload = path.read_text(encoding="utf-8").strip()

    if not payload:
        raise ValueError("Input payload is empty.")
    return payload


def save_output(path: str, content: str) -> None:
    """Persist text output to a file."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")


def format_output(title: str, json_text: str) -> str:
    """Pretty CLI display."""
    return f"{title}\n{'=' * len(title)}\n\n{json_text}"
