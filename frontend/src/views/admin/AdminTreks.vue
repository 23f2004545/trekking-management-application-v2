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
          <label class="d-block fs-9 text-white-50 mb-1">Max Budget / <i class="bi bi-person"></i> : <span class="text-success fw-bold">₹{{ filters.price }}</span></label>
          <input v-model.number="filters.price" type="range" :min="filterExtremes.min_price" :max="filterExtremes.max_price" step="250" class="form-range custom-slider">
        </div>
        <!-- Altitude Cap Filter -->
        <div class="col-md-3">
          <label class="d-block fs-9 text-white-50 mb-1">Max Altitude: <span class="text-success fw-bold">{{ filters.altitude }}m</span></label>
          <input v-model.number="filters.altitude" type="range" :min="filterExtremes.min_altitude" :max="filterExtremes.max_altitude" step="100" class="form-range custom-slider">
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
        <div 
          class="trek-premium-card position-relative rounded-4 shadow-sm d-flex flex-column text-start"
          @click="routeToDeepInsights(trek.trek_id)"
        >
          
          <div class="card-bg-wrapper position-absolute top-0 start-0 w-100 h-100 z-0">
            <img :src="resolveMediaUrl(trek.image_url)" alt="Trek Graphic" class="card-bg-img w-100 h-100 object-cover" />
          </div>

          <div class="card-gradient-overlay position-absolute top-0 start-0 w-100 h-100 z-1"></div>

          <div class="position-relative z-2 d-flex flex-column h-100 p-4 w-100">

            <span class="badge position-absolute status-pill" :class="trek.status.toLowerCase()" style="top: 1rem; left: 1rem;">
              {{ trek.status }}
            </span>
            <span v-if="trek.trek_name.toLowerCase().includes('demo')" class="badge position-absolute status-pill " style="top: 3rem; left: 1rem; background: rgba(255, 193, 7, 0.8); color: black; ">
              DEMO
            </span>
            <span class="badge position-absolute difficulty-pill" :class="trek.difficulty.toLowerCase()" style="top: 1rem; right: 1rem;">
              <i class="bi bi-activity me-1.5 opacity-50"></i> {{ trek.difficulty }}
            </span>

            <div class="mt-auto w-100 pb-1">
              
              <div class="d-flex flex-column align-items-start gap-2 mb-2">
                <div v-if="trek.trek_rating ">
                  <span class="badge bg-white bg-opacity-10 text-white border border-warning border-opacity-20 rounded-pill px-2.5 py-1 fs-10 backdrop-blur fw-normal">
                  Rating : {{ trek.trek_rating }} <i class="bi bi-star-fill text-warning"></i>
                  </span>
                </div>
                <span class="fs-10 text-white fw-medium">
                  <i class="bi bi-people-fill text-success opacity-75 me-1"></i> 
                  <span :class="trek.available_slots < 5 ? 'text-warning' : ''">{{ trek.available_slots }} Slots Available</span>
                </span>
              </div>

              <div class="d-flex justify-content-between align-items-end mb-1">
                <h3 class="fw-bold text-white m-0 text-truncate pe-3 tracking-tight text-shadow-sm">{{ trek.trek_name.split(' ').slice(0, 2).join(' ') }}</h3>
                <h4 class="fw-bold text-success m-0 tracking-tight text-shadow-sm">₹{{ trek.price_per_person }} / <i class="bi bi-person"></i></h4>
              </div>

              <p class="fs-9 text-info m-0 text-truncate fw-medium mb-2">
                <i class="bi bi-geo-alt-fill text-danger opacity-50 me-1"></i>{{ trek.location }}
              </p>

              <hr class="border-white border-opacity-20 my-3" />

              <div class="d-flex flex-row align-items-center justify-content-between fs-9 text-white-75 w-100">
  
                <!-- Duration: Left aligned -->
                <div class="d-flex align-items-center pe-3">
                  <i class="bi bi-clock-history me-1 opacity-50 "></i>
                  <span>{{ trek.duration_days }} Day(s)</span>
                </div>

                <!-- Dates: Responsive display (Compact on mobile, full on desktop) -->
                <div class="d-flex align-items-center  border-start border-end border-white border-opacity-20 px-2 text-truncate justify-content-center flex-grow-1">
                  <i class="bi bi-calendar3 me-1 d-inline d-sm-none"></i>
                  <!-- Mobile: Shows just start date -->
                  <span class="d-inline d-sm-none">{{ trek.start_date }}</span>
                  <!-- Desktop: Shows full date span -->
                  <span class="d-none d-sm-inline">{{ trek.start_date }} : {{ trek.end_date }}</span>
                </div>

                <!-- Altitude: Right aligned -->
                <div class="d-flex align-items-center ps-3 justify-content-end">
                  <i class="bi bi-graph-up me-1 text-info"></i>
                  <span>{{ trek.max_altitude }}m</span>
                </div>
              
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
      <div v-if="createModalActive" @click.self="createModalActive = false" class="admin-modal-backdrop d-flex align-items-center justify-content-center p-3">
        <div class="glass-modal-card p-4 p-md-5 rounded-4 border border-white border-opacity-15 shadow-lg overflow-y-auto max-vh-70 text-start">
          
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
                <input v-model="form.start_date" type="date" required class="modal-field">
              </div>
              <div class="col-md-6">
                <label class="modal-label">End Date Coordinates *</label>
                <input v-model="form.end_date" type="date" required class="modal-field">
              </div>
              <div class="col-12 position-relative">
                <label class="modal-label">Assign Commander (Select date first)</label>
                
                <div class="input-wrapper position-relative" @click="staffDropdownOpen = true">
                  <input 
                    v-model="staffSearchQuery" 
                    type="text" 
                    class="modal-field w-100 pe-5" 
                    placeholder="Search active guides by name or email..."
                    @focus="staffDropdownOpen = true"
                  >
                  <i class="bi bi-search position-absolute top-50 end-0 translate-middle-y me-3 text-white-50"></i>
                </div>

                <Transition name="fade">
                  <div v-if="staffDropdownOpen" class="position-absolute w-100 mt-1 rounded-3 border border-white border-opacity-10 overflow-hidden shadow-lg z-index-top" style="background: rgba(10, 16, 13, 0.95); backdrop-filter: blur(20px); max-height: 220px; overflow-y: auto;">
                    
                    <div @click="clearStaffSelection" class="p-3 border-bottom border-white border-opacity-10 cursor-pointer hover-bg-glass text-white-50 fs-9">
                      <i class="bi bi-x-circle me-2"></i> Leave Unassigned
                    </div>

                    <div v-if="availableStaff.length === 0" class="p-3 text-center text-white-50 fs-9 italic">
                      No active guides match your search.
                    </div>
                    
                    <div 
                      v-for="s in availableStaff" 
                      :key="s.id"
                      @click="selectStaff(s)"
                      class="p-3 border-bottom border-white border-opacity-5 cursor-pointer transition-all d-flex justify-content-between align-items-center"
                      :class="{ 'opacity-50': s.occupied, 'hover-bg-glass': !s.occupied }"
                    >
                      <div>
                        <span class="d-block fw-bold text-white fs-8"><i class="bi bi-person-badge text-success me-1"></i> {{ s.name }}</span>
                        <span class="fs-10 text-success-tint font-monospace">{{ s.email }}</span>
                      </div>
                      
                      <span v-if="s.occupied" class="badge bg-danger bg-opacity-20 text-danger-tint border border-danger border-opacity-25 rounded-pill fs-10">Occupied</span>
                      <span v-else-if="form.assigned_staff_id === s.id" class="badge bg-success text-dark rounded-pill fs-10"><i class="bi bi-check-lg"></i> Selected</span>
                    </div>

                  </div>
                </Transition>
              </div>
              <div class="col-12">
                <label class="modal-label">Expedition Media Gallery (Select 4 images, Max 500KB each) *</label>
                <div class="input-wrapper py-1.5">
                  <input id='trek_image' type="file" accept="image/*" multiple @change="handleMultipleImagesSelection" class="hidden-file-input text-white-50" >
                  <label for="trek_image" class="file-custom-btn">Choose file</label>
                  <span class="file-name-label">{{ fileNameDisplay }}</span>
                </div>
                <small v-if="selectedGalleryFiles.length" class="text-success-tint mt-1 d-block fs-9 fw-medium">
                  <i class="bi bi-check-lg text-success"></i> {{ selectedGalleryFiles.length }} image(s) selected for compilation queue.
                </small>
              </div>
              <div class="col-12">
                <label class="modal-label">Expedition Description</label>
                <div class="input-wrapper py-2">
                  <textarea v-model="form.description" rows="3" class="modal-field text-area-fix" placeholder="Describe terrain boundaries, environmental risk variables..."></textarea>
                </div>
              </div>
              <div class="col-12 mt-2">
                <label class="modal-label text-success-tint d-flex justify-content-between">
                  <span>Geographical Telemetry *</span>
                  <span class="fs-10 font-monospace text-white-50">LAT: {{ form.latitude }} · LNG: {{ form.longitude }}</span>
                </label>
                <button type="button" @click="openMapLocator" class="btn btn-outline-success w-100 rounded-3 py-2 fs-9 fw-bold d-flex align-items-center justify-content-center gap-2 bg-success bg-opacity-10">
                  <i class="bi bi-geo-alt-fill fs-8"></i> Open Tactical Map Picker
                </button>
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

    <Transition name="modal-fade">
      <div v-if="mapPickerActive" @click.self="mapPickerActive = false" class="admin-modal-backdrop d-flex align-items-center justify-content-center p-3" style="z-index: 1060;">
        <div class="glass-modal-card p-4 rounded-4 border border-success border-opacity-30 shadow-lg d-flex flex-column" style="max-width: 650px; width: 100%; height: 80vh; max-height: 550px;">
          
          <!-- Header -->
          <div class="d-flex justify-content-between align-items-center mb-3 pb-2 border-bottom border-white border-opacity-10 flex-shrink-0">
            <div>
              <h5 class="fw-bold text-white m-0 tracking-tight">Basecamp Grid Deployment</h5>
              <span class="fs-10 text-white-50">Pan satellite feed and click target terrain to drop marker.</span>
            </div>
            <button @click="resetPinToCenter" class="btn btn-sm btn-outline-warning rounded-pill fs-10 px-3 py-1 fw-bold" title="Reset Pin">
              <i class="bi bi-arrow-counterclockwise me-1"></i> Reset Pin
            </button>
          </div>

          <!-- The Leaflet Component -->
          <div class="flex-grow-1 w-100 rounded-3 overflow-hidden border border-white border-opacity-10 mb-3 position-relative">
            <TrekMap :lat="tacticalCoords.lat" :lng="tacticalCoords.lng" :interactive="true" @update:coords="handlePinMoved" />
          </div>

          <!-- Footer -->
          <div class="d-flex gap-3 flex-shrink-0 mt-auto">
            <button type="button" @click="mapPickerActive = false" class="btn btn-outline-light rounded-pill px-4 py-2 flex-grow-1 fs-8">Cancel</button>
            <button type="button" @click="lockGridCoordinates" class="btn btn-success rounded-pill px-4 py-2 fw-bold text-dark flex-grow-1 fs-8 shadow-sm">
              <i class="bi bi-check-lg me-1"></i> Lock & Transmit Grid
            </button>
          </div>

        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import TrekMap from '../../components/TrekMap.vue'
import { useAlertStore } from '../../stores/alert'
import { useAuthStore } from '../../stores/auth'
import { useConfirmStore } from '../../stores/confirm'
import { secureFetch } from '@/utils/api'
import { resolveMediaUrl } from '@/utils/media'

const router = useRouter()
const alertStore = useAlertStore()
const authStore = useAuthStore()
const confirmStore = useConfirmStore()

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
const adminTreks = ref([])
const staffDropdown = ref([])
// -----
const staffSearchQuery = ref('')
const staffDropdownOpen = ref(false)
const createModalActive = ref(false)
const selectedGalleryFiles = ref([])
const fileNameDisplay = ref('No file chosen')
const filterExtremes = ref({ max_altitude: 6000 , max_price: 50000 , min_altitude: 0, min_price: 0})

// Filtering state metrics
const filters = ref({ query: '', difficulty: '', price: 25000, altitude: 10000 })

const mapPickerActive = ref(false)
const tacticalCoords = ref({ lat: 32.2396, lng: 77.1887 })

// Model alignment fields mapping
const form = ref({
  name: '', location: '', difficulty: 'Moderate', duration_days: 3,
  available_slots: 15, max_altitude: 3000, price_per_person: 5000,
  start_date: '', end_date: '', description: '', assigned_staff_id: null,
  latitude: 32.2396, longitude: 77.1887
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
    const res = await secureFetch(`${BACKEND_URL}/api/admin/treks`, { method: 'GET', headers })
    if (res.ok) {
      adminTreks.value = await res.json()
    }
  } catch (err) {
    alertStore.showAlert(`Telemetry Sync Drop: ${err.message}`, 'danger')
  }
}

async function syncMinMax() {
  try {
    const headers = { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' }
    const res = await secureFetch(`${BACKEND_URL}/api/utils/trek-extremes`, { method: 'GET', headers })
    if (res.ok) {
      filterExtremes.value = await res.json()
    }
  } catch (err) {
    alertStore.showAlert(`Telemetry Sync Drop: ${err.message}`, 'danger')
  }
}


watch(
  [() => form.value.start_date, () => form.value.end_date],
  async ([newStart, newEnd]) => {
    // Only fetch if BOTH dates are provided
    if (newStart && newEnd) {
      try {
        const res = await secureFetch(
          `${BACKEND_URL}/api/admin/staff?start_date=${newStart}&end_date=${newEnd}`, 
          { method: 'GET' , headers: { 'Authorization': `Bearer ${authStore.token}` } }
        )
        if (res.ok) staffDropdown.value = await res.json()
      } catch (err) {
        console.error("Failed to fetch dynamic staff availability.")
      }
    }
  }
)

// Computed property to filter out inactive staff AND apply the search query
const availableStaff = computed(() => {
  if (!staffDropdown.value) return []
  
  return staffDropdown.value.filter(s => {
    // 1. Must be active (adjust checking logic based on your exact backend payload boolean/string)
    const isActive = s.is_active === true || s.is_active === 'Active'
    if (!isActive) return false
    
    // 2. Must match search query (if any)
    const matchesSearch = s.name.toLowerCase().includes(staffSearchQuery.value.toLowerCase()) || 
                          s.email.toLowerCase().includes(staffSearchQuery.value.toLowerCase())
                          
    return matchesSearch
  })
})

// Function to handle selection
function selectStaff(staff) {
  if (staff.occupied) return // Prevent clicking occupied staff
  
  form.value.assigned_staff_id = staff.id
  staffSearchQuery.value = staff.name // Update the input to show the selected name
  staffDropdownOpen.value = false
}

// Function to clear selection
function clearStaffSelection() {
  form.value.assigned_staff_id = null
  staffSearchQuery.value = ''
  staffDropdownOpen.value = false
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
  
  if (files.length === 0) {
    alertStore.showAlert('Please select images for trek', 'danger')
    form.value.trek_gallery = []
    return
  }

  // Strict 4-image rule
  if (files.length !== 4) {
    alertStore.showAlert('You must select exactly 4 images for the terrain gallery.', 'warning')
    event.target.value = '' // Reset the input
    form.value.trek_gallery = []
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
    fileNameDisplay.value = file.name
  }
}

function openMapLocator() {
  tacticalCoords.value.lat = form.value.latitude || 32.2396
  tacticalCoords.value.lng = form.value.longitude || 77.1887
  mapPickerActive.value = true
}

function handlePinMoved(newCoords) {
  tacticalCoords.value.lat = newCoords.lat
  tacticalCoords.value.lng = newCoords.lng
}

function resetPinToCenter() {
  tacticalCoords.value.lat = 32.2396
  tacticalCoords.value.lng = 77.1887
}

function lockGridCoordinates() {
  form.value.latitude = tacticalCoords.value.lat
  form.value.longitude = tacticalCoords.value.lng
  mapPickerActive.value = false
}

async function submitTrekForm() {
  // Multipart packaging data configuration layers

  if (selectedGalleryFiles.value.length === 0) {
    alertStore.showAlert('Please select images for trek', 'danger')
    return // Stop the submission
  }

  if (!form.value.latitude || !form.value.longitude) {
  alertStore.showAlert('Please pin the trek start coordinate.', 'warning')
  return
  }

  const formData = new FormData()
  Object.keys(form.value).forEach(key => {
    formData.append(key, form.value[key])
  })
  selectedGalleryFiles.value.forEach(file => {
    formData.append('trek_gallery', file)
  })

  try {
    const res = await secureFetch(`${BACKEND_URL}/api/admin/treks`, {
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

function routeToDeepInsights(id) {
  // Automatically routes down to your reusable nested component structure
  router.push(`/portal/trek/view/${id}`)
}

onMounted(() => {
  syncMinMax()
  syncTrekDataset()
})
</script>

<style scoped>

/* Style the input field itself */
input[type="date"] {
  background-color: rgba(62, 66, 57, 0.314);
  color: white;
  border: 1px solid #333;
  padding: 10px;
  border-radius: 8px;
}

/* Hide or modify the calendar icon */
input[type="date"]::-webkit-calendar-picker-indicator {
  cursor: pointer;
  filter: invert(1); /* Makes the black icon white for dark themes */
}

/* Style the text parts inside the input (day, month, year text) */
input[type="date"]::-webkit-datetime-edit { padding: 2px; }
input[type="date"]::-webkit-datetime-edit-fields-wrapper { background: transparent; }
input[type="date"]::-webkit-datetime-edit-text { color: #888; padding: 0 0.3em; }
input[type="date"]::-webkit-datetime-edit-month-field { color: #fff; }
input[type="date"]::-webkit-datetime-edit-day-field { color: #fff; }
input[type="date"]::-webkit-datetime-edit-year-field { color: #fff; }

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
.status-pill.cancelled { background: rgba(220, 53, 69, 0.8); }
.status-pill.completed { background: rgba(13, 110, 253, 0.8); }
.status-pill.ongoing { background: rgba(255, 193, 7, 0.8); color: black; }

.difficulty-pill { padding: 3px 9px; font-size: 0.7rem; border-radius: 20px; font-weight: 600; text-transform: uppercase; }
.difficulty-pill.easy { background: rgba(25, 135, 84, 0.8); }
.difficulty-pill.moderate { background: rgba(255, 193, 7, 0.8); color: black; }
.difficulty-pill.hard { background: rgba(220, 53, 69, 0.8); }

/* Modal overlay layouts */
.admin-modal-backdrop { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0, 0, 0, 0.8) !important; backdrop-filter: blur(8px); z-index: 999; }
.glass-modal-card { background: rgba(13, 20, 16, 0.96) !important; backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.15) !important; box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7); width: 100%; max-width: 650px; }
.max-vh-70 { max-height: 70vh; }

.modal-label { font-size: 0.78rem; color: rgba(255,255,255,0.5); font-weight: 500; margin-bottom: 3px; display: block; }
.input-wrapper { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12); border-radius: 8px; padding: 6px 12px; }
.modal-field { border: none; background: transparent; color: #fff; outline: none; width: 100%; font-size: 0.9rem; }
.text-area-fix { resize: none; line-height: 1.4; }
.select-fix option { background: #1c241e; color: white; }

.file-custom-btn {
  background: rgba(255, 255, 255, 0.15);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  margin: 0;
  transition: background 0.2s;
}
.file-custom-btn:hover {
  background: rgba(255, 255, 255, 0.25);
}
.hidden-file-input {
  display: none;
}
.file-name-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.88rem;
  margin-left: 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.custom-slider::-webkit-slider-runnable-track { background: rgba(255, 255, 255, 0.1); border-radius: 5px; height: 4px; }
.custom-slider::-webkit-slider-thumb { background: #198754; margin-top: -6px; }

.extra-small { font-size: 0.68rem; }
.fs-8 { font-size: 0.88rem; }
.fs-9 { font-size: 0.76rem; }


.trek-premium-card {
  min-height: 440px;       /* Taller to give landscape images room to breathe */
  height: 100%;            /* Ensures flex children behave */
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.05); /* Extremely subtle border */
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  background-color: #0d0f12;
  overflow: hidden;
}

/* Hover Selection Outline & Lift */
.trek-premium-card:hover {
  border-color: rgba(255, 255, 255, 0.4); 
  transform: translateY(-5px);            
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
}

/* The Image Wrapper & Zoom Effect */
.card-bg-wrapper {
  overflow: hidden;
  border-radius: inherit; /* Keeps the rounded corners clean */
}

.card-bg-img {
  transition: transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.trek-premium-card:hover .card-bg-img {
  transform: scale(1.06); /* The "Ken Burns" subtle zoom */
}

/* Gradient Overlay - Reversed to explicitly build from the bottom up */
.card-gradient-overlay {
  background: linear-gradient(
    to top, 
    rgba(0, 8, 15, 0.98) 0%,   /* Solid dark at the very bottom */
    rgb(0, 7, 14) 25%,  /* Heavy dark behind the text */
    rgba(1, 8, 15, 0.21) 50%,   /* Fading out */
    rgba(8, 10, 12, 0.1) 80%, 
    rgba(0, 0, 0, 0) 100%
  );
  pointer-events: none; 
}
/* Extra small font size for meta tags */
.fs-10 {
  font-size: 0.72rem;
}

/* Utility Classes */
.object-cover { object-fit: cover; }
.backdrop-blur { backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); }
.tracking-tight { letter-spacing: -0.03em; }
.text-shadow-sm { text-shadow: 0 2px 10px rgba(0,0,0,0.5); }

/* Button Hover State */
.premium-action-btn:hover {
  background-color: rgba(255, 255, 255, 0.2) !important;
  color: #fff;
}

.z-index-top { z-index: 1050; } .hover-bg-glass:hover { background: rgba(255,255,255,0.05); }

</style>