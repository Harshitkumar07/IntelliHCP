"""
Doctor service — search and lookup for HCP records.

Supports fuzzy name search (ILIKE) and filtering by
specialization and city. Used by the search_doctor tool.
"""

from __future__ import annotations

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models.doctor import Doctor

logger = get_logger(__name__)


class DoctorService:
    """Stateless service for doctor queries."""

    @staticmethod
    def search(db: Session, query: str, limit: int = 10) -> list[Doctor]:
        """Fuzzy-search doctors by name, specialization, or city.
        
        Splits query by spaces and ensures all terms match (ignoring order)
        to handle missing middle names (e.g., 'Dr. Smith' matches 'Dr. John Smith').
        """
        terms = [t.strip() for t in query.split() if t.strip()]
        if not terms:
            return []
            
        conditions = []
        for term in terms:
            pattern = f"%{term}%"
            conditions.append(
                or_(
                    Doctor.name.ilike(pattern),
                    Doctor.specialization.ilike(pattern),
                    Doctor.city.ilike(pattern),
                    Doctor.hospital.ilike(pattern),
                )
            )
            
        stmt = select(Doctor).where(*conditions).limit(limit)
        results = list(db.execute(stmt).scalars().all())
        logger.info("Doctor search '%s' returned %d results", query, len(results))
        return results

    @staticmethod
    def get_by_name(db: Session, name: str) -> Doctor | None:
        """Find a doctor by exact name match (case-insensitive)."""
        stmt = select(Doctor).where(Doctor.name.ilike(name.strip()))
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def list_all(db: Session, limit: int = 100) -> list[Doctor]:
        """List all doctors."""
        stmt = select(Doctor).order_by(Doctor.name).limit(limit)
        return list(db.execute(stmt).scalars().all())
