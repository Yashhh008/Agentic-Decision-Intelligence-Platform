"""
ADIP — Knowledge Ingestion Script

Reads all enterprise documents, chunks them, generates embeddings,
and saves to the FAISS vector index.

Run ONCE before starting the backend:
    python -m backend.scripts.ingest_knowledge

Re-run whenever new documents are added to the knowledge base.
"""
import os
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.config.settings import settings
from backend.services.embedding_service import EmbeddingService
from backend.vectorstore.faiss_store import FAISSVectorStore
from backend.utils.logger import get_logger

logger = get_logger(__name__)

# Document type mapping based on folder name
FOLDER_TO_TYPE = {
    "playbooks": "playbook",
    "crm": "crm_record",
    "meetings": "meeting_transcript",
    "emails": "email",
    "support": "support_ticket",
    "product_docs": "product_documentation",
    "pricing": "pricing",
    "release_notes": "release_notes",
    "faq": "faq",
    "policies": "policy",
    "customers": "customer_profile",
}

# Folder names that contain customer-specific data
CUSTOMER_FOLDERS = {"crm", "meetings", "emails", "support"}

# Known customer ID prefixes in filenames
CUSTOMER_IDS = ["acme_corp", "techflow_inc", "buildify", "novasoft"]


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Splits text into overlapping chunks.

    Args:
        text: Full document text.
        chunk_size: Characters per chunk.
        overlap: Characters of overlap between chunks.

    Returns:
        List of text chunks.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end].strip())
        start += chunk_size - overlap
    return [c for c in chunks if len(c) > 50]  # skip tiny fragments


def extract_customer_id(filename: str, folder_name: str) -> str | None:
    """Infers customer_id from filename if applicable."""
    if folder_name not in CUSTOMER_FOLDERS:
        return None
    for cid in CUSTOMER_IDS:
        if cid in filename:
            return cid
    return None


def ingest_all_documents() -> int:
    """
    Main ingestion function.

    Returns:
        Total number of chunks indexed.
    """
    knowledge_root = Path(settings.knowledge_base_path)
    if not knowledge_root.exists():
        logger.error(f"Knowledge base path does not exist: {knowledge_root}")
        return 0

    embedder = EmbeddingService()
    all_vectors = []
    all_metadata = []

    doc_count = 0
    chunk_count = 0

    for folder in knowledge_root.iterdir():
        if not folder.is_dir():
            continue

        folder_name = folder.name
        doc_type = FOLDER_TO_TYPE.get(folder_name, "document")

        for file_path in folder.rglob("*.md"):
            text = file_path.read_text(encoding="utf-8")
            if not text.strip():
                continue

            customer_id = extract_customer_id(file_path.stem, folder_name)
            source = f"{folder_name}/{file_path.name}"

            chunks = chunk_text(text, settings.chunk_size, settings.chunk_overlap)
            for i, chunk in enumerate(chunks):
                chunk_id = f"{file_path.stem}_chunk_{i}"
                metadata = {
                    "chunk_id": chunk_id,
                    "content": chunk,
                    "source": source,
                    "document_type": doc_type,
                    "customer_id": customer_id,
                    "filename": file_path.name,
                }
                all_metadata.append(metadata)
                chunk_count += 1

            doc_count += 1
            logger.info(f"Processed: {source} -> {len(chunks)} chunks")

    if not all_metadata:
        logger.warning("No documents found to index.")
        return 0

    # Generate embeddings for all chunks at once
    logger.info(f"Generating embeddings for {chunk_count} chunks...")
    texts = [m["content"] for m in all_metadata]
    import numpy as np
    vectors = embedder.embed_batch(texts)

    # Save to FAISS
    store = FAISSVectorStore()
    store.save(vectors.astype("float32"), all_metadata)

    logger.info(
        f"[OK] Ingestion complete: {doc_count} documents, {chunk_count} chunks indexed."
    )
    return chunk_count


if __name__ == "__main__":
    print("Starting knowledge base ingestion...")
    count = ingest_all_documents()
    print(f"[OK] Done. {count} chunks indexed into FAISS.")
