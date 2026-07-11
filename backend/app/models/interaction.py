"""
Interaction ORM model.

Stores every HCP interaction logged through the AI assistant.
Uses JSONB for variable-length list fields (products, brochures, samples)
and enforces a constrained set of sentiment values.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime, time, timezone

from sqlalchemy import Date, DateTime, Enum, ForeignKey, String, Text, Time, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Interaction(Base):
    """Logged HCP interaction record."""

    __tablename__ = "interactions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    # ── HCP Reference ────────────────────────────────────
    doctor_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("doctors.id", ondelete="SET NULL"),
        nullable=True,
    )
    doctor_name: Mapped[str] = mapped_column(
        String(200), nullable=False, default=""
    )

    # ── Interaction Details ──────────────────────────────
    interaction_date: Mapped[date | None] = mapped_column(
        Date, nullable=True
    )
    interaction_time: Mapped[time | None] = mapped_column(
        Time, nullable=True
    )
    interaction_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="Meeting"
    )
    attendees: Mapped[str] = mapped_column(
        Text, nullable=False, default=""
    )

    # ── Content ──────────────────────────────────────────
    topics: Mapped[str] = mapped_column(
        Text, nullable=False, default=""
    )
    products: Mapped[list] = mapped_column(
        JSON, nullable=False, default=list
    )
    summary: Mapped[str] = mapped_column(
        Text, nullable=False, default=""
    )

    # ── Sentiment ────────────────────────────────────────
    sentiment: Mapped[str] = mapped_column(
        String(20), nullable=False, default="Neutral"
    )

    # ── Materials ────────────────────────────────────────
    brochures: Mapped[list] = mapped_column(
        JSON, nullable=False, default=list
    )
    samples: Mapped[list] = mapped_column(
        JSON, nullable=False, default=list
    )

    # ── Outcomes & Follow-up ─────────────────────────────
    outcomes: Mapped[str] = mapped_column(
        Text, nullable=False, default=""
    )
    follow_up: Mapped[str] = mapped_column(
        Text, nullable=False, default=""
    )
    follow_up_suggestions: Mapped[list] = mapped_column(
        JSON, nullable=False, default=list
    )

    # ── Metadata ─────────────────────────────────────────
    session_id: Mapped[str] = mapped_column(
        String(100), nullable=False, default=""
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # ── Relationships ────────────────────────────────────
    doctor = relationship("Doctor", backref="interactions", lazy="joined")

    def __repr__(self) -> str:
        return f"<Interaction(doctor='{self.doctor_name}', date={self.interaction_date})>"

    def to_dict(self) -> dict:
        """Serialise to a plain dict for Redux form consumption."""
        return {
            "interaction_id": str(self.id),
            "doctor_name": self.doctor_name,
            "interaction_date": self.interaction_date.isoformat() if self.interaction_date else "",
            "interaction_time": self.interaction_time.strftime("%H:%M") if self.interaction_time else "",
            "interaction_type": self.interaction_type,
            "attendees": self.attendees,
            "topics": self.topics,
            "products": self.products or [],
            "summary": self.summary,
            "sentiment": self.sentiment,
            "brochures": self.brochures or [],
            "samples": self.samples or [],
            "outcomes": self.outcomes,
            "follow_up": self.follow_up,
            "follow_up_suggestions": self.follow_up_suggestions or [],
        }
