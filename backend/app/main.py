"""
FastAPI application factory and lifespan management.

Responsibilities:
  - Create the FastAPI app with metadata
  - Configure CORS for React frontend
  - Register the global exception handler
  - Run database table creation and seed on startup
  - Mount all API routers
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import router as v1_router
from app.core.config import settings
from app.core.exceptions import AppError
from app.core.logging import get_logger, setup_logging
from app.database.base import Base
from app.database.engine import engine
from app.database.seed import seed_database
from app.models import Doctor, Interaction, Product  # noqa: F401 — register models

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan — runs on startup and shutdown."""
    # ── Startup ──────────────────────────────────────────
    setup_logging()
    logger.info("Starting %s...", settings.APP_NAME)

    # Create all tables (safe to call if they already exist)
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables ensured.")

    import os
    os.makedirs("logs", exist_ok=True)
    os.makedirs("uploads", exist_ok=True)
    logger.info("Required directories (logs/, uploads/) checked.")

    # Seed sample data
    seed_database()
    logger.info("Seed data checked.")

    yield

    # ── Shutdown ─────────────────────────────────────────
    logger.info("Shutting down %s.", settings.APP_NAME)


# ── App Factory ──────────────────────────────────────────

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-First CRM for Pharmaceutical HCP Interaction Logging",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Global Exception Handler ────────────────────────────

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    """Convert AppError subclasses to structured JSON responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message},
    )


# ── Routes ───────────────────────────────────────────────

app.include_router(v1_router, prefix=settings.API_V1_PREFIX)


# ── Health Check ─────────────────────────────────────────

@app.get("/health")
def health_check() -> dict:
    """Simple health check endpoint."""
    return {"status": "healthy", "app": settings.APP_NAME}
