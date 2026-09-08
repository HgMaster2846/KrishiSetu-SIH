from datetime import datetime
from typing import Dict, Any
from sqlalchemy.orm import Session
from ..models import models

class NegotiationService:
    @classmethod
    def start_negotiation(cls, listing_id: str, buyer_id: str, buyer_offer_per_kg: float, db: Session) -> Dict[str, Any]:
        listing = db.query(models.ListingModel).filter(models.ListingModel.id == listing_id).first()
        buyer = db.query(models.BuyerModel).filter(models.BuyerModel.id == buyer_id).first()
        if not listing or not buyer:
            raise ValueError("Listing or Buyer not found")

        mandi = db.query(models.MandiPriceModel).filter(models.MandiPriceModel.crop_name.ilike(f"%{listing.crop_name}%")).first()
        benchmark = mandi.modal_price if mandi else listing.ai_mandi_benchmark
        farmer_min = listing.farmer_min_price
        
        # Determine initial AI counter offer
        if buyer_offer_per_kg >= benchmark:
            status = "ACCEPTED"
            ai_counter = buyer_offer_per_kg
            ai_reasoning = f"Buyer offer of ?{buyer_offer_per_kg}/kg exceeds current mandi average of ?{benchmark}/kg. AI auto-accepted on behalf of farmer."
        elif buyer_offer_per_kg < farmer_min:
            status = "AI_COUNTERED"
            ai_counter = round(max(benchmark, farmer_min * 1.08), 1)
            ai_reasoning = f"Buyer offer of ?{buyer_offer_per_kg}/kg is below farmer's reserve price (?{farmer_min}/kg). AI countered at ?{ai_counter}/kg protecting farmer income."
        else:
            status = "AI_COUNTERED"
            ai_counter = round((buyer_offer_per_kg + benchmark) / 2.0, 1)
            ai_reasoning = f"Current mandi average is ?{benchmark}/kg. Buyer offered ?{buyer_offer_per_kg}/kg. AI countered at ?{ai_counter}/kg to maximize profit while keeping deal attractive."

        neg_id = f"NEG-{datetime.utcnow().strftime('%M%S')}"
        neg = models.NegotiationModel(
            id=neg_id,
            listing_id=listing_id,
            buyer_id=buyer_id,
            farmer_min_price=farmer_min,
            current_buyer_offer=buyer_offer_per_kg,
            current_ai_counter=ai_counter,
            status=status,
            ai_reasoning=ai_reasoning
        )
        db.add(neg)
        db.commit()

        offer_buyer = models.OfferModel(
            negotiation_id=neg_id,
            sender="BUYER",
            amount_per_kg=buyer_offer_per_kg,
            message=f"{buyer.name} offered ?{buyer_offer_per_kg:.2f}/kg for {listing.quantity_kg:g}kg {listing.crop_name}."
        )
        db.add(offer_buyer)
        
        if status == "AI_COUNTERED":
            offer_ai = models.OfferModel(
                negotiation_id=neg_id,
                sender="AI_FARMER_AGENT",
                amount_per_kg=ai_counter,
                message=f"KrishiSetu AI Counter: ?{ai_counter:.2f}/kg. (APMC Modal Benchmark: ?{benchmark:.2f}/kg)."
            )
            db.add(offer_ai)
            
        sms_msg = f"[KrishiSetu AI] Buyer {buyer.name} ne aapke {listing.crop_name} ke liye Rs {buyer_offer_per_kg}/kg ka offer diya hai. AI ne Rs {ai_counter}/kg ka counter bheja hai."
        sms = models.SMSLogModel(
            phone=listing.farmer_phone,
            direction="OUTGOING",
            message=sms_msg,
            status="DELIVERED"
        )
        db.add(sms)
        
        listing.status = "NEGOTIATING"
        listing.current_best_offer = buyer_offer_per_kg
        db.commit()
        
        return cls.get_negotiation_details(neg_id, db)

    @classmethod
    def respond_to_negotiation(cls, negotiation_id: str, counter_offer: float, action: str, db: Session) -> Dict[str, Any]:
        neg = db.query(models.NegotiationModel).filter(models.NegotiationModel.id == negotiation_id).first()
        if not neg:
            raise ValueError("Negotiation not found")
            
        listing = db.query(models.ListingModel).filter(models.ListingModel.id == neg.listing_id).first()
        buyer = db.query(models.BuyerModel).filter(models.BuyerModel.id == neg.buyer_id).first()
        mandi = db.query(models.MandiPriceModel).filter(models.MandiPriceModel.crop_name.ilike(f"%{listing.crop_name}%")).first()
        benchmark = mandi.modal_price if mandi else listing.ai_mandi_benchmark

        if action == "ACCEPT":
            neg.status = "ACCEPTED"
            neg.current_buyer_offer = counter_offer or neg.current_ai_counter
            neg.ai_reasoning = f"Deal accepted at ?{neg.current_buyer_offer}/kg! Final profitable price locked for {listing.farmer_name}."
            
            offer = models.OfferModel(
                negotiation_id=neg.id,
                sender="BUYER",
                amount_per_kg=neg.current_buyer_offer,
                message=f"Buyer {buyer.name} accepted the counter price of ?{neg.current_buyer_offer:.2f}/kg."
            )
            db.add(offer)
            
            listing.status = "SOLD"
            listing.current_best_offer = neg.current_buyer_offer
            
            total_amt = round(neg.current_buyer_offer * listing.quantity_kg, 2)
            tx_id = f"TX-{datetime.utcnow().strftime('%M%S')}"
            tx = models.TransactionModel(
                id=tx_id,
                listing_id=listing.id,
                buyer_id=buyer.id,
                farmer_id=listing.farmer_id,
                truck_route_id="TRUCK-001",
                quantity_kg=listing.quantity_kg,
                agreed_price_per_kg=neg.current_buyer_offer,
                total_amount=total_amt,
                logistics_shared_cost=450.0,
                logistics_solo_cost=1200.0,
                farmer_savings=750.0,
                escrow_status="HELD_IN_ESCROW",
                status="DISPATCH_SCHEDULED",
                otp_code="582914",
                pickup_time="Tomorrow 08:00 AM"
            )
            db.add(tx)
            
            sms_msg = (
                f"[KrishiSetu AI] Badhai ho! {listing.crop_name} ki deal Rs {neg.current_buyer_offer}/kg par pakki ho gayi. "
                f"Buyer: {buyer.name}. Total Payout: Rs {total_amt:g}. Pickup: Kal subah 8 AM. "
                f"Truck HR-10-AJ-4821 assign ho gaya hai. Confirm karne ke liye reply karein YES ya Dial karein 1."
            )
            sms = models.SMSLogModel(
                phone=listing.farmer_phone,
                direction="OUTGOING",
                message=sms_msg,
                status="DELIVERED"
            )
            db.add(sms)
            db.commit()

        elif action == "REJECT":
            neg.status = "REJECTED"
            neg.ai_reasoning = "Negotiation closed without agreement."
            db.commit()
            
        else: # "COUNTER"
            neg.current_buyer_offer = counter_offer
            offer_buyer = models.OfferModel(
                negotiation_id=neg.id,
                sender="BUYER",
                amount_per_kg=counter_offer,
                message=f"Buyer counter-offered ?{counter_offer:.2f}/kg."
            )
            db.add(offer_buyer)

            if counter_offer >= (benchmark * 0.98):
                neg.status = "ACCEPTED"
                neg.current_ai_counter = counter_offer
                neg.ai_reasoning = f"Current mandi average is ?{benchmark:.2f}/kg. Buyer offer of ?{counter_offer:.2f}/kg is fair and profitable. AI accepted on behalf of farmer."
                
                offer_ai = models.OfferModel(
                    negotiation_id=neg.id,
                    sender="AI_FARMER_AGENT",
                    amount_per_kg=counter_offer,
                    message=f"KrishiSetu AI: Accepted! Current mandi average is ?{benchmark:.2f}/kg. This is the best profitable offer."
                )
                db.add(offer_ai)
                listing.status = "SOLD"
                listing.current_best_offer = counter_offer
                
                total_amt = round(counter_offer * listing.quantity_kg, 2)
                tx_id = f"TX-{datetime.utcnow().strftime('%M%S')}"
                tx = models.TransactionModel(
                    id=tx_id,
                    listing_id=listing.id,
                    buyer_id=buyer.id,
                    farmer_id=listing.farmer_id,
                    truck_route_id="TRUCK-001",
                    quantity_kg=listing.quantity_kg,
                    agreed_price_per_kg=counter_offer,
                    total_amount=total_amt,
                    logistics_shared_cost=450.0,
                    logistics_solo_cost=1200.0,
                    farmer_savings=750.0,
                    escrow_status="HELD_IN_ESCROW",
                    status="DISPATCH_SCHEDULED",
                    otp_code="582914",
                    pickup_time="Tomorrow 08:00 AM"
                )
                db.add(tx)
                
                sms_msg = (
                    f"[KrishiSetu AI] Badhai ho! {listing.crop_name} ki deal Rs {counter_offer}/kg par pakki ho gayi. "
                    f"Buyer: {buyer.name}. Total Payout: Rs {total_amt:g}. Pickup: Kal subah 8 AM. "
                    f"Truck HR-10-AJ-4821 assign ho gaya hai. Confirm karne ke liye reply karein YES ya Dial karein 1."
                )
                sms = models.SMSLogModel(
                    phone=listing.farmer_phone,
                    direction="OUTGOING",
                    message=sms_msg,
                    status="DELIVERED"
                )
                db.add(sms)

            elif counter_offer < neg.farmer_min_price:
                neg.status = "AI_COUNTERED"
                new_ai_counter = round(max(benchmark, neg.farmer_min_price * 1.05), 1)
                neg.current_ai_counter = new_ai_counter
                neg.ai_reasoning = f"Buyer counter ?{counter_offer}/kg is below farmer minimum ?{neg.farmer_min_price}/kg. AI stood firm at ?{new_ai_counter}/kg."
                
                offer_ai = models.OfferModel(
                    negotiation_id=neg.id,
                    sender="AI_FARMER_AGENT",
                    amount_per_kg=new_ai_counter,
                    message=f"KrishiSetu AI Counter: Minimum reserve is ?{neg.farmer_min_price}/kg. Best counter is ?{new_ai_counter:.2f}/kg based on APMC rates."
                )
                db.add(offer_ai)
            else:
                neg.status = "AI_COUNTERED"
                new_ai_counter = round((counter_offer + benchmark) / 2.0, 1)
                neg.current_ai_counter = new_ai_counter
                neg.ai_reasoning = f"Buyer offered ?{counter_offer}/kg. AI strategically met midway towards mandi rate ?{benchmark}/kg with counter ?{new_ai_counter}/kg."
                
                offer_ai = models.OfferModel(
                    negotiation_id=neg.id,
                    sender="AI_FARMER_AGENT",
                    amount_per_kg=new_ai_counter,
                    message=f"KrishiSetu AI Counter: Moving closer to agreement at ?{new_ai_counter:.2f}/kg."
                )
                db.add(offer_ai)

            db.commit()

        return cls.get_negotiation_details(negotiation_id, db)

    @classmethod
    def get_negotiation_details(cls, negotiation_id: str, db: Session) -> Dict[str, Any]:
        neg = db.query(models.NegotiationModel).filter(models.NegotiationModel.id == negotiation_id).first()
        if not neg:
            raise ValueError("Negotiation not found")
        listing = db.query(models.ListingModel).filter(models.ListingModel.id == neg.listing_id).first()
        buyer = db.query(models.BuyerModel).filter(models.BuyerModel.id == neg.buyer_id).first()
        offers = db.query(models.OfferModel).filter(models.OfferModel.negotiation_id == neg.id).order_by(models.OfferModel.id.asc()).all()
        
        offer_history = []
        for o in offers:
            offer_history.append({
                "sender": o.sender,
                "amount_per_kg": o.amount_per_kg,
                "message": o.message,
                "timestamp": o.created_at.strftime("%I:%M %p") if o.created_at else "Just now"
            })
            
        return {
            "id": neg.id,
            "listing_id": neg.listing_id,
            "buyer_id": neg.buyer_id,
            "buyer_name": buyer.name if buyer else "Buyer",
            "crop_name": listing.crop_name if listing else "Crop",
            "quantity_kg": listing.quantity_kg if listing else 0.0,
            "farmer_min_price": neg.farmer_min_price,
            "current_buyer_offer": neg.current_buyer_offer,
            "current_ai_counter": neg.current_ai_counter,
            "status": neg.status,
            "ai_reasoning": neg.ai_reasoning,
            "offers": offer_history
        }
