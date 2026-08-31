"""
POST /ingest/documents

Accepts a batch of {path, content} documents, chunks + embeds each one, and
upserts (delete-then-recreate) their chunks in Postgres.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.chunking import chunk_text
from app.db import get_db
from app.embeddings import embed_texts
from app.models import Chunk, Document
from app.schemas import IngestRequest, IngestResponse

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("/documents", response_model=IngestResponse)
def ingest_documents(payload: IngestRequest, db: Session = Depends(get_db)) -> IngestResponse:
    documents_ingested = 0
    chunks_created = 0

    for doc in payload.documents:
        pieces = chunk_text(doc.content)
        if not pieces:
            continue

        existing = db.query(Document).filter(Document.path == doc.path).one_or_none()
        if existing is None:
            existing = Document(path=doc.path)
            db.add(existing)
            db.flush()  # assign existing.id
        else:
            # Upsert by path: drop old chunks, we'll recreate them below.
            db.query(Chunk).filter(Chunk.document_id == existing.id).delete()

        vectors = embed_texts(pieces)
        for idx, (piece, vector) in enumerate(zip(pieces, vectors)):
            db.add(
                Chunk(
                    document_id=existing.id,
                    content=piece,
                    chunk_index=idx,
                    embedding=vector,
                )
            )
            chunks_created += 1

        documents_ingested += 1

    db.commit()
    return IngestResponse(documents_ingested=documents_ingested, chunks_created=chunks_created)
