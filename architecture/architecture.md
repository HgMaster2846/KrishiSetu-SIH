# KrishiSetu AI ? System Architecture Specification
**Smart India Hackathon 2026 ? Problem Statement SIH 26033**

## Core Philosophy
**Farmer DOES NOT need a smartphone.**
- Feature phone farmers interact strictly through 24?7 Voice Calling (IVR/NLP), Keypad (DTMF), and 2-way SMS.
- Only verified buyers, logistics drivers/aggregators, and administrators access smartphone apps and web dashboards.

## Architecture Layers
1. **Feature Phone Layer**:
   - Voice calls to toll-free number `1800-260-3300`.
   - DTMF tones for keypad interaction (1 = Accept, 2 = Reject).
   - 2-Way SMS for listing receipt, buyer offers, and dispatch pickup OTPs.

2. **Cloud Telephony & Gateway Layer**:
   - Ingests PSTN/VoIP phone calls.
   - Streams audio chunks to FastAPI voice router `/voice/incoming` and `/voice/step`.
   - Synthesizes dynamic Hindi/regional speech cues.

3. **AI & Intelligence Engine Layer (FastAPI)**:
   - **Voice NLP & Entity Extractor**: Parses conversational Hindi speech into structured JSON (Crop Name, Quantity, Expected Price, Village, District, State).
   - **Buyer Recommendation Engine**: Weighted mathematical ranking:
     $$\text{Score} = 0.35 \times \text{Mandi} + 0.20 \times \text{Dist} + 0.20 \times \text{Demand} + 0.15 \times \text{Trust} + 0.10 \times \text{Cost}$$
   - **Autonomous Negotiation Agent**: Negotiates on farmer\'s behalf, protecting minimum reserve price and anchoring to APMC modal benchmarks.
   - **Pooled Logistics Matching Engine**: Identifies passing trucks with spare capacity, slashing transport costs by up to 62.5% (saving ?750 on a standard ?1200 run).
   - **Trust & Fraud Anomaly Detector**: Flags unverified entities, delayed COD promises, and extreme price deviations.

4. **Data Persistence Layer**:
   - PostgreSQL / SQLite with relational models for Farmers, Buyers, Listings, Negotiations, Offers, TruckRoutes, Transactions, MandiPrices, and SMSLogs.

5. **Client Applications Layer**:
   - Production Flutter application (`frontend_flutter/`).
   - Interactive demo SPA with Nokia/Jio Feature Phone simulator (`web_demo/`).
