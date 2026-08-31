-- Enable the pgvector extension. Table creation itself is handled by
-- SQLAlchemy's Base.metadata.create_all() on backend startup (see app/main.py)
-- for simplicity in this skeleton project.
CREATE EXTENSION IF NOT EXISTS vector;
