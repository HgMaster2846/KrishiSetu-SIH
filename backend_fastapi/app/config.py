import os
from typing import Optional

# Try loading .env file from current or root directory
try:
    from dotenv import load_dotenv
    _current_dir = os.path.dirname(os.path.abspath(__file__))
    _env_candidates = [
        os.path.join(_current_dir, "..", "..", ".env"),
        os.path.join(_current_dir, "..", ".env"),
        os.path.join(os.getcwd(), ".env"),
        os.path.join(os.getcwd(), "backend_fastapi", ".env")
    ]
    for _p in _env_candidates:
        if os.path.exists(_p):
            load_dotenv(_p)
            break
except Exception:
    pass

class Settings:
    PROJECT_NAME: str = 'KrishiSetu AI'
    VERSION: str = '1.0.0'
    API_PREFIX: str = ''
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///./krishisetu.db')
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'krishisetu-sih2026-supersecret-jwt-key')
    DEMO_MODE: bool = os.getenv('DEMO_MODE', 'true').lower() in ('true', '1', 'yes')
    HOTLINE_NUMBER: str = os.getenv('HOTLINE_NUMBER', '9513886363')
    
    # Exotel Primary Telephony
    EXOTEL_API_KEY: Optional[str] = os.getenv('EXOTEL_API_KEY', '')
    EXOTEL_API_SECRET: Optional[str] = os.getenv('EXOTEL_API_SECRET', '')
    EXOTEL_ACCOUNT_SID: Optional[str] = os.getenv('EXOTEL_ACCOUNT_SID', '')
    EXOTEL_PHONE_NUMBER: Optional[str] = os.getenv('EXOTEL_PHONE_NUMBER', '9513886363')
    EXOTEL_API_DOMAIN: str = os.getenv('EXOTEL_API_DOMAIN', 'api.exotel.com')
    
    # Sarvam AI Voice
    SARVAM_API_KEY: Optional[str] = os.getenv('SARVAM_API_KEY', '')
    
    # Google Gemini
    GEMINI_API_KEY: Optional[str] = os.getenv('GEMINI_API_KEY', '')
    
    # Agmarknet / Open Government Data Mandi Intelligence
    AGMARKNET_API_KEY: Optional[str] = os.getenv('AGMARKNET_API_KEY', '')
    DATA_GOV_IN_API_KEY: Optional[str] = os.getenv('DATA_GOV_IN_API_KEY', '')
    
    # SMS Gateway Provider ('exotel', 'twilio', 'mock')
    SMS_PROVIDER: str = os.getenv('SMS_PROVIDER', 'mock')
    
    # Twilio Fallback
    TWILIO_ACCOUNT_SID: Optional[str] = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN: Optional[str] = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_PHONE_NUMBER: Optional[str] = os.getenv('TWILIO_PHONE_NUMBER', '')
    
    # Public Base URL for Webhooks (e.g. ngrok or deployment URL)
    BASE_URL: str = os.getenv('BASE_URL', 'http://localhost:8000')

    @classmethod
    def update_from_dict(cls, data: dict):
        for k, v in data.items():
            upper_k = k.upper()
            if hasattr(cls, upper_k) and v is not None:
                setattr(cls, upper_k, v)

settings = Settings()
