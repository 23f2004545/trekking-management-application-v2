# 🏔️ Apex Expeditions - Wilderness Operations Portal

**Apex** is a comprehensive, decoupled, enterprise-grade web application engineered for high-altitude trekking logistics. It serves as a unified operational telemetry platform connecting **Explorers (Trekkers)**, **Field Guides (Staff)**, and **Central Command (Admins)**. It handles everything from secure geographical mapping and live manifest tracking to asynchronous data exporting and cryptographic passwordless authentication.

> [!TIP]
> ### 🌐 Live Production Experience
> Apex Expeditions is deployed live on global cloud infrastructure. Explore the system across all role clearances:
> 
> | Service Layer | Deployment Target | Live URL | Status |
> | :--- | :--- | :--- | :--- |
> | **Frontend Client (PWA)** | Vercel Edge Network | [trekking-management-application-v2-snowy.vercel.app](https://trekking-management-application-v2-snowy.vercel.app/) | ![Vercel](https://img.shields.io/badge/Deployment-Live%20Production-success?logo=vercel&logoColor=white) |
> | **REST API & Celery Core** | Render Web Service | [trekking-management-application-v2.onrender.com](https://trekking-management-application-v2.onrender.com) | ![Render](https://img.shields.io/badge/API-Operational-46e3b7?logo=render&logoColor=white) |
> 
> **Interactive Evaluation Mode:** Visitors and evaluators can click **"Try Demo Accounts"** directly on the login page to immediately test **Explorer (Trekker)**, **Field Commander (Staff)**, or **Central Command (Admin)** portals with zero manual signups. Real-time transactional emails can be tested live using the interactive demo email preview dialog without saving your email to our database!

---

## 🚀 The Core Engine (Role-Based Features)

### 🏕️ For Explorers (Trekkers)
- **Passwordless Authentication**: Secure, frictionless login using time-limited OTPs dispatched via email.
- **Expedition Discovery**: Filter active routes by difficulty, altitude, and dynamically calculated budget constraints.
- **Smart Booking Terminal**: Interactive payment simulation gateway that validates server-side slot availability in real-time.
- **Medical & Passport Telemetry**: Attach specific medical parameters to bookings for guide review.
- **Immutable Historical Archives**: Access past expedition receipts with preserved pricing and temporal data, alongside rating submissions.

### 👨‍✈️ For Field Commanders (Staff Guides)
- **Live Roster Manifests**: Access active trekker headcounts, emergency contacts, and medical alerts for assigned routes.
- **Operational Status Control**: Update expedition phases (Ongoing, Completed, Cancelled).
- **Hazard Watchers**: Enforced dynamic UI rendering for mandatory hazard reporting upon route cancellation.
- **Performance Analytics**: View aggregated reviews and ratings from past guided expeditions.

### 🛡️ For Central Command (Admins)
- **System Health Core**: Real-time microservice pinging for Database, Redis, Celery, and SMTP statuses.
- **Tactical Map Deployment**: Create new treks using a responsive, interactive Leaflet.js satellite map to drop precise Basecamp GPS coordinates.
- **Immutable Audit Logs**: Gamified timeline tracking every major CRUD action, deletion, or suspension on the platform.
- **Asynchronous Telemetry Export**: Generate and email comprehensive statistical yields (Revenue, Pax, Completion Rates) for archived treks via background workers.

---

## 🏗️ Architectural Masterpieces (Beyond the Basics)
This project breaks past standard CRUD applications by implementing industry-standard enterprise solutions:

**1. The "Snapshot Pattern" (Data Immutability)**
- **The Problem**: If an admin changes the price or date of a "Rohtang Pass" trek, all past trekkers' historical receipts would corrupt and show the new future data.
- **The Solution**: Implemented temporal snapshot columns inside the `Booking` table. When a transaction clears, the exact price, date, and assigned guide are permanently locked into the booking row, severing its reliance on the mutable `Trek` template.

**2. The "Ask Admin" Dispatch Desk (Professional Support)**
- **The Solution**: A complete ticketing system allowing field staff and trekkers to report hazards or queries. Admins triage tickets by priority (Routine, Urgent, Hazard) and transmit resolutions that automatically trigger background Celery tasks to dispatch heavily formatted, official HTML emails to the user.

**3. Progressive Web App (PWA) Integration**
- **The Solution**: Configured via Vite, the platform is fully installable on iOS/Android devices. It utilizes service workers to cache essential assets, providing native-app aesthetics and offline resilience for field guides operating in low-connectivity environments.

**4. Advanced JWT Lifecycle Interceptors**
- **The Problem**: Standard JWTs expire, abruptly kicking users out of the application mid-action.
- **The Solution**: Engineered an Axios/Fetch wrapper that catches `401 Unauthorized` responses, silently requests a new Access Token using a long-lived Refresh Token stored in LocalStorage, and automatically retries the user's failed request without them ever noticing.

**5. Asynchronous Task Queuing (Celery + Redis)**
- **The Solution**: To prevent the main Flask thread from freezing during heavy operations (like rendering telemetry exports or dispatching emails), all communications and heavy data processing are offloaded to asynchronous Celery workers brokered by Redis memory.

---

## 🛠️ Technology Stack

**Frontend Architecture (Decoupled SPA)**
- **Framework**: Vue.js 3 (Composition API) + Vite
- **State Management**: Pinia (Persistent Store)
- **Routing**: Vue Router (Navigation Guards + RBAC)
- **UI/UX**: Custom Glassmorphism CSS, Bootstrap 5 Grid, Bootstrap Icons
- **Geospatial**: Leaflet.js (Interactive Satellite Maps)

**Backend Architecture (RESTful API)**
- **Framework**: Python 3, Flask
- **Database**: PostgreSQL / SQLite (SQLAlchemy ORM)
- **Authentication**: Flask-JWT-Extended (Access/Refresh Tokens), Bcrypt Hashing
- **Asynchronous Workers**: Celery
- **Message Broker & Caching**: Redis
- **Mail Server**: Mailpit (SMTP Sandbox)

---

## 📂 System Structure

The application is heavily decoupled into two distinct environments to simulate real-world microservice scaling.

```bash
Apex_Expeditions/
├── backend/                 # Python Flask API Core
│   ├── app.py               # Application Factory & Config
│   ├── tasks.py             # Celery Background Workers (Emails/Exports)
│   ├── mail.py              # SMTP Setup & Mail Functioning (Mailpit)
│   ├── config.py             # Configuration file
│   ├── controller/
│   │   ├── models.py        # Database Schema (User, Trek, Booking, Tickets, etc.)
│   │   ├── decorators.py    # Decorators for different roles 
│   │   └── extensions.py    # SQLAlchemy, JWT, Cache Initialization
│   └── routes/              # Blueprint Modules
│       ├── admin_apis.py      # Infrastructure, Staff Auth, Fleet Management
│       ├── auth_apis.py       # Passwordless OTP & JWT Rotations
│       ├── staff_apis.py      # Guide Manifests & Operations
│       ├── trekker_apis.py    # Explorer Bookings & Payments
│       └── utils_apis.py      # Shared History Aggregations & Support Desk
│
└── frontend/                # Vue.js 3 SPA
    ├── index.html           # PWA Entry Point
    ├── vite.config.js       # Vite & PWA Plugin Configurations
    ├── src/
    │   ├── main.js          # Vue App Initialization
    │   ├── App.vue          
    │   ├── router/          # Route Guards & Navigation
    │   ├── stores/          # Pinia State (Auth, Alerts)
    │   ├── utils/           # JWT Interceptors & API Wrappers
    │   ├── components/      # Reusable UI (TrekMap, PaymentTerminal, Modals)
    │   └── views/           # Page Components (Separated by Role)
    └── public/              # PWA Manifests & OS Icons
```

---

## ⚙️ Setup & Deployment Initialization
**Phase 1: Backend Infrastructure (Terminal 1)**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # (or venv\Scripts\activate on Windows)
pip install -r requirements.txt

# Start Flask API
python3 app.py
```

**Phase 2: Asynchronous Workers (Terminal 2 & 3)**
```bash
# Ensure Redis Server is installed and running locally on port 6379
redis-server

# Start Celery Worker (Terminal 3 - inside backend folder)
python3 -m celery -A tasks:celery_app worker --loglevel=info
```

**Phase 3: Frontend PWA Compilation (Terminal 4)**
```bash
cd frontend
npm install

# Start Vite Development Server
npm run dev

# (To test PWA installation locally, use build & preview)
npm run build
npm run preview
```

- Access the client portal at http://localhost:5173

--- 

## 📜 Standardized API Architecture (Sample)
The backend enforces strict separation of concerns via RESTful JSON blueprints.

| Method | Endpoint | Description | Clearance Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/request-login-otp` | Triggers Redis/Celery passwordless token | Public |
| `GET` | `/api/admin/profile/system-health` | Pings microservices (Redis, SMTP, DB) | Admin |
| `POST` | `/api/admin/treks` | Deploys new Trek (Accepts Geo-Coords & Images) | Admin |
| `PATCH` | `/api/utils/tickets/<id>/resolve` | Transmits official command resolution | Admin |
| `GET` | `/api/utils/history` | Aggregates Snapshot Cohorts for Analytics | Admin / Staff |

---

## 🚀 Production Engineering & Cloud Deployment Audits

To transition Apex Expeditions from a localized development build to an enterprise-grade, cloud-hosted production platform, a series of comprehensive architectural audits and infrastructure adaptations were engineered across every layer of the stack.

---

### ☁️ Cloud Service Ecosystem

The production deployment coordinates six specialized cloud platforms working in high-availability unison:

| Service Platform | Functional Scope | Cloud Tier & Architecture | Connectivity Protocol |
| :--- | :--- | :--- | :--- |
| **Vercel** | **Frontend Client (PWA)** | Edge Network & CDN; SPA rewrites via `vercel.json`; automated Vite builds; Workbox PWA service worker caching. | `HTTPS / HTTP/2` |
| **Render** | **REST API & Worker Engine** | Unified Linux container running Gunicorn WSGI server and Celery background workers simultaneously via `start.sh` process supervisor. | `HTTPS / Port 443` |
| **Neon** | **Relational Database** | Managed Serverless PostgreSQL 16 cluster; pooled connections (`sslmode=require`); transactional rollbacks; schema auto-seeding. | `postgresql://` (TLS) |
| **Upstash** | **In-Memory Cache & Broker** | Serverless Redis instance; sub-millisecond response caching for Flask-Caching; distributed message queue brokering for Celery. | `rediss://` (TLS) |
| **Brevo (Sendinblue)** | **Transactional Email Service** | Cloud email dispatch via HTTPS REST API (`sib-api-v3-sdk`); verified sender domain authentication; bypassed container firewall restrictions. | `REST HTTPS / Port 443` |
| **Cloudinary** | **Asset Delivery Network** | Cloud asset and expedition gallery media hosting with dynamic image optimization and secure upload tokens. | `HTTPS CDN` |

---

### 🛡️ Production Audits & Architectural Adaptations

#### 1. Outbound SMTP Firewall Bypass & Brevo HTTPS REST API Transition
> [!IMPORTANT]
> **Problem:** Cloud container platforms (including Render Free Tier) enforce strict network security policies that completely block outbound traffic on standard SMTP ports (`25`, `465`, and `587`) to prevent spam relay abuse. Traditional Python `smtplib` connections hung indefinitely and terminated with connection timeouts.  
> **Solution:** Refactored the core mailing engine in `backend/mail.py` and `backend/tasks.py` to utilize Brevo's cloud-native REST API via `sib-api-v3-sdk` over standard HTTPS (Port 443). Configured verified sender signatures (`Apex Expeditions <nohara1887@gmail.com>`), enabling reliable, instantaneous transactional dispatch with zero port-blocking friction.

#### 2. Dual Daemon Orchestration (`start.sh`) & Celery/Redis Graceful Fallbacks
> [!NOTE]
> **Problem:** Standard cloud web tiers only allocate a single exposed web process, leaving background task runners (Celery) unserved without purchasing expensive secondary worker services.  
> **Solution:** Engineered a lightweight bash supervisor (`start.sh`, executable via `chmod +x`) that orchestrates both the Celery worker daemon (`celery -A tasks.celery_app worker --loglevel=info --concurrency=2`) and the multi-threaded Gunicorn WSGI application server (`gunicorn -w 4 -b 0.0.0.0:$PORT app:app`) within a unified container. Additionally, implemented defensive try/except fallbacks across all API endpoints: if Redis or Celery encounters brief connectivity drops, tasks seamlessly fall back or log non-blocking warnings without halting the user's HTTP request.

#### 3. Strict Zero-DB Demo Simulation & Role Quarantine
> [!TIP]
> **Problem:** Allowing public portfolio evaluators to test Admin, Staff, and Trekker privileges could lead to malicious database mutation, deletion of production treks, or spamming real users.  
> **Solution:** Engineered a robust, JWT-based sandbox engine (`is_demo=True`). All mutation endpoints (booking reservations, trek creation, status updates, staff assignments, review submissions, ticket resolutions, and user suspensions) detect demo status and route execution through simulation interceptors. These generate authentic real-world responses while strictly suppressing database commits (`db.session.rollback()`). Furthermore, strict role quarantine prevents demo admins from altering real users or assigning non-demo staff to live expeditions.

#### 4. Ephemeral Demo Email Delivery Architecture
- **Interactive In-Memory Dispatch:** When evaluators trigger email-sending operations within demo roles (booking confirmations, cancellation alerts, password reset OTPs, telemetry history exports), the UI opens an interactive modal requesting a destination email address.
- **Privacy & Database Hygiene:** Evaluators are explicitly informed that their email is held only in ephemeral memory for the duration of the demo session and is never persisted to the PostgreSQL database.
- **Contextual Preview Banners:** All emails dispatched under demo mode automatically inject high-visibility contextual headers (`[DEMO PREVIEW] Dispatched for portfolio demonstration...`) to distinguish test transmissions from authentic operational directives.

#### 5. PostgreSQL Dialect Compatibility & Query Optimization
- **`func.avg` Ambiguity Resolution:** Diagnosed and resolved `psycopg2.errors.AmbiguousFunction: function avg(unknown) is not unique` occurring in PostgreSQL by replacing untyped string arguments with explicit SQLAlchemy column expressions (`func.avg(Review.rating)`).
- **Idempotent Schema Seeding:** Hardened `backend/app.py` auto-seeding routines with table existence verification and transaction rollback shielding, ensuring clean cold restarts without unique constraint collisions.
- **Non-Destructive Soft-Delete Auditing:** Standardized trek purges to toggle the `is_deleted=True` audit flag, safeguarding historical booking receipts and snapshot immutability while removing archived treks from active search indices.

#### 6. Anti-`<!DOCTYPE>` Error Shielding & JSON Standard Enforcement
- **Universal JSON Handlers:** Registered comprehensive HTTP error handlers (`400`, `404`, `405`, `500`, and uncaught `Exception`) in Flask to ensure that every server-side fault returns structured JSON (`{"message": ..., "status": ...}`).
- **Eliminating Frontend SyntaxErrors:** Completely eliminated the notorious `SyntaxError: Unexpected token '<', "<!DOCTYPE ... is not valid JSON"` error, ensuring the Vue 3 frontend always renders clean, informative error banners.

#### 7. Cold-Boot Server Warmup & Live Ping Handshake
- **Proactive Health Polling:** Because free-tier server containers spin down during periods of inactivity, a cold-boot warmup screen was integrated into the client application.
- **Dynamic UX Feedback:** Automatically pings `/api/utils/ping` with live status indicators, guiding the evaluator through container awakening before transitioning smoothly into the application portal.

#### 8. Obsidian Glassmorphism Hardening & SVG Icon Standards
- **Modal Transparency Fix:** Replaced fragile semi-transparent CSS modal backdrops with high-opacity obsidian frosted glass (`rgba(10, 15, 20, 0.95)`, `backdrop-filter: blur(16px)`), eliminating background card bleed-through and ensuring accessibility compliance.
- **Cross-Platform Icon Audit:** Replaced all legacy raw text glyphs and emojis (`←`, `→`) across all views with standard SVG Bootstrap Icons (`<i class="bi bi-arrow-left"></i>`), ensuring crisp, uniform rendering across all mobile and desktop operating systems.

#### 9. Cross-Client Responsive HTML Email Architecture
- **Email Client Compatibility:** Refactored all 8 email templates in `backend/tasks.py` from fragile CSS Flexbox layouts (which break in desktop Outlook and older email clients) to bulletproof, mobile-responsive HTML presentation tables (`<table role="presentation">`).
- **Dynamic Routing:** Replaced all hardcoded localhost URLs with dynamic environment variables (`FRONTEND_URL`), ensuring all action buttons, booking links, and review prompts redirect seamlessly to the live Vercel production deployment.

---

Mute the digital noise. Swap infinite feeds for open mountain horizons. <br>
Developed By: Kartikey Tripathi | IITM BS Degree Program