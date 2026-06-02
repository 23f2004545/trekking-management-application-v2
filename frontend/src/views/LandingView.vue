<template>
  <div class="public-bg-wrapper w-100 min-vh-100 d-flex flex-column justify-content-between p-3">
    
    <header class="custom-header w-100 px-4 pt-2">
      <div class="nav-container">
        
        <div class="logo-zone">
          <RouterLink to="/" class="brand-logo">
            <span class="logo-wrapper">
              <img src="@/assets/logo.png" alt="Apex Logo" class="apex-brand-img"/>
            </span>
          </RouterLink>
        </div>
        
        <!-- <nav class="center-glass-nav">
          <ul class="nav-links-list">
            <li><RouterLink to="/explore" class="nav-item-link">Explore</RouterLink></li>
            <li><RouterLink to="/difficulty" class="nav-item-link">Difficulty</RouterLink></li>
            <li><RouterLink to="/safety" class="nav-item-link">Safety</RouterLink></li>
            <li><RouterLink to="/community" class="nav-item-link">Community</RouterLink></li>
          </ul>
        </nav> -->

        <div class="action-zone ">
          <RouterLink to="/login" class="btn-get-started-glass" type="button">
            Get Started
          </RouterLink>
        </div>

      </div>
    </header>

    <main class="hero-center-container">
      
      <div class="badge-wrapper">
        <span class="glass-badge">
          🏔️ 15+ Scenic Seasonal Tracks Open Today
        </span>
      </div>

      <h1 class="display-headline">
        Find Your Path In A <br>Constantly Connected World
      </h1>

      <p class="descriptive-subtext">
        Mute the digital noise. Swap infinite feeds for open mountain horizons. Discover curated 
        trekking maps, live slot bookings, and verified staff coordinates engineered for clean mountain air.
      </p>

      <div class="glass-search-box">
        <div class="search-input-wrapper">
          <span class="search-icon">🔍</span>
          <input 
            type="text" 
            class="clean-input" 
            placeholder="Search paths by difficulty, duration, or location..."
          >
        </div>
        <button class="search-action-btn">
          Find My Expedition
        </button>
      </div>

    </main>

    <footer class="persistent-footer mt-auto px-3 px-md-5 pb-4">
      <div class="glass-footer-card container-fluid p-4 p-lg-5 rounded-4 border border-white border-opacity-10 shadow-lg text-white">
        
        <div class="row align-items-center justify-content-between pb-4 mb-4 border-bottom border-white border-opacity-10">
          <div class="col-lg-7 col-md-8 text-start mb-3 mb-md-0">
            <h3 class="fw-bold tracking-tight m-0 mb-1">Secure your spot on the next alpine expedition today.</h3>
            <p class="m-0 text-white-50 small">Spaces are highly restricted per seasonal route to preserve environmental stability and guide ratios.</p>
          </div>
          <div class="col-auto">
            <button @click="$router.push('/')" class="btn-footer-cta rounded-pill px-4 py-2 fw-semibold fs-8">
              Explore Open Trails →
            </button>
          </div>
        </div>

        <div class="row text-start g-4">
          
          <div class="col-lg-4 col-md-12">
            <div class="d-flex align-items-center mb-3">
              <img src="@/assets/logo.png" alt="Apex Logo" class="footer-brand-img me-2"/>
            </div>
            <p class="text-white-50 small max-w-xs lh-base">
              Mute the digital noise. Swap infinite scrolling for pristine mountain horizons. Engineered for clean air and precise tracking.
            </p>
          </div>

          <div class="col-6 col-md-3 col-lg-2 ms-lg-auto">
            <h6 class="fw-bold small tracking-wider mb-3 text-uppercase opacity-50">Main Tracks</h6>
            <ul class="list-unstyled d-flex flex-column gap-2 fs-9">
              <li><a href="#" class="footer-link">Alpine Paths</a></li>
              <li><a href="#" class="footer-link">Forest Ridges</a></li>
              <li><a href="#" class="footer-link">Glacier Passes</a></li>
              <li><a href="#" class="footer-link">Seasonal Maps</a></li>
            </ul>
          </div>

          <div class="col-6 col-md-3 col-lg-2">
            <h6 class="fw-bold small tracking-wider mb-3 text-uppercase opacity-50">Safety Desk</h6>
            <ul class="list-unstyled d-flex flex-column gap-2 fs-9">
              <li><a href="#" class="footer-link">Gear Checklist</a></li>
              <li><a href="#" class="footer-link">Weather Monitoring</a></li>
              <li><a href="#" class="footer-link">Emergency Protocols</a></li>
              <li><a href="#" class="footer-link">Medical Clearance</a></li>
            </ul>
          </div>

          <div class="col-6 col-md-3 col-lg-2">
            <h6 class="fw-bold small tracking-wider mb-3 text-uppercase opacity-50">Portal Utility</h6>
            <ul class="list-unstyled d-flex flex-column gap-2 fs-9">
              <li><a href="#" class="footer-link">My Basecamp</a></li>
              <li><a href="#" class="footer-link">Staff Directories</a></li>
              <li><a href="#" class="footer-link">System Metrics</a></li>
              <li><a href="#" class="footer-link">Route Licensing</a></li>
            </ul>
          </div>

        </div>

        <div class="row align-items-center justify-content-between pt-4 mt-4 border-top border-white border-opacity-10 fs-9 text-white-50">
          <div class="col-auto">
            <span>© 2026 APEX APP SYSTEMS. DESIGNED FOR WILDERNESS OPERATIONS & CODES.</span>
          </div>
          <div class="col-auto d-flex gap-3 fs-7">
            <a href="#" class="text-white-50 hover-white text-decoration-none"><i class="bi bi-facebook"></i></a>
            <a href="#" class="text-white-50 hover-white text-decoration-none"><i class="bi bi-instagram"></i></a>
            <a href="#" class="text-white-50 hover-white text-decoration-none"><i class="bi bi-twitter"></i></a>
          </div>
        </div>

      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'LandingView'
}
</script>

<style scoped>
/* ==========================================================================
   1. STRUCTURAL BREAKDOWN LAYOUTS
   ========================================================================== */

.public-bg-wrapper {
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(
      rgba(0, 0, 0, 0.15), 
      rgba(0, 0, 0, 0.3)
    ), 
    url('@/assets/bg.jpeg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;

}

.custom-header {
  max-width: 1400px;
  margin: 0 auto;
}

.nav-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.logo-zone, .action-zone {
  flex: 1;
  display: flex;
  align-content: end;
}
.action-zone {
  display: flex;
  justify-content: flex-end;
}

/* ==========================================================================
   2. GLASSMORPHISM NAVBAR 
   ========================================================================== */
.center-glass-nav {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(10px) !important;
  /* -webkit-backdrop-filter: blur(16px) !important; */
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 24px 0 rgba(0, 0, 0, 0.04);
  padding: 4px 10px;
  border-radius: 50px;
}

.nav-links-list {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 4px;
  align-items: center;
}

/* .brand-logo {
  font-weight: 700;
  color: #ffffff;
  text-decoration: none;
  font-size: 1.35rem;
  letter-spacing: -0.5px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
} */

.brand-logo {
  display: inline-flex;
  align-items: center;
  cursor: pointer;
  text-decoration: none;
}

.logo-wrapper {
  position: relative;
  overflow: hidden;
  display: inline-block;
  border-radius: 8px;
  height: 3rem;
}

/* The elegant shimmer overlay passing across your PNG logo */
.logo-wrapper::after {
  content: '';
  position: absolute;
  top: 0;
  left: -150%;
  width: 50%;
  height: 100%;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.4) 50%,
    rgba(255, 255, 255, 0) 100%
  );
  transform: skewX(-20deg);
  animation: logo-shimmer 4.5s infinite ease-in-out;
}

.apex-brand-img {
  height: 3rem;
  display: block;
  object-fit: contain;
}

@keyframes logo-shimmer {
  0% { left: -150%; }
  30% { left: 150%; }
  100% { left: 150%; }
}

.nav-item-link {
  text-decoration: none;
  font-size: 0.88rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.8);
  padding: 5px 14px;
  display: inline-block;
  transition: all 0.25s ease;
}

.nav-item-link.active {
  color: #ffffff !important;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(4px);
  border-radius: 30px;
}

.nav-item-link:hover:not(.active) {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 30px;
}

/* ==========================================================================
   3. GET STARTED GLASS BUTTON
   ========================================================================== */
.btn-get-started-glass {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.4);
  font-size: 0.88rem;
  font-weight: 600;
  text-decoration: none;
  border-radius: 30px;
  padding: 8px 20px;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-get-started-glass:hover {
  background: rgba(118, 191, 119, 0.501); /* Semi-transparent green background */
  border-color: #679e84;                          /* Bright green boundary frame */
  box-shadow: 0 4px 20px rgba(25, 135, 84, 0.25);
  transform: translateY(-1px);
}

/* ==========================================================================
   4. HERO SEGMENT 
   ========================================================================== */
.hero-center-container {
  text-align: center;
  margin: auto 0;
  padding: 20px 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.badge-wrapper {
  margin-bottom: 16px;
}

.glass-badge {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 6px 14px;
  border-radius: 30px;
  color: #ffffff;
  font-weight: 500;
  font-size: 0.8rem;
  letter-spacing: 0.3px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.display-headline {
  font-size: 3.2rem;
  font-weight: 800;
  line-height: 1.15;
  letter-spacing: -1.2px;
  margin-bottom: 16px;
  color: #ffffff;
  text-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
}

.descriptive-subtext {
  font-size: 1.05rem;
  color: rgba(255, 255, 255, 0.9);
  max-width: 600px;
  line-height: 1.6;
  margin: 0 auto 32px auto;
  font-weight: 400;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

/* ==========================================================================
   5. COMPACT GLASS SEARCH BAR 
   ========================================================================== */
.glass-search-box {
  background: rgba(255, 255, 255, 0.15) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(255, 255, 255, 0.35);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
  padding: 5px 6px 5px 16px; /* Reduced padding for ultra-slim profile */
  border-radius: 50px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 580px; /* Reduced max width to make it compact */
  width: 100%;
  box-sizing: border-box;
}

.search-input-wrapper {
  display: flex;
  align-items: center;
  width: 100%;
}

.search-icon {
  font-size: 1rem;
  margin-right: 8px;
  color: #ffffff;
  opacity: 1;
}

.clean-input {
  border: none;
  background: transparent;
  width: 100%;
  font-size: 0.92rem;
  color: #ffffff;
  outline: none;
}

.clean-input::placeholder {
  color: rgba(255, 255, 255, 0.75);
}

.search-action-btn {
  background: rgba(0, 0, 0, 0.15);
  color: white;
  border: none;
  padding: 10px 22px; /* Smaller, modern button padding */
  font-size: 0.9rem;
  font-weight: 600;
  border-radius: 30px;
  cursor: pointer;
  white-space: nowrap;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.search-action-btn:hover {
  background-color: rgba(118, 191, 119, 0.501);
  transform: scale(1.02);
}

/* Footer layout anchoring */
.glass-footer-card {
  background: rgba(255, 255, 255, 0.05) !important;
  backdrop-filter: blur(25px) !important;
  -webkit-backdrop-filter: blur(25px) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
}

.footer-brand-img {
  height: 38px;
  object-fit: contain;
}

.btn-footer-cta {
  background: #ffffff;
  color: #0b1f15;
  border: none;
  transition: all 0.25s ease;
}
.btn-footer-cta:hover {
  background: #e8f5e9;
  transform: translateY(-1px);
}

.footer-link {
  color: rgba(255, 255, 255, 0.65);
  text-decoration: none;
  transition: color 0.2s ease;
}
.footer-link:hover {
  color: #ffffff;
}

.hover-white:hover { color: #ffffff !important; }
.max-w-xs { max-width: 280px; }
.tracking-wider { letter-spacing: 0.8px; }
</style>