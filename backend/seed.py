import os
import sys

# Ensure the app module can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.engine import get_session
from app.models.doctor import Doctor

dummy_doctors = [
    {
        "name": "Dr. John Smith",
        "hospital": "City General Hospital",
        "specialization": "Gastroenterologist",
        "city": "New York"
    },
    {
        "name": "Dr. Priya Sharma",
        "hospital": "Sunrise Oncology Center",
        "specialization": "Oncologist",
        "city": "San Francisco"
    },
    {
        "name": "Dr. Sarah Johnson",
        "hospital": "Heartbeat Cardiology Clinic",
        "specialization": "Cardiologist",
        "city": "Chicago"
    },
    {
        "name": "Dr. Michael Chen",
        "hospital": "Metro Neurology Institute",
        "specialization": "Neurologist",
        "city": "Boston"
    },
    {
        "name": "Dr. Emily Davis",
        "hospital": "Women's Health Pavilion",
        "specialization": "Gynecologist",
        "city": "Austin"
    },
    {
        "name": "Dr. Robert Wilson",
        "hospital": "Valley Orthopedics",
        "specialization": "Orthopedic Surgeon",
        "city": "Denver"
    },
    {
        "name": "Dr. Lisa Martinez",
        "hospital": "Pediatric Care Center",
        "specialization": "Pediatrician",
        "city": "Miami"
    },
    {
        "name": "Dr. David Kim",
        "hospital": "Clear Skin Dermatology",
        "specialization": "Dermatologist",
        "city": "Seattle"
    },
    {
        "name": "Dr. Amanda White",
        "hospital": "Advanced Endocrinology",
        "specialization": "Endocrinologist",
        "city": "Atlanta"
    },
    {
        "name": "Dr. James Taylor",
        "hospital": "Breathe Easy Pulmonology",
        "specialization": "Pulmonologist",
        "city": "Portland"
    },
    {
        "name": "Dr. Olivia Brown",
        "hospital": "Mindful Psychiatry Clinic",
        "specialization": "Psychiatrist",
        "city": "San Diego"
    },
    {
        "name": "Dr. William Lee",
        "hospital": "General Family Practice",
        "specialization": "General Practitioner",
        "city": "Dallas"
    }
]

def seed_database():
    with get_session() as db:
        # Check if we already have doctors to prevent duplicates
        existing_count = db.query(Doctor).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} doctors. Clearing them for a fresh seed...")
            db.query(Doctor).delete()
            db.commit()
            
        print("Seeding database with 12 dummy doctors...")
        for doc_data in dummy_doctors:
            doc = Doctor(**doc_data)
            db.add(doc)
            
        db.commit()
        print("Successfully seeded the database!")

if __name__ == "__main__":
    seed_database()
