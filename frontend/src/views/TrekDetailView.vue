<template>
  <div class="portal-content-page text-white text-start pb-5">
    
    <div class="mb-4">
      <button @click="$router.back()" class="btn btn-sm btn-outline-light rounded-pill px-3.5 py-1.5 fs-9 border-opacity-25">
        ← Back to List
      </button>
    </div>

    <div v-if="loading" class="text-center py-5 text-white-50 small opacity-50">
       Synchronizing operational trail coordinates telemetry...
    </div>
    
    <div v-else-if="!trekData" class="text-center py-5 text-danger">
      ❌ Expedition profile coordinates failed verification checkpoint.
    </div>

    <div v-else>
      <TrekDetail 
        :trek="trekData" 
        @request-checkout="checkoutActive = true"
        @admin-delete="handleAdminDeletePurge"
        @admin-modify="openModifyFormModal"
        @staff-toggle-status="handleStaffStatusChange"
      />
    </div>

    <Transition name="modal-fade">
      <div v-if="checkoutActive" class="checkout-overlay-backdrop d-flex align-items-center justify-content-center p-3">
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
              ⚠️ Senior slots require submitting a physical fitness certificate at basecamp arrival.
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
      <div v-if="modifyModalActive" class="checkout-overlay-backdrop d-flex align-items-center justify-content-center p-3">
        <div class="glass-checkout-card p-4 p-md-5 rounded-4 border border-white border-opacity-15 shadow-lg overflow-y-auto max-vh-90 text-start" style="max-width: 650px;">
          
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
                <div class="modal-input-wrapper"><input v-model="editForm.start_date" type="date" class="modal-clean-field"></div>
              </div>
              <div class="col-md-6">
                <label class="modal-input-label">End Date Coordinates</label>
                <div class="modal-input-wrapper"><input v-model="editForm.end_date" type="date" class="modal-clean-field"></div>
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
                    <option value="Pending">Pending</option> <option value="Approved">Approved</option>
                    <option value="Open">Open</option> <option value="Closed">Closed</option> <option value="Completed">Completed</option>
                  </select>
                </div>
              </div>
              <div class="col-12">
                <label class="modal-input-label">Change Assigned Guide Staff</label>
                <div class="modal-input-wrapper">
                  <select v-model="editForm.assigned_staff_id" class="modal-clean-field bg-transparent select-fix">
                    <option :value="null">Leave Unassigned</option>
                    <option v-for="s in staffOptions" :key="s.id" :value="s.id">👨‍✈️ {{ s.name }}</option>
                  </select>
                </div>
              </div>
              <div class="col-12">
                <label class="modal-input-label">Replace Gallery Images (Max 4, Capped at 500KB each)</label>
                <div class="modal-input-wrapper py-1.5"><input type="file" accept="image/*" multiple @change="handleUpdateFiles" class="modal-clean-field text-white-50"></div>
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

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import TrekDetail from '../components/TrekDetail.vue'
import { useAlertStore } from '../stores/alert'
import { useAuthStore } from '../stores/auth'
import { useConfirmStore } from '../stores/confirm'

const route = useRoute()
const router = useRouter()
const alertStore = useAlertStore()
const authStore = useAuthStore()
const confirmStore = useConfirmStore()

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
const trekData = ref(null)
const loading = ref(true)
const checkoutActive = ref(false)

const modifyModalActive = ref(false)
const staffOptions = ref([])
const updateGalleryFiles = ref([])
const editForm = ref({})

const form = ref({ adults: 1, children: 0, seniors: 0, payment_method: 'UPI', medical_instructions: '' })

const totalPassengers = computed(() => form.value.adults + form.value.children + form.value.seniors)
const computedTotalPrice = computed(() => {
  if (!trekData.value) return 0
  return totalPassengers.value * trekData.value.price_per_person
})

async function fetchLiveTrekDetails() {
  try {
    loading.value = true
    const res = await fetch(`${BACKEND_URL}/api/admin/treks/${route.params.id}/details`, {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      trekData.value = await res.json()
    } else {
      alertStore.showAlert('Expedition mapping verification drop.', 'danger')
    }
  } catch (err) {
    alertStore.showAlert(`Sync Drop: ${err.message}`, 'danger')
  } finally {
    loading.value = false
  }
}

async function submitBookingRequest() {
  try {
    const res = await fetch(`${BACKEND_URL}/api/admin/staff`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ trek_id: trekData.value.trek_id, ...form.value })
    })
    const data = await res.json()
    if (res.ok) {
      alertStore.showAlert(data.message || 'Slot booked successfully!', 'success')
      checkoutActive.value = false
      router.push('/portal/trekker/bookings')
    } else {
      alertStore.showAlert(data.message || 'Booking transaction rejected.', 'danger')
    }
  } catch (err) {
    alertStore.showAlert(`Network drop: ${err.message}`, 'danger')
  }
}

function handleAdminDeletePurge() {
  confirmStore.ask('Purge this entire trek out of system tables?', async () => {
    const res = await fetch(`${BACKEND_URL}/api/admin/treks/${trekData.value.trek_id}`, {
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
  const staffRes = await fetch(`${BACKEND_URL}/api/admin/staff`, {
    method: 'GET', headers: { 'Authorization': `Bearer ${authStore.token}` }
  })
  if (staffRes.ok) staffOptions.value = await staffRes.json()

  // Seed model input proxies with active row values context mapping fields perfectly
  editForm.value = {
    trek_name: trekData.value.trek_name, location: trekData.value.location,
    difficulty: trekData.value.difficulty, duration_days: trekData.value.duration_days,
    available_slots: trekData.value.available_slots, status: trekData.value.status,
    start_date: trekData.value.start_date, end_date: trekData.value.end_date,
    max_altitude: trekData.value.max_altitude, price_per_person: trekData.value.price_per_person,
    description: trekData.value.description, assigned_staff_id: trekData.value.staff?.id || null
  }
  updateGalleryFiles.value = []
  modifyModalActive.value = true
}

function handleUpdateFiles(event) {
  const files = Array.from(event.target.files)
  if (files.length > 4) {
    alertStore.showAlert('Gallery limits capped at 4 items maximum.', 'danger')
    event.target.value = ''
    return
  }
  const MAX_LIMIT = 500 * 1024
  for (const f of files) {
    if (f.size > MAX_LIMIT) {
      alertStore.showAlert('Each image selection must stand below exactly 500KB.', 'danger')
      event.target.value = ''
      return
    }
  }
  updateGalleryFiles.value = files
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
    const res = await fetch(`${BACKEND_URL}/api/admin/treks/${trekData.value.trek_id}`, {
      method: 'PUT', headers: { 'Authorization': `Bearer ${authStore.token}` }, body: formData
    })
    if (res.ok) {
      alertStore.showAlert('Expedition record variables patched inside core tables.', 'success')
      modifyModalActive.value = false
      await fetchLiveTrekDetails() // Re-fetch fields cleanly
    }
  } catch (err) { alertStore.showAlert(`Patch drop: ${err.message}`, 'danger') }
}

function handleStaffStatusChange() {
  alertStore.showAlert('Toggling route visibility operations lifecycle flags...', 'warning')
}

onMounted(() => {
  fetchLiveTrekDetails()
})
</script>

<style scoped>
.checkout-overlay-backdrop { position: fixed !important; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(10, 20, 15, 0.55) !important; backdrop-filter: blur(20px) !important; -webkit-backdrop-filter: blur(20px) !important; z-index: 999999999 !important; }
.glass-checkout-card { background: rgba(25, 35, 30, 0.88) !important; backdrop-filter: blur(35px); width: 100%; max-width: 440px; }
.form-group-capsule { display: flex; flex-direction: column; text-align: left; }
.modal-input-label { font-size: 0.82rem; color: rgba(255, 255, 255, 0.6); font-weight: 500; margin-bottom: 4px; }
.modal-input-wrapper { background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 8px 12px; display: flex; align-items: center; }
.modal-clean-field { border: none; background: transparent; color: #ffffff; width: 100%; font-size: 0.92rem; outline: none; }
.text-area-fix { resize: none; line-height: 1.4; }
.select-fix option { background: #16241c; color: white; }
.btn-close-modal { position: absolute; top: 20px; right: 20px; background: transparent; border: none; color: rgba(255,255,255,0.5); font-size: 1.1rem; cursor: pointer; }
.btn-close-modal:hover { color: white; }
.alert-senior-msg { background: rgba(255, 193, 7, 0.08); }
.fs-8 { font-size: 0.88rem; } .fs-9 { font-size: 0.76rem; } .gap-3 { gap: 12px; }
</style>