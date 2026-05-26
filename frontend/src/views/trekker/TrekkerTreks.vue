<template>
  <div class="treks-exploration-viewport text-white text-start">
    
    <div class="mb-4">
      <h2 class="fw-bold tracking-tight m-0">Discover Expedition Trails</h2>
      <p class="m-0 text-white-50 fs-8 mt-1">Browse open mountain coordinates, check altitude parameters, and examine verified safety guide telemetry.</p>
    </div>

    <div class="row g-4">
      <div v-for="trek in tracksList" :key="trek.trek_id" class="col-xl-4 col-md-6">
        <div class="trek-glass-card h-100 rounded-4 overflow-hidden border border-white border-opacity-10 shadow d-flex flex-column justify-content-between">
          
          <div class="card-image-thumbnail-wrapper position-relative">
            <img :src="trek.images[0] || 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b'" alt="Trek Thumbnail" class="thumbnail-img w-100" />
            <span class="badge position-absolute top-3 right-3 status-pill" :class="trek.status.toLowerCase()">
              ● {{ trek.status }}
            </span>
          </div>

          <div class="p-3_5 flex-grow-1 d-flex flex-column justify-content-between">
            <div>
              <div class="d-flex align-items-center justify-content-between text-white-50 fs-9 fw-bold mb-1.5">
                <span class="text-uppercase tracking-wider">🧗 {{ trek.difficulty }}</span>
                <span>🏔️ {{ trek.max_altitude }}m</span>
              </div>
              <h4 class="fw-bold tracking-tight m-0 mb-1 text-white">{{ trek.trek_name }}</h4>
              <p class="fs-8 text-white-50 m-0 mb-3">📍 {{ trek.location }}</p>
            </div>

            <div class="pt-3 border-top border-white border-opacity-10 d-flex align-items-center justify-content-between">
              <div>
                <span class="d-block fs-9 text-white-50 opacity-50 fw-semibold">VALUED AT</span>
                <strong class="fs-6 text-success">₹{{ trek.price_per_person }}</strong>
              </div>
              <button @click="openDetailedOverlay(trek)" class="btn btn-sm btn-light rounded-pill px-3.5 py-1.5 fs-8 fw-bold text-dark">
                View Details
              </button>
            </div>
          </div>

        </div>
      </div>
    </div>

    <Transition name="modal-fade">
      <div v-if="selectedTrek" class="detailed-overlay-backdrop d-flex align-items-center justify-content-center p-2 p-md-3">
        <div class="glass-detail-card rounded-4 border border-white border-opacity-15 shadow-lg w-100 overflow-y-auto max-vh-90">
          
          <div class="row g-0">
            <div class="col-lg-6 p-4">
              <div class="active-gallery-frame rounded-3 overflow-hidden border border-white border-opacity-10 mb-2">
                <img :src="selectedTrek.images[activeImageIndex]" alt="Master view" class="w-100 master-gallery-view" />
              </div>
              <div class="row g-2">
                <div v-for="(img, idx) in selectedTrek.images" :key="idx" class="col-3">
                  <div @click="activeImageIndex = idx" class="gallery-thumb-container rounded-2 overflow-hidden cursor-pointer" :class="{ 'active-thumb': activeImageIndex === idx }">
                    <img :src="img" alt="Thumb" class="w-100 thumb-img-element" />
                  </div>
                </div>
              </div>

              <div class="mt-4 text-start">
                <h6 class="fw-bold small tracking-wider opacity-50 text-uppercase border-bottom border-white border-opacity-10 pb-1 mb-2">Trail Synopsis</h6>
                <p class="fs-8 text-white-50 lh-base m-0 text-justify">{{ selectedTrek.description }}</p>
              </div>
            </div>

            <div class="col-lg-6 p-4 d-flex flex-column justify-content-between border-start border-white border-opacity-10">
              <div class="text-start">
                <div class="d-flex align-items-center justify-content-between mb-2">
                  <h3 class="fw-bold tracking-tight m-0">{{ selectedTrek.trek_name }}</h3>
                  <button @click="closeDetailedOverlay" class="btn-close-modal-round">✕</button>
                </div>
                <p class="text-success small fw-semibold m-0 mb-3">📍 {{ selectedTrek.location }}</p>

                <div class="spec-matrix-grid mb-4 fs-8  bg-opacity-5 p-3 rounded-3 border border-white border-opacity-10">
                  <div class="row g-2">
                    <div class="col-6 mb-2"><strong>Duration:</strong> <span class="text-white-50">{{ selectedTrek.duration_days }} Days</span></div>
                    <div class="col-6 mb-2"><strong>Peak Altitude:</strong> <span class="text-white-50">{{ selectedTrek.max_altitude }} Meters</span></div>
                    <div class="col-6 mb-2"><strong>Available Slots:</strong> <span class="text-white-50 text-success">{{ selectedTrek.available_slots }} left</span></div>
                    <div class="col-6 mb-2"><strong>Est. Completion:</strong> <span class="text-white-50">{{ selectedTrek.end_date }}</span></div>
                  </div>
                </div>

                <h6 class="fw-bold small tracking-wider opacity-50 text-uppercase border-bottom border-white border-opacity-10 pb-1 mb-2">Verified Assigned Staff Guide</h6>
                <div class="staff-glass-capsule p-3 rounded-3 border border-white border-opacity-10 d-flex gap-3 mb-4">
                  <img :src="selectedTrek.staff.avatar" alt="Staff Guide" class="staff-card-avatar" />
                  <div class="text-start flex-grow-1">
                    <h6 class="m-0 fw-bold text-white fs-8">{{ selectedTrek.staff.name }}</h6>
                    <p class="m-0 fs-9 text-success fw-medium mt-0.5">Clearance: Senior Guide ({{ selectedTrek.staff.experience }} Exp)</p>
                    
                    <div class="mt-2 pt-2 border-top border-white border-opacity-10">
                      <span class="d-block fs-9 text-white-50 fw-semibold mb-1">EXPLORER FEEDBACK LOOP</span>
                      <p class="m-0 fs-9 text-white-50 italic">"{{ selectedTrek.staff.top_review }}"</p>
                    </div>
                  </div>
                </div>
              </div>

              <div class="pt-3 border-top border-white border-opacity-10 d-flex align-items-center justify-content-between">
                <div>
                  <span class="fs-9 text-white-50 opacity-60">PRICE PER TREKKER</span>
                  <h4 class="m-0 fw-bold text-success">₹{{ selectedTrek.price_per_person }}</h4>
                </div>
                <button @click="executeBookingAction(selectedTrek.trek_id)" class="btn btn-success rounded-pill px-4 py-2 fw-bold text-dark fs-8">
                  Confirm Base Authorization Slot
                </button>
              </div>

            </div>
          </div>

        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAlertStore } from '../../stores/alert'

const alertStore = useAlertStore()

const selectedTrek = ref(null)
const activeImageIndex = ref(0)

// Mocked response records containing paginated 4-image array limits schemas definitions
const tracksList = ref([
  {
    trek_id: 1,
    trek_name: 'Solang Valley Alpine Pass',
    location: 'Manali, Himachal Pradesh',
    difficulty: 'Moderate',
    duration_days: 4,
    available_slots: 12,
    status: 'Open',
    max_altitude: 3840,
    price_per_person: 6499,
    description: 'Traverse magnificent cedar woodlands and crystalline stream junctions before rising into pristine high alpine zones. This route features scenic photography points and reliable emergency coordinates.',
    images: [
      'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=600&q=80',
      'https://images.unsplash.com/photo-1501555088652-021faa106b9b?auto=format&fit=crop&w=600&q=80',
      'https://images.unsplash.com/photo-1454496522488-7a8e488e8606?auto=format&fit=crop&w=600&q=80',
      'https://images.unsplash.com/photo-1486915309851-b0cc1f8a0084?auto=format&fit=crop&w=600&q=80'
    ],
    staff: {
      name: 'Captain Vikram Singh',
      experience: '6+ Years',
      avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=150&q=80',
      top_review: 'Vikram coordinated our entire safety checkpoint array perfectly during the snow shifts. Ultimate professional guide.'
    }
  }
])

function openDetailedOverlay(trek) {
  activeImageIndex.value = 0
  selectedTrek.value = trek
}

function closeDetailedOverlay() {
  selectedTrek.value = null
}

function executeBookingAction(id) {
  alertStore.showAlert(`Slot application sequence for Trek #${id} dispatched to Flask database layers.`, 'success')
  selectedTrek.value = null
}
</script>

<style scoped>
.trek-glass-card {
  background: rgba(255, 255, 255, 0.05) !important;
  backdrop-filter: blur(20px);
}

.card-image-thumbnail-wrapper { height: 160px; overflow: hidden; }
.thumbnail-img { height: 100%; object-fit: cover; }

/* Status pill classes mapping definitions */
.status-pill { padding: 4px 10px; font-size: 0.72rem; border-radius: 20px; font-weight: 600; }
.status-pill.open { background: rgba(25, 135, 84, 0.8); border: 1px solid #198754; }

/* Immersive Detailed Modal Shell Elements */
.detailed-overlay-backdrop {
  position: fixed !important; top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(10, 20, 15, 0.6) !important;
  backdrop-filter: blur(20px) !important; -webkit-backdrop-filter: blur(20px) !important;
  z-index: 99999999 !important;
}

.glass-detail-card {
  background: rgba(25, 35, 30, 0.88) !important;
  backdrop-filter: blur(35px);
  max-width: 900px;
}
.max-vh-90 { max-height: 90vh; }

.active-gallery-frame { height: 260px; }
.master-gallery-view { height: 100%; object-fit: cover; }
.gallery-thumb-container { height: 50px; opacity: 0.4; transition: opacity 0.2s; }
.gallery-thumb-container:hover, .active-thumb { opacity: 1; border: 1.5px solid #198754; }
.thumb-img-element { height: 100%; object-fit: cover; }

/* Staff Capsule styles */
.staff-glass-capsule { background: rgba(255, 255, 255, 0.04); }
.staff-card-avatar { width: 55px; height: 55px; border-radius: 8px; object-fit: cover; border: 1px solid rgba(255,255,255,0.15); }

.btn-close-modal-round { background: rgba(255, 255, 255, 0.1); border: none; color: white; width: 28px; height: 28px; border-radius: 50%; cursor: pointer; }
.btn-close-modal-round:hover { background: rgba(255, 255, 255, 0.2); }

.text-justify { text-align: justify; }
.italic { font-style: italic; }
.p-3_5 { padding: 14px; }
.fs-8 { font-size: 0.88rem; }
.fs-9 { font-size: 0.76rem; }
.tracking-wider { letter-spacing: 0.5px; }
</style>