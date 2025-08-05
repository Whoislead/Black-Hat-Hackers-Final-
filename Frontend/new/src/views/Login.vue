<template>
  <div class="login">
    <img class="background-svg" src="/images/Vector 2.svg" alt="Background" />
    <div class="login-content">
      <div class="header">
        <img class="logo" src="/images/Untitled design 1.png" alt="Logo" />
        <h1 class="title">EVIL TWIN DETECTOR</h1>
      </div>

      <form class="login-form" @submit.prevent="handleLogin">
        <!-- Error Messages -->
        <div v-if="errors.length > 0" class="error-messages">
          <div v-for="error in errors" :key="error" class="error-message">
            {{ error }}
          </div>
        </div>

        <!-- Success Message -->
        <div v-if="successMessage" class="success-message">
          {{ successMessage }}
        </div>

        <label class="input-label">
          <span>User Name</span>
          <div class="input-group" :class="{ error: fieldErrors.username }">
            <img src="/images/user-1.png" alt="user icon" class="icon" />
            <input 
              type="text" 
              v-model="username" 
              placeholder="Enter your username"
              :disabled="loading"
              @input="clearFieldError('username')"
            />
          </div>
        </label>

        <label class="input-label">
          <span>Password</span>
          <div class="input-group" :class="{ error: fieldErrors.password }">
            <img src="/images/padlock 1.png" alt="padlock icon" class="icon" />
            <input 
              type="password" 
              v-model="password" 
              placeholder="Enter your password"
              :disabled="loading"
              @input="clearFieldError('password')"
            />
          </div>
        </label>

        <div class="forget-password" @click="handleForgotPassword">Forget password?</div>

        <button type="submit" class="login-button" :disabled="loading">
          <span v-if="!loading">LOGIN</span>
          <span v-else class="loading-spinner">
            <span class="spinner"></span>
            Logging in...
          </span>
        </button>
        
        <button type="button" class="register-button" @click="goToRegister" :disabled="loading">
          REGISTER
        </button>

        <!-- Demo Credentials -->
        <div class="demo-credentials">
          <h4>Demo Credentials:</h4>
          <p><strong>Admin:</strong> admin / admin123</p>
          <p><strong>User:</strong> user / user123</p>
        </div>
      </form>
    </div>

    <img class="spy-img" src="/images/spyvsspy 1.png" alt="Spy Art" />
  </div>
</template>

<script>
import { authService, authState } from '../stores/auth.js'

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      errors: [],
      fieldErrors: {},
      successMessage: '',
      loading: false
    }
  },
  computed: {
    isAuthenticated() {
      return authState.isAuthenticated
    }
  },
  watch: {
    // Watch for authentication state changes
    isAuthenticated(newVal) {
      if (newVal) {
        this.successMessage = 'Login successful! Redirecting...'
        setTimeout(() => {
          this.$router.push('/home')
        }, 1500)
      }
    }
  },
  methods: {
    async handleLogin() {
      // Clear previous errors
      this.errors = []
      this.fieldErrors = {}
      this.successMessage = ''
      
      // Validate inputs
      const validationErrors = authService.validateLogin(this.username, this.password)
      if (validationErrors.length > 0) {
        this.errors = validationErrors
        this.highlightErrorFields(validationErrors)
        return
      }
      
      this.loading = true
      
      try {
        const result = await authService.login(this.username, this.password)
        
        if (result.success) {
          this.successMessage = 'Login successful! Welcome back!'
          // Clear form
          this.username = ''
          this.password = ''
          // Navigation will be handled by watcher
        } else {
          this.errors = [result.error]
          this.highlightErrorFields(['Invalid credentials'])
        }
      } catch (error) {
        this.errors = ['An unexpected error occurred. Please try again.']
      } finally {
        this.loading = false
      }
    },
    
    goToRegister() {
      this.$router.push('/register')
    },
    
    handleForgotPassword() {
      alert('Forgot password functionality would be implemented here.\n\nFor demo purposes, use:\nAdmin: admin/admin123\nUser: user/user123')
    },
    
    clearFieldError(field) {
      if (this.fieldErrors[field]) {
        delete this.fieldErrors[field]
      }
      // Clear general errors when user starts typing
      if (this.errors.length > 0) {
        this.errors = []
      }
    },
    
    highlightErrorFields(errors) {
      // Highlight specific fields based on error messages
      errors.forEach(error => {
        if (error.toLowerCase().includes('username')) {
          this.fieldErrors.username = true
        }
        if (error.toLowerCase().includes('password')) {
          this.fieldErrors.password = true
        }
        if (error.toLowerCase().includes('invalid') || error.toLowerCase().includes('credentials')) {
          this.fieldErrors.username = true
          this.fieldErrors.password = true
        }
      })
    },
    
    // Quick login for demo purposes
    quickLogin(username, password) {
      this.username = username
      this.password = password
      this.handleLogin()
    }
  },
  
  beforeUnmount() {
    // Clear any timeouts or intervals if needed
  }
}
</script>

<style scoped>
.login {
  background-color: #000dbf;
  color: #393dff;
  height: 100vh;
  width: 100%;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.background-svg {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  opacity: 0.4;
  z-index: 0;
  object-fit: cover;
}

.login-content {
  z-index: 1;
  background: white;
  padding: 40px;
  border-radius: 16px;
  max-width: 600px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 32px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.header {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo {
  height: 120px;
  width: auto;
  object-fit: contain;
}

.title {
  font-family: 'Jost', sans-serif;
  font-size: 32px;
  color: #1e0303;
  text-align: center;
  margin-top: 12px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-label {
  display: flex;
  flex-direction: column;
  font-weight: 500;
  color: #a3a3a3;
  font-size: 16px;
}

.input-group {
  display: flex;
  align-items: center;
  border-bottom: 3px solid #000;
  padding: 8px 0;
  transition: border-color 0.3s ease;
}

.input-group.error {
  border-bottom-color: #f44336;
}

.input-group input {
  border: none;
  outline: none;
  flex: 1;
  padding-left: 10px;
  font-size: 16px;
  background-color: transparent;
}

.input-group input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.icon {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.forget-password {
  text-align: right;
  font-weight: 500;
  font-size: 14px;
  color: #000;
  cursor: pointer;
}

.login-button, .register-button {
  background-color: #000;
  color: white;
  font-size: 20px;
  font-weight: 500;
  padding: 14px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.3s ease, opacity 0.3s ease;
  position: relative;
}

.login-button:disabled, .register-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.register-button {
  margin-top: 10px;
  background-color: #222;
}

.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #ffffff40;
  border-top: 2px solid #ffffff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-messages {
  background: #ffebee;
  border: 1px solid #f44336;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 16px;
}

.error-message {
  color: #d32f2f;
  font-size: 14px;
  margin-bottom: 4px;
}

.error-message:last-child {
  margin-bottom: 0;
}

.success-message {
  background: #e8f5e8;
  border: 1px solid #4caf50;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 16px;
  color: #2e7d32;
  font-size: 14px;
  text-align: center;
}

.demo-credentials {
  margin-top: 20px;
  padding: 15px;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  border: 1px solid #ddd;
}

.demo-credentials h4 {
  margin: 0 0 8px 0;
  color: #666;
  font-size: 14px;
}

.demo-credentials p {
  margin: 4px 0;
  font-size: 12px;
  color: #888;
}

.demo-credentials strong {
  color: #555;
}

.spy-img {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 200px;
  object-fit: contain;
  z-index: 0;
}
</style>
