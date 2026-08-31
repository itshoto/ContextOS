"""
Pydantic request/response schemas for the API routers.
"""
from pydantic import BaseModel, Field


class IngestDocument(BaseModel):
    path: str
    content: str


class IngestRequest(BaseModel):
    documents: list[IngestDocument]


class IngestResponse(BaseModel):
    documents_ingested: int
    chunks_created: int


class AskRequest(BaseModel):
    question: str
    top_k: int = Field(default=5, ge=1, le=50)


class SourceCitation(BaseModel):
    path: str
    score: float
    snippet: str


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceCitation]


class GraphEntity(BaseModel):
    """Placeholder shape for a future knowledge-graph entity. Not yet populated."""

    id: str
    name: str
    type: str
