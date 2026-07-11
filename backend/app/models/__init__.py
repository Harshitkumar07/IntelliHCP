"""
Re-export all ORM models so Alembic and `Base.metadata.create_all()`
can discover them in a single import.
"""

from app.models.doctor import Doctor
from app.models.interaction import Interaction
from app.models.product import Product

__all__ = ["Doctor", "Interaction", "Product"]
