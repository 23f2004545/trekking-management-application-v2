<template>
  <div class="master-trek-detail text-white text-start animate-fade-in pb-4">
    
    <div class="d-flex justify-content-between align-items-center opacity-40 fs-9 mb-3 px-2">
      
    </div>

    <div class="row g-4 align-items-start">
      
      <div class="col-lg-12">
        <div class="row g-3 mb-4">
          <div class="col-md-9">
            <div class="active-image-frame rounded-4 overflow-hidden border border-white border-opacity-10 shadow-sm">
              <img :src="resolveImageUrl(trek.images[activeImageIdx])" alt="Active View" class="w-100 h-100 object-cover" />
            </div>
          </div>
          <div class="col-md-3 d-flex flex-row flex-md-column gap-2 justify-content-between">
            <div 
              v-for="(img, idx) in trek.images.slice(0, 4)" 
              :key="idx" 
              @click="activeImageIdx = idx"
              class="thumb-track-pod rounded-3 overflow-hidden cursor-pointer flex-grow-1"
              :class="{ 'active-thumb-layer': activeImageIdx === idx }"
            >
              <img :src="resolveImageUrl(img)" alt="Thumb" class="w-100 h-100 object-cover" />
            </div>
          </div>
        </div>
      </div>
        
      <div class="col-lg-8">


        <div class="glass-container p-4 rounded-4 mb-4 shadow-sm">
          <div class="d-flex gap-2 mb-3">
            <span class="badge glass-badge text-uppercase fs-9 border border-warning border-opacity-25 text-warning-tint"><i class="bi bi-activity"></i> {{ trek.difficulty }}</span>
            <span class="badge glass-badge text-uppercase fs-9 border border-success border-opacity-25 text-success-tint"><i class="bi bi-circle-fill fs-9"></i> {{ trek.status }}</span>
          </div>
          <h5 class="fw-bold small tracking-wider opacity-40 text-uppercase mb-2">Trek Synopsis</h5>
          <p class="fs-8 text-white-50 lh-base text-justify mb-4">{{ trek.description }}</p>

          <h5 class="fw-bold small tracking-wider opacity-40 text-uppercase mb-2">Trek Details Specifications</h5>
          <div class="inner-spec-table p-4 rounded-3 border border-white border-opacity-5 bg-opacity-5 fs-8">
            <div class="row g-3">
              <div class="col-sm-6"><strong><i class="bi bi-clock-history"></i>  Duration :</strong> <span class="text-white-50">{{ trek.duration_days }} Days</span></div>
              <div class="col-sm-6"><strong><i class="bi bi-graph-up"></i>  Max Altitude:</strong> <span class="text-white-50">{{ trek.max_altitude }}m</span></div>
              <div class="col-sm-6"><strong><i class="bi bi-calendar-minus"></i> Start Date:</strong> <span class="text-white-50"> {{ trek.start_date }}</span></div>
              <div class="col-sm-6"><strong><i class="bi bi-calendar-check"></i> End Date:</strong> <span class="text-white-50"> {{ trek.end_date }}</span></div>
              <div class="col-sm-6"><strong><i class="bi bi-people"></i> Slots Left:</strong> <span class="text-success fw-bold">{{ trek.available_slots }} left</span></div>
              <div class="col-sm-6"><strong><i class="bi bi-currency-rupee"></i> Price:</strong> <span class="text-success fw-bold">{{ trek.price_per_person }}</span></div>
            </div>
          </div>
        </div>

        <div class="glass-container p-4 rounded-4 shadow-sm">
          <h6 class="fw-bold small tracking-wider opacity-50 text-uppercase mb-3 border-bottom border-white border-opacity-10 pb-1"><i class="bi bi-person-lines-fill"></i> Historic Route Reviews ({{ trek.trek_reviews?.length || 0 }})</h6>
          <div class="mb-3"><strong>Trek Rating :</strong> <span class="text-warning-tint ">{{ '★'.repeat(trek.trek_rating_avg) || 'No ratings yet' }}</span></div>
          <div class="d-flex flex-row flex-nowrap gap-3 overflow-x-auto pb-3 custom-scrollbar">
              <div v-if="!trek.trek_reviews?.length" class="text-white-50 opacity-50 fs-9 py-2 italic text-center w-100">
                No structural terrain evaluations logged for this sector yet.
              </div>
              
              <div v-for="rev in trek.trek_reviews" :key="rev.id" class="comment-bubble p-3 rounded-4 flex-shrink-0 d-flex flex-column">
                <div class="d-flex align-items-center justify-content-between mb-2">
                  <span class="fs-8 fw-semibold text-white">{{ rev.trekker }}</span>
                  <span class="text-warning-tint small">{{ '★'.repeat(rev.stars) || 0 }}</span>
                </div>
                <p class="m-0 fs-9 text-white-50 lh-base review-text">"{{ rev.comment }}"</p>
              </div>
          </div>
        </div>
      </div>

      <div class="col-lg-4">
        <div class="glass-container p-4 rounded-4 shadow-sm h-100 d-flex flex-column justify-content-between">
          <div class="meta-profile-zone">
            <div class="mb-3">
              <h3 class="fw-bold tracking-tight m-0 text-white fs-4">{{ trek.trek_name }}</h3>
              <p class="fs-8 text-warning fw-medium m-0 mt-1"> <i class="bi bi-geo-alt"></i> {{ trek.location }}</p>
              
              <span class="fs-8 text-light">Trek Registered : {{ trek.created_at }}</span><br />
              <span class="fs-8 text-info">Last Update : {{ trek.updated_at }}</span>

            </div>
            <hr class="border-white border-opacity-10 my-3" />

            <h6 class="fw-bold small tracking-wider opacity-50 text-uppercase mb-3">Assigned Staff Profile</h6>
            <div class="d-flex align-items-center gap-3 mb-3">
              <img :src="BACKEND_URL + (trek.staff.profile_pic || '/static/Profile_pics/trek_staff.png')" alt="Staff Avatar" class="staff-profile-thumb border border-white border-opacity-20 shadow-sm" />
              <div>
                <h6 class="m-0 fw-bold text-white fs-8">{{ trek.staff.name }}</h6>
                <p class="m-0 fs-9 text-white-50 opacity-75 mt-0.5">{{ trek.staff.experience || 'N/A' }} Years Experience</p>
                <span class="badge active-pulse-tag fs-9 mt-1">● {{ trek.staff.status }}</span>
              </div>
            </div>

            <div class="d-flex flex-column gap-2 fs-9 text-white-50 bg-opacity-5 p-3 rounded-3 border border-white border-opacity-5 mb-3">
              <div><strong>Specialization:</strong> <span class="text-white">{{ trek.staff.specialization }}</span></div>
              <div><strong>Certification:</strong> <span class="text-white">{{ trek.staff.certification }}</span></div>
              <div><strong>Guide Rating:</strong> <span class="text-warning-tint">{{ '★'.repeat(trek.staff.staff_rating_avg) || 'No ratings yet' }}</span></div>
            </div>

            <div class="staff-comments-container mt-3">
              <span class="d-block fs-9 text-white-50 opacity-40 fw-bold text-uppercase mb-2">Guide Performance Logs</span>
              <div v-if="!trek.staff.staff_reviews?.length" class="text-white-50 opacity-40 extra-small py-1 italic">No guide feedback lines submitted.</div>
              <div v-for="s_rev in trek.staff.staff_reviews" :key="s_rev.id" class="staff-comment-pod p-3 rounded-3 mb-2">
                <div class="d-flex align-items-center justify-content-between mb-1">
                  <span class="extra-small text-white-50">{{ s_rev.trekker }}</span>
                  <span class="text-warning-tint extra-small">{{ '★'.repeat(s_rev.stars) }}</span>
                </div>
                <p class="m-0 fs-9 text-white-50 opacity-80 lh-sm">"{{ s_rev.comment }}"</p>
              </div>
            </div>
          </div>

          <div class="pt-3 border-top border-white border-opacity-10 mt-4 text-center">
            
            <button v-if="(authStore.role === 'trekker') && showCheckoutButton" @click="$emit('request-checkout')" class="btn btn-success w-100 rounded-pill py-2.5 fw-bold text-dark fs-8 shadow-sm">
              Book Your Trek Now
            </button>

            <div v-else-if="authStore.role === 'admin'" class="d-flex flex-column gap-2">
              <span class="d-block fs-9 text-warning mb-1 opacity-75"><i class="bi bi-exclamation-triangle-fill text-warning"></i> ADMINISTRATIVE CONTROL OVERRIDE</span>
              <div class="d-flex gap-2">
                <button @click="$emit('admin-modify')" class="btn btn-sm btn-light rounded-pill flex-grow-1 py-2 fw-semibold text-dark fs-9">Modify Route</button>
                <button @click="$emit('admin-delete')" class="btn btn-sm btn-danger rounded-pill flex-grow-1 py-2 fw-semibold text-white fs-9">Purge Track</button>
              </div>
            </div>

            <div v-else-if="authStore.role === 'trek_staff'" class="text-start">
              <span class="d-block fs-9 text-warning mb-2 opacity-75"> <i class="bi bi-exclamation-triangle-fill text-warning"></i> TRAIL MODIFICATIONS </span>
              <button @click="$emit('staff-toggle-status')" class="btn btn-sm btn-outline-success rounded-pill w-100 py-2 fs-9 fw-semibold border-opacity-35 text-white">
                Toggle Lifecycle Status (Open/Closed)
              </button>
            </div>

          </div>

        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const props = defineProps({ trek: { type: Object, required: true }, showCheckoutButton: { type: Boolean, default: true } })
defineEmits(['request-checkout', 'admin-modify', 'admin-delete', 'staff-toggle-status'])

const activeImageIdx = ref(0)
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

function resolveImageUrl(url) {
  if (!url) return ''
  return url.startsWith('http') ? url : `${BACKEND_URL}${url}`
}
</script>

<style scoped>
.glass-container { background: rgba(255, 255, 255, 0.05) !important; backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.12) !important; }
.active-image-frame { height: 320px; }
.thumb-track-pod { height: 74px; opacity: 0.5; transition: opacity 0.2s; background: rgba(0,0,0,0.2); }
.thumb-track-pod:hover, .active-thumb-layer { opacity: 1; border: 2px solid #198754; }
.object-cover { width: 100%; height: 100%; object-fit: cover; }
/* .comment-bubble { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.03); } */
.comment-bubble { 
  background: rgba(255, 255, 255, 0.02); 
  border: 1px solid rgba(255, 255, 255, 0.03); 
  /* Force the cards to maintain a specific width in the horizontal layout */
  min-width: 260px;
  max-width: 260px;
  /* Optional: min-height keeps them uniform even if comments are short */
  height: 160px; 
}

.review-text {
  overflow-y: auto;
  flex-grow: 1;
  padding-right: 4px; /* Gives the scrollbar a little breathing room */
}

/* Optional: Style the mini scrollbar inside the card so it matches your theme */
.review-text::-webkit-scrollbar {
  width: 4px;
}
.review-text::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

/* Custom horizontal scrollbar styling to match the dark/glass UI */
.custom-scrollbar::-webkit-scrollbar {
  height: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.02);
  border-radius: 8px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 8px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.25);
}
.staff-comment-pod { background: rgba(255, 255, 255, 0.01); border-left: 2px solid #198754; }
.staff-profile-thumb { width: 68px; height: 68px; border-radius: 12px; object-fit: cover; }
.active-pulse-tag { background: rgba(25, 135, 84, 0.15); color: #7bf1a8; border: 1px solid rgba(25, 135, 84, 0.3); }
.text-warning-tint { color: #ffe066; } .text-success-tint { color: #7bf1a8; }
.glass-badge { background: rgba(255, 255, 255, 0.06); padding: 5px 12px; border-radius: 20px; }
.text-justify { text-align: justify; } .italic { font-style: italic; }
.fs-8 { font-size: 0.88rem; } .fs-9 { font-size: 0.76rem; } .extra-small { font-size: 0.68rem; } 
</style>