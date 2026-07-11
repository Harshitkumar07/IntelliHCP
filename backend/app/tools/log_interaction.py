"""
Tool 1: log_interaction (MANDATORY)

Receives pre-extracted structured fields from the LLM's tool call,
normalises them through the validation layer, and persists to the database.

NO LLM call inside this tool — the main LLM node already performed
the extraction when it decided to call this tool with specific arguments.
This tool does purely deterministic work: validate → normalise → save.
"""

from __future__ import annotations

import json
from typing import Optional, Union

from langchain_core.tools import tool

from app.core.logging import get_logger
from app.database.engine import get_session
from app.services.interaction_service import InteractionService
from app.validators.interaction_validator import InteractionNormalizer

logger = get_logger(__name__)


@tool
def log_interaction(
    doctor_name: str,
    interaction_date: Optional[str] = None,
    interaction_time: Optional[str] = None,
    interaction_type: Optional[str] = "Meeting",
    attendees: Optional[str] = "",
    topics: Optional[str] = "",
    products: Union[list[str], str, None] = None,
    summary: Optional[str] = "",
    sentiment: Optional[str] = "Neutral",
    brochures: Union[list[str], str, None] = None,
    samples: Union[list[str], str, None] = None,
    outcomes: Optional[str] = "",
    follow_up: Optional[str] = "",
) -> str:
    """Log a new HCP interaction into the CRM system.

    Use this tool when a pharmaceutical sales rep describes a meeting, call,
    or any interaction with a Healthcare Professional. Extract all relevant
    details from their description and provide them as arguments.

    Args:
        doctor_name: Name of the Healthcare Professional (REQUIRED).
        interaction_date: Date of the interaction (e.g., "today", "2026-07-11").
        interaction_time: Time of the interaction (e.g., "14:30", "2:30 PM").
        interaction_type: Type of interaction (Meeting, Call, Email, Video Call, Conference).
        attendees: Other people present during the interaction.
        topics: Key discussion points from the interaction.
        products: List of pharmaceutical products discussed.
        summary: Brief summary of the interaction.
        sentiment: Observed HCP sentiment (Positive, Neutral, Negative).
        brochures: List of marketing materials shared with the HCP.
        samples: List of product samples distributed to the HCP.
        outcomes: Key outcomes or agreements from the interaction.
        follow_up: Next steps or follow-up tasks planned.

    Returns:
        JSON string with status, interaction_id, and the complete form_data.
    """
    logger.info("log_interaction called for doctor: %s", doctor_name)

    def _coerce_list(val):
        if not val:
            return []
        if isinstance(val, str):
            return [val]
        return val

    # ── 1. Assemble raw data from tool arguments ────────
    raw_data = {
        "doctor_name": doctor_name,
        "interaction_date": interaction_date,
        "interaction_time": interaction_time,
        "interaction_type": interaction_type,
        "attendees": attendees or "",
        "topics": topics or "",
        "products": _coerce_list(products),
        "summary": summary or "",
        "sentiment": sentiment,
        "brochures": _coerce_list(brochures),
        "samples": _coerce_list(samples),
        "outcomes": outcomes or "",
        "follow_up": follow_up or "",
    }

    # ── 2. Normalise through validation layer ───────────
    normalised = InteractionNormalizer.normalize_full(raw_data)

    # ── 3. Persist to database ──────────────────────────
    with get_session() as db:
        interaction = InteractionService.create(db, normalised)
        form_data = interaction.to_dict()

    logger.info("Interaction saved with id: %s", form_data["interaction_id"])

    return json.dumps({
        "status": "success",
        "message": f"Interaction with {normalised['doctor_name']} logged successfully.",
        "interaction_id": form_data["interaction_id"],
        "form_data": form_data,
    })
