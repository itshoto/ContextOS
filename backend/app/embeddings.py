"""
Lazily-loaded singleton wrapper around a sentence-transformers embedding model.

The model is loaded once per process on first use (not at import time), so
importing this module stays cheap and fast (e.g. for tests / tooling that
never actually call embed_texts).
"""
import threading

from app.config import get_settings

_model = None
_model_lock = threading.Lock()


def _get_model():
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                # Imported lazily: sentence-transformers/torch are heavy and
                # slow to import, so we defer that cost until embeddings are
                # actually needed.
                from sentence_transformers import SentenceTransformer

                settings = get_settings()
                _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a batch of texts, returning one vector (list[float]) per text."""
    if not texts:
        return []
    model = _get_model()
    vectors = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    return [vector.tolist() for vector in vectors]
