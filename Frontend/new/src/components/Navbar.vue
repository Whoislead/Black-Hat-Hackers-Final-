<template>
  <nav class="nav-bar" v-if="isAuthenticated">
    <router-link to="/home" class="nav-btn">Home</router-link>
    <router-link to="/account" class="nav-btn">Account</router-link>
    <router-link to="/scan" class="nav-btn">Scan</router-link>
    <router-link to="/previous-scans" class="nav-btn">Previous Scans</router-link>
    <router-link to="/about" class="nav-btn">About</router-link>
    <button @click="handleLogout" class="nav-btn logout-btn">Logout</button>
  </nav>
</template>

<script>
import { authService, authState } from '../stores/auth.js'

export default {
  name: 'Navbar',
  computed: {
    isAuthenticated() {
      return authState.isAuthenticated
    },
    currentUser() {
      return authState.user
    }
  },
  methods: {
    handleLogout() {
      if (confirm('Are you sure you want to logout?')) {
        authService.logout()
        this.$router.push('/login')
      }
    }
  }
}
</script>

<style scoped>
.logout-btn {
  background: rgba(255, 255, 255, 0.2) !important;
  color: #ffcccb !important;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.logout-btn:hover {
  background: #ff4444 !important;
  color: white !important;
  transform: translateY(-2px) scale(1.03);
}
</style>
