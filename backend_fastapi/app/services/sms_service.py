from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models import models

class SMSService:
    @classmethod
    def send_sms(cls, phone: str, message: str, db: Session) -> models.SMSLogModel:
        log = models.SMSLogModel(
            phone=phone,
            direction="OUTGOING",
            message=message,
            status="DELIVERED"
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    @classmethod
    def handle_incoming_sms(cls, phone: str, reply_text: str, db: Session) -> Dict[str, Any]:
        reply_clean = reply_text.strip().upper()
        log_in = models.SMSLogModel(
            phone=phone,
            direction="INCOMING",
            message=reply_text,
            status="RECEIVED"
        )
        db.add(log_in)
        db.commit()
        
        farmer = db.query(models.FarmerModel).filter(models.FarmerModel.phone == phone).first()
        tx = None
        if farmer:
            tx = db.query(models.TransactionModel).filter(
                models.TransactionModel.farmer_id == farmer.id,
                models.TransactionModel.status == "DISPATCH_SCHEDULED"
            ).order_by(models.TransactionModel.created_at.desc()).first()
            
        if reply_clean in ["YES", "1", "HAAN", "CONFIRM"]:
            if tx:
                tx.otp_verified = True
                tx.status = "IN_TRANSIT"
                db.commit()
                
                resp_msg = (
                    f"[KrishiSetu AI] Dhanyawad {farmer.name}! Aapka deal aur pickup confirm ho gaya hai. "
                    f"Truck HR-10-AJ-4821 Kal subah 8 AM pahunch raha hai. "
                    f"Pickup OTP: {tx.otp_code}. Payment Rs {tx.total_amount:g} Escrow mein surakshit hai."
                )
            else:
                resp_msg = "[KrishiSetu AI] Dhanyawad! Aapka response prapt ho gaya hai. Hum jald aapse sampark karenge."
        elif reply_clean in ["NO", "2", "NAHI"]:
            if tx:
                tx.status = "CANCELLED"
                db.commit()
            resp_msg = "[KrishiSetu AI] Aapka order radd kar diya gaya hai. Agle offer ke liye AI hotline 1800-260-3300 par call karein."
        else:
            resp_msg = "[KrishiSetu AI] Kripya deal confirm karne ke liye YES ya 1 reply karein, radd karne ke liye NO ya 2."

        cls.send_sms(phone, resp_msg, db)
        
        return {
            "status": "PROCESSED",
            "reply_received": reply_text,
            "response_sent": resp_msg,
            "transaction_id": tx.id if tx else None
        }

    @classmethod
    def get_logs(cls, phone: str, db: Session) -> List[Dict[str, Any]]:
        logs = db.query(models.SMSLogModel).filter(models.SMSLogModel.phone == phone).order_by(models.SMSLogModel.created_at.asc()).all()
        return [
            {
                "id": l.id,
                "phone": l.phone,
                "direction": l.direction,
                "message": l.message,
                "status": l.status,
                "timestamp": l.created_at.strftime("%I:%M %p, %d %b") if l.created_at else ""
            }
            for l in logs
        ]
