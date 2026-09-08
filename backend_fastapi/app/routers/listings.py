from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import schemas
from ..models import models

router = APIRouter(prefix="/listing", tags=["Marketplace Listings"])

@router.post("/create", response_model=schemas.ListingResponse)
def create_listing(req: schemas.ListingCreate, db: Session = Depends(get_db)):
    farmer = db.query(models.FarmerModel).filter(models.FarmerModel.phone == req.farmer_phone).first()
    if not farmer:
        farmer = models.FarmerModel(
            id=f"FARM-{datetime.utcnow().strftime('%H%M%S')}",
            name=req.farmer_name or "Kisan Sathi",
            phone=req.farmer_phone or "+919812345001",
            village=req.village,
            district=req.district,
            state=req.state,
            language="hi"
        )
        db.add(farmer)
        db.commit()

    mandi = db.query(models.MandiPriceModel).filter(models.MandiPriceModel.crop_name.ilike(f"%{req.crop_name}%")).first()
    benchmark = mandi.modal_price if mandi else round(req.expected_price_per_kg * 1.03, 1)

    lid = f"LIST-{datetime.utcnow().strftime('%M%S')}"
    listing = models.ListingModel(
        id=lid,
        farmer_id=farmer.id,
        farmer_name=farmer.name,
        farmer_phone=farmer.phone,
        crop_name=req.crop_name,
        category=req.category or "Vegetable",
        quantity_kg=req.quantity_kg,
        expected_price_per_kg=req.expected_price_per_kg,
        farmer_min_price=req.farmer_min_price or round(req.expected_price_per_kg * 0.90, 1),
        current_best_offer=None,
        village=req.village,
        district=req.district,
        state=req.state,
        harvest_date=req.harvest_date or (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d"),
        description=f"Fresh harvest {req.crop_name} from {req.village}, {req.district}",
        quality_grade=req.quality_grade or "Grade A",
        status="ACTIVE",
        ai_mandi_benchmark=benchmark,
        recommended_buyer_id="BUY-001",
        created_via=req.created_via or "AI_HOTLINE_VOICE",
        created_at=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    )
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing

@router.get("/all", response_model=List[schemas.ListingResponse])
def get_all_listings(
    crop: Optional[str] = None,
    status: Optional[str] = None,
    state: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(models.ListingModel)
    if crop:
        query = query.filter(models.ListingModel.crop_name.ilike(f"%{crop}%"))
    if status:
        query = query.filter(models.ListingModel.status == status)
    if state:
        query = query.filter(models.ListingModel.state.ilike(f"%{state}%"))
    return query.order_by(models.ListingModel.id.desc()).limit(limit).all()

@router.get("/{id}", response_model=schemas.ListingResponse)
def get_listing_by_id(id: str, db: Session = Depends(get_db)):
    listing = db.query(models.ListingModel).filter(models.ListingModel.id == id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing
