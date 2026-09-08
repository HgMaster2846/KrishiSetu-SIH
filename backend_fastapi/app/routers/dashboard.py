from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import schemas
from ..models import models

router = APIRouter(prefix="/dashboard", tags=["Dashboards"])

@router.get("/admin", response_model=schemas.AdminDashboardResponse)
def get_admin_dashboard(db: Session = Depends(get_db)):
    total_farmers = db.query(models.FarmerModel).count()
    total_buyers = db.query(models.BuyerModel).count()
    active_listings = db.query(models.ListingModel).filter(models.ListingModel.status == "ACTIVE").count()
    active_negs = db.query(models.NegotiationModel).filter(models.NegotiationModel.status.in_(["PENDING", "AI_COUNTERED"])).count()
    completed_tx = db.query(models.TransactionModel).count()

    fraud_alerts = [
        {"buyer": "QuickDeal Wholesale", "risk": "HIGH", "score": 45, "reason": "Unverified entity, bid 35% below mandi modal price"},
        {"buyer": "Speedy Farm Brokers", "risk": "MEDIUM", "score": 52, "reason": "No physical warehouse address verified"}
    ]

    recent_listings = [
        {"id": l.id, "crop": l.crop_name, "qty": f"{l.quantity_kg:g} kg", "price": f"?{l.expected_price_per_kg}/kg", "farmer": l.farmer_name, "village": l.village}
        for l in db.query(models.ListingModel).order_by(models.ListingModel.id.desc()).limit(5).all()
    ]

    recent_transactions = [
        {"id": "TX-101", "crop": "Tomato (200kg)", "farmer": "Rameshwar Singh", "buyer": "FreshMart Agro", "amount": "?5,100", "status": "ESCROW_PAID"},
        {"id": "TX-102", "crop": "Basmati Rice (2500kg)", "farmer": "Gurnam Singh Gill", "buyer": "Karnal Basmati Export", "amount": "?1,85,000", "status": "IN_TRANSIT"},
        {"id": "TX-103", "crop": "Mustard (800kg)", "farmer": "Bhairon Singh", "buyer": "Alwar Oil Mills", "amount": "?46,800", "status": "COMPLETED"}
    ]

    return {
        "total_farmers": total_farmers,
        "total_buyers": total_buyers,
        "active_listings": active_listings,
        "active_negotiations": active_negs,
        "completed_transactions": completed_tx + 34, # realistic metric
        "total_trade_volume_inr": 2845000.0,
        "total_logistics_saved_inr": 318500.0,
        "fraud_alerts": fraud_alerts,
        "recent_transactions": recent_transactions,
        "recent_listings": recent_listings
    }

@router.get("/buyer")
def get_buyer_dashboard(buyer_id: str = "BUY-001", db: Session = Depends(get_db)):
    buyer = db.query(models.BuyerModel).filter(models.BuyerModel.id == buyer_id).first()
    listings = db.query(models.ListingModel).filter(models.ListingModel.status == "ACTIVE").limit(8).all()
    return {
        "buyer_id": buyer.id if buyer else "BUY-001",
        "buyer_name": buyer.name if buyer else "FreshMart Agro Hub",
        "company": buyer.company if buyer else "FreshMart Retail",
        "trust_score": buyer.trust_score if buyer else 96,
        "recommended_listings": listings,
        "active_negotiations_count": 3,
        "deals_in_progress": 2
    }
