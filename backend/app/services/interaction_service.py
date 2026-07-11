"""
Interaction service — CRUD operations for HCP interactions.

This is the single source of truth for database reads/writes
on the interactions table. Both the API endpoints and LangGraph
tools delegate here.

WHY a service layer?
  - Keeps DB logic out of API handlers and tools (SRP)
  - Makes business rules testable without HTTP or LangGraph
  - Centralises commit/rollback semantics
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.core.logging import get_logger
from app.models.interaction import Interaction

logger = get_logger(__name__)


class InteractionService:
    """Stateless service with class-methods for interaction CRUD."""

    @staticmethod
    def create(db: Session, data: dict[str, Any], session_id: str = "") -> Interaction:
        """Create a new interaction record.

        Args:
            db: Active database session.
            data: Normalised interaction fields (from InteractionNormalizer).
            session_id: Chat session identifier for audit trail.

        Returns:
            The created Interaction ORM instance.
        """
        interaction = Interaction(
            doctor_name=data.get("doctor_name", ""),
            interaction_date=data.get("interaction_date"),
            interaction_time=data.get("interaction_time"),
            interaction_type=data.get("interaction_type", "Meeting"),
            attendees=data.get("attendees", ""),
            topics=data.get("topics", ""),
            products=data.get("products", []),
            summary=data.get("summary", ""),
            sentiment=data.get("sentiment", "Neutral"),
            brochures=data.get("brochures", []),
            samples=data.get("samples", []),
            outcomes=data.get("outcomes", ""),
            follow_up=data.get("follow_up", ""),
            follow_up_suggestions=data.get("follow_up_suggestions", []),
            session_id=session_id,
        )
        db.add(interaction)
        db.commit()
        db.refresh(interaction)

        logger.info(
            "Created interaction %s for doctor '%s'",
            interaction.id,
            interaction.doctor_name,
        )
        return interaction

    @staticmethod
    def get_by_id(db: Session, interaction_id: str) -> Interaction:
        """Retrieve an interaction by its UUID.

        Raises:
            NotFoundError: If the interaction does not exist.
        """
        try:
            uid = uuid.UUID(interaction_id)
        except ValueError as exc:
            raise NotFoundError("Interaction", interaction_id) from exc

        stmt = select(Interaction).where(Interaction.id == uid)
        interaction = db.execute(stmt).scalar_one_or_none()

        if interaction is None:
            raise NotFoundError("Interaction", interaction_id)
        return interaction

    @staticmethod
    def update(
        db: Session,
        interaction_id: str,
        updates: dict[str, Any],
    ) -> Interaction:
        """Surgically update only the provided fields.

        Args:
            db: Active database session.
            interaction_id: UUID string of the interaction to update.
            updates: Dict of field_name → new_value (only changed fields).

        Returns:
            The updated Interaction ORM instance.
        """
        interaction = InteractionService.get_by_id(db, interaction_id)

        for field, value in updates.items():
            if hasattr(interaction, field) and value is not None:
                setattr(interaction, field, value)

        interaction.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(interaction)

        logger.info(
            "Updated interaction %s — fields: %s",
            interaction_id,
            list(updates.keys()),
        )
        return interaction

    @staticmethod
    def list_all(
        db: Session,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Interaction]:
        """List interactions ordered by creation date (newest first)."""
        stmt = (
            select(Interaction)
            .order_by(Interaction.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(db.execute(stmt).scalars().all())

    @staticmethod
    def get_latest_by_session(db: Session, session_id: str) -> Optional[Interaction]:
        """Get the most recent interaction for a given chat session."""
        stmt = (
            select(Interaction)
            .where(Interaction.session_id == session_id)
            .order_by(Interaction.created_at.desc())
            .limit(1)
        )
        return db.execute(stmt).scalar_one_or_none()
