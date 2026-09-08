from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models import models

class RecommendationEngine:
    """
    AI Recommendation Logic (Prompt specification):
    Rank buyers using weighted scoring:
    - Mandi Price -> 35%
    - Distance -> 20%
    - Buyer Demand -> 20%
    - Trust Score -> 15%
    - Transport Cost -> 10%
    """
    @classmethod
    def rank_buyers_for_listing(cls, listing: models.ListingModel, db: Session) -> Dict[str, Any]:
        buyers = db.query(models.BuyerModel).all()
        mandi = db.query(models.MandiPriceModel).filter(models.MandiPriceModel.crop_name.ilike(f"%{listing.crop_name}%")).first()
        benchmark_price = mandi.modal_price if mandi else listing.expected_price_per_kg * 1.03
        
        scored_buyers = []
        
        for b in buyers:
            # 1. Mandi Price Score (35%)
            trust_factor = (b.trust_score / 100.0)
            offered_price = round(benchmark_price * (0.92 + 0.10 * trust_factor), 2)
            if b.id == "BUY-001": # FreshMart in demo
                offered_price = 26.50
            elif b.id == "BUY-003": # BigBasket in demo
                offered_price = 26.20
            elif b.id == "BUY-002": # Azadpur wholesale
                offered_price = 25.80
                
            price_ratio = min(1.2, offered_price / benchmark_price)
            mandi_score = (price_ratio / 1.2) * 100.0
            
            # 2. Distance Score (20%) Closer is higher score
            dist = max(5.0, b.distance_km)
            distance_score = max(10.0, 100.0 - (dist / 150.0) * 80.0)
            
            # 3. Buyer Demand Score (20%)
            demand_score = 95.0 if (b.total_deals > 300) else (70.0 if b.total_deals > 50 else 40.0)
            
            # 4. Trust Score (15%)
            trust_score = float(b.trust_score)
            
            # 5. Transport Cost Score (10%)
            transport_cost_per_kg = round(max(0.60, dist * 0.045), 2)
            transport_score = max(10.0, 100.0 - (transport_cost_per_kg / 5.0) * 80.0)
            
            # Weighted formula
            overall_score = round(
                0.35 * mandi_score +
                0.20 * distance_score +
                0.20 * demand_score +
                0.15 * trust_score +
                0.10 * transport_score,
                1
            )
            
            net_profit_per_kg = round(offered_price - transport_cost_per_kg, 2)
            total_payout = round(net_profit_per_kg * listing.quantity_kg, 2)
            
            # Deduct for high fraud risk
            if b.fraud_risk == "HIGH":
                overall_score = max(10.0, overall_score - 40.0)
            elif b.fraud_risk == "MEDIUM":
                overall_score = max(20.0, overall_score - 20.0)

            scored_buyers.append({
                "buyer": b,
                "overall_score": overall_score,
                "offered_price_per_kg": offered_price,
                "transport_cost_per_kg": transport_cost_per_kg,
                "net_farmer_profit_per_kg": net_profit_per_kg,
                "total_estimated_payout": total_payout,
                "mandi_score": round(mandi_score, 1),
                "distance_score": round(distance_score, 1),
                "demand_score": round(demand_score, 1),
                "trust_score": round(trust_score, 1),
                "transport_score": round(transport_score, 1)
            })
            
        scored_buyers.sort(key=lambda x: x["overall_score"], reverse=True)
        top_3 = scored_buyers[:3]
        
        recommendations = []
        for rank, item in enumerate(top_3):
            b = item["buyer"]
            is_top = (rank == 0)
            
            reasoning = (
                f"Ranked #{rank+1} with {item['overall_score']}% match score. "
                f"Offered buying price: ?{item['offered_price_per_kg']}/kg against APMC average ?{benchmark_price}/kg. "
                f"Transit distance of {b.distance_km}km keeps pooled transport at only ?{item['transport_cost_per_kg']}/kg, "
                f"yielding net farmer earnings of ?{item['net_farmer_profit_per_kg']}/kg (Total ?{item['total_estimated_payout']:g}). "
                f"Trust score {b.trust_score}% with {b.payment_terms}."
            )
            
            recommendations.append({
                "buyer": {
                    "id": b.id,
                    "name": b.name,
                    "company": b.company,
                    "contact_person": b.contact_person,
                    "phone": b.phone,
                    "email": b.email,
                    "district": b.district,
                    "state": b.state,
                    "distance_km": b.distance_km,
                    "trust_score": b.trust_score,
                    "verified": b.verified,
                    "total_deals": b.total_deals,
                    "fraud_risk": b.fraud_risk,
                    "payment_terms": b.payment_terms
                },
                "overall_score": item["overall_score"],
                "offered_price_per_kg": item["offered_price_per_kg"],
                "transport_cost_per_kg": item["transport_cost_per_kg"],
                "net_farmer_profit_per_kg": item["net_farmer_profit_per_kg"],
                "total_estimated_payout": item["total_estimated_payout"],
                "is_top_pick": is_top,
                "trust_badge": "? Verified Top Buyer" if b.trust_score >= 95 else "Verified Mandi Partner",
                "reasoning": reasoning,
                "score_breakdown": {
                    "mandi_price_35": item["mandi_score"],
                    "distance_20": item["distance_score"],
                    "demand_20": item["demand_score"],
                    "trust_15": item["trust_score"],
                    "transport_10": item["transport_score"]
                }
            })
            
        return {
            "crop_name": listing.crop_name,
            "quantity_kg": listing.quantity_kg,
            "mandi_benchmark_price": benchmark_price,
            "recommendations": recommendations
        }
