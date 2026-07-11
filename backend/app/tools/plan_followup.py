"""
Tool 5: plan_followup

Generates intelligent follow-up action items based on interaction context.
Uses rule-based logic driven by sentiment, interaction type, and products
discussed — no secondary LLM call needed.

The rules encode pharmaceutical sales best practices:
  - Positive sentiment → deepen engagement
  - Negative sentiment → address concerns quickly
  - Neutral → maintain contact and provide more data
"""

from __future__ import annotations

import json
from datetime import date, timedelta

from langchain_core.tools import tool

from app.core.logging import get_logger

logger = get_logger(__name__)


@tool
def plan_followup(
    doctor_name: str,
    sentiment: str = "Neutral",
    interaction_type: str = "Meeting",
    topics_discussed: str = "",
    products: list[str] | None = None,
    outcomes: str = "",
) -> str:
    """Generate follow-up action items based on the interaction context.

    Use this tool when the user asks for follow-up planning, next steps,
    or when you want to proactively suggest follow-up actions after
    logging an interaction.

    Args:
        doctor_name: Name of the HCP for personalised suggestions.
        sentiment: Observed HCP sentiment (Positive, Neutral, Negative).
        interaction_type: Type of the interaction that occurred.
        topics_discussed: What was discussed during the interaction.
        products: Products that were discussed or shared.
        outcomes: Any agreements or outcomes from the interaction.

    Returns:
        JSON string with prioritised follow-up suggestions and target dates.
    """
    logger.info("plan_followup called for %s (sentiment: %s)", doctor_name, sentiment)

    products = products or []
    today = date.today()
    suggestions: list[dict[str, str]] = []

    # ── Sentiment-driven rules ──────────────────────────
    sentiment_lower = sentiment.strip().lower()

    if sentiment_lower == "positive":
        suggestions.append({
            "action": f"Schedule follow-up meeting with {doctor_name} in 2 weeks",
            "target_date": (today + timedelta(weeks=2)).isoformat(),
            "priority": "High",
        })
        if products:
            suggestions.append({
                "action": f"Send {products[0]} Phase III clinical trial data to {doctor_name}",
                "target_date": (today + timedelta(days=3)).isoformat(),
                "priority": "High",
            })
        suggestions.append({
            "action": f"Add {doctor_name} to advisory board invite list",
            "target_date": (today + timedelta(weeks=1)).isoformat(),
            "priority": "Medium",
        })

    elif sentiment_lower == "negative":
        suggestions.append({
            "action": f"Schedule urgent follow-up with {doctor_name} within 1 week to address concerns",
            "target_date": (today + timedelta(weeks=1)).isoformat(),
            "priority": "Critical",
        })
        suggestions.append({
            "action": "Prepare objection handling materials and competitive analysis",
            "target_date": (today + timedelta(days=2)).isoformat(),
            "priority": "High",
        })
        suggestions.append({
            "action": f"Escalate {doctor_name}'s concerns to medical affairs team",
            "target_date": (today + timedelta(days=1)).isoformat(),
            "priority": "High",
        })

    else:  # Neutral
        suggestions.append({
            "action": f"Schedule follow-up meeting with {doctor_name} in 3 weeks",
            "target_date": (today + timedelta(weeks=3)).isoformat(),
            "priority": "Medium",
        })
        if products:
            suggestions.append({
                "action": f"Send {products[0]} clinical summary and patient case studies",
                "target_date": (today + timedelta(days=5)).isoformat(),
                "priority": "Medium",
            })

    # ── Universal follow-ups ────────────────────────────
    suggestions.append({
        "action": f"Update CRM notes and territory plan for {doctor_name}",
        "target_date": today.isoformat(),
        "priority": "Low",
    })

    if products and len(products) > 1:
        suggestions.append({
            "action": f"Prepare comparison deck for {', '.join(products)}",
            "target_date": (today + timedelta(days=5)).isoformat(),
            "priority": "Medium",
        })

    # ── Format as simple string list for the form ───────
    suggestion_strings = [s["action"] for s in suggestions]

    return json.dumps({
        "status": "success",
        "message": f"Generated {len(suggestions)} follow-up action(s) for {doctor_name}.",
        "follow_up_suggestions": suggestion_strings,
        "detailed_suggestions": suggestions,
    })
