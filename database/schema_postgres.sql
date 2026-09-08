-- ==========================================================
-- KrishiSetu AI - Production PostgreSQL Database Schema
-- Smart India Hackathon 2026 (Problem SIH 26033)
-- Digital Public Infrastructure for Feature Phone Farmers
-- ==========================================================

-- Drop existing tables if re-deploying
DROP TABLE IF EXISTS sms_logs CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS offers CASCADE;
DROP TABLE IF EXISTS negotiations CASCADE;
DROP TABLE IF EXISTS listings CASCADE;
DROP TABLE IF EXISTS truck_routes CASCADE;
DROP TABLE IF EXISTS mandi_prices CASCADE;
DROP TABLE IF EXISTS buyers CASCADE;
DROP TABLE IF EXISTS farmers CASCADE;

-- 1. Farmers Table (Feature phone users)
CREATE TABLE farmers (
    id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    village VARCHAR(128) NOT NULL,
    district VARCHAR(128) NOT NULL,
    state VARCHAR(128) NOT NULL,
    language VARCHAR(10) DEFAULT 'hi',
    land_size_acres NUMERIC(5,2) DEFAULT 2.0,
    phone_type VARCHAR(64) DEFAULT 'Feature Phone',
    kyc_verified BOOLEAN DEFAULT TRUE,
    total_sales_kg NUMERIC(10,2) DEFAULT 0.0,
    rating NUMERIC(3,2) DEFAULT 4.8,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Buyers Table (Smart dashboard users)
CREATE TABLE buyers (
    id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    company VARCHAR(256) NOT NULL,
    contact_person VARCHAR(128),
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(128) NOT NULL,
    district VARCHAR(128) NOT NULL,
    state VARCHAR(128) NOT NULL,
    distance_km NUMERIC(6,2) DEFAULT 50.0,
    trust_score INTEGER CHECK (trust_score BETWEEN 0 AND 100),
    verified BOOLEAN DEFAULT TRUE,
    total_deals INTEGER DEFAULT 0,
    fraud_risk VARCHAR(16) DEFAULT 'LOW',
    payment_terms VARCHAR(128) DEFAULT 'Instant Escrow',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Listings Table (Crops listed via Voice Hotline or SMS)
CREATE TABLE listings (
    id VARCHAR(32) PRIMARY KEY,
    farmer_id VARCHAR(32) REFERENCES farmers(id) ON DELETE CASCADE,
    crop_name VARCHAR(128) NOT NULL,
    category VARCHAR(64) DEFAULT 'Vegetable',
    quantity_kg NUMERIC(10,2) NOT NULL,
    expected_price_per_kg NUMERIC(8,2) NOT NULL,
    farmer_min_price NUMERIC(8,2) NOT NULL,
    current_best_offer NUMERIC(8,2),
    village VARCHAR(128) NOT NULL,
    district VARCHAR(128) NOT NULL,
    state VARCHAR(128) NOT NULL,
    harvest_date DATE NOT NULL,
    description TEXT,
    quality_grade VARCHAR(32) DEFAULT 'Grade A',
    status VARCHAR(32) DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'NEGOTIATING', 'SOLD', 'EXPIRED', 'CANCELLED')),
    ai_mandi_benchmark NUMERIC(8,2),
    recommended_buyer_id VARCHAR(32) REFERENCES buyers(id),
    created_via VARCHAR(32) DEFAULT 'AI_HOTLINE_VOICE',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Negotiations Table (AI-assisted negotiation)
CREATE TABLE negotiations (
    id VARCHAR(32) PRIMARY KEY,
    listing_id VARCHAR(32) REFERENCES listings(id) ON DELETE CASCADE,
    buyer_id VARCHAR(32) REFERENCES buyers(id) ON DELETE CASCADE,
    farmer_min_price NUMERIC(8,2) NOT NULL,
    current_buyer_offer NUMERIC(8,2) NOT NULL,
    current_ai_counter NUMERIC(8,2),
    status VARCHAR(32) DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'AI_COUNTERED', 'ACCEPTED', 'REJECTED', 'CLOSED')),
    ai_reasoning TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Offers Table (Step-by-step negotiation thread)
CREATE TABLE offers (
    id SERIAL PRIMARY KEY,
    negotiation_id VARCHAR(32) REFERENCES negotiations(id) ON DELETE CASCADE,
    sender VARCHAR(32) NOT NULL CHECK (sender IN ('BUYER', 'AI_FARMER_AGENT')),
    amount_per_kg NUMERIC(8,2) NOT NULL,
    message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Truck Routes Table (Pooled logistics routes)
CREATE TABLE truck_routes (
    id VARCHAR(32) PRIMARY KEY,
    driver_name VARCHAR(128) NOT NULL,
    driver_phone VARCHAR(20) NOT NULL,
    truck_number VARCHAR(32) NOT NULL,
    truck_type VARCHAR(64) NOT NULL,
    origin VARCHAR(128) NOT NULL,
    destination VARCHAR(128) NOT NULL,
    current_location VARCHAR(128) NOT NULL,
    total_capacity_kg NUMERIC(10,2) NOT NULL,
    available_capacity_kg NUMERIC(10,2) NOT NULL,
    rate_per_kg_km NUMERIC(6,4) DEFAULT 0.045,
    scheduled_departure VARCHAR(64),
    estimated_arrival VARCHAR(64),
    waypoints TEXT,
    pooled_rate_per_kg NUMERIC(6,2),
    solo_rate_per_kg NUMERIC(6,2),
    status VARCHAR(32) DEFAULT 'ACTIVE'
);

-- 7. Transactions Table (Settled deals & dispatch)
CREATE TABLE transactions (
    id VARCHAR(32) PRIMARY KEY,
    listing_id VARCHAR(32) REFERENCES listings(id),
    buyer_id VARCHAR(32) REFERENCES buyers(id),
    farmer_id VARCHAR(32) REFERENCES farmers(id),
    truck_route_id VARCHAR(32) REFERENCES truck_routes(id),
    quantity_kg NUMERIC(10,2) NOT NULL,
    agreed_price_per_kg NUMERIC(8,2) NOT NULL,
    total_amount NUMERIC(12,2) NOT NULL,
    logistics_shared_cost NUMERIC(10,2),
    logistics_solo_cost NUMERIC(10,2),
    farmer_savings NUMERIC(10,2),
    escrow_status VARCHAR(32) DEFAULT 'HELD_IN_ESCROW' CHECK (escrow_status IN ('PENDING', 'HELD_IN_ESCROW', 'RELEASED_TO_FARMER', 'REFUNDED')),
    status VARCHAR(32) DEFAULT 'DISPATCH_SCHEDULED' CHECK (status IN ('PENDING_PAYMENT', 'DISPATCH_SCHEDULED', 'IN_TRANSIT', 'DELIVERED', 'COMPLETED')),
    otp_code VARCHAR(6),
    otp_verified BOOLEAN DEFAULT FALSE,
    pickup_time VARCHAR(64),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 8. Mandi Prices Table (APMC Live Intelligence)
CREATE TABLE mandi_prices (
    id SERIAL PRIMARY KEY,
    crop_name VARCHAR(128) NOT NULL,
    category VARCHAR(64),
    mandi_name VARCHAR(128) NOT NULL,
    district VARCHAR(128) NOT NULL,
    state VARCHAR(128) NOT NULL,
    min_price NUMERIC(8,2) NOT NULL,
    max_price NUMERIC(8,2) NOT NULL,
    modal_price NUMERIC(8,2) NOT NULL,
    arrival_tonnes NUMERIC(10,2),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 9. SMS Logs Table (2-Way SMS confirmation trail)
CREATE TABLE sms_logs (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(20) NOT NULL,
    direction VARCHAR(16) NOT NULL CHECK (direction IN ('OUTGOING', 'INCOMING')),
    message TEXT NOT NULL,
    status VARCHAR(32) DEFAULT 'DELIVERED',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for lightning fast queries
CREATE INDEX idx_listings_crop ON listings(crop_name);
CREATE INDEX idx_listings_status ON listings(status);
CREATE INDEX idx_buyers_trust ON buyers(trust_score);
CREATE INDEX idx_trucks_avail ON truck_routes(available_capacity_kg);
