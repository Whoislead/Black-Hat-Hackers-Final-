"""
SSL Certificate scanning API routes
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import SSL_Cert_Check
from api_models import SSLScanRequest, SSLScanResponse

router = APIRouter(prefix="/ssl", tags=["SSL Certificate Scanning"])

# Global state for SSL scanning
ssl_scanning_state = {
    "scanning": False,
    "scanned_domains": set()
}

@router.post("/scan", response_model=SSLScanResponse)
async def scan_ssl_certificate(request: SSLScanRequest):
    """
    Scan SSL certificates for a domain or auto-detect from network traffic
    """
    try:
        result = SSL_Cert_Check.ssl_scan(
            auto=request.auto,
            domain_override=request.domain
        )
        
        return SSLScanResponse(
            status=result["status"],
            details=result["details"],
            domain=request.domain
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SSL scan failed: {str(e)}")

@router.post("/scan/start-background")
async def start_ssl_background_scan(background_tasks: BackgroundTasks, interface: str = "Wi-Fi"):
    """
    Start continuous SSL scanning in the background
    """
    if ssl_scanning_state["scanning"]:
        raise HTTPException(status_code=400, detail="SSL scanning already running")
    
    ssl_scanning_state["scanning"] = True
    background_tasks.add_task(ssl_background_worker, interface)
    
    return {"message": "Background SSL scanning started", "interface": interface}

@router.post("/scan/stop-background")
async def stop_ssl_background_scan():
    """
    Stop continuous SSL scanning
    """
    ssl_scanning_state["scanning"] = False
    return {"message": "Background SSL scanning stopped"}

@router.get("/status")
async def get_ssl_status():
    """
    Get SSL scanning status
    """
    return {
        "scanning": ssl_scanning_state["scanning"],
        "domains_scanned": len(ssl_scanning_state["scanned_domains"])
    }

async def ssl_background_worker(interface: str):
    """
    Background worker for continuous SSL scanning
    """
    import time
    
    while ssl_scanning_state["scanning"]:
        try:
            result = SSL_Cert_Check.auto_scan_step(
                ssl_scanning_state["scanned_domains"],
                interface=interface
            )
            if result:
                print(f"SSL Background scan result: {result}")
        except Exception as e:
            print(f"SSL background scan error: {e}")
        
        time.sleep(3)  # Wait 3 seconds between scans
