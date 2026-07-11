"""
Interaction CRUD endpoints.

These are secondary to the chat endpoint — most interaction
mutations happen through the AI agent. These endpoints exist for:
  - Direct retrieval (GET /interactions/{id})
  - Admin updates (PUT /interactions/{id})
  - Listing history (GET /interactions)
  - Doctor search (GET /doctors/search)
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.exceptions import NotFoundError
from app.core.logging import get_logger
from app.services.doctor_service import DoctorService
from app.services.interaction_service import InteractionService

logger = get_logger(__name__)

router = APIRouter(tags=["Interactions"])


# ── Interactions ─────────────────────────────────────────

@router.get("/interactions")
def list_interactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[dict]:
    """List all interactions, newest first."""
    interactions = InteractionService.list_all(db, skip=skip, limit=limit)
    return [i.to_dict() for i in interactions]


@router.get("/interactions/{interaction_id}")
def get_interaction(
    interaction_id: str,
    db: Session = Depends(get_db),
) -> dict:
    """Retrieve a single interaction by ID."""
    try:
        interaction = InteractionService.get_by_id(db, interaction_id)
        return interaction.to_dict()
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=exc.message) from exc


@router.put("/interactions/{interaction_id}")
def update_interaction(
    interaction_id: str,
    updates: dict,
    db: Session = Depends(get_db),
) -> dict:
    """Update an interaction directly (admin use)."""
    try:
        interaction = InteractionService.update(db, interaction_id, updates)
        return interaction.to_dict()
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=exc.message) from exc


# ── Doctors ──────────────────────────────────────────────

@router.get("/doctors/search")
def search_doctors(
    q: str = Query(..., min_length=1, max_length=200),
    db: Session = Depends(get_db),
) -> list[dict]:
    """Search doctors by name, specialization, or city."""
    doctors = DoctorService.search(db, q)
    return [d.to_dict() for d in doctors]


@router.get("/doctors")
def list_doctors(
    db: Session = Depends(get_db),
) -> list[dict]:
    """List all doctors in the HCP database."""
    doctors = DoctorService.list_all(db)
    return [d.to_dict() for d in doctors]
