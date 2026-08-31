"""
Automatic task extraction -- STUB, not implemented.

TODO(analysis): Pull out actionable tasks (todos, open action items,
unresolved questions) mentioned across notes/emails/documents, e.g. so
"what tasks are still unresolved about my thesis?" can be answered directly
instead of requiring the user to re-read every note. A real implementation
would:
  1. Run an LLM extraction pass (see app/llm/client.py) or a rules/NER pass
     over chunk text to identify task-like statements ("need to", "TODO",
     "follow up on", explicit checklist items) and their status (open/done)
     if stated.
  2. Link extracted tasks back to source chunks/documents and, where
     possible, to knowledge-graph entities (app/graph.py) and a timestamp
     (app/analysis/timeline.py) so tasks can be filtered by topic or recency.
  3. Store tasks (new table, not yet modeled) so they can be queried
     independently of a full RAG question -- e.g. "list my open tasks".

No extraction logic exists here -- calling extract_tasks() raises
NotImplementedError rather than returning fabricated results.
"""
from dataclasses import dataclass


@dataclass
class ExtractedTask:
    description: str
    status: str  # "open" | "done" | "unknown"
    source_path: str


def extract_tasks(text: str, source_path: str) -> list[ExtractedTask]:
    """STUB: extract action items from `text`. Not implemented."""
    raise NotImplementedError(
        "Task extraction is not implemented yet. See module docstring in "
        "app/analysis/tasks.py for the intended design."
    )
