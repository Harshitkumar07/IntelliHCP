"""
SQLAlchemy declarative base.

Every ORM model inherits from `Base`. Centralising it here
avoids circular-import issues when models reference each other.
"""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative base class for all ORM models."""
    pass
