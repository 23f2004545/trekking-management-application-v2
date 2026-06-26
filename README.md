# 🏔️ Apex Expeditions - Wilderness Operations Portal

**Apex** is a comprehensive, decoupled, enterprise-grade web application engineered for high-altitude trekking logistics. It serves as a unified operational telemetry platform connecting **Explorers (Trekkers)**, **Field Guides (Staff)**, and **Central Command (Admins)**. It handles everything from secure geographical mapping and live manifest tracking to asynchronous data exporting and cryptographic passwordless authentication.

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
│   ├── controller/
│   │   ├── models.py        # Database Schema (User, Trek, Booking, Tickets, etc.)
│   │   └── extensions.py    # SQLAlchemy, JWT, Cache Initialization
│   └── routes/              # Blueprint Modules
│       ├── admin_bp.py      # Infrastructure, Staff Auth, Fleet Management
│       ├── auth_bp.py       # Passwordless OTP & JWT Rotations
│       ├── staff_bp.py      # Guide Manifests & Operations
│       ├── trekker_bp.py    # Explorer Bookings & Payments
│       └── utils_bp.py      # Shared History Aggregations & Support Desk
│
└── frontend/                # Vue.js 3 SPA
    ├── index.html           # PWA Entry Point
    ├── vite.config.js       # Vite & PWA Plugin Configurations
    ├── src/
    │   ├── main.js          # Vue App Initialization
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

--- 

- Access the client portal at http://localhost:5173

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

Mute the digital noise. Swap infinite feeds for open mountain horizons. 
Developed By: Kartikey Tripathi | IITM BS Degree Program