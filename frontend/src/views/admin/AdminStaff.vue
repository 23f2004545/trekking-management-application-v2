<template>
  <div class="admin-staff-viewport text-white text-start pb-5 animate-fade-in px-3">
    

    <div class="d-flex align-items-center justify-content-between mb-1 flex-wrap ">
        <div class="mb-4">
            <h2 class="fw-bold tracking-tight m-0">Verified Guides Registry</h2>
            <p class="m-0 text-white-50 fs-8 mt-1">Audit active guide staff coordinates, modify account clearances or investigate blacklists.</p>
        </div>
          <button @click="openCreateModal" class="btn btn-success rounded-pill px-4 py-2 fs-8 fw-bold text-dark shadow-sm mb-2">
            <i class="bi bi-plus-lg me-2 fs-8"></i> Add Staff Member
          </button>
    </div>

    <div class="glass-container p-3 rounded-4 mb-4 shadow-sm">
      <div class="row g-2 align-items-center">
        <div class="col-md-6">
          <div class="search-field-capsule px-3 py-1 rounded-3 d-flex align-items-center">
            <span class="me-2 text-white-50 opacity-40"><i class="bi bi-search"></i></span>
            <input v-model="searchQuery" type="text" placeholder="Search by name, specialized field, or license metrics..." class="bg-transparent border-0 text-white w-100 fs-8 clean-field">
          </div>
        </div>
        <div class="col-md-6 text-md-end opacity-50 fs-9 fw-medium">
          Live Staff Records Tracked: {{ filteredStaff.length }} Operators Active
        </div>
      </div>
    </div>

    <div class="d-flex flex-column gap-3">
      <div v-for="member in filteredStaff" :key="member.id" class="staff-rect-card p-3 rounded-4 border border-white border-opacity-10 d-flex flex-wrap align-items-center justify-content-between gap-3 shadow-sm">
        
        <div class="d-flex align-items-center gap-3">
          <img :src="BACKEND_URL + (member.profile_pic )" alt="Guide Thumbnail" class="rect-avatar-img border border-white border-opacity-15 shadow" />
          <div>
            <div class="d-flex align-items-center gap-2">
              <h5 class="fw-bold m-0 text-white tracking-tight">{{ member.name }}</h5>
              <span v-if="member.blacklisted" class="badge bg-danger extra-small py-0.5 rounded px-2">BLACKLISTED</span>
            </div>
            <p class="m-0 fs-9 text-success fw-medium mt-0.5"><i class="bi bi-briefcase-fill"></i> {{ member.specialization }} ({{ member.experience }} Exp)</p>
            <p class="m-0 extra-small text-white-50 opacity-60 mt-0.5">Last login: {{ member.last_login_at }}</p>
          </div>
        </div>

        <div class="d-flex align-items-center gap-2">
          <button v-if="member.status == 'Active'" @click="openAssignmentWorkflow(member)" class="btn btn-sm btn-outline-success rounded-pill px-3 fs-9 border-opacity-35 text-white">
            Assign Route
          </button>
          <span v-else class="badge status-tag text-uppercase fs-9" :class="member.status.toLowerCase()">
             {{ member.status }}
          </span>

          <button @click="confirmStore.ask('Are you sure to ' + (member.blacklisted ? 'whitelist' : 'blacklist') + ' ' + member.name + '?', () => toggleBlacklistState(member))" class="btn btn-sm fw-bold rounded-pill px-3 fs-9 border-opacity-25" :class="member.blacklisted === false ? 'btn-warning' : 'btn-success' " >
            {{ member.blacklisted ? 'Whitelist' : 'Blacklist' }}
          </button>
          
          <button @click="launchAuditView(member.id)" class="btn btn-sm btn-info rounded-pill px-3 fs-8 fw-bold text-dark shadow-sm">
            View Profile
          </button>
        </div>

      </div>
    </div>

        <!-- ===================================================================
         3. ADD EXPEDITION PATH MODAL METRICS FORM PANEL
         =================================================================== -->
    <Transition name="modal-fade">
      <div v-if="createModalActive" @click.self="createModalActive = false" class="audit-overlay-backdrop d-flex align-items-center justify-content-center p-3">
        <div class="glass-modal-card p-4 p-md-5 rounded-4 border border-white border-opacity-15 shadow-lg overflow-y-auto max-vh-90 text-start">
          
          <h4 class="fw-bold tracking-tight text-white m-0">Add New Staff Member</h4>
          <p class="text-white-50 small m-0 mt-0.5 mb-4">Fill in the details for the new staff member you want to add.</p>

          <form @submit.prevent="submitStaffForm" class="d-flex flex-column gap-3">
                <div class="form-group-capsule">
                    <label class="modal-input-label">Staff Email</label>
                    <div class="modal-input-wrapper"><input v-model="form.email" type="email" required class="modal-clean-field"></div>
                </div>
                <div class="form-group-capsule">
                    <label class="modal-input-label">Staff Password</label>
                    <div class="modal-input-wrapper"><input v-model="form.password" type="password" required class="modal-clean-field"></div>
                </div>
                <div class="form-check d-flex align-items-center gap-2 mt-2 text-start">
                  <input v-model="form.send_credentials" type="checkbox" id="sendCredsFlag" class="form-check-input bg-dark border-secondary cursor-pointer" style="width: 18px; height: 18px;">
                  <label for="sendCredsFlag" class="form-check-label text-white-50 fs-9 cursor-pointer user-select-none">
                    Transmit initial security keys to candidate via secure email
                  </label>
                </div>
                <Transition name="fade">
                  <div v-if="form.send_credentials" class="form-group-capsule mt-2">
                    <label class="modal-input-label text-success-tint"><i class="bi bi-envelope-paper-fill me-1"></i> Candidate's Personal Email</label>
                    <div class="modal-input-wrapper">
                      <input v-model="form.personal_email" type="email" required class="modal-clean-field border-success border-opacity-25" placeholder="Where should we send the password?">
                    </div>
                  </div>
                </Transition>

            <!-- Trigger Button Rows -->
            <div class="mt-4 d-flex align-items-center justify-content-end gap-3 border-top border-white border-opacity-10 pt-3">
              <button type="button" @click="createModalActive = false" class="btn btn-outline-light rounded-pill px-4 py-2 fs-8">Cancel</button>
              <button type="submit" class="btn btn-success rounded-pill px-5 py-2.5 fw-bold text-dark fs-8">Add Staff</button>
            </div>
          </form>

        </div>
      </div>
    </Transition>

    <Transition name="modal-fade">
      <div v-if="auditTargetProfile" @click.self="auditTargetProfile = null" class="audit-overlay-backdrop d-flex align-items-center justify-content-center p-3">
        <div class="glass-modal-card p-4 p-md-5 rounded-4 border border-white border-opacity-15 shadow-lg max-vh-65 overflow-y-auto position-relative">
          
          <button @click="auditTargetProfile = null" class="btn-close-modal">✕</button>
          
          <UserProfile 
            :profile="auditTargetProfile" 
            profileRole="trek_staff" 
            @admin-toggle-blacklist="handleBlacklistAction"
            @admin-toggle-active="handleDeactivateAction"
          />

        </div>
      </div>
    </Transition>

    <Transition name="modal-fade">
      <div v-if="assignModalActive" @click.self="assignModalActive = false" class="audit-overlay-backdrop d-flex align-items-center justify-content-center p-3">
        <div class="glass-modal-card p-4 p-md-5 rounded-4 border border-white border-opacity-15 shadow-lg max-vh-90 overflow-y-auto text-start" style="max-width: 520px;">
          
          <button @click="assignModalActive = false" class="btn-close-modal">✕</button>
          <h4 class="fw-bold tracking-tight text-white m-0">Route Allocation Node</h4>
          <p class="text-white-50 small m-0 mt-0.5 mb-4">Select an active expedition trail route map coordinates to assign to <strong>{{ activeStaffTarget?.name }}</strong>.</p>

          <div class="d-flex flex-column gap-2 max-height-overflow pe-1">
            <div v-for="trek in availableTreksList" :key="trek.trek_id" class="p-3 bg-opacity-5 rounded-3 border border-white border-opacity-5 d-flex align-items-center justify-content-between gap-3 fs-8">
              <div>
                <strong class="text-white d-block">{{ trek.trek_name }}</strong>
                <span class="text-white-50 extra-small"><i class="bi bi-geo-alt"></i> {{ trek.location }} — Current Guide: <span class="text-success">{{ trek.assigned_staff.name || 'None' }}</span></span>
              </div>
              <button @click="processStaffAssignment(trek.trek_id, false)" class="btn btn-sm btn-light text-dark fw-bold rounded-pill px-3 fs-9">
                Assign Here
              </button>
            </div>
          </div>

        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import UserProfile from '../../components/UserProfile.vue'
import { useAlertStore } from '../../stores/alert'
import { useAuthStore } from '../../stores/auth'
import { useConfirmStore } from '@/stores/confirm.js'
import { secureFetch } from '@/utils/api.js'

const alertStore = useAlertStore()
const authStore = useAuthStore()
const confirmStore = useConfirmStore()
const router = useRouter()
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
const staffList = ref([])
const searchQuery = ref('')
const createModalActive = ref(false)
const auditTargetProfile = ref(null)
const assignModalActive = ref(false)
const activeStaffTarget = ref(null)
const availableTreksList = ref([])

// SEARCH ENGINE MATRIX COMPUTATION
const filteredStaff = computed(() => {
  return staffList.value.filter(s => {
    return s.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
           s.specialization.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
           s.certification.toLowerCase().includes(searchQuery.value.toLowerCase())
  })
})

const form = ref({
  name: '', email: '', send_credentials: true , personal_email: ''
})

function openCreateModal() {
  form.value = {
    name: '', email: '', send_credentials: true , personal_email: ''
  }
  createModalActive.value = true
}

async function syncStaffDataset() {
  try {
    const res = await secureFetch(`${BACKEND_URL}/api/admin/staff`, {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      staffList.value = await res.json()
    }
  } catch (err) {
    alertStore.showAlert(`Handshake Drop: ${err.message}`, 'danger')
  }
}

async function submitStaffForm() {
  try {
    const res = await secureFetch(`${BACKEND_URL}/api/admin/staff`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })
    const data = await res.json()
    if (res.ok) {
      alertStore.showAlert(data.message || 'Staff added successfully!', 'success')
      createModalActive.value = false
      await syncStaffDataset()
    } else {
      alertStore.showAlert(data.message || 'Failed to add staff.', 'danger')
    }
  } catch (err) {
    alertStore.showAlert(`Network drop: ${err.message}`, 'danger')
  }
}

async function launchAuditView(id) {
  try {
    const res = await secureFetch(`${BACKEND_URL}/api/admin/staff/${id}`, {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      auditTargetProfile.value = await res.json()
    }
  } catch (err) {
    alertStore.showAlert('Could not read detailed profile parameters.', 'danger')
  }
}

async function openAssignmentWorkflow(member) {
  activeStaffTarget.value = member
  try {
    // Re-use your master endpoint to fetch all present treks arrays mapping context
    const res = await secureFetch(`${BACKEND_URL}/api/admin/treks`, {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      availableTreksList.value = await res.json()
      assignModalActive.value = true
    }
  } catch (err) {
    alertStore.showAlert('Could not read expedition tracks list indices.', 'danger')
  }
}

async function processStaffAssignment(trekId, forceSwitchFlag = false) {
  try {
    const res = await secureFetch(`${BACKEND_URL}/api/admin/assign-staff-override`, {
      method: 'PATCH',
      headers: { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        trek_id: trekId,
        staff_id: activeStaffTarget.value.id,
        force_switch: forceSwitchFlag
      })
    })
    
    const data = await res.json()
    
    if (res.ok) {
      if (data.collision) {
        // CLOSE MODAL PANEL AND TRIGGER GLOBAL CONFIRM CARD POPUP OVERLAY
        assignModalActive.value = false
        confirmStore.ask(
          `Conflict Detected: '${data.trek_name}' is currently assigned to ${data.old_staff_name}. Are you completely sure you want to switch them with ${data.new_staff_name}?`,
          async () => {
            // Re-fire assignment request setting forceSwitchFlag parameter explicitly to true
            await processStaffAssignment(trekId, true)
          }
        )
        return
      }
      
      alertStore.showAlert(data.message || 'Guide re-routing parameters updated inside system tables.', 'success')
      assignModalActive.value = false
      await syncStaffDataset()
    } else {
      alertStore.showAlert(data.message || 'Assignment operation aborted.', 'danger')
    }
  } catch (err) {
    alertStore.showAlert(`Network error: ${err.message}`, 'danger')
  }
}

async function toggleBlacklistState(member) {
  try {
    const res = await secureFetch(`${BACKEND_URL}/api/admin/users/${member.id}/toggle-status`, {
      method: 'PATCH',
      headers: { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      member.blacklisted = !member.blacklisted
      alertStore.showAlert(`Staff status coordinates modified successfully.`, 'success')
      if (auditTargetProfile.value && auditTargetProfile.value.id === member.id) {
        auditTargetProfile.value.blacklisted = member.blacklisted
      }
    }
  } catch (err) {
    alertStore.showAlert('Blacklist toggle transaction drop.', 'danger')
  }
}

async function handleBlacklistAction(id) {
  const match = staffList.value.find(s => s.id === id)
  if (match) await toggleBlacklistState(match)
}

async function handleDeactivateAction(id) {
  try {
    const res = await secureFetch(`${BACKEND_URL}/api/admin/users/${id}/toggle-status`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      alertStore.showAlert('User profile status updated within storage lines.', 'success')
      await syncStaffDataset()
      auditTargetProfile.value = null // Close context
    }
  } catch (err) {
    alertStore.showAlert('Status change rejected.', 'danger')
  }
}

onMounted(() => {
  syncStaffDataset()
})
</script>

<style scoped>
.glass-container { background: rgba(255, 255, 255, 0.05) !important; backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.12) !important; }
.staff-rect-card { background: rgba(255, 255, 255, 0.04) !important; backdrop-filter: blur(15px); }

.rect-avatar-img { width: 56px; height: 56px; border-radius: 12px; object-fit: cover; }
.search-field-capsule { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); }
.clean-field:focus { outline: none; }

/* Modal layer specifications */
.audit-overlay-backdrop { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(1, 4, 2, 0.341); backdrop-filter: blur(10px); z-index: 999; }
.glass-modal-card { background: rgba(2, 16, 9, 0.323) !important; backdrop-filter: blur(15px); width: 100%; max-width: 850px; }
.max-vh-65 { max-height: 65vh; }

.btn-close-modal { position: absolute; top: 0.25rem; right: 0.5rem; background: transparent; border: none; color: rgba(255,255,255,0.5); font-size: 1.3rem; cursor: pointer; }
.btn-close-modal:hover { color: white; }

.status-tag { padding: 4px 12px; border-radius: 20px; font-weight: 600; }
.status-tag.onleave { background: rgba(255, 193, 7, 0.15); color: #ffe066; border: 1px solid rgba(255, 193, 7, 0.3); }
.status-tag.inactive { background: rgba(220, 53, 69, 0.15); color: #ff8787; border: 1px solid rgba(220, 53, 69, 0.25); }

.fs-8 { font-size: 0.88rem; } .fs-9 { font-size: 0.76rem; } .extra-small { font-size: 0.68rem; }

.form-group-capsule { display: flex; flex-direction: column; text-align: left; }
.modal-input-label { font-size: 0.82rem; color: rgba(255, 255, 255, 0.6); font-weight: 500; margin-bottom: 4px; }
.modal-input-wrapper { background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 8px 12px; display: flex; align-items: center; }
.modal-clean-field { border: none; background: transparent; color: #ffffff; width: 100%; font-size: 0.92rem; outline: none; }

</style>