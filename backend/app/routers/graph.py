"""
GET /graph/entities -- STUB. See app/graph.py for details on what a real
implementation would do. Always returns an empty list; no fake data.
"""
from fastapi import APIRouter

from app.graph import get_entities
from app.schemas import GraphEntity

router = APIRouter(prefix="/graph", tags=["graph"])


@router.get("/entities", response_model=list[GraphEntity])
def list_entities() -> list[GraphEntity]:
    """
    STUB endpoint. TODO(knowledge-graph): once app.graph implements real
    entity extraction and Neo4j storage, this should return the extracted
    entities (optionally filtered/paginated). For now it always returns [].
    """
    return get_entities()
