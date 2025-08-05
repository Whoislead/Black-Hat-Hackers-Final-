<template>
  <div class="register">
    <img class="register-child" alt="" src="/images/Vector 2.svg">
    <img class="untitled-design-1" alt="" src="/images/Untitled design 1.png">
    <div class="evil-twin-detector">EVIL TWIN DETECTOR</div>
    <img class="spyvsspy-1-icon" alt="" src="/images/spyvsspy 1.png">

    <form class="register-form" @submit.prevent="handleRegister">
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

      <label class="register-label" for="username">Create Username:</label>
      <input 
        class="register-input" 
        type="text" 
        id="username" 
        name="username" 
        v-model="username" 
        placeholder="Enter username (min 3 characters)"
        :disabled="loading"
        required 
      />

      <label class="register-label" for="email">Email Address:</label>
      <input 
        class="register-input" 
        type="email" 
        id="email" 
        name="email" 
        v-model="email" 
        placeholder="Enter your email"
        :disabled="loading"
        required 
      />

      <label class="register-label" for="password">Create Password:</label>
      <input 
        class="register-input" 
        type="password" 
        id="password" 
        name="password" 
        v-model="password" 
        placeholder="Enter password (min 6 characters)"
        :disabled="loading"
        required 
      />

      <button class="create-btn" type="submit" :disabled="loading">
        <span v-if="!loading">CREATE</span>
        <span v-else class="loading-spinner">
          <span class="spinner"></span>
          Creating Account...
        </span>
      </button>

      <div class="login-link">
        Already have an account? 
        <button type="button" @click="goToLogin" class="link-btn" :disabled="loading">
          Login here
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { authService } from '../stores/auth.js'

export default {
  name: 'Register',
  data() {
    return {
      username: '',
      password: '',
      email: '',
      errors: [],
      successMessage: '',
      loading: false
    }
  },
  methods: {
    async handleRegister() {
      // Clear previous errors
      this.errors = []
      this.successMessage = ''
      
      // Validate inputs
      const validationErrors = authService.validateRegister(this.username, this.password, this.email)
      if (validationErrors.length > 0) {
        this.errors = validationErrors
        return
      }
      
      this.loading = true
      
      try {
        const result = await authService.register(this.username, this.password, this.email)
        
        if (result.success) {
          this.successMessage = result.message
          // Clear form
          this.username = ''
          this.password = ''
          this.email = ''
          
          // Redirect to login after 2 seconds
          setTimeout(() => {
            this.$router.push('/login')
          }, 2000)
        } else {
          this.errors = [result.error]
        }
      } catch (error) {
        this.errors = ['An unexpected error occurred. Please try again.']
      } finally {
        this.loading = false
      }
    },
    
    goToLogin() {
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.register {
  width: 100vw;
  height: 100vh;
  min-height: 100vh;
  position: relative;
  background-color: #000dbf;
  overflow: hidden;
  text-align: left;
  font-size: 20px;
  color: #a3a3a3;
  font-family: Inter, sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
}

.register-child {
  position: absolute;
  top: 2px;
  left: 0px;
  width: 1041px;
  height: 1115px;
  mix-blend-mode: multiply;
  z-index: 0;
}

.untitled-design-1 {
  position: absolute;
  top: 159px;
  right: 50px;
  width: 152px;
  height: 177px;
  object-fit: cover;
  z-index: 1;
}

.evil-twin-detector {
  position: absolute;
  top: 80px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 64px;
  letter-spacing: 0.06em;
  font-weight: 500;
  font-family: Jost, sans-serif;
  color: #1e0303;
  display: inline-block;
  width: 924px;
  height: 85px;
  text-align: center;
  z-index: 2;
}

.spyvsspy-1-icon {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 200px;
  height: auto;
  object-fit: contain;
  z-index: 1;
}

.register-form {
  position: relative;
  z-index: 2;
  background: rgba(255,255,255,0.07);
  border-radius: 18px;
  box-shadow: 0 4px 32px rgba(0,0,0,0.08);
  padding: 3rem 2.5rem 2.5rem 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  min-width: 350px;
  max-width: 400px;
}

.register-label {
  color: #fff;
  font-size: 1.1em;
  font-weight: 500;
  margin-bottom: 0.3em;
}

.register-input {
  padding: 0.8em 1em;
  border-radius: 8px;
  border: none;
  font-size: 1em;
  margin-bottom: 0.5em;
  background: #f7f7f7;
  color: #222;
  font-family: inherit;
  outline: none;
  transition: box-shadow 0.2s;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

.register-input:focus {
  box-shadow: 0 0 0 2px #0057ff;
}

.create-btn {
  margin-top: 1.2em;
  background: #fff;
  color: #000dbf;
  border: none;
  border-radius: 8px;
  padding: 1em 0;
  font-size: 1.2em;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, color 0.2s, transform 0.1s, opacity 0.3s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  position: relative;
}

.create-btn:hover:not(:disabled),
.create-btn:focus:not(:disabled) {
  background: #e6e6e6;
  color: #003bbf;
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}

.create-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
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
  border: 2px solid #000dbf40;
  border-top: 2px solid #000dbf;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-messages {
  background: rgba(244, 67, 54, 0.1);
  border: 1px solid rgba(244, 67, 54, 0.3);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 16px;
}

.error-message {
  color: #f44336;
  font-size: 14px;
  margin-bottom: 4px;
}

.error-message:last-child {
  margin-bottom: 0;
}

.success-message {
  background: rgba(76, 175, 80, 0.1);
  border: 1px solid rgba(76, 175, 80, 0.3);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 16px;
  color: #4caf50;
  font-size: 14px;
  text-align: center;
}

.login-link {
  margin-top: 1.5rem;
  text-align: center;
  color: #fff;
  font-size: 0.9rem;
}

.link-btn {
  background: none;
  border: none;
  color: #fff;
  text-decoration: underline;
  cursor: pointer;
  font-size: 0.9rem;
  padding: 0;
  margin-left: 4px;
  transition: opacity 0.3s;
}

.link-btn:hover:not(:disabled) {
  opacity: 0.8;
}

.link-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
