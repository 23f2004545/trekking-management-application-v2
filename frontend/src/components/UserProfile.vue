<template>
  <div class="user-profile-shared-component text-white text-start animate-fade-in">
    
    <div v-if="profile.blacklisted" class="alert alert-warning border border-danger border-opacity-20 rounded-3 p-3 mb-4 bg-danger bg-opacity-10">
      <i class="bi bi-exclamation-triangle text-warning"></i> <strong>Blacklisted:</strong> This exploration profile coordinate layer has been blacklisted by administration.
    </div>

    <div class="row g-4">
      
      <div class="col-lg-12">
        <div class="glass-profile-panel text-center p-4 rounded-4 border border-white border-opacity-10 h-100 shadow-sm">
          
          <div class="avatar-edit-cluster position-relative d-inline-block mx-auto mb-3">
            <img :src="BACKEND_URL + (profile.profile_pic )" alt="Avatar Profile" class="profile-main-avatar shadow border border-white border-opacity-20" />
          </div>

          <h4 class="fw-bold tracking-tight mb-2">{{ profile.name }}</h4>
          
          
          <hr class="my-4 border-white border-opacity-10" />

          <div class="telemetry-logs text-start gap-3 d-flex flex-column fs-9 text-white-50">
            <div class="log-item d-flex justify-content-between">
              <span>Account Status</span>
              <span class="fw-bold" :class="profile.is_active ? 'text-success' : 'text-danger'">
                ● {{ profile.is_active ? 'Active' : 'Deactivated' }}
              </span>
            </div>
            <div v-if="profileRole=='trek_staff'" class="log-item d-flex justify-content-between">
              <span>Staff Status</span>
              <span class="fw-bold" :class="profile.status=='Active' ? 'text-info' : 'text-warning'">
                ● {{ profile.status }}
              </span>
            </div>
            <div class="log-item d-flex justify-content-between">
              <span>Key Code:</span>
              <span class="fw-bold text-white">#APX-U{{ profile.id }}</span>
            </div>
            <div class="log-item d-flex justify-content-between" v-if="profile.created_at">
              <span>Created </span>
              <span class="fw-bold text-white">{{ profile.created_at }}</span>
            </div>
            <div class="log-item d-flex justify-content-between">
              <span>Last Entry:</span>
              <span class="fw-bold text-success text-glow">● {{ profile.last_login_at }}</span>
            </div>
          </div>

        </div>
      </div>

      <div class="col-lg-12">
        <div class="glass-profile-panel p-4 p-md-5 rounded-4 border border-white border-opacity-10 h-100 shadow-sm">
          <h5 class="fw-bold mb-4 tracking-tight border-bottom border-white border-opacity-10 pb-2">Profile Specifications Registry</h5>
          
          <div class="d-flex flex-column gap-2">
            
            <div class="profile-input-group mb-3">
              <label class="input-label-tag">Registered Name</label>
              <div class="interactive-input-wrapper locked-input opacity-75">
                <input :value="profile.name" type="text" class="clean-profile-field w-100" disabled>
              </div>
            </div>

            <div class="profile-input-group mb-3">
              <label class="input-label-tag">Contact Number</label>
              <div class="interactive-input-wrapper locked-input opacity-75">
                <input :value="profile.contact" type="tel" class="clean-profile-field w-100" disabled>
              </div>
            </div>

            <div class="profile-input-group mb-3">
              <label class="input-label-tag opacity-50">Email Reference </label>
              <div class="interactive-input-wrapper locked-input opacity-60">
                <input :value="profile.email" type="email" class="clean-profile-field w-100" disabled>
              </div>
            </div>

            <div v-if="profileRole == 'trek_staff'" class="mt-4 pt-3 border-top border-white border-opacity-10">
              <h6 class="fw-bold mb-3 text-warning">Staff Credentials Registry</h6>
              <div class="row g-3">
                <div class="col-sm-6">
                  <label class="input-label-tag">Field Specialization</label>
                  <div class="interactive-input-wrapper locked-input opacity-75">
                    <input :value="profile.specialization || 'N/A'" type="text" class="clean-profile-field w-100" disabled>
                  </div>
                </div>
                <div class="col-sm-6">
                  <label class="input-label-tag">Guide Certification</label>
                  <div class="interactive-input-wrapper locked-input opacity-75">
                    <input :value="profile.certification || 'N/A'" type="text" class="clean-profile-field w-100" disabled>
                  </div>
                </div>
                <div class="col-sm-6">
                  <label class="input-label-tag">Emergency Contact</label>
                  <div class="interactive-input-wrapper locked-input opacity-75">
                    <input :value="profile.emergency_contact || 'N/A'" type="text" class="clean-profile-field w-100" disabled>
                  </div>
                </div>
                <div class="col-sm-6">
                  <label class="input-label-tag">Experience</label>
                  <div class="interactive-input-wrapper locked-input opacity-75">
                    <input :value="profile.experience || '0'" type="number" class="clean-profile-field w-100" disabled>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="profileRole === 'trekker'" class="mt-4 pt-3 border-top border-white border-opacity-10">
              <h6 class="fw-bold mb-3 text-info">Trekker Medical & Emergency Data</h6>
              <div class="row g-3">
                <div class="col-sm-6">
                  <label class="input-label-tag">Blood Group</label>
                  <div class="interactive-input-wrapper locked-input opacity-75">
                    <input :value="profile.blood_group || 'N/A'" type="text" class="clean-profile-field w-100" disabled>
                  </div>
                </div>
                <div class="col-sm-6">
                  <label class="input-label-tag">Diagonisis</label>
                  <div class="interactive-input-wrapper locked-input opacity-75">
                    <input :value="profile.diagnosis || 'N/A'" type="text" class="clean-profile-field w-100" disabled>
                  </div>
                </div>
                <div class="col-sm-6">
                  <label class="input-label-tag">Emergency Contact</label>
                  <div class="interactive-input-wrapper locked-input opacity-75">
                    <input :value="profile.emergency_contact || 'N/A'" type="text" class="clean-profile-field w-100" disabled>
                  </div>
                </div>
                <div class="col-sm-6">
                  <label class="input-label-tag">Emergency Name</label>
                  <div class="interactive-input-wrapper locked-input opacity-75">
                    <input :value="profile.emergency_name || 'N/A'" type="text" class="clean-profile-field w-100" disabled>
                  </div>
                </div>
                <div class="col-sm-6">
                  <label class="input-label-tag">Medication</label>
                  <div class="interactive-input-wrapper locked-input opacity-75">
                    <input :value="profile.medications || 'N/A'" type="text" class="clean-profile-field w-100" disabled>
                  </div>
                </div>
                <div class="col-sm-6">
                  <label class="input-label-tag">Allergies</label>
                  <div class="interactive-input-wrapper locked-input opacity-75">
                    <input :value="profile.allergies || 'N/A'" type="text" class="clean-profile-field w-100" disabled>
                  </div>
                </div>
              </div>
            </div>


            <div v-if="mode!='readonly'" class="mt-4 pt-2 border-top border-white border-opacity-5 d-flex align-items-center justify-content-between flex-wrap gap-3">
              <div class="d-flex justify-content-end gap-2 w-100 pt-3">
                <button type="button" @click="confirmStore.ask('Are you sure to ' + (profile.blacklisted ? 'whitelist' : 'blacklist') + ' ' + profile.name + '?', () => $emit('admin-toggle-blacklist', profile.id))" class="btn btn-sm rounded-pill px-4 py-2 fs-9 fw-semibold" :class="profile.blacklisted === false ? 'btn-outline-warning' : 'btn-outline-success' " >
                  {{ profile.blacklisted ? 'Whitelist' : 'Blacklist' }}
                </button>
                <button type="button" @click="confirmStore.ask('Are you sure about ' + (profile.is_active ? 'deactivating' : 'reactivating') + ' ' + profile.name + '`s account ?', () => $emit('admin-toggle-active', profile.id))" class="btn btn-sm rounded-pill px-4 py-2 fs-9 fw-bold" :class="profile.is_active === true ? 'btn-danger' : 'btn-success' ">
                  {{ profile.is_active ? 'Deactivate' : 'Reactivate' }}
                </button>
              </div>
            </div>

          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { readonly } from 'vue';
import { useConfirmStore } from '@/stores/confirm.js'

const confirmStore = useConfirmStore()
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL 

defineProps({
  profile: { type: Object, required: true },
  profileRole: { type: String, default: 'trekker' },
  mode : { type: String, default: 'audit'}
})

defineEmits(['admin-toggle-blacklist', 'admin-toggle-active'])
</script>

<style scoped>
.glass-profile-panel { background: rgba(255, 255, 255, 0.05) !important; backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.12) !important; }
.profile-main-avatar { width: 110px; height: 110px; border-radius: 50%; object-fit: cover; }
.avatar-upload-badge { position: absolute; bottom: 0; right: 4px; background: #ffffff; color: #111; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; cursor: pointer; }
.role-indicator-badge { background: rgba(25, 135, 84, 0.15); color: #7bf1a8; border: 1px solid rgba(25, 135, 84, 0.3); text-transform: uppercase; }

.input-label-tag { font-size: 0.8rem; color: rgba(255, 255, 255, 0.5); font-weight: 500; margin-bottom: 5px; display: block; }
.interactive-input-wrapper { background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 10px; padding: 10px 14px; display: flex; }
.clean-profile-field { border: none; background: transparent; color: #ffffff; outline: none; font-size: 0.95rem;  }

.btn-security-link { color: #ffc107; cursor: pointer; font-size: 0.85rem; } .btn-security-link:hover { text-decoration: underline; }
.uppercase { text-transform: uppercase; } .fs-8 { font-size: 0.88rem; } .fs-9 { font-size: 0.76rem; }
</style>