<template>
  <div class="staff-dashboard-canvas text-white text-start pb-5 animate-fade-in position-relative">
    
    <div v-if="!stats.is_onboarded && stats.is_loaded" class="onboarding-glass-banner p-4 rounded-4 mb-4 border border-warning border-opacity-25 d-flex flex-column flex-md-row align-items-md-center justify-content-between gap-3 animate-slide-down">
      <div class="d-flex align-items-center gap-3">
        <span class="fs-2">🛠️</span>
        <div>
          <h5 class="m-0 fw-bold text-warning tracking-tight">Profile Onboarding Required</h5>
          <p class="m-0 fs-8 text-white-50 mt-1">Your profile details are currently marked as default parameters. Please configure your operational field specifications.</p>
        </div>
      </div>
      <button @click="$router.push('/portal/trek_staff/profile')" class="btn btn-warning text-dark font-weight-bold rounded-pill px-4 py-2 fs-8 shadow-sm hover-grow">
        Complete Profile Setup →
      </button>
    </div>

    <div class="welcome-hero-section py-4 mb-4 border-bottom border-white border-opacity-10">
      <div class="row align-items-end justify-content-between g-3">
        <div class="col-lg-8">
          <span class="badge operations-badge mb-2 px-3 py-1.5 rounded-pill fs-9 fw-bold">
            <i class="bi bi-globe"></i> ACTIVE FIELD COMMAND
          </span>
          <h1 class="display-5 fw-bold tracking-tight m-0">
            Guide Operations, <span class="text-success-tint">{{ authStore.userName }}</span>
          </h1>
          <p class="lead opacity-75 m-0 mt-2 fs-8 max-w-xl">
            Monitor your assigned trail networks, track incoming expedition rosters, and manage sector capacities in real-time.
          </p>
        </div>
        
        <div class="col-lg-4 d-flex justify-content-lg-end">
          <div class="deployment-glass-alert p-3 rounded-3 border border-white border-opacity-15 d-flex align-items-center gap-3">
            <span class="fs-2">⏱️</span>
            <div class="text-start">
              <h6 class="m-0 fw-bold text-white small tracking-tight text-uppercase">Next Deployment</h6>
              <p class="m-0 fs-8 text-success fw-bold mt-1">{{ stats.next_deployment }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div :class="{ 'onboarding-blurred-zone': !stats.is_onboarded && stats.is_loaded }">
      
      <div class="row g-3 mb-5">
        <div class="col-md-4">
          <div class="metric-glass-card p-4 rounded-4 shadow-sm text-center">
            <div class="metric-icon mb-2"><i class="bi bi-map"></i></div>
            <h6 class="metric-label opacity-60 small m-0 uppercase tracking-wider mb-1">Active Assigned Routes</h6>
            <p class="metric-value display-4 fw-bold m-0 tracking-tighter">{{ stats.active_routes }}</p>
          </div>
        </div>
        
        <div class="col-md-4">
          <div class="metric-glass-card p-4 rounded-4 shadow-sm text-center border-success border-opacity-25">
            <div class="metric-icon mb-2"><i class="bi bi-people"></i></div>
            <h6 class="metric-label opacity-60 small m-0 uppercase tracking-wider mb-1">Incoming Explorers</h6>
            <p class="metric-value display-4 fw-bold m-0 text-success tracking-tighter">{{ stats.total_explorers }}</p>
          </div>
        </div>
        
        <div class="col-md-4">
          <div class="metric-glass-card p-4 rounded-4 shadow-sm text-center">
            <div class="metric-icon mb-2"><i class="bi bi-signal"></i></div>
            <h6 class="metric-label opacity-60 small m-0 uppercase tracking-wider mb-1">Sector Safety Status</h6>
            <p class="metric-value fs-3 fw-bold m-0 mt-2 text-white">ALL CLEAR</p>
          </div>
        </div>
      </div>

      <div class="roster-overview-section">
        <div class="d-flex align-items-center justify-content-between mb-3">
          <h4 class="fw-bold tracking-tight m-0">Upcoming Trail Deployments</h4>
          <button :disabled="!stats.is_onboarded" @click="$router.push('/portal/trek_staff/treks')" class="btn btn-sm btn-outline-light rounded-pill px-3 fs-9 border-opacity-25">
            Manage All Routes →
          </button>
        </div>

        <div v-if="stats.active_roster.length === 0" class="empty-state-glass p-5 text-center rounded-4 border border-white border-opacity-10">
          <span class="fs-1">🏕️</span>
          <h5 class="fw-bold mt-2 mb-1">No Active Deployments Scheduled</h5>
          <p class="m-0 text-white-50 small">Administration has not assigned any upcoming active grids to your profile.</p>
        </div>

        <div v-else class="row g-3">
          <div v-for="trek in stats.active_roster" :key="trek.trek_id" class="col-md-6">
            <div class="roster-glass-card p-4 rounded-4 border border-white border-opacity-10 d-flex flex-column justify-content-between h-100">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <div>
                  <h5 class="fw-bold m-0 tracking-tight text-white mb-1">{{ trek.name }}</h5>
                  <p class="fs-9 text-white-50 m-0">Departure: <span class="text-white">{{ trek.start_date }}</span></p>
                </div>
                <span class="badge lifecycle-tag text-uppercase fs-9" :class="trek.status.toLowerCase()">
                  ● {{ trek.status }}
                </span>
              </div>

              <div class="mt-2">
                <div class="d-flex justify-content-between fs-9 text-white-50 mb-1 fw-medium">
                  <span>Roster Saturation</span>
                  <span>{{ trek.registered_count }} / {{ trek.capacity }} Booked</span>
                </div>
                <div class="progress custom-progress-bar">
                  <div class="progress-bar bg-success" role="progressbar" :style="{ width: `${(trek.registered_count / trek.capacity) * 100}%` }"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { useAlertStore } from '../../stores/alert'

const authStore = useAuthStore()
const alertStore = useAlertStore()
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

const stats = ref({
  is_onboarded: true, // Default to true so components look normal during fast loads
  is_loaded: false,
  active_routes: 0,
  total_explorers: 0,
  next_deployment: "Calculating...",
  active_roster: []
})

async function fetchFieldOperationsData() {
  try {
    const res = await fetch(`${BACKEND_URL}/api/trek_staff/dashboard/stats`, {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    
    if (res.ok) {
      const data = await res.json()
      stats.value = { ...data, is_loaded: true }
    } else {
      alertStore.showAlert("Failed to synchronize with administration matrices.", "danger")
    }
  } catch (err) {
    alertStore.showAlert(`Network Drop: ${err.message}`, "danger")
  }
}

onMounted(() => {
  fetchFieldOperationsData()
})
</script>

<style scoped>
/* Core Custom Styles added to your setup */
.onboarding-glass-banner {
  background: rgba(255, 193, 7, 0.08);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 193, 7, 0.25) !important;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
}

.onboarding-blurred-zone {
  filter: blur(4px);
  pointer-events: none; /* Block user interactions entirely while locked */
  user-select: none;
  opacity: 0.5;
  transition: filter 0.4s ease, opacity 0.4s ease;
}

.hover-grow {
  transition: transform 0.2s ease;
}
.hover-grow:hover {
  transform: scale(1.03);
}

.animate-slide-down {
  animation: slideDown 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideDown {
  from { transform: translateY(-20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

/* Base style extensions remain consistent with previous design styles */
.text-success-tint { color: #7bf1a8; }
.tracking-tight { letter-spacing: -0.5px; }
.tracking-tighter { letter-spacing: -1.2px; }
.uppercase { text-transform: uppercase; }
.tracking-wider { letter-spacing: 0.8px; }
.operations-badge { background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.2); }
.deployment-glass-alert { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); }
.metric-glass-card { background: rgba(255, 255, 255, 0.05) !important; backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.1); }
.metric-icon { font-size: 1.8rem; }
.roster-glass-card { background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(10px); transition: transform 0.2s; }
.roster-glass-card:hover { transform: translateY(-2px); border-color: rgba(255, 255, 255, 0.2) !important; }
.lifecycle-tag { padding: 4px 10px; border-radius: 20px; font-weight: 600; }
.lifecycle-tag.open { background: rgba(25, 135, 84, 0.15); color: #7bf1a8; border: 1px solid rgba(25, 135, 84, 0.3); }
.lifecycle-tag.ongoing { background: rgba(0, 123, 255, 0.15); color: #7cd1ff; border: 1px solid rgba(0, 123, 255, 0.3); }
.lifecycle-tag.pending { background: rgba(255, 193, 7, 0.15); color: #ffe066; border: 1px solid rgba(255, 193, 7, 0.3); }
.custom-progress-bar { height: 6px; background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; overflow: hidden; }
.fs-8 { font-size: 0.88rem; }
.fs-9 { font-size: 0.76rem; }
</style>