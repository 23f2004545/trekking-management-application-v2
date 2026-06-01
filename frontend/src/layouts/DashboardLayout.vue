<template>
  <div class="dashboard-viewport w-100 min-vh-100 d-flex flex-column">

    <header class="dashboard-header w-100 px-4 py-2 mt-3 z-index-top">
      <div class="nav-container glass-pill d-flex align-items-center justify-content-between mx-auto px-4 py-1.5 shadow-sm">
        
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
          
          <button class="icon-utility-btn d-none d-lg-flex" title="View Alerts" @click="alertStore.showAlert('No active safety notifications inside your sector.', 'info')">
            <i class="bi bi-bell text-white-50" style="font-size: 1.25rem;"></i>
          </button>

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
          <button @click="handleSignOut" class="btn btn-danger w-100 rounded-pill py-2.5 fw-bold fs-6 shadow-sm">
            Sign Out <i class="bi bi-box-arrow-right ms-2"></i>
          </button>
        </li>
      </ul>
    </div>
    
    <!-- Drawer Blur Backdrop -->
    <Transition name="fade">
      <div v-if="isMobileMenuOpen" class="mobile-drawer-backdrop" @click="isMobileMenuOpen = false"></div>
    </Transition>

    <main class="workspace-area flex-grow-1 w-100 mx-auto px-md-5 pt-NAV_MARGIN mb-5">
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
import { RouterLink, useRouter } from 'vue-router'
import { computed, ref , onMounted} from 'vue'
import { useAuthStore } from '../stores/auth' 
import { useAlertStore } from '../stores/alert'
import { useConfirmStore } from '../stores/confirm'

const router = useRouter()
const authStore = useAuthStore()
const alertStore = useAlertStore()
const confirmStore = useConfirmStore()
const isMobileMenuOpen = ref(false)

// This variable will be used to offset the scrolling content below the fixed header
// const NAV_MARGIN = '100px';

const reactiveMenu = computed(() => authStore.navigationMenu)

const API_BASE = `http://127.0.0.1:5000/api/${authStore.role}` 
const profile_pic = ref('')

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
    const profileRes = await fetch(`${API_BASE}/profile`, { method: 'GET', headers })
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

onMounted(() => {
  handleProfilePic()
})

</script>

<style scoped>
/* Core Locked Viewport with Dashboard Background */
.dashboard-viewport {
  position: relative;
  overflow: hidden;
  /* Use your aesthetic, professional background image */
  background: 
    linear-gradient(rgba(20, 30, 25, 0.45), rgba(25, 35, 30, 0.25)), 
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
  z-index: 999999999;
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
  z-index: 999999998;
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

</style>