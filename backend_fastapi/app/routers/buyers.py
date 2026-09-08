from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import schemas
from ..services.recommendation_service import RecommendationEngine
from ..models import models

router = APIRouter(prefix="/buyers", tags=["Buyer Intelligence"])

@router.get("/all", response_model=List[schemas.BuyerResponse])
def get_all_buyers(db: Session = Depends(get_db)):
    return db.query(models.BuyerModel).all()

@router.get("/recommend", response_model=schemas.BuyerRecommendationResponse)
def recommend_buyers(
    listing_id: Optional[str] = Query(None, description="Optional listing ID to evaluate"),
    crop: Optional[str] = Query("Tomato", description="Crop name if no listing ID"),
    quantity_kg: Optional[float] = Query(200.0),
    db: Session = Depends(get_db)
):
    """
    Returns top 3 ranked buyers using exact 5-factor weighted algorithm:
    Mandi Price (35%), Distance (20%), Demand (20%), Trust Score (15%), Transport Cost (10%).
    """
    if listing_id:
        listing = db.query(models.ListingModel).filter(models.ListingModel.id == listing_id).first()
    else:
        listing = db.query(models.ListingModel).filter(models.ListingModel.crop_name.ilike(f"%{crop}%")).first()
        
    if not listing:
        # Generate temporary listing wrapper for ranking
        listing = models.ListingModel(
            id="TEMP-001",
            farmer_id="FARM-001",
            crop_name=crop,
            quantity_kg=quantity_kg,
            expected_price_per_kg=25.0,
            farmer_min_price=23.5,
            village="Murthal",
            district="Sonipat",
            state="Haryana",
            status="ACTIVE"
        )
        
    return RecommendationEngine.rank_buyers_for_listing(listing, db)
