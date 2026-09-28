<template>
  <div class="history-canvas text-white text-start pb-5 animate-fade-in p-3 p-md-4">

    <div v-if="!onboarded" class="onboarding-glass-banner p-4 rounded-4 mb-4 border border-warning border-opacity-25 d-flex flex-column flex-md-row align-items-md-center justify-content-between gap-3 animate-slide-down">
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

    <!-- ===================================================================
         VIEW 1: MASTER ARCHIVE LISTING
         =================================================================== -->
    <div v-if="!selectedTripForDetails" class="master-list-flow">
      
      <div class="mb-4 border-bottom border-white border-opacity-10 pb-4 d-flex justify-content-between align-items-end flex-wrap gap-2">
        <div>
          <span class="badge border border-white border-opacity-20 rounded-pill px-3 py-1 fs-10 text-success-tint tracking-widest uppercase mb-2">IMMUTABLE ARCHIVES</span>
          <h2 class="fw-bold tracking-tight m-0">Historical Route Analytics</h2>
          <p class="m-0 text-white-50 fs-8 mt-1">Select a completed expedition cohort to inspect financial yields and trail feedback.</p>
        </div>
        <div class="col-md-3">
          <div class="search-box px-3 py-1.5 rounded-3 d-flex align-items-center">
            <span class="me-2 text-white-50 opacity-50"><i class="bi bi-search"></i></span>
            <input v-model="query" type="text" placeholder="Search by Trek name" class="bg-transparent border-0 text-white w-100 fs-8 clean-field">
          </div>
        </div>
      </div>

      <div :class="{ 'onboarding-blurred-zone': !onboarded }">
      <!-- Empty State -->
      <div v-if="filteredData.length === 0" class="text-center py-5 my-5 glass-card-clean rounded-4 border border-white border-opacity-5">
        <span class="fs-1 opacity-25 d-block mb-2">🏔️</span>
        <h6 class="fw-bold text-white tracking-widest uppercase">No Archived Logs Found</h6>
        <p class="text-white-50 fs-9 m-0">No completed expeditions match your current security clearance.</p>
      </div>

        <!-- Card Grid -->
        <div v-else class="row g-3">
          <div v-for="trek in filteredData" :key="trek.trek_id + trek.trek_info.start_date" class="col-md-6 col-xl-4">
            <div @click="selectedTripForDetails = trek" class="glass-summary-card p-4 rounded-4 border border-white border-opacity-10 cursor-pointer hover-emerald position-relative overflow-hidden d-flex flex-column justify-content-between" style="min-height: 10rem;">
              
              <div>
                <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
                  <h5 class="fw-bold m-0 tracking-tight text-white line-clamp-1">{{ trek.trek_info.name }}</h5>
                  <span class="badge bg-success bg-opacity-15 border border-success border-opacity-25 rounded-pill px-2 py-1 fs-10 flex-shrink-0" :class="trek.trek_info.status == 'Completed' ? 'bg-success text-success-tint' : 'bg-danger' ">{{ trek.trek_info.status }}</span>
                </div>
                <p class="fs-9 text-white-50 m-0"><i class="bi bi-geo-alt-fill text-success-tint me-1"></i> {{ trek.trek_info.location }}</p>
              </div>

              <div class="pt-2 mt-2 border-top border-white border-opacity-10 d-flex justify-content-between align-items-center">
                <span class="fs-10 font-monospace text-white-50">{{ trek.trek_info.start_date }} ➔ {{ trek.trek_info.end_date }}</span>
                <span class="fs-9 fw-bold text-success-tint d-flex align-items-center gap-1">Inspect <i class="bi bi-arrow-right"></i></span>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ===================================================================
         VIEW 2: DETAILED CASCADING TELEMETRY
         =================================================================== -->
    <div v-else class="extended-history-details-flow animate-fade-in">
      
      <!-- Top Navigation Bar -->
      <div class="d-flex flex-wrap justify-content-between align-items-center mb-4 pb-3 border-bottom border-white border-opacity-10 gap-3">
        <button @click="selectedTripForDetails = null" class="btn btn-sm btn-outline-light rounded-pill px-2 py-1 fs-9 border-opacity-25 hover-white">
          ← Return to Archives
        </button>
        <button v-if="selectedTripForDetails.trek_info.status == 'Completed'" @click="triggerExport" :disabled="isExporting" class="btn btn-sm btn-success rounded-pill px-4 py-2 fs-9 fw-bold text-dark shadow-sm d-flex align-items-center gap-2 transition-all">
          <span v-if="isExporting" class="spinner-border spinner-border-sm" role="status"></span>
          <i v-else class="bi bi-cloud-arrow-down-fill fs-8"></i> 
          {{ isExporting ? 'Transmitting...' : 'Export Telemetry Data' }}
        </button>
      </div>

        <!-- Trek Cancelled Card -->
        <div class="row g-4">
          <div v-if="selectedTripForDetails.trek_info.status == 'Cancelled'" class="col-lg-12">
            <div class="glass-card-clean p-4 p-md-5 rounded-4 h-100 border border-danger border-opacity-25 d-flex flex-column justify-content-between">
              <div>
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <!-- Updated badge to reflect cancelled status with danger coloring -->
                  <span class="badge bg-danger bg-opacity-10 border border-danger border-opacity-25 rounded-pill px-3 py-1 fs-10 tracking-widest text-danger">CANCELLED EXPEDITION</span>
                  <span class="fs-8 fw-bold text-danger"><i class="bi bi-x-circle-fill me-1"></i>ABORTED</span>
                </div>
                
                <h2 class="fw-bold text-white tracking-tight mb-1">{{ selectedTripForDetails.trek_info.name }}</h2>
                <p class="fs-9 text-white-50 mb-3"><i class="bi bi-geo-alt-fill text-white-50 me-1"></i> {{ selectedTripForDetails.trek_info.location }}</p>

                <!-- Dedicated Cancellation Reason Box -->
                <div class="bg-danger bg-opacity-10 border border-danger border-opacity-20 rounded-3 p-3 mb-4 pe-lg-4">
                  <span class="d-block fs-10 text-danger tracking-widest mb-1"><i class="bi bi-exclamation-triangle me-1"></i>REASON FOR CANCELLATION</span>
                  <p class="text-white-50 fs-9 lh-base mb-0">{{ selectedTripForDetails.cancellation_reason }}</p>
                </div>
              </div>
              
              <div class="row g-3 border-top border-white border-opacity-10 pt-4 font-monospace">
                <!-- Added Cancellation Date -->
                <div class="col-6 col-sm-3">
                  <span class="d-block fs-10 text-white-50 tracking-widest">CANCELLED ON</span>
                  <strong class="fs-8 text-white">{{ selectedTripForDetails.cancellation_date }}</strong>
                </div>
                
                <!-- Impacted Participants -->
                <div class="col-6 col-sm-3">
                  <span class="d-block fs-10 text-white-50 tracking-widest">IMPACTED PAX</span>
                  <strong class="fs-8 text-white">{{ selectedTripForDetails.analytics.cancelled_participants }}</strong>
                </div>
                
                <!-- Estimated Revenue Loss (Calculated inline) -->
                <div class="col-12 col-sm-6">
                  <span class="d-block fs-10 text-white-50 tracking-widest">EST. REVENUE LOSS</span>
                  <strong class="fs-8 text-danger">₹{{ selectedTripForDetails.analytics.cancelled_participants * selectedTripForDetails.trek_info.price }}</strong>
                </div>
                
                <!-- Original Dates (Added text-decoration-line-through to show they are no longer valid) -->
                <div class="col-6 col-sm-6">
                  <span class="d-block fs-10 text-white-50 tracking-widest">ORIGINAL DEPARTURE</span>
                  <strong class="fs-9 text-white-50 text-decoration-line-through">{{ selectedTripForDetails.trek_info.start_date }}</strong>
                </div>
                <div class="col-6 col-sm-6">
                  <span class="d-block fs-10 text-white-50 tracking-widest">ORIGINAL CONCLUSION</span>
                  <strong class="fs-9 text-white-50 text-decoration-line-through">{{ selectedTripForDetails.trek_info.end_date }}</strong>
                </div>
              </div>
            </div>
          </div>

        <div v-else class="row g-4">
          <!-- Trek Meta Card -->
          <div class="col-lg-7">
            <div class="glass-card-clean p-4 p-md-5 rounded-4 h-100 border border-white border-opacity-10 d-flex flex-column justify-content-between">
              <div>
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <span class="badge bg-white bg-opacity-10 border border-white border-opacity-20 rounded-pill px-3 py-1 fs-10 tracking-widest text-white-50">SECTOR ARCHIVE</span>
                  <span class="fs-8 fw-bold text-warning">{{ selectedTripForDetails.trek_info.difficulty }}</span>
                </div>
                <h2 class="fw-bold text-white tracking-tight mb-1">{{ selectedTripForDetails.trek_info.name }}</h2>
                <p class="fs-9 text-white-50 mb-2"><i class="bi bi-geo-alt-fill text-success-tint me-1"></i> {{ selectedTripForDetails.trek_info.location }}</p>
                <p class="text-white-50 fs-9 lh-base mb-4 pe-lg-4">{{ selectedTripForDetails.trek_info.description }}</p>
              </div>
              
              <div class="row g-3 border-top border-white border-opacity-10 pt-4 font-monospace">
                <div class="col-6 col-sm-4"><span class="d-block fs-10 text-white-50 tracking-widest">DURATION</span><strong class="fs-8 text-white">{{ selectedTripForDetails.trek_info.duration }} Days</strong></div>
                <div class="col-6 col-sm-4"><span class="d-block fs-10 text-white-50 tracking-widest">ALTITUDE</span><strong class="fs-8 text-white">{{ selectedTripForDetails.trek_info.altitude }}m</strong></div>
                <div class="col-12 col-sm-4"><span class="d-block fs-10 text-white-50 tracking-widest">YIELD RATE</span><strong class="fs-8 text-success-tint">₹{{ selectedTripForDetails.trek_info.price }}/pax</strong></div>
                <div class="col-6 col-sm-6"><span class="d-block fs-10 text-white-50 tracking-widest">DEPARTURE</span><strong class="fs-9 text-white-50">{{ selectedTripForDetails.trek_info.start_date }}</strong></div>
                <div class="col-6 col-sm-6"><span class="d-block fs-10 text-white-50 tracking-widest">CONCLUSION</span><strong class="fs-9 text-white-50">{{ selectedTripForDetails.trek_info.end_date }}</strong></div>
              </div>
            </div>
          </div>

          <!-- Operational Yield Card -->
          <div class="col-lg-5">
            <div class="glass-card-emerald p-4 rounded-4 h-100 border border-success border-opacity-25 d-flex flex-column justify-content-between">
              <h6 class="fw-bold fs-10 tracking-widest text-success-tint text-uppercase mb-3 pb-2 border-bottom border-success border-opacity-20 d-flex align-items-center gap-2">
                <i class="bi bi-graph-up-arrow fs-8"></i> Operational Yield
              </h6>
              <div class="d-flex flex-column gap-4 my-auto font-monospace">
                <div class="d-flex justify-content-between align-items-center p-2 bg-success bg-opacity-10 rounded-3 border border-white border-opacity-5">
                  <span class="fs-9 text-white-50">Gross Revenue</span><strong class="fs-6 text-success-tint">₹{{ selectedTripForDetails.analytics.total_revenue.toLocaleString() }}</strong>
                </div>
                <div class="d-flex justify-content-between align-items-center p-2 rounded-3  border border-white border-opacity-5">
                  <span class="fs-9 text-white-50">Distinct Passports</span><strong class="fs-6 text-white">{{ selectedTripForDetails.analytics.accounts_booked }}</strong>
                </div>
                <div class="d-flex justify-content-between align-items-center p-2 rounded-3 border border-white border-opacity-5">
                  <span class="fs-9 text-white-50">Pax Cleared</span><strong class="fs-6 text-white">{{ selectedTripForDetails.analytics.completed_participants }}</strong>
                </div>
                <div class="d-flex justify-content-between align-items-center p-2 rounded-3 bg-danger bg-opacity-10 border border-danger border-opacity-25">
                  <span class="fs-9 text-danger-tint">Cancelled Slots</span><strong class="fs-6 text-danger-tint">{{ selectedTripForDetails.analytics.cancelled_participants }}</strong>
                </div>
              </div>
              <div class="text-end mt-2"><span class="fs-10 text-white-50 uppercase tracking-widest">Completion Rate: {{ selectedTripForDetails.analytics.completion_rate }}%</span></div>
            </div>
          </div>

          <!-- Manifest Log Card -->
          <div class="col-lg-12">
            <div class="glass-card-clean p-4 rounded-4 h-100 border border-white border-opacity-10 d-flex flex-column">
              <h6 class="fw-bold fs-10 tracking-widest text-white-50 text-uppercase mb-3 pb-2 border-bottom border-white border-opacity-10 d-flex justify-content-between align-items-center">
                <span>Manifest Log</span>
                <span class="font-monospace text-success-tint">{{ selectedTripForDetails.roster.length }} Accounts Logged</span>
              </h6>
              
              <div class="roster-scroll pe-2 flex-grow-1">
                <div v-if="selectedTripForDetails.roster.length === 0" class="text-center py-5 text-white-50 fs-9 italic">No participant records snapshotted.</div>
                <div v-for="(person, idx) in selectedTripForDetails.roster" :key="idx" class="p-3 mb-2 rounded-3 border border-white border-opacity-5 hover-border-subtle">
                  <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-1.5">
                    <h6 class="m-0 fw-bold fs-8 text-white d-flex align-items-center gap-2">
                      {{ person.name }} 
                      <span class="badge bg-white bg-opacity-10 text-white-50 fw-normal font-monospace fs-10 px-2 py-0.5">+{{ person.pax - 1 }} Pax</span>
                    </h6>
                    <span class="fs-10 font-monospace text-success-tint">{{ person.contact }}</span>
                  </div>
                  <span class="fs-10 text-white-50 d-block mb-2 font-monospace">{{ person.email }}</span>
                  <div class="p-2 bg-warning bg-opacity-10 border border-warning border-opacity-20 rounded text-warning fs-10 font-monospace">
                    <i class="bi bi-heart-pulse me-1"></i> Medical: {{ person.medical }}
                  </div>
                </div>
              </div>

            </div>
          </div>

          <!-- Feedback & Reviews Section (Side-by-Side on Desktop) -->
          <div class="col-12">
            <div class="glass-card-clean p-4 p-md-5 rounded-4 border border-white border-opacity-10">
              <div class="row g-5">
                
                <!-- Terrain Feedback -->
                <div class="col-lg-12 border-white border-opacity-10 pe-lg-4">
                  <div class="d-flex justify-content-between align-items-end border-bottom border-white border-opacity-10 pb-2 mb-4">
                    <h6 class="fw-bold fs-10 tracking-widest text-white-50 text-uppercase m-0 d-flex align-items-center gap-2">
                      <i class="bi bi-chat-left-quote text-success-tint fs-8"></i> Terrain Evaluations
                    </h6>
                    <span class="text-warning font-monospace fs-8 fw-bold">{{ selectedTripForDetails.reviews.trek_avg }} ★</span>
                  </div>
                  
                  <div class="d-flex flex-row flex-nowrap gap-3 overflow-x-auto pb-3 custom-scrollbar">
                    <div v-if="!selectedTripForDetails.reviews.trek_list.length" class="text-white-50 fs-9 py-4 italic text-center w-100 rounded-3 border border-white border-opacity-5">No structural terrain logs recorded.</div>
                    <div v-for="rev in selectedTripForDetails.reviews.trek_list" :key="'t'+rev.id" class="comment-bubble p-3 rounded-4 flex-shrink-0 d-flex flex-column justify-content-between">
                      <div class="d-flex justify-content-between align-items-center mb-2 pb-2 border-bottom border-white border-opacity-5">
                        <span class="fs-9 fw-bold text-white text-truncate pe-2">{{ rev.author }}</span>
                        <span class="text-warning fs-10 flex-shrink-0">{{ '★'.repeat(rev.stars) }}</span>
                      </div>
                      <p class="m-0 fs-9 text-white-50 lh-base review-text italic pe-1">"{{ rev.comment }}"</p>
                    </div>
                  </div>
                </div>

                <!-- Commander Feedback -->
                <div class="col-lg-12 ps-lg-4">
                  <div class="d-flex justify-content-between align-items-end border-bottom border-white border-opacity-10 pb-2 mb-4">
                    <h6 class="fw-bold fs-10 tracking-widest text-white-50 text-uppercase m-0 d-flex align-items-center gap-2">
                      <i class="bi bi-person-lines-fill text-success-tint fs-8"></i> Commander Evaluations
                    </h6>
                    <span class="text-warning font-monospace fs-8 fw-bold">{{ selectedTripForDetails.reviews.staff_avg }} ★</span>
                  </div>
                  
                  <div class="d-flex flex-row flex-nowrap gap-3 overflow-x-auto pb-3 custom-scrollbar">
                    <div v-if="!selectedTripForDetails.reviews.staff_list.length" class="text-white-50 fs-9 py-4 italic text-center w-100 rounded-3 border border-white border-opacity-5">No guide performance evaluations logged.</div>
                    <div v-for="rev in selectedTripForDetails.reviews.staff_list" :key="'s'+rev.id" class="comment-bubble p-3 rounded-4 flex-shrink-0 d-flex flex-column justify-content-between">
                      <div class="d-flex justify-content-between align-items-center mb-2 pb-2 border-bottom border-white border-opacity-5">
                        <span class="fs-9 fw-bold text-white text-truncate pe-2">{{ rev.author }}</span>
                        <span class="text-warning fs-10 flex-shrink-0">{{ '★'.repeat(rev.stars) }}</span>
                      </div>
                      <p class="m-0 fs-9 text-white-50 lh-base review-text italic pe-1">"{{ rev.comment }}"</p>
                    </div>
                  </div>
                </div>

              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Interactive Demo Email Delivery Modal -->
    <DemoEmailPromptModal 
      :isOpen="showEmailModal"
      title="Telemetry Export Email Delivery"
      description="Experience Celery background workers and real cloud SMTP delivery by receiving historical telemetry reports in your inbox."
      @close="showEmailModal = false"
      @submit="handleLiveExportSubmit"
      @simulate="handleSimulateExportSubmit"
    />

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { secureFetch } from '../../utils/api.js'
import { useAlertStore } from '../../stores/alert.js'
import { useAuthStore } from '../../stores/auth.js'
import DemoEmailPromptModal from '@/components/DemoEmailPromptModal.vue'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
const authStore = useAuthStore()
const historicalData = ref([])
const alertStore = useAlertStore()
const selectedTripForDetails = ref(null)
const activeDetail = ref(null)
const loading = ref(true)
const onboarded = ref(false)
const isExporting = ref(false)
const showEmailModal = ref(false)
const query = ref('')

console.log(historicalData)
const filteredData = computed(() => {
  return historicalData.value.filter(d => d.trek_info.name.toLowerCase().includes(query.value.toLowerCase()) )
})

async function fetchHistory() {
  try {
    const res = await secureFetch(`${BACKEND_URL}/api/utils/history`)
    if (res.ok) {
      const data = await res.json()
      historicalData.value = data.results
      onboarded.value = data.is_onboarded

      // Automatically select the first item to populate the right column!
      if (historicalData.value.length > 0) activeDetail.value = historicalData.value[0]
    }
  } catch (err) {
    console.error("Failed to aggregate history matrix", err)
  } finally {
    loading.value = false
  }
}

function triggerExport() {
  if (!selectedTripForDetails.value) return
  if (authStore.isDemo) {
    showEmailModal.value = true
    return
  }
  executeExport(null)
}

function handleLiveExportSubmit(email) {
  showEmailModal.value = false
  executeExport(email)
}

function handleSimulateExportSubmit() {
  showEmailModal.value = false
  executeExport(null)
}

async function executeExport(demoDeliveryEmail = null) {
  if (!selectedTripForDetails.value) return
  
  isExporting.value = true
  try {
    const payload = { ...selectedTripForDetails.value }
    if (demoDeliveryEmail) {
      payload.demo_delivery_email = demoDeliveryEmail
    }
    const res = await secureFetch(`${BACKEND_URL}/api/utils/export-history`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    const data = await res.json()
    if (res.ok) {
      alertStore.showAlert(data.message, 'success')
    } else {
      alertStore.showAlert('Export pipeline failed.', 'danger')
    }
  } catch (err) {
    alertStore.showAlert('Network drop during export.', 'danger')
  } finally {
    isExporting.value = false
  }
}

onMounted(() => {
  fetchHistory()
})
</script>

<style scoped>
/* Glassmorphism Tiering */
.glass-summary-card { background: rgba(12, 22, 17, 0.55); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
.hover-emerald:hover { transform: translateY(-5px); border-color: rgba(123, 241, 168, 0.45) !important; background: rgba(16, 30, 22, 0.75); box-shadow: 0 12px 30px rgba(0,0,0,0.4); }

.glass-card-clean { background: rgba(10, 16, 13, 0.6); backdrop-filter: blur(20px); }
.glass-card-obsidian { background: rgba(3, 16, 22, 0.85); backdrop-filter: blur(15px); }
.glass-card-emerald { background: rgba(19, 43, 29, 0.35); backdrop-filter: blur(20px); }
.rect-avatar-img { width: 4rem; height: 4rem; border-radius: 50%; object-fit: cover; }

.search-box { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); }
.clean-field:focus { outline: none; }

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

/* Typography & Colors */
.text-success-tint { color: #7bf1a8; }
.text-danger-tint { color: #ff8787; }
.tracking-widest { letter-spacing: 1.5px; }
.tracking-tight { letter-spacing: -0.5px; }
.fs-10 { font-size: 0.68rem; }
.line-clamp-1 { display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden; }

/* Desktop Split Borders */
@media (min-width: 992px) {
  .border-end-lg { border-right: 1px solid rgba(255, 255, 255, 0.1); }
}

/* Scrollbars & Interactions */
.roster-scroll { max-height: 280px; overflow-y: auto; }
.roster-scroll::-webkit-scrollbar { width: 4px; }
.roster-scroll::-webkit-scrollbar-thumb { background: rgba(123, 241, 168, 0.2); border-radius: 4px; }

.hover-border-subtle { transition: border-color 0.2s; }
.hover-border-subtle:hover { border-color: rgba(255,255,255,0.15) !important; }

/* Review Bubbles */
.comment-bubble { background: rgba(5, 9, 7, 0.6); border: 1px solid rgba(255, 255, 255, 0.06); min-width: 280px; max-width: 280px; height: 150px; }
.review-text { overflow-y: auto; flex-grow: 1; }
.review-text::-webkit-scrollbar { width: 3px; }
.review-text::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.15); border-radius: 4px; }

.custom-scrollbar::-webkit-scrollbar { height: 5px; }
.custom-scrollbar::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); border-radius: 8px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.15); border-radius: 8px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(123, 241, 168, 0.4); }
</style>