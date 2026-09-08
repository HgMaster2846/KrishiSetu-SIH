import json
import re
import httpx
from typing import Dict, Any, Optional
from ..config import settings

FARMER_ASSISTANT_SYSTEM_PROMPT = """
You are KrishiSetu AI (कृषिसेतु एआई), an empathetic, polite, and farmer-first AI agricultural assistant for Indian farmers.
You converse naturally in Hindi (or Hinglish), keeping answers concise and spoken-friendly (1-2 short sentences max).

Your goal in this phone call is to collect:
1. Crop name (e.g. Tamatar, Pyaz, Aloo, Gehun, Chawal, Sarson)
2. Quantity in kilograms or quintals
3. Location: Village and District (Sonipat, Karnal, Ludhiana, etc.)
4. Expected price per kg (in Rupees)
5. Harvest readiness or pickup preference

When enough information is gathered, output a JSON block:
```json
{
  "action": "LISTING_CONFIRMED",
  "crop_name": "Tomato",
  "quantity_kg": 200,
  "village": "Murthal",
  "district": "Sonipat",
  "state": "Haryana",
  "expected_price": 25.0,
  "farmer_speech_summary": "200 kg tamatar from Murthal at Rs 25/kg",
  "ai_speech": "Bahut badhiya! Aapka 200 kilo tamatar Rs 25/kg par darj ho gaya hai. Abhi SMS bhej rahe hain."
}
```
If you still need more information, respond naturally:
```json
{
  "action": "CONTINUE",
  "ai_speech": "Namaste! Main KrishiSetu AI hoon. Aap kaunsi fasal bechna chahte hain aur kitna maal hai?"
}
```
"""

class GeminiService:
    @staticmethod
    async def verify_key() -> Dict[str, Any]:
        """Validates Google Gemini API Key."""
        if not settings.GEMINI_API_KEY:
            return {"valid": False, "message": "Gemini API Key not configured"}
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={settings.GEMINI_API_KEY}"
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                res = await client.get(url)
                if res.status_code == 200:
                    return {"valid": True, "message": "Gemini AI (2.5 / 2.0 Flash) connected & ready"}
                return {"valid": False, "message": f"Gemini API returned HTTP {res.status_code}: {res.text[:100]}"}
        except Exception as e:
            return {"valid": False, "message": f"Gemini connection failed: {str(e)}"}

    @staticmethod
    async def process_conversation_step(
        user_speech: str,
        conversation_history: list,
        phone: str = ""
    ) -> Dict[str, Any]:
        """
        Sends conversation step to Gemini 2.0/2.5 Flash for natural Hindi reasoning.
        Falls back seamlessly to local regex / rules if Gemini API is not configured or offline.
        """
        if not settings.GEMINI_API_KEY:
            return None # Trigger fallback to AIVoiceService
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={settings.GEMINI_API_KEY}"
        
        # Build contents from history
        contents = [
            {"role": "user", "parts": [{"text": FARMER_ASSISTANT_SYSTEM_PROMPT}]}
        ]
        for turn in conversation_history:
            contents.append(turn)
        contents.append({"role": "user", "parts": [{"text": f"Farmer ({phone}) said: '{user_speech}'"}]})
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 400
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=12.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                        # Try parsing JSON
                        match = re.search(r'\{.*\}', text, re.DOTALL)
                        if match:
                            return json.loads(match.group())
        except Exception:
            pass
        return None

    @classmethod
    async def extract_entities_with_gemini(cls, user_speech: str) -> Optional[Dict[str, Any]]:
        """
        Uses Gemini to extract agricultural entities from spoken Hindi text.
        Returns dict with crop_name, quantity_kg, village, district, state, expected_price, or confirmation_response.
        """
        if not settings.GEMINI_API_KEY or not user_speech:
            return None
        
        prompt = f"""
You are an expert NLP parser for Indian agriculture in Hindi/Hinglish.
Analyze the farmer's speech: "{user_speech}"

Extract whatever entities are mentioned and respond ONLY in valid JSON format:
{{
  "crop_name": "<Standard English crop name like Tomato, Potato, Onion, Rice (Basmati 1121), Wheat (Sharbati / MP), Mustard (Sarson), etc., or null if not mentioned>",
  "quantity_kg": <float value in kg or null (e.g. 200, or 2000 for 20 quintal)>,
  "village": "<village name or null>",
  "district": "<district name or null>",
  "state": "<Indian state name or null>",
  "expected_price_per_kg": <float price in INR/kg or null>,
  "confirmation_intent": "<'YES' if confirming agreement (haan, sahi hai, yes, ok, bilkul), 'NO' if rejecting (nahi, galat, na, no), 'CORRECTION' if correcting a field, or null>",
  "correction_field": "<'crop', 'quantity', 'location', 'price', or null>"
}}
"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={settings.GEMINI_API_KEY}"
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.1, "maxOutputTokens": 250}
        }
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    candidates = res.json().get("candidates", [])
                    if candidates:
                        text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                        match = re.search(r'\{.*\}', text, re.DOTALL)
                        if match:
                            return json.loads(match.group())
        except Exception:
            pass
        return None


    @staticmethod
    async def negotiate_counter_offer(
        farmer_min: float,
        buyer_offer: float,
        mandi_avg: float,
        crop: str = "Tomato"
    ) -> Dict[str, Any]:
        """
        Calculates an intelligent counter-offer protecting the farmer's margin.
        """
        if buyer_offer >= mandi_avg:
            counter = buyer_offer
            accepted = True
            reasoning = f"Buyer offer (Rs {buyer_offer}) meets or exceeds APMC Mandi average (Rs {mandi_avg}). Deal accepted!"
        elif buyer_offer < farmer_min:
            # Never accept below farmer limit! Counter at midpoint of mandi and reserve
            counter = max(farmer_min, round((farmer_min + mandi_avg) / 2, 1))
            accepted = False
            reasoning = (
                f"Buyer offer of Rs {buyer_offer}/kg is below farmer's reserve limit of Rs {farmer_min}/kg. "
                f"KrishiSetu AI generated counter-offer of Rs {counter}/kg to protect farmer livelihood."
            )
        else:
            counter = round((buyer_offer + mandi_avg) / 2, 1)
            accepted = False
            reasoning = f"Countering with APMC-indexed price Rs {counter}/kg to capture maximum surplus for farmer."

        return {
            "accepted": accepted,
            "counter_offer": counter,
            "farmer_min_price": farmer_min,
            "buyer_offer": buyer_offer,
            "mandi_avg": mandi_avg,
            "reasoning": reasoning
        }
