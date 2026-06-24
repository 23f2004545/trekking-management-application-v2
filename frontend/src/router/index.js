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
        { path: 'admin/dashboard', name: 'admin-dashboard', component: () => import('../views/admin/AdminDashboard.vue'), meta: { role: 'admin' } },
        { path: 'admin/treks', name: 'admin-treks', component: () => import('../views/admin/AdminTreks.vue'), meta: { role: 'admin' } },
        { path: 'admin/staff', name: 'admin-staff', component: () => import('../views/admin/AdminStaff.vue'), meta: { role: 'admin' } },
        { path: 'admin/trekkers', name: 'admin-trekkers', component: () => import('../views/admin/AdminTrekkers.vue'), meta: { role: 'admin' } },
        { path: 'admin/bookings', name: 'admin-bookings', component: () => import('../views/admin/AdminBookings.vue'), meta: { role: 'admin' } },
        { path: 'admin/profile', name: 'admin-profile', component: () => import('../views/admin/AdminProfile.vue'), meta: { role: 'admin' } },
        { path: 'admin/history', name: 'admin-history', component: () => import('../views/admin/AdminHistory.vue'), meta: { role: 'admin' } },
        { path: 'admin/tickets', name: 'admin-tickets', component: () => import('../views/admin/AdminTickets.vue'), meta: { role: 'admin' } },


        { path: 'trek_staff/dashboard', name: 'staff-dashboard', component: () => import('../views/staff/StaffDashboard.vue'), meta: { role: 'trek_staff' } },
        { path: 'trek_staff/profile', name: 'staff-profile', component: () => import('../views/staff/StaffProfile.vue'), meta: { role: 'trek_staff' } },
        { path: 'trek_staff/treks', name: 'staff-treks', component: () => import('../views/staff/StaffTreks.vue'), meta: { role: 'trek_staff' } },
        { path: 'trek_staff/participants', name: 'staff-participants', component: () => import('../views/staff/StaffParticipants.vue'), meta: { role: 'trek_staff' } },
        { path: 'trek_staff/history', name: 'staff-history', component: () => import('../views/staff/StaffHistory.vue'), meta: { role: 'trek_staff' } },

        { path: 'trekker/dashboard', name: 'trekker-dashboard', component: () => import('../views/trekker/TrekkerDashboard.vue'), meta: { role: 'trekker' } },
        { path: 'trekker/profile', name: 'trekker-profile', component: () => import('../views/trekker/TrekkerProfile.vue'), meta: { role: 'trekker' } },
        { path: 'trekker/treks', name: 'trekker-treks', component: () => import('../views/trekker/TrekkerTreks.vue'), meta: { role: 'trekker' } },      
        { path: 'trekker/bookings', name: 'trekker-bookings', component: () => import('../views/trekker/TrekkerBookings.vue'), meta: { role: 'trekker' } },
        { path: 'trekker/history', name: 'trekker-history', component: () => import('../views/trekker/TrekkerHistory.vue'), meta: { role: 'trekker' } }, 

        
        { path: 'trek/view/:id', name: 'trek-details', component: () => import('../views/TrekDetailView.vue'), meta: { requiresAuth: true } }
      ]
    },
    {
      path: '/:pathMatch(.*)*', // Matches anything not defined previously
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue') // Triggers the customized 404 Lost Trail view
    },
  ],
})

function getRoleDashboard(role) {
  switch (role) {
    case 'admin': return '/portal/admin/dashboard'
    case 'trek_staff': return '/portal/trek_staff/dashboard'
    case 'trekker': return '/portal/trekker/dashboard'
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
