"""
FastAPI dependency injection.

Provides reusable dependencies for database sessions
and other shared resources across API endpoints.
"""

from __future__ import annotations

from typing import Generator

from sqlalchemy.orm import Session

from app.database.engine import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and close it after the request.

    Usage in endpoints:
        @router.get("/items")
        def list_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
