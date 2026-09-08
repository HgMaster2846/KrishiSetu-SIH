from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import schemas
from ..services.negotiation_service import NegotiationService
from ..models import models

router = APIRouter(prefix="/negotiation", tags=["AI Negotiation"])

@router.post("/start", response_model=schemas.NegotiationResponse)
def start_negotiation(req: schemas.NegotiationStartRequest, db: Session = Depends(get_db)):
    """
    Starts an AI-managed negotiation round on behalf of the farmer.
    """
    try:
        return NegotiationService.start_negotiation(req.listing_id, req.buyer_id, req.buyer_offer_per_kg, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/respond", response_model=schemas.NegotiationResponse)
def respond_negotiation(req: schemas.NegotiationRespondRequest, db: Session = Depends(get_db)):
    """
    Buyer counter-offers, accepts, or rejects. AI counter-acts protecting farmer reserve price.
    """
    try:
        return NegotiationService.respond_to_negotiation(req.negotiation_id, req.buyer_counter_offer, req.action, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id}/history", response_model=schemas.NegotiationResponse)
def get_negotiation_history(id: str, db: Session = Depends(get_db)):
    try:
        return NegotiationService.get_negotiation_details(id, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
