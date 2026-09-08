from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db, init_db, Base, engine

router = APIRouter(prefix="/seed", tags=["Demo Reset"])

@router.post("/reset")
def reset_demo_data():
    """
    Drops and re-populates full fresh demo data across farmers, buyers, listings, routes, and mandi rates.
    """
    Base.metadata.drop_all(bind=engine)
    init_db()
    return {"status": "SUCCESS", "message": "Database reset and seeded with fresh SIH 2026 demo data!"}
