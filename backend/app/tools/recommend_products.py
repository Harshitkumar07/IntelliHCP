"""
Tool 4: recommend_products

Recommends pharmaceutical products based on the doctor's specialization
and discussion context. Queries the product catalog deterministically
using specialization matching.

No LLM call — the product-to-specialization mapping is in the database.
The LLM can add contextual commentary in its response message.
"""

from __future__ import annotations

import json

from langchain_core.tools import tool
from sqlalchemy import or_, select

from app.core.logging import get_logger
from app.database.engine import get_session
from app.models.product import Product

logger = get_logger(__name__)


@tool
def recommend_products(
    specialization: str,
    topics_discussed: str = "",
) -> str:
    """Recommend pharmaceutical products and brochures for an HCP.

    Use this tool when the user asks for product suggestions, or when
    you want to proactively recommend relevant products based on the
    doctor's medical specialization.

    Args:
        specialization: The doctor's medical specialization
                        (e.g., "Cardiology", "Oncology", "Neurology").
        topics_discussed: Optional context about what was discussed,
                          to help refine recommendations.

    Returns:
        JSON string with matching products including name, category,
        and clinical description.
    """
    logger.info(
        "recommend_products called — specialization: %s, topics: %s",
        specialization,
        topics_discussed,
    )

    with get_session() as db:
        # Primary: match by specialization
        pattern = f"%{specialization.strip()}%"
        stmt = select(Product).where(
            Product.specialization_target.ilike(pattern)
        )
        products = list(db.execute(stmt).scalars().all())

        # If topics mentioned, also search by product name/description
        if topics_discussed and not products:
            topic_pattern = f"%{topics_discussed.strip()}%"
            stmt = select(Product).where(
                or_(
                    Product.name.ilike(topic_pattern),
                    Product.description.ilike(topic_pattern),
                )
            )
            products = list(db.execute(stmt).scalars().all())

    if not products:
        return json.dumps({
            "status": "no_results",
            "message": f"No products found for specialization '{specialization}'.",
            "recommendations": [],
        })

    recommendations = [
        {
            "name": p.name,
            "category": p.category,
            "specialization_target": p.specialization_target,
            "description": p.description,
        }
        for p in products
    ]

    return json.dumps({
        "status": "success",
        "message": f"Found {len(recommendations)} product(s) for {specialization}.",
        "recommendations": recommendations,
    })
