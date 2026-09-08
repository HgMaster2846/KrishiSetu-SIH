import httpx
import base64
import io
import wave
import math
import logging
from typing import Dict, Any, Optional
import numpy as np
from scipy import signal
from ..config import settings

logger = logging.getLogger("krishisetu.sarvam")

SARVAM_STT_URL = "https://api.sarvam.ai/speech-to-text"
SARVAM_TTS_URL = "https://api.sarvam.ai/text-to-speech"

def convert_to_telephony_pcm(audio_bytes: bytes, target_rate: int = 8000) -> bytes:
    """
    Converts arbitrary WAV audio bytes into telephony-standard
    8000 Hz, 16-bit, Mono PCM WAV format.
    Required by telecom carrier media gateways (Exotel).
    """
    if not audio_bytes or len(audio_bytes) < 44 or not audio_bytes.startswith(b"RIFF"):
        return audio_bytes

    try:
        with io.BytesIO(audio_bytes) as in_io:
            with wave.open(in_io, "rb") as wf:
                n_channels = wf.getnchannels()
                sampwidth = wf.getsampwidth()
                framerate = wf.getframerate()
                n_frames = wf.getnframes()
                raw_frames = wf.readframes(n_frames)

        # If already 8000 Hz, mono (1 channel), 16-bit (2 bytes)
        if framerate == target_rate and n_channels == 1 and sampwidth == 2:
            return audio_bytes

        # Decode samples according to sampwidth
        if sampwidth == 2:
            data = np.frombuffer(raw_frames, dtype=np.int16)
        elif sampwidth == 1:
            data = ((np.frombuffer(raw_frames, dtype=np.uint8).astype(np.int32) - 128) * 256).astype(np.int16)
        elif sampwidth == 4:
            data = (np.frombuffer(raw_frames, dtype=np.int32) / 65536).astype(np.int16)
        else:
            return audio_bytes

        # Convert multi-channel to mono
        if n_channels > 1:
            data = data.reshape(-1, n_channels)
            data = data.mean(axis=1).astype(np.int16)

        # Resample to target_rate (e.g. 8000 Hz)
        if framerate != target_rate:
            gcd = math.gcd(framerate, target_rate)
            up = target_rate // gcd
            down = framerate // gcd
            resampled = signal.resample_poly(data, up, down)
            resampled = np.clip(resampled, -32768, 32767).astype(np.int16)
        else:
            resampled = data

        # Package into 8kHz mono 16-bit WAV
        out_io = io.BytesIO()
        with wave.open(out_io, "wb") as out_wf:
            out_wf.setnchannels(1)
            out_wf.setsampwidth(2)
            out_wf.setframerate(target_rate)
            out_wf.writeframes(resampled.tobytes())

        telephony_bytes = out_io.getvalue()
        logger.info(f"AUDIO_RESAMPLED: {framerate}Hz ({n_channels}ch) -> {target_rate}Hz (1ch mono), size: {len(audio_bytes)} -> {len(telephony_bytes)} bytes")
        return telephony_bytes

    except Exception as e:
        logger.warning(f"Audio resampling failed: {e}; returning original bytes")
        return audio_bytes

class SarvamService:
    @staticmethod
    def convert_to_telephony_pcm(audio_bytes: bytes, target_rate: int = 8000) -> bytes:
        return convert_to_telephony_pcm(audio_bytes, target_rate=target_rate)

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
            "speaker": "priya",
            "model": "bulbul:v3"
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
        """Synthesizes speech using Sarvam Bulbul in Hindi and converts to 8kHz mono PCM WAV for telecom carrier."""
        if not settings.SARVAM_API_KEY:
            return None
            
        headers = {
            "api-subscription-key": settings.SARVAM_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": [text],
            "target_language_code": language,
            "speaker": "priya",
            "model": "bulbul:v3"
        }
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(SARVAM_TTS_URL, headers=headers, json=payload)
                if res.status_code == 200:
                    audios = res.json().get("audios", [])
                    if audios:
                        raw_wav = base64.b64decode(audios[0])
                        # Convert to 8kHz telephony mono PCM WAV
                        return convert_to_telephony_pcm(raw_wav, target_rate=8000)
        except Exception as e:
            logger.error(f"Sarvam text_to_speech failed: {e}")
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
        """Stores synthesized audio in memory (ensuring 8kHz PCM) and returns unique audio_id."""
        import uuid
        import time
        # Ensure audio is 8000 Hz telephony PCM
        pcm_bytes = convert_to_telephony_pcm(audio_bytes, target_rate=8000)
        audio_id = f"aud_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        AUDIO_CACHE[audio_id] = pcm_bytes
        # Evict oldest items if cache exceeds 100 entries
        if len(AUDIO_CACHE) > 100:
            oldest_key = next(iter(AUDIO_CACHE))
            AUDIO_CACHE.pop(oldest_key, None)
        return audio_id

    @staticmethod
    def get_cached_audio(audio_id: str) -> Optional[bytes]:
        """Retrieves cached audio bytes by audio_id."""
        # Clean audio_id in case .wav or .mp3 extension was appended
        clean_id = audio_id.replace(".wav", "").replace(".mp3", "")
        return AUDIO_CACHE.get(clean_id) or AUDIO_CACHE.get(audio_id)

AUDIO_CACHE: Dict[str, bytes] = {}
