"""
MAC address and network lookup API routes
"""

from fastapi import APIRouter, HTTPException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from MAC_Vendor_Lookup import lookup_vendor
from WigleAPI import wigle_check
from ShodanAPI import validate_domain, fetch_certificates
from api_models import (
    MacLookupRequest, MacLookupResponse,
    WigleLookupRequest, WigleLookupResponse,
    ShodanLookupRequest, ShodanLookupResponse
)

mac_router = APIRouter(prefix="/mac", tags=["MAC Address Lookup"])
wigle_router = APIRouter(prefix="/wigle", tags=["Wigle Database"])
shodan_router = APIRouter(prefix="/shodan", tags=["Shodan Analysis"])

@mac_router.post("/lookup", response_model=MacLookupResponse)
async def lookup_mac_vendor(request: MacLookupRequest):
    """
    Look up vendor information for a MAC address
    """
    try:
        vendor = lookup_vendor(request.mac_address)
        return MacLookupResponse(
            mac_address=request.mac_address,
            vendor=vendor
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MAC lookup failed: {str(e)}")

@wigle_router.post("/lookup", response_model=WigleLookupResponse)
async def lookup_wigle_database(request: WigleLookupRequest):
    """
    Look up WiFi network information in Wigle database
    """
    try:
        if not request.bssid and not request.ssid:
            raise HTTPException(status_code=400, detail="Either BSSID or SSID must be provided")
        
        results = wigle_check(bssid=request.bssid, ssid=request.ssid)
        
        return WigleLookupResponse(
            found=results is not None,
            results=results or []
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Wigle lookup failed: {str(e)}")

@shodan_router.post("/lookup", response_model=ShodanLookupResponse)
async def lookup_shodan_domain(request: ShodanLookupRequest):
    """
    Analyze domain using Shodan API and certificate transparency logs
    """
    try:
        # Validate domain first
        if not validate_domain(request.domain):
            raise HTTPException(status_code=400, detail="Invalid domain or could not resolve DNS")
        
        # Fetch certificates
        certificates = fetch_certificates(request.domain)
        
        # Get Shodan results (placeholder for now)
        # The original ShodanAPI.py prints results, we'd need to modify it to return data
        shodan_results = []
        
        return ShodanLookupResponse(
            domain=request.domain,
            certificates=certificates,
            shodan_results=shodan_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Shodan lookup failed: {str(e)}")
