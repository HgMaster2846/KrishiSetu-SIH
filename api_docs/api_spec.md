# KrishiSetu AI ? REST API Documentation
Base URL: `http://localhost:8000` ? Swagger Docs: `http://localhost:8000/docs`

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/voice/incoming` | Initiates hotline voice call session |
| `POST` | `/voice/step` | Processes conversational voice dialogue steps |
| `POST` | `/voice/transcribe` | Simulates Whisper Speech-to-Text extraction |
| `POST` | `/listing/create` | Creates new crop listing |
| `GET` | `/listing/all` | Lists all marketplace crops with filters |
| `GET` | `/listing/{id}` | Gets listing details by ID |
| `GET` | `/buyers/all` | Lists registered buyers |
| `GET` | `/buyers/recommend` | Top 3 AI-ranked buyers with 5-factor scoring |
| `POST` | `/negotiation/start` | Starts AI negotiation session |
| `POST` | `/negotiation/respond` | Submits counter-offer, accept, or reject |
| `GET` | `/negotiation/{id}/history`| Gets negotiation timeline & AI reasoning |
| `GET` | `/mandi/prices` | Real-time APMC Agmarknet price feeds |
| `GET` | `/mandi/best-today` | Top market arbitrage recommendations |
| `GET` | `/logistics/routes` | Lists pooled truck routes with savings |
| `POST` | `/transaction/confirm` | Confirms trade, locks escrow, assigns truck |
| `POST` | `/transaction/verify-otp` | Verifies produce handover OTP |
| `GET` | `/dashboard/admin` | Platform analytics & fraud alerts |
| `GET` | `/dashboard/buyer` | Buyer dashboard statistics |
| `POST` | `/sms/send` | Dispatches outgoing SMS |
| `POST` | `/sms/reply` | Simulates feature phone SMS incoming response |
| `GET` | `/sms/logs` | Fetches SMS conversation thread |
| `POST` | `/seed/reset` | Resets and re-seeds fresh SIH demo data |
