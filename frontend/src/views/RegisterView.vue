<template>
  <div class="register-viewport w-100 min-vh-100 d-flex align-items-center justify-content-center p-2 p-md-3">
    
    <button @click="$router.push('/')" class="btn-back-home">
      ← Back to Main
    </button>

    <div class="glass-register-card p-4 text-center my-3">
      
      <div class="brand-header mb-4">
        <div class="logo-accent mx-auto mb-2">🥾</div>
        <h2 class="auth-title">Create Trekker Account</h2>
        <p class="auth-subtitle">Set up your profile to start exploring paths, secure high-alpine slot bookings, and track safety logs.</p>
      </div>

      <form @submit.prevent="handleRegistration" class="auth-form text-start" enctype="multipart/form-data">
        
        <div class="form-row-grid mb-3">
          <div class="input-group-container">
            <label class="input-label">Full Name</label>
            <div class="input-field-wrapper">
              <input v-model.lazy="name" type="text" placeholder="Alex Mercer" class="auth-clean-input" @change="validateName">
            </div>
            <div v-if="nameError" class="input-label my-2 text-warning">
              {{ nameError }}
            </div>
          </div>

          <div class="input-group-container">
            <label class="input-label">Contact</label>
            <div class="input-field-wrapper">
              <input v-model.lazy="contact" type="tel" placeholder="+91 98765..." class="auth-clean-input" @change="validateContact">
            </div>
            <div v-if="contactError" class="input-label my-2 text-warning">
              {{ contactError }}
            </div>
          </div>
        </div>

        <div class="input-group-container mb-3">
          <label class="input-label">Email Address</label>
          <div class="input-field-wrapper">
            <input v-model.lazy="email" type="text" placeholder="name@domain.com" class="auth-clean-input" @change="validateEmail">
          </div>
          <div v-if="emailError" class="input-label my-2 text-warning">
            {{ emailError }}
          </div>
        </div>

        <div class="form-row-grid mb-3">
          <div class="input-group-container">
            <label class="input-label">Password</label>
            <div class="input-field-wrapper">
              <input v-model.lazy="password" type="password" placeholder="Create password" class="auth-clean-input" @change="validatePassword">
            </div>
            <div v-if="passwordError" class="input-label my-2 text-warning">
              {{ passwordError }}
            </div>
          </div>

          <div class="input-group-container">
            <label class="input-label">Confirm Password</label>
            <div class="input-field-wrapper" :class="{ 'error-border': passwordMismatch }">
              <input v-model.lazy="confirmPassword" type="password" placeholder="Retype password" class="auth-clean-input" @change="validatePassword">
            </div>
            <div v-if="passwordMismatch" class="input-label my-2 text-warning">
              ⚠️ Passwords do not match.
            </div>
          </div>
        </div>

        <div class="input-group-container mb-4">
          <label class="input-label">Profile Picture <span class="muted-note">(Optional)</span></label>
          <div class="file-upload-wrapper">
            <input 
              type="file" 
              id="profile_pic" 
              ref="fileInput"
              accept="image/*" 
              @change="handleFileSelection"
              class="hidden-file-input"
            >
            <label for="profile_pic" class="file-custom-btn">Choose file</label>
            <span class="file-name-label">{{ fileNameDisplay }}</span>
          </div>
          <div v-if="fileError" class="input-label my-2 text-warning">
            {{ fileError }}
          </div>
        </div>

        <button type="submit" class="btn-auth-submit w-100 py-3 mb-4 fw-bold">
          Create Account
        </button>

      </form>

      <div class="divider-zone mb-4">
        <span class="divider-text">Already registered your camp details?</span>
      </div>

      <p class="switch-auth-text m-0">
        Have an account? 
        <RouterLink to="/login" class="action-link fw-bold">Sign In</RouterLink>
      </p>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAlertStore } from '@/stores/alert'

const router = useRouter()
const alertStore = useAlertStore()

// Core Form State Input Variables
const name = ref('')
const email = ref('')
const contact = ref('')
const password = ref('')
const confirmPassword = ref('')
const profileFile = ref(null)
const fileNameDisplay = ref('No file chosen')

// Dedicated Field Error Messages 
const nameError = ref('')
const emailError = ref('')
const contactError = ref('')
const passwordError = ref('')
const fileError = ref('')
const serverError = ref('')


// Validation Functions for Each Input Field 
function validateName() {
  // Regex ensures text strictly contains characters and space breaks (no numbers/specials)
  const namePattern = /^[a-zA-Z\s]+$/
  if (!namePattern.test(name.value)) {
    nameError.value = 'Name should only contain letters.'
  } else {
    nameError.value = ''
  }
}

function validateEmail() {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailPattern.test(email.value)) {
    emailError.value = 'Please enter a valid email address.'
  } else {
    emailError.value = ''
  }
}

function validateContact() {
  // Verifies the field contains exactly 10 numeric units
  const contactPattern = /^\d{10}$/
  if (!contactPattern.test(contact.value)) {
    contactError.value = 'Number must be exactly 10 digits.'
  } else {
    contactError.value = ''
  }
}

function validatePassword() {
  if (password.value.length < 8) {
    passwordError.value = 'Atleast 8 characters required.'
  } else {
    passwordError.value = ''
  }
}

const passwordMismatch = computed(() => {
  if (!confirmPassword.value) return false
  return password.value !== confirmPassword.value
})

const isFormInvalid = computed(() => {
  return (
    !!nameError.value ||
    !!emailError.value ||
    !!contactError.value ||
    !!passwordError.value ||
    !!fileError.value ||
    passwordMismatch.value ||
    !name.value ||
    !email.value ||
    !contact.value ||
    !password.value
  )
})

function handleFileSelection(event) {
  const file = event.target.files[0]
  fileError.value = ''
  
  if (file) {
    if (file.size > 1 * 1024 * 1024) {
      fileError.value = 'Max file size should not exceed 1MB'
      profileFile.value = null
      fileNameDisplay.value = 'No file chosen'
      event.target.value = '' // Clear input channel element
      return
    }
    profileFile.value = file
    fileNameDisplay.value = file.name
  } else {
    profileFile.value = null
    fileNameDisplay.value = 'No file chosen'
  }
}

async function handleRegistration() {
  // Final safeguard pass-check execution loop
  validateName()
  validateEmail()
  validateContact()
  validatePassword()
  
  if (email.value === '' || password.value === '' || name.value === '' || contact.value === '' || confirmPassword.value === '') {
  alertStore.showAlert('Please fill in all fields.', 'error');
  return;
  }

  if (isFormInvalid.value) return
  serverError.value = ''

  // Using FormData wrapper object to map request payload properties perfectly
  const formData = new FormData()
  formData.append('name', name.value)
  formData.append('email', email.value)
  formData.append('contact', contact.value)
  formData.append('password', password.value)
  
  if (profileFile.value) {
    formData.append('profile_pic', profileFile.value)
  }

  const response = await fetch("http://127.0.0.1:5000/api/auth/register", {
      method: "POST",
      // Important: When using FormData, the browser automatically sets the correct Content-Type header with boundary, so we should NOT set it manually.
      body: formData
    })

    const data = await response.json()

    if (!response.ok) {
      // Catches your backend checks (e.g., 'Email already registered')
      serverError.value = data.error || data.message || 'Registration anomaly detected.'
      alertStore.showAlert(serverError.value, 'error')
      return
    }

    alertStore.showAlert('Profile activated successfully!', 'success')
    router.push('/login')
}
</script>

<style scoped>
/* Base positioning layer */
.register-viewport {
  position: relative;
  z-index: 10;
  box-sizing: border-box;
}

/* Floating Return Anchor */
.btn-back-home {
  position: absolute;
  top: 24px;
  left: 24px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(8px);
  color: #ffffff;
  padding: 8px 16px;
  border-radius: 30px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s ease;
}
.btn-back-home:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* Identical Premium High-Translucency Login Glass Structure */
.glass-register-card {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(25px) !important;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
  border-radius: 24px;
  width: 100%;
  max-width: 520px; /* Slightly wider to give side-by-side inputs clean breathing room */
}

/* Typography Aesthetics */
.logo-accent {
  font-size: 2.2rem;
}

.auth-title {
  color: #ffffff;
  font-size: 1.85rem;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.auth-subtitle {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.88rem;
  line-height: 1.5;
  max-width: 440px;
  margin: 0 auto;
}

/* Two-Column Responsive Layout Grid Grid */
.form-row-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.input-group-container {
  display: flex;
  flex-direction: column;
}

.input-label {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.82rem;
  font-weight: 500;
  margin-bottom: 6px;
}

.muted-note {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.5);
}

/* Translucent input fields matched directly to login screen dimensions */
.input-field-wrapper {
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 12px;
  padding: 10px 14px;
  display: flex;
  align-items: center;
  transition: border-color 0.2s ease;
}

.input-field-wrapper:focus-within {
  border-color: #ffffff;
  background: rgba(255, 255, 255, 0.18);
}

.auth-clean-input {
  border: none;
  background: transparent;
  color: #ffffff;
  width: 100%;
  font-size: 0.95rem;
  outline: none;
}

.auth-clean-input::placeholder {
  color: rgba(255, 255, 255, 0.45);
}

/* Custom Unified Glass File Uploader Element */
.file-upload-wrapper {
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 12px;
  display: flex;
  align-items: center;
  overflow: hidden;
  padding: 5px;
}

.hidden-file-input {
  display: none;
}

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

.file-name-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.88rem;
  margin-left: 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Action Gate Buttons & Links */
.action-link {
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.88rem;
  text-decoration: none;
  transition: color 0.2s ease;
}
.action-link:hover {
  color: #ffffff;
  text-decoration: underline;
}

/* Crisp Solid High-Contrast Submit Button */
.btn-auth-submit {
  background-color: #ffffff;
  color: #0b1f15;
  border: none;
  border-radius: 12px;
  font-size: 0.95rem;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  transition: background-color 0.2s ease, transform 0.1s ease;
}
.btn-auth-submit:hover:not(:disabled) {
  background-color: #e8f5e9;
}
.btn-auth-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.btn-auth-submit:active {
  transform: scale(0.99);
}

/* Mismatch Warnings */
.error-border {
  border-color: #ff6b6b !important;
  background: rgba(255, 107, 107, 0.05) !important;
}

.validation-warning {
  color: #ff6b6b;
  font-size: 0.82rem;
  font-weight: 500;
  text-shadow: 0 1px 4px rgba(0,0,0,0.2);
}

/* Symmetric Boundary Splitters */
.divider-zone {
  position: relative;
  text-align: center;
}
.divider-zone::before {
  content: "";
  position: absolute;
  top: 50%; left: 0; right: 0;
  height: 1px;
  background: rgba(255, 255, 255, 0.15);
  z-index: 1;
}
.divider-text {
  position: relative;
  z-index: 2;
  background: rgba(255, 255, 255, 0.1); 
  backdrop-filter: blur(10px);
  padding: 2px 12px;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.78rem;
}

.switch-auth-text {
  color: rgba(255, 255, 255, 0.75);
  font-size: 0.88rem;
}

</style>