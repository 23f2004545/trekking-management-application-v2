import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '@/views/LandingView.vue'
import { useAlertStore } from '@/stores/alert'



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
      path: '/portal',
      component: () => import('../layouts/DashboardLayout.vue'), // One parent layout shell for all dashboard operations
      meta: { requiresAuth: true },
      children: [
        { path: '/admin/dashboard', name: 'admin-dashboard', component: () => import('../views/admin/AdminDashboard.vue'), meta: { role: 'admin' } },
        { path: '/staff/dashboard', name: 'staff-dashboard', component: () => import('../views/staff/StaffDashboard.vue'), meta: { role: 'trek_staff' } },

        { path: '/trekker/dashboard', name: 'trekker-dashboard', component: () => import('../views/trekker/TrekkerDashboard.vue'), meta: { role: 'trekker' } },
        { path: '/trekker/profile', name: 'trekker-profile', component: () => import('../views/trekker/TrekkerProfile.vue'), meta: { role: 'trekker' } },
        { path: '/trekker/treks', name: 'trekker-treks', component: () => import('../views/trekker/TrekkerTreks.vue'), meta: { role: 'trekker' } },      
        { path: '/trekker/bookings', name: 'trekker-bookings', component: () => import('../views/trekker/TrekkerBookings.vue'), meta: { role: 'trekker' } }
      ]
    },
    {
      path: '/:pathMatch(.*)*', // Matches anything not defined previously
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue') // Triggers the customized 404 Lost Trail view
    },
    // {
    //   path: '/admin',
    //   component: () => import('../layouts/AdminLayout.vue'), // The shared layout parent shell
    //   meta: { requiresAuth: true, role: 'admin' },
    //   children: [
    //     { path: 'dashboard', name: 'admin-dashboard', component: () => import('../views/admin/AdminDashboard.vue') }
    //   ]
    // },
    // {
    //   path: '/staff',
    //   component: () => import('../layouts/StaffLayout.vue'),
    //   meta: { requiresAuth: true, role: 'trek_staff' }, // Adjusted to match your exact DB Enum names later
    //   children: [
    //     { path: 'dashboard', name: 'staff-dashboard', component: () => import('../views/staff/StaffDashboard.vue') }
    //   ]
    // },
    // {
    //   path: '/trekker',
    //   component: () => import('../layouts/TrekkerLayout.vue'),
    //   meta: { requiresAuth: true, role: 'trekker' },
    //   children: [
    //     { path: 'dashboard', name: 'trekker-dashboard', component: () => import('../views/trekker/TrekkerDashboard.vue') }
    //   ]
    // }
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
  const alertStore = useAlertStore()
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
      alertStore.showAlert('Login required', 'danger')
      return next({ name: 'login' })
    }

    // Condition B: User is logged in, but their role does not match route meta clearance
    if (requiredRole && userRole !== requiredRole) {
      alertStore.showAlert('Access denied: Unauthorized access.', 'danger')
      return next(getRoleDashboard(userRole)) // Send them back to landing safely
    }
  }

  // If they pass all checks, allow them through
  next()
})

export default router
