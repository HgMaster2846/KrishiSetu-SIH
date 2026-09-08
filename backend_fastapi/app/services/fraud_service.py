from typing import Dict, Any
from sqlalchemy.orm import Session
from ..models import models

class FraudDetectionService:
    @classmethod
    def evaluate_buyer(cls, buyer: models.BuyerModel, offer_price: float, benchmark_price: float) -> Dict[str, Any]:
        risk_score = 0
        flags = []
        
        if not buyer.verified:
            risk_score += 40
            flags.append("Unverified business entity (No APMC/GSTIN KYC)")
            
        if buyer.trust_score < 60:
            risk_score += 35
            flags.append(f"Low historical trust score ({buyer.trust_score}/100)")
            
        if buyer.total_deals < 10:
            risk_score += 15
            flags.append("New buyer with fewer than 10 completed trades")
            
        price_diff_pct = ((offer_price - benchmark_price) / benchmark_price) * 100.0
        if price_diff_pct < -30.0:
            risk_score += 25
            flags.append(f"Suspiciously low price offer ({abs(price_diff_pct):.1f}% below APMC modal rate)")
        elif price_diff_pct > 35.0:
            risk_score += 20
            flags.append("Unusually inflated offer price (potential escrow bypass bait)")
            
        if risk_score >= 50:
            category = "HIGH"
            warning_msg = "CAUTION: Highly risky transaction detected. Escrow protection enforced."
        elif risk_score >= 25:
            category = "MEDIUM"
            warning_msg = "NOTE: Standard caution advised. Verify goods upon physical handover."
        else:
            category = "LOW"
            warning_msg = "SAFE: Verified trusted partner with verified digital settlement record."
            
        return {
            "risk_level": category,
            "risk_score": risk_score,
            "flags": flags,
            "warning_message": warning_msg,
            "is_safe_to_transact": (category != "HIGH")
        }
