<template>
  <div class="profile-dashboard-wrapper container-fluid px-0 text-white animate-fade-in pb-5">
    
    <div class="row mb-4 align-items-center text-start">
      <div class="col-md-12">
        <h2 class="fw-bold tracking-tight m-0">Account Profile Basecamp</h2>
        <p class="m-0 text-white-50 fs-8 mt-1">Audit profile registries, manage operational tracking data, and cross-reference access logs.</p>
      </div>
    </div>

    <div v-if="userProfile.blacklisted" class="alert alert-danger border border-danger border-opacity-30 rounded-3 p-3 mb-4 text-start bg-danger bg-opacity-10">
      <i class="bi bi-exclamation-triangle text-warning"></i> <strong>Account Flag Restrictions Active:</strong> Your access profile has been blacklisted by administration. Booking submission vectors are currently offline.
    </div>

    <div class="row g-4 text-start mb-4">
      
      <div class="col-lg-4">
        <div class="glass-profile-panel text-center p-4 rounded-4 border border-white border-opacity-10 h-100 shadow-sm">
          
          <div class="avatar-edit-cluster position-relative d-inline-block mx-auto mb-3">
            <img :src="backend_url + userProfile.profile_pic" alt="Avatar User" class="profile-main-avatar shadow border border-white border-opacity-20" />
            <label class="avatar-upload-badge" title="Change Avatar Image">
              <i class="bi bi-pencil" style="font-size: 1rem;"></i>
              <input type="file" accept="image/*" class="d-none" @change="uploadAvatarImage">
            </label>
          </div>

          <h4 class="fw-bold tracking-tight m-0">{{ userProfile.name }}</h4>
          <span class="badge role-indicator-badge mt-1.5 px-3 py-1 rounded-pill small">AUTHORIZED TREKKER</span>
          
          <hr class="my-4 border-white border-opacity-10" />

          <div class="telemetry-logs text-start gap-3 d-flex flex-column fs-8 text-white-50">
            <div class="log-item d-flex justify-content-between">
              <span>Account Status:</span>
              <span class="fw-bold text-success" :class="{ 'text-danger': !userProfile.is_active }">
                ● {{ userProfile.is_active ? 'Active Sync' : 'Offline Restricted' }}
              </span>
            </div>
            <div class="log-item d-flex justify-content-between">
              <span>System ID:</span>
              <span class="fw-bold text-white">#APX-{{ userProfile.id }}</span>
            </div>
            <div class="log-item d-flex justify-content-between">
              <span>Created:</span>
              <span class="fw-bold text-white">{{ userProfile.created_at }}</span>
            </div>
            <div class="log-item d-flex justify-content-between">
              <span>Last Login:</span>
              <span class="fw-bold text-success text-glow">● {{ userProfile.last_login_at }}</span>
            </div>
          </div>

        </div>
      </div>

      <div class="col-lg-8">
        <div class="glass-profile-panel p-4 p-md-5 rounded-4 border border-white border-opacity-10 h-100 shadow-sm d-flex flex-column justify-content-between">
          <div>
            <h5 class="fw-bold mb-4 tracking-tight border-bottom border-white border-opacity-10 pb-2">Profile Core Fields</h5>
            
            <form @submit.prevent="saveProfileFields" class="d-flex flex-column gap-3_5">
              <div class="profile-input-group">
                <label class="input-label-tag">Full Registered Name</label>
                <div class="interactive-input-wrapper">
                  <input v-model="userProfile.name" type="text" class="clean-profile-field w-100" placeholder="Alex Mercer" required>
                </div>
              </div>

              <div class="profile-input-group">
                <label class="input-label-tag">Contact Number Registry</label>
                <div class="interactive-input-wrapper">
                  <input v-model="userProfile.contact" type="tel" class="clean-profile-field w-100" placeholder="+91 XXXXX XXXXX" required>
                </div>
              </div>

              <div class="profile-input-group">
                <label class="input-label-tag opacity-50">Email Reference Coordinate (Immutable Key)</label>
                <div class="interactive-input-wrapper locked-input opacity-60">
                  <input :value="userProfile.email" type="email" class="clean-profile-field w-100" disabled>
                </div>
              </div>

              <div class="mt-4 d-flex align-items-center justify-content-between flex-wrap gap-2">
                <button type="button" @click="triggerPasswordReset" class="btn-security-link text-warning-tint fw-semibold small bg-transparent border-0 p-0">
                  <i class="bi bi-gear"></i> Reset System Security Key (Password)
                </button>
                
                <button type="submit" class="btn-profile-submit rounded-3 px-5 py-2.5 fw-bold text-dark border-0">
                  Patch Profile Coordinates
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

    </div>

    <div class="row mx-0 text-start">
      <div class="col-12 p-0">
        
        <div v-if="!hasStaffData" class="medical-alert-pill p-3 px-4 rounded-pill border border-warning border-opacity-20 d-flex align-items-center justify-content-between shadow-sm">
          <div class="d-flex align-items-center gap-3">
            <span class="fs-4">🚨</span>
            <div>
              <h6 class="m-0 fw-bold text-warning tracking-tight">System Staff Profile Missing</h6>
              <p class="m-0 fs-9 text-white-50 fw-medium opacity-80 mt-0.5">Staff profile information is required to manage your trekking assignments and ensure safety protocols are followed.</p>
            </div>
          </div>
          <button @click="openStaffModal" class="btn btn-warning rounded-pill px-4 py-2 fs-9 fw-bold text-dark shadow-sm">
            Complete Profile
          </button>
        </div>

        <div v-else class="glass-profile-panel p-4 p-md-5 rounded-4 border border-white border-opacity-10 shadow-sm animate-scale-up">
          <div class="d-flex align-items-center justify-content-between border-bottom border-white border-opacity-10 pb-2 mb-4">
            <h5 class="fw-bold tracking-tight m-0"><i class="bi bi-hospital mx-2" style="font-size:1rem;"></i> Staff Specific Details</h5>
            <div class="d-flex align-items-center gap-3 fs-9 text-white-50">
              <!-- <span>Last Updated : {{ staffProfile.updated_at }}</span> -->
               <span>Status : {{ staffProfile.status }}</span>
              <button @click="openStaffModal" class="btn btn-outline-light btn-xs rounded-pill px-3 py-1 fs-9 border-opacity-25">
                Modify Metrics
              </button>
            </div>
          </div>

          <div class="row g-4 fs-8">
            <div class="col-md-3">
              <span class="d-block text-white-50 small mb-1">EXPERIENCE (YEARS)</span>
              <strong class="fs-5 text-success text-glow">{{ staffProfile.experience_years }}</strong>
            </div>
            <div class="col-md-9">
              <span class="d-block text-white-50 small mb-1">CERTIFICATIONS</span>
              <p class="m-0 fw-medium text-white">{{ staffProfile.certifications || 'None declared.' }}</p>
            </div>
            <div class="col-md-6">
            <span class="d-block text-white-50 small mb-1">SPECIALIZATION</span>
              <p class="m-0 fw-medium text-white">{{ staffProfile.specialization || 'None declared.' }}</p>
            </div>
            <div class="col-md-6">
              <span class="d-block text-white-50 small mb-1">EMERGENCY CONTACT</span>
              <p class="m-0 fw-medium text-white">
                <strong>{{ staffProfile.emergency_contact}}</strong> 
              </p>
            </div>
            <div class="col-md-12">
              <span class="d-block text-white-50 small mb-1">ABOUT</span>
              <p class="m-0 fw-medium text-white">{{ staffProfile.bio || ' No information available.' }}</p>
            </div>
          </div>
        </div>

      </div>
    </div>

    <Transition name="modal-fade">
      <div v-if="staffModalVisible" class="staff-overlay-backdrop d-flex align-items-center justify-content-center">
        <div class="glass-modal-card p-4 p-md-5 rounded-4 border border-white border-opacity-15 shadow-lg text-start animate-scale-up">
          
          <h4 class="fw-bold tracking-tight text-white m-0 mb-1">Staff Profile Matrix</h4>
          <p class="text-white-50 small m-0 mb-4 lh-base">Configure critical emergency contact profiles and trail safety parameters.</p>

          <form @submit.prevent="submitStaffForm" class="d-flex flex-column gap-3_5">
              <div class="row g-3">
            <div class="col-6">
                <div class="profile-input-group">
                    <label class="input-label-tag">Experience (Years)</label>
                    <div class="interactive-input-wrapper">
                        <input v-model="staffFormFields.experience_years" type="number" class="clean-profile-field w-100" placeholder="2+ (Round number)" required>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="profile-input-group">
                <label class="input-label-tag">Status</label>
                <div class="interactive-input-wrapper">
                    <select v-model="staffFormFields.status" class="clean-profile-field bg-transparent" required>
                        <option value="" disabled hidden >Activity</option>
                        <option value="Active" >Active</option>
                        <option value="Inactive">Inactive</option>
                        <option value="On Leave">On Leave</option>
                    </select>
                </div>
                </div>
            </div>
              <div class="col-12">
                <div class="profile-input-group">
                  <label class="input-label-tag">Specialization</label>
                  <div class="interactive-input-wrapper py-2">
                    <textarea v-model="staffFormFields.specialization" rows="2" class="clean-profile-field w-100 style-textarea" placeholder="Mountain Climbing, Trail Running, ..."></textarea>
                  </div>
                </div>
              </div>
              <div class="col-12">
                <div class="profile-input-group">
                  <label class="input-label-tag">Certifications</label>
                  <div class="interactive-input-wrapper py-2">
                    <textarea v-model="staffFormFields.certifications" rows="2" class="clean-profile-field w-100 style-textarea" placeholder="NIMC, First Aid, ..."></textarea>
                  </div>
                </div>
              </div>
              <div class="col-12">
                <div class="profile-input-group">
                  <label class="input-label-tag">About</label>
                  <div class="interactive-input-wrapper py-2">
                    <textarea v-model="staffFormFields.bio" rows="2" class="clean-profile-field w-100 style-textarea" placeholder="About yourself"></textarea>
                  </div>
                </div>
              </div>
              <div class="col-md-12">
                <div class="profile-input-group">
                  <label class="input-label-tag">Emergency Contact </label>
                  <div class="interactive-input-wrapper">
                    <input v-model="staffFormFields.emergency_contact" type="tel" class="clean-profile-field w-100" placeholder="10-digit number" required>
                  </div>
                </div>
              </div>
            </div>

            <div class="mt-4 d-flex align-items-center justify-content-end gap-3">
              <button type="button" @click="staffModalVisible = false" class="btn btn-outline-light rounded-pill px-4 py-2 fs-8">
                Aborted
              </button>
              <button type="submit" class="btn btn-success rounded-pill px-4 py-2 fs-8 fw-semibold text-dark">
                Submit File Coordinates
              </button>
            </div>
          </form>

        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAlertStore } from '../../stores/alert'
import { useAuthStore } from '../../stores/auth'

const alertStore = useAlertStore()
const authStore = useAuthStore()
const backend_url = import.meta.env.VITE_BACKEND_URL

const API_BASE = 'http://127.0.0.1:5000/api/trek_staff'

// Structural layout reactive visibility boundaries variables
const hasStaffData = ref(false)
const staffModalVisible = ref(false)

// Synchronized state containers matching backend model configurations
const userProfile = ref({
  id: '',
  name: '',
  email: '',
  contact: '',
  is_active: true,
  created_at: '',
  last_login_at: '',
  profile_pic: '',
  blacklisted: false
})

const staffProfile = ref({
    specialization: '',
    experience_years: '',
    certifications: '',
    status:'',
    emergency_contact:'',
    bio:''
})

const staffFormFields = ref({
    specialization: '',
    experience_years: '',
    certifications: '',
    status:'Active',
    emergency_contact:'',
    bio:''
})

// ==========================================================================
// 3. NETWORK DATA ORCHESTRATION PIPELINES (Fetch Engine)
// ==========================================================================
async function fetchProfileAndStaffData() {
  try {
    const headers = {
      'Authorization': `Bearer ${authStore.token}`,
      'Content-Type': 'application/json'
    }

    // 1. Dispatch Core User Profile Retrieval Request
    const profileRes = await fetch(`${API_BASE}/profile`, { method: 'GET', headers })
    if (profileRes.ok) {
      const pData = await profileRes.json()// Debug log for profile data
      userProfile.value = pData
    } else {
      const errorData = await profileRes.json();
      alertStore.showAlert(errorData.message || 'Could not sync user profile metrics from backend.', 'danger')
    }

    // 2. Dispatch Adaptive Staff Profile Retrieval Request
    const staffRes = await fetch(`${API_BASE}/staff`, { method: 'GET', headers })
    if (staffRes.ok) {
      const sData = await staffRes.json()
      if (sData.has_data) {
        hasStaffData.value = true
        staffProfile.value = sData
      } else {
        hasStaffData.value = false
      }
    }
  } catch (err) {
    alertStore.showAlert(`Network tracking error: ${err.message}`, 'danger')
  }
}

async function saveProfileFields() {
  // Input structural constraints checkpoints
  const namePattern = /^[a-zA-Z\s]+$/
  if (!namePattern.test(userProfile.value.name)) {
    alertStore.showAlert('Validation Error: Name fields must contain alpha values only.', 'danger')
    return
  }
  if (userProfile.value.contact.length !== 10 || !/^\d+$/.test(userProfile.value.contact)) {
    alertStore.showAlert('Validation Error: Contact field requires exactly 10 digits.', 'danger')
    return
  }

  try {
    const res = await fetch(`${API_BASE}/profile`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: userProfile.value.name,
        contact: userProfile.value.contact
      })
    })

    const data = await res.json()
    if (res.ok) {
      alertStore.showAlert(data.message || 'Profile patches committed successfully.', 'success')
      // Sync local Pinia global user naming registry coordinate values
      if (authStore.userName) {
        authStore.userName = userProfile.value.name
        sessionStorage.setItem('user_name', userProfile.value.name)
      }
    } else {
      alertStore.showAlert(data.message || 'Profile updates rejected.', 'danger')
    }
  } catch (err) {
    alertStore.showAlert(`Network transaction error: ${err.message}`, 'danger')
  }
}

async function submitStaffForm() {
  if (staffFormFields.value.emergency_contact.length !== 10 || !/^\d+$/.test(staffFormFields.value.emergency_contact)) {
    alertStore.showAlert('Validation Error: Emergency contact requires exactly 10 digits.', 'danger')
    return
  }

  try {
    const res = await fetch(`${API_BASE}/staff`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(staffFormFields.value)
    })

    const data = await res.json()
    if (res.ok) {
      alertStore.showAlert(data.message || 'Staff profile updated successfully.', 'success')
      staffModalVisible.value = false
      await fetchProfileAndStaffData() // Trigger a clean network re-fetch to draw the populated card view
    } else {
      alertStore.showAlert(data.message || 'Staff tracking payload rejected.', 'danger')
    }
  } catch (err) {
    alertStore.showAlert(`Network transaction error: ${err.message}`, 'danger')
  }
}

function openStaffModal() {

  if (hasStaffData.value) {
    // If they have real data, deep copy it into the form input proxies
    staffFormFields.value = { ...staffProfile.value }
  } else {
    // If it's still 'Pending' (or completely missing), initialize empty values 
    // instead of letting 'Pending' populate your text fields.
    staffFormFields.value = {
      specialization: '',
      experience_years: '', // Empty input allows placeholder to render cleanly
      certifications: '',
      status: 'Active',
      emergency_contact: '',
      bio: ''
    }
  }
  staffModalVisible.value = true
}

function triggerPasswordReset() {
  alertStore.showAlert('Security Key Protocol: OTP deployment queue initialized via Celery channels.', 'warning')
}

async function uploadAvatarImage(event) {
  const file = event.target.files[0]
  if (!file) return

  // ===================================================================
  // SECURE FRONTEND 1MB CAPACITY CONSTRAINT VALIDATION (Matches Register)
  // ===================================================================
  const MAX_SIZE = 1 * 1024 * 1024 // Exactly 1 Megabyte in bytes
  if (file.size > MAX_SIZE) {
    alertStore.showAlert('Avatar upload bounds exceeded! Maximum limit is exactly 1MB.', 'danger')
    event.target.value = '' // Flush the input buffer cache channel element
    return
  }

  // Construct a multipart FormData payload context layer
  const formData = new FormData()
  formData.append('profile_pic', file)

  try {
    alertStore.showAlert('Syncing new profile picture coordinates...', 'info')
    
    const res = await fetch(`${API_BASE}/profile`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      },
      body: formData
    })

    const data = await res.json()
    
    if (res.ok) {
      alertStore.showAlert('Avatar image updated successfully!', 'success')
      
      // Update local state reactively so the changes display immediately on screen
      userProfile.value.profile_pic = data.user.profile_pic
      authStore.updateLocalAvatar(data.user.profile_pic) 
      
      // Update parent fallback links if necessary
      await fetchProfileAndMedicalData() 
    } else {
      alertStore.showAlert(data.message || 'Avatar update rejected by backend matrix.', 'danger')
    }
  } catch (err) {
    console.error('File sync handshake broken:', err)
    alertStore.showAlert(`Upload connection drops detected: ${err.message}`, 'danger')
  } finally {
    event.target.value = '' 
  }
}

// Global Lifecycle Mounting Gate Execution Node
onMounted(() => {
  fetchProfileAndStaffData()
})
</script>

<style scoped>
.glass-profile-panel {
  background: rgba(255, 255, 255, 0.05) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
}

.profile-main-avatar { width: 110px; height: 110px; border-radius: 50%; object-fit: cover; }
.avatar-upload-badge {
  position: absolute; bottom: 0; right: 4px; background: #ffffff; color: #111;
  width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
  font-size: 0.8rem; cursor: pointer;
}
.role-indicator-badge { background: rgba(25, 135, 84, 0.15); color: #7bf1a8; border: 1px solid rgba(25, 135, 84, 0.3); }

/* Form Input Configurations */
.input-label-tag { font-size: 0.8rem; color: rgba(255, 255, 255, 0.5); font-weight: 500; margin-bottom: 5px; }
.interactive-input-wrapper {
  background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 10px; padding: 10px 14px; display: flex; align-items: center;
}
.clean-profile-field { border: none; background: transparent; color: #ffffff; outline: none; font-size: 0.95rem; }
.style-textarea { resize: none; line-height: 1.5; }

.btn-profile-submit { background-color: #ffffff; cursor: pointer; font-weight: 600; font-size: 0.88rem; }
.btn-security-link { color: #ffc107; font-size: 0.85rem; text-decoration: none; cursor: pointer; opacity: 0.85; transition: opacity 0.2s; }
.btn-security-link:hover { opacity: 1; text-decoration: underline; }

/* ==========================================================================
   ADAPTIVE MEDICAL ROW & IMMERSIVE POPUP MODAL STYLES
   ========================================================================== */
.medical-alert-pill {
  background: rgba(255, 193, 7, 0.05) !important;
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 193, 7, 0.18) !important;
}

.staff-overlay-backdrop {
  position: fixed !important; top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(0, 5, 2, 0.316) !important;
  backdrop-filter: blur(7px) !important; -webkit-backdrop-filter: blur(20px) !important;
  z-index: 999 !important;
}

.glass-modal-card {
  background: rgba(0, 0, 0, 0.206) !important;
  backdrop-filter: blur(6px);
  width: 92%; max-width: 580px;
}

.select-fix option { background: #16241c; color: white; }

/* Modal Animations hooks */
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.3s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }

.text-glow { text-shadow: 0 0 10px rgba(25, 135, 84, 0.4); }
.text-warning-tint { color: #ffe066; }
.gap-3_5 { gap: 14px; }
.fs-8 { font-size: 0.88rem; }
.fs-9 { font-size: 0.76rem; }
</style>