<template>
  <div class="login-viewport w-100 min-vh-100 d-flex align-items-center justify-content-center p-3">
    
    <button @click="$router.push('/')" class="btn-back-home">
      ← Back to Main
    </button>

    <div class="glass-login-card p-4 p-md-5 text-center">
      
      <div class="brand-header mb-4">
        <div class="logo-accent mx-auto mb-2">🍃</div>
        <h2 class="auth-title">Welcome Back</h2>
        <p class="auth-subtitle">Sign in to access your base camp dashboards, upcoming treks, and staff logs.</p>
      </div>

      <form @submit.prevent="handleLogin" class="auth-form text-start">
        
        <div class="input-group-container mb-3">
          <label class="input-label">Email Address</label>
          <div class="input-field-wrapper">
            <span class="field-icon">✉️</span>
            <input 
              v-model="email"
              type="email" 
              required
              placeholder="name@domain.com"
              class="auth-clean-input"
              @input="validateEmail"
            >
          </div>
          <div v-if="emailError" class="input-label my-2 text-warning">
            {{ emailError }}
          </div>
        </div>

        <div class="input-group-container mb-4">
          <div class="d-flex justify-content-between align-items-center mb-1">
            <label class="input-label mb-0">Password</label>
            <RouterLink to="/forgot-password" class="helper-link">Forgot password?</RouterLink>
          </div>
          <div class="input-field-wrapper">
            <span class="field-icon">🔒</span>
            <input 
              v-model="password"
              type="password" 
              required
              placeholder="••••••••"
              class="auth-clean-input"
            >
          </div>
        </div>

        <button type="submit" class="btn-auth-submit w-100 py-3 mb-4">
          Log In
        </button>

      </form>

      <div class="divider-zone mb-4">
        <span class="divider-text">Ready for new horizons?</span>
      </div>

      <p class="switch-auth-text m-0">
        Don't have an account? 
        <RouterLink to="/register" class="action-link fw-bold">Sign Up</RouterLink>
      </p>

    </div>
  </div>
</template>

<script setup>
  import {ref} from 'vue';
  import { useRouter } from 'vue-router';
  import { showToast } from '../utils/toast'

  const router = useRouter();

  const email = ref('');
  const password = ref('');

  const emailError = ref('');

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
      showToast('Please enter a valid email address.', 'error');
      return;
    }
    
    if (email.value === '' || password.value === '') {
      showToast('Please fill in all fields.', 'error');
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
      showToast(`${errorData.message}`, 'error')
      return;
    } else {
      const responseData = await response.json();

      sessionStorage.setItem('access_token', responseData.access_token) // Short-lived (Wipes when tab closes)
      localStorage.setItem('refresh_token', responseData.refresh_token) // Long-lived (Persists across tabs)
      sessionStorage.setItem('user_role', responseData.role)


      showToast(`Login successful! Welcome, ${responseData.role}`, 'success');
      
      if (responseData.role === 'admin') {
        router.push('/admin/dashboard')
      } else if (responseData.role === 'trek_staff') {
        router.push('/staff/dashboard')
      } else {
        router.push('/trekker/dashboard')
      }

    }

  }
</script>

<style scoped>
/* Viewport Wrapper leveraging your global background layers safely */
.login-viewport {
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

/* Perfect Glassmorphic Pod Shell sizing matching your reference image structure */
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
  background-color: #ffffff;
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
</style>