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

      <form @submit.prevent="handleRegistration" class="auth-form text-start">
        
        <div class="form-row-grid mb-3">
          <div class="input-group-container">
            <label class="input-label">Full Name</label>
            <div class="input-field-wrapper">
              <input v-model="name" type="text" required placeholder="Alex Mercer" class="auth-clean-input">
            </div>
          </div>

          <div class="input-group-container">
            <label class="input-label">Contact Number</label>
            <div class="input-field-wrapper">
              <input v-model="contact" type="tel" required placeholder="+91 98765..." class="auth-clean-input">
            </div>
          </div>
        </div>

        <div class="input-group-container mb-3">
          <label class="input-label">Email Address</label>
          <div class="input-field-wrapper">
            <input v-model="email" type="email" required placeholder="name@domain.com" class="auth-clean-input">
          </div>
        </div>

        <div class="form-row-grid mb-3">
          <div class="input-group-container">
            <label class="input-label">Password</label>
            <div class="input-field-wrapper">
              <input v-model="password" type="password" required placeholder="Create password" class="auth-clean-input">
            </div>
          </div>

          <div class="input-group-container">
            <label class="input-label">Confirm Password</label>
            <div class="input-field-wrapper" :class="{ 'error-border': passwordMismatch }">
              <input v-model="confirmPassword" type="password" required placeholder="Retype password" class="auth-clean-input">
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
        </div>

        <div v-if="passwordMismatch" class="validation-warning mb-3">
          ⚠️ Passwords do not match.
        </div>

        <button type="submit" :disabled="passwordMismatch" class="btn-auth-submit w-100 py-3 mb-4 fw-bold">
          Create Account
        </button>

      </form>

      <div class="divider-zone mb-4">
        <span class="divider-text">Already registered your camp details?</span>
      </div>

      <p class="switch-auth-text m-0">
        Have an account? 
        <a href="#" @click.prevent="$router.push('/login')" class="action-link fw-bold">Sign In</a>
      </p>

    </div>
  </div>
</template>

<script>
export default {
  name: 'RegisterView',
  data() {
    return {
      name: '',
      email: '',
      contact: '',
      password: '',
      confirmPassword: '',
      profileFile: null,
      fileNameDisplay: 'No file chosen'
    }
  },
  computed: {
    passwordMismatch() {
      if (!this.confirmPassword) return false;
      return this.password !== this.confirmPassword;
    }
  },
  methods: {
    handleFileSelection(event) {
      const file = event.target.files[0];
      if (file) {
        if (file.size > 2 * 1024 * 1024) {
          alert("File is too large! Maximum limit is 2MB.");
          this.clearFileInput();
          return;
        }
        this.profileFile = file;
        this.fileNameDisplay = file.name;
      } else {
        this.clearFileInput();
      }
    },
    clearFileInput() {
      this.profileFile = null;
      this.fileNameDisplay = 'No file chosen';
      if (this.$refs.fileInput) this.$refs.fileInput.value = '';
    },
    handleRegistration() {
      if (this.passwordMismatch) return;

      const formData = new FormData();
      formData.append('name', this.name);
      formData.append('email', this.email);
      formData.append('contact', this.contact);
      formData.append('password', this.password);
      
      if (this.profileFile) {
        formData.append('profile_pic', this.profileFile);
      }

      console.log('Multipart FormData compiled payload successfully.');
      alert('Registration successful! Moving back to the base authorization gate.');
      this.$router.push('/login');
    }
  }
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