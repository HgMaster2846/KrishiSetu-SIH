from typing import List, Dict, Any
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import schemas
from ..services.mandi_service import MandiService

router = APIRouter(prefix="/mandi", tags=["Mandi Intelligence"])

@router.get("/prices", response_model=List[schemas.MandiPriceResponse])
def get_all_mandi_prices(db: Session = Depends(get_db)):
    return MandiService.get_all_prices(db)

@router.get("/crop/{crop_name}", response_model=schemas.MandiPriceResponse)
def get_crop_mandi_details(crop_name: str, db: Session = Depends(get_db)):
    return MandiService.get_crop_price(crop_name, db)

@router.get("/best-today")
def get_best_mandi_today(db: Session = Depends(get_db)):
    prices = MandiService.get_all_prices(db)
    return {
        "title": "Top Arbitrage Opportunities Across North Indian APMCs Today",
        "top_picks": [
            {"crop": "Tomato", "mandi": "Azadpur Mandi, Delhi", "modal_price": "?28.50/kg", "gain_over_local": "+12.4%"},
            {"crop": "Rice (Basmati 1121)", "mandi": "Karnal Grain Terminal", "modal_price": "?76.00/kg", "gain_over_local": "+5.8%"},
            {"crop": "Mustard (Sarson)", "mandi": "Alwar Krishi Mandi", "modal_price": "?61.50/kg", "gain_over_local": "+8.2%"}
        ],
        "all_benchmarks": prices
    }
