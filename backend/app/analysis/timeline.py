"""
Timeline construction -- STUB, not implemented.

TODO(analysis): Build a chronological view of decisions/events for a topic
or entity, so questions like "why did I make this decision?" or "what
happened with my thesis last month?" can be answered by walking a timeline
instead of a single similarity match. A real implementation would:
  1. Use timestamps attached to chunks/entities (see
     app/retrieval/temporal.py) plus knowledge-graph relationships (see
     app/graph.py, e.g. DECIDED / CAUSED_BY / FOLLOWED_BY edges) to order
     events and decisions related to a topic.
  2. For a given decision/event, walk backwards through causally/temporally
     linked entities to answer "why" questions with cited provenance.
  3. Expose a queryable timeline (e.g. a `/graph/timeline` endpoint,
     mirroring the existing /graph/entities stub) once the underlying graph
     and temporal retrieval pieces are implemented.

No timeline construction logic exists here -- calling build_timeline() raises
NotImplementedError rather than returning fabricated results.
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TimelineEvent:
    timestamp: datetime
    description: str
    source_path: str


def build_timeline(topic: str) -> list[TimelineEvent]:
    """STUB: build a chronological timeline of events/decisions about `topic`. Not implemented."""
    raise NotImplementedError(
        "Timeline construction is not implemented yet. See module docstring "
        "in app/analysis/timeline.py for the intended design."
    )
