<template>
  <div class="treks-exploration-viewport text-white text-start">
  
    <div class="mb-4">
      <h2 class="fw-bold tracking-tight m-0">Discover Expedition Trails</h2>
      <p class="m-0 text-white-50 fs-8 mt-1">Browse open mountain coordinates, check altitude parameters, and examine verified safety guide telemetry.</p>
    </div>

    <!-- ===================================================================
         1. COMPACT SEARCH & COMPREHENSIVE FILTER SYSTEM
         =================================================================== -->
    <div class="glass-container p-3.5 rounded-4 mb-4 shadow-sm">
      <div class="row g-3 align-items-center">
        <!-- Text Lookup Search -->
        <div class="col-md-3">
          <div class="search-box px-3 py-1.5 rounded-3 d-flex align-items-center">
            <span class="me-2 text-white-50 opacity-50">🔍</span>
            <input v-model="filters.query" type="text" placeholder="Search by name or grid..." class="bg-transparent border-0 text-white w-100 fs-8 clean-field">
          </div>
        </div>
        <!-- Difficulty Dropdown Filter -->
        <div class="col-md-3">
          <select v-model="filters.difficulty" class="select-glass w-100 px-3 py-1.5 rounded-3 text-white fs-8">
            <option value="">All Intensities</option>
            <option value="Easy">Easy Trails</option>
            <option value="Moderate">Moderate Tracks</option>
            <option value="Hard">High-Alpine Hard</option>
          </select>
        </div>
        <!-- Price Range Filter Slider -->
        <div class="col-md-3">
          <label class="d-block fs-9 text-white-50 mb-1">Max Budget: <span class="text-success fw-bold">₹{{ filters.price }}</span></label>
          <input v-model.number="filters.price" type="range" min="3000" max="25000" step="500" class="form-range custom-slider">
        </div>
        <!-- Altitude Cap Filter -->
        <div class="col-md-3">
          <label class="d-block fs-9 text-white-50 mb-1">Max Altitude: <span class="text-success fw-bold">{{ filters.altitude }}m</span></label>
          <input v-model.number="filters.altitude" type="range" min="2500" max="6000" step="200" class="form-range custom-slider">
        </div>
      </div>
    </div>

      <!-- ===================================================================
         2. EXISTING EXPEDITIONS GRID CANVAS
         =================================================================== -->
    <div v-if="filteredTreks.length === 0" class="empty-state p-5 text-center rounded-4 border border-white border-opacity-10 bg-opacity-5">
      <span class="fs-1">🗺️</span>
      <h5 class="fw-bold mt-2">No Expedition Inventories Map Matches</h5>
      <p class="text-white-50 small m-0">Reset parameters filters or configure a brand new track route.</p>
    </div>

    <div v-else class="row g-4">
      <div v-for="trek in filteredTreks" :key="trek.trek_id" class="col-xl-4 col-md-6">
                <div class="trek-glass-card h-100 rounded-4 overflow-hidden border border-white border-opacity-10 shadow d-flex flex-column justify-content-between">
          
          <div class="card-image-thumbnail-wrapper position-relative">
            <img :src="BACKEND_URL + trek.image_url" alt="Trek Thumbnail" class="thumbnail-img w-100" />
          </div>
          <span class="badge position-absolute  status-pill" :class="trek.status.toLowerCase()" style="top: 1rem; right: 1rem;">
            ● {{ trek.status }}
          </span>

          <div class="p-3_5 flex-grow-1 d-flex flex-column justify-content-between">
            <div>
              <div class="d-flex align-items-center justify-content-between text-white-50 fs-9 fw-bold mb-1.5">
                <span class="text-uppercase tracking-wider">🧗 {{ trek.difficulty }}</span>
                <span>🏔️ {{ trek.max_altitude }}m</span>
              </div>
              <h4 class="fw-bold tracking-tight m-0 mb-1 text-white">{{ trek.trek_name }}</h4>
              <p class="fs-8 text-white-50 m-0 mb-3">📍 {{ trek.location }}</p>
            </div>

            <div class="pt-3 border-top border-white border-opacity-10 d-flex align-items-center justify-content-between">
              <div>
                <span class="d-block fs-9 text-white-50 opacity-50 fw-semibold">VALUED AT</span>
                <strong class="fs-6 text-success">₹{{ trek.price_per_person }}</strong>
              </div>
              <button @click="routeToDeepInsights(trek.trek_id)" class="btn btn-sm btn-light rounded-pill px-3.5 py-1.5 fs-8 fw-bold text-dark">
                View Details
              </button>
            </div>
          </div>

        </div>
      </div>
    </div>

  </div>
</template>

<script setup>

import { ref, onMounted ,computed } from 'vue'
import { useAlertStore } from '../../stores/alert'
import { useAuthStore } from '../../stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const alertStore = useAlertStore()
const authStore = useAuthStore()
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

const selectedTrek = ref(null)
const activeImageIndex = ref(0)
const tracksList = ref([])


// Filtering state metrics
const filters = ref({ query: '', difficulty: '', price: 25000, altitude: 6000 })

// DYNAMIC SEARCH & FILTER CALCULATOR ENGINE
const filteredTreks = computed(() => {
  return tracksList.value.filter(t => {
    const matchesQuery = t.trek_name.toLowerCase().includes(filters.value.query.toLowerCase()) || 
                         t.location.toLowerCase().includes(filters.value.query.toLowerCase())
    const matchesDiff = !filters.value.difficulty || t.difficulty === filters.value.difficulty
    const matchesPrice = t.price_per_person <= filters.value.price
    const matchesAlt = t.max_altitude <= filters.value.altitude
    return matchesQuery && matchesDiff && matchesPrice && matchesAlt
  })
})


// ==========================================================================
// REAL DATA FETCH ENGINE
// ==========================================================================
async function fetchDiscoverableTreks() {
  try {
    const res = await fetch(`${BACKEND_URL}/api/trekker/treks`, {
      method: 'GET',
      headers: { 
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
      }
    })

    if (res.ok) {
      tracksList.value = await res.json()

    } else {
      alertStore.showAlert('Failed to synchronize open expedition parameters.', 'danger')
    }
  } catch (err) {
    alertStore.showAlert(`Network tracking drop: ${err.message}`, 'danger')
  }
}

// ==========================================================================
// MODAL & ACTION HANDLERS (Preserved from original design)
// ==========================================================================
function openDetailedOverlay(trek) {
  activeImageIndex.value = 0
  selectedTrek.value = trek
}

function closeDetailedOverlay() {
  selectedTrek.value = null
}

function executeBookingAction(id) {
  alertStore.showAlert(`Slot application sequence for Trek #${id} dispatched to Flask database layers.`, 'success')
  selectedTrek.value = null
}

function routeToDeepInsights(id) {
  // Automatically routes down to your reusable nested component structure
  router.push(`/portal/trek/view/${id}`)
}

onMounted(() => {
  fetchDiscoverableTreks()
})

</script>

<style scoped>

.glass-container { background: rgba(255, 255, 255, 0.05) !important; backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.12) !important; padding: 0.5rem; }
.trek-glass-card {
  background: rgba(255, 255, 255, 0.05) !important;
  backdrop-filter: blur(20px);
}

.card-image-thumbnail-wrapper { height: 160px; overflow: hidden; }
.thumbnail-img { height: 100%; object-fit: cover; }

/* Status pill classes mapping definitions */
.status-pill { padding: 4px 10px; font-size: 0.72rem; border-radius: 20px; font-weight: 600; }
.status-pill.open { background: rgba(25, 135, 84, 0.8); border: 1px solid #198754; }

.search-box { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); }
.clean-field:focus { outline: none; }
.select-glass { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); outline: none; padding:0.2rem; }
.select-glass option { background: #141c16; color: white; }

.custom-slider::-webkit-slider-runnable-track { background: rgba(255, 255, 255, 0.1); border-radius: 5px; height: 4px; }
.custom-slider::-webkit-slider-thumb { background: #198754; margin-top: -6px; }

/* Immersive Detailed Modal Shell Elements */
.detailed-overlay-backdrop {
  position: fixed !important; top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(10, 20, 15, 0.6) !important;
  backdrop-filter: blur(20px) !important; -webkit-backdrop-filter: blur(20px) !important;
  z-index: 99999999 !important;
}

.glass-detail-card {
  background: rgba(25, 35, 30, 0.88) !important;
  backdrop-filter: blur(35px);
  max-width: 900px;
}
.max-vh-90 { max-height: 90vh; }

.active-gallery-frame { height: 260px; }
.master-gallery-view { height: 100%; object-fit: cover; }
.gallery-thumb-container { height: 50px; opacity: 0.4; transition: opacity 0.2s; }
.gallery-thumb-container:hover, .active-thumb { opacity: 1; border: 1.5px solid #198754; }
.thumb-img-element { height: 100%; object-fit: cover; }

/* Staff Capsule styles */
.staff-glass-capsule { background: rgba(255, 255, 255, 0.04); }
.staff-card-avatar { width: 55px; height: 55px; border-radius: 8px; object-fit: cover; border: 1px solid rgba(255,255,255,0.15); }

.btn-close-modal-round { background: rgba(255, 255, 255, 0.1); border: none; color: white; width: 28px; height: 28px; border-radius: 50%; cursor: pointer; }
.btn-close-modal-round:hover { background: rgba(255, 255, 255, 0.2); }

.text-justify { text-align: justify; }
.italic { font-style: italic; }
.p-3_5 { padding: 14px; }
.fs-8 { font-size: 0.88rem; }
.fs-9 { font-size: 0.76rem; }
.tracking-wider { letter-spacing: 0.5px; }
</style>