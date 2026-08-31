"""
Temporal (time-scoped) retrieval -- STUB, not implemented.

TODO(hybrid-retrieval): Many real questions are implicitly time-scoped --
"what did I decide about my thesis LAST MONTH", "what happened THIS WEEK".
A real implementation would:
  1. Extract or attach timestamps to chunks/entities at ingest time -- either
     document metadata (email date, note creation time, calendar event time)
     or dates mentioned in the text itself (via NER/date parsing).
  2. Parse the temporal scope out of a natural-language question (e.g. "last
     month", "in Q1", "since Tuesday") into a concrete date range.
  3. Filter/boost retrieval results whose timestamp falls in that range, and
     support explicitly time-ordered queries (build a chronological view of
     events for a topic -- see app/analysis/timeline.py, which this feeds).
  4. Feed those results into app/retrieval/hybrid.py to be fused with vector,
     keyword, and knowledge-graph signals.

No date extraction or filtering happens here -- calling search() raises
NotImplementedError rather than returning fabricated results.
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TemporalResult:
    chunk_id: int
    timestamp: datetime
    score: float


def search(query: str, start: datetime | None = None, end: datetime | None = None, top_k: int = 5) -> list[TemporalResult]:
    """STUB: time-scoped retrieval over indexed chunks/entities. Not implemented."""
    raise NotImplementedError(
        "Temporal retrieval is not implemented yet. See module docstring in "
        "app/retrieval/temporal.py for the intended design."
    )
