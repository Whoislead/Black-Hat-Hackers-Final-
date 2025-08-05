<template>
  <div class="scan">
    <img class="untitled-design-1" alt="" src="/images/Untitled design 1.png">
    <img class="spy-img" alt="Spy Art" src="/images/spyvsspy 1.png" />

    <div class="scan-header">
      <button 
        class="scan-btn" 
        @click="checkSecureConnection"
        :disabled="isScanning"
      >
        {{ sslScanning ? 'Checking SSL...' : 'Check secure connection' }}
      </button>
      <button 
        class="scan-btn" 
        @click="scanNearbyNetworks"
        :disabled="isScanning"
      >
        {{ beaconScanning ? 'Scanning...' : 'Scan nearby networks' }}
      </button>
    </div>

    <!-- Loading indicator -->
    <div v-if="isScanning" class="loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">{{ loadingMessage }}</p>
    </div>

    <!-- Error message -->
    <div v-if="errorMessage" class="error-container">
      <p class="error-text">{{ errorMessage }}</p>
      <button class="retry-btn" @click="clearError">Dismiss</button>
    </div>

    <!-- Connection status -->
    <div class="status-container">
      <div class="connection-status" :class="{ 'connected': apiConnected, 'disconnected': !apiConnected }">
        <span class="status-indicator"></span>
        {{ apiConnected ? 'API Connected' : 'API Disconnected' }}
      </div>
    </div>

    <h1 class="network-info">Network Information</h1>
    <div class="network-table-container">
      <table class="network-table">
        <thead>
          <tr>
            <th>SSID</th>
            <th>BSSID</th>
            <th>CHANNEL</th>
            <th>CHANNEL FREQUENCY</th>
            <th>DOMAIN CERTIFICATE</th>
            <th>MAC VENDOR</th>
            <th>TAG SPECIFIC VENDOR</th>
            <th>LOCATION</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="network in networks" :key="network.id || network.bssid">
            <td>{{ network.ssid }}</td>
            <td>{{ network.bssid }}</td>
            <td>{{ network.channel }}</td>
            <td>{{ network.frequency }}</td>
            <td>{{ network.certificate }}</td>
            <td>{{ network.vendor }}</td>
            <td>{{ network.tagVendor }}</td>
            <td>{{ network.location }}</td>
          </tr>
          <tr v-if="networks.length === 0 && !isScanning">
            <td colspan="8">No networks scanned yet. Click a scan button to start.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <Navbar />
  </div>
</template>

<script>
import Navbar from '../components/Navbar.vue'
import ApiService from '../services/api.js'

export default {
  name: 'Scan',
  components: {
    Navbar
  },
  data() {
    return {
      networks: [],
      isScanning: false,
      beaconScanning: false,
      sslScanning: false,
      errorMessage: '',
      loadingMessage: '',
      apiConnected: false,
      scanResults: null
    }
  },
  async mounted() {
    // Check API connection on component mount
    await this.checkApiConnection()
  },
  methods: {
    async checkApiConnection() {
      try {
        this.apiConnected = await ApiService.checkConnection()
        if (!this.apiConnected) {
          this.errorMessage = 'Cannot connect to API server. Please ensure the backend server is running on http://localhost:8000'
        }
      } catch (error) {
        this.apiConnected = false
        this.errorMessage = 'Failed to connect to API server'
      }
    },

    async checkSecureConnection() {
      if (!this.apiConnected) {
        this.errorMessage = 'API server not connected. Please check if the backend server is running.'
        return
      }

      this.sslScanning = true
      this.isScanning = true
      this.loadingMessage = 'Checking SSL certificates and secure connections...'
      this.clearError()

      try {
        // Start with SSL scan
        const sslResult = await ApiService.scanSSL({
          auto: true,
          interface: 'Wi-Fi',
          timeout: 5
        })

        console.log('SSL Scan Result:', sslResult)

        // Create network entry based on SSL result
        const networkEntry = {
          id: Date.now(),
          ssid: 'Current Connection',
          bssid: 'Detecting...',
          channel: 'Auto',
          frequency: 'Detecting...',
          certificate: sslResult.status === 'safe' ? 'Valid' : 'Invalid',
          vendor: 'Detecting...',
          tagVendor: 'Analyzing...',
          location: 'Current'
        }

        // Try to get additional beacon frame data if available
        try {
          const beaconResults = await ApiService.getBeaconResults()
          if (beaconResults.access_points && beaconResults.access_points.length > 0) {
            const currentAP = beaconResults.access_points[0]
            networkEntry.bssid = currentAP.bssid || 'Unknown'
            networkEntry.ssid = currentAP.SSID || networkEntry.ssid
            networkEntry.channel = currentAP.Channel || networkEntry.channel
            networkEntry.frequency = currentAP['Channel Frequency'] ? `${currentAP['Channel Frequency']} MHz` : networkEntry.frequency
            networkEntry.vendor = currentAP['Vendor (MAC Lookup)'] || networkEntry.vendor
            networkEntry.tagVendor = currentAP['Vendor Tags (Broadcast)']?.join(', ') || networkEntry.tagVendor
          }
        } catch (beaconError) {
          console.log('No beacon data available:', beaconError.message)
        }

        this.networks = [networkEntry]
        this.loadingMessage = `SSL Check Complete: ${sslResult.status.toUpperCase()}`

      } catch (error) {
        console.error('SSL scan error:', error)
        this.errorMessage = `SSL scan failed: ${error.message}`
      } finally {
        this.sslScanning = false
        this.isScanning = false
      }
    },

    async scanNearbyNetworks() {
      if (!this.apiConnected) {
        this.errorMessage = 'API server not connected. Please check if the backend server is running.'
        return
      }

      this.beaconScanning = true
      this.isScanning = true
      this.loadingMessage = 'Scanning for nearby networks... This may take 30 seconds.'
      this.clearError()

      try {
        // Clear previous results
        await ApiService.clearBeaconResults()

        // Start beacon frame scan
        const scanResult = await ApiService.scanBeaconFrames('wlan0', 30)
        
        console.log('Beacon Scan Result:', scanResult)

        if (scanResult.aps_detected === 0) {
          this.errorMessage = 'No access points detected. This feature requires Linux with monitor mode support, or the network interface may need to be configured.'
          this.networks = []
          return
        }

        // Process the scan results
        const processedNetworks = []
        
        for (const ap of scanResult.access_points) {
          try {
            // Get additional vendor information if MAC lookup failed
            let vendor = ap['Vendor (MAC Lookup)'] || 'Unknown'
            let certificate = 'Unknown'
            let location = 'Unknown'

            // Try to get vendor info if not already available
            if (vendor === 'Unknown Vendor' && ap.bssid) {
              try {
                const macResult = await ApiService.lookupMACVendor(ap.bssid)
                vendor = macResult.vendor || vendor
              } catch (macError) {
                console.log('MAC lookup failed for', ap.bssid)
              }
            }

            // Try to get location info from Wigle if SSID is available
            if (ap.SSID) {
              try {
                const wigleResult = await ApiService.lookupWigle({ 
                  bssid: ap.bssid, 
                  ssid: ap.SSID 
                })
                if (wigleResult.found && wigleResult.results.length > 0) {
                  const locationData = wigleResult.results[0]
                  if (locationData.city || locationData.region) {
                    location = `${locationData.city || 'Unknown'}, ${locationData.region || 'Unknown'}`
                  }
                }
              } catch (wigleError) {
                console.log('Wigle lookup failed for', ap.SSID)
              }
            }

            const networkEntry = {
              id: ap.bssid,
              ssid: ap.SSID || 'Hidden Network',
              bssid: ap.bssid,
              channel: ap.Channel || 'Unknown',
              frequency: ap['Channel Frequency'] ? `${ap['Channel Frequency']} MHz` : 'Unknown',
              certificate: certificate,
              vendor: vendor,
              tagVendor: ap['Vendor Tags (Broadcast)']?.join(', ') || 'None',
              location: location
            }

            processedNetworks.push(networkEntry)
          } catch (processingError) {
            console.error('Error processing network:', processingError)
          }
        }

        this.networks = processedNetworks
        this.loadingMessage = `Scan complete! Found ${scanResult.aps_detected} access points.`

      } catch (error) {
        console.error('Beacon scan error:', error)
        if (error.message.includes('not supported on Windows')) {
          this.errorMessage = 'Beacon frame scanning is not supported on Windows. Please use a Linux system for full network scanning capabilities.'
        } else {
          this.errorMessage = `Network scan failed: ${error.message}`
        }
      } finally {
        this.beaconScanning = false
        this.isScanning = false
      }
    },

    clearError() {
      this.errorMessage = ''
    }
  }
}
</script>

<style scoped>
.scan {
  width: 100vw;
  min-height: 100vh;
  background-color: #000dbf;
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 2rem 1rem 4rem 1rem;
  box-sizing: border-box;
  position: relative;
}

.untitled-design-1 {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 100px;
  height: 120px;
  object-fit: cover;
  z-index: 1;
  opacity: 0.7;
}

.spy-img {
  position: absolute;
  bottom: 80px;
  left: 10px;
  height: 150px;
  width: auto;
  object-fit: contain;
  z-index: 1;
  opacity: 0.6;
}

.scan-header {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  width: 100%;
  max-width: 600px;
  margin: 2rem 0 2rem 0;
  z-index: 2;
}

.scan-btn {
  background-color: #fff;
  color: #000dbf;
  border: none;
  padding: 1rem 2.5rem;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  transition: background 0.2s, color 0.2s, transform 0.1s;
  min-width: 220px;
}

.scan-btn:hover:not(:disabled),
.scan-btn:active:not(:disabled) {
  background-color: #e6e6e6;
  color: #003bbf;
  transform: translateY(-2px) scale(1.03);
}

.scan-btn:disabled {
  background-color: #cccccc;
  color: #666666;
  cursor: not-allowed;
  transform: none;
}

/* Loading Styles */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 1rem 0;
  z-index: 2;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top: 3px solid #fff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  font-size: 1.1rem;
  color: #fff;
  text-align: center;
  margin: 0;
}

/* Error Styles */
.error-container {
  background-color: rgba(255, 0, 0, 0.1);
  border: 1px solid #ff4444;
  border-radius: 8px;
  padding: 1rem;
  margin: 1rem 0;
  width: 100%;
  max-width: 600px;
  text-align: center;
  z-index: 2;
}

.error-text {
  color: #ff6666;
  font-size: 1rem;
  margin: 0 0 0.5rem 0;
}

.retry-btn {
  background-color: #ff4444;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.retry-btn:hover {
  background-color: #ff6666;
}

/* Status Styles */
.status-container {
  margin: 1rem 0;
  z-index: 2;
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.connection-status.connected {
  background-color: rgba(0, 255, 0, 0.1);
  color: #66ff66;
  border: 1px solid #00ff00;
}

.connection-status.disconnected {
  background-color: rgba(255, 0, 0, 0.1);
  color: #ff6666;
  border: 1px solid #ff0000;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.connected .status-indicator {
  background-color: #00ff00;
  animation: pulse 2s infinite;
}

.disconnected .status-indicator {
  background-color: #ff0000;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

.network-info {
  font-size: 2.2rem;
  color: #fff;
  margin-bottom: 1.2rem;
  text-align: center;
  font-family: 'Jost', sans-serif;
  letter-spacing: 0.04em;
}

.network-table-container {
  width: 100%;
  display: flex;
  justify-content: center;
  z-index: 2;
}

.network-table {
  width: 95%;
  max-width: 1200px;
  border-collapse: collapse;
  background: rgba(255,255,255,0.08);
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 2rem;
  backdrop-filter: blur(5px);
}

.network-table th, .network-table td {
  padding: 0.9rem 1.1rem;
  text-align: center;
  font-size: 1rem;
  color: #fff;
}

.network-table th {
  background: rgba(0,0,0,0.18);
  font-weight: 600;
  letter-spacing: 0.03em;
}

.network-table tr:nth-child(even) {
  background: rgba(255,255,255,0.04);
}

.network-table tr:nth-child(odd) {
  background: rgba(0,0,0,0.04);
}

/* Responsive Design */
@media (max-width: 768px) {
  .scan-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .scan-btn {
    min-width: 200px;
  }
  
  .network-table {
    font-size: 0.8rem;
  }
  
  .network-table th, .network-table td {
    padding: 0.6rem 0.8rem;
  }
}
</style>
