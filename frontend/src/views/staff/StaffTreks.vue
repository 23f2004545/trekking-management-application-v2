<template>
  <div class="staff-treks-viewport text-white text-start pb-5 animate-fade-in">
    
    <div class="mb-4">
      <h2 class="fw-bold tracking-tight m-0">My Assigned Trails</h2>
      <p class="m-0 text-white-50 fs-8 mt-1">Manage your operational routes, track lifecycle states, and review map details.</p>
    </div>

    <!-- Search & Filter Controls -->
    <div class="filter-glass-panel p-3 rounded-4 mb-4 shadow-sm border border-white border-opacity-10">
      <div class="row g-3 align-items-center">
        <div class="col-md-6">
          <div class="search-input-box px-3 py-2 rounded-3 d-flex align-items-center">
            <span class="me-2 opacity-60"><i class="bi bi-search"></i></span>
            <input v-model="filters.query" type="text" placeholder="Search route by name or location..." class="bg-transparent border-0 text-white w-100 clean-field">
          </div>
        </div>
        <div class="col-md-6">
          <select v-model="filters.status" class="select-glass-box w-100 px-3 py-2 rounded-3 text-white">
            <option value="">All Operational Statuses</option>
            <option value="Open">Open (Booking Active)</option>
            <option value="Ongoing">Ongoing (On-Trail)</option>
            <option value="Completed">Completed</option>
            <option value="Cancelled">Cancelled</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Cards Grid -->
    <div v-if="filteredTreks.length === 0" class="empty-state-glass p-5 text-center rounded-4 border border-white border-opacity-10">
      <span class="fs-1"><i class="bi bi-exclamation-triangle"></i></span>
      <h5 class="fw-bold mt-2 mb-1">No Routes Found</h5>
      <p class="m-0 text-white-50 small">No assigned routes match the current telemetry filter parameters.</p>
    </div>

    <div v-else class="row g-4 text-start">
      <div v-for="trek in filteredTreks" :key="trek.id" class="col-xl-4 col-md-6">
        <div class="trek-glass-card h-100 p-3 rounded-4 d-flex flex-column justify-content-between shadow-sm">
          
          <div class="img-frame rounded-3 overflow-hidden mb-3 position-relative">
            <img :src="getAbsoluteUrl(trek.image)" class="w-100 h-100 object-cover" alt="Trek Cover"/>
            <span class="badge position-absolute status-pill" :class="trek.status.toLowerCase()" style="top: 1rem; right: 1rem;">
             ● {{  trek.status }}
            </span>
          </div>

          <div class="flex-grow-1">
            <div class="d-flex justify-content-between align-items-center mb-1">
              <span class="fs-9 text-uppercase tracking-wider fw-bold text-white-50">{{ trek.difficulty }}</span>
              <span class="fs-9 text-white-50"><i class="bi bi-clock"></i> {{ trek.duration }} Days</span>
            </div>
            <h5 class="fw-bold tracking-tight m-0 text-white">{{ trek.name }}</h5>
            <p class="fs-9 text-white-50 m-0 mt-1"><i class="bi bi-geo-alt"></i> {{ trek.location }}</p>
          </div>

          <div class="pt-3 border-top border-white border-opacity-10 mt-3 d-flex align-items-center justify-content-between">
            <div>
              <span class="d-block fs-9 text-white-50 opacity-60 fw-semibold">DEPARTURE</span>
              <strong class="fs-7 text-white">{{ trek.start_date }}</strong>
            </div>
            <button @click="$router.push(`/portal/trek/view/${trek.id}`)" class="btn btn-sm btn-light rounded-pill px-3.5 py-1.5 fw-bold text-dark">
              View Route Details
            </button>
          </div>

        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { useAlertStore } from '../../stores/alert'

const authStore = useAuthStore()
const alertStore = useAlertStore()
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

const myTreks = ref([])
const filters = ref({ query: '', status: '' })

const filteredTreks = computed(() => {
  return myTreks.value.filter(t => {
    const matchName = t.name.toLowerCase().includes(filters.value.query.toLowerCase()) || 
                      t.location.toLowerCase().includes(filters.value.query.toLowerCase())
    const matchStatus = filters.value.status === '' || t.status === filters.value.status
    return matchName && matchStatus
  })
})

function getAbsoluteUrl(url) {
  if (!url) return ''
  return url.startsWith('http') ? url : `${BACKEND_URL}${url}`
}

async function fetchMyTreks() {
  try {
    const res = await fetch(`${BACKEND_URL}/api/trek_staff/treks`, {
      method: 'GET', headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    if (res.ok) myTreks.value = await res.json()
  } catch (err) { alertStore.showAlert("Failed to sync routes.", "danger") }
}

onMounted(() => { fetchMyTreks() })
</script>

<style scoped>
.filter-glass-panel, .trek-glass-card {
  background: rgba(255, 255, 255, 0.05) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.12);
}
.trek-glass-card { transition: transform 0.2s; }
.trek-glass-card:hover { transform: translateY(-4px); border-color: rgba(25, 135, 84, 0.4); }

.img-frame { height: 160px; }
.object-cover { object-fit: cover; }

.search-input-box, .select-glass-box {
  background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.15);
}
.select-glass-box { outline: none; }
.select-glass-box option { background: #16241c; color: white; }
.clean-field:focus { outline: none; }

.status-pill { padding: 4px 10px; border-radius: 20px; font-weight: 600; }
.status-pill.open { background: rgba(25, 135, 84, 0.8); }
.status-pill.ongoing { background: rgba(0, 123, 255, 0.8); }
.status-pill.completed { background: rgba(9, 105, 214, 0.78); }
.status-pill.cancelled { background: rgba(220, 53, 69, 0.8); }

.fs-8 { font-size: 0.88rem; } .fs-9 { font-size: 0.76rem; }
</style>