"""
Application configuration, loaded from environment variables / a .env file.

Uses pydantic-settings so every value below can be overridden by setting the
corresponding environment variable (see ../../.env.example for the full list).
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- Postgres (pgvector) ---
    DATABASE_URL: str = "postgresql+psycopg://contextos:contextos@localhost:5432/contextos"

    # --- Redis (reserved for future caching / job queue use; not yet wired up) ---
    REDIS_URL: str = "redis://localhost:6379/0"

    # --- Neo4j (stubbed knowledge graph; see app/graph.py) ---
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "changeme"

    # --- LLM provider selection ---
    # "gemini" (default), "anthropic", or "openai"
    LLM_PROVIDER: str = "gemini"

    ANTHROPIC_API_KEY: str = ""
    # Current Claude model id as of this writing. Anthropic model ids change
    # over time -- if this stops working, check the latest available model
    # id and update here or override via the ANTHROPIC_MODEL env var.
    ANTHROPIC_MODEL: str = "claude-sonnet-5"

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # --- CORS ---
    # Comma-separated list of allowed origins for the browser extension (and
    # any other client) to call this API from. A Chrome extension's
    # background service worker calling a URL covered by its manifest's
    # host_permissions generally isn't subject to CORS the way a normal
    # webpage fetch is, but we add an explicit allowlist defensively anyway.
    CORS_ALLOWED_ORIGINS: str = "*"

    # --- Embeddings ---
    # sentence-transformers model used to embed both documents and queries.
    # all-MiniLM-L6-v2 produces 384-dimensional embeddings; if you change this,
    # also update the Vector(384) dimension in app/models.py.
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIM: int = 384


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance (env is read once per process)."""
    return Settings()
