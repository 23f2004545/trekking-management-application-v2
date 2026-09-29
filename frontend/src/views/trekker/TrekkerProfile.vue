<template>
  <div class="profile-dashboard-wrapper container-fluid text-white animate-fade-in pb-5" style="z-index: 99;">
    
    <div class="d-flex align-items-center justify-content-between mb-1 flex-wrap ">
        <div class="mb-4">
            <h2 class="fw-bold tracking-tight m-0">Account Profile Basecamp</h2>
            <p class="m-0 text-white-50 fs-8 mt-1">Audit profile registries, manage operational tracking data, and cross-reference access logs.</p>
        </div>
          <button @click="confirmStore.ask('Are you sure you want to delete your account permanently?', deleteAccount)" class="btn btn-outline-danger rounded-pill px-4 py-2 fs-8 shadow-sm mb-2">
             Delete Account
          </button>
    </div>

    <div v-if="userProfile.blacklisted" class="alert alert-warning border border-danger border-opacity-30 rounded-3 p-3 mb-4 text-start bg-danger bg-opacity-10">
      <i class="bi bi-exclamation-triangle text-warning"></i> <strong>Blacklisted :</strong> Your access profile has been blacklisted by administration. Booking submission vectors are currently offline.
    </div>

    <div class="row g-4 text-start mb-4">
      
      <div class="col-lg-4">
        <div class="glass-profile-panel text-center p-4 rounded-4 border border-white border-opacity-10 h-100 shadow-sm">
          
          <div class="avatar-edit-cluster position-relative d-inline-block mx-auto mb-3">
            <img :src="resolveMediaUrl(userProfile.profile_pic)" alt="Avatar User" class="profile-main-avatar shadow border border-white border-opacity-20" />
            <label class="avatar-upload-badge" title="Change Avatar Image">
              <i class="bi bi-pencil" style="font-size: 1rem;"></i>
              <input type="file" accept="image/*" class="d-none" @change="uploadAvatarImage">
            </label>
          </div>

          <h4 class="fw-bold tracking-tight m-0">{{ userProfile.name }}</h4>
          <span class="badge role-indicator-badge mt-2 px-3 py-1 rounded-pill small">AUTHORIZED TREKKER</span>
          
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
                
                <button type="submit" class="btn-profile-submit rounded-5 px-5 py-1 fw-bold text-dark border-0">
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
        
        <div v-if="!hasMedicalData" class="medical-alert-pill p-3 px-4 rounded-pill border border-warning border-opacity-20 d-flex align-items-center justify-content-between shadow-sm">
          <div class="d-flex align-items-center gap-3">

            <div>
              <h6 class="m-0 fw-bold text-warning tracking-tight mb-1">System Medical Emergency Profile Missing</h6>
              <p class="m-0 fs-9 text-white-50 fw-medium opacity-80 mt-0.5">Emergency coordinates are mandatory to secure active booking slots on the high trail. Please update your telemetry layout.</p>
            </div>
          </div>
          <button @click="openMedicalModal" class="btn btn-warning rounded-pill px-2 py-1 fs-9 fw-bold text-dark shadow-sm">
            Complete Registry
          </button>
        </div>

        <div v-else class="glass-profile-panel p-4 p-md-5 rounded-4 border border-white border-opacity-10 shadow-sm animate-scale-up">
          <div class="d-flex align-items-center justify-content-between border-bottom border-white border-opacity-10 pb-2 mb-4 flex-wrap">
            <h5 class="fw-bold tracking-tight m-0"><i class="bi bi-hospital mx-2 mb-3" style="font-size:1rem;"></i> Medical Diagnostics</h5>
            <div class="d-flex flex-wrap flex-md-row align-items-center gap-2 fs-9 text-white-50">
              <span>Last Updated : {{ medicalProfile.updated_at }}</span>
              <button @click="openMedicalModal" class="btn btn-outline-light btn-xs rounded-pill px-3 py-1 fs-9 border-opacity-25">
                Modify Metrics
              </button>
            </div>
          </div>

          <div class="row g-4 fs-8">
            <div class="col-md-3">
              <span class="d-block text-white-50 small mb-1">BLOOD GROUP</span>
              <strong class="fs-5 text-success text-glow">{{ medicalProfile.blood_group }}</strong>
            </div>
            <div class="col-md-9">
              <span class="d-block text-white-50 small mb-1">CHRONIC DIAGNOSTICS</span>
              <p class="m-0 fw-medium text-white">{{ medicalProfile.diagnosis || 'None declared.' }}</p>
            </div>
            <div class="col-md-6">
              <span class="d-block text-white-50 small mb-1">ALLERGIES & MEDICAL RESTRICTIONS</span>
              <p class="m-0 fw-medium text-white">{{ medicalProfile.allergies || 'No environmental constraints flagged.' }}</p>
            </div>
            <div class="col-md-6">
              <span class="d-block text-white-50 small mb-1">EMERGENCY RESPONSE CONTACTS</span>
              <p class="m-0 fw-medium text-white">
                <strong>{{ medicalProfile.emergency_name }}</strong> ({{ medicalProfile.emergency_relation }}) — <span class="text-success">{{ medicalProfile.emergency_phone }}</span>
              </p>
            </div>
          </div>
        </div>

      </div>
    </div>

    <Transition name="modal-fade">
      <div v-if="medicalModalVisible" @click.self="medicalModalVisible = false" class="medical-overlay-backdrop d-flex align-items-center justify-content-center p-3">
        <div class="glass-modal-card p-4 p-md-5 rounded-4 border border-white border-opacity-15 overflow-y-auto shadow-lg text-start max-vh-70 animate-scale-up">
          
          <div class="d-flex align-items-center justify-content-between border-bottom flex-wrap border-white border-opacity-50 pb-2 mb-4">
            <button @click="medicalModalVisible = false" class="btn-close-modal" title="Close Panel">✕</button>
            <h4 class="fw-bold tracking-tight text-white m-0 mb-1">Field Medical Matrix</h4>
            <p class="text-white-50 small m-0 mb-4 lh-base extra-small">Configure critical emergency contact profiles and trail safety parameters parameters.</p>
          </div>

          <form @submit.prevent="submitMedicalForm" class="d-flex flex-column gap-3_5">
            <div class="row g-3">
              <div class="col-6">
                <div class="profile-input-group">
                  <label class="input-label-tag">Blood Group</label>
                  <div class="interactive-input-wrapper">
                    <input v-model="medicalFormFields.blood_group" type="text" class="clean-profile-field w-100" placeholder="O+" required>
                  </div>
                </div>
              </div>
              <div class="col-12">
                <div class="profile-input-group">
                  <label class="input-label-tag">Chronic Diagnosis</label>
                  <div class="interactive-input-wrapper py-2">
                    <textarea v-model="medicalFormFields.diagnosis" rows="2" class="clean-profile-field w-100 style-textarea" placeholder="Asthma, Diabetes, or None..."></textarea>
                  </div>
                </div>
              </div>
              <div class="col-12">
                <div class="profile-input-group">
                  <label class="input-label-tag">Allergies & Trail Restrictions</label>
                  <div class="interactive-input-wrapper py-2">
                    <textarea v-model="medicalFormFields.allergies" rows="2" class="clean-profile-field w-100 style-textarea" placeholder="List food, drug, or sting allergies..."></textarea>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="profile-input-group">
                  <label class="input-label-tag">Emergency Contact Name</label>
                  <div class="interactive-input-wrapper">
                    <input v-model="medicalFormFields.emergency_name" type="text" class="clean-profile-field w-100" placeholder="Sarah Connor" required>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="profile-input-group">
                  <label class="input-label-tag">Emergency Contact Phone</label>
                  <div class="interactive-input-wrapper">
                    <input v-model="medicalFormFields.emergency_phone" type="tel" class="clean-profile-field w-100" placeholder="10-digit number" required>
                  </div>
                </div>
              </div>
              <div class="col-12">
                <div class="profile-input-group">
                  <label class="input-label-tag">Relationship to Explorer</label>
                  <div class="interactive-input-wrapper">
                    <input v-model="medicalFormFields.emergency_relation" type="text" class="clean-profile-field w-100" placeholder="Spouse, Parent, Guardian" required>
                  </div>
                </div>
              </div>
            </div>

            <div class="mt-4 d-flex align-items-center justify-content-end gap-3">
              <button type="button" @click="medicalModalVisible = false" class="btn btn-outline-light rounded-pill px-4 py-2 fs-8">
                Abort
              </button>
              <button type="submit" class="btn btn-success rounded-pill px-4 py-2 fs-8 fw-semibold text-dark">
                Submit 
              </button>
            </div>
          </form>

        </div>
      </div>
    </Transition>

    <Transition name="modal-fade">
      <div v-if="passwordModalActive" @click.self="passwordModalActive = false" class="profile-overlay-backdrop d-flex align-items-center justify-content-center p-3">
        <div class="glass-profile-card p-4 p-md-5 rounded-4 border border-white border-opacity-15 shadow-lg text-start animate-scale-up position-relative" style="max-width: 450px; width: 100%;">
          
          <button @click="passwordModalActive = false" class="btn-close-modal" title="Close Panel">✕</button>

          <h4 class="fw-bold tracking-tight text-white mb-1">Update Security Key</h4>
          <p class="text-white-50 small mb-4">Request a 6-digit authorization code to your registered email to process this mutation.</p>

          <form @submit.prevent="submitPasswordChange" class="d-flex flex-column gap-3">
            
            <div class="profile-input-group">
              <label class="input-label-tag">New Security Key (Password)</label>
              <div class="interactive-input-wrapper">
                <input v-model="securityForm.newPassword" type="password" required class="clean-profile-field w-100" placeholder="••••••••">
              </div>
            </div>

            <div class="profile-input-group">
              <label class="input-label-tag">Confirm Security Key</label>
              <div class="interactive-input-wrapper">
                <input v-model="securityForm.confirmPassword" type="password" required class="clean-profile-field w-100" placeholder="••••••••">
              </div>
            </div>

            <hr class="border-white border-opacity-10 my-1" />

            <div class="profile-input-group">
              <div class="d-flex justify-content-between align-items-end mb-1">
                <label class="input-label-tag m-0">Authorization Code (OTP)</label>
                <button type="button" @click="requestOTP" :disabled="otpCooldown > 0" class="btn btn-sm btn-outline-warning rounded-pill px-3 py-1 fs-9 border-opacity-50 mb-2">
                  {{ otpCooldown > 0 ? `Resend in ${otpCooldown}s` : 'Send OTP ' }}
                </button>
              </div>
              <div class="interactive-input-wrapper">
                <input v-model="securityForm.otpCode" type="text" required class="clean-profile-field w-100 fw-bold tracking-widest text-warning" placeholder="000000" maxlength="6">
              </div>
            </div>

            <div class="mt-4">
              <button type="submit" class="btn btn-warning w-100 rounded-pill py-2.5 fw-bold text-dark fs-8 shadow-sm">
                Authorize Password Mutation
              </button>
            </div>

          </form>
        </div>
      </div>
    </Transition>

    <!-- Interactive Demo Email Delivery Modal -->
    <DemoEmailPromptModal 
      :isOpen="showEmailModal"
      title="Security Key OTP Email Delivery"
      description="Experience Celery background workers and real cloud SMTP delivery by receiving password reset OTP in your inbox."
      @close="showEmailModal = false"
      @submit="handleLiveOtpSubmit"
      @simulate="handleSimulateOtpSubmit"
    />

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAlertStore } from '../../stores/alert'
import { useAuthStore } from '../../stores/auth'
import { secureFetch, BACKEND_URL } from '@/utils/api'
import { useConfirmStore } from '../../stores/confirm'
import { resolveMediaUrl } from '@/utils/media'
import DemoEmailPromptModal from '@/components/DemoEmailPromptModal.vue'

const alertStore = useAlertStore()
const router = useRouter()
const authStore = useAuthStore()
const backend_url = BACKEND_URL
const confirmStore = useConfirmStore()
const showEmailModal = ref(false)

const API_BASE = `${BACKEND_URL}/api/trekker`

// Structural layout reactive visibility boundaries variables
const hasMedicalData = ref(false)
const medicalModalVisible = ref(false)

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

const medicalProfile = ref({
  blood_group: '',
  diagnosis: '',
  allergies: '',
  medications: '',
  emergency_name: '',
  emergency_phone: '',
  emergency_relation: '',
  updated_at: ''
})

const medicalFormFields = ref({
  blood_group: '',
  diagnosis: '',
  allergies: '',
  medications: '',
  emergency_name: '',
  emergency_phone: '',
  emergency_relation: ''
})

const passwordModalActive = ref(false)
const otpCooldown = ref(0)
const securityForm = ref({
  newPassword: '',
  confirmPassword: '',
  otpCode: ''
})

// ==========================================================================
//  NETWORK DATA ORCHESTRATION PIPELINES (Fetch Engine)
// ==========================================================================
async function fetchProfileAndMedicalData() {
  try {
    const headers = {
      'Authorization': `Bearer ${authStore.token}`,
      'Content-Type': 'application/json'
    }

    // 1. Dispatch Core User Profile Retrieval Request
    const profileRes = await secureFetch(`${API_BASE}/profile`, { method: 'GET', headers })
    if (profileRes.ok) {
      const pData = await profileRes.json()// Debug log for profile data
      userProfile.value = pData
    } else {
      const errorData = await profileRes.json();
      alertStore.showAlert(errorData.message || 'Could not sync user profile metrics from backend.', 'danger')
    }

    // 2. Dispatch Adaptive Medical Telemetry Record Retrieval Request
    const medicalRes = await secureFetch(`${API_BASE}/medical`, { method: 'GET', headers })
    if (medicalRes.ok) {
      const mData = await medicalRes.json()
      if (mData.has_data) {
        hasMedicalData.value = true
        medicalProfile.value = mData
      } else {
        hasMedicalData.value = false
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
    const res = await secureFetch(`${API_BASE}/profile`, {
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

async function submitMedicalForm() {
  if (medicalFormFields.value.emergency_phone.length !== 10 || !/^\d+$/.test(medicalFormFields.value.emergency_phone)) {
    alertStore.showAlert('Validation Error: Emergency contact phone requires exactly 10 digits.', 'danger')
    return
  }

  try {
    const res = await secureFetch(`${API_BASE}/medical`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(medicalFormFields.value)
    })

    const data = await res.json()
    if (res.ok) {
      alertStore.showAlert(data.message || 'Medical profile updated successfully.', 'success')
      medicalModalVisible.value = false
      await fetchProfileAndMedicalData() // Trigger a clean network re-fetch to draw the populated card view
    } else {
      alertStore.showAlert(data.message || 'Medical tracking payload rejected.', 'danger')
    }
  } catch (err) {
    alertStore.showAlert(`Network transaction error: ${err.message}`, 'danger')
  }
}

function openMedicalModal() {
  // Deep copy the active values into input proxies so cancel operations keep historical metrics safe
  medicalFormFields.value = hasMedicalData.value ? { ...medicalProfile.value } : {
    blood_group: '', diagnosis: '', allergies: '', medications: '', emergency_name: '', emergency_phone: '', emergency_relation: ''
  }
  medicalModalVisible.value = true
}

function triggerPasswordReset() {
  securityForm.value = { newPassword: '', confirmPassword: '', otpCode: '' }
  passwordModalActive.value = true
}

function requestOTP() {
  if (authStore.isDemo) {
    showEmailModal.value = true
    return
  }
  executeRequestOTP(null)
}

function handleLiveOtpSubmit(email) {
  showEmailModal.value = false
  executeRequestOTP(email)
}

function handleSimulateOtpSubmit() {
  showEmailModal.value = false
  executeRequestOTP(null)
}

// Logic to ask Flask for OTP and start UI cooldown
async function executeRequestOTP(demoDeliveryEmail = null) {
  try {
    alertStore.showAlert('Dispatching authorization request to Celery workers...', 'info')
    const payload = {}
    if (demoDeliveryEmail) {
      payload.demo_delivery_email = demoDeliveryEmail
    }
    const res = await secureFetch(`${API_BASE}/request-password-otp`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })
    
    if (res.ok) {
      alertStore.showAlert('OTP dispatched! Please check your communication logs.', 'success')
      // Start 60 second cooldown to prevent spamming the email server
      otpCooldown.value = 60
      const timer = setInterval(() => {
        otpCooldown.value--
        if (otpCooldown.value <= 0) clearInterval(timer)
      }, 1000)
    } else {
      alertStore.showAlert('Failed to generate OTP.', 'danger')
    }
  } catch (err) {
    alertStore.showAlert(`Network drop: ${err.message}`, 'danger')
  }
}

// Logic to submit the final change
async function submitPasswordChange() {
  if (securityForm.value.newPassword !== securityForm.value.confirmPassword) {
    alertStore.showAlert('Security keys do not match. Please verify your inputs.', 'danger')
    return
  }
  
  try {
    const res = await secureFetch(`${API_BASE}/reset-password`, {
      method: 'PATCH',
      headers: { 
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json' 
      },
      body: JSON.stringify({
        otp: securityForm.value.otpCode,
        new_password: securityForm.value.newPassword
      })
    })
    
    const data = await res.json()
    if (res.ok) {
      alertStore.showAlert('Success: Account security key has been mutated.', 'success')
      passwordModalActive.value = false
    } else {
      alertStore.showAlert(data.message || 'Authorization rejected.', 'danger')
    }
  } catch (err) {
    alertStore.showAlert(`Network drop: ${err.message}`, 'danger')
  }
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
    
    const res = await secureFetch(`${API_BASE}/profile`, {
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

async function deleteAccount(id) {
  try {
    const res = await secureFetch(`${API_BASE}/profile`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${authStore.token}`, 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      authStore.logoutUser() 
      router.push('/')
    }
  } catch (err) {
    alertStore.showAlert('Failed to delete account', 'danger')
  }
}

// Global Lifecycle Mounting Gate Execution Node
onMounted(() => {
  fetchProfileAndMedicalData()
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

.medical-overlay-backdrop {
  position: fixed !important; top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(0, 5, 2, 0.316) !important;
  backdrop-filter: blur(12px) !important; -webkit-backdrop-filter: blur(20px) !important;
  z-index: 999 !important;
}

.glass-modal-card {
  background: rgba(0, 0, 0, 0.206) !important;
  backdrop-filter: blur(6px);
  width: 92%; max-width: 580px;
}

/* Modal Animations hooks */
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.3s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }

.text-glow { text-shadow: 0 0 10px rgba(25, 135, 84, 0.4); }
.text-warning-tint { color: #ffe066; }
.gap-3_5 { gap: 14px; }
.fs-8 { font-size: 0.88rem; }
.fs-9 { font-size: 0.76rem; }
.max-vh-70 { max-height: 70vh; }
.extra-small { font-size: 0.68rem; }

/* OTP Modal Specific Styles */
.profile-overlay-backdrop { position: fixed !important; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0, 6, 2, 0.459); backdrop-filter: blur(5px); z-index: 999; }
.glass-profile-card { background: rgba(1, 1, 1, 0.383) !important; backdrop-filter: blur(10px); }
.btn-close-modal { position: absolute; top: 20px; right: 20px; background: transparent; border: none; color: rgba(255,255,255,0.5); font-size: 1.2rem; cursor: pointer; }
.btn-close-modal:hover { color: white; }
.tracking-widest { letter-spacing: 4px; }
</style>