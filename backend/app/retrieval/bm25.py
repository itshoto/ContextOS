"""
Keyword / BM25 retrieval -- STUB, not implemented.

TODO(hybrid-retrieval): The working slice (app/routers/query.py) currently
does vector-only retrieval via pgvector cosine distance. Pure vector search
misses exact-term matches (names, IDs, error codes, rare jargon) that BM25 /
keyword search handles well. A real implementation would:
  1. Maintain a keyword index over chunk content -- either Postgres full-text
     search (`tsvector`/`tsquery`, GIN index) to avoid a second datastore, or
     an external index (e.g. Elasticsearch/OpenSearch/Tantivy) if scale
     demands it.
  2. Given a query string, return the top-k chunk ids ranked by BM25 (or
     Postgres's `ts_rank`/`ts_rank_cd`) score.
  3. Feed those results into app/retrieval/hybrid.py to be fused with vector
     search results (and, later, knowledge-graph and temporal signals).

No index is built and no query is executed here -- calling search() raises
NotImplementedError rather than returning fabricated results.
"""
from dataclasses import dataclass


@dataclass
class KeywordResult:
    chunk_id: int
    score: float


def search(query: str, top_k: int = 5) -> list[KeywordResult]:
    """STUB: BM25/keyword search over indexed chunks. Not implemented."""
    raise NotImplementedError(
        "BM25 keyword retrieval is not implemented yet. See module docstring "
        "in app/retrieval/bm25.py for the intended design."
    )
