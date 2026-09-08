import re
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple
from sqlalchemy.orm import Session
from ..models import models

CROP_MAP = {
    "tamatar": "Tomato", "tomato": "Tomato",
    "pyaz": "Onion", "pyaj": "Onion", "onion": "Onion", "kanda": "Onion",
    "aloo": "Potato", "aalu": "Potato", "potato": "Potato", "batata": "Potato",
    "chawal": "Rice (Basmati 1121)", "dhan": "Rice (Basmati 1121)", "rice": "Rice (Basmati 1121)", "basmati": "Rice (Basmati 1121)",
    "gehun": "Wheat (Sharbati / MP)", "gehu": "Wheat (Sharbati / MP)", "wheat": "Wheat (Sharbati / MP)", "kanak": "Wheat (Sharbati / MP)",
    "sarson": "Mustard (Sarson)", "sarso": "Mustard (Sarson)", "mustard": "Mustard (Sarson)",
    "kapas": "Cotton (Kapas)", "cotton": "Cotton (Kapas)", "rui": "Cotton (Kapas)",
    "ganna": "Sugarcane", "sugarcane": "Sugarcane", "ik": "Sugarcane",
    "gobhi": "Cauliflower (Gobhi)", "phool gobhi": "Cauliflower (Gobhi)", "cauliflower": "Cauliflower (Gobhi)",
    "mirch": "Green Chilli (Hari Mirch)", "hari mirch": "Green Chilli (Hari Mirch)", "chilli": "Green Chilli (Hari Mirch)"
}

class AIVoiceService:
    @staticmethod
    def extract_crop_and_qty(text: str) -> Tuple[str, float]:
        text_lower = text.lower()
        detected_crop = "Tomato"
        for k, v in CROP_MAP.items():
            if k in text_lower:
                detected_crop = v
                break
        
        qty = 200.0
        match = re.search(r'(\d+(?:\.\d+)?)\s*(?:kilo|kg|kilos|quintal|k|quental)', text_lower)
        if match:
            val = float(match.group(1))
            if "quintal" in text_lower or "quental" in text_lower:
                qty = val * 100.0
            else:
                qty = val
        else:
            num_match = re.search(r'(\d+)', text_lower)
            if num_match:
                qty = float(num_match.group(1))
        return detected_crop, qty

    @staticmethod
    def extract_location(text: str) -> Tuple[str, str, str]:
        text_clean = text.strip()
        parts = [p.strip() for p in re.split(r'[,-]|\s+(?:se|mein|in)\s+', text_clean, flags=re.IGNORECASE) if p.strip()]
        
        village = "Murthal"
        district = "Sonipat"
        state = "Haryana"

        if len(parts) >= 2:
            village = parts[0].title()
            district = parts[1].title()
        elif len(parts) == 1:
            village = parts[0].title()
            district = parts[0].title()
        
        haryana_districts = ["sonipat", "panipat", "karnal", "ambala", "rohtak", "gurugram", "faridabad", "rewari"]
        punjab_districts = ["ludhiana", "khanna", "amritsar", "jalandhar", "bathinda", "muktsar", "patiala"]
        up_districts = ["meerut", "ghaziabad", "noida", "hapur", "baghpat", "muzaffarnagar", "mathura"]
        rajasthan_districts = ["alwar", "jaipur", "dausa", "kotputli", "khairthal", "chomu"]
        mp_districts = ["indore", "bhopal", "raisen", "sehore"]
        
        d_lower = district.lower()
        if any(d in d_lower for d in haryana_districts):
            state = "Haryana"
        elif any(d in d_lower for d in punjab_districts):
            state = "Punjab"
        elif any(d in d_lower for d in up_districts):
            state = "Uttar Pradesh"
        elif any(d in d_lower for d in rajasthan_districts):
            state = "Rajasthan"
        elif any(d in d_lower for d in mp_districts):
            state = "Madhya Pradesh"
            
        return village, district, state

    @staticmethod
    def extract_price(text: str) -> float:
        text_lower = text.lower()
        match = re.search(r'(\d+(?:\.\d+)?)\s*(?:rupaye|rupees|rs|rupya|inr|prati|kilo)', text_lower)
        if match:
            return float(match.group(1))
        match2 = re.search(r'(\d+(?:\.\d+)?)', text_lower)
        if match2:
            return float(match2.group(1))
        return 25.0

    @classmethod
    def process_voice_step(cls, step: int, user_speech: str, phone: str, session_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
        session_data = session_data or {}
        
        if step == 0:
            ai_speech = "Namaste! KrishiSetu AI mein aapka swagat hai. Main aapka Digital Mandi Sahayak hoon. Aap konsi fasal bechna chahte hain aur kitni maatra hai?"
            return {
                "step": 1,
                "ai_speech": ai_speech,
                "is_final": False,
                "extracted_entities": {},
                "created_listing_id": None,
                "session_data": {"phone": phone}
            }

        elif step == 1:
            crop_name, qty = cls.extract_crop_and_qty(user_speech)
            session_data["crop_name"] = crop_name
            session_data["quantity_kg"] = qty
            
            ai_speech = f"Maine darj kar liya hai: {qty:g} kilo {crop_name}. Aap kis gaon aur zile se bol rahe hain?"
            return {
                "step": 2,
                "ai_speech": ai_speech,
                "is_final": False,
                "extracted_entities": {"crop_name": crop_name, "quantity_kg": qty},
                "created_listing_id": None,
                "session_data": session_data
            }

        elif step == 2:
            village, district, state = cls.extract_location(user_speech)
            session_data["village"] = village
            session_data["district"] = district
            session_data["state"] = state
            
            ai_speech = f"{village}, {district} se. Bahut achha. Aapko apni fasal ke liye kitna daam chahiye prati kilo?"
            return {
                "step": 3,
                "ai_speech": ai_speech,
                "is_final": False,
                "extracted_entities": {
                    "crop_name": session_data.get("crop_name"),
                    "quantity_kg": session_data.get("quantity_kg"),
                    "village": village,
                    "district": district,
                    "state": state
                },
                "created_listing_id": None,
                "session_data": session_data
            }

        else:
            price = cls.extract_price(user_speech)
            session_data["expected_price"] = price
            
            crop_name = session_data.get("crop_name", "Tomato")
            qty = session_data.get("quantity_kg", 200.0)
            village = session_data.get("village", "Murthal")
            district = session_data.get("district", "Sonipat")
            state = session_data.get("state", "Haryana")
            
            farmer = db.query(models.FarmerModel).filter(models.FarmerModel.phone == phone).first()
            if not farmer:
                farmer_id = "FARM-" + datetime.utcnow().strftime("%H%M%S")
                farmer = models.FarmerModel(
                    id=farmer_id,
                    name="Kisan Sathi",
                    phone=phone,
                    village=village,
                    district=district,
                    state=state,
                    language="hi"
                )
                db.add(farmer)
                db.commit()
            
            mandi_row = db.query(models.MandiPriceModel).filter(models.MandiPriceModel.crop_name.ilike(f"%{crop_name}%")).first()
            benchmark = mandi_row.modal_price if mandi_row else round(price * 1.03, 1)
            
            listing_id = "LIST-" + datetime.utcnow().strftime("%M%S")
            new_listing = models.ListingModel(
                id=listing_id,
                farmer_id=farmer.id,
                farmer_name=farmer.name,
                farmer_phone=farmer.phone,
                crop_name=crop_name,
                quantity_kg=qty,
                expected_price_per_kg=price,
                farmer_min_price=round(price * 0.90, 1),
                current_best_offer=None,
                village=village,
                district=district,
                state=state,
                harvest_date=(datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d"),
                quality_grade="Grade A",
                status="ACTIVE",
                ai_mandi_benchmark=benchmark,
                created_via="AI_HOTLINE_VOICE",
                created_at=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            )
            db.add(new_listing)
            
            sms_msg = f"[KrishiSetu AI] Namaste! Aapka {qty:g}kg {crop_name} listing darj ho gaya hai (ID: {listing_id}). Expected daam: Rs {price}/kg. Mandi rate: Rs {benchmark}/kg. Khareedaar aate hi SMS milega."
            sms_log = models.SMSLogModel(
                phone=phone,
                direction="OUTGOING",
                message=sms_msg,
                status="DELIVERED"
            )
            db.add(sms_log)
            db.commit()
            
            ai_speech = (
                f"Bahut badhiya {farmer.name} ji! Aapka {qty:g} kilo {crop_name}, "
                f"{village} ({district}) se, {price:g} rupaye prati kilo par darj kar liya gaya hai. "
                f"Azadpur mandi ka ausat daam {benchmark:g} rupaye chal raha hai. "
                f"Jaise hi buyer ka offer aayega, AI aapke paksh mein behtareen mol-bhav karega "
                f"aur aapko SMS aayega. KrishiSetu AI par call karne ke liye dhanyawad!"
            )
            
            return {
                "step": 4,
                "ai_speech": ai_speech,
                "is_final": True,
                "extracted_entities": {
                    "listing_id": listing_id,
                    "farmer_name": farmer.name,
                    "crop_name": crop_name,
                    "quantity_kg": qty,
                    "expected_price": price,
                    "village": village,
                    "district": district,
                    "state": state,
                    "mandi_benchmark": benchmark
                },
                "created_listing_id": listing_id,
                "session_data": session_data
            }
