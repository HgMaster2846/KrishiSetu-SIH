import os, json
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import settings

connect_args = {'check_same_thread': False} if 'sqlite' in settings.DATABASE_URL else {}
engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from .models import models
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        farmer_count = db.query(models.FarmerModel).count()
        if farmer_count > 0:
            return
        
        sample_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'sample_data'))
        
        # 1. Farmers
        farmers_file = os.path.join(sample_dir, 'farmers.json')
        if os.path.exists(farmers_file):
            with open(farmers_file, encoding='utf-8') as f:
                farmers_data = json.load(f)
                for f_item in farmers_data:
                    farmer = models.FarmerModel(
                        id=f_item['id'],
                        name=f_item['name'],
                        phone=f_item['phone'],
                        village=f_item['village'],
                        district=f_item['district'],
                        state=f_item['state'],
                        language=f_item.get('language', 'hi'),
                        land_size_acres=f_item.get('land_size_acres', 2.0),
                        phone_type=f_item.get('phone_type', 'Feature Phone'),
                        kyc_verified=f_item.get('kyc_verified', True),
                        rating=f_item.get('rating', 4.8)
                    )
                    db.add(farmer)
            db.commit()

        # 2. Buyers
        buyers_file = os.path.join(sample_dir, 'buyers.json')
        if os.path.exists(buyers_file):
            with open(buyers_file, encoding='utf-8') as f:
                buyers_data = json.load(f)
                for b_item in buyers_data:
                    buyer = models.BuyerModel(
                        id=b_item['id'],
                        name=b_item['name'],
                        company=b_item['company'],
                        contact_person=b_item.get('contact_person', ''),
                        phone=b_item['phone'],
                        email=b_item['email'],
                        district=b_item['district'],
                        state=b_item['state'],
                        distance_km=b_item.get('distance_km', 50.0),
                        trust_score=b_item.get('trust_score', 90),
                        verified=b_item.get('verified', True),
                        total_deals=b_item.get('total_deals', 100),
                        fraud_risk=b_item.get('fraud_risk', 'LOW'),
                        payment_terms=b_item.get('payment_terms', 'Instant Escrow')
                    )
                    db.add(buyer)
            db.commit()

        # 3. Truck Routes
        trucks_file = os.path.join(sample_dir, 'truck_routes.json')
        if os.path.exists(trucks_file):
            with open(trucks_file, encoding='utf-8') as f:
                trucks_data = json.load(f)
                for t_item in trucks_data:
                    truck = models.TruckRouteModel(
                        id=t_item['id'],
                        driver_name=t_item['driver_name'],
                        driver_phone=t_item['driver_phone'],
                        truck_number=t_item['truck_number'],
                        truck_type=t_item['truck_type'],
                        origin=t_item['origin'],
                        destination=t_item['destination'],
                        current_location=t_item['current_location'],
                        total_capacity_kg=t_item['total_capacity_kg'],
                        available_capacity_kg=t_item['available_capacity_kg'],
                        rate_per_kg_km=t_item.get('rate_per_kg_km', 0.045),
                        scheduled_departure=t_item.get('scheduled_departure', 'Today 06:30 PM'),
                        estimated_arrival=t_item.get('estimated_arrival', 'Today 09:15 PM'),
                        waypoints=','.join(t_item.get('waypoints', [])),
                        pooled_rate_per_kg=t_item.get('pooled_rate_per_kg', 1.8),
                        solo_rate_per_kg=t_item.get('solo_rate_per_kg', 4.5)
                    )
                    db.add(truck)
            db.commit()

        # 4. Mandi Prices
        mandi_file = os.path.join(sample_dir, 'mandi_prices.json')
        if os.path.exists(mandi_file):
            with open(mandi_file, encoding='utf-8') as f:
                mandi_data = json.load(f)
                for m_item in mandi_data:
                    mandi = models.MandiPriceModel(
                        crop_name=m_item['crop'],
                        category=m_item.get('category', 'Vegetable'),
                        modal_price=m_item['modal_price'],
                        min_price=m_item['min_price'],
                        max_price=m_item['max_price'],
                        trend=m_item.get('trend', 'STABLE'),
                        best_mandi=m_item.get('best_mandi', ''),
                        history_json=json.dumps(m_item.get('history_7d', [])),
                        mandis_json=json.dumps(m_item.get('mandis', []))
                    )
                    db.add(mandi)
            db.commit()

        # 5. Listings
        listings_file = os.path.join(sample_dir, 'listings.json')
        if os.path.exists(listings_file):
            with open(listings_file, encoding='utf-8') as f:
                listings_data = json.load(f)
                for l_item in listings_data:
                    listing = models.ListingModel(
                        id=l_item['id'],
                        farmer_id=l_item['farmer_id'],
                        farmer_name=l_item['farmer_name'],
                        farmer_phone=l_item['farmer_phone'],
                        crop_name=l_item['crop_name'],
                        category=l_item.get('category', 'Vegetable'),
                        quantity_kg=l_item['quantity_kg'],
                        expected_price_per_kg=l_item['expected_price_per_kg'],
                        farmer_min_price=l_item.get('farmer_min_price', l_item['expected_price_per_kg'] * 0.9),
                        current_best_offer=l_item.get('current_best_offer'),
                        village=l_item['village'],
                        district=l_item['district'],
                        state=l_item['state'],
                        harvest_date=l_item.get('harvest_date', '2026-09-06'),
                        description=l_item.get('description', ''),
                        quality_grade=l_item.get('quality_grade', 'Grade A'),
                        status=l_item.get('status', 'ACTIVE'),
                        ai_mandi_benchmark=l_item.get('ai_mandi_benchmark', 25.8),
                        recommended_buyer_id=l_item.get('recommended_buyer_id', 'BUY-001'),
                        created_via=l_item.get('created_via', 'AI_HOTLINE_VOICE'),
                        created_at=l_item.get('created_at')
                    )
                    db.add(listing)
            db.commit()

        # 6. Sample Initial Negotiation and Offer for LIST-001
        neg = models.NegotiationModel(
            id='NEG-001',
            listing_id='LIST-001',
            buyer_id='BUY-001',
            farmer_min_price=23.5,
            current_buyer_offer=24.0,
            current_ai_counter=25.8,
            status='AI_COUNTERED',
            ai_reasoning='Current mandi average is ₹25.80/kg. Offering ₹24.0/kg is below APMC modal rate. AI proposed counter of ₹25.80/kg to secure fair farmer return.'
        )
        db.add(neg)
        db.commit()

        offer1 = models.OfferModel(
            negotiation_id='NEG-001',
            sender='BUYER',
            amount_per_kg=24.0,
            message='Buyer FreshMart offered ₹24.00/kg for 200kg Tomato.'
        )
        offer2 = models.OfferModel(
            negotiation_id='NEG-001',
            sender='AI_FARMER_AGENT',
            amount_per_kg=25.8,
            message='KrishiSetu AI Counter: Current Azadpur modal price is ₹28.50/kg and local average is ₹25.80/kg. We counter at ₹25.80/kg.'
        )
        db.add(offer1)
        db.add(offer2)
        db.commit()

        # 7. Sample Initial SMS Log
        sms1 = models.SMSLogModel(
            phone='+919812345001',
            direction='OUTGOING',
            message='[KrishiSetu AI] Namaste Rameshwar ji! Aapka 200kg Tamatar listing darj ho gaya hai (ID: LIST-001). Expected daam: Rs 25/kg.',
            status='DELIVERED'
        )
        sms2 = models.SMSLogModel(
            phone='+919812345001',
            direction='OUTGOING',
            message='[KrishiSetu AI] Buyer FreshMart ne Rs 25.5/kg ka offer bheja hai. Shared truck pickup: Kal subah 8 AM. Confirm karne ke liye reply karein YES ya Dial karein 1.',
            status='DELIVERED'
        )
        sms3 = models.SMSLogModel(
            phone='+919812345001',
            direction='INCOMING',
            message='YES',
            status='RECEIVED'
        )
        db.add_all([sms1, sms2, sms3])
        db.commit()

        # 8. Sample Initial Call Logs for Live Hotline Monitor
        call1 = models.CallLogModel(
            call_sid='CALL-EXO-9812345001-01',
            from_number='+919812345001',
            direction='INBOUND',
            duration_seconds=94,
            stage='LISTING_CREATED',
            transcript='Farmer: Namaste, mere paas 200 kilo tamatar hai Murthal Sonipat se aur 25 rupaye kilo chahiye.\nAI: Namaste Rameshwar ji! Aapka 200kg Tamatar darj kar liya gaya hai.',
            ai_response='Aapka listing LIST-001 ban gaya hai.',
            extracted_entities_json=json.dumps({'crop_name': 'Tomato', 'quantity_kg': 200, 'village': 'Murthal', 'district': 'Sonipat', 'expected_price': 25.0}),
            listing_id='LIST-001',
            status='COMPLETED'
        )
        call2 = models.CallLogModel(
            call_sid='CALL-EXO-9812345002-02',
            from_number='+919812345002',
            direction='INBOUND',
            duration_seconds=78,
            stage='LISTING_CREATED',
            transcript='Farmer: Haanji, Samalkha Panipat se 5 quintal pyaz bechna hai 18 rupaye kilo.\nAI: Sat Sri Akal Baldev ji! 500kg Pyaz listing LIST-002 darj ho gayi hai.',
            ai_response='Aapka listing LIST-002 ban gaya hai.',
            extracted_entities_json=json.dumps({'crop_name': 'Onion', 'quantity_kg': 500, 'village': 'Samalkha', 'district': 'Panipat', 'expected_price': 18.0}),
            listing_id='LIST-002',
            status='COMPLETED'
        )
        db.add_all([call1, call2])
        db.commit()

        # 9. Sample Trust Score Logs
        t1 = models.TrustLogModel(
            entity_type='BUYER',
            entity_id='BUY-001',
            event_type='PROMPT_ESCROW_RELEASE',
            delta_score=2.0,
            final_score=94.0,
            notes='Released escrow payment within 15 minutes of farmgate weighing.'
        )
        t2 = models.TrustLogModel(
            entity_type='BUYER',
            entity_id='BUY-019',
            event_type='UNREASONABLE_PRICE_DROP',
            delta_score=-15.0,
            final_score=42.0,
            notes='High fraud risk: Buyer attempted to unilaterally cut agreed price at delivery.'
        )
        db.add_all([t1, t2])
        db.commit()


    except Exception as e:
        db.rollback()
        print(f'Error seeding database: {e}')
    finally:
        db.close()
