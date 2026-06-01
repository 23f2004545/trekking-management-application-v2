import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: sessionStorage.getItem('access_token') || null,
    role: sessionStorage.getItem('user_role') || null,
    userName: sessionStorage.getItem('user_name') || 'User',
    profile_pic: sessionStorage.getItem('profile_pic') || null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    
    // Dynamically provides navigation menus to the layout based on the user role
    navigationMenu(state) {
      if (!state.role) return []
      
      const menus = {
        admin: [
          { label: 'Overview', route: '/portal/admin/dashboard' },
          { label: 'Treks', route: '/portal/admin/treks' },
          { label: 'Staff', route: '/portal/admin/staff' },
          { label: 'Trekkers', route: '/portal/admin/trekkers' },
          { label: 'Bookings', route: '/portal/admin/bookings' }
        ],
        trek_staff: [
          { label: 'My Treks', route: '/portal/staff/dashboard' },
          { label: 'Registrations', route: '/portal/staff/participants' }
        ],
        trekker: [
          { label: 'Home', route: '/portal/trekker/dashboard' },
          { label: 'Treks', route: '/portal/trekker/treks' },
          { label: 'Bookings', route: '/portal/trekker/bookings' },
          { label: 'History', route: '/portal/trekker/history' },
        ]
      }
      return menus[state.role] || []
    },

    activeAvatarUrl: (state) => {

      const backendBaseUrl = import.meta.env.VITE_BACKEND_URL;

      if (state.profile_pic == "null") {
        return `${backendBaseUrl}/static/Profile_pics/${state.role}.png`
      }
      
      // CONCATENATION GATEWAY
      return `${backendBaseUrl}${state.profile_pic}`
    }
  },
  
  actions: {
    loginUser(payload) {
      this.token = payload.access_token
      this.role = payload.role
      this.userName = payload.name || 'User'
      this.profile_pic = payload.profile_pic || null

      sessionStorage.setItem('access_token', payload.access_token)
      sessionStorage.setItem('user_role', payload.role)
      sessionStorage.setItem('user_name', this.userName)
      sessionStorage.setItem('profile_pic', this.profile_pic)
    },
    updateLocalAvatar(newRelativeKey) {
      this.profile_pic = newRelativeKey
      sessionStorage.setItem('profile_pic', newRelativeKey)
    },
    logoutUser() {
      this.token = null
      this.role = null
      this.userName = 'User'
      this.profile_pic = null
      sessionStorage.clear()
      localStorage.removeItem('refresh_token')
    }
  }
})