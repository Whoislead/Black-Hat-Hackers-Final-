<template>
  <div class="previous-scans">
    <img class="untitled-design-1" alt="" src="/images/Untitled design 1.png">
    <img class="spy-img" alt="Spy Art" src="/images/spyvsspy 1.png" />

    <h1 class="network-info">Previous Scans</h1>

    <div class="filter-section">
      <label for="filter-column" class="filter-label">Filter by:</label>
      <select id="filter-column" class="filter-dropdown" v-model="filterColumn">
        <option value="ssid">SSID</option>
        <option value="bssid">BSSID</option>
        <option value="channel">CHANNEL</option>
        <option value="frequency">CHANNEL FREQUENCY</option>
        <option value="certificate">DOMAIN CERTIFICATE</option>
        <option value="vendor">MAC VENDOR</option>
        <option value="tagVendor">TAG SPECIFIC VENDOR</option>
        <option value="location">LOCATION</option>
        <option value="threatLevel">THREAT LEVEL</option>
      </select>
      <input type="text" class="filter-input" v-model="filterValue" placeholder="Enter filter value..." />
      <button class="scan-btn" @click="applyFilter">Filter</button>
      <button class="scan-btn clear-btn" @click="clearFilter">Clear</button>
    </div>

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
            <th>THREAT LEVEL</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="scan in filteredScans" :key="scan.id" :class="getThreatClass(scan.threatLevel)">
            <td>{{ scan.ssid }}</td>
            <td>{{ scan.bssid }}</td>
            <td>{{ scan.channel }}</td>
            <td>{{ scan.frequency }}</td>
            <td>{{ scan.certificate }}</td>
            <td>{{ scan.vendor }}</td>
            <td>{{ scan.tagVendor }}</td>
            <td>{{ scan.location }}</td>
            <td>{{ scan.threatLevel }}</td>
          </tr>
          <tr v-if="filteredScans.length === 0">
            <td colspan="9">No previous scans found.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <Navbar />
  </div>
</template>

<script>
import Navbar from '../components/Navbar.vue'

export default {
  name: 'PreviousScans',
  components: {
    Navbar
  },
  data() {
    return {
      filterColumn: 'ssid',
      filterValue: '',
      previousScans: [
        {
          id: 1,
          ssid: 'HomeNetwork',
          bssid: 'AA:BB:CC:DD:EE:FF',
          channel: '6',
          frequency: '2.437 GHz',
          certificate: 'Valid',
          vendor: 'Netgear',
          tagVendor: 'Netgear Inc',
          location: 'Home',
          threatLevel: 'Low'
        },
        {
          id: 2,
          ssid: 'SuspiciousWiFi',
          bssid: '11:22:33:44:55:66',
          channel: '11',
          frequency: '2.462 GHz',
          certificate: 'Invalid',
          vendor: 'Unknown',
          tagVendor: 'Unknown',
          location: 'Public',
          threatLevel: 'High'
        },
        {
          id: 3,
          ssid: 'OfficeWiFi',
          bssid: '99:88:77:66:55:44',
          channel: '1',
          frequency: '2.412 GHz',
          certificate: 'Valid',
          vendor: 'Cisco',
          tagVendor: 'Cisco Systems',
          location: 'Office',
          threatLevel: 'Low'
        },
        {
          id: 4,
          ssid: 'EvilTwin_HomeNetwork',
          bssid: 'AA:BB:CC:DD:EE:FE',
          channel: '6',
          frequency: '2.437 GHz',
          certificate: 'Suspicious',
          vendor: 'Generic',
          tagVendor: 'Generic Corp',
          location: 'Unknown',
          threatLevel: 'Critical'
        }
      ]
    }
  },
  computed: {
    filteredScans() {
      if (!this.filterValue) {
        return this.previousScans;
      }
      
      return this.previousScans.filter(scan => {
        const value = scan[this.filterColumn];
        return value && value.toLowerCase().includes(this.filterValue.toLowerCase());
      });
    }
  },
  methods: {
    applyFilter() {
      // Filter is automatically applied through computed property
      console.log('Filter applied:', this.filterColumn, this.filterValue);
    },
    clearFilter() {
      this.filterValue = '';
      this.filterColumn = 'ssid';
    },
    getThreatClass(threatLevel) {
      return {
        'threat-low': threatLevel === 'Low',
        'threat-medium': threatLevel === 'Medium',
        'threat-high': threatLevel === 'High',
        'threat-critical': threatLevel === 'Critical'
      };
    }
  }
}
</script>

<style scoped>
.previous-scans {
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

.network-info {
  font-size: 2.2rem;
  color: #fff;
  margin-bottom: 1.2rem;
  text-align: center;
  font-family: 'Jost', sans-serif;
  letter-spacing: 0.04em;
  z-index: 2;
}

.filter-section {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin: 2rem 0;
  flex-wrap: wrap;
  justify-content: center;
  z-index: 2;
  background: rgba(0, 0, 0, 0.1);
  padding: 1rem;
  border-radius: 12px;
  backdrop-filter: blur(5px);
}

.filter-label {
  color: #fff;
  font-weight: 500;
}

.filter-dropdown,
.filter-input {
  padding: 0.5rem;
  border-radius: 6px;
  border: none;
  background: #fff;
  color: #000;
}

.filter-dropdown {
  min-width: 150px;
}

.filter-input {
  min-width: 200px;
}

.scan-btn {
  background-color: #fff;
  color: #000dbf;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  transition: background 0.2s, color 0.2s, transform 0.1s;
}

.scan-btn:hover {
  background-color: #e6e6e6;
  color: #003bbf;
  transform: translateY(-2px) scale(1.03);
}

.clear-btn {
  background-color: #666;
  color: #fff;
}

.clear-btn:hover {
  background-color: #555;
}

.network-table-container {
  width: 100%;
  display: flex;
  justify-content: center;
  z-index: 2;
}

.network-table {
  width: 95%;
  max-width: 1400px;
  border-collapse: collapse;
  background: rgba(255,255,255,0.08);
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 2rem;
}

.network-table th,
.network-table td {
  padding: 0.9rem 0.8rem;
  text-align: center;
  font-size: 0.9rem;
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

.threat-low {
  border-left: 4px solid #4caf50;
}

.threat-medium {
  border-left: 4px solid #ff9800;
}

.threat-high {
  border-left: 4px solid #ff5722;
}

.threat-critical {
  border-left: 4px solid #f44336;
}
</style>
