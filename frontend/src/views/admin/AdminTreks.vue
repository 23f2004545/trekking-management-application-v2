<template>
  <div class="admin-treks-viewport text-white text-start pb-5 animate-fade-in px-3">
    
    <!-- HEADER BAR: High-end title and quick launch trigger -->
    <div class="d-flex align-items-center justify-content-between mb-4 flex-wrap gap-3">
      <div>
        <h2 class="fw-bold tracking-tight m-0">Expedition Route Inventories</h2>
        <p class="m-0 text-white-50 fs-8 mt-1">Audit active routes, deploy fresh locations map files, or configure tracking parameters.</p>
      </div>
      <button @click="openCreateModal" class="btn btn-success rounded-pill px-4 py-2 fs-8 fw-bold text-dark shadow-sm">
        <i class="bi bi-plus-lg me-2 fs-8"></i> Add Trek Route
      </button>
    </div>

    <!-- ===================================================================
         1. COMPACT SEARCH & COMPREHENSIVE FILTER SYSTEM
         =================================================================== -->
    <div class="glass-container p-3 rounded-4 mb-4 shadow-sm">
      <div class="row g-3 align-items-center">
        <!-- Text Lookup Search -->
        <div class="col-md-3">
          <div class="search-box px-3 py-1.5 rounded-3 d-flex align-items-center">
            <span class="me-2 text-white-50 opacity-50"><i class="bi bi-search"></i></span>
            <input v-model="filters.query" type="text" placeholder="Search by name or grid..." class="bg-transparent border-0 text-white w-100 fs-8 clean-field">
          </div>
        </div>
        <!-- Difficulty Dropdown Filter -->
        <div class="col-md-3">
          <select v-model="filters.difficulty" class="select-glass w-100 px-3 py-1 rounded-3 text-white fs-8">
            <option value="">All Intensities</option>
            <option value="Easy">Easy Trails</option>
            <option value="Moderate">Moderate Tracks</option>
            <option value="Hard">High-Alpine Hard</option>
          </select>
        </div>
        <!-- Price Range Filter Slider -->
        <div class="col-md-3">
          <label class="d-block fs-9 text-white-50 mb-1">Max Budget: <span class="text-success fw-bold">₹{{ filters.price }}</span></label>
          <input v-model.number="filters.price" type="range" min="3000" max="25000" step="500" class="form-range custom-slider">
        </div>
        <!-- Altitude Cap Filter -->
        <div class="col-md-3">
          <label class="d-block fs-9 text-white-50 mb-1">Max Altitude: <span class="text-success fw-bold">{{ filters.altitude }}m</span></label>
          <input v-model.number="filters.altitude" type="range" min="2500" max="6000" step="200" class="form-range custom-slider">
        </div>
      </div>
    </div>

    <!-- ===================================================================
         2. EXISTING EXPEDITIONS GRID CANVAS
         =================================================================== -->
    <div v-if="filteredTreks.length === 0" class="empty-state p-5 text-center rounded-4 border border-white border-opacity-10 bg-opacity-5">
      <span class="fs-1"><i class="bi bi-map"></i></span>
      <h5 class="fw-bold mt-2">No Expedition Inventories Map Matches</h5>
      <p class="text-white-50 small m-0">Reset parameters filters or configure a brand new track route.</p>
    </div>

    <div v-else class="row g-4">
      <div v-for="trek in filteredTreks" :key="trek.trek_id" class="col-xl-4 col-md-6">
        <div class="trek-glass-card h-100 rounded-4 overflow-hidden border border-white border-opacity-10 shadow d-flex flex-column justify-content-between">
          
          <!-- Image Top Cap Area -->
          <div class="card-img-frame position-relative">
            <img :src="BACKEND_URL + trek.image_url" alt="Trek Layout Graphic" class="w-100 h-100 object-cover" />
            <span class="badge position-absolute status-pill" :class="trek.status.toLowerCase()" style="top: 1rem; right: 1rem;">
             ● {{  trek.status }}
            </span>
          </div>

          <!-- Body Technical Parameters Details -->
          <div class="p-3 flex-grow-1 d-flex flex-column justify-content-between">
            <div>
              <div class="d-flex justify-content-between text-white-50 fs-9 mb-1.5 fw-medium">
                <span class="text-info">{{ trek.difficulty }}</span>
                <span><i class="bi bi-caret-up-fill text-success"></i> {{ trek.max_altitude }}m</span>
              </div>
              <h5 class="fw-bold tracking-tight text-white mb-1 text-truncate">{{ trek.trek_name }}</h5>
              <p class="fs-9 text-white-50 m-0 mt-0.5 mb-2"><i class="bi bi-pin-map-fill"></i> Location: {{ trek.location }}</p>
              <p class="fs-9 text-white-50 m-0 opacity-75"><i class="bi bi-person-fill "></i> Guide: <span class="text-warning fw-bold">{{ trek.assigned_staff.name }}</span></p>
            </div>

            <!-- Double Bottom Action Execution Nodes Row -->
            <div class="pt-3 border-top border-white border-opacity-10 mt-3 d-flex align-items-center justify-content-between">
              <div>
                <span class="d-block extra-small text-white-50 opacity-50 fw-semibold">BASE UNIT COST</span>
                <strong class="fs-7 text-success">₹{{ trek.price_per_person }}</strong>
              </div>
              <div class="d-flex gap-2">
                <button @click="triggerRemoval(trek.trek_id)" class="btn btn-sm btn-outline-danger rounded-pill px-3 fs-9 border-opacity-25">Remove</button>
                <button @click="routeToDeepInsights(trek.trek_id)" class="btn btn-sm btn-light rounded-pill px-3 fs-9 fw-bold text-dark">View Detail</button>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- ===================================================================
         3. ADD EXPEDITION PATH MODAL METRICS FORM PANEL
         =================================================================== -->
    <Transition name="modal-fade">
      <div v-if="createModalActive" class="admin-modal-backdrop d-flex align-items-center justify-content-center p-3">
        <div class="glass-modal-card p-4 p-md-5 rounded-4 border border-white border-opacity-15 shadow-lg overflow-y-auto max-vh-90 text-start">
          
          <h4 class="fw-bold tracking-tight text-white m-0">Deploy New Trekking Map</h4>
          <p class="text-white-50 small m-0 mt-0.5 mb-4">Input structural location parameters, assign guides, and declare pricing coordinates.</p>

          <form @submit.prevent="submitTrekForm" class="d-flex flex-column gap-3">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="modal-label">Trek Name *</label>
                <div class="input-wrapper"><input v-model="form.name" type="text" required class="modal-field" placeholder="e.g. Rohtang Glacier Pass"></div>
              </div>
              <div class="col-md-6">
                <label class="modal-label">Location Grid *</label>
                <div class="input-wrapper"><input v-model="form.location" type="text" required class="modal-field" placeholder="e.g. Manali, HP"></div>
              </div>
              <div class="col-md-4">
                <label class="modal-label">Difficulty Range *</label>
                <div class="input-wrapper">
                  <select v-model="form.difficulty" required class="modal-field bg-transparent select-fix">
                    <option value="Easy">Easy Intensity</option>
                    <option value="Moderate">Moderate Range</option>
                    <option value="Hard">High-Alpine Hard</option>
                  </select>
                </div>
              </div>
              <div class="col-md-4">
                <label class="modal-label">Duration (Days) *</label>
                <div class="input-wrapper"><input v-model.number="form.duration_days" type="number" min="1" required class="modal-field"></div>
              </div>
              <div class="col-md-4">
                <label class="modal-label">Available Slots *</label>
                <div class="input-wrapper"><input v-model.number="form.available_slots" type="number" min="1" required class="modal-field"></div>
              </div>
              <div class="col-md-6">
                <label class="modal-label">Peak Altitude (Meters)</label>
                <div class="input-wrapper"><input v-model.number="form.max_altitude" type="number" class="modal-field" placeholder="3200"></div>
              </div>
              <div class="col-md-6">
                <label class="modal-label">Price Per Explorer (INR)</label>
                <div class="input-wrapper"><input v-model.number="form.price_per_person" type="number" class="modal-field" placeholder="5500"></div>
              </div>
              <div class="col-md-6">
                <label class="modal-label">Start Date Coordinates *</label>
                <div class="input-wrapper"><input v-model="form.start_date" type="date" required class="modal-field"></div>
              </div>
              <div class="col-md-6">
                <label class="modal-label">End Date Coordinates *</label>
                <div class="input-wrapper"><input v-model="form.end_date" type="date" required class="modal-field"></div>
              </div>
              <div class="col-12">
                <label class="modal-label">Assign Trek Staff Guide</label>
                <div class="input-wrapper">
                  <select v-model="form.assigned_staff_id" class="modal-field bg-transparent select-fix">
                    <option :value="null">Leave Unassigned</option>
                    <option v-for="s in staffDropdown" :key="s.id" :value="s.id">👨‍✈️ {{ s.name }} (ID: {{ s.id }})</option>
                  </select>
                </div>
              </div>
              <div class="col-12">
                <label class="modal-label">Expedition Media Gallery (Select up to 4 images, Max 500KB each) *</label>
                <div class="input-wrapper py-1.5">
                  <input type="file" accept="image/*" multiple @change="handleMultipleImagesSelection" class="modal-field text-white-50" required>
                </div>
                <small v-if="selectedGalleryFiles.length" class="text-success-tint mt-1 d-block fs-9 fw-medium">
                  ✔ {{ selectedGalleryFiles.length }} images selected for compilation queue.
                </small>
              </div>
              <div class="col-12">
                <label class="modal-label">Expedition Description</label>
                <div class="input-wrapper py-2">
                  <textarea v-model="form.description" rows="3" class="modal-field text-area-fix" placeholder="Describe terrain boundaries, environmental risk variables..."></textarea>
                </div>
              </div>
            </div>

            <!-- Trigger Button Rows -->
            <div class="mt-4 d-flex align-items-center justify-content-end gap-3 border-top border-white border-opacity-10 pt-3">
              <button type="button" @click="createModalActive = false" class="btn btn-outline-light rounded-pill px-4 py-2 fs-8">Cancel</button>
              <button type="submit" class="btn btn-success rounded-pill px-5 py-2.5 fw-bold text-dark fs-8">Deploy Route</button>
            </div>
          </form>

        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAlertStore } from '../../stores/alert'
import { useAuthStore } from '../../stores/auth'
import { useConfirmStore } from '../../stores/confirm'

const router = useRouter()
const alertStore = useAlertStore()
const authStore = useAuthStore()
const confirmStore = useConfirmStore()

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
const adminTreks = ref([])
const staffDropdown = ref([])
const createModalActive = ref(false)
const selectedGalleryFiles = ref([])

// Filtering state metrics
const filters = ref({ query: '', difficulty: '', price: 25000, altitude: 6000 })

// Model alignment fields mapping
const form = ref({
  name: '', location: '', difficulty: 'Moderate', duration_days: 3,
  available_slots: 15, max_altitude: 3000, price_per_person: 5000,
  start_date: '', end_date: '', description: '', assigned_staff_id: null
})

// DYNAMIC SEARCH & FILTER CALCULATOR ENGINE
const filteredTreks = computed(() => {
  return adminTreks.value.filter(t => {
    const matchesQuery = t.trek_name.toLowerCase().includes(filters.value.query.toLowerCase()) || 
                         t.location.toLowerCase().includes(filters.value.query.toLowerCase())
    const matchesDiff = !filters.value.difficulty || t.difficulty === filters.value.difficulty
    const matchesPrice = t.price_per_person <= filters.value.price
    const matchesAlt = t.max_altitude <= filters.value.altitude
    return matchesQuery && matchesDiff && matchesPrice && matchesAlt
  })
})

async function syncTrekDataset() {
  try {
    const headers = { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' }
    const res = await fetch(`${BACKEND_URL}/api/admin/treks`, { method: 'GET', headers })
    if (res.ok) {
      adminTreks.value = await res.json()
    }
    
    // Quick async retrieval load to populate staff selectors downstream
    const staffRes = await fetch(`${BACKEND_URL}/api/admin/staff`, { method: 'GET', headers })
    if (staffRes.ok) {
      staffDropdown.value = await staffRes.json()
    }
  } catch (err) {
    alertStore.showAlert(`Telemetry Sync Drop: ${err.message}`, 'danger')
  }
}

function openCreateModal() {
  form.value = {
    name: '', location: '', difficulty: 'Moderate', duration_days: 3,
    available_slots: 15, max_altitude: 3000, price_per_person: 5000,
    start_date: '', end_date: '', description: '', assigned_staff_id: null
  }
  createModalActive.value = true
}

function handleMultipleImagesSelection(event) {
  const files = Array.from(event.target.files)
  selectedGalleryFiles.value = []
  
  if (files.length > 4) {
    alertStore.showAlert('Validation Warning: Gallery space capped at a maximum parameter of 4 images.', 'danger')
    event.target.value = ''
    return
  }

  const MAX_SIZE = 500 * 1024 // 500 KB in raw bytes threshold safety metrics
  for (const file of files) {
    if (file.size > MAX_SIZE) {
      alertStore.showAlert(`Validation Error: '${file.name}' breaks file constraints limit. Capped at 500KB.`, 'danger')
      event.target.value = ''
      selectedGalleryFiles.value = []
      return
    }
    selectedGalleryFiles.value.push(file)
  }
}

async function submitTrekForm() {
  // Multipart packaging data configuration layers
  const formData = new FormData()
  Object.keys(form.value).forEach(key => {
    formData.append(key, form.value[key])
  })
  selectedGalleryFiles.value.forEach(file => {
    formData.append('trek_gallery', file)
  })

  try {
    const res = await fetch(`${BACKEND_URL}/api/admin/treks`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${authStore.token}` },
      body: formData
    })
    const data = await res.json()
    if (res.ok) {
      alertStore.showAlert(data.message || 'Expedition deployed successfully!', 'success')
      createModalActive.value = false
      await syncTrekDataset()
    } else {
      alertStore.showAlert(data.message || 'Route submission rejected.', 'danger')
    }
  } catch (err) {
    alertStore.showAlert(`Transaction drop: ${err.message}`, 'danger')
  }
}

function triggerRemoval(id) {
  confirmStore.ask(
    `Are you entirely sure you want to drop Expedition ID #${id} completely out of system indexes? This action is irreversible.`,
    async () => {
      try {
        const res = await fetch(`${BACKEND_URL}/api/admin/treks/${id}`, {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' }
        })
        if (res.ok) {
          alertStore.showAlert('Expedition record purged from database successfully.', 'success')
          await syncTrekDataset()
        } else {
          const data = await res.json()
          alertStore.showAlert(data.message || 'Purge request rejected.', 'danger')
        }
      } catch (err) {
        alertStore.showAlert(`Network drop: ${err.message}`, 'danger')
      }
    }
  )
}

function routeToDeepInsights(id) {
  // Automatically routes down to your reusable nested component structure
  router.push(`/portal/trek/view/${id}`)
}

onMounted(() => {
  syncTrekDataset()
})
</script>

<style scoped>
.glass-container { background: rgba(255, 255, 255, 0.05) !important; backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.12) !important; padding: 0.5rem; }
.trek-glass-card { background: rgba(255, 255, 255, 0.04) !important; backdrop-filter: blur(20px); transition: transform 0.2s; }
.trek-glass-card:hover { transform: translateY(-3px); }

.card-img-frame { height: 150px; overflow: hidden; }
.object-cover { width: 100%; height: 100%; object-fit: cover; }

.search-box { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); }
.clean-field:focus { outline: none; }
.select-glass { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); outline: none; }
.select-glass option { background: #141c16; color: white; }

/* Status pill mappings */
.status-pill { padding: 3px 9px; font-size: 0.7rem; border-radius: 20px; font-weight: 600; text-transform: uppercase; }
.status-pill.open { background: rgba(25, 135, 84, 0.8); }
.status-pill.pending { background: rgba(255, 193, 7, 0.8); color: black; }
.status-pill.closed { background: rgba(220, 53, 69, 0.8); }
.status-pill.completed { background: rgba(13, 110, 253, 0.8); }

/* Modal overlay layouts */
.admin-modal-backdrop { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(10,15,12,0.6); backdrop-filter: blur(20px); z-index: 999; }
.glass-modal-card { background: rgba(20, 28, 24, 0.9) !important; backdrop-filter: blur(35px); width: 100%; max-width: 650px; }
.max-vh-90 { max-height: 90vh; }

.modal-label { font-size: 0.78rem; color: rgba(255,255,255,0.5); font-weight: 500; margin-bottom: 3px; display: block; }
.input-wrapper { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12); border-radius: 8px; padding: 6px 12px; }
.modal-field { border: none; background: transparent; color: #fff; outline: none; width: 100%; font-size: 0.9rem; }
.text-area-fix { resize: none; line-height: 1.4; }
.select-fix option { background: #1c241e; color: white; }

.custom-slider::-webkit-slider-runnable-track { background: rgba(255, 255, 255, 0.1); border-radius: 5px; height: 4px; }
.custom-slider::-webkit-slider-thumb { background: #198754; margin-top: -6px; }

.extra-small { font-size: 0.68rem; }
.fs-8 { font-size: 0.88rem; }
.fs-9 { font-size: 0.76rem; }
</style>