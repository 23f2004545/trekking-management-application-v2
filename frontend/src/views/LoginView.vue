<template>
  <div class="public-bg-wrapper w-100 min-vh-100 d-flex align-items-center justify-content-center p-3">
    
    <button @click="$router.push('/')" class="btn-back-home ">
      ← Back to Main
    </button>

    <div class="glass-login-card p-4 p-md-5 mt-5 text-center">
      
      <div class="brand-header mb-4">
        <div class="logo-accent mx-auto mb-2">🍃</div>
        <h2 class="auth-title">Welcome Back</h2>
        <p class="auth-subtitle">Sign in to access your base camp dashboards, upcoming treks, and staff logs.</p>
      </div>

      <form @submit.prevent="handleLogin" class="auth-form text-start">
        
        <div class="input-group-container mb-3">
          <label class="input-label">Email Address</label>
          <div class="input-field-wrapper">
            <span class="field-icon"><i class="bi bi-envelope-fill text-white"></i></span>
            <input 
              v-model.lazy="email"
              type="text" 
              placeholder="name@domain.com"
              class="auth-clean-input"
              @change="validateEmail"
            >
          </div>
          <div v-if="emailError" class="input-label my-2 text-warning">
            {{ emailError }}
          </div>
        </div>

        <div class="input-group-container mb-4">
          <div class="d-flex justify-content-between align-items-center mb-1">
            <label class="input-label mb-0">Password</label>
            <p @click="openForgotModal" class="helper-link">Forgot password?</p>
          </div>
          <div class="input-field-wrapper">
            <span class="field-icon"><i class="bi bi-key-fill text-white"></i></span>
            <input 
              v-model="password"
              type="password" 
              placeholder="••••••••"
              class="auth-clean-input"
            >
          </div>
        </div>

        <button type="submit" class="btn-auth-submit w-100 py-3 mb-4">
          Log In
        </button>

      </form>

      <!-- INSTANT PORTFOLIO DEMO ACCESS SECTION -->
      <div class="demo-access-cluster mb-4">
        <div class="divider-zone mb-3">
          <span class="divider-text">⚡ Instant Demo Access (Portfolio Preview)</span>
        </div>

        <div class="d-flex gap-2 justify-content-center">
          <!-- Admin Button -->
          <button 
            type="button" 
            @click="handleDemoLogin('admin')" 
            :disabled="isDemoLoading"
            class="btn btn-sm btn-outline-danger d-flex align-items-center gap-2 px-3 py-1.5 rounded-pill"
          >
            <i class="bi bi-shield-lock-fill text-reset"></i>
            <span>{{ isDemoLoading && activeDemoRole === 'admin' ? 'Seeding...' : 'Admin' }}</span>
          </button>

          <!-- Staff Button -->
          <button 
            type="button" 
            @click="handleDemoLogin('trek_staff')" 
            :disabled="isDemoLoading"
            class="btn btn-sm btn-outline-warning d-flex align-items-center gap-2 px-3 py-1.5 rounded-pill"
          >
            <!-- text-dark ensures the staff icon stays visible if warning turns background bright yellow -->
            <i class="bi bi-compass-fill text-reset"></i>
            <span>{{ isDemoLoading && activeDemoRole === 'trek_staff' ? 'Seeding...' : 'Staff' }}</span>
          </button>

          <!-- Trekker Button -->
          <button 
            type="button" 
            @click="handleDemoLogin('trekker')" 
            :disabled="isDemoLoading"
            class="btn btn-sm btn-outline-success d-flex align-items-center gap-2 px-3 py-1.5 rounded-pill"
          >
            <i class="bi bi-person-fill-gear text-reset"></i>
            <span>{{ isDemoLoading && activeDemoRole === 'trekker' ? 'Seeding...' : 'Trekker' }}</span>
          </button>
        </div>
      </div>


      <div class="divider-zone mb-4">
        <span class="divider-text">Ready for new horizons?</span>
      </div>

      <p class="switch-auth-text m-0">
        Don't have an account? 
        <RouterLink to="/register" class="action-link fw-bold">Sign Up</RouterLink>
      </p>

    </div>

    <Transition name="modal-fade">
      <div v-if="forgotModalActive" @click.self="closeForgotModal" class="login-overlay-backdrop d-flex align-items-center justify-content-center p-3">
        <div class="glass-modal-card p-4 p-md-5 rounded-4 border border-white border-opacity-15 shadow-lg text-start animate-scale-up position-relative" style="max-width: 450px; width: 100%;">
          
          <button @click="closeForgotModal" class="btn-close-modal">✕</button>

          <h4 class="fw-bold tracking-tight text-white mb-1">Secure Access</h4>
          <p class="text-white-50 small mb-4">
            {{ otpStep === 1 ? 'Enter your registered email to receive a temporary authorization token.' : 'Enter the 6-digit token sent to your terminal.' }}
          </p>

          <form v-if="otpStep === 1" @submit.prevent="requestLoginOTP" class="d-flex flex-column gap-3">
            <div class="input-group-capsule">
              <label class="modal-input-label">Registered Email</label>
              <div class="modal-input-wrapper">
                <input v-model="forgotEmail" type="email" required class="modal-clean-field w-100" placeholder="explorer@apex.com">
              </div>
            </div>
            <button type="submit" :disabled="isProcessing" class="btn btn-success w-100 rounded-pill py-2.5 fw-bold text-dark mt-2 shadow-sm">
              {{ isProcessing ? 'Pinging Servers...' : 'Transmit Token' }}
            </button>
          </form>

          <form v-else @submit.prevent="verifyLoginOTP" class="d-flex flex-column gap-3">
            <div class="input-group-capsule">
              <div class="d-flex justify-content-between align-items-end mb-1">
                <label class="modal-input-label m-0">Authorization Code</label>
                <span class="fs-9 text-warning">Expires in {{ formattedTime }}</span>
              </div>
              <div class="modal-input-wrapper">
                <input v-model="forgotOTP" type="text" required class="modal-clean-field w-100 fw-bold tracking-widest text-warning text-center fs-4" placeholder="000000" maxlength="6">
              </div>
            </div>
            <button type="submit" :disabled="isProcessing" class="btn btn-warning w-100 rounded-pill py-2.5 fw-bold text-dark mt-2 shadow-sm">
              {{ isProcessing ? 'Verifying...' : 'Authorize & Connect' }}
            </button>
            <button type="button" @click="otpStep = 1" class="btn btn-link text-white-50 text-decoration-none fs-9 w-100 mt-1">
              ← Use a different email
            </button>
          </form>

        </div>
      </div>
    </Transition>

    <!-- Interactive Demo Email Delivery Modal for OTP Login -->
    <DemoEmailPromptModal 
      :isOpen="showDemoOtpEmailModal"
      title="Demo OTP Code Delivery"
      description="Experience Celery background workers and real cloud SMTP delivery by receiving your 6-digit demo login token in your personal inbox."
      @close="showDemoOtpEmailModal = false"
      @submit="handleLiveOtpEmailSubmit"
      @simulate="handleSimulateOtpEmailSubmit"
    />

  </div>

  
</template>

<script setup>
  import {ref , onMounted , onUnmounted , computed , watch} from 'vue';
  import { useRouter } from 'vue-router';
  import { useAlertStore } from '@/stores/alert';
  import { useAuthStore } from '@/stores/auth';
  import DemoEmailPromptModal from '@/components/DemoEmailPromptModal.vue';

  const router = useRouter();
  const alertStore = useAlertStore();
  const authStore = useAuthStore();

  const email = ref('');
  const password = ref('');

  const emailError = ref('');

  const forgotModalActive = ref(false)
  const otpStep = ref(1)
  const forgotEmail = ref('')
  const forgotOTP = ref('')
  const isProcessing = ref(false)

  // Timer state
  const TIME_LIMIT = 300; // 5 minutes in seconds
  const timeLeft = ref(TIME_LIMIT);
  let timerInterval = null;

  const formattedTime = computed(() => {
  const minutes = Math.floor(timeLeft.value / 60);
  const seconds = timeLeft.value % 60;
  return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  });

  const isExpired = computed(() => timeLeft.value === 0);

  const stopTimer = () => {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
  };

  // Timer function
  const startTimer = () => {
  stopTimer(); // Always clear any existing interval first to prevent double-counting
  timeLeft.value = TIME_LIMIT; // Reset the clock to 5:00
  
  timerInterval = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--;
      } else {
        stopTimer(); // Stop counting at 0
      }
    }, 1000);
  };  

  watch([forgotModalActive, otpStep], ([isModalActive, currentStep]) => {
  // Only start the timer if the modal is OPEN and they are on STEP 2
  if (isModalActive && currentStep === 2) {
    startTimer(); 
  } else {
    // If the modal closes OR they change steps, kill the timer
    stopTimer();
  }
  });

  function validateEmail() {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email.value)) {
      emailError.value = 'Please enter a valid email address.';
      return false;
    } else { 
        emailError.value = '';
        return true;
    }
  }
  
  async function handleLogin() {
    if (!validateEmail()) {
      alertStore.showAlert('Please enter a valid email address.', 'danger');
      return;
    }
    
    if (password.value === '') {
      alertStore.showAlert('Please enter your password.', 'danger');
      return;
    }
    
    const user = {
      email: email.value,
      password: password.value
    }

    const response = await fetch("http://127.0.0.1:5000/api/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(user)
    })

    if(!response.ok) {
      const errorData = await response.json();
      alertStore.showAlert(`${errorData.message}`, 'danger')
      return;
    } else {
      const responseData = await response.json();

      authStore.loginUser(responseData);


      alertStore.showAlert(`Login successful! Welcome, ${responseData.role}`, 'success');
      
      if (responseData.role === 'admin') {
        router.push('/portal/admin/dashboard')
      } else if (responseData.role === 'trek_staff') {
        router.push('/portal/trek_staff/dashboard')
      } else {
        router.push('/portal/trekker/dashboard')
      }

    }
  }

  const isDemoLoading = ref(false)
  const activeDemoRole = ref('')

  async function handleDemoLogin(role) {
    isDemoLoading.value = true
    activeDemoRole.value = role
    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:5000'
    try {
      const response = await fetch(`${BACKEND_URL}/api/auth/demo-login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ role })
      })

      if (!response.ok) {
        const err = await response.json()
        alertStore.showAlert(err.message || 'Demo access auto-reseed failed.', 'danger')
        return
      }

      const data = await response.json()
      authStore.loginUser(data)
      alertStore.showAlert(data.message || `Demo access granted as ${role}!`, 'success')

      if (data.role === 'admin') {
        router.push('/portal/admin/dashboard')
      } else if (data.role === 'trek_staff') {
        router.push('/portal/trek_staff/dashboard')
      } else {
        router.push('/portal/trekker/dashboard')
      }
    } catch (error) {
      alertStore.showAlert(`Demo server connection error: ${error.message}`, 'danger')
    } finally {
      isDemoLoading.value = false
      activeDemoRole.value = ''
    }
  }

  function openForgotModal() {
  forgotEmail.value = ''
  forgotOTP.value = ''
  otpStep.value = 1
  forgotModalActive.value = true
  }

  function closeForgotModal() {
    forgotModalActive.value = false
  }

  const showDemoOtpEmailModal = ref(false)

  function requestLoginOTP() {
    if (forgotEmail.value.toLowerCase().includes('demo')) {
      showDemoOtpEmailModal.value = true
      return
    }
    executeRequestLoginOTP(null)
  }

  function handleLiveOtpEmailSubmit(email) {
    showDemoOtpEmailModal.value = false
    executeRequestLoginOTP(email)
  }

  function handleSimulateOtpEmailSubmit() {
    showDemoOtpEmailModal.value = false
    executeRequestLoginOTP(null)
  }

  async function executeRequestLoginOTP(demoDeliveryEmail = null) {
    isProcessing.value = true
    try {
      const payload = { email: forgotEmail.value }
      if (demoDeliveryEmail) {
        payload.demo_delivery_email = demoDeliveryEmail
      }
      const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/auth/request-login-otp`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      const data = await res.json()
      if (res.ok) {
        alertStore.showAlert(data.message, 'success')
        otpStep.value = 2 // Move to verification step
      } else {
        alertStore.showAlert(data.message, 'danger')
      }
    } catch (err) {
      alertStore.showAlert('Network configuration error.', 'danger')
    } finally {
      isProcessing.value = false
    }
  }

  async function verifyLoginOTP() {
    isProcessing.value = true
    try {
      const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/auth/verify-login-otp`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: forgotEmail.value, otp: forgotOTP.value })
      })
      const data = await res.json()
      if (res.ok) {
        alertStore.showAlert('Authorization accepted.', 'success')
        authStore.loginUser(data)
        closeForgotModal()
        
        // Route based on role
        if (data.role === 'admin') router.push('/portal/admin/dashboard')
        else if (data.role === 'trek_staff') router.push('/portal/trek_staff/dashboard')
        else router.push('/portal/trekker/dashboard')
      } else {
        alertStore.showAlert(data.message || 'Invalid token.', 'danger')
      }
    } catch (err) {
      alertStore.showAlert('Network configuration error.', 'danger')
    } finally {
      isProcessing.value = false
    }
  }

  onUnmounted(() => {
  stopTimer();
  });

</script>

<style scoped>

.public-bg-wrapper {
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(
      rgba(5, 12, 8, 0.587), 
      rgba(5, 12, 8, 0.748)
    ), 
    url('@/assets/bg.jpeg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
  z-index: 10;
  box-sizing: border-box;
}

/* Elegant Floating Return Anchor */
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


.glass-login-card {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(25px) !important;
  -webkit-backdrop-filter: blur(25px) !important;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
  border-radius: 24px;
  width: 100%;
  max-width: 460px;
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
  max-width: 360px;
  margin: 0 auto;
}

/* Custom Field Mechanics */
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

.input-field-wrapper {
  background: rgba(255, 255, 255, 0.1);
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

.field-icon {
  font-size: 0.95rem;
  margin-right: 10px;
  opacity: 1;
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

/* Action Links & Helper Styling */
p.helper-link {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
  text-decoration: underline;
  cursor: pointer;
}
.helper-link, .action-link {
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.82rem;
  text-decoration: none;
  transition: color 0.2s ease;
}
.helper-link:hover, .action-link:hover {
  color: #ffffff;
  text-decoration: underline;
}

/* High Contrast Solid Submit Button */
.btn-auth-submit {
  color: #0b1f15; /* Deep contrast dark-forest green font color */
  border: none;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  transition: background-color 0.2s ease, transform 0.1s ease;
}
.btn-auth-submit:hover {
  background-color: #0b6f304c; /* Soft tint white shift */
  transform: translateY(-1px);
}
.btn-auth-submit:active {
  transform: scale(0.99);
}

/* Aesthetic Dividers */
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
  background: rgba(100, 130, 110, 0.25); /* Approximate color tint to blend out line */
  backdrop-filter: blur(10px);
  padding: 0 12px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.78rem;
  border-radius: 12px;
}

.switch-auth-text {
  color: rgba(255, 255, 255, 0.75);
  font-size: 0.88rem;
}

.login-overlay-backdrop { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(1, 4, 2, 0.6); backdrop-filter: blur(5px); z-index: 999; }
.glass-modal-card { background: rgba(2, 7, 4, 0.422) !important; backdrop-filter: blur(15px); width: 100%; max-width: 650px; }
.max-vh-90 { max-height: 90vh; }

.btn-close-modal { position: absolute; top: 0.25rem; right: 0.5rem; background: transparent; border: none; color: rgba(255,255,255,0.5); font-size: 1.3rem; cursor: pointer; }
.btn-close-modal:hover { color: white; }
.modal-input-label { font-size: 0.82rem; color: rgba(255, 255, 255, 0.6); font-weight: 500; margin-bottom: 4px; }
.modal-input-wrapper { background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 8px 12px; display: flex; align-items: center; }
.modal-clean-field { border: none; background: transparent; color: #ffffff; width: 100%; font-size: 0.92rem; outline: none; }

/* Demo Access Cluster Styling */
.demo-access-cluster {
  text-align: left;
}
.btn-demo-access {
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.16);
  backdrop-filter: blur(8px);
  transition: all 0.2s ease;
  cursor: pointer;
}
.btn-demo-access:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.14);
  transform: translateY(-1px);
}
.btn-demo-admin:hover:not(:disabled) {
  border-color: rgba(220, 53, 69, 0.6) !important;
}
.btn-demo-staff:hover:not(:disabled) {
  border-color: rgba(255, 193, 7, 0.6) !important;
}
.btn-demo-trekker:hover:not(:disabled) {
  border-color: rgba(25, 135, 84, 0.6) !important;
}
.demo-icon {
  font-size: 1.25rem;
}
</style>