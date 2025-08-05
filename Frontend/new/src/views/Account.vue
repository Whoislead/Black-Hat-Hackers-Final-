<template>
  <div class="account">
    <img class="untitled-design-1" alt="" src="/images/Untitled design 1.png">
    
    <div class="account-header">
      <div class="profile-section">
        <img class="profile-icon" alt="Profile" src="/images/user-1.png">
        <div class="user-info">
          <div class="username">{{ currentUser?.username || 'Guest' }}</div>
          <div class="email-address">{{ currentUser?.email || userEmail }}</div>
          <div class="user-role">{{ currentUser?.role || 'User' }}</div>
        </div>
      </div>
    </div>

    <div class="settings-section">
      <div class="setting-item">
        <div class="setting-label">WiFi Protection</div>
        <div class="toggle-switch" :class="{ active: wifiProtection }" @click="toggleWifiProtection">
          <div class="toggle-slider"></div>
        </div>
        <div class="setting-status">{{ wifiProtection ? 'WiFi is safe' : 'WiFi protection disabled' }}</div>
      </div>

      <div class="setting-item">
        <div class="setting-label">Notifications</div>
        <div class="toggle-switch" :class="{ active: notifications }" @click="toggleNotifications">
          <div class="toggle-slider"></div>
        </div>
      </div>
    </div>

    <div class="activity-section">
      <h3 class="section-title">Activity History</h3>
      <div class="activity-list">
        <div class="activity-item" v-for="activity in activityHistory" :key="activity.id" :class="activity.type">
          <div class="activity-text">{{ activity.message }}</div>
          <div class="activity-time">{{ activity.time }}</div>
        </div>
      </div>
    </div>

    <Navbar />
  </div>
</template>

<script>
import Navbar from '../components/Navbar.vue'
import { authState } from '../stores/auth.js'

export default {
  name: 'Account',
  components: {
    Navbar
  },
  data() {
    return {
      userEmail: 'user@example.com',
      wifiProtection: true,
      notifications: true,
      activityHistory: [
        {
          id: 1,
          message: 'Suspicious network detected',
          time: '2 hours ago',
          type: 'warning'
        },
        {
          id: 2,
          message: 'SSL certificate mismatch detected',
          time: '5 hours ago',
          type: 'error'
        },
        {
          id: 3,
          message: 'Duplicate SSID found',
          time: '1 day ago',
          type: 'warning'
        },
        {
          id: 4,
          message: 'Secure connection verified',
          time: '2 days ago',
          type: 'success'
        }
      ]
    }
  },
  computed: {
    currentUser() {
      return authState.user
    }
  },
  methods: {
    toggleWifiProtection() {
      this.wifiProtection = !this.wifiProtection;
    },
    toggleNotifications() {
      this.notifications = !this.notifications;
    }
  }
}
</script>

<style scoped>
.account {
  width: 100vw;
  min-height: 100vh;
  background-color: #000dbf;
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem 1rem 4rem 1rem;
  box-sizing: border-box;
  position: relative;
}

.untitled-design-1 {
  position: absolute;
  top: 40px;
  right: 50px;
  width: 152px;
  height: 177px;
  object-fit: cover;
  z-index: 1;
}

.account-header {
  margin-top: 2rem;
  text-align: center;
  z-index: 2;
}

.profile-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.profile-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #fff;
  padding: 10px;
}

.user-info {
  text-align: center;
}

.username {
  font-size: 1.4rem;
  font-weight: 600;
  color: #fff;
  margin-bottom: 0.5rem;
}

.email-address {
  font-size: 1rem;
  color: #ddd;
  margin-bottom: 0.3rem;
}

.user-role {
  font-size: 0.9rem;
  color: #bbb;
  text-transform: capitalize;
  background: rgba(255, 255, 255, 0.1);
  padding: 0.2rem 0.8rem;
  border-radius: 12px;
  display: inline-block;
}

.settings-section {
  margin: 3rem 0;
  width: 100%;
  max-width: 500px;
  z-index: 2;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: rgba(255,255,255,0.1);
  border-radius: 12px;
  margin-bottom: 1rem;
}

.setting-label {
  font-size: 1.1rem;
  font-weight: 500;
}

.toggle-switch {
  width: 50px;
  height: 26px;
  background: #ccc;
  border-radius: 13px;
  position: relative;
  cursor: pointer;
  transition: background 0.3s;
}

.toggle-switch.active {
  background: #4CAF50;
}

.toggle-slider {
  width: 22px;
  height: 22px;
  background: #fff;
  border-radius: 50%;
  position: absolute;
  top: 2px;
  left: 2px;
  transition: transform 0.3s;
}

.toggle-switch.active .toggle-slider {
  transform: translateX(24px);
}

.setting-status {
  font-size: 0.9rem;
  color: #ddd;
}

.activity-section {
  width: 100%;
  max-width: 600px;
  z-index: 2;
}

.section-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  text-align: center;
}

.activity-list {
  background: rgba(255,255,255,0.08);
  border-radius: 12px;
  overflow: hidden;
}

.activity-item {
  padding: 1rem;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-item.warning {
  border-left: 4px solid #ff9800;
}

.activity-item.error {
  border-left: 4px solid #f44336;
}

.activity-item.success {
  border-left: 4px solid #4caf50;
}

.activity-text {
  flex: 1;
}

.activity-time {
  font-size: 0.8rem;
  color: #ccc;
}
</style>
