<template>
  <div class="historical-audit-viewport text-white text-start animate-fade-in pb-5 px-3">
    
    <!-- COMPACT HISTORICAL ROW LIST ARCHITECTURE -->
    <div v-if="!selectedTripForDetails">
      <div class="mb-4 d-flex justify-content-between flex-wrap gap-3 align-items-start">
        <div>
          <h2 class="fw-bold tracking-tight m-0">Expedition History Logs</h2>
          <p class="m-0 text-white-50 fs-8 mt-1">Review finalized high-alpine routes, evaluate guide staff columns, and audit past data logs.</p>
        </div>
        <button @click="requestCSVExport" class="btn btn-outline-light rounded-pill fs-9 border-opacity-25">
          <i class="bi bi-download"></i>  Export History 
        </button>
      </div>

      <div v-if="historicTrips.length == 0" class="empty-state p-5 text-center rounded-4 border border-white border-opacity-10 bg-opacity-5">
        <span class="fs-1"><i class="bi bi-archive"></i></span>
        <h5 class="fw-bold mt-2">No Archived Logs Found</h5>
        <p class="text-white-50 small m-0">Not completed any trek so far.</p>
      </div>

      <div v-else class="row g-3">
        <div v-for="trip in historicTrips" :key="trip.booking_id" class="col-12">
          <div class="history-glass-row p-3 rounded-3 border border-white border-opacity-10 d-flex align-items-center justify-content-between gap-3">
            <div class="d-flex align-items-center gap-3">
              <div class="icon-shield fs-4 p-2 rounded-2"><i class="bi bi-backpack2-fill text-danger"></i></div>
              <div>
                <span class="badge completed-badge mb-1 text-uppercase fs-9">● Completed</span>
                <h5 class="fw-bold m-0 text-white">{{ trip.trek_name }}</h5>
                <p class="m-0 fs-9 text-white-50 mt-0.5">Departed trail on: {{ trip.booking_date }}</p>
              </div>
            </div>
            <button @click="selectedTripForDetails = trip" class="btn btn-sm btn-success rounded-pill px-4 py-2 fs-8 fw-bold text-dark shadow-sm">
              View 
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- DETAILED SYSTEM CASCADING DEPLOYMENT -->
    <div v-else class="extended-history-details-flow">
      <div class="mb-4">
        <button @click="selectedTripForDetails = null" class="btn btn-outline-light rounded-pill px-3 py-1 fs-9 border-opacity-25">
          <i class="bi bi-arrow-left me-1"></i> Return to History Logs
        </button>
      </div>

      <!-- REUSE CARD A-->
      <TrekDetail :trek="selectedTripForDetails" :showCheckoutButton="false" />

      <!-- REUSE CARD B -->
      <TrekHistory :booking="selectedTripForDetails" @commit-review="handlePublishedReview" />
    </div>

    <!-- Interactive Demo Email Delivery Modal -->
    <DemoEmailPromptModal 
      :isOpen="showEmailModal"
      title="Expedition History CSV Delivery"
      description="Experience Celery background CSV compilation and real cloud SMTP delivery by receiving your expedition matrix directly in your personal inbox."
      @close="showEmailModal = false"
      @submit="handleLiveExportSubmit"
      @simulate="handleSimulateExportSubmit"
    />

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import TrekDetail from '../../components/TrekDetail.vue'
import TrekHistory from '../../components/TrekHistory.vue'
import DemoEmailPromptModal from '@/components/DemoEmailPromptModal.vue'
import { useAlertStore } from '../../stores/alert'
import { useAuthStore } from '../../stores/auth'
import { secureFetch } from '@/utils/api.js'

const alertStore = useAlertStore()
const authStore = useAuthStore()
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

const selectedTripForDetails = ref(null)
const historicTrips = ref([])

async function fetchCompletedHistory() {
  try {
    const res = await secureFetch(`${BACKEND_URL}/api/trekker/history`, {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    if (res.ok) {
      const data = await res.json()
      
      // Resolve image absolute URLs safely
      historicTrips.value = data.map(trip => {
        trip.images = trip.images.map(img => img.startsWith('http') ? img : `${BACKEND_URL}${img}`)
        if (trip.staff.profile_pic && !trip.staff.profile_pic.startsWith('http')) {
          trip.staff.profile_pic = `${BACKEND_URL}${trip.staff.profile_pic}`
        }
        return trip
      })
    }
  } catch (err) {
    alertStore.showAlert('Historical registry sync dropped.', 'danger')
  }
}

async function handlePublishedReview(formData) {
  try {
    const res = await secureFetch(`${BACKEND_URL}/api/trekker/reviews`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        trek_id: selectedTripForDetails.value.trek_id,
        staff_id: selectedTripForDetails.value.staff?.id || null, // Assuming staff ID is attached if needed
        trek_rating: formData.trek_rating,
        trek_comment: formData.trek_comment,
        staff_rating: formData.staff_rating,
        staff_comment: formData.staff_comment
      })
    })
    
    if (res.ok) {
      // Optimistically update the UI to read-only view
      selectedTripForDetails.value.review_submitted = true
      selectedTripForDetails.value.existing_trek_review = { stars: formData.trek_rating, comment: formData.trek_comment }
      selectedTripForDetails.value.existing_staff_review = { stars: formData.staff_rating, comment: formData.staff_comment }
      alertStore.showAlert('Success: Review variables committed to the apex network.', 'success')
    } else {
      const data = await res.json()
      alertStore.showAlert(data.message || 'Review rejection flagged.', 'danger')
    }
  } catch (err) {
    alertStore.showAlert(`Network Drop: ${err.message}`, 'danger')
  }
}

const showEmailModal = ref(false)

function requestCSVExport() {
  if (historicTrips.value.length === 0) {
    alertStore.showAlert('No data to export.', 'warning')
    return 
  }
  if (authStore.isDemo) {
    showEmailModal.value = true
    return
  }
  dispatchExportRequest(null)
}

function handleLiveExportSubmit(email) {
  showEmailModal.value = false
  dispatchExportRequest(email)
}

function handleSimulateExportSubmit() {
  showEmailModal.value = false
  dispatchExportRequest(null)
}

async function dispatchExportRequest(demoDeliveryEmail = null) {
  try {
    alertStore.showAlert('Initializing secure CSV data compilation via background workers...', 'info')
    const payload = demoDeliveryEmail ? { demo_delivery_email: demoDeliveryEmail } : {}
    const res = await secureFetch(`${import.meta.env.VITE_BACKEND_URL}/api/trekker/export-history`, {
      method: 'POST',
      headers: { 
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })
    const data = await res.json()
    if (res.ok) {
      alertStore.showAlert(data.message, 'success')
    } else {
      alertStore.showAlert(data.message || 'Export failed.', 'danger')
    }
  } catch (err) {
    alertStore.showAlert(`Export drop: ${err.message}`, 'danger')
  }
}

onMounted(() => {
  fetchCompletedHistory()
})
</script>

<style scoped>
.history-glass-row { background: rgba(255, 255, 255, 0.05) !important; backdrop-filter: blur(15px); }
.icon-shield { background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.1); }
.completed-badge { background: rgba(0, 123, 255, 0.15); color: #7cd1ff; border: 1px solid rgba(0, 123, 255, 0.25); }
.fs-8 { font-size: 0.88rem; }
.fs-9 { font-size: 0.76rem; }
</style>