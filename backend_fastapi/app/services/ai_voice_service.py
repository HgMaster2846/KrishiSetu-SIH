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
        speech_clean = (user_speech or "").strip()
        speech_lower = speech_clean.lower()
        conf_state = session_data.get("confirmation_state", "PENDING")

        # Step 0: Initial Greeting
        if step == 0:
            ai_speech = "Namaste! KrishiSetu AI mein aapka swagat hai. Main aapka Digital Mandi Sahayak hoon. Aap konsi fasal bechna chahte hain aur kitni maatra hai?"
            session_data["confirmation_state"] = "PENDING"
            session_data["phone"] = phone
            return {
                "step": 1,
                "ai_speech": ai_speech,
                "is_final": False,
                "extracted_entities": {},
                "created_listing_id": None,
                "confirmation_state": "PENDING",
                "session_data": session_data
            }

        # Handle Mandatory Confirmation (Task 4)
        if conf_state == "AWAITING_CONFIRMATION" or step == 4:
            is_no = any(w in speech_lower for w in ["nahi", "galat", "na", "no", "badal", "change", "2", "mat", "nhi", "wrong"]) or speech_lower == "2"
            is_yes = (not is_no) and (any(w in speech_lower for w in ["haan", "bilkul", "theek", "yes", "han", "confirm", "1"]) or "sahi hai" in speech_lower or speech_lower == "1")

            if is_yes:
                # Farmer Confirmed -> Create Listing & Trigger Real Matching Pipeline
                crop_name = session_data.get("crop_name", "Tomato")
                qty = float(session_data.get("quantity_kg", 200.0))
                village = session_data.get("village", "Murthal")
                district = session_data.get("district", "Sonipat")
                state = session_data.get("state", "Haryana")
                price = float(session_data.get("expected_price", 25.0))

                # Lookup / Register Farmer
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

                # Mandi Benchmark
                mandi_row = db.query(models.MandiPriceModel).filter(models.MandiPriceModel.crop_name.ilike(f"%{crop_name}%")).first()
                benchmark = mandi_row.modal_price if mandi_row else round(price * 1.03, 1)

                # Persist Listing
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
                db.commit()

                # Trigger Buyer Recommendation (Task 6)
                from .recommendation_service import RecommendationEngine
                rec_result = RecommendationEngine.rank_buyers_for_listing(new_listing, db)
                top_recs = rec_result.get("recommendations", [])
                top_buyer_name = top_recs[0]["buyer"]["name"] if top_recs else "Verified Mandi Buyer"
                top_buyer_price = top_recs[0]["offered_price_per_kg"] if top_recs else price

                # Trigger Logistics AI Match (Task 7)
                from .logistics_service import LogisticsService
                logistics_info = LogisticsService.get_top_logistics_pitch(village, district, "Azadpur Mandi, Delhi", qty, db)
                logistics_pitch = logistics_info.get("spoken_pitch", "")
                truck_num = logistics_info.get("best_truck", {}).get("truck_number", "HR-10-AJ-4821") if logistics_info.get("best_truck") else "HR-10-AJ-4821"

                # Trigger Enriched SMS (Task 8)
                from .sms_service import SMSService
                deal_id = f"DEAL-{listing_id[-4:]}"
                SMSService.send_deal_offer_sms(
                    phone=phone,
                    buyer_name=top_buyer_name,
                    crop=crop_name,
                    quantity_kg=qty,
                    price_per_kg=top_buyer_price,
                    pickup_date="Kal Subah 8:00 AM",
                    pickup_location=f"{village}, {district}",
                    truck_info=f"Pooled Truck ({truck_num})",
                    deal_id=deal_id,
                    db=db
                )

                session_data["confirmation_state"] = "CONFIRMED"
                session_data["created_listing_id"] = listing_id
                session_data["selected_buyer"] = top_recs[0] if top_recs else {}
                session_data["logistics_offer"] = logistics_info

                ai_speech = (
                    f"Bahut badhiya {farmer.name} ji! Aapka {qty:g} kilo {crop_name} listing darj ho gaya hai (ID {listing_id}). "
                    f"{top_buyer_name} ne ₹{top_buyer_price:g} prati kilo ka offer diya hai. "
                    f"{logistics_pitch} "
                    f"Offer SMS aapke phone par bhej diya hai. Sauda pakka karne ke liye SMS par YES reply karein. "
                    f"KrishiSetu AI par call karne ke liye dhanyawad!"
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
                        "mandi_benchmark": benchmark,
                        "top_buyer": top_buyer_name,
                        "top_buyer_price": top_buyer_price
                    },
                    "created_listing_id": listing_id,
                    "confirmation_state": "CONFIRMED",
                    "session_data": session_data
                }

            elif is_no:
                # Farmer Rejected -> Ask what to correct (Task 4)
                session_data["confirmation_state"] = "CORRECTION"
                return {
                    "step": 5,
                    "ai_speech": "Koi baat nahi. Aap kaunsi jankari badalna chahte hain? Fasal, maatra, gaon, ya daam?",
                    "is_final": False,
                    "extracted_entities": session_data,
                    "confirmation_state": "CORRECTION",
                    "session_data": session_data
                }

        # Handle Correction State (Step 5)
        if conf_state == "CORRECTION" or step == 5:
            if any(w in speech_lower for w in ["tamatar", "pyaz", "aloo", "gehun", "chawal", "sarson", "fasal"]):
                c, _ = cls.extract_crop_and_qty(user_speech)
                session_data["crop_name"] = c
            if any(w in speech_lower for w in ["kilo", "kg", "quintal", "maatra"]) or any(char.isdigit() for char in speech_lower):
                _, q = cls.extract_crop_and_qty(user_speech)
                if q > 0:
                    session_data["quantity_kg"] = q
            if any(w in speech_lower for w in ["gaon", "zila", "district", "se", "mein"]):
                v, d, s = cls.extract_location(user_speech)
                session_data["village"] = v
                session_data["district"] = d
                session_data["state"] = s
            if any(w in speech_lower for w in ["rupaye", "rs", "daam", "rate", "bhav", "paisa"]):
                p = cls.extract_price(user_speech)
                session_data["expected_price"] = p

            session_data["confirmation_state"] = "AWAITING_CONFIRMATION"
            crop = session_data.get("crop_name", "Tomato")
            qty = session_data.get("quantity_kg", 200.0)
            village = session_data.get("village", "Murthal")
            district = session_data.get("district", "Sonipat")
            price = session_data.get("expected_price", 25.0)

            ai_speech = (
                f"Maine badal diya hai: {qty:g} kilo {crop}, {village}, {district} se, "
                f"daam ₹{price:g} prati kilo. Kya ab ye sab sahi hai? Haan ya Na bolein."
            )
            return {
                "step": 4,
                "ai_speech": ai_speech,
                "is_final": False,
                "extracted_entities": session_data,
                "confirmation_state": "AWAITING_CONFIRMATION",
                "session_data": session_data
            }

        # Step 1: Crop & Quantity Extraction (Never ask already answered questions - Task 3)
        if step == 1 or ("crop_name" not in session_data and "quantity_kg" not in session_data):
            crop_name, qty = cls.extract_crop_and_qty(user_speech)
            session_data["crop_name"] = crop_name
            session_data["quantity_kg"] = qty
            
            # Check if user already provided location or price in this first sentence!
            if any(sep in speech_lower for sep in [" se", " mein", "from", ","]):
                v, d, s = cls.extract_location(user_speech)
                if v != "Murthal" or "murthal" in speech_lower:
                    session_data["village"] = v
                    session_data["district"] = d
                    session_data["state"] = s
            if any(p_word in speech_lower for p_word in ["rupaye", "rs", "rate", "daam"]):
                session_data["expected_price"] = cls.extract_price(user_speech)

        # Step 2: Location Extraction
        elif step == 2 or ("village" not in session_data):
            v, d, s = cls.extract_location(user_speech)
            session_data["village"] = v
            session_data["district"] = d
            session_data["state"] = s
            if any(p_word in speech_lower for p_word in ["rupaye", "rs", "rate", "daam"]):
                session_data["expected_price"] = cls.extract_price(user_speech)

        # Step 3: Price Extraction
        elif step == 3 or ("expected_price" not in session_data):
            session_data["expected_price"] = cls.extract_price(user_speech)

        # Intelligently decide next turn based on missing entities
        crop = session_data.get("crop_name")
        qty = session_data.get("quantity_kg")
        village = session_data.get("village")
        district = session_data.get("district")
        price = session_data.get("expected_price")

        if not crop or not qty:
            return {
                "step": 1,
                "ai_speech": "Aap konsi fasal bechna chahte hain aur kitni maatra hai?",
                "is_final": False,
                "extracted_entities": session_data,
                "created_listing_id": None,
                "session_data": session_data
            }
        elif not village or not district:
            return {
                "step": 2,
                "ai_speech": f"Maine darj kar liya hai: {qty:g} kilo {crop}. Aap kis gaon aur zile se bol rahe hain?",
                "is_final": False,
                "extracted_entities": session_data,
                "created_listing_id": None,
                "session_data": session_data
            }
        elif price is None:
            return {
                "step": 3,
                "ai_speech": f"{village}, {district} se. Bahut achha. Aapko apni fasal ke liye kitna daam chahiye prati kilo?",
                "is_final": False,
                "extracted_entities": session_data,
                "created_listing_id": None,
                "session_data": session_data
            }
        else:
            # All 4 fields present -> Enter Mandatory Confirmation Flow (Task 4)
            session_data["confirmation_state"] = "AWAITING_CONFIRMATION"
            ai_speech = (
                f"Maine aapki jankari darj kar li hai: {qty:g} kilo {crop}, {village}, {district} se, "
                f"daam ₹{price:g} prati kilo. Ye sab sahi hai? Haan ya Na bolein."
            )
            return {
                "step": 4,
                "ai_speech": ai_speech,
                "is_final": False,
                "extracted_entities": {
                    "crop_name": crop,
                    "quantity_kg": qty,
                    "village": village,
                    "district": district,
                    "expected_price": price
                },
                "created_listing_id": None,
                "confirmation_state": "AWAITING_CONFIRMATION",
                "session_data": session_data
            }

