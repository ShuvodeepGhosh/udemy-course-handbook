"""Lecture parsing utilities for transcript text."""

from __future__ import annotations

import re

BOUNDARY_PATTERN = re.compile(
    r"(?im)^\s*(?:"
    r"===\s*.+?\s*===|"
    r"---\s*.+?\s*---|"
    r"(?:lecture|lesson|module)\s+\d+\b[^\n]*|"
    r"\[no\s+transcript\s+available\s+for\s+this\s+lecture\]"
    r")\s*$"
)


def split_lectures(text: str) -> list[str]:
    """Split transcript text into lecture segments.

    The function detects common transcript boundaries, including:
    - Section headers wrapped with === ... ===
    - Lecture titles wrapped with --- ... ---
    - Markers like "Lecture 1", "Lesson 2", or "Module 3"
    - Placeholder markers for missing lecture text

    Args:
        text: Transcript text to parse.

    Returns:
        List of non-empty lecture segments.
    """
    if not isinstance(text, str):
        raise TypeError("split_lectures expects a string input")

    source = text.strip()
    if not source:
        return []

    markers = list(BOUNDARY_PATTERN.finditer(source))
    if not markers:
        return [source]

    lectures: list[str] = []

    if markers[0].start() > 0:
        intro = source[: markers[0].start()].strip()
        if intro:
            lectures.append(intro)

    for index, marker in enumerate(markers):
        start = marker.start()
        end = markers[index + 1].start() if index + 1 < len(markers) else len(source)
        segment = source[start:end].strip()
        if segment:
            lectures.append(segment)

    return lectures

