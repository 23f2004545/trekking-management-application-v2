<template>
  <div class="dashboard-viewport w-100 min-vh-100 d-flex flex-column">

    <DemoWelcomeModal ref="demoWelcomeModalRef" />

    <!-- FLOATING NAVIGATION ISLAND (Docked when scrolling down) -->
    <Transition name="slide-down-fade">
      <div v-if="isScrolled" class="apex-floating-hud position-fixed start-50 translate-middle-x z-index-top d-flex align-items-center justify-content-between gap-3 px-4 py-2 rounded-pill shadow-lg border border-white border-opacity-15">
        
        <!-- Logo / Brand link -->
        <router-link to="/" class="d-flex align-items-center flex-shrink-0" title="Return to Peak Overview">
          <img src="@/assets/logo.png" alt="Apex Logo" class="floating-logo-img" />
        </router-link>

        <!-- Desktop Nav Links (Compact) -->
        <nav class="d-none d-lg-flex align-items-center gap-2">
          <router-link 
            v-for="item in reactiveMenu" 
            :key="'hud-'+item.label" 
            :to="item.route" 
            class="floating-nav-link px-2 py-1 rounded-pill extra-small fw-medium text-decoration-none"
            active-class="active"
          >
            {{ item.label }}
          </router-link>
        </nav>

        <!-- Cluster: Quick Scroll-To-Top + Mobile Drawer Toggle -->
        <div class="d-flex align-items-center gap-2">
          <button @click="scrollToTop" class="btn-floating-action" title="Scroll to Top">
            <i class="bi bi-arrow-up-short fs-6"></i>
          </button>

          <button class="btn-floating-action d-lg-none" @click="isMobileMenuOpen = true" title="Open Navigation Menu">
            <i class="bi bi-list fs-6"></i>
          </button>
        </div>

      </div>
    </Transition>

    <header class="dashboard-header w-100 px-4 py-2 mt-3 z-index-top">
      <div class="nav-container glass-pill d-flex align-items-center justify-content-between mx-auto px-3 py-1 shadow-sm">
        
        <router-link to="/" class="brand-logo d-flex align-items-center">
          <img src="@/assets/logo.png" alt="Apex Logo" class="apex-brand-img"/>
        </router-link>
        
        <!-- DESKTOP NAV ARRAY (Hidden on Mobile) -->
        <nav class="center-links-array d-none d-lg-block">
          <ul class="navbar-nav d-flex flex-row align-items-center gap-1.5 m-0 p-0">
            <li v-for="item in reactiveMenu" :key="item.label" class="nav-item mx-1">
              <router-link :to="item.route" class="nav-link glass-link px-1.5 py-1 fw-medium fs-6" active-class="active">
                {{ item.label }}
              </router-link>
            </li>
          </ul>
        </nav>

        <!-- ACTION CLUSTER  -->
        <div class="action-icon-cluster d-flex align-items-center gap-3">
          
          <div class="notification-wrapper position-relative">
            <button class="icon-utility-btn position-relative " title="View Alerts" @click="toggleNotifications">
              <i class="bi bi-bell text-white-50" style="font-size: 1.3rem;"></i>
              <span v-if="unreadCount > 0" class="translate-middle p-1 bg-danger border border-dark rounded-circle" style="width: 10px; height: 10px; position:absolute; top:17px; left:23px;"></span>
            </button>
            
            <div v-if="showNotifications" @click.self="showNotifications = false" class="position-fixed top-0 start-0 w-100 h-100" style="z-index: 1040;"></div>

            <Transition name="fade-slide">
              <div v-if="showNotifications" class="notif-dropdown-glass position-absolute end-0 mt-3 rounded-4 shadow-lg border border-white border-opacity-15 overflow-hidden" >
                
                <div class="d-flex align-items-center justify-content-between p-3 border-bottom border-white border-opacity-10 bg-black bg-opacity-25">
                  <h6 class="m-0 fw-bold tracking-tight text-white">System Alerts</h6>
                  <button v-if="notifications.length > 0" @click="clearAllNotifications" class="btn btn-sm btn-link text-white-50 text-decoration-none p-0 fs-9">Clear All</button>
                </div>

                <div class="notif-list-scroll">
                  <div v-if="notifications.length === 0" class="p-4 text-center text-white-50 opacity-75 fs-9 italic">
                    System telemetry is quiet. No active alerts.
                  </div>
                  
                  <div v-else class="d-flex flex-column">
                    <div v-for="notif in notifications" :key="notif.id" 
                        class="notif-item p-3 border-bottom border-white border-opacity-5 d-flex align-items-start justify-content-between gap-3"
                        :class="{ 'bg-opacity-5': !notif.is_read }"
                        @mouseenter="markAsRead(notif)">
                      
                      <div class="d-flex align-items-start gap-2 w-100">
                        <div class="status-indicator mt-1 rounded-circle flex-shrink-0" :class="`bg-${notif.type}`"></div>
                        <div>
                          <p class="m-0 fs-8 lh-sm" :class="notif.is_read ? 'text-white-50' : 'text-white fw-semibold'">{{ notif.message }}</p>
                          <span class="fs-9 text-white-50 opacity-50">{{ notif.created_at }}</span>
                        </div>
                      </div>
                      
                      <button @click.stop="deleteNotification(notif.id)" class="btn-close-notif text-white-50 opacity-50 border-0 bg-transparent p-0">✕</button>
                    </div>
                  </div>
                </div>

              </div>
            </Transition>
          </div>

          <!-- Avatar (Always visible on mobile & desktop) -->
          <div @click="$router.push(`/portal/${authStore.role}/profile`)" class="avatar-capsule-wrapper d-flex align-items-center cursor-pointer" title="My Profile Settings">
            <img :src="authStore.activeAvatarUrl" alt="Profile" class="nav-avatar-img" />
          </div>

          <button class="icon-utility-btn d-none d-lg-flex" @click="confirmStore.ask('Are you ready to break camp and sign out of your current tracking session?', handleSignOut)" title="Sign Out Session">
            <i class="bi bi-box-arrow-right text-danger-tint" style="font-size: 1.25rem;"></i>
          </button>

          <!-- MOBILE HAMBURGER ICON -->
          <button class="icon-utility-btn d-lg-none border-0 bg-transparent p-0" @click="isMobileMenuOpen = true">
            <i class="bi bi-list text-white" style="font-size: 1.8rem;"></i>
          </button>
        </div>

      </div>
    </header>

    <!-- ===================================================================
         MOBILE SIDE DRAWER MODAL
         =================================================================== -->
    <div class="mobile-side-drawer" :class="{ 'open': isMobileMenuOpen }">
      <div class="d-flex justify-content-end p-4 pb-2">
        <button class="btn-close-drawer" @click="isMobileMenuOpen = false">✕</button>
      </div>
      
      <ul class="mobile-nav-list d-flex flex-column gap-3 px-4 m-0 list-unstyled text-start mt-2">
        <li v-for="item in reactiveMenu" :key="item.label" @click="isMobileMenuOpen = false">
          <router-link :to="item.route" class="mobile-nav-link text-white text-decoration-none fw-semibold tracking-tight" active-class="text-success">
            {{ item.label }}
          </router-link>
        </li>
        <li class="mt-4 pt-4 border-top border-white border-opacity-10">
          <button @click="confirmStore.ask('Are you ready to break camp and sign out of your current tracking session?', handleSignOut)" class="btn btn-danger w-100 rounded-pill py-2.5 fw-bold fs-6 shadow-sm">
            Sign Out <i class="bi bi-box-arrow-right ms-2"></i>
          </button>
        </li>

        <!-- MOBILE QUICK DEMO ROLE SWITCHER -->
        <li v-if="authStore.isDemo" class="mt-3 pt-3 border-top border-white border-opacity-10 text-start">
          <div class="d-flex align-items-center justify-content-between mb-2">
            <span class="text-info extra-small text-uppercase tracking-wider fw-semibold">Instant Demo Switch</span>
            <button @click="demoWelcomeModalRef?.openModal(); isMobileMenuOpen = false" class="btn btn-link text-warning p-0 extra-small text-decoration-none">
              <i class="bi bi-info-circle me-1"></i>Info
            </button>
          </div>
          <div class="d-flex flex-column gap-2">
            <button 
              type="button"
              @click="handleQuickSwitch('admin')" 
              :disabled="isSwitchingRole"
              class="btn btn-sm d-flex align-items-center justify-content-between px-3 py-2 rounded-pill w-100"
              :class="authStore.role === 'admin' ? 'btn-danger text-white fw-bold shadow-sm' : 'btn-outline-danger'"
            >
              <div class="d-flex align-items-center gap-2">
                <i class="bi bi-shield-lock-fill"></i>
                <span>Admin</span>
              </div>
              <span v-if="authStore.role === 'admin'" class="badge bg-white text-danger rounded-pill extra-small">Active</span>
            </button>

            <button 
              type="button"
              @click="handleQuickSwitch('trek_staff')" 
              :disabled="isSwitchingRole"
              class="btn btn-sm d-flex align-items-center justify-content-between px-3 py-2 rounded-pill w-100"
              :class="authStore.role === 'trek_staff' ? 'btn-warning text-dark fw-bold shadow-sm' : 'btn-outline-warning'"
            >
              <div class="d-flex align-items-center gap-2">
                <i class="bi bi-compass-fill"></i>
                <span>Staff</span>
              </div>
              <span v-if="authStore.role === 'trek_staff'" class="badge bg-dark text-warning rounded-pill extra-small">Active</span>
            </button>

            <button 
              type="button"
              @click="handleQuickSwitch('trekker')" 
              :disabled="isSwitchingRole"
              class="btn btn-sm d-flex align-items-center justify-content-between px-3 py-2 rounded-pill w-100"
              :class="authStore.role === 'trekker' ? 'btn-success text-dark fw-bold shadow-sm' : 'btn-outline-success'"
            >
              <div class="d-flex align-items-center gap-2">
                <i class="bi bi-person-fill-gear"></i>
                <span>Trekker</span>
              </div>
              <span v-if="authStore.role === 'trekker'" class="badge bg-dark text-success rounded-pill extra-small">Active</span>
            </button>
          </div>
        </li>
      </ul>
    </div>
    
    <!-- Drawer Blur Backdrop -->
    <Transition name="fade">
      <div v-if="isMobileMenuOpen" class="mobile-drawer-backdrop" @click="isMobileMenuOpen = false"></div>
    </Transition>

    <button v-if="authStore.role != 'admin'" @click="ticketModalActive = true" class="btn btn-warning rounded-circle position-fixed bottom-0 end-0 m-4 shadow-lg d-flex align-items-center justify-content-center" style="width: 56px; height: 56px; z-index: 998;">
      <i class="bi bi-headset fs-4"></i>
    </button>

    <Transition name="modal-fade">
      <div v-if="ticketModalActive" @click.self="ticketModalActive = false" class="query-overlay-backdrop d-flex align-items-center justify-content-center p-3" style="z-index: 1050;">
        <div class="glass-query-card p-4 p-md-5 rounded-4 border border-white border-opacity-15 shadow-lg text-start position-relative" style="max-width: 500px; width: 100%;">
          
          <button @click="ticketModalActive = false" class="btn-dismiss-circle-cross">✕</button>
          
          <h4 class="fw-bold text-white mb-1"><i class="bi bi-headset me-2 text-warning"></i> Command Dispatch</h4>
          
          <div v-if="activeTicket" class="mt-4">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <span class="badge bg-warning bg-opacity-10 text-warning border border-warning border-opacity-25 px-3 py-2 rounded-pill"><span class="spinner-grow spinner-grow-sm me-2" style="width: 0.5rem; height: 0.5rem;"></span>PENDING REVIEW</span>
              <span class="fs-9 text-white-50">{{ activeTicket.date }}</span>
            </div>
            
            <div class="bg-black bg-opacity-25 p-3 rounded-4 border border-white border-opacity-10 mb-4">
              <h6 class="fw-bold text-white mb-2">{{ activeTicket.subject }}</h6>
              <p class="fs-9 text-white-50 m-0 lh-base">{{ activeTicket.message }}</p>
            </div>
            
            <p class="text-white-50 fs-9 text-center mb-4">You may only maintain one active dispatch at a time. Awaiting administrative clearance.</p>
            
            <button @click="withdrawTicket(activeTicket.id)" class="btn btn-outline-danger w-100 rounded-pill py-2.5 fw-bold fs-8">Withdraw / Cancel Dispatch</button>
          </div>

          <div v-else>
            <p class="text-white-50 small mb-4">Request administrative override or ask operational queries.</p>
            <form @submit.prevent="submitTicket" class="d-flex flex-column gap-3">
              <div>
                <label class="modal-input-label">Priority Level</label>
                <div class="modal-input-wrapper">
                  <select v-model="ticketForm.priority" class="modal-clean-field w-100 bg-transparent select-fix text-white">
                    <option value="Routine" class="bg-dark">Routine Query</option>
                    <option value="Urgent" class="bg-dark ">Urgent Modification</option>
                    <option value="Hazard" class="bg-dark ">Field Hazard / SOS</option>
                  </select>
                </div>
              </div>
              <div>
                <label class="modal-input-label">Subject Vector</label>
                <div class="modal-input-wrapper"><input v-model="ticketForm.subject" type="text" required class="modal-clean-field w-100" placeholder="e.g. Trail Blockage / Roster Issue"></div>
              </div>
              <div>
                <label class="modal-input-label">Operational Details</label>
                <div class="modal-input-wrapper"><textarea v-model="ticketForm.message" required rows="4" class="modal-clean-field w-100 text-area-fix" placeholder="Describe the hazard or query..."></textarea></div>
              </div>
              <button type="submit" class="btn btn-warning w-100 rounded-pill py-2.5 fw-bold text-dark mt-2 shadow-sm">Transmit to Command</button>
            </form>
          </div>

        </div>
      </div>
    </Transition>

    <main class="workspace-area flex-grow-1 w-100 mx-auto px-md-5 pt-NAV_MARGIN mb-5">
      <!-- DEMO MODE NOTICE BANNER & QUICK ROLE SWITCHER -->

      <div v-if="authStore.isDemo && route.meta.showDemoSwitcher" class="demo-mode-alert mb-2 mx-4">
        <div class="px-3 py-2 px-sm-4 py-sm-2 d-flex flex-column flex-sm-row align-items-center justify-content-between gap-3 border border-warning border-opacity-30 rounded-4 shadow-sm" style="background: rgba(255, 193, 7, 0.08); backdrop-filter: blur(8px);">
          
          
          <div class="d-flex flex-column flex-sm-row align-items-center gap-2 text-center text-sm-start">
            <div>
              <span class="badge bg-warning text-dark fw-bold px-2 py-1 rounded-pill fs-9">
                <i class="bi bi-shield-lock-fill me-1"></i>DEMO MODE
              </span>
            </div>
            <span class="text-white-50 fs-8 px-1">
              Logged in as <strong class="text-warning text-capitalize">{{ authStore.role }}</strong> in Sandbox Simulation.
            </span>
            <button @click="demoWelcomeModalRef?.openModal()" class="btn btn-sm btn-outline-warning rounded-pill px-2 py-1 extra-small d-inline-flex align-items-center gap-1 ms-1">
                <i class="bi bi-info-circle"></i> Info
            </button>
          </div>

          <!-- Desktop Quick Demo Role Switcher -->
            <div class="d-none d-md-flex align-items-center gap-2 ms-auto">
              <span class="text-white-50 extra-small me-1">Switch:</span>
              
              <button 
                type="button"
                @click="handleQuickSwitch('admin')" 
                :disabled="isSwitchingRole"
                class="btn btn-sm d-flex align-items-center gap-1 px-2.5 py-1 rounded-pill extra-small"
                :class="authStore.role === 'admin' ? 'btn-danger text-white fw-bold shadow-sm' : 'btn-outline-danger'"
              >
                <i class="bi bi-shield-lock-fill"></i>
                <span>Admin</span>
              </button>

              <button 
                type="button"
                @click="handleQuickSwitch('trek_staff')" 
                :disabled="isSwitchingRole"
                class="btn btn-sm d-flex align-items-center gap-1 px-2.5 py-1 rounded-pill extra-small"
                :class="authStore.role === 'trek_staff' ? 'btn-warning text-dark fw-bold shadow-sm' : 'btn-outline-warning'"
              >
                <i class="bi bi-compass-fill"></i>
                <span>Staff</span>
              </button>

              <button 
                type="button"
                @click="handleQuickSwitch('trekker')" 
                :disabled="isSwitchingRole"
                class="btn btn-sm d-flex align-items-center gap-1 px-2.5 py-1 rounded-pill extra-small"
                :class="authStore.role === 'trekker' ? 'btn-success text-dark fw-bold shadow-sm' : 'btn-outline-success'"
              >
                <i class="bi bi-person-fill-gear"></i>
                <span>Trekker</span>
              </button>
            </div>

        </div>

      </div>

      <router-view />
    </main>

    <footer class="persistent-footer mt-auto px-3 px-md-5 pb-4">
      <div class="glass-footer-card container-fluid p-4 p-lg-5 rounded-4 border border-white border-opacity-10 shadow-lg text-white">
        
        <div class="row align-items-center justify-content-between pb-4 mb-4 border-bottom border-white border-opacity-10">
          <div class="col-lg-7 col-md-8 text-start mb-3 mb-md-0">
            <h3 class="fw-bold tracking-tight m-0 mb-1">Secure your spot on the next alpine expedition today.</h3>
            <p class="m-0 text-white-50 small">Spaces are highly restricted per seasonal route to preserve environmental stability and guide ratios.</p>
          </div>
          <div class="col-auto">
            <button @click="$router.push(`/portal/${authStore.role}/treks`)" class="btn-footer-cta rounded-pill px-4 py-2 fw-semibold fs-8">
              Explore Open Trails →
            </button>
          </div>
        </div>

        <div class="row text-start g-4">
          
          <div class="col-lg-4 col-md-12">
            <div class="d-flex align-items-center mb-3">
              <img src="@/assets/logo.png" alt="Apex Logo" class="footer-brand-img me-2"/>
            </div>
            <p class="text-white-50 small max-w-xs lh-base">
              Mute the digital noise. Swap infinite scrolling for pristine mountain horizons. Engineered for clean air and precise tracking.
            </p>
          </div>

          <div class="col-6 col-md-3 col-lg-2 ms-lg-auto">
            <h6 class="fw-bold small tracking-wider mb-3 text-uppercase opacity-50">Main Tracks</h6>
            <ul class="list-unstyled d-flex flex-column gap-2 fs-9">
              <li><a href="#" class="footer-link">Alpine Paths</a></li>
              <li><a href="#" class="footer-link">Forest Ridges</a></li>
              <li><a href="#" class="footer-link">Glacier Passes</a></li>
              <li><a href="#" class="footer-link">Seasonal Maps</a></li>
            </ul>
          </div>

          <div class="col-6 col-md-3 col-lg-2">
            <h6 class="fw-bold small tracking-wider mb-3 text-uppercase opacity-50">Safety Desk</h6>
            <ul class="list-unstyled d-flex flex-column gap-2 fs-9">
              <li><a href="#" class="footer-link">Gear Checklist</a></li>
              <li><a href="#" class="footer-link">Weather Monitoring</a></li>
              <li><a href="#" class="footer-link">Emergency Protocols</a></li>
              <li><a href="#" class="footer-link">Medical Clearance</a></li>
            </ul>
          </div>

          <div class="col-6 col-md-3 col-lg-2">
            <h6 class="fw-bold small tracking-wider mb-3 text-uppercase opacity-50">Portal Utility</h6>
            <ul class="list-unstyled d-flex flex-column gap-2 fs-9">
              <li><a href="#" class="footer-link">My Basecamp</a></li>
              <li><a href="#" class="footer-link">Staff Directories</a></li>
              <li><a href="#" class="footer-link">System Metrics</a></li>
              <li><a href="#" class="footer-link">Route Licensing</a></li>
            </ul>
          </div>

        </div>

        <div class="row align-items-center justify-content-between pt-4 mt-4 border-top border-white border-opacity-10 fs-9 text-white-50">
          <div class="col-auto">
            <span>© 2026 APEX APP SYSTEMS. DESIGNED FOR WILDERNESS OPERATIONS & CODES.</span>
          </div>
          <div class="col-auto d-flex gap-3 fs-7">
            <a href="#" class="text-white-50 hover-white text-decoration-none"><i class="bi bi-facebook"></i></a>
            <a href="#" class="text-white-50 hover-white text-decoration-none"><i class="bi bi-instagram"></i></a>
            <a href="#" class="text-white-50 hover-white text-decoration-none"><i class="bi bi-twitter"></i></a>
          </div>
        </div>

      </div>
    </footer>

  </div>
</template>

<script setup>
import { RouterLink, useRouter, useRoute } from 'vue-router'
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '../stores/auth' 
import { useAlertStore } from '../stores/alert'
import { useConfirmStore } from '../stores/confirm'
import { secureFetch } from '@/utils/api'
import DemoWelcomeModal from '@/components/DemoWelcomeModal.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const alertStore = useAlertStore()
const confirmStore = useConfirmStore()
const isMobileMenuOpen = ref(false)
const activeTicket = ref(null)
const ticketModalActive = ref(false)
const ticketForm = ref({ subject: '', message: '', priority: 'Routine'}) 

const demoWelcomeModalRef = ref(null)
const isScrolled = ref(false)
const isSwitchingRole = ref(false)

const activePageTitle = computed(() => {
  const current = reactiveMenu.value.find(item => item.route === route.path)
  return current ? current.label : (authStore.role || 'Portal').toUpperCase()
})

const roleBadgeTheme = computed(() => {
  if (authStore.role === 'admin') return 'bg-danger bg-opacity-20 text-white border border-danger border-opacity-30'
  if (authStore.role === 'trek_staff') return 'bg-warning bg-opacity-20 text-black border border-warning border-opacity-30'
  return 'bg-success bg-opacity-20 text-white border border-success border-opacity-30'
})

const roleDisplayName = computed(() => {
  if (authStore.role === 'admin') return 'Apex Admin'
  if (authStore.role === 'trek_staff') return 'Staff Guide'
  return 'Active Trekker'
})

function handleScroll() {
  isScrolled.value = window.scrollY > 150
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

async function handleQuickSwitch(newRole) {
  if (isSwitchingRole.value || authStore.role === newRole) return
  isSwitchingRole.value = true
  try {
    const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/auth/demo-login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role: newRole })
    })
    if (res.ok) {
      const data = await res.json()
      authStore.loginUser(data)
      isMobileMenuOpen.value = false
      alertStore.showAlert(`Switched to ${data.role} demo profile.`, 'success')
      router.push(`/portal/${data.role}/dashboard`)
    } else {
      alertStore.showAlert('Demo profile switch failed. Try again.', 'danger')
    }
  } catch (err) {
    alertStore.showAlert('Network error during demo switch.', 'danger')
  } finally {
    isSwitchingRole.value = false
  }
} 

// This variable will be used to offset the scrolling content below the fixed header
// const NAV_MARGIN = '100px';

const reactiveMenu = computed(() => authStore.navigationMenu)

const API_BASE = `http://127.0.0.1:5000/api/${authStore.role}` 
const profile_pic = ref('')

const showNotifications = ref(false)
const notifications = ref([])

// Computed property to calculate the red dot visibility
const unreadCount = computed(() => notifications.value.filter(n => !n.is_read).length)

function handleSignOut() {
  isMobileMenuOpen.value = false // close drawer if open
  authStore.logoutUser() // Pinia action cleans session keys
  router.push('/')
}

async function handleProfilePic() {
  try {
    const headers = {
      'Authorization': `Bearer ${authStore.token}`,
      'Content-Type': 'application/json'
    }

    // 1. Dispatch Core User Profile Retrieval Request
    const profileRes = await secureFetch(`${API_BASE}/profile`, { method: 'GET', headers })
    if (profileRes.ok) {
      const pData = await profileRes.json() // Debug log for profile data
      profile_pic.value = pData.profile_pic || '' // Update reactive profile picture state
    } else {
      const errorData = await profileRes.json();
      alertStore.showAlert(errorData.message || 'Could not sync user profile metrics from backend.', 'danger')
    }
  } catch (error) {
    console.error('Error fetching user profile:', error)
    alertStore.showAlert('An unexpected error occurred while fetching your profile data.', 'danger')
  }
}


function toggleNotifications() {
  showNotifications.value = !showNotifications.value
  if (showNotifications.value && notifications.value.length === 0) {
    fetchNotifications()
  }
}

async function fetchNotifications() {
  try {
    const res = await secureFetch(`${import.meta.env.VITE_BACKEND_URL}/api/utils/notifications`, {
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    if (res.ok) notifications.value = await res.json()
  } catch (err) { console.error("Notification sync failed", err) }
}

async function markAsRead(notif) {
  if (notif.is_read) return
  notif.is_read = true // Optimistic UI update
  await secureFetch(`${import.meta.env.VITE_BACKEND_URL}/api/utils/notifications/${notif.id}/read`, {
    method: 'PATCH', headers: { 'Authorization': `Bearer ${authStore.token}` }
  })
}

async function deleteNotification(id) {
  notifications.value = notifications.value.filter(n => n.id !== id) // Optimistic UI update
  await secureFetch(`${import.meta.env.VITE_BACKEND_URL}/api/utils/notifications/${id}`, {
    method: 'DELETE', headers: { 'Authorization': `Bearer ${authStore.token}` }
  })
}

async function clearAllNotifications() {
  notifications.value = [] // Optimistic UI update
  await secureFetch(`${import.meta.env.VITE_BACKEND_URL}/api/utils/notifications/clear`, {
    method: 'DELETE', headers: { 'Authorization': `Bearer ${authStore.token}` }
  })
}

async function fetchActiveTicket() {
  try {
    const res = await secureFetch(`${import.meta.env.VITE_BACKEND_URL}/api/utils/tickets`)
    if (res.ok) activeTicket.value = await res.json()
  } catch (err) { console.error(err) }
}

async function submitTicket() {
  try {
    const res = await secureFetch(`${import.meta.env.VITE_BACKEND_URL}/api/utils/tickets`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(ticketForm.value)
    })
    
    const data = await res.json()
    if (res.ok) {
      alertStore.showAlert(data.message, 'success')
      await fetchActiveTicket()
    } else {
      alertStore.showAlert(data.message, 'danger')
      ticketModalActive.value = false
    }
  } catch(err) { alertStore.showAlert('Transmission failed.', 'danger') } 
}

async function withdrawTicket(id) {
  try {
    const res = await secureFetch(`${import.meta.env.VITE_BACKEND_URL}/api/utils/tickets/${id}`, { method: 'DELETE' })
    if (res.ok) {
      alertStore.showAlert('Dispatch withdrawn successfully.', 'info')
      activeTicket.value = null // Resets UI back to the form!
      ticketForm.value = { subject: '', message: '', priority: 'Routine' } 
    }
  } catch(err) { console.error(err) }
}


onMounted(() => {
  handleProfilePic()
  fetchNotifications()
  fetchActiveTicket()
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

</script>

<style scoped>
/* Core Locked Viewport with Dashboard Background */
.dashboard-viewport {
  position: relative;
  overflow: hidden;
  /* Use your aesthetic, professional background image */
  background: 
    linear-gradient(rgba(2, 11, 7, 0.693), rgba(25, 35, 30, 0.25)), 
    url('@/assets/dashboard-bg.jpg'); 
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed; /* Crucial: background stays while content scrolls over it */
}

/* Nav Offsetting Variables */
.pt-NAV_MARGIN { padding-top: 2rem; }

/* Navbar Structural Elements */
.nav-container {
  max-width: 1300px;
  width: 95%;
}

.glass-pill {
  background: rgba(255, 255, 255, 0.25) !important;
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 50px;
  height: 4rem;
  
}

.brand-logo { text-decoration: none; }
.apex-brand-img { height: 3rem; object-fit: contain; }

/* Dynamic Navigation Links */
.glass-link {
  color: rgba(255, 255, 255, 0.9) !important;
  text-decoration: none;
  border-radius: 50px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  min-width: 6rem;
  text-align: center;
}

.glass-link.active {
  color: #ffffff !important;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}

.glass-link:hover:not(.active) {
  color: #ffffff !important;
  background: rgba(255, 255, 255, 0.1);
}

/* Sign Out Action Element */
.btn-signout-glass {
  background: rgba(220, 53, 69, 0.2);
  border: 1px solid rgba(220, 53, 69, 0.4);
  backdrop-filter: blur(8px);
  color: #ff8787;
  cursor: pointer;
  transition: all 0.25s ease;
}
.btn-signout-glass:hover {
  background: rgba(220, 53, 69, 0.4);
  border-color: rgba(220, 53, 69, 0.6);
  color: #ffffff;
}

/* Scrollable Inner Canvas */
.workspace-area {
  overflow-y: auto; /* Content scrolls vertically over the background */
  max-width: 1500px;
}

/* Aesthetic Footer Card */
.glass-footer-card {
  background: rgba(255, 255, 255, 0.05) !important;
  backdrop-filter: blur(25px) !important;
  -webkit-backdrop-filter: blur(25px) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
}

.footer-brand-img {
  height: 38px;
  object-fit: contain;
}

.btn-footer-cta {
  background: #ffffff;
  color: #0b1f15;
  border: none;
  transition: all 0.25s ease;
}
.btn-footer-cta:hover {
  background: #e8f5e9;
  transform: translateY(-1px);
}

.footer-link {
  color: rgba(255, 255, 255, 0.65);
  text-decoration: none;
  transition: color 0.2s ease;
}
.footer-link:hover {
  color: #ffffff;
}

.hover-white:hover { color: #ffffff !important; }
.max-w-xs { max-width: 280px; }
.tracking-wider { letter-spacing: 0.8px; }

/* Icon Clusters Style Elements */
.icon-utility-btn { background: transparent; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; padding: 6px; border-radius: 50%; transition: background 0.2s; }
.icon-utility-btn:hover { background: rgba(255, 255, 255, 0.1); height: 2.25rem; width:2.15rem; border-radius: 50%; transition: background 0.2s; }
.text-danger-tint { color: #ff8787; }

.nav-avatar-img { width: 34px; height: 34px; border-radius: 50%; object-fit: cover; border: 1.5px solid rgba(255, 255, 255, 0.6); transition: border-color 0.2s; }
.avatar-capsule-wrapper:hover .nav-avatar-img { border-color: #198754; }



/* Mobile Drawer Infrastructure */
.mobile-side-drawer {
  position: fixed;
  top: 0;
  right: -320px; /* Hide off-screen initially */
  width: 320px;
  max-width: 75vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(15px);
  border-left: 1px solid rgba(255, 255, 255, 0.1);
  z-index: 999 ;
  transition: right 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.mobile-side-drawer.open {
  right: 0;
}

.btn-close-drawer {
  background: rgba(255, 255, 255, 0.1);
  border: none; color: white;
  width: 36px; height: 36px;
  border-radius: 50%;
  font-size: 1.2rem;
}
.btn-close-drawer:hover { background: rgba(255, 255, 255, 0.2); }

.mobile-nav-link {
  font-size: 1.5rem;
  opacity: 0.8;
  transition: opacity 0.2s;
}
.mobile-nav-link:hover, .mobile-nav-link.text-success {
  opacity: 1;
}

.mobile-drawer-backdrop {
  position: fixed;
  top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  z-index: 998;
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }


/* Notification Dropdown Aesthetics */

.dashboard-header {
  position: relative;
  z-index: 999 !important; 
}
.notif-dropdown-glass {
  position: absolute;
  width: 340px;
  background: rgba(1, 4, 2, 0.961);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(25px);
  top: 100%;
  left: -12rem;
  right: 0;
  z-index: 9999 !important;
}

.notif-list-scroll {
  max-height: 380px;
  overflow-y: auto;
}

/* Custom Scrollbar for Dropdown */
.notif-list-scroll::-webkit-scrollbar { width: 4px; }
.notif-list-scroll::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 4px; }

.status-indicator {
  width: 8px;
  height: 8px;
}

.notif-item { transition: background-color 0.2s; }
.notif-item:hover { background-color: rgba(255, 255, 255, 0.08) !important; }

.btn-close-notif { transition: opacity 0.2s; }
.btn-close-notif:hover { opacity: 1 !important; color: #ff8787 !important; }

/* Smooth Fade & Slide Animation */
.fade-slide-enter-active, .fade-slide-leave-active { transition: all 0.2s ease; }
.fade-slide-enter-from, .fade-slide-leave-to { opacity: 0; transform: translateY(-10px); }

.query-overlay-backdrop {
  position: fixed !important; top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(0, 5, 2, 0.583) !important;
  backdrop-filter: blur(7px) !important; -webkit-backdrop-filter: blur(20px) !important;
  z-index: 999 !important;
}

.glass-query-card {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(25px) !important;
  -webkit-backdrop-filter: blur(25px) !important;
  border: 1px solid rgba(178, 183, 35, 0.922);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
  border-radius: 240px;
  width: 100%;
  max-width: 460px;
}

.btn-dismiss-circle-cross {
  position: absolute; top: 1rem; right: 0.5rem;
  background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.15);
  color: rgba(255,255,255,0.6); width: 30px; height: 30px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center; font-size: 0.9rem; cursor: pointer; transition: all 0.2s;
}
.btn-dismiss-circle-cross:hover { background: rgba(255,255,255,0.2); color: #ffffff; transform: scale(1.05); }

.modal-input-label { font-size: 0.82rem; color: rgba(255, 255, 255, 0.6); font-weight: 500; margin-bottom: 4px; }
.modal-input-wrapper { background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 8px 12px; display: flex; align-items: center; }
.modal-clean-field { border: none; background: transparent; color: #ffffff; width: 100%; font-size: 0.92rem; outline: none; }

/* ==========================================================================
   FLOATING NAVIGATION ISLAND (HUD) & DEMO ACTIONS
   ========================================================================== */
.apex-floating-hud {
  top: 1rem;
  z-index: 1030 !important;
  background: rgba(10, 18, 14, 0.88) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  max-width: 94vw;
}

.floating-logo-img {
  height: 24px;
  width: auto;
  object-fit: contain;
}

.floating-nav-link {
  color: rgba(255, 255, 255, 0.7);
  transition: all 0.2s ease;
}

.floating-nav-link:hover, .floating-nav-link.active {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.15);
}

.btn-floating-action {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #ffffff;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-floating-action:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: scale(1.05);
}

.extra-small {
  font-size: 0.75rem;
}

.slide-down-fade-enter-active, .slide-down-fade-leave-active {
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-down-fade-enter-from, .slide-down-fade-leave-to {
  opacity: 0;
  transform: translate(-50%, -15px) !important;
}

</style>