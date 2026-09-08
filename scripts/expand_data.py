import json
import random
import os

sample_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sample_data"))

# 1. Expand Buyers to 35
buyers_file = os.path.join(sample_dir, "buyers.json")
with open(buyers_file, encoding="utf-8") as f:
    buyers = json.load(f)

buyer_companies = [
    ("Reliance Retail Fresh Hub", "Sanjay Bhatia", "Gurugram", "Haryana", 96, "LOW", "Instant Escrow (T+0)"),
    ("BigBasket Delhi DC", "Pooja Narang", "Delhi", "Delhi", 94, "LOW", "Instant Escrow (T+0)"),
    ("Blinkit Darkstore North", "Rohit Aggarwal", "Noida", "Uttar Pradesh", 91, "LOW", "Digital UPI Mandate"),
    ("Zepto Farmgate Procurement", "Aditya Singhal", "Delhi", "Delhi", 93, "LOW", "Instant Escrow (T+0)"),
    ("Otipy Direct Kisan Mart", "Naveen Goyal", "Faridabad", "Haryana", 89, "LOW", "Digital Escrow"),
    ("ITC e-Choupal Hub", "Manish Kapoor", "Chandigarh", "Punjab", 97, "LOW", "Direct Bank Transfer"),
    ("Mother Dairy Fruit & Veg", "Sunil Saxena", "Delhi", "Delhi", 95, "LOW", "Government APMC Guarantee"),
    ("Adani Agri Logistics Hub", "Kiran Patel", "Karnal", "Haryana", 92, "LOW", "Instant Escrow (T+0)"),
    ("Haldiram Snacks Procurement", "Vikram Mittal", "Noida", "Uttar Pradesh", 90, "LOW", "Letter of Credit"),
    ("Bikanervala Agro Division", "Deepak Jindal", "Faridabad", "Haryana", 88, "LOW", "Advance 50% + Escrow"),
    ("Amritsar Cold Storage & Exports", "Harjit Chawla", "Amritsar", "Punjab", 87, "LOW", "Instant Escrow (T+0)"),
    ("Kisan Mitra Mandi Arthiya", "Ramesh Chand Gupta", "Panipat", "Haryana", 82, "MEDIUM", "Mandi Parchhi Settlement"),
    ("Jaipur Mega Food Park", "Mukesh Khandelwal", "Jaipur", "Rajasthan", 86, "LOW", "Escrow Account"),
    ("Alwar Oilseed Processors", "Nand Lal Saini", "Alwar", "Rajasthan", 89, "LOW", "Bank RTGS on Weighing"),
    ("Ludhiana Agri Supermarket", "Jaswant Sidhu", "Ludhiana", "Punjab", 85, "LOW", "Instant Escrow (T+0)")
]

for i in range(len(buyers), 35):
    idx = i - len(buyers)
    co, cp, dist, st, score, risk, terms = buyer_companies[idx % len(buyer_companies)]
    clean_name = co.lower().replace(" ", "").replace("&", "")[:10]
    b_obj = {
        "id": f"BUY-{i+1:03d}",
        "name": cp,
        "company": co,
        "contact_person": cp,
        "phone": f"+919820000{i+1:03d}",
        "email": f"procure@{clean_name}.in",
        "district": dist,
        "state": st,
        "distance_km": round(random.uniform(15.0, 110.0), 1),
        "trust_score": score,
        "verified": True,
        "total_deals": random.randint(45, 320),
        "fraud_risk": risk,
        "payment_terms": terms
    }
    buyers.append(b_obj)

with open(buyers_file, "w", encoding="utf-8") as f:
    json.dump(buyers, f, indent=2)

print(f"Buyers expanded to {len(buyers)}")

# 2. Expand Truck Routes to 22
trucks_file = os.path.join(sample_dir, "truck_routes.json")
with open(trucks_file, encoding="utf-8") as f:
    trucks = json.load(f)

extra_trucks = [
    ("Harbhajan Gill", "+919876000016", "PB-10-CZ-4411", "10-Tyre Eicher (8 Ton)", "Ludhiana Mandi", "Azadpur Mandi, Delhi", "Khanna GT Road", 8000.0, 3500.0, 0.040, "Today 07:00 PM", "Tomorrow 04:00 AM", ["Khanna", "Ambala", "Karnal", "Panipat", "Sonipat"], 1.6, 4.2),
    ("Dharampal Saini", "+919876000017", "HR-38-EF-9021", "Tata 407 (2.5 Ton)", "Alwar APMC", "Okhla Mandi, Delhi", "Bhiwadi Toll", 2500.0, 1200.0, 0.052, "Today 05:00 PM", "Today 08:30 PM", ["Bhiwadi", "Dharuhera", "Gurugram"], 2.1, 5.0),
    ("Satinder Mann", "+919876000018", "PB-02-GH-3104", "Mahindra Bolero Maxi (1.8 Ton)", "Amritsar Rural", "Jalandhar Veg Terminal", "Beas Bridge", 1800.0, 900.0, 0.055, "Today 06:15 PM", "Today 08:45 PM", ["Beas", "Kartarpur"], 2.4, 5.5),
    ("Rampal Yadav", "+919876000019", "HR-12-JK-6688", "Ashok Leyland Dost (1.5 Ton)", "Rohtak Veg Hub", "Keshopur Mandi, Delhi", "Bahadurgarh Bypass", 1500.0, 600.0, 0.058, "Today 07:30 PM", "Today 09:30 PM", ["Sampla", "Bahadurgarh"], 2.2, 5.2),
    ("Gurnoor Chatha", "+919876000020", "PB-11-LM-1123", "Tata LPT 1109 (6 Ton)", "Patiala Mandi", "Chandigarh Sector 26", "Rajpura Junction", 6000.0, 2800.0, 0.044, "Today 06:45 PM", "Today 09:15 PM", ["Rajpura", "Zirakpur"], 1.8, 4.5),
    ("Balwant Chauhan", "+919876000021", "UP-15-NP-8833", "Eicher Pro 2049 (3 Ton)", "Hapur Mandi", "Gazipur Mandi, Delhi", "Pilkhuwa Toll", 3000.0, 1400.0, 0.048, "Today 08:00 PM", "Today 10:15 PM", ["Pilkhuwa", "Dasna", "Ghaziabad"], 1.9, 4.8),
    ("Surender Dagar", "+919876000022", "HR-55-QR-5544", "Mahindra Furio (4.5 Ton)", "Faridabad Rural", "Azadpur Mandi, Delhi", "Badarpur Flyover", 4500.0, 2000.0, 0.046, "Today 09:00 PM", "Today 11:30 PM", ["Sarita Vihar", "Ring Road"], 1.7, 4.4)
]

for item in extra_trucks:
    truck_id = f"TRK-{len(trucks)+1:03d}"
    t_obj = {
        "id": truck_id,
        "driver_name": item[0],
        "driver_phone": item[1],
        "truck_number": item[2],
        "truck_type": item[3],
        "origin": item[4],
        "destination": item[5],
        "current_location": item[6],
        "total_capacity_kg": item[7],
        "available_capacity_kg": item[8],
        "rate_per_kg_km": item[9],
        "scheduled_departure": item[10],
        "estimated_arrival": item[11],
        "waypoints": item[12],
        "pooled_rate_per_kg": item[13],
        "solo_rate_per_kg": item[14],
        "status": "ACTIVE"
    }
    trucks.append(t_obj)

with open(trucks_file, "w", encoding="utf-8") as f:
    json.dump(trucks, f, indent=2)

print(f"Truck routes expanded to {len(trucks)}")

# 3. Expand Listings to 105
listings_file = os.path.join(sample_dir, "listings.json")
with open(listings_file, encoding="utf-8") as f:
    listings = json.load(f)

farmers_file = os.path.join(sample_dir, "farmers.json")
with open(farmers_file, encoding="utf-8") as f:
    farmers = json.load(f)

crops_data = [
    ("Tomato", "Vegetable", 200.0, 800.0, 22.0, 30.0, 25.8),
    ("Onion", "Vegetable", 400.0, 2000.0, 16.0, 24.0, 19.5),
    ("Potato", "Vegetable", 500.0, 3000.0, 12.0, 18.0, 14.5),
    ("Rice (Basmati 1121)", "Grain", 1000.0, 5000.0, 68.0, 85.0, 76.0),
    ("Wheat (Sharbati / MP)", "Grain", 1500.0, 8000.0, 22.0, 28.0, 24.5),
    ("Mustard (Sarson)", "Oilseed", 300.0, 1500.0, 52.0, 68.0, 61.5),
    ("Cauliflower (Gobhi)", "Vegetable", 200.0, 600.0, 18.0, 28.0, 22.0),
    ("Green Chilli (Hari Mirch)", "Vegetable", 100.0, 400.0, 35.0, 55.0, 44.0),
    ("Cotton (Kapas)", "Cash Crop", 500.0, 2500.0, 62.0, 78.0, 71.0),
    ("Sugarcane", "Cash Crop", 2000.0, 10000.0, 3.4, 4.2, 3.8)
]

for i in range(len(listings), 105):
    f_item = farmers[i % len(farmers)]
    c_info = crops_data[i % len(crops_data)]
    crop, cat, min_q, max_q, min_p, max_p, bench = c_info
    qty = round(random.uniform(min_q, max_q), 0)
    price = round(random.uniform(min_p, max_p), 1)
    
    l_obj = {
        "id": f"LIST-{i+1:03d}",
        "farmer_id": f_item["id"],
        "farmer_name": f_item["name"],
        "farmer_phone": f_item["phone"],
        "crop_name": crop,
        "category": cat,
        "quantity_kg": qty,
        "expected_price_per_kg": price,
        "farmer_min_price": round(price * 0.90, 1),
        "current_best_offer": round(price * 0.94, 1) if i % 2 == 0 else None,
        "village": f_item["village"],
        "district": f_item["district"],
        "state": f_item["state"],
        "harvest_date": "2026-09-08",
        "description": f"Freshly harvested {crop} from {f_item['village']}, {f_item['district']}. Direct farmgate pickup.",
        "quality_grade": random.choice(["Grade A+", "Grade A", "Grade A"]),
        "status": random.choice(["ACTIVE", "ACTIVE", "NEGOTIATING", "ACTIVE"]),
        "ai_mandi_benchmark": bench,
        "recommended_buyer_id": f"BUY-{(i%35)+1:03d}",
        "created_via": "AI_HOTLINE_VOICE",
        "created_at": "2026-09-06T10:00:00Z"
    }
    listings.append(l_obj)

with open(listings_file, "w", encoding="utf-8") as f:
    json.dump(listings, f, indent=2)

print(f"Listings expanded to {len(listings)}")
