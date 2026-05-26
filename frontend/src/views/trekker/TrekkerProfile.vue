<template>
  <div class="profile-dashboard-wrapper container-fluid px-0 text-white animate-fade-in pb-5">
    
    <div class="row mb-4 align-items-center text-start">
      <div class="col-md-12">
        <h2 class="fw-bold tracking-tight m-0">Account Profile Basecamp</h2>
        <p class="m-0 text-white-50 fs-8 mt-1">Audit profile registries, manage operational tracking data, and cross-reference access logs.</p>
      </div>
    </div>

    <div v-if="userProfile.blacklisted" class="alert alert-danger border border-danger border-opacity-30 rounded-3 p-3 mb-4 text-start bg-danger bg-opacity-10">
      ⚠️ <strong>Account Flag Restrictions Active:</strong> Your access profile has been blacklisted by administration. Booking submission vectors are currently offline.
    </div>

    <div class="row g-4 text-start mb-4">
      
      <div class="col-lg-4">
        <div class="glass-profile-panel text-center p-4 rounded-4 border border-white border-opacity-10 h-100 shadow-sm">
          
          <div class="avatar-edit-cluster position-relative d-inline-block mx-auto mb-3">
            <img :src="userProfile.profile_pic" alt="Avatar User" class="profile-main-avatar shadow border border-white border-opacity-20" />
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
              <span>System ID Code:</span>
              <span class="fw-bold text-white">#APX-{{ userProfile.id }}</span>
            </div>
            <div class="log-item d-flex justify-content-between">
              <span>Created Coordinates:</span>
              <span class="fw-bold text-white">{{ userProfile.created_at }}</span>
            </div>
            <div class="log-item d-flex justify-content-between">
              <span>Last Network Entry:</span>
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
                  ⚙️ Reset System Security Key (Password)
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
        
        <div v-if="!hasMedicalData" class="medical-alert-pill p-3 px-4 rounded-pill border border-warning border-opacity-20 d-flex align-items-center justify-content-between shadow-sm">
          <div class="d-flex align-items-center gap-3">
            <span class="fs-4">🚨</span>
            <div>
              <h6 class="m-0 fw-bold text-warning tracking-tight">System Medical Emergency Profile Missing</h6>
              <p class="m-0 fs-9 text-white-50 fw-medium opacity-80 mt-0.5">Emergency coordinates are mandatory to secure active booking slots on the high trail. Please update your telemetry layout.</p>
            </div>
          </div>
          <button @click="openMedicalModal" class="btn btn-warning rounded-pill px-4 py-2 fs-9 fw-bold text-dark shadow-sm">
            Complete Registry
          </button>
        </div>

        <div v-else class="glass-profile-panel p-4 p-md-5 rounded-4 border border-white border-opacity-10 shadow-sm animate-scale-up">
          <div class="d-flex align-items-center justify-content-between border-bottom border-white border-opacity-10 pb-2 mb-4">
            <h5 class="fw-bold tracking-tight m-0"><i class="bi bi-hospital mx-2" style="font-size:1rem;"></i> Medical Diagnostics & Field Safeguards</h5>
            <div class="d-flex align-items-center gap-3 fs-9 text-white-50">
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
              <p class="m-0 fw-medium text-white">{{ medicalProfile.diagonisis || 'None declared.' }}</p>
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
      <div v-if="medicalModalVisible" class="medical-overlay-backdrop d-flex align-items-center justify-content-center">
        <div class="glass-modal-card p-4 p-md-5 rounded-4 border border-white border-opacity-15 shadow-lg text-start animate-scale-up">
          
          <h4 class="fw-bold tracking-tight text-white m-0 mb-1">Field Medical Matrix</h4>
          <p class="text-white-50 small m-0 mb-4 lh-base">Configure critical emergency contact profiles and trail safety parameters parameters.</p>

          <form @submit.prevent="submitMedicalForm" class="d-flex flex-column gap-3_5">
            <div class="row g-3">
              <div class="col-4">
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
                    <textarea v-model="medicalFormFields.diagonisis" rows="2" class="clean-profile-field w-100 style-textarea" placeholder="Asthma, Diabetes, or None..."></textarea>
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
import { ref } from 'vue'
import { useAlertStore } from '../../stores/alert'

const alertStore = useAlertStore()

// State parameters managing profile fields configurations
const hasMedicalData = ref(false) // Toggle to TRUE locally to view the read-only dashboard card instantly
const medicalModalVisible = ref(false)

const userProfile = ref({
  id: 1042,
  name: 'Alex Mercer',
  email: 'alex.mercer@apex.com',
  contact: '9876543210',
  is_active: true,
  created_at: 'May 14, 2026',
  last_login_at: '3 minutes ago',
  profile_pic: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80',
  blacklisted: false
})

// Database model field mappings for empty display states fallback
const medicalProfile = ref({
  blood_group: '',
  diagonisis: '',
  allergies: '',
  emergency_name: '',
  emergency_phone: '',
  emergency_relation: '',
  updated_at: ''
})

// Input proxy state variables inside the popup overlay wrapper
const medicalFormFields = ref({
  blood_group: '',
  diagonisis: '',
  allergies: '',
  emergency_name: '',
  emergency_phone: '',
  emergency_relation: ''
})

function openMedicalModal() {
  // Populate form with existing data if editing
  medicalFormFields.value = { ...medicalProfile.value }
  medicalModalVisible.value = true
}

function submitMedicalForm() {
  const contactPattern = /^\d{10}$/
  if (!contactPattern.test(medicalFormFields.value.emergency_phone)) {
    alertStore.showAlert('Validation Warning: Contact phone must contain exactly 10 digits.', 'danger')
    return
  }

  // Simulate a successful API response capture handler
  medicalProfile.value = {
    ...medicalFormFields.value,
    updated_at: 'Just now'
  }
  
  hasMedicalData.value = true
  medicalModalVisible.value = false
  alertStore.showAlert('Success: Multi-part medical metrics saved to database matrix.', 'success')
}

function saveProfileFields() {
  alertStore.showAlert('Success: Base profile credentials patched.', 'success')
}

function triggerPasswordReset() {
  alertStore.showAlert('Security Matrix Alert: OTP code dispatcher initializing via Celery + Redis workers sequence.', 'warning')
}

function uploadAvatarImage(event) {
  const file = event.target.files[0]
  if (file) {
    userProfile.value.profile_pic = URL.createObjectURL(file)
    alertStore.showAlert('Success: Avatar image cache sync verified.', 'success')
  }
}
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
  background: rgba(10, 20, 15, 0.55) !important;
  backdrop-filter: blur(20px) !important; -webkit-backdrop-filter: blur(20px) !important;
  z-index: 99999999 !important;
}

.glass-modal-card {
  background: rgba(25, 35, 30, 0.8) !important;
  backdrop-filter: blur(30px);
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
</style>