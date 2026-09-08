import httpx
from typing import Dict, Any
from ..config import settings

class TelephonyFallbackService:
    @staticmethod
    async def verify_twilio() -> Dict[str, Any]:
        """Validates Twilio Account SID and Auth Token."""
        if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
            return {"valid": False, "message": "Twilio fallback credentials not set"}
            
        url = f"https://api.twilio.com/2010-04-01/Accounts/{settings.TWILIO_ACCOUNT_SID}.json"
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                res = await client.get(
                    url,
                    auth=(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                )
                if res.status_code == 200:
                    return {"valid": True, "message": "Twilio fallback active & verified"}
                return {"valid": False, "message": f"Twilio returned HTTP {res.status_code}"}
        except Exception as e:
            return {"valid": False, "message": f"Twilio error: {str(e)}"}

    @staticmethod
    async def send_sms(to_phone: str, message: str) -> Dict[str, Any]:
        """Dispatches an SMS via Twilio API."""
        if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
            return {"success": False, "message": "Twilio credentials missing"}
            
        url = f"https://api.twilio.com/2010-04-01/Accounts/{settings.TWILIO_ACCOUNT_SID}/Messages.json"
        payload = {
            "From": settings.TWILIO_PHONE_NUMBER,
            "To": to_phone,
            "Body": message
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(
                    url,
                    auth=(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN),
                    data=payload
                )
                if res.status_code in (200, 201):
                    return {"success": True, "provider": "twilio", "message": "SMS dispatched via Twilio"}
                return {"success": False, "message": f"Twilio SMS error: {res.text[:100]}"}
        except Exception as e:
            return {"success": False, "message": str(e)}
