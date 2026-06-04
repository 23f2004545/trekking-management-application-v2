<template>
  <div class="user-profile-shared-component text-white text-start animate-fade-in">
    
    <div v-if="profile.blacklisted" class="alert alert-danger border border-danger border-opacity-20 rounded-3 p-3 mb-4 bg-danger bg-opacity-10">
      <i class="bi bi-exclamation-triangle text-warning"></i> <strong>Account Flag Restriction Status Active:</strong> This exploration profile coordinate layer has been blacklisted by administration.
    </div>

    <div class="row g-4">
      
      <div class="col-lg-4">
        <div class="glass-profile-panel text-center p-4 rounded-4 border border-white border-opacity-10 h-100 shadow-sm">
          
          <div class="avatar-edit-cluster position-relative d-inline-block mx-auto mb-3">
            <img :src="BACKEND_URL + (profile.profile_pic )" alt="Avatar Profile" class="profile-main-avatar shadow border border-white border-opacity-20" />
            
            <label v-if="mode === 'self'" class="avatar-upload-badge clickable" title="Upload Fresh Avatar Image">
              📸
              <input type="file" accept="image/*" class="d-none" @change="$emit('avatar-upload', $event)">
            </label>
          </div>

          <h4 class="fw-bold tracking-tight mb-2">{{ profile.name }}</h4>
          <span class="badge role-indicator-badge mt-1.5 px-3 py-1 rounded-pill small uppercase">{{ profileRole }}</span>
          
          <hr class="my-4 border-white border-opacity-10" />

          <div class="telemetry-logs text-start gap-3 d-flex flex-column fs-9 text-white-50">
            <div class="log-item d-flex justify-content-between">
              <span>Status</span>
              <span class="fw-bold" :class="profile.is_active ? 'text-success' : 'text-danger'">
                ● {{ profile.is_active ? 'Active' : 'Deactivated' }}
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

      <div class="col-lg-8">
        <div class="glass-profile-panel p-4 p-md-5 rounded-4 border border-white border-opacity-10 h-100 shadow-sm">
          <h5 class="fw-bold mb-4 tracking-tight border-bottom border-white border-opacity-10 pb-2">Profile Specifications Registry</h5>
          
          <form @submit.prevent="$emit('patch-profile', localForm)" class="d-flex flex-column gap-3.5">
            
            <div class="profile-input-group mb-3">
              <label class="input-label-tag">Registered Identity Name</label>
              <div class="interactive-input-wrapper" :class="{ 'locked-input opacity-75': mode === 'audit' }">
                <input v-model="localForm.name" type="text" class="clean-profile-field w-100" :disabled="mode === 'audit'" required>
              </div>
            </div>

            <div class="profile-input-group mb-3">
              <label class="input-label-tag">Contact Number Channel</label>
              <div class="interactive-input-wrapper" :class="{ 'locked-input opacity-75': mode === 'audit' }">
                <input v-model="localForm.contact" type="tel" class="clean-profile-field w-100" :disabled="mode === 'audit'" required>
              </div>
            </div>

            <div class="profile-input-group mb-3">
              <label class="input-label-tag opacity-50">Email Reference Coordinate (Immutable Identity Key)</label>
              <div class="interactive-input-wrapper locked-input opacity-60">
                <input :value="profile.email" type="email" class="clean-profile-field w-100" disabled>
              </div>
            </div>

            <div v-if="profileRole === 'trek_staff'" class="row g-3 mt-1 text-start">
              <div class="col-sm-6">
                <label class="input-label-tag">Field Specialization</label>
                <div class="interactive-input-wrapper locked-input opacity-75">
                  <input :value="profile.specialization || 'High-Altitude Traversal'" type="text" class="clean-profile-field w-100" disabled>
                </div>
              </div>
              <div class="col-sm-6">
                <label class="input-label-tag">Guide Certification License</label>
                <div class="interactive-input-wrapper locked-input opacity-75">
                  <input :value="profile.certification || 'NIM Mountaineering'" type="text" class="clean-profile-field w-100" disabled>
                </div>
              </div>
            </div>

            <div class="mt-4 pt-2 border-top border-white border-opacity-5 d-flex align-items-center justify-content-between flex-wrap gap-3">
              
              <div v-if="mode === 'self'" class="d-flex align-items-center justify-content-between w-100">
                <button type="button" @click="$emit('request-password-otp')" class="btn-security-link text-warning fw-semibold small bg-transparent border-0 p-0">
                  ⚙️ Reset System Security Key
                </button>
                <button type="submit" class="btn btn-light rounded-3 px-5 py-2.5 fw-bold text-dark border-0 fs-8 shadow-sm">
                  Patch Profile Coordinates
                </button>
              </div>

              <div v-else-if="mode === 'audit'" class="d-flex justify-content-end gap-2 w-100 pt-3">
                <button type="button" @click="$emit('admin-toggle-blacklist', profile.id)" class="btn btn-sm btn-outline-warning rounded-pill px-4 py-2 fs-9 fw-semibold">
                  {{ profile.blacklisted ? 'Whitelist Account' : 'Blacklist Profile' }}
                </button>
                <button type="button" @click="$emit('admin-toggle-active', profile.id)" class="btn btn-sm btn-danger rounded-pill px-4 py-2 fs-9 fw-bold">
                  {{ profile.is_active ? 'Deactivate Guides Code' : 'Activate User Profile' }}
                </button>
              </div>

            </div>

          </form>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL 
const props = defineProps({
  profile: { type: Object, required: true },
  profileRole: { type: String, default: 'trekker' }, // Options: 'admin', 'trek_staff', 'trekker'
  mode: { type: String, default: 'self' }         // Options: 'self', 'audit'
})

defineEmits(['patch-profile', 'avatar-upload', 'request-password-otp', 'admin-toggle-blacklist', 'admin-toggle-active'])

// Reactive input proxies
const localForm = ref({
  name: props.profile.name,
  contact: props.profile.contact
})

// Deep watch values context to sync dynamic dataset when admin switches audit logs lists targets
watch(() => props.profile, (newProfile) => {
  localForm.value.name = newProfile.name
  localForm.value.contact = newProfile.contact
}, { deep: true })
</script>

<style scoped>
.glass-profile-panel { background: rgba(255, 255, 255, 0.05) !important; backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.12) !important; }
.profile-main-avatar { width: 110px; height: 110px; border-radius: 50%; object-fit: cover; }
.avatar-upload-badge { position: absolute; bottom: 0; right: 4px; background: #ffffff; color: #111; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; cursor: pointer; }
.role-indicator-badge { background: rgba(25, 135, 84, 0.15); color: #7bf1a8; border: 1px solid rgba(25, 135, 84, 0.3); text-transform: uppercase; }

.input-label-tag { font-size: 0.8rem; color: rgba(255, 255, 255, 0.5); font-weight: 500; margin-bottom: 5px; display: block; }
.interactive-input-wrapper { background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 10px; padding: 10px 14px; display: flex; }
.clean-profile-field { border: none; background: transparent; color: #ffffff; outline: none; font-size: 0.95rem; }

.btn-security-link { color: #ffc107; cursor: pointer; font-size: 0.85rem; } .btn-security-link:hover { text-decoration: underline; }
.uppercase { text-transform: uppercase; } .gap-3.5 { gap: 14px; } .fs-8 { font-size: 0.88rem; } .fs-9 { font-size: 0.76rem; }
</style>