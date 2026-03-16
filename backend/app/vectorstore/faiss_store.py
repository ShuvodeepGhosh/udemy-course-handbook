"""FAISS index creation and persistence utilities."""

from __future__ import annotations

from pathlib import Path

import faiss
import numpy as np


def _to_float32_array(embeddings) -> np.ndarray:
    """Convert embeddings input into a 2D float32 numpy array."""
    array = np.asarray(embeddings, dtype=np.float32)

    if array.size == 0:
        raise ValueError("Embeddings are empty; cannot create a FAISS index")

    if array.ndim != 2:
        raise ValueError("Embeddings must be a 2D array-like structure")

    return array


def create_faiss_index(embeddings):
    """Create a FAISS IndexFlatL2 index from embedding vectors.

    Args:
        embeddings: 2D list or numpy array of shape (n_vectors, embedding_dim).

    Returns:
        FAISS IndexFlatL2 containing all vectors.
    """
    vectors = _to_float32_array(embeddings)
    embedding_dim = vectors.shape[1]

    index = faiss.IndexFlatL2(embedding_dim)
    index.add(vectors)
    return index


def save_index(index, path: str) -> None:
    """Persist a FAISS index to disk.

    Args:
        index: FAISS index instance.
        path: Destination file path.
    """
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(output_path))


def load_index(path: str):
    """Load a FAISS index from disk.

    Args:
        path: Path to a persisted FAISS index file.

    Returns:
        Loaded FAISS index.

    Raises:
        FileNotFoundError: If index file does not exist.
    """
    index_path = Path(path)
    if not index_path.exists() or not index_path.is_file():
        raise FileNotFoundError(f"FAISS index file not found: {path}")

    return faiss.read_index(str(index_path))
