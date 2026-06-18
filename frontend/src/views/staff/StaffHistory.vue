<template>
  <div class="history-canvas text-white text-start pb-5 animate-fade-in p-3">

    <div v-if="!selectedTripForDetails" class="master-list-flow">
      
      <div class="mb-4 border-bottom border-white border-opacity-10 pb-4">
        <h2 class="fw-bold tracking-tight m-0">Historical Route Analytics</h2>
        <p class="m-0 text-white-50 fs-8 mt-1">Select an archived expedition to review operational yields and feedback.</p>
      </div>

      <div class="row g-3">
        <div v-for="trek in historicalData" :key="trek.trek_id" class="col-md-6 col-xl-4">
          <div  @click="selectedTripForDetails = trek" class="glass-summary-card p-4 rounded-4 border border-white border-opacity-10 cursor-pointer hover-lift">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <h5 class="fw-bold m-0 tracking-tight text-white line-clamp-1">{{ trek.trek_info.name }}</h5>
              <span class="fs-9 text-success-tint border border-success border-opacity-25 bg-success bg-opacity-10 px-2 py-0.5 rounded-pill">Completed</span>
            </div>
            <p class="fs-9 text-white-50 mb-3"><i class="bi bi-geo-alt-fill"></i> {{ trek.trek_info.location }}</p>
            
            <div class="d-flex justify-content-between align-items-center pt-3 border-top border-white border-opacity-10">
              <span class="fs-9 text-white-50">{{ trek.trek_info.start_date }} - {{ trek.trek_info.end_date }}</span>
              <span class="fs-8 fw-semibold text-white">→ View Data</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="extended-history-details-flow animate-fade-in">
      
      <div class="d-flex flex-wrap justify-content-between align-items-center mb-4 pb-3 border-bottom border-white border-opacity-10 gap-3">
        <button @click="selectedTripForDetails = null" class="btn btn-outline-light rounded-pill px-4 py-2 fs-8 border-opacity-25">
          ← Return to Archives
        </button>
        <button class="btn btn-success rounded-pill px-4 py-2 fs-8 fw-bold text-dark shadow-sm">
          <i class="bi bi-cloud-arrow-down-fill me-1"></i> Export Telemetry Data
        </button>
      </div>

      <div class="row g-4">
        
        <div class="col-lg-7">
          <div class="glass-container p-4 rounded-4 h-100 border border-white border-opacity-10">
            <span class="badge bg-white bg-opacity-10 border border-white border-opacity-25 rounded-pill mb-2">ROUTE ARCHIVE</span>
            <h3 class="fw-bold text-white tracking-tight mb-4">{{ selectedTripForDetails.trek_info.name }}</h3>
            
            <div class="row g-4 border-top border-white border-opacity-10 pt-3">
              <div class="col-6 col-sm-4"><span class="d-block fs-10 text-white-50 uppercase tracking-widest">DURATION</span><strong class="fs-8">{{ selectedTripForDetails.trek_info.duration }} Days</strong></div>
              <div class="col-6 col-sm-4"><span class="d-block fs-10 text-white-50 uppercase tracking-widest">ALTITUDE</span><strong class="fs-8">{{ selectedTripForDetails.trek_info.altitude }}m</strong></div>
              <div class="col-6 col-sm-4"><span class="d-block fs-10 text-white-50 uppercase tracking-widest">PRICE RATE</span><strong class="fs-8">₹{{ selectedTripForDetails.trek_info.price }}</strong></div>
              <div class="col-6 col-sm-6"><span class="d-block fs-10 text-white-50 uppercase tracking-widest">DEPARTURE</span><strong class="fs-8">{{ selectedTripForDetails.trek_info.start_date }}</strong></div>
              <div class="col-6 col-sm-6"><span class="d-block fs-10 text-white-50 uppercase tracking-widest">CONCLUSION</span><strong class="fs-8">{{ selectedTripForDetails.trek_info.end_date }}</strong></div>
            </div>
          </div>
        </div>

        <div class="col-lg-5">
          <div class="glass-container p-4 rounded-4 h-100 border border-success border-opacity-25 bg-success bg-opacity-5">
            <h6 class="fw-bold fs-9 tracking-wider opacity-75 text-uppercase mb-3 border-bottom border-success border-opacity-25 pb-2 text-success-tint">Operational Yield</h6>
            <div class="d-flex flex-column gap-3">
              <div class="d-flex justify-content-between align-items-center p-2 rounded bg-black bg-opacity-25 border border-white border-opacity-5">
                <span class="fs-9 text-white-50">Total Revenue</span><strong class="fs-6">{{ selectedTripForDetails.analytics.total_revenue }}</strong>
              </div>
              <div class="d-flex justify-content-between align-items-center p-2 rounded bg-black bg-opacity-25 border border-white border-opacity-5">
                <span class="fs-9 text-white-50">Distinct Accounts</span><strong class="fs-6">{{ selectedTripForDetails.analytics.accounts_booked }}</strong>
              </div>
              <div class="d-flex justify-content-between align-items-center p-2 rounded bg-black bg-opacity-25 border border-white border-opacity-5">
                <span class="fs-9 text-white-50">Explorers Cleared</span><strong class="fs-6">{{ selectedTripForDetails.analytics.completed_participants }}</strong>
              </div>
              <div class="d-flex justify-content-between align-items-center p-2 rounded bg-black bg-opacity-25 border border-danger border-opacity-25">
                <span class="fs-9 text-danger-tint">Cancelled Slots</span><strong class="fs-6 text-danger-tint">{{ selectedTripForDetails.analytics.cancelled_participants }}</strong>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-12">
          <div class="glass-container p-4 rounded-4 h-100 border border-white border-opacity-10">
            <h6 class="fw-bold fs-9 tracking-wider opacity-75 text-uppercase mb-3 border-bottom border-white border-opacity-10 pb-2">Manifest Log ({{ selectedTripForDetails.roster.length }})</h6>
            <div class="roster-scroll pe-2">
              <div v-for="(person, idx) in selectedTripForDetails.roster" :key="idx" class="p-3 mb-2 rounded-3 bg-black bg-opacity-25 border border-white border-opacity-5">
                <div class="d-flex flex-wrap justify-content-between align-items-start gap-2 mb-2">
                  <div>
                    <h6 class="m-0 fw-semibold fs-8">{{ person.name }} <span class="badge bg-white bg-opacity-10 text-white-50 ms-2 fw-normal">+{{ person.pax - 1 }} Pax</span></h6>
                    <span class="fs-9 text-white-50">{{ person.email }} · {{ person.contact }}</span>
                  </div>
                </div>
                <!-- <div class="p-2 bg-warning bg-opacity-10 border border-warning border-opacity-25 rounded text-warning-tint fs-9 italic">
                  <i class="bi bi-heart-pulse me-1"></i> Medical Instructions : {{ person.medical }}
                </div> -->
              </div>
            </div>
          </div>
        </div>

        <div class="col-12">
          <div class="glass-container p-4 rounded-4 border border-white border-opacity-10">
            <div class="row g-5">
              
              <div class="col-lg-12">
                <div class="d-flex justify-content-between align-items-end border-bottom border-white border-opacity-10 pb-2 mb-3">
                  <h6 class="fw-bold fs-9 tracking-wider opacity-75 text-uppercase m-0">Terrain Feedback</h6>
                  <span class="text-warning fs-8 fw-bold"> Avg Rating : {{ selectedTripForDetails.reviews.trek_avg }} ★</span>
                </div>
                <div class="d-flex flex-row flex-nowrap gap-3 overflow-x-auto pb-3 custom-scrollbar">
                  <div v-if="!selectedTripForDetails.reviews.trek_list.length" class="text-white-50 fs-9 py-3 italic w-100">No route logs available.</div>
                  <div v-for="rev in selectedTripForDetails.reviews.trek_list" :key="'t'+rev.id" class="comment-bubble p-3 rounded-4 flex-shrink-0 d-flex flex-column">
                    <div class="d-flex justify-content-between mb-2"><span class="fs-9 fw-semibold text-white">{{ rev.author }}</span><span class="text-warning fs-9">{{ '★'.repeat(rev.stars) }}</span></div>
                    <p class="m-0 fs-9 text-white-50 lh-base review-text">"{{ rev.comment }}"</p>
                  </div>
                </div>
              </div>

              <div class="col-lg-12">
                <div class="d-flex justify-content-between align-items-end border-bottom border-white border-opacity-10 pb-2 mb-3">
                  <h6 class="fw-bold fs-9 tracking-wider opacity-75 text-uppercase m-0">Your Feedback</h6>
                  <span class="text-warning fs-8 fw-bold">Avg Rating : {{ selectedTripForDetails.reviews.staff_avg }} ★</span>
                </div>
                <div class="d-flex flex-row flex-nowrap gap-3 overflow-x-auto pb-3 custom-scrollbar">
                  <div v-if="!selectedTripForDetails.reviews.staff_list.length" class="text-white-50 fs-9 py-3 italic w-100">No staff evaluations logged.</div>
                  <div v-for="rev in selectedTripForDetails.reviews.staff_list" :key="'s'+rev.id" class="comment-bubble p-3 rounded-4 flex-shrink-0 d-flex flex-column">
                    <div class="d-flex justify-content-between mb-2"><span class="fs-9 fw-semibold text-white">{{ rev.author }}</span><span class="text-warning fs-9">{{ '★'.repeat(rev.stars) }}</span></div>
                    <p class="m-0 fs-9 text-white-50 lh-base review-text">"{{ rev.comment }}"</p>
                  </div>
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
import { secureFetch } from '../../utils/api.js'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
const historicalData = ref([])
const selectedTripForDetails = ref(null)
const activeDetail = ref(null)
const loading = ref(true)

async function fetchHistory() {
  try {
    const res = await secureFetch(`${BACKEND_URL}/api/utils/history`)
    if (res.ok) {
      historicalData.value = await res.json()
      // Automatically select the first item to populate the right column!
      if (historicalData.value.length > 0) activeDetail.value = historicalData.value[0]
    }
  } catch (err) {
    console.error("Failed to aggregate history matrix", err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchHistory()
})
</script>

<style scoped>
/* Core structural styles */
.glass-summary-card { background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(10px); transition: transform 0.2s; }
.hover-lift:hover { transform: translateY(-4px); border-color: rgba(25, 135, 84, 0.4) !important; }
.glass-container { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(15px); }

/* Typography & Utility */
.uppercase { text-transform: uppercase; }
.tracking-widest { letter-spacing: 1.5px; }
.tracking-tight { letter-spacing: -0.5px; }
.fs-10 { font-size: 0.65rem; }
.text-success-tint { color: #7bf1a8; }
.text-danger-tint { color: #ff8787; }
.text-warning-tint { color: #ffda6a; }

/* Scrollbars & Interactions */
.roster-scroll { max-height: 250px; overflow-y: auto; }
.roster-scroll::-webkit-scrollbar { width: 4px; }
.roster-scroll::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 4px; }

/* Review Bubbles */
.comment-bubble { background: rgba(0, 0, 0, 0.2); border: 1px solid rgba(255, 255, 255, 0.05); min-width: 260px; max-width: 260px; height: 140px; }
.review-text { overflow-y: auto; flex-grow: 1; padding-right: 6px; }
.review-text::-webkit-scrollbar { width: 4px; }
.review-text::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 4px; }

.custom-scrollbar::-webkit-scrollbar { height: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: rgba(255, 255, 255, 0.02); border-radius: 8px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.15); border-radius: 8px; }
</style>