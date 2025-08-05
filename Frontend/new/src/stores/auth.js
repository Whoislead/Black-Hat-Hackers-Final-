// Simple authentication store using reactive Vue 3 features
import { reactive } from 'vue'

// Mock user database - in a real app, this would be handled by a backend
const mockUsers = [
  {
    id: 1,
    username: 'admin',
    password: 'admin123',
    email: 'admin@eviltwincorp.com',
    role: 'admin'
  },
  {
    id: 2,
    username: 'user',
    password: 'user123',
    email: 'user@example.com',
    role: 'user'
  },
  {
    id: 3,
    username: 'testuser',
    password: 'password',
    email: 'test@example.com',
    role: 'user'
  }
]

// Authentication state
export const authState = reactive({
  isAuthenticated: false,
  user: null,
  loading: false,
  error: null
})

// Authentication service
export const authService = {
  // Login method
  async login(username, password) {
    authState.loading = true
    authState.error = null
    
    try {
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Find user in mock database
      const user = mockUsers.find(u => 
        u.username === username && u.password === password
      )
      
      if (user) {
        // Remove password from user object for security
        const { password: _, ...userWithoutPassword } = user
        
        authState.isAuthenticated = true
        authState.user = userWithoutPassword
        
        // Store in localStorage for persistence
        localStorage.setItem('isAuthenticated', 'true')
        localStorage.setItem('user', JSON.stringify(userWithoutPassword))
        
        return { success: true, user: userWithoutPassword }
      } else {
        authState.error = 'Invalid username or password'
        return { success: false, error: 'Invalid username or password' }
      }
    } catch (error) {
      authState.error = 'Login failed. Please try again.'
      return { success: false, error: 'Login failed. Please try again.' }
    } finally {
      authState.loading = false
    }
  },

  // Register method
  async register(username, password, email) {
    authState.loading = true
    authState.error = null
    
    try {
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Check if username already exists
      const existingUser = mockUsers.find(u => u.username === username)
      if (existingUser) {
        authState.error = 'Username already exists'
        return { success: false, error: 'Username already exists' }
      }
      
      // Check if email already exists
      const existingEmail = mockUsers.find(u => u.email === email)
      if (existingEmail) {
        authState.error = 'Email already registered'
        return { success: false, error: 'Email already registered' }
      }
      
      // Create new user
      const newUser = {
        id: mockUsers.length + 1,
        username,
        password,
        email,
        role: 'user'
      }
      
      mockUsers.push(newUser)
      
      return { success: true, message: 'Registration successful. Please login.' }
    } catch (error) {
      authState.error = 'Registration failed. Please try again.'
      return { success: false, error: 'Registration failed. Please try again.' }
    } finally {
      authState.loading = false
    }
  },

  // Logout method
  logout() {
    authState.isAuthenticated = false
    authState.user = null
    authState.error = null
    
    // Clear localStorage
    localStorage.removeItem('isAuthenticated')
    localStorage.removeItem('user')
  },

  // Initialize authentication state from localStorage
  initAuth() {
    const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true'
    const user = localStorage.getItem('user')
    
    if (isAuthenticated && user) {
      authState.isAuthenticated = true
      authState.user = JSON.parse(user)
    }
  },

  // Validate form inputs
  validateLogin(username, password) {
    const errors = []
    
    if (!username.trim()) {
      errors.push('Username is required')
    }
    
    if (!password.trim()) {
      errors.push('Password is required')
    } else if (password.length < 3) {
      errors.push('Password must be at least 3 characters long')
    }
    
    return errors
  },

  validateRegister(username, password, email) {
    const errors = []
    
    if (!username.trim()) {
      errors.push('Username is required')
    } else if (username.length < 3) {
      errors.push('Username must be at least 3 characters long')
    }
    
    if (!password.trim()) {
      errors.push('Password is required')
    } else if (password.length < 6) {
      errors.push('Password must be at least 6 characters long')
    }
    
    if (!email.trim()) {
      errors.push('Email is required')
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      errors.push('Please enter a valid email address')
    }
    
    return errors
  }
}
