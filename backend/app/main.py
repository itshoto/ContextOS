"""
FastAPI application factory / entrypoint.

Run with: uvicorn app.main:app --host 0.0.0.0 --port 8000
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db import Base, engine
from app.routers import graph, ingest, query


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup if they don't exist yet. Fine for a skeleton
    # project; a real deployment would use Alembic migrations instead.
    Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="ContextOS Backend", lifespan=lifespan)

    settings = get_settings()
    allowed_origins = [o.strip() for o in settings.CORS_ALLOWED_ORIGINS.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(ingest.router)
    app.include_router(query.router)
    app.include_router(graph.router)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    return app


app = create_app()
