from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import schemas
from ..services.sms_service import SMSService

router = APIRouter(prefix="/sms", tags=["SMS Gateway"])

@router.post("/send")
def send_sms(req: schemas.SMSSendRequest, db: Session = Depends(get_db)):
    log = SMSService.send_sms(req.phone, req.message, db)
    return {"status": "SENT", "id": log.id, "phone": log.phone, "message": log.message}

@router.post("/reply")
def reply_sms(req: schemas.SMSReplyRequest, db: Session = Depends(get_db)):
    """
    Simulates incoming SMS from feature phone farmer (e.g. 'YES', '1', 'NO').
    """
    return SMSService.handle_incoming_sms(req.phone, req.reply_text, db)

@router.get("/logs", response_model=List[schemas.SMSLogResponse])
def get_sms_logs(phone: str = Query("+919812345001"), db: Session = Depends(get_db)):
    return SMSService.get_logs(phone, db)
