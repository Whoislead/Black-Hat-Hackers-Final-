/**
 * Configuration settings for the Evil Twin Detector frontend
 */

export const config = {
  // API Configuration
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  
  // Application Settings
  APP_NAME: 'Evil Twin Detector',
  VERSION: '1.0.0',
  
  // Scan Settings
  DEFAULT_BEACON_SCAN_DURATION: 30, // seconds
  DEFAULT_SSL_TIMEOUT: 5, // seconds
  
  // UI Settings
  LOADING_MESSAGES: {
    BEACON_SCAN: 'Scanning for nearby networks... This may take 30 seconds.',
    SSL_SCAN: 'Checking SSL certificates and secure connections...',
    CONNECTING: 'Connecting to API server...'
  },
  
  // Error Messages
  ERROR_MESSAGES: {
    API_DISCONNECTED: 'Cannot connect to API server. Please ensure the backend server is running on http://localhost:8000',
    BEACON_SCAN_FAILED: 'Network scan failed. This feature requires Linux with monitor mode support.',
    SSL_SCAN_FAILED: 'SSL certificate check failed.',
    WINDOWS_LIMITATION: 'Beacon frame scanning is not supported on Windows. Please use a Linux system for full network scanning capabilities.'
  }
}

export default config
