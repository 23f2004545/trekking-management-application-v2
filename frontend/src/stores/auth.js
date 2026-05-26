import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: sessionStorage.getItem('access_token') || null,
    role: sessionStorage.getItem('user_role') || null,
    userName: sessionStorage.getItem('user_name') || 'Trekker'
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    
    // Dynamically provides navigation menus to the layout based on the user role
    navigationMenu(state) {
      if (!state.role) return []
      
      const menus = {
        admin: [
          { label: 'Overview', route: '/admin/dashboard' },
          { label: 'Routes', route: '/admin/routes' },
          { label: 'Staff', route: '/admin/staff' }
        ],
        trek_staff: [
          { label: 'My Treks', route: '/staff/dashboard' },
          { label: 'Registrations', route: '/staff/participants' }
        ],
        trekker: [
          { label: 'Home', route: '/trekker/dashboard' },
          { label: 'Treks', route: '/trekker/treks' },
          { label: 'Bookings', route: '/trekker/bookings' },
          { label: 'History', route: '/trekker/history' },
        ]
      }
      return menus[state.role] || []
    }
  },
  
  actions: {
    loginUser(payload) {
      this.token = payload.access_token
      this.role = payload.role
      this.userName = payload.name || 'User'
      
      sessionStorage.setItem('access_token', payload.access_token)
      sessionStorage.setItem('user_role', payload.role)
      sessionStorage.setItem('user_name', this.userName)
    },
    logoutUser() {
      this.token = null
      this.role = null
      sessionStorage.clear()
      localStorage.removeItem('refresh_token')
    }
  }
})