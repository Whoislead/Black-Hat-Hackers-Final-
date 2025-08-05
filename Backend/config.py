"""
Configuration settings for Evil Twin Detection API
"""

import os
from typing import List

class Settings:
    # API Configuration
    API_TITLE = "Evil Twin Detection API"
    API_DESCRIPTION = "REST API for detecting evil twin WiFi networks and malicious connections"
    API_VERSION = "1.0.0"
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    RELOAD = os.getenv("RELOAD", "true").lower() == "true"
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "*"  # Configure appropriately for production
    ]
    
    # Scanning Configuration
    DEFAULT_SCAN_TIMEOUT = 30  # seconds
    DEFAULT_SSL_INTERFACE = "Wi-Fi"
    SSL_SCAN_INTERVAL = 3  # seconds between SSL scans
    
    # API Keys (should be moved to environment variables in production)
    SHODAN_API_KEY = "Ims2KdUauqQBpLcooMwzVvguk7IxneJD"
    WIGLE_USERNAME = "AID353e1b45a21270feb01d6319058a0d6b"
    WIGLE_PASSWORD = "92016658087d849231db3a1d2c4f1870"
    MACLOOKUP_API_KEY = "01k1gmjj9m9vjpatcbwx7zysqz01k1gmqn38q7fgwcwbjymd5rctuwgclm6iyywj"

# Create settings instance
settings = Settings()
