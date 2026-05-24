<template>
  <div class="portal-viewport w-100 min-vh-100 d-flex flex-column justify-content-between p-3">
    
    <header class="container-fluid px-md-4 pt-2 mb-4">
      <div class="row align-items-center justify-content-between">
        
        <div class="col-auto col-md-3">
          <a @click.prevent="goHome" class="brand-logo" href="#">
            <div class="logo-wrapper">
              <img src="@/assets/logo.png" alt="Apex Logo" class="apex-brand-img"/>
            </div>
          </a>
        </div>
        
        <div class="col-auto col-md-6 d-flex justify-content-center">
          <nav class="navbar navbar-expand p-0 m-0 glass-pill px-4 py-2">
            <ul class="navbar-nav d-flex flex-row align-items-center gap-2">
              <li v-for="item in authStore.navigationMenu" :key="item.label" class="nav-item">
                <router-link :to="item.route" class="nav-link glass-link px-3 py-1" active-class="active">
                  {{ item.label }}
                </router-link>
              </li>
            </ul>
          </nav>
        </div>

        <div class="col-auto col-md-3 d-flex justify-content-end">
          <button @click="handleSignOut" class="btn-signout-glass" type="button">
            Sign Out
          </button>
        </div>

      </div>
    </header>

    <main class="flex-grow-1 w-100 max-width-container mx-auto px-2 px-md-4">
      <router-view />
    </main>

    <footer class="modern-footer-card text-center py-4 mt-5">
      <div class="container text-white opacity-75 small">
        <h5>Apex Wilderness Management Portal</h5>
        <p class="m-0 opacity-50">Logged in operator coordinates: {{ authStore.userName }} ({{ authStore.role }})</p>
        <p class="fs-7 mt-2 opacity-25">© 2026 APEX PORTAL SYSTEMS. ALL ROUTE CLEARANCES SECURED.</p>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useAlertStore } from '@/stores/alert'

const router = useRouter()
const authStore = useAuthStore()
const alertStore = useAlertStore()

function goHome() {
  router.push('/')
}

function handleSignOut() {
  alertStore.showAlert('Logged Out', 'warning')
  authStore.logoutUser()
  router.push('/')
}
</script>

<style scoped>
.portal-viewport {
  position: relative;
  z-index: 10;
}

.max-width-container {
  max-width: 1400px;
}

/* Glass Links and Pillars */
.glass-pill {
  background: rgba(255, 255, 255, 0.25) !important;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 50px;
}

.glass-link {
  font-size: 0.88rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.85);
  text-decoration: none;
  border-radius: 30px;
  transition: all 0.2s ease;
}

.glass-link.active {
  color: #ffffff !important;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.25);
}

/* Glass Sign Out Styling */
.btn-signout-glass {
  background: rgba(220, 53, 69, 0.15);
  border: 1px solid rgba(220, 53, 69, 0.3);
  backdrop-filter: blur(8px);
  color: #ff8787;
  padding: 8px 18px;
  border-radius: 30px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-signout-glass:hover {
  background: rgba(220, 53, 69, 0.35);
  color: #ffffff;
}

/* Modern Footer Card */
.modern-footer-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

.logo-wrapper { height: 50px; overflow: hidden; display: inline-block; }
.apex-brand-img { height: 50px; object-fit: contain; }
</style>