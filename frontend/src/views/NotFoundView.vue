<template>
  <div class="lost-trail-viewport w-100 min-vh-100 d-flex flex-column align-items-center justify-content-center p-3 text-center">
    
    <h1 class="display-huge-404 fw-black m-0 tracking-tighter animate-fade-in">
      404
    </h1>

    <div class="glass-message-capsule p-4 mt-n4 rounded-4 border border-white border-opacity-10 shadow animate-slide-up">
      <h2 class="path-error-title mb-2">Base Camp Not Found</h2>
      <p class="path-error-text mx-auto mb-0">
        Oops ! It seems you've veered off the established coordinates. The path you sought has shifted, but your journey doesn't end here.
      </p>
    </div>

    <div class="mt-4 animate-slide-up delay-1">
      <button @click="$router.push('/')" class="btn-retrace-glass d-flex align-items-center gap-2 px-4 py-2.5 rounded-pill fs-7 fw-semibold">
        Reroute <span class="arrow-icon">→</span>
      </button>
    </div>

  </div>
</template>

<script>
export default {
  name: 'NotFoundView'
}
</script>

<style scoped>
/* Immersive Viewport Layer utilizing your 404-bg image asset */
.lost-trail-viewport {
  position: relative;
  z-index: 10;
  background: 
    linear-gradient(180deg, rgba(127, 149, 135, 0.4) 0%, rgba(1, 6, 3, 0.86) 100%), 
    url('@/assets/404-bg.jpg'); /* Dynamically maps to your background file */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  overflow: hidden;
  box-sizing: border-box;
}

/* Giant Uncontained Typography Configuration */
.display-huge-404 {
  font-size: clamp( 20rem, 16vw, 13rem); /* Responsive fluid sizing */
  font-weight: 1200;
  color: rgba(3, 45, 25, 0.638); /* Subtle metallic gradient */
  letter-spacing: 0.1rem;
  line-height: 0.9;
  /* Premium metallic/ambient overlay text reflection shadow */
  text-shadow: 0 10px 40px rgba(0, 0, 0, 0.45), 0 0 80px rgba(255, 255, 255, 0.08);
}

/* Compensate space to pull content up into the giant number slightly */
.mt-n4 {
  margin-top: -3.9rem !important;
}

/* Ultra-Slim Glass message container holding text details */
.glass-message-capsule {
  background: rgba(255, 255, 255, 0.05) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  max-width: 40rem;
  width: 92%;
}

.path-error-title {
  color: #ffffff;
  font-size: 1.4rem;
  font-weight: 600;
  letter-spacing: -0.3px;
}

.path-error-text {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.88rem;
  line-height: 1.6;
  font-weight: 400;
}

/* The Sleek Minimalistic Floating Glass Return Button */
.btn-retrace-glass {
  background: rgba(255, 255, 255, 0.12) !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  color: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  height: 3.5rem ;
}

.btn-retrace-glass:hover {
  background: rgba(255, 255, 255, 0.22) !important;
  border-color: rgba(255, 255, 255, 0.35);
  color: #ffffff;
  transform: translateY(-1px);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.2);
}

.arrow-icon {
  transition: transform 0.2s ease;
}
.btn-retrace-glass:hover .arrow-icon {
  transform: translateX(3px); /* Subtle interactive nudge animation */
}

/* Elegant UI Transition Fade In Keyframes */
.animate-fade-in {
  animation: fadeIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

.animate-slide-up {
  opacity: 0;
  animation: slideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

.delay-1 {
  animation-delay: 0.15s;
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.96); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Utilities */
.fw-black { font-weight: 900; }
.fs-7 { font-size: 0.85rem; }
</style>