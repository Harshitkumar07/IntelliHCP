"""
Tool 3: search_doctor

Searches the HCP database by name, specialization, or city.
Purely deterministic — queries PostgreSQL with ILIKE fuzzy matching.
No LLM call needed.
"""

from __future__ import annotations

import json

from langchain_core.tools import tool

from app.core.logging import get_logger
from app.database.engine import get_session
from app.services.doctor_service import DoctorService

logger = get_logger(__name__)


@tool
def search_doctor(query: str) -> str:
    """Search for Healthcare Professionals (doctors) in the CRM database.

    Use this tool when the user asks to find, search for, or look up
    a doctor by name, specialization, hospital, or city.

    Args:
        query: Search term — can be a name fragment, specialization,
               hospital name, or city (e.g., "Smith", "Cardiology", "Mumbai").

    Returns:
        JSON string with matching doctors including their name, hospital,
        specialization, and city.
    """
    logger.info("search_doctor called with query: %s", query)

    with get_session() as db:
        doctors = DoctorService.search(db, query)

    if not doctors:
        return json.dumps({
            "status": "no_results",
            "message": f"No doctors found matching '{query}'.",
            "doctors": [],
        })

    doctor_list = [doc.to_dict() for doc in doctors]

    return json.dumps({
        "status": "success",
        "message": f"Found {len(doctor_list)} doctor(s) matching '{query}'.",
        "doctors": doctor_list,
    })
