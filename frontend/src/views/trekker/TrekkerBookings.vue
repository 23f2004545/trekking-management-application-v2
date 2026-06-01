<template>
  <div class="bookings-audit-viewport text-white text-start animate-fade-in pb-5">
    
    <div class="mb-4">
      <h2 class="fw-bold tracking-tight m-0">Active Basecamp Bookings</h2>
      <p class="m-0 text-white-50 fs-8 mt-1">Audit active pass verifications, inspect transaction telemetry statuses, or submit route cancellations.</p>
    </div>

    <!-- MAIN DISPLAY ROW LIST (Keeps minimalist meta presentation layout) -->
    <div class="row g-3">
      <div v-for="book in activeBookingsList" :key="book.booking_id" class="col-12">
        <div class="booking-glass-row p-3 rounded-3 border border-white border-opacity-10 shadow-sm d-flex flex-wrap align-items-center justify-content-between gap-3">
          
          <div class="d-flex align-items-center gap-3">
            <div class="booking-icon-shield fs-4 p-2 rounded-2">🎒</div>
            <div>
              <span class="fs-9 text-white-50 fw-semibold tracking-wider">BOOKING PASS ID: #APX-B{{ book.booking_id }}</span>
              <h5 class="fw-bold m-0 text-white mt-0.5">{{ book.trek_name }}</h5>
              <p class="m-0 fs-9 text-white-50 mt-0.5">Secured on: {{ book.booking_date }}</p>
            </div>
          </div>

          <div class="text-start">
            <span class="d-block fs-9 text-white-50 opacity-50 fw-semibold">PAYMENT PARAMETER</span>
            <span class="badge payment-badge mt-0.5" :class="book.payment_status.toLowerCase()">
              {{ book.payment_status }}
            </span>
          </div>

          <div class="text-start">
            <span class="d-block fs-9 text-white-50 opacity-50 fw-semibold">ROUTE SYSTEM LIFECYCLE</span>
            <span class="badge status-badge mt-0.5" :class="book.booking_status.toLowerCase()">
              ● {{ book.booking_status }}
            </span>
          </div>

          <!-- REFINED BUTTON ZONE: Exactly one single clean programmatic details viewer button -->
          <div class="d-flex align-items-center">
            <button @click="openDeepContextModal(book)" class="btn btn-sm btn-success rounded-pill px-4 py-2 fs-8 fw-bold text-dark shadow-sm">
              View Details
            </button>
          </div>

        </div>
      </div>
    </div>

    <!-- ===================================================================
         IMMERSIVE AUDIT MODAL OVERLAY (With Staff Access Coordinates)
         =================================================================== -->
    <Transition name="modal-fade">
      <div v-if="modalTarget" class="bookings-modal-backdrop d-flex align-items-center justify-content-center p-3">
        <div class="glass-audit-card p-4 p-md-5 rounded-4 border border-white border-opacity-15 shadow-lg position-relative text-start animate-scale-up">
          
          <!-- Circle Cross Dismiss Trigger Button -->
          <button @click="modalTarget = null" class="btn-dismiss-circle-cross" title="Close Context Panel">✕</button>

          <h4 class="fw-bold tracking-tight text-white mb-1">Reservation Passport Context</h4>
          <p class="text-white-50 small mb-4">Complete logistical registry metrics and verified guide assignment info.</p>

          <div class="row g-3">
            <!-- Left Grid Segment: Route thumbnail graphic -->
            <div class="col-md-4">
              <div class="modal-thumbnail-wrapper rounded-3 overflow-hidden border border-white border-opacity-10 h-100">
                <img :src="modalTarget.trek_image" alt="Trek Layout Thumbnail" class="w-100 h-100 object-cover" />
              </div>
            </div>

            <!-- Right Grid Segment: Multi-column meta specification rows -->
            <div class="col-md-8 fs-8 d-flex flex-column gap-2 bg-opacity-5 p-3 rounded-3 border border-white border-opacity-5">
              <div><strong>Booking ID Key:</strong> <span class="text-white-50">#APX-B{{ modalTarget.booking_id }}</span></div>
              <div><strong>Expedition Trail Name:</strong> <span class="text-white fw-bold">{{ modalTarget.trek_name }}</span></div>
              <div><strong>Trail Duration Matrix:</strong> <span class="text-white-50">{{ modalTarget.duration_days }} Days</span></div>
              <div><strong>Reservation Logged Date:</strong> <span class="text-white-50">{{ modalTarget.booking_date }}</span></div>
              <div><strong>Group Headcount Size:</strong> <span class="text-white-50 text-success fw-bold">{{ modalTarget.total_people }} Explorers</span></div>
              <div><strong>Financial Status:</strong> <span class="badge payment-badge" :class="modalTarget.payment_status.toLowerCase()">{{ modalTarget.payment_status }}</span></div>
              <div><strong>Lifecycle State Flag:</strong> <span class="badge status-badge" :class="modalTarget.booking_status.toLowerCase()">● {{ modalTarget.booking_status }}</span></div>
            </div>

            <!-- Full Width Verified Guide Contact Info Cluster Box -->
            <div class="col-12 mt-2">
              <h6 class="fw-bold small tracking-wider opacity-50 text-uppercase mb-2 border-bottom border-white border-opacity-5 pb-1">Assigned Guide Assignment Node</h6>
              <div class="staff-contact-glass p-3 rounded-3 border border-white border-opacity-10 d-flex flex-column gap-1.5 fs-8">
                <div>👨‍✈️ <strong>Guide Leader Name:</strong> <span class="text-white fw-medium">{{ modalTarget.staff.name }}</span></div>
                <div>✉️ <strong>Emergency Comm Registry:</strong> <span class="text-success-tint">{{ modalTarget.staff.email }}</span></div>
                <div>📞 <strong>Secure Satellite Contact:</strong> <span class="text-success-tint">{{ modalTarget.staff.contact }}</span></div>
              </div>
            </div>
          </div>

          <!-- Bottom Action Gate Condition Lock: Render cancellation control exclusively if active 'Booked' -->
          <div class="mt-4 pt-3 border-top border-white border-opacity-10 text-end">
            <button 
              v-if="modalTarget.booking_status === 'Booked'"
              @click="triggerRouteCancellation(modalTarget.booking_id)"
              class="btn btn-danger rounded-pill px-4 py-2 fs-8 fw-semibold w-100 w-md-auto shadow"
            >
              Cancel Expedition Pass
            </button>
            <div v-else class="text-center text-white-50 small opacity-40 italic py-1">
              🔒 This transaction record has been finalized and locked against mutations.
            </div>
          </div>

        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
// import { ref } from 'vue'
// import { useAlertStore } from '../../stores/alert'
// import { useConfirmStore } from '../../stores/confirm'

// const alertStore = useAlertStore()
// const confirmStore = useConfirmStore()

// const modalTarget = ref(null)

// const activeBookingsList = ref([
//   { 
//     booking_id: 9024, trek_name: 'Solang Valley Alpine Pass', booking_date: '2026-05-20', booking_status: 'Booked', payment_status: 'Paid',
//     duration_days: 4, total_people: 3, trek_image: 'https://images.unsplash.com/photo-1501555088652-021faa106b9b?auto=format&fit=crop&w=300&q=80',
//     staff: { name: 'Captain Vikram Singh', email: 'vikram.singh@apex.com', contact: '+91 98765 43210' }
//   },
//   { 
//     booking_id: 8142, trek_name: 'Rohtang Pass Crest Loop', booking_date: '2026-05-14', booking_status: 'Cancelled', payment_status: 'Refunded',
//     duration_days: 5, total_people: 1, trek_image: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=300&q=80',
//     staff: { name: 'Guide Rohan Negi', email: 'rohan.negi@apex.com', contact: '+91 88776 55443' }
//   }
// ])

// function openDeepContextModal(record) {
//   modalTarget.value = record
// }

// function triggerRouteCancellation(id) {
//   confirmStore.ask(
//     `Are you completely certain you want to revoke Expedition Pass #${id}? This restores slot boundaries immediately.`, 
//     () => {
//       const target = activeBookingsList.value.find(b => b.booking_id === id)
//       if (target) {
//         target.booking_status = 'Cancelled'
//         target.payment_status = 'Refunded'
//       }
//       modalTarget.value = null // Terminate modal context stack view
//       alertStore.showAlert(`Expedition Pass #${id} cancelled. Financial refund loop initializing.`, 'warning')
//     }
//   )
// }

import { ref, onMounted } from 'vue'
import { useAlertStore } from '../../stores/alert'
import { useConfirmStore } from '../../stores/confirm'
import { useAuthStore } from '../../stores/auth'

const alertStore = useAlertStore()
const confirmStore = useConfirmStore()
const authStore = useAuthStore()

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
const modalTarget = ref(null)
const activeBookingsList = ref([])

async function fetchLiveBookings() {
  try {
    const res = await fetch(`${BACKEND_URL}/api/trekker/bookings`, {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    if (res.ok) {
      const data = await res.json()
      
      // Ensure image routes map to absolute addresses properly
      activeBookingsList.value = data.map(b => {
        if (b.trek_image && !b.trek_image.startsWith('http')) {
          b.trek_image = `${BACKEND_URL}${b.trek_image}`
        }
        return b
      })
    }
  } catch (err) {
    alertStore.showAlert(`Telemetry Sync Drop: ${err.message}`, 'danger')
  }
}

function openDeepContextModal(record) {
  modalTarget.value = record
}

function triggerRouteCancellation(id) {
  confirmStore.ask(
    `Are you completely certain you want to revoke Expedition Pass #${id}? This restores slot boundaries immediately.`, 
    async () => {
      try {
        const res = await fetch(`${BACKEND_URL}/api/trekker/bookings/${id}/cancel`, {
          method: 'PATCH',
          headers: { 'Authorization': `Bearer ${authStore.token}` }
        })
        const data = await res.json()
        if (res.ok) {
          alertStore.showAlert(`Expedition Pass #${id} cancelled. Refund loops initialized.`, 'warning')
          modalTarget.value = null
          await fetchLiveBookings() // Re-sync the view cleanly
        } else {
          alertStore.showAlert(data.message || "Cancellation failed.", 'danger')
        }
      } catch (err) {
        alertStore.showAlert(`Network error: ${err.message}`, 'danger')
      }
    }
  )
}

onMounted(() => {
  fetchLiveBookings()
})
</script>

<style scoped>
.booking-glass-row { background: rgba(255, 255, 255, 0.05) !important; backdrop-filter: blur(20px); }
.booking-icon-shield { background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.1); }

/* Status Labels & Flags colors */
.payment-badge { padding: 4px 10px; font-size: 0.72rem; border-radius: 4px; font-weight: 600; }
.payment-badge.paid { background: rgba(25, 135, 84, 0.15); color: #7bf1a8; border: 1px solid rgba(25, 135, 84, 0.25); }
.payment-badge.refunded { background: rgba(255, 255, 255, 0.1); color: rgba(255,255,255,0.5); }

.status-badge { padding: 4px 10px; font-size: 0.72rem; border-radius: 20px; font-weight: 600; }
.status-badge.booked { background: rgba(25, 135, 84, 0.2); color: #7bf1a8; border: 1px solid rgba(25, 135, 84, 0.3); }
.status-badge.cancelled { background: rgba(220, 53, 69, 0.15); color: #ff8787; border: 1px solid rgba(220, 53, 69, 0.25); }

/* Immersive Audit Modal Box elements */
.bookings-modal-backdrop {
  position: fixed !important; top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(1, 23, 12, 0.454) !important;
  backdrop-filter: blur(6px) !important; -webkit-backdrop-filter: blur(20px) !important;
  z-index: 999 !important;
}
.glass-audit-card { background: rgba(0, 0, 0, 0.2) !important; backdrop-filter: blur(6px); width: 100%; max-width: 580px; }

.modal-thumbnail-wrapper { height: 155px; }
.object-cover { width: 100%; height: 100%; object-fit: cover; }
.staff-contact-glass { background: rgba(255,255,255, 0.03); }

/* Circle Cross Dismiss Mechanics */
.btn-dismiss-circle-cross {
  position: absolute; top: 20px; right: 20px;
  background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.15);
  color: rgba(255,255,255,0.6); width: 30px; height: 30px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center; font-size: 0.9rem; cursor: pointer; transition: all 0.2s;
}
.btn-dismiss-circle-cross:hover { background: rgba(255,255,255,0.2); color: #ffffff; transform: scale(1.05); }

.text-success-tint { color: #7bf1a8; }
.italic { font-style: italic; }
.fs-8 { font-size: 0.88rem; }
.fs-9 { font-size: 0.76rem; }
.gap-1.5 { gap: 6px; }
</style>