# 🌾 KrishiSetu AI (कृषिसेतु एआई)
### Feature-Phone-First AI Farmer Marketplace • Smart India Hackathon 2026 (SIH 26033)
> **Tagline:** *Technology adapts to the Farmer, not the Farmer to technology.*

---

## ⚡ Zero-Coding Setup Guide (For Non-Programmers)

You **do not need to write any code**, edit files, or manually configure webhooks on telecommunication dashboards. Everything is automated through the **AI Hotline Setup** screen.

### Step 1: Create an Exotel Trial Account
1. Visit [exotel.com](https://exotel.com/) and register for a free trial.
2. Note your **Account SID**, **API Key**, **API Secret**, and your assigned **Trial Phone Number** (or use the simulated hotline number).

### Step 2: Create a Sarvam AI Account
1. Visit [sarvam.ai](https://www.sarvam.ai/) and sign up.
2. Copy your **API Subscription Key** from the dashboard (used for Hindi Speech-to-Text *Saaras* and Voice Synthesis *Bulbul*).

### Step 3: Create a Google Gemini API Key
1. Visit [aistudio.google.com](https://aistudio.google.com/).
2. Click **Create API Key** and copy it (used for Gemini 2.5 Flash natural language understanding).

### Step 4: Open KrishiSetu & Paste Credentials
1. Start the platform by running:
   ```bash
   python backend_fastapi/run.py
   ```
   *Or with Docker:*
   ```bash
   docker compose up -d
   ```
2. Open your browser to `http://localhost:8000/`.
3. Click the **AI Hotline Setup** tab on the navigation bar.
4. Paste your **Exotel**, **Sarvam**, and **Gemini** credentials into the fields.

### Step 5: Click "Verify" & "Auto Connect Hotline"
1. Click **Verify Credentials** — all indicators will turn green.
2. Click **Auto Connect Hotline** — KrishiSetu AI automatically registers all telephony webhooks (`VoiceUrl`, `SmsUrl`, `StatusCallback`, and `Live Stream`). **No manual webhook configuration needed!**

### Step 6: Deploy (1-Click)
Choose your preferred hosting provider right from the Setup page:
* **Docker Compose:** `docker compose up -d` (PostgreSQL + Redis + FastAPI + Nginx)
* **Railway:** Click the **Railway 1-Click Deploy** button in the dashboard.
* **Render:** Connect GitHub repo and launch using `render.yaml`.
* **Local Ngrok:** Run `ngrok http 8000` to get a public HTTPS link for your hotline.

### Step 7: Call the Phone Number!
1. Dial the hotline number from any mobile phone (or click **Simulate Call** on the Web Demo).
2. AI answers in conversational Hindi:
   > *"Namaste! KrishiSetu AI mein aapka swagat hai. Main aapki AI Krishi Sahayak hoon. Aap kaunsi fasal bechna chahte hain aur kitni maatra hai?"*
3. Speak your crop and location naturally (e.g. *"Mere paas 200 kilo tamatar hai Murthal Sonipat se"*).
4. Watch the listing appear live on the Buyer Marketplace!
5. Receive an SMS with buyer offers and reply **"YES"** or press **"1"** to lock the deal.

---

## 🌟 Key Features & Architectures

| Module | Feature | Capability |
| :--- | :--- | :--- |
| 📞 **AI Hotline** | Real Phone Integration | Exotel Primary + Twilio Fallback with WebSockets live audio monitor |
| 🗣️ **Voice AI** | Hindi-First Conversational Stack | Sarvam Saaras (STT) + Google Gemini 2.5 Flash (LLM) + Sarvam Bulbul (TTS) |
| 🛒 **Marketplace** | Autonomous Voice Listings | Speech converted into structured PostgreSQL listing tagged *"Created via AI Hotline"* |
| 🎯 **AI Matching** | Multi-Factor Buyer Ranking | Mandi Price (35%) + Distance (20%) + Buyer Demand (20%) + Trust (15%) + Transport (10%) |
| 🤝 **Negotiation** | Autonomous Reserve Protection | AI negotiates on farmer's behalf, never selling below the farmer's minimum reserve price |
| 📈 **Mandi APMC** | Real-Time Price Index | Real-time Mandi modal benchmark comparison with Azadpur, Karnal, and Alwar |
| 🚛 **Logistics** | Pooled Truck Route Matching | Groups nearby farmers into passing freight trucks, saving up to 60% on freight costs |
| 📩 **Feature Phone SMS** | No-Smartphone Confirmation | Confirmation via single SMS ("YES" / "HAAN"), DTMF 1 keypad press, or speech |
| 🛡️ **Trust & Fraud** | Dynamic Fraud Guard | Buyer scoring, completed order tracking, dispute flags, and instant escrow settlement |

---

## 🧪 Automated Testing & Diagnostics

KrishiSetu AI comes with automated unit and integration tests covering the complete pipeline:

```bash
# Run all 13 automated tests
python -m pytest tests/ -v
```

### 9-Point System Diagnostics Checklist
1. ✅ **Phone Number Connected:** Real Exotel trial number active
2. ✅ **Voice Telephony Gateway:** ExoML & TwiML voice routes registered
3. ✅ **Speech-to-Text (STT):** Sarvam Saaras v1 Hindi model active
4. ✅ **Conversational AI Engine:** Google Gemini 2.5 Flash + Hindi Agro NLP rules
5. ✅ **Text-to-Speech (TTS):** Sarvam Bulbul Meera Hindi TTS voice synthesis
6. ✅ **SMS Confirmation Gateway:** Multi-provider gateway (Exotel / Twilio / Mock)
7. ✅ **Relational Database:** 45 Farmers, 35 Buyers, 105 Listings, 22 Trucks indexed
8. ✅ **Buyer Marketplace Hub:** Multi-factor recommendation engine operational
9. ✅ **Pooled Logistics Engine:** Dynamic transport savings & OTP verification

---

## 📱 Frontend Applications

1. **Interactive Web Demo (`web_demo/`):**
   * Accessible at `http://localhost:8000/`
   * Interactive Nokia/Jio feature phone simulator with keypad audio (DTMF)
   * Live Call Monitor with WebSockets, streaming waveforms, and transcripts
   * AI Hotline Setup Dashboard with 1-click cloud deployment links
2. **Flutter Mobile & Web App (`frontend_flutter/`):**
   * Material Design 3 theme with agricultural palette (`#2E7D32`)
   * Android, Web, and Desktop support
   * Buyer App, Admin Dashboard, Logistics Portal, and Hotline Setup screens

---

## 📂 Project Structure

```
KrishiSetu-AI/
├── backend_fastapi/           # Production FastAPI backend
│   ├── app/
│   │   ├── api/               # API routers & endpoints
│   │   │   ├── voice.py       # Exotel webhooks, speech gather, SMS, WebSockets
│   │   │   ├── setup.py       # Zero-coding credential setup & diagnostics
│   │   │   ├── listings.py    # Marketplace listing CRUD
│   │   │   ├── buyers.py      # Buyer catalog & negotiations
│   │   │   ├── logistics.py   # Pooled truck route matching
│   │   │   └── mandi.py       # APMC mandi benchmarks
│   │   ├── services/          # Business logic & AI engines
│   │   │   ├── exotel_service.py       # Exotel telephony & webhook auto-registration
│   │   │   ├── sarvam_service.py       # Sarvam Saaras STT & Bulbul TTS
│   │   │   ├── gemini_service.py       # Google Gemini 2.5 Flash conversational AI
│   │   │   ├── websocket_manager.py    # Live call WebSocket pub/sub
│   │   │   ├── recommendation_service.py # 5-factor weighted buyer ranking
│   │   │   └── negotiation_service.py  # Autonomous reserve price protection
│   │   ├── models/            # SQLAlchemy database ORM models
│   │   └── main.py            # FastAPI entry point
│   ├── Dockerfile             # Production container spec
│   └── requirements.txt       # Dependencies
├── frontend_flutter/          # Flutter cross-platform app
├── web_demo/                  # Interactive single-page web simulator
│   └── index.html             # Feature phone simulator + Admin Monitor + Setup Dashboard
├── sample_data/               # Realistic Indian agriculture dataset
│   ├── farmers.json           # 45 Farmers (Haryana, Punjab, Rajasthan, UP)
│   ├── buyers.json            # 35 Buyers (Retail, APMC, Processors)
│   ├── listings.json          # 105 Crop listings
│   ├── truck_routes.json      # 22 Pooled freight truck routes
│   └── mandi_prices.json      # APMC mandi price history
├── tests/                     # Test suite
│   ├── test_krishisetu.py     # Core algorithm & service tests
│   └── test_ai_hotline.py     # Real telephony webhook & setup tests
├── docker-compose.yml         # Full-stack orchestrator
└── README.md                  # This documentation
```

---

## 🏆 Smart India Hackathon 2026
* **Problem Statement:** SIH 26033 – Farmer Marketplace
* **Category:** Software / Agriculture / Artificial Intelligence / Voice Public Infrastructure
* **Team:** KrishiSetu AI
