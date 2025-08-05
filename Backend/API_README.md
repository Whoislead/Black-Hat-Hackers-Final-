# Evil Twin Detection API Documentation

## Overview
The Evil Twin Detection API is a unified FastAPI server that consolidates all the backend functionalities of the Evil Twin Detector system into a single RESTful API. This API provides endpoints for SSL certificate scanning, beacon frame analysis, MAC address lookups, and network intelligence gathering.

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows PowerShell (for Windows users)
- Administrator privileges (for network scanning features)

### Installation
1. Navigate to the Backend directory
2. Run the setup script:
   ```bash
   setup.bat
   ```
3. Start the server:
   ```bash
   start_server.bat
   ```

### Alternative Manual Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Start server
python main.py
```

## API Endpoints

### Base URL
- Local development: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### Core Endpoints

#### 1. Root Information
- **GET** `/`
- Returns API information and available endpoints

#### 2. Health Check
- **GET** `/health`
- Returns server health status and service availability

#### 3. System Status
- **GET** `/status`
- Returns current scanning status for all services

### SSL Certificate Scanning

#### Single SSL Scan
- **POST** `/ssl/scan`
- Body:
  ```json
  {
    "domain": "example.com",  // Optional: specific domain
    "auto": true,             // Auto-detect from traffic
    "interface": "Wi-Fi",     // Network interface
    "timeout": 3              // Timeout in seconds
  }
  ```

#### Background SSL Scanning
- **POST** `/ssl/scan/start-background?interface=Wi-Fi`
- **POST** `/ssl/scan/stop-background`
- **GET** `/ssl/status`

### Beacon Frame Analysis

#### Scan Beacon Frames
- **POST** `/beacon/scan`
- Body:
  ```json
  {
    "interface": "wlan0",  // Network interface
    "duration": 30         // Scan duration in seconds
  }
  ```
- **Note**: Requires Linux and monitor mode support

#### Beacon Results Management
- **GET** `/beacon/results` - Get current results
- **DELETE** `/beacon/results` - Clear stored results
- **GET** `/beacon/status` - Get scanning status

### MAC Address Lookup

#### Vendor Lookup
- **POST** `/mac/lookup`
- Body:
  ```json
  {
    "mac_address": "00:11:22:33:44:55"
  }
  ```

### Network Intelligence

#### Wigle Database Lookup
- **POST** `/wigle/lookup`
- Body:
  ```json
  {
    "bssid": "00:11:22:33:44:55",  // Optional
    "ssid": "NetworkName"          // Optional
  }
  ```
- **Note**: Either BSSID or SSID must be provided

#### Shodan Domain Analysis
- **POST** `/shodan/lookup`
- Body:
  ```json
  {
    "domain": "example.com"
  }
  ```

## Response Formats

### Success Response Example
```json
{
  "status": "safe",
  "details": "SSL certificate validation successful",
  "domain": "example.com"
}
```

### Error Response Example
```json
{
  "detail": "SSL scan failed: Connection timeout"
}
```

### Status Response Example
```json
{
  "ssl_scanning": false,
  "beacon_scanning": false,
  "ssl_domains_scanned": 5,
  "beacon_aps_detected": 12
}
```

## Configuration

### Environment Variables
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `RELOAD`: Enable auto-reload (default: true)

### API Keys
Configure in `config.py`:
- Shodan API Key
- Wigle API Credentials
- MAC Lookup API Key

## Platform Support

### Windows
- ✅ SSL Certificate Scanning
- ✅ MAC Address Lookup
- ✅ Wigle Database Queries
- ✅ Shodan Analysis
- ❌ Beacon Frame Analysis (limited Windows support)

### Linux
- ✅ Full feature support
- ✅ Beacon Frame Analysis with monitor mode

## Security Considerations

1. **API Keys**: Store sensitive API keys in environment variables
2. **CORS**: Configure allowed origins appropriately for production
3. **Network Access**: Some features require elevated privileges
4. **Rate Limiting**: Consider implementing rate limiting for production

## Error Handling

The API uses standard HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid parameters)
- `500`: Internal Server Error

## Integration Examples

### Python Client
```python
import requests

# SSL Scan
response = requests.post('http://localhost:8000/ssl/scan', 
                        json={'domain': 'example.com'})
result = response.json()

# MAC Lookup
response = requests.post('http://localhost:8000/mac/lookup',
                        json={'mac_address': '00:11:22:33:44:55'})
vendor = response.json()['vendor']
```

### JavaScript/Frontend
```javascript
// SSL Scan
const response = await fetch('http://localhost:8000/ssl/scan', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ domain: 'example.com' })
});
const result = await response.json();
```

## Migration from Original Files

The API consolidates these original files:
- `Driver.py` → GUI replaced with REST API
- `SSL_Cert_Check.py` → `/ssl/*` endpoints
- `Beacon_frame_analyzer.py` → `/beacon/*` endpoints
- `MAC_Vendor_Lookup.py` → `/mac/*` endpoints
- `WigleAPI.py` → `/wigle/*` endpoints
- `ShodanAPI.py` → `/shodan/*` endpoints
- `MainApp.py` → Consolidated into main API

## Support

For issues or questions:
1. Check the interactive API documentation at `/docs`
2. Review server logs for error details
3. Ensure all dependencies are properly installed
4. Verify network interface names for your system
