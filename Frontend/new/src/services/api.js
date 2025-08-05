/**
 * API service for Evil Twin Detection backend
 * Handles all API calls to the FastAPI server
 */

import config from '../config/index.js'

class ApiService {
  constructor() {
    this.baseURL = config.API_BASE_URL
  }

  /**
   * Generic API request handler
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  /**
   * GET request
   */
  async get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  }

  /**
   * POST request
   */
  async post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  /**
   * DELETE request
   */
  async delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }

  // ==========================================
  // Beacon Frame Analysis APIs
  // ==========================================

  /**
   * Scan for beacon frames
   * @param {string} interface - Network interface (e.g., 'wlan0')
   * @param {number} duration - Scan duration in seconds
   */
  async scanBeaconFrames(interface = 'wlan0', duration = 30) {
    return this.post('/beacon/scan', {
      interface,
      duration
    });
  }

  /**
   * Get current beacon scan results
   */
  async getBeaconResults() {
    return this.get('/beacon/results');
  }

  /**
   * Clear beacon scan results
   */
  async clearBeaconResults() {
    return this.delete('/beacon/results');
  }

  /**
   * Get beacon scanning status
   */
  async getBeaconStatus() {
    return this.get('/beacon/status');
  }

  // ==========================================
  // SSL Certificate APIs
  // ==========================================

  /**
   * Scan SSL certificates
   * @param {string} domain - Optional domain to check
   * @param {boolean} auto - Auto-detect from traffic
   * @param {string} interface - Network interface
   * @param {number} timeout - Timeout in seconds
   */
  async scanSSL({ domain = null, auto = true, interface = 'Wi-Fi', timeout = 3 } = {}) {
    return this.post('/ssl/scan', {
      domain,
      auto,
      interface,
      timeout
    });
  }

  /**
   * Start background SSL scanning
   */
  async startSSLBackgroundScan(interface = 'Wi-Fi') {
    return this.post(`/ssl/scan/start-background?interface=${interface}`);
  }

  /**
   * Stop background SSL scanning
   */
  async stopSSLBackgroundScan() {
    return this.post('/ssl/scan/stop-background');
  }

  // ==========================================
  // MAC Address Lookup APIs
  // ==========================================

  /**
   * Look up MAC address vendor
   * @param {string} macAddress - MAC address to lookup
   */
  async lookupMACVendor(macAddress) {
    return this.post('/mac/lookup', {
      mac_address: macAddress
    });
  }

  // ==========================================
  // Wigle Database APIs
  // ==========================================

  /**
   * Look up network in Wigle database
   * @param {string} bssid - BSSID to lookup
   * @param {string} ssid - SSID to lookup
   */
  async lookupWigle({ bssid = null, ssid = null } = {}) {
    return this.post('/wigle/lookup', {
      bssid,
      ssid
    });
  }

  // ==========================================
  // Shodan APIs
  // ==========================================

  /**
   * Analyze domain with Shodan
   * @param {string} domain - Domain to analyze
   */
  async analyzeDomainWithShodan(domain) {
    return this.post('/shodan/lookup', {
      domain
    });
  }

  // ==========================================
  // System Status APIs
  // ==========================================

  /**
   * Get overall system status
   */
  async getSystemStatus() {
    return this.get('/status');
  }

  /**
   * Get system health
   */
  async getSystemHealth() {
    return this.get('/health');
  }

  /**
   * Check if API server is reachable
   */
  async checkConnection() {
    try {
      await this.get('/health');
      return true;
    } catch (error) {
      return false;
    }
  }
}

// Create and export a singleton instance
export default new ApiService();
