import httpx
import base64
from typing import Dict, Any, Optional
from ..config import settings

SARVAM_STT_URL = "https://api.sarvam.ai/speech-to-text"
SARVAM_TTS_URL = "https://api.sarvam.ai/text-to-speech"

class SarvamService:
    @staticmethod
    async def verify_key() -> Dict[str, Any]:
        """Validates the Sarvam AI subscription key."""
        if not settings.SARVAM_API_KEY:
            return {"valid": False, "message": "Sarvam API Key not configured"}
        
        headers = {
            "api-subscription-key": settings.SARVAM_API_KEY,
            "Content-Type": "application/json"
        }
        # Minimal probe payload
        payload = {
            "inputs": ["नमस्ते"],
            "target_language_code": "hi-IN",
            "speaker": "meera",
            "model": "bulbul:v1"
        }
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                res = await client.post(SARVAM_TTS_URL, headers=headers, json=payload)
                if res.status_code in (200, 201):
                    return {"valid": True, "message": "Sarvam Voice AI (Saaras + Bulbul) verified active"}
                return {"valid": False, "message": f"Sarvam returned HTTP {res.status_code}: {res.text[:120]}"}
        except Exception as e:
            return {"valid": False, "message": f"Sarvam connection error: {str(e)}"}

    @staticmethod
    async def speech_to_text(audio_bytes: bytes, language: str = "hi-IN") -> str:
        """Converts raw audio bytes to text using Sarvam Saaras."""
        if not settings.SARVAM_API_KEY:
            return ""
        
        headers = {"api-subscription-key": settings.SARVAM_API_KEY}
        files = {"file": ("farmer_audio.wav", audio_bytes, "audio/wav")}
        data = {"language_code": language, "model": "saaras:v1"}
        
        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                res = await client.post(SARVAM_STT_URL, headers=headers, files=files, data=data)
                if res.status_code == 200:
                    return res.json().get("transcript", "")
        except Exception:
            pass
        return ""

    @staticmethod
    async def text_to_speech(text: str, language: str = "hi-IN") -> Optional[bytes]:
        """Synthesizes speech using Sarvam Bulbul in Hindi."""
        if not settings.SARVAM_API_KEY:
            return None
            
        headers = {
            "api-subscription-key": settings.SARVAM_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": [text],
            "target_language_code": language,
            "speaker": "meera",
            "model": "bulbul:v1"
        }
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(SARVAM_TTS_URL, headers=headers, json=payload)
                if res.status_code == 200:
                    audios = res.json().get("audios", [])
                    if audios:
                        return base64.b64decode(audios[0])
        except Exception:
            pass
        return None

    @classmethod
    async def speech_to_text_from_url(cls, recording_url: str, language: str = "hi-IN") -> str:
        """Downloads audio file from Exotel or carrier URL and transcribes via Sarvam."""
        if not recording_url:
            return ""
        try:
            auth = None
            if settings.EXOTEL_API_KEY and settings.EXOTEL_API_SECRET and "exotel.com" in recording_url:
                auth = (settings.EXOTEL_API_KEY, settings.EXOTEL_API_SECRET)
            async with httpx.AsyncClient(timeout=25.0, follow_redirects=True) as client:
                res = await client.get(recording_url, auth=auth)
                if res.status_code == 200 and len(res.content) > 0:
                    return await cls.speech_to_text(res.content, language=language)
        except Exception:
            pass
        return ""

    @staticmethod
    def cache_audio(audio_bytes: bytes) -> str:
        """Stores synthesized audio in memory and returns unique audio_id."""
        import uuid
        import time
        audio_id = f"aud_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        AUDIO_CACHE[audio_id] = audio_bytes
        # Evict old items if cache exceeds 100 entries
        if len(AUDIO_CACHE) > 100:
            oldest_key = next(iter(AUDIO_CACHE))
            AUDIO_CACHE.pop(oldest_key, None)
        return audio_id

    @staticmethod
    def get_cached_audio(audio_id: str) -> Optional[bytes]:
        """Retrieves cached audio bytes by audio_id."""
        # Clean audio_id in case .wav extension was appended
        clean_id = audio_id.replace(".wav", "").replace(".mp3", "")
        return AUDIO_CACHE.get(clean_id) or AUDIO_CACHE.get(audio_id)

AUDIO_CACHE: Dict[str, bytes] = {}
