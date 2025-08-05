"""
Test script for Evil Twin Detection API
Run this script to test the API endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, data=None, expected_status=200):
    """Test a single API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n{'='*50}")
    print(f"Testing: {method} {endpoint}")
    print(f"{'='*50}")
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == expected_status:
            print("✅ SUCCESS")
        else:
            print("❌ FAILED")
        
        try:
            result = response.json()
            print("Response:")
            print(json.dumps(result, indent=2))
        except:
            print("Response (text):", response.text)
    
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR - Is the server running?")
    except Exception as e:
        print(f"❌ ERROR: {e}")

def main():
    print("🚀 Testing Evil Twin Detection API")
    print(f"Server URL: {BASE_URL}")
    
    # Test basic endpoints
    test_endpoint("GET", "/")
    test_endpoint("GET", "/health")
    test_endpoint("GET", "/status")
    
    # Test MAC lookup
    test_endpoint("POST", "/mac/lookup", {
        "mac_address": "00:11:22:33:44:55"
    })
    
    # Test SSL scan (without auto mode to avoid network dependency)
    test_endpoint("POST", "/ssl/scan", {
        "domain": "google.com",
        "auto": False
    })
    
    # Test Wigle lookup
    test_endpoint("POST", "/wigle/lookup", {
        "ssid": "TestNetwork"
    })
    
    # Test Shodan lookup
    test_endpoint("POST", "/shodan/lookup", {
        "domain": "google.com"
    })
    
    # Test beacon results (should be empty initially)
    test_endpoint("GET", "/beacon/results")
    
    # Test SSL status
    test_endpoint("GET", "/ssl/status")
    
    # Test beacon status
    test_endpoint("GET", "/beacon/status")
    
    print(f"\n{'='*50}")
    print("🎉 API Testing Complete!")
    print("Check the results above for any failures.")
    print("✅ = Success, ❌ = Failed")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
