"""
POST /query/ask

Embeds the question, runs a pgvector cosine-distance nearest-neighbor search
for the top-k most relevant chunks, assembles them into a context block, and
calls the configured LLM provider for a grounded answer with citations.
"""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.embeddings import embed_texts
from app.llm.client import get_llm_client
from app.models import Chunk, Document
from app.schemas import AskRequest, AskResponse, SourceCitation

router = APIRouter(prefix="/query", tags=["query"])


@router.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest, db: Session = Depends(get_db)) -> AskResponse:
    [question_vector] = embed_texts([payload.question])

    # pgvector's `<=>` operator is cosine distance (0 = identical, 2 = opposite).
    # We convert to a similarity score (1 - distance) for the response.
    distance = Chunk.embedding.cosine_distance(question_vector)
    stmt = (
        select(Chunk, Document.path, distance.label("distance"))
        .join(Document, Chunk.document_id == Document.id)
        .order_by(distance)
        .limit(payload.top_k)
    )
    rows = db.execute(stmt).all()

    if not rows:
        return AskResponse(
            answer=(
                "No indexed content found yet. Run 'ContextOS: Index Workspace' "
                "first, then ask again."
            ),
            sources=[],
        )

    context_blocks = []
    sources: list[SourceCitation] = []
    for chunk, path, dist in rows:
        score = 1.0 - float(dist)
        context_blocks.append(f"[{path}]\n{chunk.content}")
        snippet = chunk.content[:200] + ("..." if len(chunk.content) > 200 else "")
        sources.append(SourceCitation(path=path, score=score, snippet=snippet))

    context = "\n\n---\n\n".join(context_blocks)

    llm = get_llm_client()
    answer = llm.complete(question=payload.question, context=context)

    return AskResponse(answer=answer, sources=sources)
