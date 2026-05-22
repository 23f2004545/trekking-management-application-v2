<template>
  <div class="landing-viewport w-100 min-vh-100 d-flex flex-column justify-content-between p-3">
    
    <header class="custom-header w-100 px-4 pt-2">
      <div class="nav-container">
        
        <div class="logo-zone">
          <a @click.prevent="$router.push('/')" class="brand-logo" href="#">
            <span class="logo-wrapper">
              <img src="@/assets/logo.png" alt="Apex Logo" height="62px" class="apex-brand-img"/>
            </span>
          </a>
        </div>
        
        <nav class="center-glass-nav">
          <ul class="nav-links-list">
            <li><a href="#" class="nav-item-link ">Explore</a></li>
            <li><a href="#" class="nav-item-link">Difficulty</a></li>
            <li><a href="#" class="nav-item-link">Safety</a></li>
            <li><a href="#" class="nav-item-link">Community</a></li>
          </ul>
        </nav>

        <div class="action-zone ">
          <button @click="$router.push('/login')" class="btn-get-started-glass" type="button">
            Get Started
          </button>
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

    <footer class="clean-footer">
      © 2026 PATHFINDER PORTAL. TAILORED FOR WILDERNESS CODES & CLEAR PATHWAYS.
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
.landing-viewport {
  position: relative;
  z-index: 10;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-sizing: border-box;
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
  height: 62px;
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
  height: 62px;
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
.clean-footer {
  text-align: center;
  padding: 15px 0;
  font-size: 0.75rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.5);
  letter-spacing: 0.5px;
}
</style>