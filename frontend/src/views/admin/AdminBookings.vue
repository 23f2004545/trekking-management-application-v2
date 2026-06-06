<template>
  <div class="admin-bookings-viewport text-white text-start pb-5 animate-fade-in px-3">
    
    <div v-if="!activeAuditDetail" class="mb-4">
      <h2 class="fw-bold tracking-tight m-0">Global Explorer Passports</h2>
      <p class="m-0 text-white-50 fs-8 mt-1">Audit active reservations parameters, inspect timeline flags, or track completed loops feedback.</p>
    </div>

    <div v-if="!activeAuditDetail" class="d-flex flex-column gap-3">
      <div v-for="item in globalBookings" :key="item.booking_id" class="booking-rect-row p-3 rounded-4 border border-white border-opacity-10 d-flex flex-wrap align-items-center justify-content-between gap-3 shadow-sm">
        
        <div class="d-flex align-items-center gap-3">
          <img :src="BACKEND_URL + item.trekker.profile_pic" alt="Trekker" class="rect-profile-img shadow" />
          <div>
            <span class="extra-small text-info opacity-40 uppercase tracking-wider">BOOKING ID : #APX-B{{ item.booking_id }}</span>
            <h5 class="fw-bold m-0 text-white tracking-tight mt-0.5">Trek : {{ item.trek_name }}</h5>
            <p class="m-0 fs-9 text-white-50 mt-0.5">User : <span class=" fw-bold">{{ item.trekker.name }}</span> </p>
            <p class="m-0 fs-9 text-white-50 mt-0.5"> Booking Date : {{ item.booking_date }}</p>
          </div>
        </div>

        <div class="d-flex align-items-center gap-4">
          <span class="badge lifecycle-tag text-uppercase fs-9" :class="item.booking_status.toLowerCase()">
            ● {{ item.booking_status }}
          </span>
          <button @click="loadDeepAuditPassport(item.booking_id)" class="btn btn-sm btn-success rounded-pill px-4 py-2 fs-8 fw-bold text-dark">
            View Details
          </button>
        </div>

      </div>
    </div>

    <div v-else class="immersive-deep-audit-panel max-w-4xl mx-auto">
      <div class="mb-4 d-flex justify-content-between align-items-center">
        <button @click="activeAuditDetail = null" class="btn btn-sm btn-outline-light rounded-pill px-3 fs-9 border-opacity-25">← Close Audit</button>
        <span class="badge lifecycle-tag text-uppercase fs-8" :class="activeAuditDetail.booking_status.toLowerCase()">● Status Timeline: {{ activeAuditDetail.booking_status }}</span>
      </div>

      <div v-if="activeAuditDetail.booking_status === 'Cancelled'" class="alert alert-danger p-4 rounded-4 border border-danger border-opacity-20 bg-danger bg-opacity-10 mb-4 animate-scale-up">
        <h6 class="fw-bold m-0 text-white tracking-tight"><i class="bi bi-exclamation-triangle text-warning"></i> SECURITY DEACTIVATION STATEMENT LOG</h6>
        <p class="m-0 fs-8 text-white-50 mt-2"><strong>Revocation Date:</strong> {{ activeAuditDetail.cancelled_date }}</p>
        <p class="m-0 fs-8 text-white-50 mt-1"><strong>Reason Column:</strong> {{ activeAuditDetail.cancelled_reason }}</p>
      </div>

      <div class="glass-audit-card p-4 rounded-4 border border-white border-opacity-10 mb-4 shadow-sm">
        <h6 class="fw-bold small tracking-wider text-uppercase text-success mb-3">1. Expedition Trail Specifications</h6>
        <div class="row g-3 fs-8 text-white-50">
          <div class="col-sm-6">Name Coordinate: <strong class="text-white">{{ activeAuditDetail.trek.name }}</strong></div>
          <div class="col-sm-6">Ecosystem Location: <strong class="text-white"><i class="bi bi-geo-alt"></i> {{ activeAuditDetail.trek.location }}</strong></div>
          <div class="col-sm-6">Schedule Bounds: <strong class="text-white"><i class="bi bi-calendar"></i> {{ activeAuditDetail.trek.schedule }}</strong></div>
          <div class="col-sm-6">Difficulty Intensity: <strong class="text-white">{{ activeAuditDetail.trek.difficulty }}</strong></div>
        </div>
      </div>

      <div class="glass-audit-card p-4 rounded-4 border border-white border-opacity-10 mb-4 shadow-sm text-center bg-white bg-opacity-5">
        <span class="fs-9 text-white-50 opacity-40 d-block tracking-widest text-uppercase">AUTHENTICATED LEDGER REFERENCE TOKEN</span>
        <h3 class="fw-black text-white m-0 my-1 tracking-tighter fs-2">#APX-B{{ activeAuditDetail.booking_id }}</h3>
        <p class="m-0 fs-9 text-success fw-medium">Secure Payment Verified On: {{ activeAuditDetail.booking_date }}</p>
      </div>

      <div class="glass-audit-card p-4 rounded-4 border border-white border-opacity-10 mb-4 shadow-sm">
        <h6 class="fw-bold small tracking-wider text-uppercase opacity-50 mb-3 border-bottom border-white border-opacity-10 pb-1">2. Registered Explorer Telemetry</h6>
        <div class="d-flex align-items-center gap-3">
          <img :src="BACKEND_URL + activeAuditDetail.trekker.profile_pic" alt="Trekker Avatar" class="audit-avatar-circle" />
          <div class="fs-8 text-white-50">
            <h5 class="fw-bold text-white m-0 mb-1">{{ activeAuditDetail.trekker.name }}</h5>
            <div>Trekker Email: <span class="text-white">{{ activeAuditDetail.trekker.email }}</span></div>
            <div class="mt-0.5">Contact: <span class="text-success">{{ activeAuditDetail.trekker.contact }}</span></div>
          </div>
        </div>
      </div>

      <div class="glass-audit-card p-4 rounded-4 border border-white border-opacity-10 mb-4 shadow-sm">
        <h6 class="fw-bold small tracking-wider text-uppercase opacity-50 mb-3 border-bottom border-white border-opacity-10 pb-1">3. Assigned Trail Guide Node</h6>
        <div class="d-flex align-items-center gap-3">
          <img :src="BACKEND_URL + (activeAuditDetail.staff.profile_pic || '/static/Profile_pics/trek_staff.png')" alt="Staff Avatar" class="audit-avatar-circle" />
          <div class="fs-8 text-white-50">
            <h5 class="fw-bold text-white m-0 mb-1">{{ activeAuditDetail.staff.name }}</h5>
            <div>Guide Email: <span class="text-white">{{ activeAuditDetail.staff.email }}</span></div>
            <div class="mt-0.5">Contact: <span class="text-success">{{ activeAuditDetail.staff.contact }}</span></div>
          </div>
        </div>
      </div>

      <div class="glass-audit-card p-4 rounded-4 border border-white border-opacity-10 shadow-sm">
        <h6 class="fw-bold small tracking-wider text-uppercase opacity-50 mb-3 border-bottom border-white border-opacity-10 pb-1">4. Post-Trip Evaluation Logs</h6>
        
        <div v-if="!activeAuditDetail.review.exists" class="text-white-50 opacity-40 italic small text-center py-3">
           No post-expedition review lines submitted by this trekker coordinate block yet.
        </div>
        
        <div v-else class="row g-3 fs-8 text-white-50">
          <div class="col-md-6 border-end border-white border-opacity-10">
            <div class="d-flex align-items-center justify-content-between mb-1 text-white">
              <strong class="tracking-tight">Route Feedback</strong>
              <span class="text-warning small">{{ '★'.repeat(activeAuditDetail.review.trek_stars) }}</span>
            </div>
            <p class="m-0 fs-9 italic">"{{ activeAuditDetail.review.trek_text }}"</p>
          </div>
          <div class="col-md-6">
            <div class="d-flex align-items-center justify-content-between mb-1 text-white">
              <strong class="tracking-tight">Guide Evaluation</strong>
              <span class="text-warning-tint small">{{ '★'.repeat(activeAuditDetail.review.staff_stars) }}</span>
            </div>
            <p class="m-0 fs-9 italic">"{{ activeAuditDetail.review.staff_text }}"</p>
          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAlertStore } from '../../stores/alert'
import { useAuthStore } from '../../stores/auth'

const alertStore = useAlertStore()
const authStore = useAuthStore()

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
const globalBookings = ref([])
const activeAuditDetail = ref(null)

async function fetchGlobalBookingsDataset() {
  try {
    const res = await fetch(`${BACKEND_URL}/api/admin/bookings`, {
      method: 'GET', headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    if (res.ok) globalBookings.value = await res.json()
  } catch (err) { alertStore.showAlert(`Sync error: ${err.message}`, 'danger') }
}

async function loadDeepAuditPassport(id) {
  try {
    const res = await fetch(`${BACKEND_URL}/api/admin/bookings/${id}/details`, {
      method: 'GET', headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    if (res.ok) activeAuditDetail.value = await res.json() 
  } catch (err) { alertStore.showAlert('Audit retrieval failure.', 'danger') }
}

// function getAbsoluteUrl(path) {
//   if (!path) return `${BACKEND_URL}/static/Profile_pics.trekker.png`
//   return path.startsWith('http') ? path : `${BACKEND_URL} + path`
// }

onMounted(() => { fetchGlobalBookingsDataset() })
</script>

<style scoped>
.booking-rect-row { background: rgba(255, 255, 255, 0.04) !important; backdrop-filter: blur(20px); }
.glass-audit-card { background: rgba(255, 255, 255, 0.05) !important; backdrop-filter: blur(25px); border: 1px solid rgba(255, 255, 255, 0.12) !important; }
.rect-profile-img { width: 52px; height: 52px; border-radius: 50%; object-fit: cover; }
.audit-avatar-circle { width: 70px; height: 70px; border-radius:50%; object-fit: cover; border: 1px solid rgba(255,255,255,0.15); }

/* Lifecycle color indices layout definitions */
.lifecycle-tag { padding: 4px 12px; border-radius: 20px; font-weight: 600; }
.lifecycle-tag.upcoming { background: rgba(255, 193, 7, 0.15); color: #ffe066; border: 1px solid rgba(255, 193, 7, 0.3); }
.lifecycle-tag.ongoing { background: rgba(25, 135, 84, 0.18); color: #7bf1a8; border: 1px solid rgba(25, 135, 84, 0.3); }
.lifecycle-tag.completed { background: rgba(0, 123, 255, 0.15); color: #7cd1ff; border: 1px solid rgba(0, 123, 255, 0.25); }
.lifecycle-tag.cancelled { background: rgba(220, 53, 69, 0.15); color: #ff8787; border: 1px solid rgba(220, 53, 69, 0.25); }

.text-warning-tint { color: #ffe066; } .italic { font-style: italic; } .tracking-tighter { letter-spacing: -1.2px; }
.fs-2 { font-size: 2.2rem; } .fs-8 { font-size: 0.88rem; } .fs-9 { font-size: 0.76rem; } .extra-small { font-size: 0.68rem; }
</style>