<template>
  <div class="booking-history-sub-component text-white text-start">
    
    <div class="glass-history-block p-4 rounded-4 border border-white border-opacity-10 mb-4 shadow-sm">
      <h5 class="fw-bold small tracking-wider opacity-50 text-uppercase mb-3 border-bottom border-white border-opacity-10 pb-1">📋 Secure Booking Specifications</h5>
      
      <div class="spec-column-grid p-4 rounded-3 border border-white border-opacity-5  bg-opacity-5 fs-8">
        <div class="row g-3">
          <div class="col-md-6 col-lg-3"><strong>Booking Pass ID:</strong> <span class="text-white-50">#APX-B{{ booking.booking_id }}</span></div>
          <div class="col-md-6 col-lg-3"><strong>Reservation Date:</strong> <span class="text-white-50">{{ booking.booking_date }}</span></div>
          <div class="col-md-6 col-lg-3"><strong>Total Group Members:</strong> <span class="text-white-50">{{ booking.total_trekkers }} Travelers</span></div>
          <div class="col-md-6 col-lg-3"><strong>Aggregate Cost Paid:</strong> <span class="text-success fw-bold">₹{{ booking.total_amount_paid }}</span></div>
          <div class="col-md-6 col-lg-4"><strong>Payment Type Protocol:</strong> <span class="text-white-50">{{ booking.payment_type }}</span></div>
          <div class="col-md-6 col-lg-4"><strong>Financial Status:</strong> <span class="badge payment-paid-badge fs-9">● {{ booking.payment_status }}</span></div>
          <div class="col-md-6 col-lg-4"><strong>Ecosystem Registry Time:</strong> <span class="text-white-50">{{ booking.booking_created_at }}</span></div>
        </div>
      </div>
    </div>

    <!-- EXCALIDRAW ELEMENT 3: DUAL FEEDBACK MATRIX FORM -->
    <div class="glass-history-block p-4 rounded-4 border border-white border-opacity-10 shadow-sm">
      <h5 class="fw-bold small tracking-wider opacity-50 text-uppercase mb-3 border-bottom border-white border-opacity-10 pb-1">✍️ Give Feedback Matrix Evaluations</h5>
      
      <!-- CONDITION A: Review Already Submitted (Render Read-Only Frame) -->
      <div v-if="booking.review_submitted" class="read-only-review-display bg-opacity-5 p-4 rounded-3 border border-white border-opacity-5">
        <span class="badge completed-badge mb-3 text-uppercase fs-9">✔ Evaluation Active Inside Database Columns</span>
        
        <div class="row g-4">
          <div class="col-md-6 border-end border-white border-opacity-10">
            <div class="d-flex align-items-center justify-content-between mb-2">
              <h6 class="fw-bold tracking-tight text-white m-0">Trek Route Terrain Rating</h6>
              <span class="text-warning small">{{ '★'.repeat(booking.existing_trek_review.stars) }}</span>
            </div>
            <p class="m-0 fs-9 text-white-50 italic">"{{ booking.existing_trek_review.comment }}"</p>
          </div>
          
          <div class="col-md-6">
            <div class="d-flex align-items-center justify-content-between mb-2">
              <h6 class="fw-bold tracking-tight text-white m-0">Staff Guide Professionalism</h6>
              <span class="text-warning-tint small">{{ '★'.repeat(booking.existing_staff_review.stars) }}</span>
            </div>
            <p class="m-0 fs-9 text-white-50 italic">"{{ booking.existing_staff_review.comment }}"</p>
          </div>
        </div>
      </div>

      <!-- CONDITION B: Empty State (Render Side-By-Side Interactive Inputs) -->
      <form v-else @submit.prevent="submitLocalFeedback" class="feedback-dual-grid-form">
        <div class="row g-4">
          
          <!-- Left Input Box: Trek Review -->
          <div class="col-md-6">
            <div class="sub-form-glass-card p-4 rounded-3 border border-white border-opacity-5 h-100">
              <h6 class="fw-bold tracking-tight text-white mb-3">Trek Route Review</h6>
              <div class="profile-input-group">
                <label class="input-label-tag">Terrain Evaluation Rating: <span class="text-warning fw-bold">{{ localForm.trek_rating }} Stars</span></label>
                <input v-model.number="localForm.trek_rating" type="range" min="1" max="5" class="form-range custom-slider mt-1">
              </div>
              <div class="profile-input-group mt-3">
                <label class="input-label-tag">Route Message Statement</label>
                <div class="interactive-input-wrapper py-2 mt-1">
                  <textarea v-model="localForm.trek_comment" rows="3" required class="clean-profile-field w-100 text-area-fix" placeholder="Describe terrain stability, trail safety markers..."></textarea>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Input Box: Staff Review -->
          <div class="col-md-6">
            <div class="sub-form-glass-card p-4 rounded-3 border border-white border-opacity-5 h-100">
              <h6 class="fw-bold tracking-tight text-white mb-3">Staff Guide Review</h6>
              <div class="profile-input-group">
                <label class="input-label-tag">Guide Competency Rating: <span class="text-warning-tint fw-bold">{{ localForm.staff_rating }} Stars</span></label>
                <input v-model.number="localForm.staff_rating" type="range" min="1" max="5" class="form-range custom-slider mt-1">
              </div>
              <div class="profile-input-group mt-3">
                <label class="input-label-tag">Guide Performance Message Statement</label>
                <div class="interactive-input-wrapper py-2 mt-1">
                  <textarea v-model="localForm.staff_comment" rows="3" required class="clean-profile-field w-100 text-area-fix " placeholder="Describe guide leadership under weather shifts, group safety..."></textarea>
                </div>
              </div>
            </div>
          </div>

        </div>

        <div class="mt-4 d-flex justify-content-end">
          <button type="submit" class="btn btn-success rounded-pill px-5 py-2.5 fw-bold text-dark fs-8 border-0 shadow-sm text-uppercase">
            Submit Evaluation
          </button>
        </div>
      </form>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  booking: { type: Object, required: true }
})

const emit = defineEmits(['commit-review'])

const localForm = ref({
  trek_rating: 5,
  trek_comment: '',
  staff_rating: 5,
  staff_comment: ''
})

function submitLocalFeedback() {
  emit('commit-review', { ...localForm.value })
}
</script>

<style scoped>
.glass-history-block {
  background: rgba(255, 255, 255, 0.05) !important;
  backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
}
.custom-slider::-webkit-slider-runnable-track { background: rgba(255, 255, 255, 0.1); border-radius: 5px; height: 4px; }
.custom-slider::-webkit-slider-thumb { background: #198754; margin-top: -6px; }

.sub-form-glass-card { background: rgba(255, 255, 255, 0.02); }
.completed-badge { background: rgba(0, 123, 255, 0.15); color: #7cd1ff; border: 1px solid rgba(0, 123, 255, 0.25); }
.payment-paid-badge { background: rgba(25, 135, 84, 0.15); color: #7bf1a8; border: 1px solid rgba(25, 135, 84, 0.25); }
.input-label-tag { font-size: 0.8rem; color: rgba(255, 255, 255, 0.5); }
.interactive-input-wrapper { background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 10px; padding: 10px 14px; display: flex; }
.clean-profile-field { border: none; background: transparent; color: #ffffff; outline: none; font-size: 0.92rem; }
.text-area-fix { resize: none; line-height: 1.5; }
.text-warning-tint { color: #ffe066; }
.italic { font-style: italic; }
.p-3.5 { padding: 14px; }
.fs-8 { font-size: 0.88rem; }
.fs-9 { font-size: 0.76rem; }
</style>