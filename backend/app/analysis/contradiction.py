"""
Contradiction detection -- STUB, not implemented.

TODO(analysis): Detect when two indexed chunks/documents make conflicting
claims (e.g. two notes giving different answers to "which database are we
using"). A real implementation would:
  1. For a topic/entity, gather candidate chunks (via app/retrieval/hybrid.py
     once implemented).
  2. Use an LLM (see app/llm/client.py) or an NLI (natural language
     inference) model to classify pairs of claims as agreeing, unrelated, or
     contradictory.
  3. Surface contradictions with both source citations so the user can see
     *why* two pieces of context disagree, and when each was stated (see
     app/analysis/timeline.py for the "when" part).

No detection logic exists here -- calling find_contradictions() raises
NotImplementedError rather than returning fabricated results.
"""
from dataclasses import dataclass


@dataclass
class Contradiction:
    claim_a: str
    claim_b: str
    source_a: str
    source_b: str
    explanation: str


def find_contradictions(topic: str) -> list[Contradiction]:
    """STUB: detect conflicting claims across indexed sources about `topic`. Not implemented."""
    raise NotImplementedError(
        "Contradiction detection is not implemented yet. See module "
        "docstring in app/analysis/contradiction.py for the intended design."
    )
