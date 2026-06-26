<template>
  <div class="portal-content-page text-white text-start pb-5 px-3">
    
    <div class="mb-4">
      <button @click="$router.back()" class="btn btn-sm btn-outline-light rounded-pill px-3 py-1 fs-9 border-opacity-25">
        ← Back to List
      </button>
    </div>

    <div v-if="loading" class="text-center py-5 text-white-50 small opacity-50">
       Synchronizing operational trail coordinates telemetry...
    </div>
    
    <div v-else-if="!trekData" class="text-center py-5 text-danger">
      <i class="bi bi-exclamation-triangle-fill text-danger"></i> Expedition profile coordinates failed verification checkpoint.
    </div>

    <div v-else>
      <TrekDetail 
        :trek="trekData" 
        :showCheckoutButton=true           
        @request-checkout="checkoutActive = true"
        @admin-delete="handleAdminDeletePurge"
        @admin-modify="openModifyFormModal"
        @staff-toggle-status="openStaffModifyModal"
      />
    </div>
    <PaymentModal 
      :active="terminalActive" 
      :payload="paymentPayload"
      @payment-success="finalizeBookingTransaction" 
      @payment-failed="failedBooking"
    />
    <div v-if="!show" class="glass-container p-4 rounded-4 border border-white border-opacity-10 mb-4" style="height: 22rem;">
      <h6 class="fw-bold fs-9 tracking-wider opacity-75 text-uppercase mb-3 border-bottom border-white border-opacity-10 pb-2">
        <i class="bi bi-compass me-1"></i> Satellite Basecamp Telemetry
      </h6>
      <TrekMap :lat="absoluteLat" :lng="absoluteLng" :popupText="location" :interactive="false" />
    </div>
    <div v-else class="border border-secondary border-opacity-25 rounded-3 p-4 text-center text-white-50">
      <i class="bi bi-radar d-block fs-3 mb-1"></i>
      <span class="font-monospace fs-9">TELEMETRY DATA PENDING FIELD RECONNAISSANCE</span>
    </div>

    <Transition name="modal-fade">
      <div v-if="checkoutActive" @click.self="checkoutActive = false" class="checkout-overlay-backdrop d-flex align-items-center justify-content-center p-3">
        <div class="glass-checkout-card p-4 p-md-5 rounded-4 border border-white border-opacity-15 shadow-lg text-start animate-scale-up position-relative">
          
          <button @click="checkoutActive = false" class="btn-close-modal">✕</button>
          <h4 class="fw-bold tracking-tight text-center text-white m-0 mb-4">Book your trek</h4>

          <form @submit.prevent="submitBookingRequest" class="d-flex flex-column gap-3">
            <div class="form-group-capsule">
              <label class="modal-input-label">Adults :</label>
              <div class="modal-input-wrapper"><input v-model.number="form.adults" type="number" min="1" max="10" required class="modal-clean-field"></div>
            </div>
            <div class="form-group-capsule">
              <label class="modal-input-label">Children :</label>
              <div class="modal-input-wrapper"><input v-model.number="form.children" type="number" min="0" max="5" required class="modal-clean-field"></div>
            </div>
            <div class="form-group-capsule">
              <label class="modal-input-label">Senior :</label>
              <div class="modal-input-wrapper"><input v-model.number="form.seniors" type="number" min="0" max="5" required class="modal-clean-field"></div>
            </div>
            <div class="form-group-capsule mt-1">
              <label class="modal-input-label">Instructions (if any)</label>
              <div class="modal-input-wrapper py-2">
                <textarea v-model="form.medical_instructions" rows="3" class="modal-clean-field text-area-fix" placeholder="Describe health conditions, medical requirements or trail care notes..."></textarea>
              </div>
            </div>
            <div class="form-group-capsule">
              <label class="modal-input-label">Payment Type :</label>
              <div class="modal-input-wrapper">
                <select v-model="form.payment_method" class="modal-clean-field bg-transparent select-fix" required>
                  <option value="UPI">UPI Gateway</option>
                  <option value="Card">Credit / Debit Card</option>
                  <option value="NetBanking">NetBanking Portal</option>
                </select>
              </div>
            </div>

            <div v-if="form.seniors > 0" class="alert-senior-msg p-2 rounded small text-warning text-center border border-warning border-opacity-10 fs-9">
              <i class="bi bi-exclamation-triangle-fill text-warning"></i> Senior slots require submitting a physical fitness certificate at basecamp arrival.
            </div>

            <div class="mt-3">
              <button type="submit" class="btn btn-success w-100 rounded-3 py-2.5 fw-bolder text-dark fs-8 tracking-tight border-0 shadow-sm text-uppercase">
                Pay : ₹{{ computedTotalPrice }}
              </button>
            </div>
          </form>

        </div>
      </div>
    </Transition>


    <Transition name="modal-fade">
      <div v-if="modifyModalActive" @click.self="modifyModalActive = false" class="checkout-overlay-backdrop d-flex align-items-center justify-content-center p-3">
        <div class="glass-checkout-card p-4 p-md-5 rounded-4 border border-white border-opacity-15 shadow-lg overflow-y-auto max-vh-12 text-start" style="max-width: 35rem; max-height: 45rem;">
          
          <button @click="modifyModalActive = false" class="btn-close-modal">✕</button>
          <h4 class="fw-bold tracking-tight text-white m-0 mb-4 text-center">Modify Trek Matrix</h4>

          <form @submit.prevent="submitModificationForm" class="d-flex flex-column gap-3">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="modal-input-label">Trek Route Name</label>
                <div class="modal-input-wrapper"><input v-model="editForm.trek_name" type="text" required class="modal-clean-field"></div>
              </div>
              <div class="col-md-6">
                <label class="modal-input-label">Location Sector</label>
                <div class="modal-input-wrapper"><input v-model="editForm.location" type="text" required class="modal-clean-field"></div>
              </div>
              <div class="col-md-4">
                <label class="modal-input-label">Intensity Range</label>
                <div class="modal-input-wrapper">
                  <select v-model="editForm.difficulty" class="modal-clean-field bg-transparent select-fix">
                    <option value="Easy">Easy Range</option> <option value="Moderate">Moderate Track</option> <option value="Hard">High Hard</option>
                  </select>
                </div>
              </div>
              <div class="col-md-4">
                <label class="modal-input-label">Duration Days</label>
                <div class="modal-input-wrapper"><input v-model.number="editForm.duration_days" type="number" required class="modal-clean-field"></div>
              </div>
              <div class="col-md-4">
                <label class="modal-input-label">Slots Capacity</label>
                <div class="modal-input-wrapper"><input v-model.number="editForm.available_slots" type="number" required class="modal-clean-field"></div>
              </div>
              <div class="col-md-6">
                <label class="modal-input-label">Start Date Coordinates</label>
                <input v-model="editForm.start_date" type="date" class="modal-clean-field">
              </div>
              <div class="col-md-6">
                <label class="modal-input-label">End Date Coordinates</label>
                <input v-model="editForm.end_date" type="date" class="modal-clean-field">
              </div>
              <div class="col-md-6">
                <label class="modal-input-label">Peak Altitude (mt)</label>
                <div class="modal-input-wrapper"><input v-model.number="editForm.max_altitude" type="number" step="any" class="modal-clean-field"></div>
              </div>
              <div class="col-md-6">
                <label class="modal-input-label">Price Per Person (INR)</label>
                <div class="modal-input-wrapper"><input v-model.number="editForm.price_per_person" type="number" step="any" class="modal-clean-field"></div>
              </div>
              <div class="col-12">
                <label class="modal-input-label">Status Lifecycle State</label>
                <div class="modal-input-wrapper">
                  <select v-model="editForm.status" class="modal-clean-field bg-transparent select-fix">
                    <option value="Pending" disabled selected>Select Status</option>
                    <option value="Open">Open</option> <option value="Ongoing">On going</option> <option value="Closed">Closed</option> 
                    <option value="Completed">Completed</option> <option value="Cancelled">Cancelled</option>
                  </select>
                </div>
                <Transition name="fade">
                  <div v-if="editForm.status === 'Cancelled'" class="form-group-capsule mt-2 border-start border-danger border-4 ps-3 bg-danger bg-opacity-10 p-2 rounded">
                    <label class="modal-input-label text-danger-tint fw-bold m-0 mb-1">Mandatory Abort Synopsis (Reason)</label>
                    <div class="modal-input-wrapper py-1">
                      <textarea v-model="editForm.cancellation_reason" required rows="2" class="modal-clean-field text-area-fix text-white" placeholder="Detail weather conditions, trail blockages, or safety hazards..."></textarea>
                    </div>
                  </div>
                </Transition>
              </div>
              <!-- <div class="col-12">
                <label class="modal-input-label">Change Assigned Guide Staff</label>
                <div class="modal-input-wrapper">
                  <select v-model="editForm.assigned_staff_id" class="modal-clean-field bg-transparent select-fix">
                    <option :value="null">Leave Unassigned</option>
                    <option 
                      v-for="s in staffOptions" 
                      :key="s.id" 
                      :value="s.id" 
                      :disabled="s.occupied"
                      :class="{ 'text-danger': s.occupied }"
                    >
                      👨‍✈️ {{ s.name }} 
                    </option>
                  </select>
                </div>
              </div> -->
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
                        <span class="d-block fw-bold text-white fs-8">👨‍✈️ {{ s.name }}</span>
                        <span class="fs-10 text-success-tint font-monospace">{{ s.email }}</span>
                      </div>
                      
                      <span v-if="s.occupied" class="badge bg-danger bg-opacity-20 text-danger-tint border border-danger border-opacity-25 rounded-pill fs-10">Occupied</span>
                      <span v-else-if="editForm.assigned_staff_id === s.id" class="badge bg-success text-dark rounded-pill fs-10"><i class="bi bi-check-lg"></i> Selected</span>
                    </div>

                  </div>
                </Transition>
              </div>

              <div class="col-12">
                <label class="modal-input-label">Replace Gallery Images (Max 4, Capped at 500KB each)</label>
                <div class="modal-input-wrapper py-2">
                  <input id='trek_image' type="file" accept="image/*" multiple @change="handleUpdateFiles" class="hidden-file-input text-white-50" >
                  <label for="trek_image" class="file-custom-btn">Choose file</label>
                  <span class="file-name-label">{{ fileNameDisplay }}</span>
                </div>
                <small v-if="updateGalleryFiles.length" class="text-success-tint mt-1 d-block fs-9 fw-medium">
                  ✔ {{ updateGalleryFiles.length }} image(s) selected for compilation queue.
                </small>
              </div>
              <div class="col-12">
                <label class="modal-input-label">Description Synopsis</label>
                <div class="modal-input-wrapper py-2"><textarea v-model="editForm.description" rows="3" class="modal-clean-field text-area-fix"></textarea></div>
              </div>
            </div>

            <div class="mt-4 d-flex justify-content-end gap-3 border-top border-white border-opacity-10 pt-3">
              <button type="button" @click="modifyModalActive = false" class="btn btn-outline-light rounded-pill px-4 py-2 fs-8">Cancel</button>
              <button type="submit" class="btn btn-success rounded-pill px-5 py-2.5 fw-bold text-dark fs-8">Commit Changes</button>
            </div>
          </form>

        </div>
      </div>
    </Transition>

    <!-- ===================================================================
         STAFF OVERRIDE: FIELD OPERATIONS POPUP MODAL
         =================================================================== -->
    <Transition name="modal-fade">
      <div v-if="staffModifyModalActive" @click.self="staffModifyModalActive = false" class="checkout-overlay-backdrop d-flex align-items-center justify-content-center p-3">
        <div class="glass-checkout-card p-4 p-md-5 rounded-4 border border-white border-opacity-15 shadow-lg overflow-y-auto max-vh-90 text-start" style="max-width: 500px;">
          
          <button @click="staffModifyModalActive = false" class="btn-close-modal">✕</button>
          <h4 class="fw-bold tracking-tight text-white m-0 mb-4 text-center">Field Operations Override</h4>
          <p class="text-white-50 small text-center mb-4">Adjust real-time tracking parameters for your currently assigned trail.</p>

          <form @submit.prevent="submitStaffFieldUpdate" class="d-flex flex-column gap-3">
            <div class="row g-3">
              
              <!-- Staff Controlled: Lifecycle Status -->
              <div class="col-12">
                <label class="modal-input-label">Route Lifecycle State</label>
                <div class="modal-input-wrapper">
                  <select v-model="staffEditForm.status" class="modal-clean-field bg-transparent select-fix" required>
                    <option value="Open">Open</option>
                    <option value="Ongoing">Ongoing</option>
                    <option value="Closed">Closed </option>
                    <option value="Completed">Completed</option>
                    <option value="Cancelled">Cancelled </option>
                  </select>
                </div>
              </div>

              <Transition name="fade">
                <div v-if="staffEditForm.status === 'Cancelled'" class="form-group-capsule mt-2 border-start border-danger border-4 ps-3 bg-danger bg-opacity-10 p-2 rounded">
                  <label class="modal-input-label text-danger-tint fw-bold m-0 mb-1">Mandatory Abort Synopsis (Reason)</label>
                  <div class="modal-input-wrapper py-1">
                    <textarea v-model="staffEditForm.cancellation_reason" required rows="2" class="modal-clean-field text-area-fix text-white" placeholder="Detail weather conditions, trail blockages, or safety hazards..."></textarea>
                  </div>
                </div>
              </Transition>

              <!-- Staff Controlled: Live Slots Configuration -->
              <div class="col-12">
                <label class="modal-input-label">Adjust Available Slots</label>
                <div class="modal-input-wrapper">
                  <input v-model.number="staffEditForm.available_slots" type="number" min="0" required class="modal-clean-field" placeholder="Update live capacity...">
                </div>
              </div>

              <!-- Staff Controlled: Live Trail Notes -->
              <div class="col-12">
                <label class="modal-input-label">Live Field Notes & Description</label>
                <div class="modal-input-wrapper py-2">
                  <textarea v-model="staffEditForm.description" rows="4" class="modal-clean-field text-area-fix" placeholder="Log real-time weather shifts, trail blockages, or group updates here..."></textarea>
                </div>
              </div>

            </div>

            <div class="mt-4 d-flex justify-content-end gap-3 border-top border-white border-opacity-10 pt-3">
              <button type="button" @click="staffModifyModalActive = false" class="btn btn-outline-light rounded-pill px-4 py-2 fs-8">Cancel</button>
              <button type="submit" class="btn btn-success rounded-pill px-5 py-2.5 fw-bold text-dark fs-8 shadow-sm">Sync Field Data</button>
            </div>
          </form>

        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted , watch} from 'vue'
import { useRoute, useRouter } from 'vue-router'
import TrekDetail from '../components/TrekDetail.vue'
import { useAlertStore } from '../stores/alert'
import { useAuthStore } from '../stores/auth'
import { useConfirmStore } from '../stores/confirm'
import PaymentModal from '../components/PaymentModal.vue'
import TrekMap from '../components/TrekMap.vue'
import { secureFetch } from '@/utils/api.js'

const route = useRoute()
const router = useRouter()
const alertStore = useAlertStore()
const authStore = useAuthStore()
const confirmStore = useConfirmStore()

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
const trekData = ref(null)
const loading = ref(true)
const checkoutActive = ref(false)
const terminalActive = ref(false)
const showCheckoutButton = ref(true)

const modifyModalActive = ref(false)
const staffOptions = ref([])
const updateGalleryFiles = ref([])
const fileNameDisplay = ref('No file chosen')
const editForm = ref({})
const staffModifyModalActive = ref(false)
const paymentPayload = ref({})

const staffSearchQuery = ref('')
const staffDropdownOpen = ref(false)

const show = ref(true)

const staffEditForm = ref({
  status: '',
  available_slots: 0,
  description: '',
  cancellation_reason : ''
})


const absoluteLat = computed(() =>  trekData.value.latitude)
const absoluteLng = computed(() =>  trekData.value.longitude)
const location = computed(() => trekData.value.location)


const totalPassengers = computed(() => form.value.adults + form.value.children + form.value.seniors)
const computedTotalPrice = computed(() => {
  if (!trekData.value) return 0
  return totalPassengers.value * trekData.value.price_per_person
})

async function fetchLiveTrekDetails() {
  try {
    loading.value = true
    const res = await secureFetch(`${BACKEND_URL}/api/admin/treks/${route.params.id}/details`, {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      trekData.value = await res.json()
      if (trekData.value.geo) {
        show.value = false
      }
    } else {
      alertStore.showAlert('Expedition mapping verification drop.', 'danger')
    }
  } catch (err) {
    alertStore.showAlert(`Sync Drop: ${err.message}`, 'danger')
  } finally {
    loading.value = false
  }
}

function submitBookingRequest() {
  // Capture the exact snapshot of the data
  paymentPayload.value = {
    trek_id: trekData.value.trek_id,
    adults: form.value.adults,
    children: form.value.children,
    seniors: form.value.seniors,
    medical_instructions: form.value.medical_instructions,
    payment_method: form.value.payment_method
  }
  
  // Close checkout, open terminal
  checkoutActive.value = false
  terminalActive.value = true
}

async function finalizeBookingTransaction() {
  terminalActive.value = false
  alertStore.showAlert('Transaction verified. Basecamp slots secured.', 'success')
  await fetchLiveTrekDetails() // Refresh slots
  router.push('/portal/trekker/bookings')
}

async function failedBooking() {
  terminalActive.value = false
  alertStore.showAlert('Transaction failed', 'danger')
}

function handleAdminDeletePurge() {
  confirmStore.ask('Purge this entire trek out of system tables?', async () => {
    const res = await secureFetch(`${BACKEND_URL}/api/admin/treks/${trekData.value.trek_id}`, {
      method: 'DELETE', headers: { 'Authorization': `Bearer ${authStore.token}` }
    })
    if (res.ok) {
      alertStore.showAlert('Purged successfully.', 'success')
      router.back()
    }
  })
}

async function openModifyFormModal() {
  // Pull drop array lists to map staff choices
  const staffRes = await secureFetch(`${BACKEND_URL}/api/admin/staff`, {
    method: 'GET', headers: { 'Authorization': `Bearer ${authStore.token}` }
  })
  if (staffRes.ok) {
    staffOptions.value = await staffRes.json()
  }


  // Seed model input proxies with active row values context mapping fields perfectly
  editForm.value = {
    trek_name: trekData.value.trek_name, location: trekData.value.location,
    difficulty: trekData.value.difficulty, duration_days: trekData.value.duration_days,
    available_slots: trekData.value.available_slots, status: trekData.value.status || "Pending",
    start_date: trekData.value.start_date, end_date: trekData.value.end_date,
    max_altitude: trekData.value.max_altitude, price_per_person: trekData.value.price_per_person,
    description: trekData.value.description, assigned_staff_id: trekData.value.staff?.id  || null,
    cancellation_reason : trekData.value.cancellation_reason
  }

  updateGalleryFiles.value = []
  modifyModalActive.value = true
}


function handleUpdateFiles(event) {
  const files = Array.from(event.target.files)
  if (files.length !== 4) {
    alertStore.showAlert('You must select exactly 4 images for the terrain gallery.', 'warning')
    event.target.value = '' // Reset the input
    form.value.trek_gallery = []
    return
  }
  const MAX_LIMIT = 500 * 1024
  for (const f of files) {
    if (f.size > MAX_LIMIT) {
      alertStore.showAlert('Each image selection must stand below exactly 500KB.', 'danger')
      event.target.value = ''
      return
    }
    updateGalleryFiles.value = files
    fileNameDisplay.value = f.name
  }
}

async function submitModificationForm() {
  const formData = new FormData()
  Object.keys(editForm.value).forEach(key => {
    formData.append(key, editForm.value[key])
  })
  updateGalleryFiles.value.forEach(file => {
    formData.append('trek_gallery', file)
  })

  try {
    const res = await secureFetch(`${BACKEND_URL}/api/admin/treks/${trekData.value.trek_id}`, {
      method: 'PUT', headers: { 'Authorization': `Bearer ${authStore.token}` }, body: formData
    })
    if (res.ok) {
      alertStore.showAlert('Expedition record variables patched inside core tables.', 'success')
      modifyModalActive.value = false
      await fetchLiveTrekDetails() // Re-fetch fields cleanly
    }
  } catch (err) { alertStore.showAlert(`Patch drop: ${err.message}`, 'danger') }
}

function openStaffModifyModal() {
  // Seed the form with current operational parameters
  staffEditForm.value = {
    status: trekData.value.status,
    available_slots: trekData.value.available_slots,
    description: trekData.value.description,
    cancellation_reason : trekData.value.cancellation_reason
  }
  staffModifyModalActive.value = true
}

async function submitStaffFieldUpdate() {
  try {
    const res = await secureFetch(`${BACKEND_URL}/api/trek_staff/treks/${trekData.value.trek_id}/update-field-data`, {
      method: 'PATCH',
      headers: { 
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json' 
      },
      body: JSON.stringify(staffEditForm.value)
    })
    
    const data = await res.json()
    
    if (res.ok) {
      alertStore.showAlert('Field parameters synchronized with apex matrices.', 'success')
      staffModifyModalActive.value = false
      await fetchLiveTrekDetails() // Re-fetch all variables cleanly to update the UI
    } else {
      alertStore.showAlert(data.message || 'Operation denied by core systems.', 'danger')
    }
  } catch (err) {
    alertStore.showAlert(`Network drop: ${err.message}`, 'danger')
  }
}

watch(
  [() => editForm.value.start_date, () => editForm.value.end_date],
  async ([newStart, newEnd]) => {
    // Only fetch if BOTH dates are provided
    if (newStart && newEnd) {
      try {
        const res = await secureFetch(
          `${BACKEND_URL}/api/admin/staff?start_date=${newStart}&end_date=${newEnd}`, 
          { method: 'GET' , headers: { 'Authorization': `Bearer ${authStore.token}` } }
        )
        if (res.ok) staffOptions.value = await res.json()
      } catch (err) {
        console.error("Failed to fetch dynamic staff availability.")
      }
    }
  }
)

// Computed property to filter out inactive staff AND apply the search query
const availableStaff = computed(() => {
  if (!staffOptions.value) return []
  
  return staffOptions.value.filter(s => {
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
  
  editForm.value.assigned_staff_id = staff.id
  staffSearchQuery.value = staff.name // Update the input to show the selected name
  staffDropdownOpen.value = false
}

// Function to clear selection
function clearStaffSelection() {
  editForm.value.assigned_staff_id = null
  staffSearchQuery.value = ''
  staffDropdownOpen.value = false
}

onMounted(() => {
  fetchLiveTrekDetails()
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


.checkout-overlay-backdrop { position: fixed !important; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0, 0, 0, 0.456) !important; backdrop-filter: blur(5px) !important; -webkit-backdrop-filter: blur(20px) !important; z-index: 999 !important; }
.glass-checkout-card { background: rgba(6, 27, 11, 0.452) !important; backdrop-filter: blur(9px); width: 100%; max-width: 440px; }
.form-group-capsule { display: flex; flex-direction: column; text-align: left; }
.modal-input-label { font-size: 0.82rem; color: rgba(255, 255, 255, 0.6); font-weight: 500; margin-bottom: 4px; }
.modal-input-wrapper { background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 8px 12px; display: flex; align-items: center; }
.modal-clean-field { border: none; background: transparent; color: #ffffff; width: 100%; font-size: 0.92rem; outline: none; }
.text-area-fix { resize: none; line-height: 1.4; }
.select-fix option { background: #16241c; color: white; }
.btn-close-modal { position: absolute; top: 20px; right: 20px; background: transparent; border: none; color: rgba(255,255,255,0.5); font-size: 1.1rem; cursor: pointer; }
.btn-close-modal:hover { color: white; }
.alert-senior-msg { background: rgba(255, 193, 7, 0.08); }
.fs-8 { font-size: 0.88rem; } .fs-9 { font-size: 0.76rem; } .gap-3 { gap: 12px; } .fs-10 { font-size: 0.72rem; }
.modal-label { font-size: 0.78rem; color: rgba(255,255,255,0.5); font-weight: 500; margin-bottom: 3px; display: block; }
.input-wrapper { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12); border-radius: 8px; padding: 6px 12px; }
.modal-field { border: none; background: transparent; color: #fff; outline: none; width: 100%; font-size: 0.9rem; }
.z-index-top { z-index: 1050; } .hover-bg-glass:hover { background: rgba(255,255,255,0.05); }

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

</style>