import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '@/views/LandingView.vue'
import { showToast } from '../utils/toast'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingView,
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/admin',
      component: () => import('../layouts/AdminLayout.vue'), // The shared layout parent shell
      meta: { requiresAuth: true, role: 'admin' },
      children: [
        { path: 'dashboard', name: 'admin-dashboard', component: () => import('../views/admin/AdminDashboard.vue') }
      ]
    },
    {
      path: '/staff',
      component: () => import('../layouts/StaffLayout.vue'),
      meta: { requiresAuth: true, role: 'trek_staff' }, // Adjusted to match your exact DB Enum names later
      children: [
        { path: 'dashboard', name: 'staff-dashboard', component: () => import('../views/staff/StaffDashboard.vue') }
      ]
    },
    {
      path: '/trekker',
      component: () => import('../layouts/TrekkerLayout.vue'),
      meta: { requiresAuth: true, role: 'trekker' },
      children: [
        { path: 'dashboard', name: 'trekker-dashboard', component: () => import('../views/trekker/TrekkerDashboard.vue') }
      ]
    }
  ],
})

function getRoleDashboard(role) {
  switch (role) {
    case 'admin': return '/admin/dashboard'
    case 'trek_staff': return '/staff/dashboard'
    case 'trekker': return '/trekker/dashboard'
    default: return '/'
  }
}

router.beforeEach((to, from, next) => {
  // Grab tokens from memory storage layers
  const token = sessionStorage.getItem('access_token')
  const userRole = sessionStorage.getItem('user_role') // Make sure your login sets this exact variable name

  const isPublicAuthRoute = ['landing', 'login', 'register'].includes(to.name)
  if (token && isPublicAuthRoute) {
    return next(getRoleDashboard(userRole))
  }

  // Check if any parent or child route requires authentication
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  
  // Find the required role from the matched route tree
  const requiredRole = to.matched.find(record => record.meta.role)?.meta.role

  if (requiresAuth) {
    // Condition A: User is not logged in at all
    if (!token) {
      showToast('Login required', 'error')
      return next({ name: 'login' })
    }

    // Condition B: User is logged in, but their role does not match route meta clearance
    if (requiredRole && userRole !== requiredRole) {
      showToast('Access denied: Unauthorized access.', 'error')
      return next(getRoleDashboard(userRole)) // Send them back to landing safely
    }
  }

  // If they pass all checks, allow them through
  next()
})

export default router
