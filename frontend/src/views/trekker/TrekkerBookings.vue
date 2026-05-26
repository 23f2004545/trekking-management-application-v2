<template>
  <div class="bookings-audit-viewport text-white text-start animate-fade-in">
    
    <div class="mb-4">
      <h2 class="fw-bold tracking-tight m-0">Active Basecamp Bookings</h2>
      <p class="m-0 text-white-50 fs-8 mt-1">Audit active pass verifications, inspect transaction telemetry statuses, or submit route cancellations.</p>
    </div>

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

          <div class="d-flex align-items-center gap-2">
            
            <button 
              v-if="book.booking_status === 'Booked'"
              @click="triggerRouteCancellation(book.booking_id)" 
              class="btn btn-sm btn-outline-danger rounded-pill px-3 py-1.5 fs-9 fw-semibold border-opacity-25"
            >
              Cancel Expedition Pass
            </button>
            
            <button 
              :disabled="book.booking_status !== 'Booked'"
              @click="viewPassCredentials(book.booking_id)"
              class="btn btn-sm btn-success rounded-pill px-3 py-1.5 fs-9 fw-bold text-dark shadow-sm"
            >
              {{ book.booking_status === 'Booked' ? 'Access Pass Coordinates' : 'Pass Locked' }}
            </button>

          </div>

        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAlertStore } from '../../stores/alert'
import { useConfirmStore } from '../../stores/confirm'

const alertStore = useAlertStore()
const confirmStore = useConfirmStore()

// Mocked response arrays containing explicit metadata states
const activeBookingsList = ref([
  { booking_id: 9024, trek_name: 'Solang Valley Alpine Pass', booking_date: '2026-05-20', booking_status: 'Booked', payment_status: 'Paid' },
  { booking_id: 8142, trek_name: 'Rohtang Pass Crest Loop', booking_date: '2026-05-14', booking_status: 'Cancelled', payment_status: 'Refunded' },
  { booking_id: 7035, trek_name: 'Kheerganga Ridge Trek', booking_date: '2026-04-12', booking_status: 'Completed', payment_status: 'Paid' }
])

function viewPassCredentials(id) {
  alertStore.showAlert(`Displaying secure digital pass credentials coordinates mapping loop for Pass #${id}.`, 'info')
}

function triggerRouteCancellation(id) {
  // Uses our globally reusable custom confirm dialog component refactored earlier
  confirmStore.ask(
    `Are you completely certain you want to revoke Expedition Pass #${id}? This action restores slot boundaries immediately.`, 
    () => {
      // Callback action closure executed explicitly upon positive confirmation submit action
      const target = activeBookingsList.value.find(b => b.booking_id === id)
      if (target) {
        target.booking_status = 'Cancelled'
        target.payment_status = 'Refunded'
      }
      alertStore.showAlert(`Expedition Pass #${id} cancelled. Financial refund loop initializing.`, 'warning')
    }
  )
}
</script>

<style scoped>
.booking-glass-row {
  background: rgba(255, 255, 255, 0.05) !important;
  backdrop-filter: blur(20px);
}

.booking-icon-shield {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Payment state badge configurations */
.payment-badge { padding: 4px 10px; font-size: 0.72rem; border-radius: 4px; font-weight: 600; }
.payment-badge.paid { background: rgba(25, 135, 84, 0.15); color: #7bf1a8; border: 1px solid rgba(25, 135, 84, 0.25); }
.payment-badge.refunded { background: rgba(255, 255, 255, 0.1); color: rgba(255,255,255,0.6); }

/* Booking lifecycle state configurations */
.status-badge { padding: 4px 10px; font-size: 0.72rem; border-radius: 20px; font-weight: 600; }
.status-badge.booked { background: rgba(25, 135, 84, 0.2); color: #7bf1a8; border: 1px solid rgba(25, 135, 84, 0.3); }
.status-badge.cancelled { background: rgba(220, 53, 69, 0.15); color: #ff8787; border: 1px solid rgba(220, 53, 69, 0.25); }
.status-badge.completed { background: rgba(0, 123, 255, 0.15); color: #7cd1ff; border: 1px solid rgba(0, 123, 255, 0.25); }

button:disabled {
  opacity: 0.35 !important;
  cursor: not-allowed !important;
}

.fs-8 { font-size: 0.88rem; }
.fs-9 { font-size: 0.76rem; }
.tracking-wider { letter-spacing: 0.6px; }
</style>