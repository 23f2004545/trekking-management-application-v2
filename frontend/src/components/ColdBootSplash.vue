<template>
  <div>
    <!-- FULL-SCREEN INTERACTIVE COLD-BOOT & MIND-RESET EXPERIENCE -->
    <Transition name="splash-fade">
      <div
        v-if="visible"
        class="apex-boot-universe"
        @touchstart="handleTouchStart"
        @touchmove="handleTouchMove"
        @touchend="handleTouchEnd"
      >
        <!-- Full-Viewport Interactive HTML5 Canvas -->
        <canvas ref="canvasRef" class="serpent-canvas"></canvas>

        <!-- Ambient Vignette & Subtle Radial Atmosphere -->
        <div class="vignette-overlay"></div>

        <!-- ============================================================== -->
        <!-- TOP HUD: BRAND IDENTITY, EDITORIAL MISSION & SCORE TELEMETRY   -->
        <!-- ============================================================== -->
        <header class="hud-top-bar">
          <!-- Top-Left: Brand & Control Mode -->
          <div class="hud-top-left">
            <div class="brand-cluster">
              <div>
                <div class="d-flex flex-wrap align-items-center gap-2">
                  <span class="mode-badge font-monospace" :class="isManualControl ? 'mode-manual' : 'mode-auto'">
                    {{ isManualControl ? 'MANUAL HELM' : 'AUTO-PILOT' }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Top-Center: Core Mission Statement & Live Antidote Feed -->
          <div class="hud-top-center text-center mt-2">
            <div class="mission-eyebrow font-monospace">
              <i class="bi bi-compass me-1"></i>MENTAL RESET PROTOCOL
            </div>
            <h1 class="mission-headline">
              Mute the Digital Noise. Consume Your Worries.
            </h1>

          </div>

          <!-- Top-Right: Game Score & Elevation Telemetry -->
          <div class="hud-top-right font-monospace">
            <div class="score-box">
              <span class="score-label">WORRIES CONSUMED</span>
              <span class="score-value text-emerald">{{ String(score).padStart(2, '0') }}</span>
            </div>
          </div>
        </header>


        <!-- ============================================================== -->
        <!-- BOTTOM HUD: CORNERS ON DESKTOP, COMPACT FOOTER ON MOBILE       -->
        <!-- ============================================================== -->
        <footer class="hud-bottom-bar">
          <!-- Bottom-Left: Patient Boot Message & Live Server Stage -->
          <div class="hud-bottom-left">
            <div class="d-flex align-items-center gap-2 mb-1">
              <span class="beacon-dot" :class="{ 'beacon-ready': isWarmedEarly }"></span>
              <span class="boot-status-title">
                {{ isWarmedEarly ? 'Basecamp Telemetry Connected · Preparing Portal' : 'Waking Alpine Infrastructure · Please Be Patient' }}
              </span>
            </div>
            <div class="boot-status-sub font-monospace">
              <i class="bi bi-broadcast me-1 text-emerald"></i>
              <span>{{ currentStage.label }} — {{ currentStage.log }}</span>
            </div>
          </div>

          <!-- Bottom-Right: Progress Bar & Percentage -->
          <div class="hud-bottom-right font-monospace">
            <div class="d-flex align-items-baseline justify-content-between gap-3 mb-1">
              <span class="progress-tag">
                {{ isHoldMode ? 'SANDBOX HOLD MODE' : (isWarmedEarly ? 'HANDSHAKE VERIFIED' : 'ESTABLISHING UPLINK') }}
              </span>
              <div class="progress-numbers">
                <span class="progress-int">{{ Math.floor(progress) }}</span>
                <span class="progress-pct">%</span>
              </div>
            </div>
            <div class="progress-rail">
              <div class="progress-bar-fill" :style="{ width: `${progress}%` }">
                <div class="progress-spark"></div>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </Transition>

    <!-- ============================================================== -->
    <!-- FLOATING REPLAY / TEST TRIGGER (For local testing convenience) -->
    <!-- Audit: Set ENABLE_LOCAL_TEST_BUTTON = false for production     -->
    <!-- ============================================================== -->
    <div v-if="!visible && showDevTestButton" class="local-test-launcher">
      <button
        type="button"
        @click="launchLocalTestSandbox"
        class="btn-launch-sandbox font-monospace shadow-lg"
        title="Launch Cold-Boot Screen in Hold Mode for Local Testing"
      >
        <i class="bi bi-joystick me-1.5 text-emerald"></i>
        <span>Test Boot Screen</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// ============================================================================
// 🛠 LOCAL TESTING / PRODUCTION AUDIT TOGGLE
// ----------------------------------------------------------------------------
// Set `ENABLE_LOCAL_TEST_BUTTON = true` to show the "Local Test: Hold Boot"
// button inside the loading screen and the "Test Boot Screen" launcher button
// on the Landing Page (since local backend boots in milliseconds).
//
// Audit back to `false` before final production commit if you want zero test
// buttons visible anywhere.
// ============================================================================
const ENABLE_LOCAL_TEST_BUTTON = false

const props = defineProps({
  backendUrl: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['finish'])

const showDevTestButton = computed(() => ENABLE_LOCAL_TEST_BUTTON)

// Core Boot & Visibility State
const visible = ref(true)
const progress = ref(1)
const isWarmedEarly = ref(false)
const isHoldMode = ref(false)

let progressInterval = null
let pingTimeoutId = null
let bootStartTime = 0
let isUnmounted = false

// Minimum showcase time (ms) on initial visit so local boot doesn't vanish in 50ms
const MIN_BOOT_DISPLAY_MS = 4200

const statusStages = [
  { min: 0, max: 22, label: 'Cold Core Spin-Up', log: 'Awakening cloud container & alpine nodes...' },
  { min: 23, max: 48, label: 'Telemetry Handshake', log: 'Establishing encrypted link to Render gateway...' },
  { min: 49, max: 72, label: 'Database Synchronization', log: 'Verifying Neon PostgreSQL & Upstash Redis pools...' },
  { min: 73, max: 94, label: 'Calibrating Trail Manifests', log: 'Loading elevation profiles & expedition cohorts...' },
  { min: 95, max: 100, label: 'Gateway Operational', log: 'All systems nominal. Entering Apex Basecamp.' }
]

const currentStage = computed(() => {
  const found = statusStages.find(s => progress.value >= s.min && progress.value <= s.max)
  return found || statusStages[statusStages.length - 1]
})

// ============================================================================
// CURATED NON-REPEATING DECK OF 32 URBAN BURDENS & ALPINE ANTIDOTES
// ============================================================================
const BURDEN_CATALOG = [
  { word: 'DIGITAL BURNOUT', antidote: 'Swapped glowing screens for starlit glaciers.' },
  { word: 'CHRONIC TENSION', antidote: 'Unknotted by crisp 4,000m pine winds.' },
  { word: 'DOOMSCROLLING', antidote: 'Infinite feeds replaced by infinite ridgelines.' },
  { word: 'DEADLINE PANIC', antidote: 'The mountain only knows seasons, not clocks.' },
  { word: 'SLEEP DEBT', antidote: 'Reset to the natural rhythm of alpine dusk.' },
  { word: 'DECISION FATIGUE', antidote: 'Simplified to one honest step after another.' },
  { word: 'ANXIETY SPIRALS', antidote: 'Grounded on ancient Himalayan granite.' },
  { word: 'NOTIFICATION SPAM', antidote: 'Zero bars. One hundred percent presence.' },
  { word: 'IMPOSTER SYNDROME', antidote: 'The summit asks for grit, never credentials.' },
  { word: 'ECHO CHAMBERS', antidote: 'Replaced by the vast silence of the valley.' },
  { word: 'BRAIN FOG', antidote: 'Cleared by thin, sub-zero mountain oxygen.' },
  { word: 'RUSH HOUR GRIDLOCK', antidote: 'Traded asphalt congestion for open high passes.' },
  { word: 'EMOTIONAL DRAIN', antidote: 'Recharged beside a crackling basecamp fire.' },
  { word: 'OVERTHINKING', antidote: 'Quieted by the steady cadence of the climb.' },
  { word: 'INBOX OVERLOAD', antidote: 'Out-of-office auto-reply: Above the clouds.' },
  { word: 'SOCIAL EXHAUSTION', antidote: 'Restorative solitude among towering peaks.' },
  { word: 'MONDAY DREAD', antidote: 'Every dawn on the trail is worth waking for.' },
  { word: 'MICROMANAGEMENT', antidote: 'You chart your own compass bearing now.' },
  { word: 'SENSORY OVERLOAD', antidote: 'Distilled to snow, stone, and open sky.' },
  { word: 'HEAVY MELANCHOLY', antidote: 'Lifted by the first golden alpenglow.' },
  { word: 'STAGNATION', antidote: 'Pulse awakened on the steep ridge ascent.' },
  { word: 'SCREEN FATIGUE', antidote: 'Eyes recalibrated to distant horizons.' },
  { word: 'OFFICE POLITICS', antidote: 'Only rope-team trust matters up here.' },
  { word: 'HUSTLE PRESSURE', antidote: 'Replaced by deliberate, mindful pacing.' },
  { word: 'CABIN FEVER', antidote: '360 degrees of untamed panoramic wilderness.' },
  { word: 'RESTLESSNESS', antidote: 'Channelled into vertical summit gain.' },
  { word: 'CYNICISM', antidote: 'Dissolved by raw awe at 14,000 feet.' },
  { word: 'COMPULSIVE CHECKING', antidote: 'Phone stowed. Senses wide awake.' },
  { word: 'WORKLOAD CRUSH', antidote: 'The only weight now is the pack on your back.' },
  { word: 'URBAN CLAUSTROPHOBIA', antidote: 'Breathing room across vast glacial valleys.' },
  { word: 'SELF-DOUBT', antidote: 'Conquered with every contour line you cross.' },
  { word: 'LOW BATTERY MOOD', antidote: 'Solar-charged under high-altitude skies.' }
]

let shuffledDeck = []
let deckPointer = 0

function getNextBurden() {
  if ( shuffledDeck.length === 0 || deckPointer >= shuffledDeck.length ) {
    shuffledDeck = [...BURDEN_CATALOG]
    // Fisher-Yates shuffle
    for (let i = shuffledDeck.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1))
      const temp = shuffledDeck[i]
      shuffledDeck[i] = shuffledDeck[j]
      shuffledDeck[j] = temp
    }
    deckPointer = 0
  }
  return shuffledDeck[deckPointer++]
}

// ============================================================================
// INTERACTIVE FULL-SCREEN SNAKE ("APEX SERPENT") ENGINE
// ============================================================================
const canvasRef = ref(null)
const score = ref(0)
const altitudeGained = ref(0)
const isManualControl = ref(false)
const lastClearedItem = ref({ id: 0, word: '', antidote: '' })

let ctx = null
let animFrameId = null
let lastMoveTime = 0
let lastManualInputTime = 0
const MOVE_INTERVAL_MS = 135

// Grid & Serpent State
let cellSize = 26
let cols = 40
let rows = 25
let minCol = 1
let maxCol = 38
let minRow = 4
let maxRow = 20

let snake = []
let dir = { x: 1, y: 0 }
let nextDir = { x: 1, y: 0 }
let targets = []
let particles = []
let floatingTexts = []

// Touch swipe tracking
let touchStartX = 0
let touchStartY = 0

function computeGridBounds(width, height) {
  const isMobile = width < 768
  cellSize = isMobile ? 22 : 26
  cols = Math.max(14, Math.floor(width / cellSize))
  rows = Math.max(14, Math.floor(height / cellSize))

  // Safe zone margins so targets never spawn behind Top HUD or Bottom HUD/D-Pad
  const topHudPx = isMobile ? 135 : 120
  const bottomHudPx = isMobile ? 165 : 95
  const sidePadPx = isMobile ? 16 : 32

  minCol = Math.max(1, Math.floor(sidePadPx / cellSize))
  maxCol = Math.min(cols - 2, cols - 1 - minCol)
  minRow = Math.max(2, Math.ceil(topHudPx / cellSize))
  maxRow = Math.min(rows - 2, rows - 1 - Math.ceil(bottomHudPx / cellSize))

  if (maxCol <= minCol + 4) {
    minCol = 1
    maxCol = Math.max(5, cols - 2)
  }
  if (maxRow <= minRow + 4) {
    minRow = 2
    maxRow = Math.max(6, rows - 3)
  }
}

function initGame() {
  const canvas = canvasRef.value
  if (!canvas) return
  const width = window.innerWidth
  const height = window.innerHeight
  const dpr = Math.min(window.devicePixelRatio || 1, 2)

  canvas.width = width * dpr
  canvas.height = height * dpr
  canvas.style.width = `${width}px`
  canvas.style.height = `${height}px`

  ctx = canvas.getContext('2d')
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)

  computeGridBounds(width, height)

  const startX = Math.floor((minCol + maxCol) / 2)
  const startY = Math.floor((minRow + maxRow) / 2)

  snake = [
    { x: startX, y: startY },
    { x: startX - 1, y: startY },
    { x: startX - 2, y: startY },
    { x: startX - 3, y: startY },
    { x: startX - 4, y: startY },
    { x: startX - 5, y: startY }
  ]
  dir = { x: 1, y: 0 }
  nextDir = { x: 1, y: 0 }
  targets = []
  particles = []
  floatingTexts = []

  spawnTarget()
  spawnTarget()
}

function handleResize() {
  const canvas = canvasRef.value
  if (!canvas || !visible.value) return
  const width = window.innerWidth
  const height = window.innerHeight
  const dpr = Math.min(window.devicePixelRatio || 1, 2)

  canvas.width = width * dpr
  canvas.height = height * dpr
  canvas.style.width = `${width}px`
  canvas.style.height = `${height}px`

  if (ctx) {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
  }
  computeGridBounds(width, height)

  // Keep existing targets inside safe bounds
  targets.forEach(t => {
    t.x = Math.max(minCol + 1, Math.min(maxCol - 1, t.x))
    t.y = Math.max(minRow + 1, Math.min(maxRow - 1, t.y))
  })
}

function spawnTarget() {
  const burden = getNextBurden()
  let x = minCol + 2
  let y = minRow + 2
  let attempts = 0

  while (attempts < 60) {
    attempts++
    const candidateX = Math.floor(minCol + 1 + Math.random() * Math.max(2, maxCol - minCol - 2))
    const candidateY = Math.floor(minRow + 1 + Math.random() * Math.max(2, maxRow - minRow - 2))

    const onSnake = snake.some(seg => Math.abs(seg.x - candidateX) <= 1 && Math.abs(seg.y - candidateY) <= 1)
    const onOtherTarget = targets.some(t => Math.abs(t.x - candidateX) < 5 && Math.abs(t.y - candidateY) < 3)

    if (!onSnake && !onOtherTarget) {
      x = candidateX
      y = candidateY
      break
    }
  }

  // Palette variation between coral rose & warm amber
  const palettes = [
    { core: '#fb7185', glow: 'rgba(244, 63, 94, 0.4)', border: 'rgba(251, 113, 133, 0.65)' },
    { core: '#fbbf24', glow: 'rgba(245, 158, 11, 0.4)', border: 'rgba(251, 191, 36, 0.65)' },
    { core: '#f87171', glow: 'rgba(239, 68, 68, 0.4)', border: 'rgba(248, 113, 113, 0.65)' }
  ]
  const palette = palettes[Math.floor(Math.random() * palettes.length)]

  targets.push({
    x,
    y,
    word: burden.word,
    antidote: burden.antidote,
    palette,
    bornAt: performance.now()
  })
}

function computeAutoPilotDirection() {
  if (targets.length === 0 || snake.length === 0) return
  const head = snake[0]

  // Pick closest target
  let bestTarget = targets[0]
  let bestDist = Infinity
  for (const t of targets) {
    const d = Math.abs(t.x - head.x) + Math.abs(t.y - head.y)
    if (d < bestDist) {
      bestDist = d
      bestTarget = t
    }
  }

  const candidateDirs = [
    { x: 1, y: 0 },
    { x: -1, y: 0 },
    { x: 0, y: 1 },
    { x: 0, y: -1 }
  ].filter(d => !(d.x === -dir.x && d.y === -dir.y))

  // Sort candidates by closeness to target while avoiding immediate body hit
  candidateDirs.sort((a, b) => {
    const ax = head.x + a.x
    const ay = head.y + a.y
    const bx = head.x + b.x
    const by = head.y + b.y

    const aHit = snake.slice(0, -1).some(s => s.x === ax && s.y === ay) ? 1000 : 0
    const bHit = snake.slice(0, -1).some(s => s.x === bx && s.y === by) ? 1000 : 0

    const aDist = Math.abs(bestTarget.x - ax) + Math.abs(bestTarget.y - ay) + aHit
    const bDist = Math.abs(bestTarget.x - bx) + Math.abs(bestTarget.y - by) + bHit
    return aDist - bDist
  })

  if (candidateDirs.length > 0) {
    nextDir = candidateDirs[0]
  }
}

function stepSnake(now) {
  if (snake.length === 0) return

  // Resume autopilot if user hasn't pressed a control in 10 seconds
  if (isManualControl.value && now - lastManualInputTime > 10000) {
    isManualControl.value = false
  }

  if (!isManualControl.value) {
    computeAutoPilotDirection()
  }

  dir = { ...nextDir }
  const head = snake[0]
  let nx = head.x + dir.x
  let ny = head.y + dir.y

  // Toroidal wrap-around within playable arena so gameplay never halts
  if (nx > maxCol) nx = minCol
  else if (nx < minCol) nx = maxCol

  if (ny > maxRow) ny = minRow
  else if (ny < minRow) ny = maxRow

  // Check if a stress target node was eaten (generous 1-cell radius for smooth feel)
  const hitIndex = targets.findIndex(t => Math.abs(t.x - nx) <= 1 && Math.abs(t.y - ny) <= 1)

  snake.unshift({ x: nx, y: ny })

  if (hitIndex !== -1) {
    const eaten = targets[hitIndex]
    targets.splice(hitIndex, 1)

    score.value += 1
    altitudeGained.value += 150
    lastClearedItem.value = {
      id: score.value,
      word: eaten.word,
      antidote: eaten.antidote
    }

    // Spawn celebratory emerald particles
    const px = eaten.x * cellSize + cellSize / 2
    const py = eaten.y * cellSize + cellSize / 2
    for (let i = 0; i < 22; i++) {
      const angle = (Math.PI * 2 * i) / 22 + (Math.random() - 0.5) * 0.3
      const speed = 1.5 + Math.random() * 3.8
      particles.push({
        x: px,
        y: py,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        radius: 2 + Math.random() * 2.5,
        alpha: 1,
        color: i % 3 === 0 ? '#7bf1a8' : (i % 2 === 0 ? '#10b981' : '#ffffff')
      })
    }

    // Floating score callout on canvas
    floatingTexts.push({
      x: px,
      y: py - 8,
      text: `${eaten.word} CLEARED · +150m`,
      alpha: 1,
      vy: -0.9
    })

    // Cap maximum snake length so screen stays clean and sleek
    if (snake.length > 22) {
      snake.pop()
    }

    spawnTarget()
  } else {
    snake.pop()

    // Non-punitive self-contact trim (keeps flow meditative & uninterrupted)
    const selfHitIdx = snake.slice(1).findIndex(s => s.x === nx && s.y === ny)
    if (selfHitIdx !== -1 && snake.length > 6) {
      snake = snake.slice(0, Math.max(6, selfHitIdx + 1))
    }
  }
}

function renderCanvas(now) {
  if (!ctx || !canvasRef.value) return
  const width = window.innerWidth
  const height = window.innerHeight

  // 1. Deep Obsidian Alpine Background
  ctx.fillStyle = '#040a07'
  ctx.fillRect(0, 0, width, height)

  // 2. Subtle Topographic Grid & Coordinate Crosshairs
  ctx.lineWidth = 1
  ctx.strokeStyle = 'rgba(16, 185, 129, 0.04)'
  ctx.beginPath()
  for (let c = 0; c <= cols; c++) {
    const x = c * cellSize
    ctx.moveTo(x, 0)
    ctx.lineTo(x, height)
  }
  for (let r = 0; r <= rows; r++) {
    const y = r * cellSize
    ctx.moveTo(0, y)
    ctx.lineTo(width, y)
  }
  ctx.stroke()

  // Subtle safe-arena boundary frame
  const arenaX = minCol * cellSize
  const arenaY = minRow * cellSize
  const arenaW = (maxCol - minCol + 1) * cellSize
  const arenaH = (maxRow - minRow + 1) * cellSize
  ctx.strokeStyle = 'rgba(123, 241, 168, 0.08)'
  ctx.setLineDash([6, 6])
  ctx.strokeRect(arenaX, arenaY, arenaW, arenaH)
  ctx.setLineDash([])

  // Ambient glow following the snake head
  if (snake.length > 0) {
    const hx = snake[0].x * cellSize + cellSize / 2
    const hy = snake[0].y * cellSize + cellSize / 2
    const grad = ctx.createRadialGradient(hx, hy, 10, hx, hy, 220)
    grad.addColorStop(0, 'rgba(16, 185, 129, 0.14)')
    grad.addColorStop(1, 'rgba(16, 185, 129, 0)')
    ctx.fillStyle = grad
    ctx.fillRect(0, 0, width, height)
  }

  // 3. Render Urban Overload Target Nodes
  targets.forEach(t => {
    const cx = t.x * cellSize + cellSize / 2
    const cy = t.y * cellSize + cellSize / 2
    const pulse = 1 + Math.sin((now - t.bornAt) * 0.005) * 0.22

    // Outer pulsing distress aura
    ctx.save()
    ctx.beginPath()
    ctx.arc(cx, cy, cellSize * 0.85 * pulse, 0, Math.PI * 2)
    ctx.fillStyle = t.palette.glow
    ctx.fill()

    // Rotating dashed target reticle
    ctx.translate(cx, cy)
    ctx.rotate((now * 0.0015) % (Math.PI * 2))
    ctx.strokeStyle = t.palette.border
    ctx.lineWidth = 1.3
    ctx.setLineDash([4, 3])
    ctx.beginPath()
    ctx.arc(0, 0, cellSize * 0.62, 0, Math.PI * 2)
    ctx.stroke()
    ctx.setLineDash([])
    ctx.restore()

    // Core node diamond
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(Math.PI / 4)
    ctx.fillStyle = t.palette.core
    ctx.shadowColor = t.palette.core
    ctx.shadowBlur = 12
    const box = cellSize * 0.44
    ctx.fillRect(-box / 2, -box / 2, box, box)
    ctx.restore()

    // Crisp Floating Label Pill above target node
    ctx.save()
    ctx.font = '600 11px "JetBrains Mono", "Fira Code", monospace'
    const labelText = `× ${t.word}`
    const textMetrics = ctx.measureText(labelText)
    const padX = 8
    const pillW = textMetrics.width + padX * 2
    const pillH = 20
    let pillX = cx - pillW / 2
    let pillY = cy - cellSize * 0.9 - pillH

    // Keep pill inside horizontal screen edges
    pillX = Math.max(10, Math.min(width - pillW - 10, pillX))
    if (pillY < arenaY + 4) {
      pillY = cy + cellSize * 0.85
    }

    ctx.fillStyle = 'rgba(10, 15, 13, 0.88)'
    ctx.strokeStyle = t.palette.border
    ctx.lineWidth = 1
    ctx.beginPath()
    ctx.roundRect(pillX, pillY, pillW, pillH, 6)
    ctx.fill()
    ctx.stroke()

    ctx.fillStyle = '#f8fafc'
    ctx.textBaseline = 'middle'
    ctx.fillText(labelText, pillX + padX, pillY + pillH / 2 + 0.5)
    ctx.restore()
  })

  // 4. Render the Apex Serpent (Trail & Beacon Head)
  if (snake.length > 0) {
    // Connect trail spine
    ctx.save()
    for (let i = snake.length - 1; i >= 0; i--) {
      const seg = snake[i]
      const sx = seg.x * cellSize + cellSize / 2
      const sy = seg.y * cellSize + cellSize / 2
      const ratio = 1 - i / (snake.length + 2)

      if (i === 0) {
        // Serpent Head (Apex Beacon)
        ctx.save()
        ctx.fillStyle = '#7bf1a8'
        ctx.shadowColor = '#10b981'
        ctx.shadowBlur = 18
        const headSize = cellSize * 0.78
        ctx.beginPath()
        ctx.roundRect(sx - headSize / 2, sy - headSize / 2, headSize, headSize, 6)
        ctx.fill()

        // Inner dark core dot
        ctx.fillStyle = '#042f1e'
        ctx.beginPath()
        ctx.arc(sx, sy, 3.2, 0, Math.PI * 2)
        ctx.fill()

        // Subtle "APEX" tag next to head
        ctx.font = '700 9px monospace'
        ctx.fillStyle = 'rgba(123, 241, 168, 0.85)'
        ctx.fillText('APEX', sx + cellSize * 0.55, sy - cellSize * 0.35)
        ctx.restore()
      } else {
        // Trail Segment
        const segSize = cellSize * (0.35 + ratio * 0.36)
        ctx.fillStyle = `rgba(16, 185, 129, ${(0.18 + ratio * 0.68).toFixed(2)})`
        ctx.beginPath()
        ctx.roundRect(sx - segSize / 2, sy - segSize / 2, segSize, segSize, 5)
        ctx.fill()
      }
    }
    ctx.restore()
  }

  // 5. Render Burst Particles
  for (let i = particles.length - 1; i >= 0; i--) {
    const p = particles[i]
    p.x += p.vx
    p.y += p.vy
    p.vx *= 0.96
    p.vy *= 0.96
    p.alpha -= 0.024

    if (p.alpha <= 0) {
      particles.splice(i, 1)
      continue
    }

    ctx.save()
    ctx.globalAlpha = Math.max(0, p.alpha)
    ctx.fillStyle = p.color
    ctx.shadowColor = p.color
    ctx.shadowBlur = 8
    ctx.beginPath()
    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2)
    ctx.fill()
    ctx.restore()
  }

  // 6. Render Floating Score Texts
  for (let i = floatingTexts.length - 1; i >= 0; i--) {
    const ft = floatingTexts[i]
    ft.y += ft.vy
    ft.alpha -= 0.018

    if (ft.alpha <= 0) {
      floatingTexts.splice(i, 1)
      continue
    }

    ctx.save()
    ctx.globalAlpha = Math.max(0, ft.alpha)
    ctx.font = '700 11px monospace'
    ctx.fillStyle = '#7bf1a8'
    ctx.textAlign = 'center'
    ctx.fillText(ft.text, ft.x, ft.y)
    ctx.restore()
  }
}

function animationLoop(now) {
  if (!visible.value || isUnmounted) return

  if (now - lastMoveTime >= MOVE_INTERVAL_MS) {
    stepSnake(now)
    lastMoveTime = now
  }

  renderCanvas(now)
  animFrameId = requestAnimationFrame(animationLoop)
}

// ============================================================================
// KEYBOARD & MOBILE TOUCH CONTROLS
// ============================================================================
function setDirection(dx, dy) {
  // Prevent 180-degree instant reversal
  if (dx === -dir.x && dy === -dir.y) return
  nextDir = { x: dx, y: dy }
  isManualControl.value = true
  lastManualInputTime = performance.now()
}

function handleKeydown(e) {
  if (!visible.value) return
  const key = e.key.toLowerCase()

  if (key === 'arrowup' || key === 'w') {
    e.preventDefault()
    setDirection(0, -1)
  } else if (key === 'arrowdown' || key === 's') {
    e.preventDefault()
    setDirection(0, 1)
  } else if (key === 'arrowleft' || key === 'a') {
    e.preventDefault()
    setDirection(-1, 0)
  } else if (key === 'arrowright' || key === 'd') {
    e.preventDefault()
    setDirection(1, 0)
  }
}

function handleTouchStart(e) {
  if (!e.touches || e.touches.length === 0) return
  touchStartX = e.touches[0].clientX
  touchStartY = e.touches[0].clientY
}

function handleTouchMove(e) {
  if (visible.value) {
    // Prevent pull-to-refresh or page bounce while steering on mobile
    e.preventDefault()
  }
}

function handleTouchEnd(e) {
  if (!e.changedTouches || e.changedTouches.length === 0) return
  const dx = e.changedTouches[0].clientX - touchStartX
  const dy = e.changedTouches[0].clientY - touchStartY

  if (Math.abs(dx) < 18 && Math.abs(dy) < 18) return

  if (Math.abs(dx) > Math.abs(dy)) {
    setDirection(dx > 0 ? 1 : -1, 0)
  } else {
    setDirection(0, dy > 0 ? 1 : -1)
  }
}

// ============================================================================
// CONTINUOUS BACKEND PING LOOP & PROGRESS SYNCHRONIZATION
// ============================================================================
async function pollBackendUntilAwake() {
  if (isUnmounted || isWarmedEarly.value) return

  if (!props.backendUrl) {
    isWarmedEarly.value = true
    return
  }

  try {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 7000)

    const res = await fetch(`${props.backendUrl}/api/utils/ping`, {
      method: 'GET',
      headers: { Accept: 'application/json' },
      signal: controller.signal
    })
    clearTimeout(timeout)

    if (res.ok) {
      isWarmedEarly.value = true
      return
    }
  } catch (err) {
    // Backend still spinning up on Render; retry in 2 seconds
  }

  if (!isUnmounted && !isWarmedEarly.value) {
    pingTimeoutId = setTimeout(pollBackendUntilAwake, 2000)
  }
}

function startProgressTicker() {
  if (progressInterval) clearInterval(progressInterval)
  bootStartTime = performance.now()

  progressInterval = setInterval(() => {
    if (isHoldMode.value) {
      // In Local Test Hold Mode, keep progress gently hovering around 78-85%
      if (progress.value < 78) {
        progress.value += 0.4
      }
      return
    }

    const elapsed = performance.now() - bootStartTime
    const minDisplayMet = elapsed >= MIN_BOOT_DISPLAY_MS

    if (isWarmedEarly.value && minDisplayMet) {
      // Backend has responded AND minimum visual grace period met -> glide to 100%
      progress.value += 3.2
    } else {
      // Smooth asymptotic progression while waiting for backend response
      if (progress.value < 40) {
        progress.value += 0.42
      } else if (progress.value < 70) {
        progress.value += 0.22
      } else if (progress.value < 88) {
        progress.value += 0.09
      } else if (progress.value < 95) {
        progress.value += 0.025
      }
    }

    if (progress.value >= 100) {
      progress.value = 100
      clearInterval(progressInterval)
      setTimeout(() => {
        completeSplash()
      }, 320)
    }
  }, 60)
}

function completeSplash() {
  visible.value = false
  if (animFrameId) cancelAnimationFrame(animFrameId)
  if (progressInterval) clearInterval(progressInterval)
  if (pingTimeoutId) clearTimeout(pingTimeoutId)
  sessionStorage.setItem('apex_boot_seen', 'true')
  emit('finish')
}

// ============================================================================
// LOCAL TESTING SANDBOX CONTROLS
// ============================================================================
function toggleHoldMode() {
  if (isHoldMode.value) {
    // Release hold and finish boot smoothly
    isHoldMode.value = false
    isWarmedEarly.value = true
  } else {
    isHoldMode.value = true
  }
}

function launchLocalTestSandbox() {
  progress.value = 42
  score.value = 0
  altitudeGained.value = 0
  isHoldMode.value = true
  visible.value = true

  setTimeout(() => {
    initGame()
    lastMoveTime = performance.now()
    if (animFrameId) cancelAnimationFrame(animFrameId)
    animFrameId = requestAnimationFrame(animationLoop)
    startProgressTicker()
  }, 50)
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
  window.addEventListener('resize', handleResize)

  // Only show automatically once per browser session on initial landing
  if (sessionStorage.getItem('apex_boot_seen') === 'true') {
    visible.value = false
    emit('finish')
    if (props.backendUrl) {
      fetch(`${props.backendUrl}/api/utils/ping`).catch(() => {})
    }
    return
  }

  initGame()
  lastMoveTime = performance.now()
  animFrameId = requestAnimationFrame(animationLoop)

  pollBackendUntilAwake()
  startProgressTicker()
})

onUnmounted(() => {
  isUnmounted = true
  window.removeEventListener('keydown', handleKeydown)
  window.removeEventListener('resize', handleResize)
  if (animFrameId) cancelAnimationFrame(animFrameId)
  if (progressInterval) clearInterval(progressInterval)
  if (pingTimeoutId) clearTimeout(pingTimeoutId)
})
</script>

<style scoped>
.apex-boot-universe {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100dvh;
  background-color: #040a07;
  z-index: 99999;
  overflow: hidden;
  user-select: none;
  touch-action: none;
}

.serpent-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
  z-index: 1;
}

.vignette-overlay {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 50% 50%, transparent 45%, rgba(2, 6, 4, 0.78) 100%),
    linear-gradient(180deg, rgba(3, 8, 5, 0.82) 0%, transparent 22%, transparent 78%, rgba(3, 8, 5, 0.88) 100%);
  pointer-events: none;
  z-index: 2;
}

/* ========================================================================== */
/* TOP EDITORIAL HUD                                                          */
/* ========================================================================== */
.hud-top-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  padding: 1.25rem 1.75rem;
  display: grid;
  grid-template-columns: 1fr minmax(280px, 560px) 1fr;
  align-items: start;
  gap: 1rem;
  z-index: 5;
  pointer-events: none;
}

.hud-top-left {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.brand-cluster {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.brand-emblem {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(123, 241, 168, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.brand-logo-img {
  width: 22px;
  height: 22px;
  object-fit: contain;
}

.brand-title {
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: #f8fafc;
}

.mode-badge {
  font-size: 0.62rem;
  padding: 0.12rem 0.45rem;
  border-radius: 99px;
  font-weight: 700;
  letter-spacing: 0.8px;
}

.mode-auto {
  background: rgba(16, 185, 129, 0.14);
  color: #7bf1a8;
  border: 1px solid rgba(123, 241, 168, 0.3);
}

.mode-manual {
  background: rgba(251, 191, 36, 0.16);
  color: #fde68a;
  border: 1px solid rgba(251, 191, 36, 0.4);
}

.control-hint {
  font-size: 0.68rem;
  color: rgba(226, 232, 240, 0.6);
  margin-top: 2px;
}

.control-hint kbd {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  padding: 0px 4px;
  font-size: 0.62rem;
  color: #7bf1a8;
  margin: 0 1px;
}

/* Local Test Button inside HUD */
.dev-control-wrapper {
  pointer-events: auto;
}

.btn-dev-toggle {
  background: rgba(15, 23, 42, 0.82);
  border: 1px solid rgba(123, 241, 168, 0.38);
  color: #cbd5e1;
  font-size: 0.68rem;
  padding: 0.32rem 0.75rem;
  border-radius: 99px;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-dev-toggle:hover {
  border-color: #7bf1a8;
  color: #ffffff;
  background: rgba(16, 185, 129, 0.2);
}

.btn-dev-toggle.is-holding {
  background: rgba(245, 158, 11, 0.18);
  border-color: #fbbf24;
  color: #fde68a;
  box-shadow: 0 0 15px rgba(245, 158, 11, 0.25);
}

/* Top-Center Editorial Mission */
.hud-top-center {
  justify-self: center;
  max-width: 560px;
}

.mission-eyebrow {
  font-size: 0.66rem;
  letter-spacing: 2.5px;
  color: #7bf1a8;
  font-weight: 700;
  margin-bottom: 0.2rem;
}

.mission-headline {
  font-size: clamp(1.05rem, 1.8vw, 1.45rem);
  font-weight: 800;
  color: #ffffff;
  letter-spacing: -0.4px;
  margin: 0 0 0.45rem 0;
  text-shadow: 0 2px 16px rgba(0, 0, 0, 0.7);
}

.antidote-pill {
  display: inline-flex;
  align-items: center;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.4rem;
  background: rgba(8, 20, 14, 0.78);
  border: 1px solid rgba(123, 241, 168, 0.22);
  padding: 0.32rem 0.85rem;
  border-radius: 99px;
  font-size: 0.76rem;
  color: #e2e8f0;
  backdrop-filter: blur(8px);
}

.cleared-word {
  color: #fb7185;
  text-decoration: line-through;
  font-weight: 700;
  font-size: 0.72rem;
}

.antidote-divider {
  color: rgba(255, 255, 255, 0.3);
}

.antidote-quote {
  color: #cbd5e1;
  font-style: italic;
}

/* Top-Right Score Telemetry */
.hud-top-right {
  justify-self: end;
  display: flex;
  align-items: center;
  gap: 0.9rem;
  background: rgba(8, 18, 13, 0.76);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 0.45rem 0.9rem;
  backdrop-filter: blur(8px);
}

.score-box {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.score-label {
  font-size: 0.58rem;
  letter-spacing: 1px;
  color: rgba(226, 232, 240, 0.55);
}

.score-value {
  font-size: 1.15rem;
  font-weight: 700;
  line-height: 1.1;
}

.score-divider {
  width: 1px;
  height: 24px;
  background: rgba(255, 255, 255, 0.12);
}

.text-emerald {
  color: #7bf1a8;
}

/* ========================================================================== */
/* BOTTOM CORNERS: SERVER STATUS & PROGRESS                                   */
/* ========================================================================== */
.hud-bottom-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 1.15rem 1.75rem;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1.5rem;
  z-index: 5;
  pointer-events: none;
}

.hud-bottom-left {
  max-width: 480px;
}

.beacon-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #f59e0b;
  box-shadow: 0 0 10px #f59e0b;
  animation: pulseBeacon 1.4s ease-in-out infinite;
  flex-shrink: 0;
}

.beacon-dot.beacon-ready {
  background-color: #10b981;
  box-shadow: 0 0 12px #10b981;
}

@keyframes pulseBeacon {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.35; transform: scale(0.85); }
}

.boot-status-title {
  font-size: 0.76rem;
  font-weight: 600;
  color: #f1f5f9;
}

.boot-status-sub {
  font-size: 0.5rem;
  color: rgba(203, 213, 225, 0.68);
}

.hud-bottom-right {
  min-width: 240px;
  max-width: 300px;
  width: 100%;
}

.progress-tag {
  font-size: 0.62rem;
  letter-spacing: 1.2px;
  color: #7bf1a8;
}

.progress-numbers {
  display: flex;
  align-items: baseline;
  gap: 1px;
}

.progress-int {
  font-size: 1.5rem;
  font-weight: 700;
  color: #ffffff;
  line-height: 1;
}

.progress-pct {
  font-size: 0.8rem;
  color: #7bf1a8;
  font-weight: 700;
}

.progress-rail {
  width: 100%;
  height: 5px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 99px;
  overflow: hidden;
  position: relative;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #059669, #10b981, #7bf1a8);
  border-radius: 99px;
  position: relative;
  transition: width 0.08s linear;
}

.progress-spark {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #ffffff;
  box-shadow: 0 0 10px #7bf1a8;
}

/* ========================================================================== */
/* MOBILE DIRECTIONAL PAD & RESPONSIVE LAYOUT                                 */
/* ========================================================================== */
.mobile-dpad {
  position: absolute;
  bottom: 92px;
  right: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  z-index: 6;
  pointer-events: auto;
  opacity: 0.82;
}

.dpad-middle-row {
  display: flex;
  align-items: center;
  gap: 4px;
}

.dpad-center-dot {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(123, 241, 168, 0.2);
}

.dpad-btn {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: rgba(10, 22, 16, 0.85);
  border: 1px solid rgba(123, 241, 168, 0.32);
  color: #f8fafc;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.95rem;
  backdrop-filter: blur(6px);
  active: scale(0.92);
}

.dpad-btn:active {
  background: rgba(16, 185, 129, 0.35);
  border-color: #7bf1a8;
}

/* Local Test Floating Trigger on Landing Page */
.local-test-launcher {
  position: fixed;
  bottom: 18px;
  left: 18px;
  z-index: 9990;
}

.btn-launch-sandbox {
  background: rgba(10, 20, 15, 0.9);
  border: 1px solid rgba(123, 241, 168, 0.4);
  color: #f8fafc;
  font-size: 0.72rem;
  padding: 0.45rem 0.9rem;
  border-radius: 99px;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  cursor: pointer;
  backdrop-filter: blur(10px);
  transition: all 0.2s ease;
}

.btn-launch-sandbox:hover {
  border-color: #7bf1a8;
  background: rgba(16, 185, 129, 0.22);
  transform: translateY(-2px);
}

/* Transitions */
.antidote-swap-enter-active,
.antidote-swap-leave-active {
  transition: opacity 0.22s ease, transform 0.22s ease;
}

.antidote-swap-enter-from {
  opacity: 0;
  transform: translateY(4px);
}

.antidote-swap-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

.splash-fade-leave-active {
  transition: opacity 0.65s cubic-bezier(0.4, 0, 0.2, 1), transform 0.65s ease;
}

.splash-fade-leave-to {
  opacity: 0;
  transform: scale(1.02);
}

/* ========================================================================== */
/* MOBILE BREAKPOINT (< 768px)                                                */
/* ========================================================================== */
@media (max-width: 767.98px) {
  .hud-top-bar {
    grid-template-columns: 1fr auto;
    padding: 0.75rem 0.9rem;
    gap: 0.5rem;
  }

  .hud-top-center {
    grid-column: 1 / -1;
    order: 3;
    max-width: 100%;
  }

  .mission-headline {
    font-size: 0.98rem;
    margin-bottom: 0.25rem;
  }

  .antidote-pill {
    font-size: 0.68rem;
    padding: 0.22rem 0.65rem;
  }

  .hud-top-right {
    padding: 0.3rem 0.6rem;
    gap: 0.55rem;
  }

  .score-value {
    font-size: 0.95rem;
  }

  .score-label {
    font-size: 0.5rem;
  }

  .hud-bottom-bar {
    flex-direction: column;
    align-items: stretch;
    gap: 0.45rem;
    padding: 0.75rem 0.9rem;
    background: linear-gradient(0deg, rgba(3, 8, 5, 0.95) 0%, rgba(3, 8, 5, 0.75) 80%, transparent 100%);
  }

  .hud-bottom-left {
    max-width: 100%;
  }

  .boot-status-title {
    font-size: 0.72rem;
  }

  .boot-status-sub {
    font-size: 0.64rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .hud-bottom-right {
    max-width: 100%;
    min-width: 0;
  }

  .progress-int {
    font-size: 1.15rem;
  }
}
</style>
