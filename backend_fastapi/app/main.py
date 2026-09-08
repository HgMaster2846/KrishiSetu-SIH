import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .config import settings
from .database import init_db
from .routers import (
    voice_router,
    listings_router,
    buyers_router,
    negotiation_router,
    mandi_router,
    logistics_router,
    transactions_router,
    dashboard_router,
    sms_router,
    seed_router,
    setup_router
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database and populate sample data on startup
    init_db()
    yield

app = FastAPI(
    title="KrishiSetu AI Backend",
    description="Smart India Hackathon 2026 (SIH 26033) - Feature Phone First Farmer Marketplace",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for Flutter web and frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(voice_router)
app.include_router(listings_router)
app.include_router(buyers_router)
app.include_router(negotiation_router)
app.include_router(mandi_router)
app.include_router(logistics_router)
app.include_router(transactions_router)
app.include_router(dashboard_router)
app.include_router(sms_router)
app.include_router(seed_router)
app.include_router(setup_router)


# Mount web demo directory if exists
web_demo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "web_demo"))
if os.path.exists(web_demo_path):
    static_path = os.path.join(web_demo_path, "static")
    if os.path.exists(static_path):
        app.mount("/static", StaticFiles(directory=static_path), name="static")

    @app.get("/")
    def serve_demo_ui():
        index_file = os.path.join(web_demo_path, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {
            "message": "KrishiSetu AI Backend API is running! Access Swagger docs at /docs",
            "hackathon": "Smart India Hackathon 2026",
            "problem": "SIH 26033 - Farmer Marketplace"
        }

@app.get("/health")
def health_check():
    return {
        "status": "HEALTHY",
        "service": "KrishiSetu AI Voice & Marketplace Gateway",
        "demo_mode": settings.DEMO_MODE,
        "hotline": settings.HOTLINE_NUMBER
    }
