"""CLI entrypoint for AI API Response Formatter."""

from __future__ import annotations

import argparse

from assistant.io_utils import format_output, read_input_payload, save_output
from assistant.llm_client import LLMClientError
from assistant.workflows import format_api_response


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Standardize messy API responses into clean JSON using Groq."
    )
    parser.add_argument(
        "--json",
        type=str,
        help="Raw API response payload as a JSON string.",
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Path to a file containing raw API response data.",
    )
    parser.add_argument(
        "--save-output",
        type=str,
        help="Optional file path to save formatted JSON output.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        payload = read_input_payload(raw_json=args.json, file_path=args.file)
        formatted = format_api_response(payload)
        output = format_output("AI API Response Formatter - Clean JSON", formatted)
        print(output)

        if args.save_output:
            save_output(args.save_output, output)
            print(f"Saved output to: {args.save_output}")
    except (ValueError, LLMClientError) as exc:
        print(f"Error: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
