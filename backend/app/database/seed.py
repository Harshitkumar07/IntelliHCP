"""
Database seed script — populates doctors and products tables
with realistic pharmaceutical CRM data.

Run via: python -m app.database.seed
Or called automatically on first app startup.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.database.engine import SessionLocal
from app.models.doctor import Doctor
from app.models.product import Product

logger = get_logger(__name__)

# ── Sample Doctors ───────────────────────────────────────
SEED_DOCTORS = [
    {"name": "Dr. Priya Sharma", "hospital": "Apollo Hospital", "specialization": "Cardiology", "city": "Mumbai"},
    {"name": "Dr. Rajesh Kumar", "hospital": "AIIMS", "specialization": "Oncology", "city": "Delhi"},
    {"name": "Dr. Anita Desai", "hospital": "Fortis Healthcare", "specialization": "Neurology", "city": "Bangalore"},
    {"name": "Dr. John Smith", "hospital": "Max Hospital", "specialization": "Cardiology", "city": "Delhi"},
    {"name": "Dr. Sarah Chen", "hospital": "Medanta", "specialization": "Endocrinology", "city": "Gurugram"},
    {"name": "Dr. Vikram Patel", "hospital": "Narayana Health", "specialization": "Orthopedics", "city": "Bangalore"},
    {"name": "Dr. Meera Iyer", "hospital": "Kokilaben Hospital", "specialization": "Dermatology", "city": "Mumbai"},
    {"name": "Dr. Arjun Reddy", "hospital": "Care Hospital", "specialization": "Pulmonology", "city": "Hyderabad"},
    {"name": "Dr. Fatima Khan", "hospital": "Lilavati Hospital", "specialization": "Gastroenterology", "city": "Mumbai"},
    {"name": "Dr. Amit Verma", "hospital": "Tata Memorial", "specialization": "Oncology", "city": "Mumbai"},
]

# ── Sample Products ──────────────────────────────────────
SEED_PRODUCTS = [
    {
        "name": "CardioX",
        "category": "Cardiovascular",
        "specialization_target": "Cardiology",
        "description": "Next-generation anti-hypertensive with dual mechanism of action. Phase III trial showed 40% reduction in cardiac events.",
    },
    {
        "name": "OncoBoost",
        "category": "Oncology",
        "specialization_target": "Oncology",
        "description": "Targeted immunotherapy agent for solid tumors. Breakthrough therapy designation by FDA.",
    },
    {
        "name": "NeuroCalm",
        "category": "Neurology",
        "specialization_target": "Neurology",
        "description": "Novel GABA modulator for treatment-resistant epilepsy. Orphan drug status granted.",
    },
    {
        "name": "GlucoStable",
        "category": "Endocrinology",
        "specialization_target": "Endocrinology",
        "description": "Once-weekly GLP-1 agonist for Type 2 diabetes. Superior HbA1c reduction in SUSTAIN trials.",
    },
    {
        "name": "BoneForte",
        "category": "Orthopedics",
        "specialization_target": "Orthopedics",
        "description": "Anti-RANKL monoclonal antibody for osteoporosis. 68% fracture risk reduction over 3 years.",
    },
    {
        "name": "DermaClear",
        "category": "Dermatology",
        "specialization_target": "Dermatology",
        "description": "IL-17 inhibitor for moderate-to-severe psoriasis. PASI 90 achieved in 80% of patients.",
    },
    {
        "name": "PulmoRelief",
        "category": "Pulmonology",
        "specialization_target": "Pulmonology",
        "description": "Long-acting muscarinic antagonist for COPD. 24-hour bronchodilation with once-daily dosing.",
    },
    {
        "name": "GastroShield",
        "category": "Gastroenterology",
        "specialization_target": "Gastroenterology",
        "description": "Proton pump inhibitor with novel delayed-release formulation for GERD and peptic ulcers.",
    },
]


def seed_database(db: Session | None = None) -> None:
    """Insert seed data if tables are empty.

    Safe to call multiple times — skips seeding if data already exists.
    """
    should_close = False
    if db is None:
        db = SessionLocal()
        should_close = True

    try:
        # Seed doctors
        existing_doctors = db.query(Doctor).count()
        if existing_doctors == 0:
            for doc_data in SEED_DOCTORS:
                db.add(Doctor(**doc_data))
            db.commit()
            logger.info("Seeded %d doctors", len(SEED_DOCTORS))
        else:
            logger.info("Doctors table already has %d records — skipping seed", existing_doctors)

        # Seed products
        existing_products = db.query(Product).count()
        if existing_products == 0:
            for prod_data in SEED_PRODUCTS:
                db.add(Product(**prod_data))
            db.commit()
            logger.info("Seeded %d products", len(SEED_PRODUCTS))
        else:
            logger.info("Products table already has %d records — skipping seed", existing_products)

    except Exception:
        db.rollback()
        logger.exception("Seed data insertion failed")
        raise
    finally:
        if should_close:
            db.close()


if __name__ == "__main__":
    from app.core.logging import setup_logging
    from app.database.base import Base
    from app.database.engine import engine
    from app.models import Doctor, Interaction, Product  # noqa: F811

    setup_logging()
    Base.metadata.create_all(bind=engine)
    seed_database()
    logger.info("Seed complete.")
