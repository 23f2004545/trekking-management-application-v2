<template>
  <div class="staff-treks-viewport text-white text-start pb-5 animate-fade-in px-3">
    
    <div class="mb-4">
      <h2 class="fw-bold tracking-tight m-0">My Assigned Trails</h2>
      <p class="m-0 text-white-50 fs-8 mt-1">Manage your operational routes, track lifecycle states, and review map details.</p>
    </div>

    <!-- Search & Filter Controls -->
    <div class="filter-glass-panel p-2 rounded-4 mb-4 shadow-sm border border-white border-opacity-10">
      <div class="row g-3 align-items-center">
        <div class="col-md-6">
          <div class="search-input-box px-3 py-2 rounded-3 d-flex align-items-center" style="height: 2rem;">
            <span class="me-2 opacity-60"><i class="bi bi-search"></i></span>
            <input v-model="filters.query" type="text" placeholder="Search route by name or location..." class="bg-transparent border-0 text-white w-100 clean-field">
          </div>
        </div>
        <div class="col-md-6">
          <select v-model="filters.status" class="select-glass-box w-100 px-3 py-1 rounded-3 text-white" >
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
        <div 
          class="trek-premium-card position-relative rounded-4 shadow-sm d-flex flex-column text-start"
          @click="routeToDeepInsights(trek.trek_id)"
        >
          
          <div class="card-bg-wrapper position-absolute top-0 start-0 w-100 h-100 z-0">
            <img :src="BACKEND_URL + trek.image_url" alt="Trek Graphic" class="card-bg-img w-100 h-100 object-cover" />
          </div>

          <div class="card-gradient-overlay position-absolute top-0 start-0 w-100 h-100 z-1"></div>

          <div class="position-relative z-2 d-flex flex-column h-100 p-4 w-100">

            <span class="badge position-absolute status-pill" :class="trek.status.toLowerCase()" style="top: 1rem; left: 1rem;">
              {{ trek.status }}
            </span>
            <span class="badge position-absolute difficulty-pill" :class="trek.difficulty.toLowerCase()" style="top: 1rem; right: 1rem;">
              <i class="bi bi-activity me-1.5 opacity-50"></i> {{ trek.difficulty }}
            </span>

            <div class="mt-auto w-100 pb-1">
              
              <div class="d-flex flex-column align-items-start gap-2 mb-2">
                <div v-if="trek.trek_rating ">
                  <span class="badge bg-white bg-opacity-10 text-white border border-warning border-opacity-20 rounded-pill px-2.5 py-1 fs-10 backdrop-blur fw-normal">
                  Rating : {{ trek.trek_rating }} <i class="bi bi-star-fill text-warning"></i>
                  </span>
                </div>
                <span class="fs-10 text-white fw-medium">
                  <i class="bi bi-people-fill text-success opacity-75 me-1"></i> 
                  <span :class="trek.available_slots < 5 ? 'text-warning' : ''">{{ trek.available_slots }} Slots Available</span>
                </span>
              </div>

              <div class="d-flex justify-content-between align-items-end mb-1">
                <h3 class="fw-bold text-white m-0 text-truncate pe-3 tracking-tight text-shadow-sm">{{ trek.trek_name }}</h3>
                <h4 class="fw-bold text-success m-0 tracking-tight text-shadow-sm">₹{{ trek.price_per_person }} / <i class="bi bi-person"></i></h4>
              </div>

              <p class="fs-9 text-info m-0 text-truncate fw-medium mb-2 ">
                <i class="bi bi-geo-alt-fill text-danger opacity-50 me-1"></i>{{ trek.location }}
              </p>

              <hr class="border-white border-opacity-20 my-3" />

              <div class="d-flex align-items-center justify-content-between fs-9 text-white-75 w-100 flex-nowrap">
                <div class="d-flex align-items-center text-truncate pe-2">
                  <i class="bi bi-clock-history me-1 opacity-50"></i> {{ trek.duration_days }} Day(s)
                </div>

                <div class="d-flex align-items-center border-start border-end border-white border-opacity-20 px-2 text-truncate justify-content-center flex-grow-1">
                  {{ trek.start_date }}  : {{ trek.end_date }}
                </div>
                <div class="d-flex align-items-center text-truncate ps-2 justify-content-end">
                  <i class="bi bi-caret-up-fill me-1 text-info"></i> {{ trek.max_altitude }}m
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
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { useAlertStore } from '../../stores/alert'
import { useRouter } from 'vue-router'
import { secureFetch } from '@/utils/api'

const authStore = useAuthStore()
const router = useRouter()
const alertStore = useAlertStore()
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

const myTreks = ref([])
const filters = ref({ query: '', status: '' })

const filteredTreks = computed(() => {
  return myTreks.value.filter(t => {
    const matchName = t.trek_name.toLowerCase().includes(filters.value.query.toLowerCase()) || 
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
    const res = await secureFetch(`${BACKEND_URL}/api/trek_staff/treks`, {
      method: 'GET', headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    if (res.ok) myTreks.value = await res.json()
  } catch (err) { alertStore.showAlert("Failed to sync routes.", "danger") }
}

function routeToDeepInsights(id) {
  // Automatically routes down to your reusable nested component structure
  router.push(`/portal/trek/view/${id}`)
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
.select-glass-box { outline: none; height: 2rem; }
.select-glass-box option { background: #16241c; color: white; }
.clean-field:focus { outline: none; }

.status-pill { padding: 4px 10px; border-radius: 20px; font-weight: 600; }
.status-pill.open { background: rgba(25, 135, 84, 0.8); }
.status-pill.ongoing { background: rgba(220, 208, 36, 0.558); }
.status-pill.pending { background: rgba(198, 192, 101, 0.768); }
.status-pill.completed { background: rgba(9, 105, 214, 0.78); }
.status-pill.cancelled { background: rgba(220, 53, 69, 0.8); }

.difficulty-pill { padding: 3px 9px; font-size: 0.7rem; border-radius: 20px; font-weight: 600; text-transform: uppercase; }
.difficulty-pill.easy { background: rgba(25, 135, 84, 0.8); }
.difficulty-pill.moderate { background: rgba(255, 193, 7, 0.8); color: black; }
.difficulty-pill.hard { background: rgba(220, 53, 69, 0.8); }

.trek-premium-card {
  min-height: 440px;       /* Taller to give landscape images room to breathe */
  height: 100%;            /* Ensures flex children behave */
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.05); /* Extremely subtle border */
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  background-color: #0d0f12;
  overflow: hidden;
}

/* Hover Selection Outline & Lift */
.trek-premium-card:hover {
  border-color: rgba(255, 255, 255, 0.4); 
  transform: translateY(-5px);            
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
}

/* The Image Wrapper & Zoom Effect */
.card-bg-wrapper {
  overflow: hidden;
  border-radius: inherit; /* Keeps the rounded corners clean */
}

.card-bg-img {
  transition: transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.trek-premium-card:hover .card-bg-img {
  transform: scale(1.06); /* The "Ken Burns" subtle zoom */
}

/* Gradient Overlay - Reversed to explicitly build from the bottom up */
.card-gradient-overlay {
  background: linear-gradient(
    to top, 
    rgba(8, 10, 12, 0.98) 0%,   /* Solid dark at the very bottom */
    rgba(8, 10, 12, 0.85) 25%,  /* Heavy dark behind the text */
    rgba(8, 10, 12, 0.4) 50%,   /* Fading out */
    rgba(8, 10, 12, 0.1) 80%, 
    rgba(0, 0, 0, 0) 100%
  );
  pointer-events: none; 
}
/* Extra small font size for meta tags */
.fs-10 {
  font-size: 0.72rem;
}

.fs-8 { font-size: 0.88rem; } .fs-9 { font-size: 0.76rem; }
</style>