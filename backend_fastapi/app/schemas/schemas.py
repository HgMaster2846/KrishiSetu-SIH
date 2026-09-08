from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# Voice Hotline Schemas
class VoiceIncomingRequest(BaseModel):
    phone: str = '+919812345001'
    language: str = 'hi'

class VoiceStepRequest(BaseModel):
    phone: str = '+919812345001'
    step: int = 0
    user_speech: str = ''
    session_data: Optional[Dict[str, Any]] = None

class VoiceStepResponse(BaseModel):
    step: int
    ai_speech: str
    audio_cue: Optional[str] = None
    is_final: bool = False
    extracted_entities: Optional[Dict[str, Any]] = None
    created_listing_id: Optional[str] = None
    session_data: Dict[str, Any]

class VoiceTranscribeRequest(BaseModel):
    mock_text: Optional[str] = None
    language: str = 'hi'

class VoiceTranscribeResponse(BaseModel):
    transcript: str
    confidence: float = 0.98
    language: str = 'hi'
    detected_entities: Dict[str, Any]

# Listing Schemas
class ListingCreate(BaseModel):
    farmer_id: Optional[str] = 'FARM-001'
    farmer_name: Optional[str] = 'Rameshwar Singh'
    farmer_phone: Optional[str] = '+919812345001'
    crop_name: str
    category: Optional[str] = 'Vegetable'
    quantity_kg: float
    expected_price_per_kg: float
    farmer_min_price: Optional[float] = None
    village: str
    district: str
    state: str
    harvest_date: Optional[str] = '2026-09-06'
    quality_grade: Optional[str] = 'Grade A'
    created_via: Optional[str] = 'AI_HOTLINE_VOICE'

class ListingResponse(BaseModel):
    id: str
    farmer_id: str
    farmer_name: str
    farmer_phone: str
    crop_name: str
    category: str
    quantity_kg: float
    expected_price_per_kg: float
    farmer_min_price: float
    current_best_offer: Optional[float] = None
    village: str
    district: str
    state: str
    harvest_date: str
    description: Optional[str] = ''
    quality_grade: str
    status: str
    ai_mandi_benchmark: float
    recommended_buyer_id: Optional[str] = None
    created_via: str
    created_at: Optional[str] = ''

# Buyer Schemas
class BuyerResponse(BaseModel):
    id: str
    name: str
    company: str
    contact_person: str
    phone: str
    email: str
    district: str
    state: str
    distance_km: float
    trust_score: int
    verified: bool
    total_deals: int
    fraud_risk: str
    payment_terms: str

class BuyerRecommendationItem(BaseModel):
    buyer: BuyerResponse
    overall_score: float
    offered_price_per_kg: float
    transport_cost_per_kg: float
    net_farmer_profit_per_kg: float
    total_estimated_payout: float
    is_top_pick: bool
    trust_badge: str
    reasoning: str
    score_breakdown: Dict[str, float]

class BuyerRecommendationResponse(BaseModel):
    crop_name: str
    quantity_kg: float
    mandi_benchmark_price: float
    recommendations: List[BuyerRecommendationItem]

# Negotiation Schemas
class NegotiationStartRequest(BaseModel):
    listing_id: str
    buyer_id: str
    buyer_offer_per_kg: float

class NegotiationRespondRequest(BaseModel):
    negotiation_id: str
    buyer_counter_offer: float
    action: str = 'COUNTER' # 'ACCEPT', 'COUNTER', 'REJECT'

class OfferHistoryItem(BaseModel):
    sender: str
    amount_per_kg: float
    message: str
    timestamp: str

class NegotiationResponse(BaseModel):
    id: str
    listing_id: str
    buyer_id: str
    buyer_name: Optional[str] = ''
    crop_name: Optional[str] = ''
    quantity_kg: Optional[float] = 0.0
    farmer_min_price: float
    current_buyer_offer: float
    current_ai_counter: Optional[float] = None
    status: str
    ai_reasoning: str
    offers: List[OfferHistoryItem] = []

# Mandi Schemas
class MandiMarketItem(BaseModel):
    name: str
    modal: float
    min: float
    max: float
    arrival_tonnes: float

class MandiPriceResponse(BaseModel):
    crop: str
    category: str
    unit: str = '₹/kg'
    modal_price: float
    min_price: float
    max_price: float
    trend: str
    best_mandi: str
    mandis: List[MandiMarketItem] = []
    history_7d: List[float] = []

# Logistics Schemas
class TruckRouteResponse(BaseModel):
    id: str
    driver_name: str
    driver_phone: str
    truck_number: str
    truck_type: str
    origin: str
    destination: str
    current_location: str
    total_capacity_kg: float
    available_capacity_kg: float
    scheduled_departure: str
    estimated_arrival: str
    waypoints: List[str]
    pooled_rate_per_kg: float
    solo_rate_per_kg: float
    status: str
    shared_cost_total: float
    solo_cost_total: float
    farmer_savings: float
    is_recommended: bool

# Transaction Schemas
class TransactionConfirmRequest(BaseModel):
    listing_id: str
    buyer_id: str
    truck_route_id: Optional[str] = 'TRUCK-001'
    agreed_price_per_kg: float
    quantity_kg: float

class TransactionResponse(BaseModel):
    id: str
    listing_id: str
    buyer_id: str
    farmer_id: str
    truck_route_id: Optional[str] = None
    quantity_kg: float
    agreed_price_per_kg: float
    total_amount: float
    logistics_shared_cost: float
    logistics_solo_cost: float
    farmer_savings: float
    escrow_status: str
    status: str
    otp_code: str
    otp_verified: bool
    pickup_time: str
    created_at: str

class OTPVerifyRequest(BaseModel):
    transaction_id: str
    otp_code: str

class OTPVerifyResponse(BaseModel):
    success: bool
    message: str
    transaction_status: str
    escrow_status: str

# SMS Schemas
class SMSSendRequest(BaseModel):
    phone: str
    message: str

class SMSReplyRequest(BaseModel):
    phone: str = '+919812345001'
    reply_text: str # 'YES', '1', 'NO', '2'

class SMSLogResponse(BaseModel):
    id: int
    phone: str
    direction: str
    message: str
    status: str
    timestamp: str

# Dashboard Schemas
class AdminDashboardResponse(BaseModel):
    total_farmers: int
    total_buyers: int
    active_listings: int
    active_negotiations: int
    completed_transactions: int
    total_trade_volume_inr: float
    total_logistics_saved_inr: float
    fraud_alerts: List[Dict[str, Any]]
    recent_transactions: List[Dict[str, Any]]
    recent_listings: List[Dict[str, Any]]

class BuyerDashboardResponse(BaseModel):
    buyer_id: str
    buyer_name: str
    recommended_listings: List[ListingResponse]
    active_negotiations_count: int
    deals_in_progress: int
