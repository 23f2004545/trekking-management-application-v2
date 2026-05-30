<template>
  <div class="historical-audit-viewport text-white text-start animate-fade-in pb-5">
    
    <!-- PHASE 1: COMPACT HISTORICAL ROW LIST ARCHITECTURE -->
    <div v-if="!selectedTripForDetails">
      <div class="mb-4">
        <h2 class="fw-bold tracking-tight m-0">Expedition History Logs</h2>
        <p class="m-0 text-white-50 fs-8 mt-1">Review finalized high-alpine routes, evaluate guide staff columns, and audit past data logs.</p>
      </div>

      <div class="row g-3">
        <div v-for="trip in historicTrips" :key="trip.booking_id" class="col-12">
          <div class="history-glass-row p-3 rounded-3 border border-white border-opacity-10 d-flex align-items-center justify-content-between gap-3">
            <div class="d-flex align-items-center gap-3">
              <div class="icon-shield fs-4 p-2 rounded-2">🏔️</div>
              <div>
                <span class="badge completed-badge mb-1 text-uppercase fs-9">● Completed</span>
                <h5 class="fw-bold m-0 text-white">{{ trip.trek_name }}</h5>
                <p class="m-0 fs-9 text-white-50 mt-0.5">Departed trail on: {{ trip.booking_date }}</p>
              </div>
            </div>
            <button @click="selectedTripForDetails = trip" class="btn btn-sm btn-success rounded-pill px-4 py-2 fs-8 fw-bold text-dark shadow-sm">
              View Deep Insights & Reviews
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- PHASE 2: DETAILED SYSTEM CASCADING DEPLOYMENT -->
    <div v-else class="extended-history-details-flow">
      <div class="mb-4">
        <button @click="selectedTripForDetails = null" class="btn btn-outline-light rounded-pill px-3.5 py-1.5 fs-9 border-opacity-25">
          ← Return to History Logs
        </button>
      </div>

      <!-- REUSE CARD A: Master Terrain Specifications Block -->
      <TrekDetail :trek="selectedTripForDetails" :showCheckoutButton="false" />

      <!-- REUSE CARD B: Excalidraw-Optimized Financial Form Block Component -->
      <TrekHistory :booking="selectedTripForDetails" @commit-review="handlePublishedReview" />
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import TrekDetail from '../../components/TrekDetail.vue'
import TrekHistory from '../../components/TrekHistory.vue'
import { useAlertStore } from '../../stores/alert'

const alertStore = useAlertStore()
const selectedTripForDetails = ref(null)

function handlePublishedReview(formData) {
  selectedTripForDetails.value.review_submitted = true
  selectedTripForDetails.value.existing_trek_review = { stars: formData.trek_rating, comment: formData.trek_comment }
  selectedTripForDetails.value.existing_staff_review = { stars: formData.staff_rating, comment: formData.staff_comment }
  alertStore.showAlert('Success: Review variables committed downstream inside dynamic components.', 'success')
}

// Complete mock dataset containing required child mapping models matching your framework configuration
const historicTrips = ref([
  {
    booking_id: 7035,
    trek_name: 'Kheerganga Ridge Trek',
    booking_date: '2026-04-12',
    total_trekkers: 3,
    total_amount_paid: '19,497',
    payment_type: 'UPI Transfer',
    payment_status: 'Paid / Settled',
    booking_created_at: '2026-04-01 14:22:10',
    trek_id: 3,
    location: 'Parvati Valley, Himachal Pradesh',
    difficulty: 'Moderate',
    duration_days: 3,
    available_slots: 0,
    status: 'Completed',
    max_altitude: 2960,
    price_per_person: 6499,
    created_at: '2026-03-15', updated_at: '2026-04-15',
    description: 'Hike along cascading thermal stream fields and ancient oak boundaries before setting base operations at the legendary high hot springs meadows.',
    images: [
      'https://images.unsplash.com/photo-1501555088652-021faa106b9b?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1454496522488-7a8e488e8606?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1486915309851-b0cc1f8a0084?auto=format&fit=crop&w=800&q=80'
    ],
    staff: {
      name: 'Guide Rohan Negi', experience: '4 Years', last_login_at: '2 hours ago',
      specialization: 'High Altitude Medical', certification: 'ABVIMAS Certified', rating: 4,
      profile_pic: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=150&q=80',
      staff_reviews: []
    },
    trek_reviews: [],
    review_submitted: true,
    existing_trek_review: { stars: 5, comment: 'The thermal valleys and cedar junctions tracking parameters were flawless.' },
    existing_staff_review: { stars: 4, comment: 'Rohan kept group pacing speed exceptionally balanced across steep slopes.' }
  }
])
</script>

<style scoped>
.history-glass-row { background: rgba(255, 255, 255, 0.05) !important; backdrop-filter: blur(15px); }
.icon-shield { background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.1); }
.completed-badge { background: rgba(0, 123, 255, 0.15); color: #7cd1ff; border: 1px solid rgba(0, 123, 255, 0.25); }
.fs-8 { font-size: 0.88rem; }
.fs-9 { font-size: 0.76rem; }
</style>