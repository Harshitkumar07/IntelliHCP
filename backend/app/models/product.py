"""
Product (pharmaceutical) ORM model.

Stores the product catalog that the recommend_products tool
queries against. Pre-seeded with sample pharmaceutical products
mapped to medical specializations.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Product(Base):
    """Pharmaceutical product in the catalog."""

    __tablename__ = "products"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    specialization_target: Mapped[str] = mapped_column(
        String(200), nullable=False, default=""
    )
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<Product(name='{self.name}', category='{self.category}')>"

    def to_dict(self) -> dict:
        """Serialise for JSON responses."""
        return {
            "id": str(self.id),
            "name": self.name,
            "category": self.category,
            "specialization_target": self.specialization_target,
            "description": self.description,
        }
