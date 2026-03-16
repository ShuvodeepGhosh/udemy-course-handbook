"""Embedding generation for transcript chunks."""

from __future__ import annotations

from functools import lru_cache
import importlib

MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def _get_model():
    """Load and cache the sentence-transformers model."""
    try:
        module = importlib.import_module("sentence_transformers")
    except ImportError as exc:
        raise ImportError(
            "sentence-transformers is required for embeddings. Install it with: pip install sentence-transformers"
        ) from exc

    SentenceTransformer = getattr(module, "SentenceTransformer")

    return SentenceTransformer(MODEL_NAME)


def generate_embeddings(chunks: list[dict]) -> list:
    """Generate embeddings for chunk dictionaries.

    Args:
        chunks: List of chunk records. Each record should contain a "text" key.

    Returns:
        List of embedding vectors.

    Raises:
        TypeError: If chunks has invalid structure.
        ValueError: If chunk text values are empty.
    """
    if not isinstance(chunks, list):
        raise TypeError("generate_embeddings expects a list of chunk dictionaries")

    if not chunks:
        return []

    texts: list[str] = []
    for chunk in chunks:
        if not isinstance(chunk, dict):
            raise TypeError("Each chunk must be a dictionary")
        text = chunk.get("text")
        if not isinstance(text, str):
            raise TypeError("Each chunk dictionary must contain a string 'text' field")
        normalized = text.strip()
        if not normalized:
            raise ValueError("Chunk text must not be empty")
        texts.append(normalized)

    model = _get_model()
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    return embeddings.tolist()
