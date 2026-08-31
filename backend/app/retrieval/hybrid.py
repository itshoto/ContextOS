"""
Hybrid retrieval fusion -- STUB, not implemented.

TODO(hybrid-retrieval): The working slice (app/routers/query.py) currently
does plain pgvector cosine-similarity search only. ContextOS's actual target
is a hybrid pipeline that combines multiple signals so cross-source,
time-aware, entity-aware questions can be answered well:
  - Vector similarity search (implemented today, in app/routers/query.py)
  - BM25 / keyword search (app/retrieval/bm25.py -- stub)
  - Knowledge-graph traversal (app/graph.py -- stub; e.g. pull in chunks
    connected to entities mentioned in the question)
  - Temporal filtering/boosting (app/retrieval/temporal.py -- stub)

A real implementation would score/rank each source's candidates, fuse them
(e.g. Reciprocal Rank Fusion or a learned re-ranker), and return a single
ranked list of chunks for the LLM context -- replacing the single
pgvector-only query currently inlined in app/routers/query.py.

Only the intended function signature is defined below; it is not wired into
app/routers/query.py and raises NotImplementedError if called.
"""
from dataclasses import dataclass


@dataclass
class FusedResult:
    chunk_id: int
    path: str
    content: str
    score: float
    matched_by: list[str]  # e.g. ["vector", "bm25", "graph", "temporal"]


def retrieve(question: str, top_k: int = 5) -> list[FusedResult]:
    """STUB: fuse vector + BM25 + knowledge-graph + temporal retrieval. Not implemented."""
    raise NotImplementedError(
        "Hybrid retrieval fusion is not implemented yet. The working slice "
        "(app/routers/query.py) uses plain pgvector similarity search "
        "directly. See module docstring in app/retrieval/hybrid.py for the "
        "intended design."
    )
