import pytest
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend_fastapi")))

from app.database import SessionLocal, init_db
from app.models import models
from app.services import RecommendationEngine, NegotiationService, LogisticsService, AIVoiceService, FraudDetectionService
from app.routers.listings import get_all_listings
from app.routers.mandi import get_all_mandi_prices
from app.routers.dashboard import get_admin_dashboard
from app.schemas import schemas

@pytest.fixture(scope="module")
def db():
    init_db()
    session = SessionLocal()
    yield session
    session.close()

def test_voice_nlp_extraction():
    # Test Crop & Quantity
    crop, qty = AIVoiceService.extract_crop_and_qty("Mere paas 200 kilo tamatar hai")
    assert crop == "Tomato"
    assert qty == 200.0

    crop2, qty2 = AIVoiceService.extract_crop_and_qty("5 quintal pyaz bechna hai")
    assert crop2 == "Onion"
    assert qty2 == 500.0

    # Test Location
    v, d, s = AIVoiceService.extract_location("Murthal, Sonipat")
    assert "Murthal" in v
    assert "Sonipat" in d
    assert s == "Haryana"

    # Test Price
    price = AIVoiceService.extract_price("25 rupaye kilo")
    assert price == 25.0

def test_buyer_recommendation_algorithm(db):
    listing = db.query(models.ListingModel).filter(models.ListingModel.crop_name == "Tomato").first()
    assert listing is not None
    
    result = RecommendationEngine.rank_buyers_for_listing(listing, db)
    recs = result["recommendations"]
    assert len(recs) == 3
    assert recs[0]["overall_score"] >= recs[1]["overall_score"] >= recs[2]["overall_score"]
    assert recs[0]["is_top_pick"] is True
    assert "overall_score" in recs[0]
    assert "mandi_price_35" in recs[0]["score_breakdown"]

def test_negotiation_reserve_price_protection(db):
    listing = db.query(models.ListingModel).filter(models.ListingModel.id == "LIST-001").first()
    assert listing is not None

    # Buyer offers low price (?20/kg) below farmer minimum (?23.5)
    res = NegotiationService.start_negotiation(listing.id, "BUY-001", 20.0, db)
    assert res["status"] == "AI_COUNTERED"
    assert res["current_ai_counter"] >= listing.farmer_min_price
    assert "below farmer's reserve price" in res["ai_reasoning"]

def test_pooled_logistics_matching(db):
    routes = LogisticsService.find_pooled_trucks("Murthal", "Sonipat", "Azadpur Mandi, Delhi", 200.0, db)
    assert len(routes) > 0
    top_truck = routes[0]
    assert top_truck["farmer_savings"] > 0
    assert top_truck["shared_cost_total"] < top_truck["solo_cost_total"]

def test_fraud_detection(db):
    buyer_suspicious = db.query(models.BuyerModel).filter(models.BuyerModel.id == "BUY-019").first()
    if buyer_suspicious:
        report = FraudDetectionService.evaluate_buyer(buyer_suspicious, 15.0, 26.5)
        assert report["risk_level"] == "HIGH"
        assert len(report["flags"]) > 0

def test_api_endpoint_handlers(db):
    listings = get_all_listings(limit=10, db=db)
    assert len(listings) > 0

    mandi_prices = get_all_mandi_prices(db=db)
    assert len(mandi_prices) > 0

    admin_dash = get_admin_dashboard(db=db)
    assert admin_dash["total_farmers"] >= 20
    assert admin_dash["total_buyers"] >= 20
    assert admin_dash["active_listings"] >= 10
