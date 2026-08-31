"""
A simple recursive character text splitter.

No external dependencies -- splits on a preference order of separators
(paragraph, line, sentence, word, character) trying to keep chunks close to
`chunk_size` characters, with `chunk_overlap` characters of overlap between
consecutive chunks so context isn't lost at chunk boundaries.
"""

DEFAULT_CHUNK_SIZE = 500
DEFAULT_CHUNK_OVERLAP = 50

_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]


def _split_text(text: str, separators: list[str]) -> list[str]:
    if not separators:
        return [text]

    sep, *rest = separators
    if sep == "":
        return list(text)

    parts = text.split(sep)
    if len(parts) == 1:
        # separator not found, try the next one
        return _split_text(text, rest)

    # Re-attach the separator (except to the last, empty tail) so we don't lose it.
    return [p + sep if i < len(parts) - 1 else p for i, p in enumerate(parts)]


def chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[str]:
    """Split `text` into overlapping chunks of roughly `chunk_size` characters."""
    if not text or not text.strip():
        return []

    if len(text) <= chunk_size:
        return [text]

    pieces = _split_text(text, _SEPARATORS)

    chunks: list[str] = []
    current = ""
    for piece in pieces:
        if len(current) + len(piece) <= chunk_size:
            current += piece
            continue

        if current:
            chunks.append(current)

        if len(piece) <= chunk_size:
            # start new chunk with overlap taken from the end of the previous one
            overlap = current[-chunk_overlap:] if chunk_overlap and current else ""
            current = overlap + piece
        else:
            # piece itself is too big (e.g. no separators found) -- hard-split it
            for i in range(0, len(piece), chunk_size - chunk_overlap):
                sub = piece[i : i + chunk_size]
                if sub:
                    chunks.append(sub)
            current = ""

    if current:
        chunks.append(current)

    return [c for c in chunks if c.strip()]
