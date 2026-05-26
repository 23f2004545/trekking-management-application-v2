<template>
  <div class="trekker-dashboard-canvas text-white">
    
    <div class="welcome-hero-section text-start py-4 mb-4">
      <div class="row align-items-end justify-content-between g-3">
        <div class="col-lg-7">
          <span class="badge status-badge mb-2 px-3 py-1.5 rounded-pill fs-9 fw-semibold">
            🥾 CURRENT ACTIVE EXPEDITION PROFILE
          </span>
          <h1 class="display-4 fw-bold tracking-tight m-0">
            Welcome Back, <span class="text-glow">{{ authStore.userName }}</span>
          </h1>
          <p class="lead opacity-75 m-0 mt-2 fs-8 max-w-xl">
            Your telemetry markers are clean. There are currently <strong class="text-white">184 trekkers</strong> out on the high-alpine grids this week alone. Don't let the season pass you by.
          </p>
        </div>
        
        <div class="col-lg-4 d-flex justify-content-lg-end">
          <div class="fomo-glass-alert p-3 rounded-3 border border-warning border-opacity-20 d-flex align-items-start gap-2">
            <span class="fs-4">⏳</span>
            <div class="text-start">
              <h6 class="m-0 fw-bold text-warning small tracking-tight">Slots Depleting Rapidly</h6>
              <p class="m-0 fs-9 text-white-50 mt-1">The premium 'Rohtang Pass Crest' tracking matrix is at 94% capacity for this cycle. Secure your base authorization codes immediately.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-3 mb-5">
      <div class="col-6 col-md-3">
        <div class="metric-glass-card p-3 text-center rounded-3">
          <h6 class="metric-label opacity-60 small m-0">MY SECURED SLOTS</h6>
          <p class="metric-value display-6 fw-bold m-0 mt-1">02</p>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="metric-glass-card p-3 text-center rounded-3">
          <h6 class="metric-label opacity-60 small m-0">PATHS COMPLETED</h6>
          <p class="metric-value display-6 fw-bold m-0 mt-1">05</p>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="metric-glass-card p-3 text-center rounded-3">
          <h6 class="metric-label opacity-60 small m-0">TOTAL ALTITUDE (M)</h6>
          <p class="metric-value display-6 fw-bold m-0 mt-1">4,240</p>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="metric-glass-card p-3 text-center rounded-3">
          <h6 class="metric-label opacity-60 small m-0">GLOBAL SAFETY ALERTS</h6>
          <p class="metric-value display-6 fw-bold m-0 mt-1 text-success">ALL CLEAR</p>
        </div>
      </div>
    </div>

    <div class="filter-controls-wrapper p-3 rounded-4 mb-4 shadow-sm border border-white border-opacity-10">
      <div class="row g-3 align-items-center">
        
        <div class="col-md-4">
          <div class="search-input-box px-3 py-2 rounded-3 d-flex align-items-center">
            <span class="me-2 opacity-60">🔍</span>
            <input 
              v-model="searchLocation" 
              type="text" 
              placeholder="Filter by mountain location..." 
              class="bg-transparent border-0 text-white w-100 clean-field"
            >
          </div>
        </div>

        <div class="col-md-4">
          <select v-model="selectedDifficulty" class="select-glass-box w-100 px-3 py-2 rounded-3 text-white">
            <option value="">All Difficulty Intensities</option>
            <option value="Easy">🟢 Easy Trails</option>
            <option value="Moderate">🟡 Moderate Tracks</option>
            <option value="Hard">🔴 High-Alpine Hard</option>
          </select>
        </div>

        <div class="col-md-4 d-flex justify-content-md-end">
          <button @click="resetFilters" class="btn-reset-glass rounded-3 px-4 py-2 w-100 w-md-auto fw-medium fs-8">
            Reset System Filters
          </button>
        </div>

      </div>
    </div>

    <div class="treks-showcase-section">
      <h3 class="fw-bold tracking-tight mb-3 text-start">Available Expeditions</h3>
      
      <div v-if="filteredTreks.length === 0" class="empty-state-glass p-5 text-center rounded-4 border border-white border-opacity-10">
        <span class="fs-1">🗺️</span>
        <h5 class="fw-bold mt-2 mb-1">No Matching Expeditions Found</h5>
        <p class="m-0 text-white-50 small">Adjust your telemetry metrics parameters or expand your search scope parameters.</p>
      </div>

      <div v-else class="row g-4 text-start">
        <div v-for="trek in filteredTreks" :key="trek.id" class="col-xl-4 col-md-6">
          <div class="trek-glass-card h-100 p-4 rounded-4 d-flex flex-column justify-content-between border border-white border-opacity-15 shadow-sm">
            
            <div>
              <div class="d-flex align-items-center justify-content-between mb-2">
                <span class="badge diff-badge text-uppercase fs-9 fw-bold" :class="trek.difficulty.toLowerCase()">
                  {{ trek.difficulty }}
                </span>
                <span class="fs-9 opacity-50 fw-bold">⌛ {{ trek.duration }} DAYS</span>
              </div>

              <h4 class="trek-card-title fw-bold m-0 tracking-tight mb-1">{{ trek.name }}</h4>
              <p class="trek-card-loc small opacity-75 d-flex align-items-center gap-1 mb-3">
                📍 <span>{{ trek.location }}</span>
              </p>
            </div>

            <div class="pt-3 border-top border-white border-opacity-10 mt-3 d-flex align-items-center justify-content-between">
              <div class="slots-indicator">
                <p class="m-0 fs-9 opacity-50 fw-semibold uppercase">SLOTS AVAILABLE</p>
                <p class="m-0 fw-bold text-success fs-7" :class="{ 'text-danger': trek.available_slots <= 3 }">
                  {{ trek.available_slots }} remaining
                </p>
              </div>
              <button @click="initiateBooking(trek.id)" class="btn-card-action rounded-pill px-3.5 py-1.5 fw-bold fs-8 border-0">
                Book Path
              </button>
            </div>

          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { useAlertStore } from '../../stores/alert'

const authStore = useAuthStore()
const alertStore = useAlertStore()

// System Reactive Control Variables
const searchLocation = ref('')
const selectedDifficulty = ref('')

// Mocked live data block matching your exact Flask route properties setup
const availableTreks = ref([
  { id: 1, name: 'Triund Peak Ridge', location: 'Dharamshala, HP', difficulty: 'Easy', duration: 2, available_slots: 14 },
  { id: 2, name: 'Rohtang Pass Crest', location: 'Manali, HP', difficulty: 'Hard', duration: 5, available_slots: 2 },
  { id: 3, name: 'Hampta Pass Corridor', location: 'Kullu Valley, HP', difficulty: 'Moderate', duration: 4, available_slots: 18 },
  { id: 4, name: 'Kheerganga Hot Springs', location: 'Parvati Valley, HP', difficulty: 'Easy', duration: 3, available_slots: 22 },
  { id: 5, name: 'Bhrigu Lake Circuit', location: 'Manali Heights, HP', difficulty: 'Hard', duration: 4, available_slots: 5 }
])

// Pure client-side dynamic search filtering pipeline engine computation
const filteredTreks = computed(() => {
  return availableTreks.value.filter(trek => {
    const matchLocation = trek.location.toLowerCase().includes(searchLocation.value.toLowerCase())
    const matchDiff = selectedDifficulty.value === '' || trek.difficulty === selectedDifficulty.value
    return matchLocation && matchDiff
  })
})

function resetFilters() {
  searchLocation.value = ''
  selectedDifficulty.value = ''
  alertStore.showAlert('System telemetry search variables reset successfully.', 'info')
}

function initiateBooking(trekId) {
  // Captures input for your Flask endpoint body payload
  alertStore.showAlert(`Booking request for route ID code #${trekId} dispatched to verification pipeline.`, 'success')
}
</script>

<style scoped>
.max-w-xl { max-width: 600px; }
.text-glow { text-shadow: 0 0 15px rgba(255, 255, 255, 0.4); }

/* Status & Fomo Alerts layout pods */
.status-badge {
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.25);
  letter-spacing: 0.5px;
}

.fomo-glass-alert {
  background: rgba(255, 193, 7, 0.08) !important;
  backdrop-filter: blur(10px);
  max-width: 360px;
}

/* Metric Display Row Cards */
.metric-glass-card {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.15);
}
.metric-label { font-size: 0.72rem; letter-spacing: 0.5px; }

/* Filter Container Blocks styling */
.filter-controls-wrapper {
  background: rgba(255, 255, 255, 0.06) !important;
  backdrop-filter: blur(16px);
}

.search-input-box {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
}
.clean-field:focus { outline: none; }
.clean-field::placeholder { color: rgba(255, 255, 255, 0.45); }

.select-glass-box {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  outline: none;
}
.select-glass-box option { background: #16241c; color: white; }

.btn-reset-glass {
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.25);
  color: white;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-reset-glass:hover { background: rgba(255, 255, 255, 0.25); }

/* Individual Trek Showcase Cards Elements */
.trek-glass-card {
  background: rgba(255, 255, 255, 0.12) !important;
  backdrop-filter: blur(16px);
  transition: transform 0.25s ease, border-color 0.25s ease;
}
.trek-glass-card:hover {
  transform: translateY(-4px);
  border-color: rgba(255, 255, 255, 0.3) !important;
}

.trek-card-title { font-size: 1.25rem; letter-spacing: -0.3px; }

.diff-badge.easy { background: rgba(25, 135, 84, 0.2); color: #7bf1a8; border: 1px solid rgba(25, 135, 84, 0.4); }
.diff-badge.moderate { background: rgba(255, 193, 7, 0.15); color: #ffe066; border: 1px solid rgba(255, 193, 7, 0.4); }
.diff-badge.hard { background: rgba(220, 53, 69, 0.2); color: #ff8787; border: 1px solid rgba(220, 53, 69, 0.4); }

.btn-card-action {
  background: #ffffff;
  color: #0b1f15;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-card-action:hover { background: #e8f5e9; }

.empty-state-glass { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); }

.fs-8 { font-size: 0.88rem; }
.fs-9 { font-size: 0.76rem; }
</style>