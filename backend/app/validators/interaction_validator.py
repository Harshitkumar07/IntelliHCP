"""
Validation and normalisation layer between LLM output and database writes.

This module sits between the LangGraph tool arguments (which are
LLM-generated and therefore unpredictable) and the database layer.
It normalises dates ("today" → ISO date), sentiments ("good" → "Positive"),
interaction types, and doctor name capitalisation.

WHY: LLM outputs vary in casing, formatting, and synonym usage.
This layer ensures consistent, valid data reaches the database
regardless of how the LLM phrases things.
"""

from __future__ import annotations

import re
from datetime import date, datetime, time, timedelta
from typing import Any, Optional

from app.core.logging import get_logger

logger = get_logger(__name__)

# ── Valid Value Sets ─────────────────────────────────────
VALID_SENTIMENTS = {"Positive", "Neutral", "Negative"}
VALID_INTERACTION_TYPES = {"Meeting", "Call", "Email", "Video Call", "Conference"}

# Sentiment synonym mapping (lowercase key → canonical value)
SENTIMENT_MAP: dict[str, str] = {
    "positive": "Positive",
    "good": "Positive",
    "great": "Positive",
    "excellent": "Positive",
    "happy": "Positive",
    "interested": "Positive",
    "favorable": "Positive",
    "enthusiastic": "Positive",
    "neutral": "Neutral",
    "okay": "Neutral",
    "ok": "Neutral",
    "indifferent": "Neutral",
    "moderate": "Neutral",
    "negative": "Negative",
    "bad": "Negative",
    "poor": "Negative",
    "unhappy": "Negative",
    "disinterested": "Negative",
    "unfavorable": "Negative",
    "skeptical": "Negative",
    "concerned": "Negative",
}

# Interaction type synonym mapping (lowercase key → canonical value)
INTERACTION_TYPE_MAP: dict[str, str] = {
    "meeting": "Meeting",
    "in-person": "Meeting",
    "in person": "Meeting",
    "face to face": "Meeting",
    "visit": "Meeting",
    "call": "Call",
    "phone": "Call",
    "phone call": "Call",
    "telephone": "Call",
    "email": "Email",
    "mail": "Email",
    "e-mail": "Email",
    "video": "Video Call",
    "video call": "Video Call",
    "virtual": "Video Call",
    "zoom": "Video Call",
    "teams": "Video Call",
    "conference": "Conference",
    "webinar": "Conference",
    "seminar": "Conference",
}


class InteractionNormalizer:
    """Stateless normaliser for interaction data coming from LLM tool calls."""

    @staticmethod
    def normalize_date(raw: str | None) -> Optional[date]:
        """Convert LLM date output to a proper date object.

        Handles: "today", "yesterday", "2026-07-11", "11/07/2026",
                 "July 11 2026", empty/null values.
        """
        if not raw or raw.strip().lower() in ("", "null", "none", "n/a"):
            return None

        cleaned = raw.strip().lower()

        # Relative dates
        today = date.today()
        if cleaned == "today":
            return today
        if cleaned == "yesterday":
            return today - timedelta(days=1)
        if cleaned == "tomorrow":
            return today + timedelta(days=1)

        # Try ISO format first (YYYY-MM-DD)
        try:
            return date.fromisoformat(raw.strip())
        except ValueError:
            pass

        # Try common formats
        for fmt in ("%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%B %d %Y", "%b %d %Y", "%d %B %Y", "%d %b %Y"):
            try:
                return datetime.strptime(raw.strip(), fmt).date()
            except ValueError:
                continue

        logger.warning("Could not parse date: %s — defaulting to today", raw)
        return today

    @staticmethod
    def normalize_time(raw: str | None) -> Optional[time]:
        """Convert LLM time output to a proper time object.

        Handles: "19:36", "7:36 PM", "19:36:00", empty/null.
        """
        if not raw or raw.strip().lower() in ("", "null", "none", "n/a"):
            return None

        cleaned = raw.strip()

        # Try HH:MM
        for fmt in ("%H:%M", "%H:%M:%S", "%I:%M %p", "%I:%M%p"):
            try:
                return datetime.strptime(cleaned, fmt).time()
            except ValueError:
                continue

        logger.warning("Could not parse time: %s — returning None", raw)
        return None

    @staticmethod
    def normalize_sentiment(raw: str | None) -> str:
        """Map sentiment synonyms to canonical values.

        Defaults to "Neutral" if unrecognisable.
        """
        if not raw:
            return "Neutral"

        cleaned = raw.strip().lower()
        canonical = SENTIMENT_MAP.get(cleaned)
        if canonical:
            return canonical

        # Check if it's already a valid value (case-insensitive)
        for valid in VALID_SENTIMENTS:
            if cleaned == valid.lower():
                return valid

        logger.warning("Unknown sentiment '%s' — defaulting to Neutral", raw)
        return "Neutral"

    @staticmethod
    def normalize_interaction_type(raw: str | None) -> str:
        """Map interaction type synonyms to canonical values.

        Defaults to "Meeting" if unrecognisable.
        """
        if not raw:
            return "Meeting"

        cleaned = raw.strip().lower()
        canonical = INTERACTION_TYPE_MAP.get(cleaned)
        if canonical:
            return canonical

        # Check valid values directly
        for valid in VALID_INTERACTION_TYPES:
            if cleaned == valid.lower():
                return valid

        logger.warning("Unknown interaction type '%s' — defaulting to Meeting", raw)
        return "Meeting"

    @staticmethod
    def normalize_doctor_name(raw: str | None) -> str:
        """Capitalise doctor name consistently.

        "dr smith" → "Dr. Smith"
        "DR. JOHN SMITH" → "Dr. John Smith"
        """
        if not raw:
            return ""

        cleaned = raw.strip()
        if not cleaned:
            return ""

        # Handle "Dr" prefix variants
        cleaned = re.sub(r"(?i)^dr\.?\s*", "Dr. ", cleaned)

        # Title-case the rest
        parts = cleaned.split()
        result_parts: list[str] = []
        for i, part in enumerate(parts):
            if i == 0 and part.lower().startswith("dr"):
                result_parts.append("Dr.")
            else:
                result_parts.append(part.capitalize())

        return " ".join(result_parts)

    @staticmethod
    def normalize_list_field(raw: Any) -> list[str]:
        """Ensure list fields are always proper string lists.

        Handles: None, "", "item1, item2", ["item1", "item2"]
        """
        if raw is None:
            return []
        if isinstance(raw, list):
            return [str(item).strip() for item in raw if item]
        if isinstance(raw, str):
            if not raw.strip():
                return []
            return [item.strip() for item in raw.split(",") if item.strip()]
        return []

    @classmethod
    def normalize_full(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Normalise all fields in an interaction dict (for log_interaction).

        Applies every normaliser to produce clean, database-ready data.
        """
        normalised: dict[str, Any] = {}

        normalised["doctor_name"] = cls.normalize_doctor_name(data.get("doctor_name"))
        normalised["interaction_date"] = cls.normalize_date(data.get("interaction_date"))
        normalised["interaction_time"] = cls.normalize_time(data.get("interaction_time"))
        normalised["interaction_type"] = cls.normalize_interaction_type(data.get("interaction_type"))
        normalised["attendees"] = str(data.get("attendees", "")).strip()
        normalised["topics"] = str(data.get("topics", "")).strip()
        normalised["products"] = cls.normalize_list_field(data.get("products"))
        normalised["summary"] = str(data.get("summary", "")).strip()
        normalised["sentiment"] = cls.normalize_sentiment(data.get("sentiment"))
        normalised["brochures"] = cls.normalize_list_field(data.get("brochures"))
        normalised["samples"] = cls.normalize_list_field(data.get("samples"))
        normalised["outcomes"] = str(data.get("outcomes", "")).strip()
        normalised["follow_up"] = str(data.get("follow_up", "")).strip()

        return normalised

    @classmethod
    def normalize_partial(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Normalise only the fields present in data (for edit_interaction).

        Only processes keys that exist in the input dict,
        leaving un-mentioned fields untouched during merges.
        """
        normalised: dict[str, Any] = {}

        if "doctor_name" in data and data["doctor_name"] is not None:
            normalised["doctor_name"] = cls.normalize_doctor_name(data["doctor_name"])
        if "interaction_date" in data and data["interaction_date"] is not None:
            normalised["interaction_date"] = cls.normalize_date(data["interaction_date"])
        if "interaction_time" in data and data["interaction_time"] is not None:
            normalised["interaction_time"] = cls.normalize_time(data["interaction_time"])
        if "interaction_type" in data and data["interaction_type"] is not None:
            normalised["interaction_type"] = cls.normalize_interaction_type(data["interaction_type"])
        if "attendees" in data and data["attendees"] is not None:
            normalised["attendees"] = str(data["attendees"]).strip()
        if "topics" in data and data["topics"] is not None:
            normalised["topics"] = str(data["topics"]).strip()
        if "products" in data and data["products"] is not None:
            normalised["products"] = cls.normalize_list_field(data["products"])
        if "summary" in data and data["summary"] is not None:
            normalised["summary"] = str(data["summary"]).strip()
        if "sentiment" in data and data["sentiment"] is not None:
            normalised["sentiment"] = cls.normalize_sentiment(data["sentiment"])
        if "brochures" in data and data["brochures"] is not None:
            normalised["brochures"] = cls.normalize_list_field(data["brochures"])
        if "samples" in data and data["samples"] is not None:
            normalised["samples"] = cls.normalize_list_field(data["samples"])
        if "outcomes" in data and data["outcomes"] is not None:
            normalised["outcomes"] = str(data["outcomes"]).strip()
        if "follow_up" in data and data["follow_up"] is not None:
            normalised["follow_up"] = str(data["follow_up"]).strip()

        return normalised
