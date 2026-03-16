"""Utilities for loading transcript content from multiple file formats."""

from __future__ import annotations

from pathlib import Path

SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx", ".vtt"}


def detect_file_type(file_path: str) -> str:
    """Return the lowercase file extension for the given transcript path.

    Args:
        file_path: Path to a transcript file.

    Returns:
        Lowercase extension including the leading dot (for example, ".txt").

    Raises:
        ValueError: If the path has no file extension.
    """
    extension = Path(file_path).suffix.lower()
    if not extension:
        raise ValueError(f"Could not detect file type from path: {file_path}")
    return extension


def load_text_file(file_path: str) -> str:
    """Load transcript content from a plain text file."""
    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        return file.read()


def load_pdf(file_path: str) -> str:
    """Load transcript content from a PDF file using pypdf."""
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise ImportError(
            "pypdf is required to load PDF transcripts. Install it with: pip install pypdf"
        ) from exc

    try:
        reader = PdfReader(file_path)
        pages = [(page.extract_text() or "") for page in reader.pages]
        return "\n".join(pages)
    except Exception as exc:
        raise RuntimeError(f"Failed to read PDF transcript: {file_path}") from exc


def load_docx(file_path: str) -> str:
    """Load transcript content from a DOCX file using python-docx."""
    try:
        from docx import Document
    except ImportError as exc:
        raise ImportError(
            "python-docx is required to load DOCX transcripts. Install it with: pip install python-docx"
        ) from exc

    try:
        document = Document(file_path)
        paragraphs = [paragraph.text for paragraph in document.paragraphs]
        return "\n".join(paragraphs)
    except Exception as exc:
        raise RuntimeError(f"Failed to read DOCX transcript: {file_path}") from exc


def load_vtt(file_path: str) -> str:
    """Load transcript content from a VTT subtitle file using webvtt-py."""
    try:
        import webvtt
    except ImportError as exc:
        raise ImportError(
            "webvtt-py is required to load VTT transcripts. Install it with: pip install webvtt-py"
        ) from exc

    try:
        captions = webvtt.read(file_path)
        lines = [caption.text.strip() for caption in captions if caption.text.strip()]
        return "\n".join(lines)
    except Exception as exc:
        raise RuntimeError(f"Failed to read VTT transcript: {file_path}") from exc


def load_transcript(file_path: str) -> str:
    """Load transcript content by auto-detecting file format.

    Args:
        file_path: Path to the transcript file.

    Returns:
        Raw transcript text loaded from disk.

    Raises:
        FileNotFoundError: If the input path does not exist.
        ValueError: If the file extension is unsupported.
    """
    path = Path(file_path)
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Transcript file not found: {file_path}")

    extension = detect_file_type(file_path)
    loaders = {
        ".txt": load_text_file,
        ".pdf": load_pdf,
        ".docx": load_docx,
        ".vtt": load_vtt,
    }

    loader = loaders.get(extension)
    if loader is None:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ValueError(
            f"Unsupported transcript format '{extension}'. Supported formats: {supported}"
        )

    return loader(file_path)
