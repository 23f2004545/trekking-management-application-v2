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
          { label: 'Bookings', route: '/portal/admin/bookings' },
          { label: 'History', route: '/portal/admin/history' },
          { label: 'Tickets', route: '/portal/admin/tickets' },
        ],
        trek_staff: [
          { label: 'Home', route: '/portal/trek_staff/dashboard' },
          { label: 'My Treks', route: '/portal/trek_staff/treks' },
          { label: 'Trekkers', route: '/portal/trek_staff/participants' },
          { label: 'History', route: '/portal/trek_staff/history' },
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
      localStorage.setItem('refresh_token', payload.refresh_token)
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
    },
    async attemptTokenRefresh() {
    const refreshToken = localStorage.getItem('refresh_token')
    if (!refreshToken) return false

    try {
      const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/auth/refresh`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${refreshToken}` }
      })

      if (res.ok) {
        const data = await res.json()
        this.token = data.access_token
        sessionStorage.setItem('access_token', data.access_token)
        return true
      } else {
        // Refresh token expired or blacklisted. Force logout.
        this.logoutUser()
        return false
      }
    } catch (err) {
      this.logoutUser()
      return false
      }
    }
  }
})