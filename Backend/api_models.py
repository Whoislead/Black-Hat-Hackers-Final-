"""
Pydantic models for API requests and responses
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class SSLScanRequest(BaseModel):
    domain: Optional[str] = None
    auto: bool = True
    interface: str = "Wi-Fi 6"
    timeout: int = 3

class SSLScanResponse(BaseModel):
    status: str
    details: str
    domain: Optional[str] = None

class BeaconScanRequest(BaseModel):
    interface: str = "Wi-Fi 6"
    duration: Optional[int] = 30  # seconds

class BeaconScanResponse(BaseModel):
    aps_detected: int
    access_points: List[Dict[str, Any]]

class MacLookupRequest(BaseModel):
    mac_address: str

class MacLookupResponse(BaseModel):
    mac_address: str
    vendor: str

class WigleLookupRequest(BaseModel):
    bssid: Optional[str] = None
    ssid: Optional[str] = None

class WigleLookupResponse(BaseModel):
    found: bool
    results: List[Dict[str, Any]]

class ShodanLookupRequest(BaseModel):
    domain: str

class ShodanLookupResponse(BaseModel):
    domain: str
    certificates: List[Dict[str, Any]]
    shodan_results: List[Dict[str, Any]]

class NetworkScanStatus(BaseModel):
    ssl_scanning: bool
    beacon_scanning: bool
    ssl_domains_scanned: int
    beacon_aps_detected: int

class HealthResponse(BaseModel):
    status: str
    timestamp: float
    services: Dict[str, str]
