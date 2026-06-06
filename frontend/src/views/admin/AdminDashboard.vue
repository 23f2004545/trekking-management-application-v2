<template>
  <div class="admin-dashboard-canvas text-white text-start pb-5 animate-fade-in px-3">
    
    <div class="d-flex align-items-center justify-content-between flex-wrap gap-4 py-4 border-bottom border-white border-opacity-10 mb-5">
      <div>
        <h1 class="display-5 fw-bold tracking-tight m-0 text-shadow-deep">System Command Center</h1>
        <p class="opacity-75 m-0 mt-2 fs-8 max-w-lg lh-base">
          Monitor ecosystem telemetry, evaluate guide performance, and audit global booking vectors.
        </p>
      </div>

      <div class="d-flex gap-3">
        <button @click="$router.push('/portal/admin/treks')" class="btn-glass-action rounded-pill px-4 py-2 fs-8 fw-semibold text-white">
          <i class="bi bi-plus-lg me-2"></i> Add Trek Route
        </button>
        <button @click="$router.push('/portal/admin/staff')" class="btn-glass-action rounded-pill px-4 py-2 fs-8 fw-semibold text-white">
          <i class="bi bi-person-plus me-2"></i> Add Staff Guide
        </button>
      </div>
    </div>

    <div class="row g-4 mb-5">
      <div class="col-xl-3 col-md-6">
        <div class="stats-glass-card p-4 rounded-4 shadow-sm d-flex flex-column justify-content-center">
          <div class="d-flex align-items-center gap-3 mb-2">
            <div class="metric-icon"><i class="bi bi-map"></i></div>
            <h6 class="card-title-lbl m-0 uppercase tracking-wider">Total Treks</h6>
          </div>
          <p class="display-4 fw-black m-0 tracking-tighter">{{ stats.counters.treks }}</p>
        </div>
      </div>
      <div class="col-xl-3 col-md-6">
        <div class="stats-glass-card p-4 rounded-4 shadow-sm d-flex flex-column justify-content-center">
          <div class="d-flex align-items-center gap-3 mb-2">
            <div class="metric-icon"><i class="bi bi-calendar-check"></i></div>
            <h6 class="card-title-lbl m-0 uppercase tracking-wider">Live Bookings</h6>
          </div>
          <p class="display-4 fw-black m-0 tracking-tighter">{{ stats.counters.bookings }}</p>
        </div>
      </div>
      <div class="col-xl-3 col-md-6">
        <div class="stats-glass-card p-4 rounded-4 shadow-sm d-flex flex-column justify-content-center">
          <div class="d-flex align-items-center gap-3 mb-2">
            <div class="metric-icon"><i class="bi bi-person-check text-success"></i></div>
            <h6 class="card-title-lbl m-0 uppercase tracking-wider">Verified Guides</h6>
          </div>
          <p class="display-4 fw-black m-0 tracking-tighter">{{ stats.counters.staff }}</p>
        </div>
      </div>
      <div class="col-xl-3 col-md-6">
        <div class="stats-glass-card p-4 rounded-4 shadow-sm d-flex flex-column justify-content-center">
          <div class="d-flex align-items-center gap-3 mb-2">
            <div class="metric-icon"><i class="bi bi-person text-info"></i></div>
            <h6 class="card-title-lbl m-0 uppercase tracking-wider">System Users</h6>
          </div>
          <p class="display-4 fw-black m-0 tracking-tighter">{{ stats.counters.trekkers }}</p>
        </div>
      </div>
    </div>

    <h5 class="fw-bold tracking-tight fs-5 mb-4"><i class="bi bi-star-fill text-warning"></i> Ecosystem Reputation Insights</h5>
    <div class="row g-4 mb-5">
      <div class="col-md-4">
        <div class="insight-glass-card p-4 rounded-4 d-flex align-items-center gap-4">
          <h2 class="display-5 fw-bold text-warning m-0">{{ stats.insights.global_avg_rating }}</h2>
          <div>
            <h6 class="m-0 fw-bold tracking-tight">Platform Average</h6>
            <p class="m-0 fs-9 text-white-50 mt-1">Overall Trek Ratings</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="insight-glass-card p-4 rounded-4">
          <h6 class="fs-9 text-white-50 uppercase tracking-wider mb-2">Highest Rated Trek</h6>
          <div v-if="stats.insights.top_trek">
            <h5 class="fw-bold text-success m-0">{{ stats.insights.top_trek.name }}</h5>
            <span class="text-warning fs-9 fw-bold"><i class="bi bi-star-fill text-warning"></i> {{ stats.insights.top_trek.rating }} / 5.0</span>
          </div>
          <div v-else class="text-white-50 italic fs-9 mt-2">Not enough review data.</div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="insight-glass-card p-4 rounded-4">
          <h6 class="fs-9 text-white-50 uppercase tracking-wider mb-2">Top Performing Guide</h6>
          <div v-if="stats.insights.top_staff">
            <h5 class="fw-bold text-success m-0">{{ stats.insights.top_staff.name }}</h5>
            <span class="text-warning fs-9 fw-bold"><i class="bi bi-star-fill text-warning"></i> {{ stats.insights.top_staff.rating }} / 5.0</span>
          </div>
          <div v-else class="text-white-50 italic fs-9 mt-2">Not enough review data.</div>
        </div>
      </div>
    </div>

    <h5 class="fw-bold tracking-tight fs-5 mb-4"><i class="bi bi-graph-up-arrow"></i> Growth & Analytics Matrix</h5>
    
    <div v-if="!stats.charts.has_data" class="empty-data-glass p-5 rounded-4 text-center border border-white border-opacity-10 mb-4">
      <div class="fs-1 mb-3 opacity-50"><i class="bi bi-graph-up-arrow"></i></div>
      <h5 class="fw-bold tracking-tight">Analytics Awaiting Telemetry</h5>
      <p class="text-white-50 fs-8 max-w-md mx-auto">
        Visual growth charts and popularity indices will populate here automatically once trekkers begin booking slots and completing routes.
      </p>
    </div>

    <div v-else class="row g-4 mb-4">
      
      <div class="col-lg-8">
        <div class="analytics-glass-container p-4 p-md-5 rounded-4 shadow-sm h-100">
          <h6 class="fw-bold tracking-tight mb-4 border-bottom border-white border-opacity-10 pb-2">6-Month Booking Velocity</h6>
          <div class="chart-canvas-wrapper position-relative" style="height: 280px;">
            <canvas ref="trendChartCanvas"></canvas>
          </div>
        </div>
      </div>

      <div class="col-lg-4">
        <div class="analytics-glass-container p-4 p-md-5 rounded-4 shadow-sm h-100 d-flex flex-column">
          <h6 class="fw-bold tracking-tight mb-4 border-bottom border-white border-opacity-10 pb-2">Most Popular Routes</h6>
          
          <div class="chart-canvas-wrapper position-relative flex-grow-1 d-flex align-items-center justify-content-center">
            <canvas ref="popularityChartCanvas"></canvas>
          </div>

          <div class="mt-4 pt-3 border-top border-white border-opacity-10 d-flex flex-column gap-2 fs-9 text-white-50">
            <div v-for="(item, idx) in stats.charts.popular" :key="idx" class="d-flex justify-content-between">
              <span class="text-truncate pe-2"><i class="bi bi-pin-map-fill"></i> {{ item.name }}</span>
              <strong class="text-white">{{ item.bookings }}</strong>
            </div>
          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { useAlertStore } from '../../stores/alert'
import Chart from 'chart.js/auto'

const authStore = useAuthStore()
const alertStore = useAlertStore()
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

const trendChartCanvas = ref(null)
const popularityChartCanvas = ref(null)
let trendChartInstance = null
let popChartInstance = null

// Initial Zero-State Baseline
const stats = ref({
  counters: { treks: 0, trekkers: 0, staff: 0, bookings: 0 },
  insights: { global_avg_rating: 0.0, top_trek: null, top_staff: null },
  charts: { has_data: false, trends: [], popular: [] }
})

async function fetchRealDataMetrics() {
  try {
    const res = await fetch(`${BACKEND_URL}/api/admin/dashboard/stats`, {
      method: 'GET', headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    
    if (res.ok) {
      const data = await res.json()
      stats.value = data
      
      // If true data exists, wait for DOM to un-hide the canvases, then draw
      if (data.charts.has_data) {
        await nextTick()
        renderCharts(data.charts.trends, data.charts.popular)
      }
    }
  } catch (err) {
    alertStore.showAlert(`Dashboard Sync Error: ${err.message}`, 'danger')
  }
}

function renderCharts(trendData, popularData) {
  // Destroy old instances to prevent hover-glitches when hot-reloading
  if (trendChartInstance) trendChartInstance.destroy()
  if (popChartInstance) popChartInstance.destroy()

  // 1. Line Chart
  if (trendChartCanvas.value) {
    trendChartInstance = new Chart(trendChartCanvas.value, {
      type: 'line',
      data: {
        labels: trendData.map(t => t.month),
        datasets: [{
          label: 'Bookings',
          data: trendData.map(t => t.count),
          borderColor: '#7bf1a8',
          backgroundColor: 'rgba(123, 241, 168, 0.15)',
          borderWidth: 2,
          tension: 0.4,
          fill: true,
          pointBackgroundColor: '#ffffff',
          pointRadius: 4
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: 'rgba(255,255,255,0.5)' } },
          y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: 'rgba(255,255,255,0.5)', stepSize: 1 } }
        }
      }
    })
  }

  // 2. Doughnut Chart
  if (popularityChartCanvas.value && popularData.length > 0) {
    popChartInstance = new Chart(popularityChartCanvas.value, {
      type: 'doughnut',
      data: {
        labels: popularData.map(p => p.name),
        datasets: [{
          data: popularData.map(p => p.bookings),
          backgroundColor: ['rgba(25, 135, 84, 0.8)', 'rgba(123, 241, 168, 0.6)', 'rgba(255, 255, 255, 0.2)'],
          borderColor: 'transparent',
          borderWidth: 0
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        cutout: '75%' 
      }
    })
  }
}

onMounted(() => {
  fetchRealDataMetrics()
})
</script>

<style scoped>
.text-shadow-deep { text-shadow: 0 4px 15px rgba(0, 0, 0, 0.3); }
.max-w-lg { max-width: 650px; }
.max-w-md { max-width: 450px; }

/* Custom Action Buttons */
.btn-glass-action {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.2s;
}
.btn-glass-action:hover { background: rgba(255, 255, 255, 0.2); border-color: rgba(255, 255, 255, 0.4); }

/* Core Metrics Spacing */
.stats-glass-card {
  background: rgba(255, 255, 255, 0.05) !important;
  backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
}
.metric-icon { font-size: 1.5rem; background: rgba(255,255,255,0.06); padding: 8px; border-radius: 10px; }
.card-title-lbl { font-size: 0.72rem; color: rgba(255,255,255,0.5); font-weight: 600; }

/* Insights Spacing */
.insight-glass-card {
  background: rgba(255, 255, 255, 0.03) !important;
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  height: 100%;
}

/* Charts Spacing */
.analytics-glass-container {
  background: rgba(255, 255, 255, 0.03) !important;
  backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

.empty-data-glass { background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(10px); }

.fw-black { font-weight: 900; }
.uppercase { text-transform: uppercase; }
.tracking-tighter { letter-spacing: -1.5px; }
.tracking-wider { letter-spacing: 0.8px; }
.italic { font-style: italic; }

.fs-8 { font-size: 0.88rem; }
.fs-9 { font-size: 0.76rem; }
</style>