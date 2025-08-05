"""
FastAPI Server for Evil Twin Detection System
Consolidated from multiple backend modules into a unified REST API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
import platform
from contextlib import asynccontextmanager
import sys
import os
import uvicorn


# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import API models and routes
from api_models import NetworkScanStatus, HealthResponse
from routes.ssl_routes import router as ssl_router, ssl_scanning_state
from routes.beacon_routes import router as beacon_router, beacon_scanning_state
from routes.lookup_routes import mac_router, wigle_router, shodan_router

# Import for accessing global state
from Beacon_frame_analyzer import observed_aps

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting Evil Twin Detection API Server...")
    yield
    # Shutdown
    print("Shutting down Evil Twin Detection API Server...")
    ssl_scanning_state["scanning"] = False
    beacon_scanning_state["scanning"] = False

app = FastAPI(
    title="Evil Twin Detection API",
    description="REST API for detecting evil twin WiFi networks and malicious connections",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ssl_router)
app.include_router(beacon_router)
app.include_router(mac_router)
app.include_router(wigle_router)
app.include_router(shodan_router)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Evil Twin Detection API",
        "version": "1.0.0",
        "endpoints": {
            "ssl": "/ssl/scan - SSL Certificate scanning",
            "beacon": "/beacon/scan - Beacon frame analysis", 
            "mac": "/mac/lookup - MAC address vendor lookup",
            "wigle": "/wigle/lookup - Wigle database lookup",
            "shodan": "/shodan/lookup - Shodan domain analysis",
            "status": "/status - Get scanning status"
        }
    }

@app.get("/status", response_model=NetworkScanStatus)
async def get_scanning_status():
    """Get current status of all scanning operations"""
    return NetworkScanStatus(
        ssl_scanning=ssl_scanning_state["scanning"],
        beacon_scanning=beacon_scanning_state["scanning"],
        ssl_domains_scanned=len(ssl_scanning_state["scanned_domains"]),
        beacon_aps_detected=len(observed_aps)
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return HealthResponse(
        status="healthy",
        timestamp=time.time(),
        services={
            "ssl_scanner": "operational",
            "beacon_analyzer": "operational" if platform.system().lower() != "windows" else "limited",
            "mac_lookup": "operational",
            "wigle_api": "operational",
            "shodan_api": "operational"
        }
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
