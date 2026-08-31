"""
Neo4j client wrapper -- STUB.

TODO(knowledge-graph): This is the intended home of ContextOS's automatic
knowledge-graph construction -- the piece that turns isolated chunks into a
connected graph across a person's documents, emails, notes, calendar, and
tasks. A real implementation would:
  1. On ingest, run entity + relationship extraction (NER and/or an LLM
     extraction prompt) over each chunk's text to pull out entities (people,
     organizations, projects, concepts, files, dates/events, decisions,
     tasks, etc.) AND the relationships between them (e.g. "Alice DECIDED
     TO use Postgres", "thesis TASK blocked_by advisor-feedback EVENT").
  2. Upsert those entities/relations into Neo4j as a knowledge graph, linked
     back to the source Chunk/Document ids for provenance, and merge
     duplicate/co-referring entities across sources over time.
  3. Expose graph queries (neighborhood expansion, shortest-path, "what
     connects to X", entity timelines) that routers/graph.py and the hybrid
     retrieval pipeline (see app/retrieval/hybrid.py) would combine with
     vector + keyword + temporal signals so cross-source questions like
     "what decisions did I make about my thesis last month, and what tasks
     are still unresolved?" can be answered by walking the graph, not just
     matching a single chunk.

None of that is implemented here. `connect()`/`close()` establish and tear
down a real Neo4j driver connection so the wiring is real, but no entities
are ever written or read -- see routers/graph.py, whose /graph/entities
endpoint always returns an empty list.
"""
from neo4j import Driver, GraphDatabase

from app.config import get_settings

_driver: Driver | None = None


def connect() -> Driver:
    """Create (if needed) and return the Neo4j driver singleton."""
    global _driver
    if _driver is None:
        settings = get_settings()
        _driver = GraphDatabase.driver(
            settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )
    return _driver


def close() -> None:
    """Close the Neo4j driver, if one was ever created."""
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None


def get_entities() -> list[dict]:
    """
    STUB: real entity-extraction / graph-query is not implemented.

    TODO(knowledge-graph): should query Neo4j for extracted entities, e.g.
        MATCH (e:Entity) RETURN e LIMIT $limit
    Always returns [] for now -- no fake data.
    """
    return []
