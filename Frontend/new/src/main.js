import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from './views/Home.vue'
import About from './views/About.vue'
import Account from './views/Account.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Scan from './views/Scan.vue'
import PreviousScans from './views/PreviousScans.vue'
import { authService, authState } from './stores/auth.js'
import './style.css'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/home', component: Home, meta: { requiresAuth: true } },
  { path: '/about', component: About, meta: { requiresAuth: true } },
  { path: '/account', component: Account, meta: { requiresAuth: true } },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/scan', component: Scan, meta: { requiresAuth: true } },
  { path: '/previous-scans', component: PreviousScans, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Route guard for authentication
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  
  if (requiresAuth && !authState.isAuthenticated) {
    // Redirect to login if route requires authentication and user is not authenticated
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && authState.isAuthenticated) {
    // Redirect to home if user is already authenticated and trying to access login/register
    next('/home')
  } else {
    next()
  }
})

// Initialize authentication state from localStorage
authService.initAuth()

const app = createApp(App)
app.use(router)
app.mount('#app')
