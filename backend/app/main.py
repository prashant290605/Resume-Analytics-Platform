from __future__ import annotations

import logging
import time
from contextlib import asynccontextmanager
from typing import AsyncIterator, Awaitable, Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.api.routes import router
from backend.app.core.config import get_settings
from backend.app.core.logging import configure_logging
from backend.app.db.database import Database
from backend.app.db.repository import ScreeningRepository
from backend.app.services.embeddings import MatchingEngine
from backend.app.services.screening import ScreeningService

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Composition root: build and wire long-lived dependencies once, at startup."""
    settings = get_settings()
    configure_logging(settings.log_level)

    app.state.database = Database()
    app.state.repository = ScreeningRepository(app.state.database)
    app.state.matching_engine = MatchingEngine()
    app.state.screening_service = ScreeningService(
        repository=app.state.repository,
        matching_engine=app.state.matching_engine,
    )
    logger.info(
        "startup complete (db=%s, embedding_provider=%s)",
        app.state.database.db_path,
        app.state.matching_engine.active_provider().name,
    )
    yield
    logger.info("shutdown complete")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="Resume Analytics Platform",
        version="2.0.0",
        description="API for resume ingestion, hybrid scoring, shortlisting, and interview email generation.",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def access_log(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info("%s %s -> %s (%.1f ms)", request.method, request.url.path, response.status_code, duration_ms)
        response.headers["X-Response-Time-Ms"] = f"{duration_ms:.1f}"
        return response

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("unhandled error on %s %s", request.method, request.url.path)
        return JSONResponse(status_code=500, content={"detail": "Internal server error."})

    if settings.enable_metrics:
        try:
            from prometheus_fastapi_instrumentator import Instrumentator

            Instrumentator(excluded_handlers=["/metrics"]).instrument(app).expose(app)
        except ImportError:  # pragma: no cover - metrics are optional
            logger.warning("prometheus-fastapi-instrumentator not installed; /metrics disabled")

    app.include_router(router)

    @app.get("/")
    async def root() -> dict[str, str]:
        return {"message": "Resume Analytics Platform API", "docs": "/docs", "health": "/api/health"}

    return app


app = create_app()
