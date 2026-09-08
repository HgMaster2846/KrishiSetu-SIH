import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from ..models import models
from ..config import settings

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
        
        # If Exotel or Twilio configured, dispatch via carrier asynchronously
        if settings.SMS_PROVIDER.lower() == "exotel" and settings.EXOTEL_API_KEY:
            from .exotel_service import ExotelService
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.create_task(ExotelService.send_sms(phone, message))
            except Exception:
                pass
                
        return log

    @classmethod
    def send_deal_offer_sms(
        cls,
        phone: str,
        buyer_name: str,
        crop: str,
        quantity_kg: float,
        price_per_kg: float,
        pickup_date: str,
        pickup_location: str,
        truck_info: str,
        deal_id: str,
        db: Session
    ) -> models.SMSLogModel:
        """
        Dispatches enriched deal offer SMS (Task 8):
        Includes Buyer, Crop, Quantity, Price, Pickup Date, Pickup Location, Truck (if pooled), Deal ID, Reply YES/NO.
        """
        total = round(quantity_kg * price_per_kg, 2)
        message = (
            f"[KrishiSetu AI] Naya Sauda Offer!\n"
            f"Deal ID: {deal_id}\n"
            f"Buyer: {buyer_name}\n"
            f"Fasal: {crop} ({quantity_kg:g} kg)\n"
            f"Daam: Rs {price_per_kg:g}/kg (Total: Rs {total:g})\n"
            f"Pickup: {pickup_date}, {pickup_location}\n"
            f"Truck: {truck_info}\n"
            f"Sauda pakka karne ke liye reply karein: YES (ya 1), radd karne ke liye: NO (ya 2)."
        )
        return cls.send_sms(phone, message, db)


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
