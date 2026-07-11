"""
Tool 2: edit_interaction (MANDATORY)

Surgically updates only the fields the user requested to change.
The LLM identifies WHICH fields changed and provides them as arguments.
This tool normalises the changed fields and applies a partial update.

NO LLM call inside — purely deterministic merge + save.
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
def edit_interaction(
    interaction_id: str,
    doctor_name: Optional[str] = None,
    interaction_date: Optional[str] = None,
    interaction_time: Optional[str] = None,
    interaction_type: Optional[str] = None,
    attendees: Optional[str] = None,
    topics: Optional[str] = None,
    products: Union[list[str], str, None] = None,
    summary: Optional[str] = None,
    sentiment: Optional[str] = None,
    brochures: Union[list[str], str, None] = None,
    samples: Union[list[str], str, None] = None,
    outcomes: Optional[str] = None,
    follow_up: Optional[str] = None,
) -> str:
    """Edit an existing HCP interaction — update only the specified fields.

    Use this tool when the user wants to correct or modify a previously
    logged interaction. Only provide the fields that need to change;
    all other fields will remain untouched.

    Args:
        interaction_id: UUID of the interaction to edit (REQUIRED — get from current form state).
        doctor_name: Updated HCP name (only if changing).
        interaction_date: Updated date (only if changing).
        interaction_time: Updated time (only if changing).
        interaction_type: Updated interaction type (only if changing).
        attendees: Updated attendees (only if changing).
        topics: Updated discussion topics (only if changing).
        products: Updated product list (only if changing).
        summary: Updated summary (only if changing).
        sentiment: Updated sentiment (only if changing).
        brochures: Updated brochures list (only if changing).
        samples: Updated samples list (only if changing).
        outcomes: Updated outcomes (only if changing).
        follow_up: Updated follow-up (only if changing).

    Returns:
        JSON string with status and the complete updated form_data.
    """
    logger.info("edit_interaction called for id: %s", interaction_id)

    def _coerce_list(val):
        if not val:
            return []
        if isinstance(val, str):
            return [val]
        return val

    # ── 1. Collect only the fields that were explicitly provided ──
    raw_updates: dict = {}
    local_vars = {
        "doctor_name": doctor_name,
        "interaction_date": interaction_date,
        "interaction_time": interaction_time,
        "interaction_type": interaction_type,
        "attendees": attendees,
        "topics": topics,
        "products": _coerce_list(products) if products is not None else None,
        "summary": summary,
        "sentiment": sentiment,
        "brochures": _coerce_list(brochures) if brochures is not None else None,
        "samples": _coerce_list(samples) if samples is not None else None,
        "outcomes": outcomes,
        "follow_up": follow_up,
    }

    for field, value in local_vars.items():
        if value is not None:
            raw_updates[field] = value

    if not raw_updates:
        return json.dumps({
            "status": "no_changes",
            "message": "No fields were provided to update.",
        })

    # ── 2. Normalise only the changed fields ────────────
    normalised_updates = InteractionNormalizer.normalize_partial(raw_updates)

    # ── 3. Apply surgical update ────────────────────────
    with get_session() as db:
        interaction = InteractionService.update(db, interaction_id, normalised_updates)
        form_data = interaction.to_dict()

    changed_fields = list(normalised_updates.keys())
    logger.info("Updated fields: %s", changed_fields)

    return json.dumps({
        "status": "success",
        "message": f"Updated {', '.join(changed_fields)} successfully.",
        "interaction_id": form_data["interaction_id"],
        "form_data": form_data,
        "changed_fields": changed_fields,
    })
