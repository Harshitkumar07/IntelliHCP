"""
Doctor (Healthcare Professional) ORM model.

Represents HCPs in the CRM system. Pre-seeded with sample data
so the search_doctor tool has records to query against.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Doctor(Base):
    """Healthcare Professional record."""

    __tablename__ = "doctors"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    hospital: Mapped[str] = mapped_column(String(300), nullable=False, default="")
    specialization: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    city: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<Doctor(name='{self.name}', specialization='{self.specialization}')>"

    def to_dict(self) -> dict:
        """Serialise to a plain dict for JSON responses."""
        return {
            "id": str(self.id),
            "name": self.name,
            "hospital": self.hospital,
            "specialization": self.specialization,
            "city": self.city,
        }
