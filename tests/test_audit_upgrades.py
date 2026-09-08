import pytest
import asyncio
import sys, os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend_fastapi")))

from app.main import app
from app.database import SessionLocal, init_db
from app.models import models
from app.services.mandi_service import MandiService
from app.services.sarvam_service import SarvamService
from app.services.ai_voice_service import AIVoiceService
from app.services.recommendation_service import RecommendationEngine
from app.services.logistics_service import LogisticsService
from app.services.sms_service import SMSService

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    init_db()
    session = SessionLocal()
    yield session
    session.close()


def test_agmarknet_sync_and_kg_conversion(db):
    """Test Agmarknet APMC mandi price sync, ₹/Quintal to ₹/kg conversion, and DB persistence."""
    result = asyncio.run(MandiService.sync_agmarknet_prices(api_key=None, db=db))
    assert result["success"] is True
    assert result["records_updated"] > 0

    # Check that prices are stored in DB with source 'Agmarknet' or 'APMC'
    rec = MandiService.get_crop_price("Tomato", db)
    assert rec is not None
    assert "Agmarknet" in rec["source"] or "APMC" in rec["source"]
    assert rec["modal_price"] > 0
    # Mandi modal price in ₹/kg should be in realistic range (10 - 100), not quintal (1000 - 10000)
    assert rec["modal_price"] < 200

    # Test API endpoints
    sync_resp = client.post("/mandi/sync-agmarknet")
    assert sync_resp.status_code == 200
    assert sync_resp.json()["success"] is True

    crop_resp = client.get("/mandi/crops/Tomato")
    assert crop_resp.status_code == 200
    crop_data = crop_resp.json()
    assert crop_data["crop"] == "Tomato"


def test_voice_audio_streaming_and_caching():
    """Test Sarvam Bulbul TTS audio caching and the /voice/audio/{audio_id} streaming endpoint."""
    dummy_wav = b"RIFF____WAVEfmt " + b"\x00" * 30
    audio_id = SarvamService.cache_audio(dummy_wav)
    assert audio_id is not None
    assert SarvamService.get_cached_audio(audio_id) == dummy_wav

    # Test HTTP endpoint
    res = client.get(f"/voice/audio/{audio_id}")
    assert res.status_code == 200
    assert res.headers["content-type"].startswith("audio/wav")
    assert res.content == dummy_wav

    # Test 404 for unknown audio
    not_found = client.get("/voice/audio/non_existent_audio_id_9999")
    assert not_found.status_code == 404


def test_mandatory_farmer_confirmation_flow_yes(db):
    """Test Step 4 Confirmation: When farmer confirms with 'Haan'/'Yes', listing is created and is_final=True."""
    session_data = {
        "crop_name": "Tomato",
        "quantity_kg": 300,
        "village": "Murthal",
        "district": "Sonipat",
        "state": "Haryana",
        "expected_price": 28.0
    }

    # Step 4 verification confirmation
    res = AIVoiceService.process_voice_step(
        step=4,
        user_speech="Haan ji, bilkul theek hai, confirm kardo",
        phone="+919876543210",
        session_data=session_data,
        db=db
    )

    assert res["is_final"] is True
    assert res["confirmation_state"] == "CONFIRMED"
    assert "listing darj ho gaya hai" in res["ai_speech"]
    assert res.get("created_listing_id") is not None

    # Verify listing in database
    listing = db.query(models.ListingModel).filter(
        models.ListingModel.id == res["created_listing_id"]
    ).first()
    assert listing is not None
    assert listing.crop_name == "Tomato"
    assert listing.quantity_kg == 300


def test_mandatory_farmer_confirmation_flow_no_correction(db):
    """Test Step 4 Confirmation: When farmer says 'Nahi'/'Galat', system asks for correction (Step 5)."""
    session_data = {
        "crop_name": "Tomato",
        "quantity_kg": 300,
        "village": "Murthal",
        "district": "Sonipat",
        "state": "Haryana",
        "expected_price": 28.0
    }

    # Step 4: Farmer rejects
    res = AIVoiceService.process_voice_step(
        step=4,
        user_speech="Nahi, quantity galat hai",
        phone="+919876543210",
        session_data=session_data,
        db=db
    )

    assert res["is_final"] is False
    assert res["step"] == 5
    assert res["confirmation_state"] == "CORRECTION"
    assert "badalna chahte hain" in res["ai_speech"]

    # Step 5: Farmer gives correction
    res_corr = AIVoiceService.process_voice_step(
        step=5,
        user_speech="Mere paas 500 kilo hai",
        phone="+919876543210",
        session_data=res["session_data"],
        db=db
    )

    assert res_corr["is_final"] is False
    assert res_corr["step"] == 4
    assert res_corr["session_data"]["quantity_kg"] == 500
    assert "500" in res_corr["ai_speech"]


def test_recommendation_reserve_price_protection(db):
    """Test that Buyer Recommendation strictly never recommends buyers offering below the farmer's minimum reserve price."""
    listing = db.query(models.ListingModel).filter(models.ListingModel.crop_name == "Tomato").first()
    assert listing is not None

    # Set farmer reserve price to 26.30/kg
    # Available offers in seeded demo: FreshMart=26.50, BigBasket=26.20, Azadpur=25.80
    listing.farmer_min_price = 26.30
    db.commit()

    result = RecommendationEngine.rank_buyers_for_listing(listing, db)
    recs = result["recommendations"]

    assert len(recs) > 0
    for rec in recs:
        assert rec["offered_price_per_kg"] >= listing.farmer_min_price

    # Reset for other tests
    listing.farmer_min_price = 23.50
    db.commit()


def test_logistics_route_matching_and_pitch(db):
    """Test logistics route matching and spoken Hindi pitch generation."""
    pitch_data = LogisticsService.get_top_logistics_pitch(
        village="Murthal",
        district="Sonipat",
        destination="Azadpur Mandi",
        quantity_kg=300,
        db=db
    )

    assert pitch_data is not None
    assert "best_truck" in pitch_data
    assert "spoken_pitch" in pitch_data
    assert "truck ja raha hai" in pitch_data["spoken_pitch"]
    assert "transport" in pitch_data["spoken_pitch"]


def test_enriched_sms_deal_offer_payload(db):
    """Test that enriched SMS offer payload contains all required fields (Buyer, Crop, Qty, Price, Pickup, Truck, Deal ID, Reply YES/NO)."""
    log = SMSService.send_deal_offer_sms(
        phone="+919876543210",
        buyer_name="Agro Fresh Delhi",
        crop="Tomato",
        quantity_kg=300.0,
        price_per_kg=28.5,
        pickup_date="Kal Subah 7:00 AM",
        pickup_location="Murthal, Sonipat",
        truck_info="HR-10-A-4421 (Pooled - Azadpur)",
        deal_id="DEAL-7890",
        db=db
    )

    assert log.status == "DELIVERED"
    body = log.message

    assert "Naya Sauda Offer" in body
    assert "Agro Fresh Delhi" in body
    assert "Tomato" in body
    assert "300" in body
    assert "28.5" in body
    assert "Murthal" in body
    assert "HR-10-A-4421" in body
    assert "DEAL-7890" in body
    assert "YES" in body
