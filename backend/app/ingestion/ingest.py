"""High-level transcript ingestion pipeline."""

from __future__ import annotations

from .cleaner import clean_text
from .loader import load_transcript
from .parser import split_lectures


def ingest_transcript(file_path: str) -> dict:
    """Ingest a transcript file into a structured dictionary.

    Pipeline:
    1. Load transcript from disk
    2. Split transcript into lecture segments
    3. Clean and normalize text
    4. Compute metadata

    Args:
        file_path: Path to transcript file.

    Returns:
        Dictionary containing cleaned text, lecture list, and metadata.
    """
    raw_text = load_transcript(file_path)

    raw_lectures = split_lectures(raw_text)
    lectures = []
    for lecture in raw_lectures:
        cleaned_lecture = clean_text(lecture)
        if not cleaned_lecture:
            continue
        if cleaned_lecture.lower() == "[no transcript available for this lecture]":
            continue
        lectures.append(cleaned_lecture)

    cleaned_transcript = clean_text(raw_text)

    return {
        "text": cleaned_transcript,
        "lectures": lectures,
        "lecture_count": len(lectures),
        "word_count": len(cleaned_transcript.split()) if cleaned_transcript else 0,
    }

