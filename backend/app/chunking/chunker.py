"""Chunking utilities for transcript text and lecture segments."""

from __future__ import annotations

import importlib

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def _build_text_splitter():
    """Create a configured RecursiveCharacterTextSplitter instance."""
    try:
        module = importlib.import_module("langchain_text_splitters")
    except ImportError as exc:
        try:
            module = importlib.import_module("langchain.text_splitter")
        except ImportError as fallback_exc:
            raise ImportError(
                "LangChain text splitters are required. Install with: pip install langchain-text-splitters"
            ) from fallback_exc

    RecursiveCharacterTextSplitter = getattr(module, "RecursiveCharacterTextSplitter")

    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )


def chunk_text(text: str) -> list[str]:
    """Split a transcript string into overlapping text chunks.

    Args:
        text: Transcript text to split.

    Returns:
        List of chunk strings.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("chunk_text expects a string input")

    source = text.strip()
    if not source:
        return []

    splitter = _build_text_splitter()
    chunks = splitter.split_text(source)
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def chunk_lectures_with_metadata(lectures: list[str]) -> list[dict]:
    """Chunk each lecture and attach lecture metadata.

    Args:
        lectures: List of lecture transcript strings.

    Returns:
        List of dictionaries with chunk text and lecture id.
        Example item: {"text": "...", "lecture_id": 0}

    Raises:
        TypeError: If lectures is not a list of strings.
    """
    if not isinstance(lectures, list):
        raise TypeError("chunk_lectures_with_metadata expects a list input")

    splitter = _build_text_splitter()
    chunk_records: list[dict] = []

    for lecture_id, lecture_text in enumerate(lectures):
        if not isinstance(lecture_text, str):
            raise TypeError("Each lecture must be a string")

        lecture_source = lecture_text.strip()
        if not lecture_source:
            continue

        lecture_chunks = splitter.split_text(lecture_source)
        for chunk in lecture_chunks:
            cleaned_chunk = chunk.strip()
            if not cleaned_chunk:
                continue
            chunk_records.append(
                {
                    "text": cleaned_chunk,
                    "lecture_id": lecture_id,
                }
            )

    return chunk_records
