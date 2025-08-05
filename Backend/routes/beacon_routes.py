"""
Beacon frame analysis API routes
"""

from fastapi import APIRouter, HTTPException
import threading
import time
import platform
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Beacon_frame_analyzer import start_sniffing, observed_aps
from api_models import BeaconScanRequest, BeaconScanResponse

router = APIRouter(prefix="/beacon", tags=["Beacon Frame Analysis"])

# Global state for beacon scanning
beacon_scanning_state = {
    "scanning": False
}

@router.post("/scan", response_model=BeaconScanResponse)
async def scan_beacon_frames(request: BeaconScanRequest):
    """
    Scan for WiFi beacon frames on specified interface
    Note: Requires appropriate permissions and monitor mode support
    """
    try:
        # Check OS compatibility
        os_type = platform.system().lower()
        if "windows" in os_type:
            raise HTTPException(
                status_code=400, 
                detail="Beacon frame scanning not supported on Windows. Use Linux for full functionality."
            )
        
        # Clear previous results
        observed_aps.clear()
        
        # Start scanning in a thread with timeout
        scan_thread = threading.Thread(
            target=start_sniffing, 
            args=(request.interface,), 
            daemon=True
        )
        scan_thread.start()
        
        # Wait for specified duration
        time.sleep(request.duration)
        
        # Convert observed_aps to response format
        access_points = []
        for bssid, data in observed_aps.items():
            access_points.append({
                "bssid": bssid,
                **data
            })
        
        return BeaconScanResponse(
            aps_detected=len(access_points),
            access_points=access_points
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Beacon scan failed: {str(e)}")

@router.get("/results")
async def get_beacon_results():
    """
    Get current beacon frame analysis results
    """
    return {
        "aps_detected": len(observed_aps),
        "access_points": [
            {"bssid": bssid, **data} 
            for bssid, data in observed_aps.items()
        ]
    }

@router.delete("/results")
async def clear_beacon_results():
    """
    Clear stored beacon frame results
    """
    observed_aps.clear()
    return {"message": "Beacon results cleared"}

@router.get("/status")
async def get_beacon_status():
    """
    Get beacon scanning status
    """
    return {
        "scanning": beacon_scanning_state["scanning"],
        "aps_detected": len(observed_aps),
        "os_support": platform.system().lower() != "windows"
    }
