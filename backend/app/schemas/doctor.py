"""
Doctor Pydantic schemas for search and output.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class DoctorSearch(BaseModel):
    """Query parameters for doctor search."""

    query: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Name, specialization, or city fragment to search",
    )


class DoctorOut(BaseModel):
    """Outbound doctor record."""

    id: str
    name: str
    hospital: str
    specialization: str
    city: str

    model_config = {"from_attributes": True}
