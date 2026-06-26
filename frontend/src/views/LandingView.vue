<template>
  <div class="public-bg-wrapper w-100 min-vh-100 d-flex flex-column justify-content-between p-2 position-relative overflow-hidden">
    
    <header class="custom-header w-100 px-4 pt-2">
      <div class="nav-container">
        <div class="logo-zone">
          <RouterLink to="/" class="brand-logo">
            <span class="logo-wrapper"><img src="@/assets/logo.png" alt="Apex Logo" class="apex-brand-img"/></span>
          </RouterLink>
        </div>
        <div class="action-zone ">
          <RouterLink to="/login" class="btn-get-started-glass">Get Started</RouterLink>
        </div>
      </div>
    </header>

    <main class="hero-center-container mt-1 pt-5">
      <div class="badge-wrapper animate-fade-up" style="animation-delay: 0.1s;">
        <span class="glass-badge">🏔️ The Global Alpine Network</span>
      </div>
      <h1 class="display-headline animate-fade-up" style="animation-delay: 0.2s;">
        Find Your Path In A <br>Constantly Connected World
      </h1>
      <p class="descriptive-subtext animate-fade-up" style="animation-delay: 0.3s;">
        Mute the digital noise. Swap infinite feeds for open mountain horizons. Discover curated 
        trekking maps, live slot bookings, and verified staff coordinates.
      </p>
      <div class="glass-search-box animate-fade-up" style="animation-delay: 0.4s;">
        <div class="search-input-wrapper">
          <span class="search-icon"><i class="bi bi-search"></i></span>
          <input type="text" class="clean-input" placeholder="Search paths by difficulty, duration, or location...">
        </div>
        <button class="search-action-btn" @click="$router.push('/portal/trekker/treks')">Find My Expedition</button>
      </div>
    </main>

    <section class="telemetry-section container my-5 pt-5">
      <div class="row g-4 justify-content-center text-center">
        <div class="col-6 col-lg-3">
          <div class="metric-block">
            <h2 class="display-5 fw-black text-white m-0 tracking-tighter">{{ metrics.highest_peak }}<span class="fs-4 text-white-50">M</span></h2>
            <p class="text-white-50 text-uppercase tracking-wider fs-9 fw-semibold mt-2">Highest Peak Conquered</p>
          </div>
        </div>
        <div class="col-6 col-lg-3">
          <div class="metric-block border-start border-white border-opacity-10 px-lg-3">
            <h2 class="display-5 fw-black text-success-tint m-0 tracking-tighter">{{ metrics.successful_participants }}+</h2>
            <p class="text-white-50 text-uppercase tracking-wider fs-9 fw-semibold mt-2">Explorers Guided</p>
          </div>
        </div>
        <div class="col-6 col-lg-3">
          <div class="metric-block border-start border-white border-opacity-10 px-lg-3">
            <h2 class="display-5 fw-black text-white m-0 tracking-tighter">{{ metrics.treks_deployed }}+</h2>
            <p class="text-white-50 text-uppercase tracking-wider fs-9 fw-semibold mt-2">Trails Completed</p>
          </div>
        </div>
        <div class="col-6 col-lg-3">
          <div class="metric-block border-start border-white border-opacity-10 px-lg-3">
            <h2 class="display-5 fw-black text-white m-0 tracking-tighter">{{ metrics.total_staff }}+</h2>
            <p class="text-white-50 text-uppercase tracking-wider fs-9 fw-semibold mt-2">Verified Guides</p>
          </div>
        </div>
      </div>
    </section>

    <section class="reviews-section container-fluid px-0 my-3 py-4">
      <div class="container mb-5 text-center">
        <span class="badge border border-white border-opacity-20 rounded-pill px-3 py-2 fs-9 text-white-50 mb-3">WHAT EXPLORERS SAY</span>
        <h2 class="fw-bold tracking-tight text-white display-6">Don't take our word for it.</h2>
        
        <div class="d-inline-flex align-items-center gap-3 mt-4 glass-rating-pill px-4 py-2 rounded-pill shadow-sm border border-success border-opacity-25">
          <span class="fs-4 text-warning">{{ '★'.repeat(averageRating) }}{{ '☆'.repeat(5 - averageRating) }}</span>
          <div class="text-start border-start border-white border-opacity-25 ps-3">
            <h4 class="m-0 fw-black text-white lh-1">{{ averageRating }} <span class="fs-6 text-white-50 fw-normal">/ 5.0</span></h4>
            <span class="fs-9 text-success-tint uppercase tracking-wider">Overall Platform Rating</span>
          </div>
        </div>
      </div>

      <div class="marquee-container">
        <div class="marquee-track">
          <div v-for="(review, index) in finalReviews" :key="'A'+index" class="review-glass-card">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <h6 class="fw-bold text-white m-0">{{ review.author }}</h6>
              <span class="text-warning text-nowrap fs-8">{{ '★'.repeat(review.rating) }}{{ '☆'.repeat(5 - review.rating) }}</span>
            </div>
            <p class="text-white-50 fs-8 lh-base m-0 italic">"{{ review.comment }}"</p>
          </div>
          <div v-for="(review, index) in finalReviews" :key="'B'+index" class="review-glass-card">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <h6 class="fw-bold text-white m-0">{{ review.author }}</h6>
              <span class="text-warning text-nowrap fs-8">{{ '★'.repeat(review.rating) }}{{ '☆'.repeat(5 - review.rating) }}</span>
            </div>
            <p class="text-white-50 fs-8 lh-base m-0 italic edit-text">"{{ review.comment }}"</p>
          </div>
        </div>
      </div>
    </section>

    <section class="story-section container-fluid px-0 my-3 py-4">
      <div class="container mb-4 text-start">
        <span class="badge border border-white border-opacity-20 rounded-pill px-3 py-1.5 fs-9 text-white-50 mb-3">THE APEX DOCTRINE</span>
        <h2 class="fw-bold tracking-tight text-white display-6 max-w-lg">Engineered for those who seek the silence above the tree line.</h2>
      </div>
      
      <!-- Horizontal Snapping Scroll Array -->
      <div class="horizontal-scroll-wrapper px-4 px-md-5 pb-4">
        
        <div class="story-glass-card">
          <div class="story-icon text-danger-tint mb-3"><i class="bi bi-phone-vibrate"></i></div>
          <h4 class="fw-bold text-white mb-2">The Digital Fatigue</h4>
          <p class="text-white-50 fs-8 lh-base m-0">The modern world demands constant connectivity. Endless notifications, algorithmic feeds, and urban gridlock drain human vitality. We built Apex as the ultimate override protocol.</p>
        </div>

        <div class="story-glass-card">
          <div class="story-icon text-warning mb-3"><i class="bi bi-compass"></i></div>
          <h4 class="fw-bold text-white mb-2">Curated Wilderness</h4>
          <p class="text-white-50 fs-8 lh-base m-0">We don't just list trails. We strictly audit mountain coordinates, monitor seasonal weather telemetry, and cap participant slots to preserve environmental purity.</p>
        </div>

        <div class="story-glass-card">
          <div class="story-icon text-success-tint mb-3"><i class="bi bi-shield-check"></i></div>
          <h4 class="fw-bold text-white mb-2">Verified Operations</h4>
          <p class="text-white-50 fs-8 lh-base m-0">Every route is commanded by ABVIMAS-certified field staff. Integrated medical forms and real-time backend logistics ensure your safety is mathematically calculated.</p>
        </div>

        <div class="story-glass-card border-success border-opacity-25 bg-success bg-opacity-10">
          <div class="story-icon text-white mb-3"><i class="bi bi-cursor-fill"></i></div>
          <h4 class="fw-bold text-white mb-2">Your Next Move</h4>
          <p class="text-white-50 fs-8 lh-base mb-4">The alpine grids are open. Your clearance is pending. It is time to secure your base authorization codes.</p>
          <button @click="$router.push('/login')" class="btn btn-success rounded-pill px-4 py-2 fs-9 fw-bold text-dark w-100 shadow-sm">Initialize Setup →</button>
        </div>

      </div>
    </section>

    <section ref="commandDeskRef" class="command-showcase-section container my-3 py-5 text-start transition-scroll" >
      
      <div class="glass-command-card p-4 p-lg-5 rounded-4 border border-white border-opacity-10 position-relative overflow-hidden shadow-lg" style="background: rgba(10, 15, 12, 0.6); backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px);">
        
        <div class="position-absolute top-0 end-0 bg-success bg-opacity-20 rounded-circle blur-orb" style="width: 400px; height: 400px; filter: blur(100px); pointer-events: none; transform: translate(20%, -20%);"></div>

        <div class="row g-5 align-items-center position-relative z-1">
          
          <div class="col-lg-5 pe-lg-4">
            <span class="badge border border-white border-opacity-20 rounded-pill px-3 py-1.5 fs-9 text-white-50 tracking-widest uppercase mb-3">
              <i class="bi bi-shield-check me-1 text-success-tint"></i> THE OVERRIDE PROTOCOL
            </span>
            <h2 class="display-6 fw-bold text-white tracking-tight m-0 mb-3">
              Direct Uplink to <br><span style="color: #7bf1a8;">Central Command.</span>
            </h2>
            <p class="text-white-50 fs-8 lh-base mb-4 italic">
              True alpine safety requires human accountability. Whether facing a medical inquiry or requesting a guide itinerary override, our ABVIMAS-certified command operators intercept and resolve your transmission personally.
            </p>
            
            <div class="d-flex align-items-center gap-3 bg-opacity-5 p-3 rounded-4 border border-white border-opacity-50 w-fit">
              <div class="bg-success bg-opacity-20 text-success-tint rounded-circle d-flex align-items-center justify-content-center flex-shrink-0" style="width: 40px; height: 40px;">
                <i class="bi bi-envelope-paper-fill fs-6"></i>
              </div>
              <div>
                <strong class="d-block text-white fs-9 tracking-wider uppercase">Sealed Directives</strong>
                <span class="text-white-50 fs-9">Immutable audit trails for every query.</span>
              </div>
            </div>
          </div>

          <div class="col-lg-7">
            <div class="d-flex flex-column gap-3">
              
              <div class="step-glass-card p-4 rounded-4 border border-white border-opacity-5 d-flex gap-3 align-items-start" style="background: rgba(255,255,255,0.02);">
                <div class="step-num text-white-50 border border-white border-opacity-20 rounded-circle d-flex align-items-center justify-content-center fw-bold fs-9 flex-shrink-0" style="width: 32px; height: 32px;">01</div>
                <div>
                  <h6 class="fw-bold text-white mb-1 tracking-tight">Transmit Hazard or Inquiry</h6>
                  <p class="text-white-50 fs-9 m-0 lh-base">Trigger a high-priority dispatch vector detailing operational roadblocks directly from your portal HUD.</p>
                </div>
              </div>

              <div class="step-glass-card p-4 rounded-4 border border-success border-opacity-25 d-flex gap-3 align-items-start ms-lg-4 shadow-lg" style="background: rgba(123, 241, 168, 0.05);">
                <div class="step-num bg-success bg-opacity-20 text-success-tint border border-success border-opacity-25 rounded-circle d-flex align-items-center justify-content-center fw-bold fs-9 flex-shrink-0 shadow" style="width: 32px; height: 32px;">02</div>
                <div>
                  <h6 class="fw-bold text-white mb-1 tracking-tight">Human Operator Triage</h6>
                  <p class="text-white-50 fs-9 m-0 lh-base">Central Command triages transmissions instantly. Field hazard reports bypass routine inquiries for immediate executive review.</p>
                </div>
              </div>

              <div class="step-glass-card p-4 rounded-4 border border-white border-opacity-5 d-flex gap-3 align-items-start ms-lg-5" style="background: rgba(255,255,255,0.02);">
                <div class="step-num text-white-50 border border-white border-opacity-20 rounded-circle d-flex align-items-center justify-content-center fw-bold fs-9 flex-shrink-0" style="width: 32px; height: 32px;">03</div>
                <div>
                  <h6 class="fw-bold text-white mb-1 tracking-tight">Cryptographic Resolution</h6>
                  <p class="text-white-50 fs-9 m-0 lh-base">An un-alterable command directive is transmitted to your registered email alongside a platform telemetry alert.</p>
                </div>
              </div>

            </div>
          </div>

        </div>
      </div>
    </section>
    
    <section class="architecture-section container my-3 py-5 text-center">
      <div class="row g-4">
        <div class="col-lg-4">
          <div class="pillar-card p-4 p-md-5 rounded-4 h-100">
            <i class="bi bi-heart-pulse text-white opacity-50 display-5 mb-3 d-block"></i>
            <h5 class="fw-bold text-white tracking-tight">Safety Telemetry</h5>
            <p class="text-white-50 fs-9 m-0 mt-2">Direct linkage of explorer physical profiles to emergency medical matrices before basecamp arrival.</p>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="pillar-card p-4 p-md-5 rounded-4 h-100">
            <i class="bi bi-cpu text-white opacity-50 display-5 mb-3 d-block"></i>
            <h5 class="fw-bold text-white tracking-tight">Decoupled Automation</h5>
            <p class="text-white-50 fs-9 m-0 mt-2">Background caching and asynchronous data processing powered by Redis and automated Celery workers.</p>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="pillar-card p-4 p-md-5 rounded-4 h-100">
            <i class="bi bi-diagram-3 text-white opacity-50 display-5 mb-3 d-block"></i>
            <h5 class="fw-bold text-white tracking-tight">Operational Control</h5>
            <p class="text-white-50 fs-9 m-0 mt-2">Strictly sandboxed organizational domains for Administrators, Field Guide Staff, and Active Trekkers.</p>
          </div>
        </div>
      </div>
    </section>

    <footer class="persistent-footer mt-auto px-3 px-md-5 pb-4">
      <div class="glass-footer-card container-fluid p-4 p-lg-5 rounded-4 border border-white border-opacity-10 shadow-lg text-white">
        
        <div class="row align-items-center justify-content-between pb-4 mb-4 border-bottom border-white border-opacity-10">
          <div class="col-lg-7 col-md-8 text-start mb-3 mb-md-0">
            <h3 class="fw-bold tracking-tight m-0 mb-1">Secure your spot on the next alpine expedition today.</h3>
            <p class="m-0 text-white-50 small">Spaces are highly restricted per seasonal route to preserve environmental stability and guide ratios.</p>
          </div>
          <div class="col-auto">
            <button @click="$router.push(`/portal/${authStore.role}/treks`)" class="btn-footer-cta rounded-pill px-4 py-2 fw-semibold fs-8">
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

    <Transition name="fomo-slide">
      <div v-if="fomoActive" class="fomo-toast position-fixed bottom-0 end-0 m-4 p-3 rounded-4 shadow-lg border border-success border-opacity-25 d-flex gap-3 align-items-center z-index-top">
        <div class="fomo-icon bg-success bg-opacity-25 text-success rounded-circle d-flex align-items-center justify-content-center flex-shrink-0" style="width: 40px; height: 40px;">
          <i class="bi bi-lightning-charge-fill fs-5"></i>
        </div>
        <div>
          <h6 class="m-0 fw-bold text-white fs-8">Demand Alert</h6>
          <p class="m-0 text-white-50 fs-9 mt-0.5 lh-sm">{{ fomoMessage }}</p>
        </div>
        <button @click="fomoActive = false" class="btn-close-toast align-self-start ms-2">✕</button>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

// State
const metrics = ref({ highest_peak: 0, total_staff: 0, successful_participants: 0, treks_deployed: 0 })
const averageRating = ref(5.0)
const finalReviews = ref([])
const fomoTreks = ref([])

// FOMO State
const fomoActive = ref(false)
const fomoMessage = ref("")
let fomoTimer = null
const commandDeskRef = ref(null)
const isVisible = ref(false)

// Fallback dummy reviews to ensure the marquee is always full and beautiful
const fallbackReviews = [
  { author: "Vikram S.", rating: 5, comment: "The logistics were mathematically perfect. An absolutely stunning alpine crossing." },
  { author: "Priya M.", rating: 4, comment: "Challenging altitude, but the verified guide made me feel entirely secure. Highly recommended." },
  { author: "Rahul K.", rating: 5, comment: "Swapped my phone for a compass. Best decision of the year. The platform makes booking effortless." },
  { author: "Neha Sharma", rating: 5, comment: "From the medical pre-screening to the basecamp arrival, Apex handles everything professionally." },
  { author: "Amit P.", rating: 4, comment: "Incredible terrain. The thermal springs were exactly as described in the trail manifest." },
  { author: "Dr. Anjali T.", rating: 5, comment: "As a physician, I heavily appreciate their strict emergency telemetry and medical protocols." },
  { author: "Rohan D.", rating: 5, comment: "Flawless execution. The staff was highly trained and the equipment checklist was spot on." },
  { author: "Sneha V.", rating: 4, comment: "A bit steep on day two, but the pacing set by our guide ensured everyone made the summit." },
  { author: "Karan B.", rating: 5, comment: "The digital passport system is brilliant. No paperwork, just pure wilderness." },
  { author: "Maya R.", rating: 5, comment: "Breathtaking views. Apex truly provides a disconnected, premium mountain experience." }
]

async function loadLandingData() {
  try {
    const res = await fetch(`${BACKEND_URL}/api/utils/public/landing-data`) // Update with your actual blueprint prefix
    if (res.ok) {
      const data = await res.json()
      
      // Animate Metrics (Optional: you can also just assign them instantly)
      metrics.value = data.metrics
      averageRating.value = data.reviews.average
      fomoTreks.value = data.fomo_treks

      // Pad reviews if backend returned less than 10
      let fetchedReviews = data.reviews.list
      if (fetchedReviews.length < 10) {
        const needed = 10 - fetchedReviews.length
        fetchedReviews = [...fetchedReviews, ...fallbackReviews.slice(0, needed)]
      }
      finalReviews.value = fetchedReviews
    } else {
      // Fallback if backend is down
      finalReviews.value = fallbackReviews
      fomoTreks.value = ["Rohtang Pass", "Kheerganga Ridge", "Bhrigu Lake Circuit"]
    }
  } catch (err) {
    console.error("Landing API unreachable, using fallbacks.")
    finalReviews.value = fallbackReviews
    fomoTreks.value = ["Rohtang Pass", "Kheerganga Ridge", "Bhrigu Lake Circuit"]
  }
}

// FOMO Engine Logic
function triggerFomo() {
  if (fomoTreks.value.length === 0) return
  
  // Randomize data
  const randomTrek = fomoTreks.value[Math.floor(Math.random() * fomoTreks.value.length)]
  const randomSeats = Math.floor(Math.random() * 12) + 1 // 1 to 3 seats
  
  fomoMessage.value = `An explorer just secured ${randomSeats} slot(s) for ${randomTrek}. Capacities are depleting.`
  fomoActive.value = true
  
  // Hide after 6 seconds
  setTimeout(() => { fomoActive.value = false }, 6000)
}

onMounted(() => {
  loadLandingData()
  
  // Fire the first FOMO popup 5 seconds after they land on the page
  setTimeout(triggerFomo, 5000)
  
  // Then fire it every 2 minutes (120,000 milliseconds)
  fomoTimer = setInterval(triggerFomo, 120000)

})

onUnmounted(() => {
  if (fomoTimer) clearInterval(fomoTimer)
  setTimeout(() => {
    if (!commandDeskRef.value) return
    
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        isVisible.value = true
        observer.disconnect() // Stop watching once it appears
      }
    }, { threshold: 0.15 }) // Triggers when 15% of it is on screen

    observer.observe(commandDeskRef.value)
  }, 300)
})
</script>

<style scoped>

/* ==========================================================================
    STRUCTURAL BACKGROUND
   ========================================================================== */

.public-bg-wrapper {
  background: linear-gradient(rgba(5, 12, 8, 0.587), rgba(5, 12, 8, 0.748)), url('@/assets/bg.jpeg');
  background-size: cover;
  background-position: center;
  background-attachment: fixed; /* Parallax effect for the background */
}

.text-success-tint { color: #7bf1a8; }
.italic { font-style: italic; }
.tracking-tighter { letter-spacing: -2px; }
.tracking-wider { letter-spacing: 1px; }

/* ==========================================================================
    HEADER & BRANDING 
   ========================================================================== */

.custom-header { max-width: 1400px; margin: 0 auto; }
.nav-container { display: flex; align-items: center; justify-content: space-between; width: 100%; }
.logo-zone, .action-zone { flex: 1; display: flex; }
.action-zone { justify-content: flex-end; }
.logo-wrapper { position: relative; overflow: hidden; display: inline-block; border-radius: 8px; height: 3rem; }
.apex-brand-img { height: 3rem; display: block; object-fit: contain; }

.btn-get-started-glass {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(12px) !important;
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.4);
  font-size: 0.88rem; font-weight: 600; text-decoration: none;
  border-radius: 30px; padding: 8px 20px;
  transition: all 0.3s ease;
}
.btn-get-started-glass:hover {
  background: rgba(25, 135, 84, 0.4) !important;
  border-color: #7bf1a8; transform: translateY(-1px);
}

/* ==========================================================================
    HERO ZONE 
   ========================================================================== */
.hero-center-container { text-align: center; display: flex; flex-direction: column; align-items: center; }
.glass-badge {
  background: rgba(255, 255, 255, 0.08); backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2); padding: 6px 14px;
  border-radius: 30px; color: #ffffff; font-size: 0.8rem;
}
.display-headline { font-size: 4rem; font-weight: 800; line-height: 1.1; letter-spacing: -1.5px; margin-bottom: 16px; color: #ffffff; }
.descriptive-subtext { font-size: 1.1rem; color: rgba(255, 255, 255, 0.7); max-width: 600px; line-height: 1.6; margin: 0 auto 32px auto; }

.glass-search-box {
  background: rgba(255, 255, 255, 0.15) !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
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
  color: rgba(74, 198, 105, 0.499);
  border: none;
  padding: 10px 22px; 
  font-size: 0.9rem;
  font-weight: 600;
  border-radius: 30px;
  cursor: pointer;
  white-space: nowrap;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.search-action-btn:hover {
  background-color: rgb(1, 16, 2);
  transform: scale(1.02);
}

/* ==========================================================================
    INFINITE MAEQUEE AND REVIEWS 
   ========================================================================== */

.glass-rating-pill { background: rgba(25, 135, 84, 0.05); backdrop-filter: blur(10px); }
.marquee-container { width: 100vw; overflow: hidden; white-space: nowrap; position: relative; left: 50%; right: 50%; margin-left: -50vw; margin-right: -50vw; padding: 20px 0; }

.marquee-track {
  display: inline-flex;
  gap: 20px;
  animation: marquee-scroll 45s linear infinite;
  padding-left: 20px;
}
.marquee-track:hover { animation-play-state: paused; } /* Pauses when user hovers to read! */

.review-glass-card {
  min-width: 380px; max-width: 380px; height:140px; white-space: normal; /* Resets text wrap inside card */
  background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 25px;
  transition: transform 0.3s, background 0.3s;
}
.review-glass-card:hover { transform: translateY(-4px); background: rgba(255, 255, 255, 0.08); border-color: rgba(255,255,255,0.2); }

.edit-text {
  display: -webkit-box;
  line-clamp: 3;
  -webkit-line-clamp: 3; /* Max number of lines */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

@keyframes marquee-scroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(calc(-50% - 10px)); } /* Scrolls exactly halfway (since content is duplicated) */
}


/* ==========================================================================
    NEW SECTIONS (METRICS, SCROLL, PILLARS)
   ========================================================================== */
.text-success-tint { color: #7bf1a8; }
.text-danger-tint { color: #ff8787; }
.tracking-tighter { letter-spacing: -2px; }
.tracking-wider { letter-spacing: 1px; }
.max-w-lg { max-width: 800px; }

/* Horizontal Scroll specific styling */
.horizontal-scroll-wrapper {
  display: flex;
  gap: 24px;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  padding-bottom: 20px;
  /* Hide scrollbar for Chrome, Safari and Opera */
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}
.horizontal-scroll-wrapper::-webkit-scrollbar { display: none; }

.story-glass-card {
  min-width: 320px;
  max-width: 320px;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 30px;
  scroll-snap-align: start;
  transition: transform 0.3s ease, background 0.3s ease;
}
.story-glass-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.06);
}
.story-icon { font-size: 2rem; }

.pillar-card {
  background: transparent;
  border: 1px solid rgba(255,255,255,0.05);
  transition: all 0.3s ease;
}
.pillar-card:hover {
  background: rgba(255,255,255,0.02);
  border-color: rgba(255,255,255,0.1);
}

/* ==========================================================================
    FOMO TOAST NOTIFICATION
   ========================================================================== */

.fomo-toast { background: rgba(15, 23, 18, 0.95); backdrop-filter: blur(25px); max-width: 380px; z-index: 1050; }
.btn-close-toast { background: transparent; border: none; color: rgba(255,255,255,0.4); padding: 0; cursor: pointer; }
.btn-close-toast:hover { color: white; }

.fomo-slide-enter-active, .fomo-slide-leave-active { transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1); }
.fomo-slide-enter-from, .fomo-slide-leave-to { opacity: 0; transform: translateX(50px); }

/* ==========================================================================
   5. FOOTER 
   ========================================================================== */
.glass-footer-card {
  background: rgba(255, 255, 255, 0.03) !important;
  backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
}
.btn-footer-cta { background: #ffffff; color: #0b1f15; border: none; transition: all 0.25s ease; }
.btn-footer-cta:hover { background: #7bf1a8; }
.footer-link { color: rgba(255, 255, 255, 0.5); text-decoration: none; transition: color 0.2s ease; }
.footer-link:hover { color: #ffffff; }
.footer-brand-img { height: 32px; object-fit: contain; }

/* Simple entrance animations */
.animate-fade-up { animation: fadeUp 0.8s ease forwards; opacity: 0; transform: translateY(20px); }
@keyframes fadeUp { to { opacity: 1; transform: translateY(0); } }

.fs-8 { font-size: 0.88rem; }
.fs-9 { font-size: 0.78rem; }

.transition-scroll { transition: opacity 0.8s ease-out, transform 0.8s cubic-bezier(0.16, 1, 0.3, 1); }
.translate-y-up { transform: translateY(40px); }
.translate-y-0 { transform: translateY(0); }
.step-glass-card { transition: transform 0.3s ease, background 0.3s ease; }
.step-glass-card:hover { transform: translateX(5px); background: rgba(255,255,255,0.04) !important; }
.text-success-tint { color: #7bf1a8; }

</style>


<!-- <style scoped>
/* ==========================================================================
   1. STRUCTURAL BACKGROUND
   ========================================================================== */
.public-bg-wrapper {
  background: linear-gradient(rgba(5, 12, 8, 0.587), rgba(5, 12, 8, 0.748)), url('@/assets/bg.jpeg');
  background-size: cover;
  background-position: center;
  background-attachment: fixed; /* Parallax effect for the background */
}

/* ==========================================================================
   2. HEADER & BRANDING (Retained & Optimized)
   ========================================================================== */
.custom-header { max-width: 1400px; margin: 0 auto; }
.nav-container { display: flex; align-items: center; justify-content: space-between; width: 100%; }
.logo-zone, .action-zone { flex: 1; display: flex; }
.action-zone { justify-content: flex-end; }
.logo-wrapper { position: relative; overflow: hidden; display: inline-block; border-radius: 8px; height: 3rem; }
.apex-brand-img { height: 3rem; display: block; object-fit: contain; }

.btn-get-started-glass {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(12px) !important;
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.4);
  font-size: 0.88rem; font-weight: 600; text-decoration: none;
  border-radius: 30px; padding: 8px 20px;
  transition: all 0.3s ease;
}
.btn-get-started-glass:hover {
  background: rgba(25, 135, 84, 0.4) !important;
  border-color: #7bf1a8; transform: translateY(-1px);
}

/* ==========================================================================
   3. HERO ZONE 
   ========================================================================== */
.hero-center-container { text-align: center; display: flex; flex-direction: column; align-items: center; }
.glass-badge {
  background: rgba(255, 255, 255, 0.08); backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2); padding: 6px 14px;
  border-radius: 30px; color: #ffffff; font-size: 0.8rem;
}
.display-headline { font-size: 4rem; font-weight: 800; line-height: 1.1; letter-spacing: -1.5px; margin-bottom: 16px; color: #ffffff; }
.descriptive-subtext { font-size: 1.1rem; color: rgba(255, 255, 255, 0.7); max-width: 600px; line-height: 1.6; margin: 0 auto 32px auto; }

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

/* ==========================================================================
   4. NEW SECTIONS (METRICS, SCROLL, PILLARS)
   ========================================================================== */
.text-success-tint { color: #7bf1a8; }
.text-danger-tint { color: #ff8787; }
.tracking-tighter { letter-spacing: -2px; }
.tracking-wider { letter-spacing: 1px; }
.max-w-lg { max-width: 800px; }

/* Horizontal Scroll specific styling */
.horizontal-scroll-wrapper {
  display: flex;
  gap: 24px;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  padding-bottom: 20px;
  /* Hide scrollbar for Chrome, Safari and Opera */
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}
.horizontal-scroll-wrapper::-webkit-scrollbar { display: none; }

.story-glass-card {
  min-width: 320px;
  max-width: 320px;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 30px;
  scroll-snap-align: start;
  transition: transform 0.3s ease, background 0.3s ease;
}
.story-glass-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.06);
}
.story-icon { font-size: 2rem; }

.pillar-card {
  background: transparent;
  border: 1px solid rgba(255,255,255,0.05);
  transition: all 0.3s ease;
}
.pillar-card:hover {
  background: rgba(255,255,255,0.02);
  border-color: rgba(255,255,255,0.1);
}

/* ==========================================================================
   5. FOOTER 
   ========================================================================== */
.glass-footer-card {
  background: rgba(255, 255, 255, 0.03) !important;
  backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
}
.btn-footer-cta { background: #ffffff; color: #0b1f15; border: none; transition: all 0.25s ease; }
.btn-footer-cta:hover { background: #7bf1a8; }
.footer-link { color: rgba(255, 255, 255, 0.5); text-decoration: none; transition: color 0.2s ease; }
.footer-link:hover { color: #ffffff; }
.footer-brand-img { height: 32px; object-fit: contain; }

/* Simple entrance animations */
.animate-fade-up { animation: fadeUp 0.8s ease forwards; opacity: 0; transform: translateY(20px); }
@keyframes fadeUp { to { opacity: 1; transform: translateY(0); } }

.fs-8 { font-size: 0.88rem; }
.fs-9 { font-size: 0.78rem; }
</style> -->