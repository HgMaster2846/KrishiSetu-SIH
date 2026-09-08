from typing import List, Dict, Any, Optional
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

@router.get("/crops/{crop_name}", response_model=schemas.MandiPriceResponse)
def get_crops_mandi_details_alias(crop_name: str, db: Session = Depends(get_db)):
    """Alias for /crop/{crop_name} to satisfy REST API plural convention."""
    return MandiService.get_crop_price(crop_name, db)

@router.post("/sync-agmarknet")
async def sync_agmarknet_live(payload: Optional[schemas.MandiSyncRequest] = None, db: Session = Depends(get_db)):
    """
    Synchronizes live APMC Mandi prices from official Government Agmarknet API (data.gov.in).
    Converts ₹/Quintal to ₹/Kg, aggregates across mandis, and updates DB cache.
    """
    api_key = payload.api_key if payload else None
    state = payload.state if payload else None
    commodity = payload.commodity if payload else None
    return await MandiService.sync_agmarknet_prices(api_key=api_key, state=state, commodity=commodity, db=db)


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
