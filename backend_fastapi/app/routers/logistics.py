from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import schemas
from ..services.logistics_service import LogisticsService
from ..models import models

router = APIRouter(prefix="/logistics", tags=["Pooled Logistics"])

@router.get("/routes", response_model=List[schemas.TruckRouteResponse])
def get_all_routes(
    village: str = Query("Murthal"),
    district: str = Query("Sonipat"),
    destination: str = Query("Azadpur Mandi, Delhi"),
    quantity_kg: float = Query(200.0),
    db: Session = Depends(get_db)
):
    """
    Returns nearby trucks travelling along route with available capacity,
    shared cost, solo cost, and estimated savings.
    """
    return LogisticsService.find_pooled_trucks(village, district, destination, quantity_kg, db)
