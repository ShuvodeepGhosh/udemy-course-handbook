from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
import uvicorn
from app.ingestion.ingest import ingest_transcript
from app.chunking.chunk_pipeline import build_vector_database

DEFAULT_TRANSCRIPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "transcripts"
    / "Udemy_transcript_Complete_Prompt_Engineerin.txt"
)

app = FastAPI(
    title="Course Handbook AI",
    description="Generate structured handbooks from course transcripts",
    version="1.0"
)

@app.get("/")
def health_check():
    return {"status": "running"}


@app.get("/test-ingest")
def test_ingestion(file_path: str = Query(default=str(DEFAULT_TRANSCRIPT_PATH))):
    """Run transcript ingestion pipeline for a provided transcript file path."""
    try:
        result = ingest_transcript(file_path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {exc}") from exc

    return result


@app.get("/test-vectorize")
def test_vectorization(file_path: str = Query(default=None)):
    """Run full Phase 3 pipeline: ingest → chunk → embed → vectorize."""
    try:
        # Use default path if not provided
        transcript_path = file_path or str(DEFAULT_TRANSCRIPT_PATH)
        
        # Step 1: Ingest transcript
        ingestion_data = ingest_transcript(transcript_path)
        
        # Step 2: Build vector database
        faiss_index, chunks = build_vector_database(ingestion_data["lectures"])
        
        # Step 3: Return results with metadata
        return {
            "file": transcript_path,
            "ingestion": {
                "lecture_count": ingestion_data["lecture_count"],
                "word_count": ingestion_data["word_count"],
            },
            "vectorization": {
                "total_chunks": len(chunks),
                "index_size": faiss_index.ntotal,
                "embedding_dimension": faiss_index.d,
                "sample_chunk": {
                    "text": chunks[0]["text"][:150] if chunks else None,
                    "lecture_id": chunks[0]["lecture_id"] if chunks else None,
                },
            },
        }
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Vectorization failed: {exc}") from exc


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)