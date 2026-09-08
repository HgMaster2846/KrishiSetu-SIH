import pytest
import sys, os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend_fastapi")))

from app.main import app
from app.database import SessionLocal, init_db
from app.models import models

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    init_db()
    session = SessionLocal()
    yield session
    session.close()

def test_setup_status_endpoint():
    res = client.get("/setup/status")
    assert res.status_code == 200
    data = res.json()
    assert "integrations" in data
    assert "hotline_number" in data
    assert data["integrations"]["database_connected"] is True

def test_setup_save_and_verify():
    payload = {
        "exotel_api_key": "test_exo_key",
        "exotel_api_secret": "test_exo_secret",
        "exotel_account_sid": "test_exo_sid",
        "exotel_phone_number": "+91 1800-260-3300",
        "sms_provider": "mock",
        "demo_mode": True
    }
    save_res = client.post("/setup/save", json=payload)
    assert save_res.status_code == 200
    assert save_res.json()["success"] is True

    verify_res = client.post("/setup/verify", json=payload)
    assert verify_res.status_code == 200
    data = verify_res.json()
    assert "checklist" in data
    assert "database" in data["checklist"]
    assert data["checklist"]["database"]["valid"] is True

def test_diagnostics_checklist():
    res = client.get("/setup/diagnostics")
    assert res.status_code == 200
    data = res.json()
    assert data["overall_status"] == "ALL_SYSTEMS_OPERATIONAL"
    assert len(data["checklist"]) == 9
    names = [item["name"] for item in data["checklist"]]
    assert "Phone Number Connected" in names
    assert "Conversational AI Engine" in names
    assert "Pooled Logistics Engine" in names

def test_real_phone_voice_webhook():
    # Simulate an incoming phone call from Exotel carrier
    form_data = {
        "CallSid": "CALL-TEST-EXO-001",
        "From": "+919812345001"
    }
    res = client.post("/voice/webhook", data=form_data)
    assert res.status_code == 200
    assert "application/xml" in res.headers["content-type"]
    assert "Namaste" in res.text
    assert "<Gather" in res.text

def test_real_phone_speech_gather():
    # Simulate speech recognition callback from caller saying their crop and quantity
    form_data = {
        "CallSid": "CALL-TEST-EXO-001",
        "From": "+919812345001",
        "SpeechResult": "Mere paas 250 kilo tamatar hai Murthal Sonipat se"
    }
    res = client.post("/voice/gather", data=form_data)
    assert res.status_code == 200
    assert "application/xml" in res.headers["content-type"]
    assert "<Response>" in res.text

def test_inbound_sms_confirmation():
    # Farmer replies "HAAN" or "YES" to confirm deal
    form_data = {
        "From": "+919812345001",
        "Body": "HAAN"
    }
    res = client.post("/voice/sms", data=form_data)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "SUCCESS"
    assert data["confirmed"] is True

def test_one_click_deploy_endpoint():
    res = client.post("/setup/deploy?platform=railway")
    assert res.status_code == 200
    data = res.json()
    assert data["selected_platform"] == "railway"
    assert "webhook_url" in data
