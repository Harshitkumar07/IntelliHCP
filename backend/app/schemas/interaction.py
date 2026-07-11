"""
Interaction Pydantic schemas.

Separate schemas for create, update, and output operations
following Interface Segregation Principle — each consumer
gets exactly the shape it needs.
"""

from __future__ import annotations

from datetime import date, time
from typing import Optional

from pydantic import BaseModel, Field


class InteractionCreate(BaseModel):
    """Schema for creating a new interaction (all fields optional except doctor_name)."""

    doctor_name: str = Field(..., min_length=1, description="HCP name")
    interaction_date: Optional[date] = Field(default=None)
    interaction_time: Optional[time] = Field(default=None)
    interaction_type: str = Field(default="Meeting")
    attendees: str = Field(default="")
    topics: str = Field(default="")
    products: list[str] = Field(default_factory=list)
    summary: str = Field(default="")
    sentiment: str = Field(default="Neutral")
    brochures: list[str] = Field(default_factory=list)
    samples: list[str] = Field(default_factory=list)
    outcomes: str = Field(default="")
    follow_up: str = Field(default="")
    follow_up_suggestions: list[str] = Field(default_factory=list)
    session_id: str = Field(default="")


class InteractionUpdate(BaseModel):
    """Schema for updating an interaction — every field is optional for surgical updates."""

    doctor_name: Optional[str] = None
    interaction_date: Optional[date] = None
    interaction_time: Optional[time] = None
    interaction_type: Optional[str] = None
    attendees: Optional[str] = None
    topics: Optional[str] = None
    products: Optional[list[str]] = None
    summary: Optional[str] = None
    sentiment: Optional[str] = None
    brochures: Optional[list[str]] = None
    samples: Optional[list[str]] = None
    outcomes: Optional[str] = None
    follow_up: Optional[str] = None
    follow_up_suggestions: Optional[list[str]] = None


class InteractionOut(BaseModel):
    """Schema for outbound interaction data (API responses and Redux form)."""

    interaction_id: str
    doctor_name: str
    interaction_date: str
    interaction_time: str
    interaction_type: str
    attendees: str
    topics: str
    products: list[str]
    summary: str
    sentiment: str
    brochures: list[str]
    samples: list[str]
    outcomes: str
    follow_up: str
    follow_up_suggestions: list[str]

    model_config = {"from_attributes": True}
