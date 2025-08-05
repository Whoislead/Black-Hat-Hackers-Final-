# Evil Twin Detector - Frontend & Backend Integration Guide

## 🚀 Quick Start

### Step 1: Start the Backend API Server

1. **Navigate to Backend directory:**
   ```bash
   cd Backend
   ```

2. **Setup and start the server:**
   ```bash
   # Run the setup script (first time only)
   setup.bat
   
   # Start the server
   start_server.bat
   ```

   The API server will be available at: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`

### Step 2: Start the Frontend

1. **Navigate to Frontend directory:**
   ```bash
   cd Frontend/new
   ```

2. **Install dependencies (first time only):**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at: `http://localhost:5173`

## 🔧 How to Use

1. **Access the application:** Open `http://localhost:5173` in your browser
2. **Login/Register:** Create an account or login
3. **Navigate to Scan page:** Click the "Scan" button in the navigation
4. **Use the scanning features:**
   - **"Check secure connection"** - Scans SSL certificates of current connections
   - **"Scan nearby networks"** - Scans for nearby WiFi networks (requires Linux for full functionality)

## 🌟 Features

### Check Secure Connection
- Analyzes SSL certificates of current network traffic
- Detects potentially malicious certificates
- Shows certificate validation status

### Scan Nearby Networks
- **Linux:** Full beacon frame analysis with monitor mode
- **Windows:** Limited functionality (API will show appropriate message)
- Displays:
  - SSID (Network Name)
  - BSSID (MAC Address)
  - Channel & Frequency
  - Vendor Information
  - Location data (if available)

## 🔍 API Integration Details

The frontend now communicates with the FastAPI backend through:

- **SSL Scanning:** `POST /ssl/scan`
- **Beacon Analysis:** `POST /beacon/scan`
- **MAC Lookup:** `POST /mac/lookup`
- **Wigle Database:** `POST /wigle/lookup`
- **System Status:** `GET /status`, `GET /health`

## 🛠️ Troubleshooting

### Backend Issues
- **"Port already in use":** Kill any existing Python processes or change the port in `main.py`
- **"Module not found":** Run `setup.bat` to install dependencies
- **"Permission denied":** Some network scanning features require administrator privileges

### Frontend Issues
- **"API Disconnected":** Ensure the backend server is running on `http://localhost:8000`
- **CORS errors:** The backend is configured to allow all origins in development
- **"Network scan failed":** Beacon frame scanning requires Linux with proper network interface access

### Network Scanning Limitations
- **Windows:** Beacon frame analysis is limited due to Windows network stack limitations
- **Linux:** Requires network interface with monitor mode support
- **Permissions:** May require running with elevated privileges for network access

## 📝 Development Notes

### Environment Variables
Create a `.env` file in the frontend directory to customize settings:
```env
VITE_API_BASE_URL=http://localhost:8000
```

### API Configuration
The backend API settings can be modified in `Backend/config.py`:
- API keys for external services (Shodan, Wigle)
- Default scan timeouts
- CORS settings

## 🔐 Security Considerations

- **API Keys:** Stored in backend configuration - move to environment variables for production
- **CORS:** Currently allows all origins - restrict for production deployment
- **Network Access:** Some features require elevated system privileges
- **Data Privacy:** Network scan results are not persisted between sessions

## 📊 API Status Monitoring

The frontend includes real-time API connection monitoring:
- **Green indicator:** API server connected and responsive
- **Red indicator:** API server unreachable or not responding

## 🎯 Next Steps

1. **Test the integration:** Use both scan buttons and verify API calls in browser dev tools
2. **Check logs:** Monitor both frontend console and backend terminal for any errors
3. **Platform testing:** Test on both Windows (limited) and Linux (full functionality) if available

---

**Note:** For full network scanning capabilities, use a Linux system with appropriate network interface permissions.
