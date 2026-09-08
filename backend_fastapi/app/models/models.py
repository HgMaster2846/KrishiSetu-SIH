from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey
from ..database import Base

class FarmerModel(Base):
    __tablename__ = 'farmers'
    id = Column(String(32), primary_key=True)
    name = Column(String(128), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    village = Column(String(128), nullable=False)
    district = Column(String(128), nullable=False)
    state = Column(String(128), nullable=False)
    language = Column(String(10), default='hi')
    land_size_acres = Column(Float, default=2.0)
    phone_type = Column(String(64), default='Feature Phone')
    kyc_verified = Column(Boolean, default=True)
    total_sales_kg = Column(Float, default=0.0)
    rating = Column(Float, default=4.8)
    created_at = Column(DateTime, default=datetime.utcnow)

class BuyerModel(Base):
    __tablename__ = 'buyers'
    id = Column(String(32), primary_key=True)
    name = Column(String(128), nullable=False)
    company = Column(String(256), nullable=False)
    contact_person = Column(String(128), default='')
    phone = Column(String(20), nullable=False)
    email = Column(String(128), nullable=False)
    district = Column(String(128), nullable=False)
    state = Column(String(128), nullable=False)
    distance_km = Column(Float, default=50.0)
    trust_score = Column(Integer, default=90)
    verified = Column(Boolean, default=True)
    total_deals = Column(Integer, default=0)
    fraud_risk = Column(String(16), default='LOW')
    payment_terms = Column(String(128), default='Instant Escrow')
    created_at = Column(DateTime, default=datetime.utcnow)

class ListingModel(Base):
    __tablename__ = 'listings'
    id = Column(String(32), primary_key=True)
    farmer_id = Column(String(32), ForeignKey('farmers.id'), nullable=False)
    farmer_name = Column(String(128), default='')
    farmer_phone = Column(String(20), default='')
    crop_name = Column(String(128), nullable=False)
    category = Column(String(64), default='Vegetable')
    quantity_kg = Column(Float, nullable=False)
    expected_price_per_kg = Column(Float, nullable=False)
    farmer_min_price = Column(Float, nullable=False)
    current_best_offer = Column(Float, nullable=True)
    village = Column(String(128), nullable=False)
    district = Column(String(128), nullable=False)
    state = Column(String(128), nullable=False)
    harvest_date = Column(String(32), default='2026-09-06')
    description = Column(Text, default='')
    quality_grade = Column(String(32), default='Grade A')
    status = Column(String(32), default='ACTIVE')
    ai_mandi_benchmark = Column(Float, default=25.8)
    recommended_buyer_id = Column(String(32), nullable=True)
    created_via = Column(String(32), default='AI_HOTLINE_VOICE')
    created_at = Column(String(64), default='')

class NegotiationModel(Base):
    __tablename__ = 'negotiations'
    id = Column(String(32), primary_key=True)
    listing_id = Column(String(32), ForeignKey('listings.id'), nullable=False)
    buyer_id = Column(String(32), ForeignKey('buyers.id'), nullable=False)
    farmer_min_price = Column(Float, nullable=False)
    current_buyer_offer = Column(Float, nullable=False)
    current_ai_counter = Column(Float, nullable=True)
    status = Column(String(32), default='PENDING')
    ai_reasoning = Column(Text, default='')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class OfferModel(Base):
    __tablename__ = 'offers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    negotiation_id = Column(String(32), ForeignKey('negotiations.id'), nullable=False)
    sender = Column(String(32), nullable=False)
    amount_per_kg = Column(Float, nullable=False)
    message = Column(Text, default='')
    created_at = Column(DateTime, default=datetime.utcnow)

class TruckRouteModel(Base):
    __tablename__ = 'truck_routes'
    id = Column(String(32), primary_key=True)
    driver_name = Column(String(128), nullable=False)
    driver_phone = Column(String(20), nullable=False)
    truck_number = Column(String(32), nullable=False)
    truck_type = Column(String(64), nullable=False)
    origin = Column(String(128), nullable=False)
    destination = Column(String(128), nullable=False)
    current_location = Column(String(128), nullable=False)
    total_capacity_kg = Column(Float, nullable=False)
    available_capacity_kg = Column(Float, nullable=False)
    rate_per_kg_km = Column(Float, default=0.045)
    scheduled_departure = Column(String(64), default='Today 06:30 PM')
    estimated_arrival = Column(String(64), default='Today 09:15 PM')
    waypoints = Column(Text, default='')
    pooled_rate_per_kg = Column(Float, default=1.8)
    solo_rate_per_kg = Column(Float, default=4.5)
    status = Column(String(32), default='ACTIVE')

class TransactionModel(Base):
    __tablename__ = 'transactions'
    id = Column(String(32), primary_key=True)
    listing_id = Column(String(32), ForeignKey('listings.id'))
    buyer_id = Column(String(32), ForeignKey('buyers.id'))
    farmer_id = Column(String(32), ForeignKey('farmers.id'))
    truck_route_id = Column(String(32), nullable=True)
    quantity_kg = Column(Float, nullable=False)
    agreed_price_per_kg = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    logistics_shared_cost = Column(Float, default=450.0)
    logistics_solo_cost = Column(Float, default=1200.0)
    farmer_savings = Column(Float, default=750.0)
    escrow_status = Column(String(32), default='HELD_IN_ESCROW')
    status = Column(String(32), default='DISPATCH_SCHEDULED')
    otp_code = Column(String(6), default='582914')
    otp_verified = Column(Boolean, default=False)
    pickup_time = Column(String(64), default='Tomorrow 08:00 AM')
    created_at = Column(DateTime, default=datetime.utcnow)

class MandiPriceModel(Base):
    __tablename__ = 'mandi_prices'
    id = Column(Integer, primary_key=True, autoincrement=True)
    crop_name = Column(String(128), nullable=False)
    category = Column(String(64), default='Vegetable')
    modal_price = Column(Float, nullable=False)
    min_price = Column(Float, nullable=False)
    max_price = Column(Float, nullable=False)
    trend = Column(String(16), default='STABLE')
    best_mandi = Column(String(128), default='')
    history_json = Column(Text, default='[]')
    mandis_json = Column(Text, default='[]')

class SMSLogModel(Base):
    __tablename__ = 'sms_logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String(20), nullable=False)
    direction = Column(String(16), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(32), default='DELIVERED')
    created_at = Column(DateTime, default=datetime.utcnow)

class CallLogModel(Base):
    __tablename__ = 'call_logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    call_sid = Column(String(64), unique=True, index=True, nullable=False)
    from_number = Column(String(20), nullable=False)
    direction = Column(String(16), default='INBOUND')
    duration_seconds = Column(Integer, default=0)
    stage = Column(String(64), default='GREETING')
    transcript = Column(Text, default='')
    ai_response = Column(Text, default='')
    extracted_entities_json = Column(Text, default='{}')
    listing_id = Column(String(32), nullable=True)
    status = Column(String(32), default='COMPLETED')
    created_at = Column(DateTime, default=datetime.utcnow)

class SystemConfigModel(Base):
    __tablename__ = 'system_configs'
    key = Column(String(64), primary_key=True)
    value = Column(Text, nullable=False)
    description = Column(String(256), default='')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TrustLogModel(Base):
    __tablename__ = 'trust_logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    entity_type = Column(String(16), nullable=False) # 'BUYER' or 'FARMER'
    entity_id = Column(String(32), nullable=False)
    event_type = Column(String(64), nullable=False)
    delta_score = Column(Float, default=0.0)
    final_score = Column(Float, default=85.0)
    notes = Column(Text, default='')
    created_at = Column(DateTime, default=datetime.utcnow)

