"""Text cleaning utilities for transcript normalization."""

from __future__ import annotations

import re

TIMESTAMP_RANGE_PATTERN = re.compile(
    r"\b\d{1,2}:\d{2}:\d{2}(?:\.\d{1,3})?\s*-->\s*\d{1,2}:\d{2}:\d{2}(?:\.\d{1,3})?\b"
)
TIMESTAMP_PATTERN = re.compile(r"\b\d{1,2}:\d{2}:\d{2}(?:\.\d{1,3})?\b")
SUBTITLE_INDEX_PATTERN = re.compile(r"(?m)^\s*\d+\s*$")
VTT_HEADER_PATTERN = re.compile(r"(?im)^\s*WEBVTT\s*$")
NOTE_LINE_PATTERN = re.compile(r"(?im)^\s*NOTE\b.*$")
STYLE_LINE_PATTERN = re.compile(r"(?im)^\s*(STYLE|REGION)\b.*$")
TAG_PATTERN = re.compile(r"<[^>]+>")
WHITESPACE_PATTERN = re.compile(r"\s+")


def clean_text(text: str) -> str:
    """Clean and normalize transcript text into a continuous string.

    The cleaner removes common subtitle artifacts such as timestamps,
    cue indices, VTT headers, and inline formatting tags.

    Args:
        text: Raw transcript text.

    Returns:
        A cleaned single-string transcript suitable for downstream parsing.
    """
    if not isinstance(text, str):
        raise TypeError("clean_text expects a string input")

    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    normalized = VTT_HEADER_PATTERN.sub(" ", normalized)
    normalized = NOTE_LINE_PATTERN.sub(" ", normalized)
    normalized = STYLE_LINE_PATTERN.sub(" ", normalized)
    normalized = TIMESTAMP_RANGE_PATTERN.sub(" ", normalized)
    normalized = TIMESTAMP_PATTERN.sub(" ", normalized)
    normalized = SUBTITLE_INDEX_PATTERN.sub(" ", normalized)
    normalized = TAG_PATTERN.sub(" ", normalized)

    # Remove cue settings like "align:start position:0%" that leak into raw subtitle text.
    normalized = re.sub(r"(?im)^\s*\w+:[^\n]+$", " ", normalized)

    cleaned = WHITESPACE_PATTERN.sub(" ", normalized).strip()
    return cleaned

