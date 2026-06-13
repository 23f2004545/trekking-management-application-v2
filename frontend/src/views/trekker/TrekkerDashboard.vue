<template>
  <div class="trekker-dashboard-canvas text-white animate-fade-in pb-5 px-3">

    <div v-if="stats.blacklisted" class="alert alert-warning border border-danger border-opacity-30 rounded-3 p-3 mb-4 text-start bg-danger bg-opacity-10">
      <i class="bi bi-exclamation-triangle text-warning"></i> <strong>Blacklisted :</strong> Your access profile has been blacklisted by administration. Booking submission vectors are currently offline.
    </div>
    
    <!-- HERO SECTION & FOMO ALERT -->
    <div class="welcome-hero-section text-start py-4 mb-4">
      <div class="row align-items-end justify-content-between g-3">
        <div class="col-lg-7">
          <span class="badge status-badge mb-2 px-3 py-1.5 rounded-pill fs-9 fw-semibold">
            <i class="bi bi-geo-alt"></i> TREKKER BASECAMP OPERATIONS
          </span>
          <h1 class="display-4 fw-bold tracking-tight m-0">
            Welcome Back, <span class="text-glow">{{ authStore.userName }}</span>
          </h1>
          <p class="lead opacity-75 m-0 mt-2 fs-8 max-w-xl">
            Your telemetry markers are clean. The high-alpine season is peaking—ensure your medical clearances are up to date before deployment.
          </p>
        </div>
        
        <div class="col-lg-5 d-flex justify-content-lg-end">
          <Transition name="slide-fade" mode="out-in">
            <!-- LIVE FOMO TICKER -->
            <div :key="activeFomoEvent.user" class="fomo-glass-alert p-3 rounded-3 border border-success border-opacity-20 d-flex align-items-center gap-3">
              <span class="fs-3">📡</span>
              <div class="text-start">
                <h6 class="m-0 fw-bold text-success-tint small tracking-tight">Live Trail Network</h6>
                <p class="m-0 fs-9 text-white-50 mt-1">
                  <strong class="text-white">{{ activeFomoEvent.user }}</strong> just {{ activeFomoEvent.action }} on <strong class="text-white">{{ activeFomoEvent.trek }}</strong>!
                </p>
              </div>
            </div>
          </Transition>
        </div>
      </div>
    </div>

    <!-- METRICS ROW -->
    <div class="row g-3 mb-5">
      <div class="col-6 col-md-3">
        <div class="metric-glass-card p-3 p-md-4 text-center rounded-4 shadow-sm">
          <h6 class="metric-label opacity-60 small m-0 uppercase tracking-wider">Secured Slots</h6>
          <p class="metric-value display-5 fw-bold m-0 mt-1">{{ stats.secured_slots }}</p>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="metric-glass-card p-3 p-md-4 text-center rounded-4 shadow-sm">
          <h6 class="metric-label opacity-60 small m-0 uppercase tracking-wider">Paths Conquered</h6>
          <p class="metric-value display-5 fw-bold m-0 mt-1">{{ stats.completed_paths }}</p>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="metric-glass-card p-3 p-md-4 text-center rounded-4 shadow-sm">
          <h6 class="metric-label opacity-60 small m-0 uppercase tracking-wider">Elevation (M)</h6>
          <p class="metric-value display-5 fw-bold m-0 mt-1 text-glow">{{ stats.total_altitude }}</p>
        </div>
      </div>
      <div class="col-6 col-md-3">
        <div class="metric-glass-card p-3 p-md-4 text-center rounded-4 shadow-sm">
          <h6 class="metric-label opacity-60 small m-0 uppercase tracking-wider">Safety Status</h6>
          <p class="metric-value fs-4 fw-bold m-0 mt-2 text-success uppercase">ALL CLEAR</p>
        </div>
      </div>
    </div>

    <!-- DISCOVERY CTA & GAMIFIED CHART ROW -->
    <div class="row g-4 mb-4">
      
      <!-- CTA Panel -->
      <div class="col-lg-4">
        <div class="cta-glass-card p-4 p-md-5 rounded-4 shadow-sm h-100 d-flex flex-column justify-content-center text-center border border-success border-opacity-25">
          <span class="fs-1 mb-3"><i class="bi bi-compass"></i></span>
          <h3 class="fw-bold tracking-tight mb-2">Ready for the Summit?</h3>
          <p class="text-white-50 fs-8 mb-4">The alpine grids are open. Discover new routes, review guide logs, and secure your authorization pass today.</p>
          <button @click="$router.push('/portal/trekker/treks')" class="btn btn-success rounded-pill py-3 fw-bold text-dark fs-8 shadow w-100">
            Explore Open Trails Now
          </button>
        </div>
      </div>

      <!-- Altitude Progression Chart -->
      <div class="col-lg-8">
        <div class="chart-glass-container p-4 p-md-5 rounded-4 shadow-sm h-100">
          <h5 class="fw-bold tracking-tight fs-5 mb-1"><i class="bi bi-graph-up-arrow me-2"></i>Vertical Progression</h5>
          <p class="fs-9 text-white-50 mb-4">Tracking maximum altitude metrics conquered across completed expeditions.</p>
          
          <div v-if="stats.chart_data.length === 0" class="d-flex align-items-center justify-content-center h-75">
            <p class="text-white-50 italic fs-8">Complete a trek to begin logging your vertical progression matrix.</p>
          </div>
          
          <div v-else class="chart-canvas-wrapper position-relative" style="height: 250px;">
            <canvas ref="altitudeChartCanvas"></canvas>
          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useAuthStore } from '../../stores/auth'
import Chart from 'chart.js/auto'
import { secureFetch } from '@/utils/api'

const authStore = useAuthStore()
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

const altitudeChartCanvas = ref(null)
let chartInstance = null
let fomoInterval = null

const stats = ref({
  secured_slots: 0,
  completed_paths: 0,
  total_altitude: 0,
  chart_data: [],
  blacklisted: false
})

const activeFomoEvent = ref({ user: "Apex System", action: "initializing", trek: "Global Grid" })
const fomoQueue = ref([])

async function fetchDashboardMetrics() {
  try {
    const res = await secureFetch(`${BACKEND_URL}/api/trekker/dashboard/stats`, {
      method: 'GET', headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    
    if (res.ok) {
      const data = await res.json()
      stats.value = data
      fomoQueue.value = data.fomo_events
      
      startFomoTicker()

      if (data.chart_data.length > 0) {
        await nextTick()
        renderAltitudeChart(data.chart_data)
      }
    }
  } catch (err) {
    console.error("Dashboard Sync Failed", err)
  }
}

function startFomoTicker() {
  if (fomoQueue.value.length === 0) return
  
  // Set initial event
  activeFomoEvent.value = fomoQueue.value[0]
  let currentIndex = 0

  // Rotate events every 8 seconds to simulate live network traffic
  fomoInterval = setInterval(() => {
    currentIndex = (currentIndex + 1) % fomoQueue.value.length
    activeFomoEvent.value = fomoQueue.value[currentIndex]
  }, 8000)
}

function renderAltitudeChart(chartData) {
  if (chartInstance) chartInstance.destroy()
  
  if (altitudeChartCanvas.value) {
    chartInstance = new Chart(altitudeChartCanvas.value, {
      type: 'bar',
      data: {
        labels: chartData.map(d => d.trek_name),
        datasets: [{
          label: 'Max Altitude (Meters)',
          data: chartData.map(d => d.altitude),
          backgroundColor: 'rgba(123, 241, 168, 0.75)',
          borderRadius: 6,
          barThickness: 20
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false }, ticks: { color: 'rgba(255,255,255,0.6)', font: { size: 10 } } },
          y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: 'rgba(255,255,255,0.6)', font: { size: 10 } } }
        }
      }
    })
  }
}

onMounted(() => {
  fetchDashboardMetrics()
})

onUnmounted(() => {
  if (fomoInterval) clearInterval(fomoInterval)
})
</script>

<style scoped>
.text-glow { text-shadow: 0 0 15px rgba(255, 255, 255, 0.4); }
.max-w-xl { max-width: 600px; }
.uppercase { text-transform: uppercase; }
.tracking-wider { letter-spacing: 0.8px; }

/* FOMO Animations */
.fomo-glass-alert {
  background: rgba(25, 135, 84, 0.08) !important;
  backdrop-filter: blur(10px);
  width: 100%;
  max-width: 420px;
}
.slide-fade-enter-active { transition: all 0.5s ease-out; }
.slide-fade-leave-active { transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1); }
.slide-fade-enter-from { transform: translateX(20px); opacity: 0; }
.slide-fade-leave-to { transform: translateX(-20px); opacity: 0; }

.metric-glass-card {
  background: rgba(255, 255, 255, 0.08) !important;
  backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  transition: transform 0.25s;
}
.metric-glass-card:hover { transform: translateY(-3px); }
.metric-label { letter-spacing: 1px; }

.cta-glass-card, .chart-glass-container {
  background: rgba(255, 255, 255, 0.05) !important;
  backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
}
.cta-glass-card { background: rgba(25, 135, 84, 0.04) !important; }

.text-success-tint { color: #7bf1a8; }
.italic { font-style: italic; }

.fs-8 { font-size: 0.88rem; }
.fs-9 { font-size: 0.76rem; }
</style>