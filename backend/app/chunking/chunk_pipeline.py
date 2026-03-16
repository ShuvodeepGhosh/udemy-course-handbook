"""Pipeline to build vector database from transcript lectures."""

from __future__ import annotations

from app.chunking.chunker import chunk_lectures_with_metadata
from app.embeddings.embedder import generate_embeddings
from app.vectorstore.faiss_store import create_faiss_index


def build_vector_database(lectures: list[str]):
    """Build a FAISS vector database from lecture transcripts.

    Pipeline:
    1. Chunk lectures with metadata
    2. Generate embeddings for chunks
    3. Build FAISS index

    Args:
        lectures: List of lecture transcript strings.

    Returns:
        Tuple of (faiss_index, chunks_with_metadata).

    Raises:
        ValueError: If there is no chunkable transcript content.
    """
    chunks = chunk_lectures_with_metadata(lectures)
    if not chunks:
        raise ValueError("No chunkable lecture content found")

    embeddings = generate_embeddings(chunks)
    index = create_faiss_index(embeddings)
    return index, chunks
