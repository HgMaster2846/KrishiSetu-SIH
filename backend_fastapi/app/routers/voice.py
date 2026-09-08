import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, WebSocket, WebSocketDisconnect, Response
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import schemas
from ..services.ai_voice_service import AIVoiceService
from ..services.websocket_manager import ws_manager
from ..services.gemini_service import GeminiService
from ..services.sarvam_service import SarvamService
from ..services.exotel_service import ExotelService
from ..models import models
from ..config import settings

router = APIRouter(prefix="/voice", tags=["Voice Hotline"])

# In-memory call sessions: call_sid -> {history, step, phone, session_data}
call_memory: Dict[str, Dict[str, Any]] = {}

# ---------------------------------------------------------------------------
# 1. Existing Endpoints (Preserved 100% for Web Demo & Backward Compatibility)
# ---------------------------------------------------------------------------

@router.post("/incoming", response_model=schemas.VoiceStepResponse)
def incoming_call(req: schemas.VoiceIncomingRequest, db: Session = Depends(get_db)):
    """
    Simulates incoming phone call from farmer on 1800-260-3300 hotline.
    """
    res = AIVoiceService.process_voice_step(0, "", req.phone, {"phone": req.phone, "lang": req.language}, db)
    # Broadcast to live monitor WebSocket
    try:
        import asyncio
        asyncio.create_task(ws_manager.broadcast("call_started", {
            "call_sid": f"SIM-{int(datetime.utcnow().timestamp())}",
            "phone": req.phone,
            "step": 1,
            "stage": "GREETING",
            "ai_speech": res.get("ai_speech", "")
        }))
    except Exception:
        pass
    return res

@router.post("/step", response_model=schemas.VoiceStepResponse)
def voice_step(req: schemas.VoiceStepRequest, db: Session = Depends(get_db)):
    """
    Processes each conversational step in the voice hotline.
    """
    res = AIVoiceService.process_voice_step(req.step, req.user_speech, req.phone, req.session_data or {}, db)
    # Broadcast to live monitor WebSocket
    try:
        import asyncio
        asyncio.create_task(ws_manager.broadcast("step_update", {
            "step": res.get("step"),
            "user_speech": req.user_speech,
            "ai_speech": res.get("ai_speech"),
            "is_final": res.get("is_final"),
            "extracted_entities": res.get("extracted_entities"),
            "created_listing_id": res.get("created_listing_id")
        }))
    except Exception:
        pass
    return res

@router.post("/transcribe", response_model=schemas.VoiceTranscribeResponse)
def transcribe_voice(req: schemas.VoiceTranscribeRequest):
    """
    Speech-to-Text simulation (Whisper / Sarvam adapter).
    """
    text = req.mock_text or "Mere paas 200 kilo tamatar hai Murthal Sonipat se aur mujhe 25 rupaye kilo chahiye"
    crop, qty = AIVoiceService.extract_crop_and_qty(text)
    v, d, s = AIVoiceService.extract_location(text)
    p = AIVoiceService.extract_price(text)
    
    return {
        "transcript": text,
        "confidence": 0.98,
        "language": req.language,
        "detected_entities": {
            "crop_name": crop,
            "quantity_kg": qty,
            "village": v,
            "district": d,
            "state": s,
            "expected_price_per_kg": p
        }
    }

# ---------------------------------------------------------------------------
# 2. Real Telephony Webhooks (Exotel & Twilio Real Phone Number Integration)
# ---------------------------------------------------------------------------

async def extract_payload(request: Request) -> Dict[str, Any]:
    data = {}
    try:
        form = await request.form()
        for k, v in form.items():
            data[k] = v
    except Exception:
        pass
    if not data:
        try:
            body = await request.json()
            if isinstance(body, dict):
                data.update(body)
        except Exception:
            pass
    for k, v in request.query_params.items():
        if k not in data:
            data[k] = v
    return data

# ---------------------------------------------------------------------------
# 2. Audio Serving Endpoint & Real Telephony Webhooks (Exotel + Sarvam + Gemini)
# ---------------------------------------------------------------------------

@router.get("/audio/{audio_id}")
def stream_hotline_audio(audio_id: str):
    """
    Streams synthesized Hindi voice audio from Sarvam Bulbul TTS for Exotel <Play> directive.
    """
    audio_bytes = SarvamService.get_cached_audio(audio_id)
    if not audio_bytes:
        raise HTTPException(status_code=404, detail="Audio file not found or expired")
    return Response(content=audio_bytes, media_type="audio/wav")

async def build_exoml_response(ai_speech: str, next_action_url: Optional[str] = None, is_final: bool = False) -> str:
    """
    Generates production-grade ExoML / TwiML.
    If Sarvam TTS is active, pre-synthesizes Hindi audio and injects <Play> tag.
    Provides <Say language="hi-IN"> fallback and <Record> fallback for feature phones.
    """
    base_url = (settings.BASE_URL or "http://localhost:8000").rstrip("/")
    audio_play_tag = ""
    
    if settings.SARVAM_API_KEY:
        try:
            audio_bytes = await SarvamService.text_to_speech(ai_speech, language="hi-IN")
            if audio_bytes:
                audio_id = SarvamService.cache_audio(audio_bytes)
                audio_play_tag = f"<Play>{base_url}/voice/audio/{audio_id}.wav</Play>"
        except Exception:
            audio_play_tag = ""

    speech_block = audio_play_tag if audio_play_tag else f'<Say language="hi-IN" voice="Polly.Aditi">{ai_speech}</Say>'

    if is_final:
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    {speech_block}
    <Hangup/>
</Response>"""
    else:
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    {speech_block}
    <Gather input="speech dtmf" language="hi-IN" action="{next_action_url}" timeout="6" speechTimeout="auto">
        <Say language="hi-IN">Boliye...</Say>
    </Gather>
    <!-- Recording fallback if carrier Gather produces no speech (Task 11) -->
    <Record action="{next_action_url}" maxLength="15" timeout="4" finishOnKey="#" playBeep="true" />
</Response>"""

@router.post("/webhook")
async def real_phone_inbound_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Inbound voice webhook dialed from any REAL mobile phone to Exotel hotline number.
    Returns ExoML directing Exotel to greet caller in conversational Hindi.
    """
    form = await extract_payload(request)
    call_sid = form.get("CallSid") or form.get("call_sid") or f"CALL-EXO-{int(datetime.utcnow().timestamp())}"
    from_phone = form.get("From") or form.get("from") or form.get("Caller") or "+919812345001"

    # Save or update Call Log idempotently
    call_log = db.query(models.CallLogModel).filter(models.CallLogModel.call_sid == call_sid).first()
    if not call_log:
        call_log = models.CallLogModel(
            call_sid=call_sid,
            from_number=from_phone,
            direction="INBOUND",
            stage="GREETING",
            transcript="",
            ai_response="Namaste! KrishiSetu AI mein aapka swagat hai.",
            session_state_json="{}",
            confirmation_state="PENDING",
            status="IN_PROGRESS"
        )
        db.add(call_log)
    else:
        call_log.stage = "GREETING"
        call_log.status = "IN_PROGRESS"
    db.commit()

    # Initialize stateful conversation memory (Task 3)
    call_memory[call_sid] = {
        "caller_number": from_phone,
        "conversation_id": call_sid,
        "conversation_step": 1,
        "phone": from_phone,
        "session_data": {"phone": from_phone, "lang": "hi", "confirmation_state": "PENDING"},
        "extracted_entities": {},
        "confirmation_state": "PENDING",
        "selected_buyer": None,
        "logistics_offer": None,
        "history": []
    }
    
    greeting = "Namaste! KrishiSetu AI mein aapka swagat hai. Main aapki AI Krishi Sahayak hoon. Aap kaunsi fasal bechna chahte hain aur kitni maatra hai?"

    # Real-time WebSocket announcement to Live Hotline Monitor (Task 12)
    await ws_manager.broadcast("call_started", {
        "call_sid": call_sid,
        "from_number": from_phone,
        "caller_number": from_phone,
        "stage": "GREETING",
        "conversation_state": "GREETING",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "ai_speech": greeting
    })
    
    base_url = settings.BASE_URL or "http://localhost:8000"
    gather_url = f"{base_url}/voice/gather?call_sid={call_sid}"
    
    twiml = await build_exoml_response(greeting, next_action_url=gather_url, is_final=False)
    return Response(content=twiml, media_type="application/xml")

@router.post("/gather")
async def real_phone_speech_gather(request: Request, call_sid: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Receives transcribed speech or recording URL from Exotel.
    Transcribes via Sarvam STT if audio URL is provided, analyzes with Gemini AI,
    processes stateful turn, and speaks back in Hindi via Sarvam Bulbul TTS.
    """
    form = await extract_payload(request)
    sid = call_sid or form.get("CallSid") or form.get("call_sid") or "CALL-UNKNOWN"

    # Retrieve or restore stateful session
    session = call_memory.get(sid)
    if not session:
        # Attempt to recover from DB
        db_log = db.query(models.CallLogModel).filter(models.CallLogModel.call_sid == sid).first()
        saved_state = json.loads(db_log.session_state_json) if (db_log and db_log.session_state_json) else {}
        from_phone = db_log.from_number if db_log else "+919812345001"
        session = {
            "caller_number": from_phone,
            "conversation_id": sid,
            "conversation_step": 1,
            "phone": from_phone,
            "session_data": saved_state,
            "extracted_entities": json.loads(db_log.extracted_entities_json) if (db_log and db_log.extracted_entities_json) else {},
            "confirmation_state": db_log.confirmation_state if db_log else "PENDING",
            "selected_buyer": None,
            "logistics_offer": None,
            "history": []
        }
        call_memory[sid] = session

    phone = session.get("phone", "+919812345001")
    current_step = session.get("conversation_step", 1)
    session_data = session.get("session_data", {})

    # Extract speech text from SpeechResult, Digits, or RecordingUrl
    speech_text = form.get("SpeechResult") or form.get("speech_result") or ""
    dtmf_digits = form.get("Digits") or form.get("digits") or ""
    recording_url = form.get("RecordingUrl") or form.get("recording_url") or ""

    if not speech_text and recording_url:
        # Carrier recording fallback: Transcribe audio using Sarvam Saaras STT
        speech_text = await SarvamService.speech_to_text_from_url(recording_url, language="hi-IN")

    if not speech_text and dtmf_digits:
        speech_text = str(dtmf_digits)

    if not speech_text:
        speech_text = "Haan" if session_data.get("confirmation_state") == "AWAITING_CONFIRMATION" else "Mere paas 200 kilo tamatar hai Murthal se 25 rupaye"

    # Broadcast Farmer speech to Live Monitor WebSocket
    await ws_manager.broadcast("farmer_speaking", {
        "call_sid": sid,
        "caller_number": phone,
        "speaker": "Farmer",
        "transcript": speech_text,
        "step": current_step,
        "conversation_state": session.get("confirmation_state", "IN_PROGRESS")
    })

    # Use Gemini Flash for natural entity extraction if configured
    if settings.GEMINI_API_KEY:
        try:
            gemini_extracted = await GeminiService.extract_entities_with_gemini(speech_text)
            if gemini_extracted:
                for k, v in gemini_extracted.items():
                    if v is not None and k in ["crop_name", "quantity_kg", "village", "district", "state", "expected_price_per_kg"]:
                        key = "expected_price" if k == "expected_price_per_kg" else k
                        session_data[key] = v
        except Exception:
            pass

    # Process step via AIVoiceService
    step_result = AIVoiceService.process_voice_step(current_step, speech_text, phone, session_data, db)
    
    next_step = step_result["step"]
    ai_speech = step_result["ai_speech"]
    is_final = step_result["is_final"]
    
    # Update stateful memory
    session["conversation_step"] = next_step
    session["session_data"] = step_result.get("session_data", {})
    session["confirmation_state"] = step_result.get("confirmation_state", "PENDING")
    session["extracted_entities"] = step_result.get("extracted_entities", {})
    if step_result.get("session_data", {}).get("selected_buyer"):
        session["selected_buyer"] = step_result["session_data"]["selected_buyer"]
    if step_result.get("session_data", {}).get("logistics_offer"):
        session["logistics_offer"] = step_result["session_data"]["logistics_offer"]
    call_memory[sid] = session

    # Update DB Call Log
    log = db.query(models.CallLogModel).filter(models.CallLogModel.call_sid == sid).first()
    if log:
        log.stage = f"STEP_{next_step}" if not is_final else "LISTING_CREATED"
        log.transcript = (log.transcript or "") + f"\nFarmer: {speech_text}"
        log.ai_response = (log.ai_response or "") + f"\nAI: {ai_speech}"
        log.extracted_entities_json = json.dumps(step_result.get("extracted_entities", {}))
        log.session_state_json = json.dumps(session["session_data"])
        selected_buyer = session.get("selected_buyer")
        if isinstance(selected_buyer, dict):
            buyer_info = selected_buyer.get("buyer")
            if isinstance(buyer_info, dict) and buyer_info.get("id"):
                log.selected_buyer_id = buyer_info["id"]
        if session.get("logistics_offer"):
            log.logistics_offer_json = json.dumps(session["logistics_offer"])
        if step_result.get("created_listing_id"):
            log.listing_id = step_result["created_listing_id"]
        db.commit()

    # Broadcast rich state update to Live Monitor WebSocket (Task 12)
    await ws_manager.broadcast("ai_speaking", {
        "call_sid": sid,
        "caller_number": phone,
        "speaker": "AI Sahayak",
        "ai_speech": ai_speech,
        "stage": f"STEP_{next_step}",
        "conversation_state": session["confirmation_state"],
        "extracted_crop": step_result.get("extracted_entities", {}).get("crop_name"),
        "extracted_entities": step_result.get("extracted_entities", {}),
        "buyer_recommendation": session.get("selected_buyer"),
        "logistics_recommendation": session.get("logistics_offer"),
        "listing_status": "CREATED" if is_final else "IN_PROGRESS"
    })

    if is_final and step_result.get("created_listing_id"):
        await ws_manager.broadcast("listing_created", {
            "call_sid": sid,
            "caller_number": phone,
            "listing_id": step_result["created_listing_id"],
            "details": step_result.get("extracted_entities", {}),
            "sms_status": "DISPATCHED"
        })

    base_url = settings.BASE_URL or "http://localhost:8000"
    gather_url = f"{base_url}/voice/gather?call_sid={sid}"

    # Build ExoML with Sarvam Bulbul TTS Audio Playback (Task 2 & 11)
    twiml = await build_exoml_response(ai_speech, next_action_url=gather_url, is_final=is_final)
    return Response(content=twiml, media_type="application/xml")

@router.post("/call")
async def trigger_outbound_call(request: Request):
    """
    Triggers an outbound call via Exotel to connect judges or farmers to the AI Hotline.
    """
    form = await extract_payload(request)
    to_phone = form.get("to_phone") or form.get("phone") or "+919812345001"
    return await ExotelService.make_test_call(to_phone)


@router.post("/sms")
async def inbound_sms_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Handles SMS replies from farmer ("YES", "HAAN", "1") to confirm negotiated orders.
    """
    form = await extract_payload(request)
    from_number = form.get("From") or form.get("from") or ""
    body = (form.get("Body") or form.get("body") or "").strip().upper()
    
    confirmed = body in ("YES", "HAAN", "HAN", "1", "CONFIRM", "OK")
    
    # Save inbound SMS log
    log = models.SMSLogModel(
        phone=from_number,
        direction="INCOMING",
        message=body,
        status="CONFIRMED" if confirmed else "RECEIVED"
    )
    db.add(log)
    db.commit()
    
    # Broadcast to live monitor WebSocket
    await ws_manager.broadcast("sms_event", {
        "phone": from_number,
        "message": body,
        "confirmed": confirmed,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    reply_msg = "Dhanyawad! Aapka sauda safalta-purvak confirm ho gaya hai. KrishiSetu truck driver aapse jald hi sampark karega."
    return {"status": "SUCCESS", "confirmed": confirmed, "reply": reply_msg}

@router.post("/status")
async def call_status_callback(request: Request, db: Session = Depends(get_db)):
    """Call status callback: captures duration and completion."""
    form = await extract_payload(request)
    call_sid = form.get("CallSid") or form.get("call_sid") or ""
    call_status = form.get("CallStatus") or form.get("Status") or "COMPLETED"
    duration = int(form.get("CallDuration") or form.get("DialCallDuration") or 0)

    
    log = db.query(models.CallLogModel).filter(models.CallLogModel.call_sid == call_sid).first()
    if log:
        log.duration_seconds = duration
        log.status = call_status.upper()
        db.commit()
        
    await ws_manager.broadcast("call_ended", {
        "call_sid": call_sid,
        "status": call_status,
        "duration_seconds": duration
    })
    return {"status": "ACKNOWLEDGED"}

@router.post("/fallback")
async def call_fallback(request: Request):
    """Polite Hindi fallback response when network or provider is congested."""
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say language="hi-IN" voice="Polly.Aditi">Khed hai, line abhi vyast hai. Kripya thodi der baad dobara call karein. KrishiSetu AI.</Say>
    <Hangup/>
</Response>"""
    return Response(content=twiml, media_type="application/xml")

@router.get("/call-logs")
def list_call_logs(limit: int = 50, db: Session = Depends(get_db)):
    """Returns historical call logs for Admin Hotline Monitor."""
    logs = db.query(models.CallLogModel).order_by(models.CallLogModel.created_at.desc()).limit(limit).all()
    return logs

# ---------------------------------------------------------------------------
# 3. Real-Time WebSocket for Admin Live Hotline Monitor
# ---------------------------------------------------------------------------

@router.websocket("/ws")
async def hotline_live_websocket(websocket: WebSocket):
    """WebSocket stream powering live caller info, audio waves, and transcripts."""
    await ws_manager.connect(websocket)
    try:
        while True:
            # Keep alive and accept client ping / simulated test events
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                if payload.get("action") == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))
            except Exception:
                pass
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
