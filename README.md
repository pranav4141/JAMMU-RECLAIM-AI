# 🏙️ JAMMU RECLAIM AI

### **Discover. Prioritise. Transform.**

> **AI-assisted Urban Opportunity & Green Planning Platform for Jammu District, Jammu & Kashmir, India**

JAMMU RECLAIM AI is a GIS and AI-assisted urban planning platform that identifies potentially underutilised urban spaces, evaluates their public and environmental value, prioritises locations for intervention, and recommends suitable interventions such as **pocket parks, rain gardens, urban forests, green corridors, and community spaces**.

**📍 Study Region: Jammu District, Jammu & Kashmir, India only**

---

## 🎯 Problem

Urban authorities need to determine **where limited urban space and resources can create the greatest public and environmental benefit**.

Identifying potential underutilised spaces is only the first step. Each location may have different:

- Population needs
- Accessibility
- Green-space deficiency
- Heat exposure
- Stormwater/flood risk
- Area suitability
- Nearby public facilities

JAMMU RECLAIM AI combines these factors into one decision-support platform to help answer:

> **“Where should Jammu intervene first, and what should be done there?”**

---

## 💡 Our Solution

JAMMU RECLAIM AI follows a simple pipeline:

```text
🛰️ GIS + Satellite Data
        ↓
🔍 Candidate Site Identification
        ↓
📊 Site Analysis
        ↓
🎯 Site Prioritisation
        ↓
🤖 AI-Assisted Recommendation
        ↓
🏙️ Priority Action
```

The platform transforms fragmented urban data into **location-specific, actionable planning recommendations**.

---

## 🚀 Key Features

### 🗺️ Interactive Jammu District Map

Explore candidate urban sites through an interactive GIS map with:

- Jammu District boundary
- Candidate sites
- Priority locations
- Environmental indicators
- Potential urban-change alerts

> All project analysis is strictly restricted to **Jammu District**.

---

### 🤖 AI-Assisted Intervention Recommendations

The system analyses site characteristics and recommends an appropriate intervention.

Possible recommendations include:

🌳 **Urban Forest**  
🌱 **Pocket Park**  
🌧️ **Rain Garden**  
🚶 **Green Corridor**  
🏘️ **Community Space**  
🏞️ **Public Plaza**  
🌿 **Green Buffer**

Example:

```text
Low Green Cover
+
High Population
+
Good Accessibility
+
High Heat Exposure
        ↓
🌳 POCKET PARK
```

The current prototype uses a **transparent rule-based recommendation engine**, making its decisions explainable.

---

### 🔎 Urban Change Monitoring

JAMMU RECLAIM AI also includes a prototype **Urban Change Monitor**.

It compares historical and recent imagery to flag potential land-use or building changes.

```text
Historical Image
       ↓
Current Image
       ↓
Change Detection
       ↓
Potential Urban Change
       ↓
Field Verification
```

⚠️ The system does **not** automatically declare construction illegal.

It reports:

> **“Potential unauthorised change — field verification required.”**

This keeps the system suitable for real-world municipal decision support.

---

## 🌱 From Underutilised Space to Urban Asset

JAMMU RECLAIM AI doesn't stop at identifying a location.

It answers:

### **What should Jammu do with it?**

Example:

**BEFORE**

Underutilised open space  
↓  
Low greenery  
↓  
Low public value

**AFTER**

🌳 Pocket Park  
🌧️ Rain Garden  
🚶 Walking Area  
🌿 Native Vegetation

The platform can provide a conceptual before/after planning recommendation.

---

## 🧠 What Makes It Innovative?

### 1️⃣ Site Prioritisation
Combines multiple urban, demographic and environmental factors to identify locations where intervention can create the greatest potential benefit.

### 2️⃣ Site-Specific Recommendations
Instead of simply identifying vacant/underutilised spaces, the platform recommends **what intervention fits each location**.

### 3️⃣ Urban Change Monitoring
Historical/current imagery can flag potential land-use changes for further investigation.

### 4️⃣ Jammu-Specific Decision Intelligence
The entire analysis is designed specifically for **Jammu District**, rather than applying generic urban-planning assumptions.

---

## 👥 Potential Users

The platform can support:

- 🏛️ **Jammu Municipal Corporation / Urban Authorities**
- 🗺️ **Urban Planners**
- 🌳 **Parks & Environment Departments**
- 🏗️ **Infrastructure & Development Agencies**
- 🏙️ **Smart City / Urban Development Teams**
- 👥 **Local Communities & Planning Organisations**

---

## 📈 Expected Impact

JAMMU RECLAIM AI aims to help Jammu:

- ♻️ Better utilise underused urban spaces
- 🌳 Increase access to green and recreational spaces
- 🌧️ Improve stormwater-resilient planning
- 🌡️ Address heat-prone areas through targeted greenery
- 🔎 Identify potential urban changes earlier
- 💰 Prioritise limited municipal resources
- 📊 Shift from fragmented assessment to data-driven planning

### Core Impact

> **From “Where is unused space?” to “Which space should we transform first, why, and what should we build there?”**

---

## 🛠️ Technology Stack

### Frontend

- React
- Vite
- TypeScript
- Tailwind CSS
- React-Leaflet
- Leaflet
- Recharts
- Lucide React

### Backend

- Python
- FastAPI

### GIS & Data

- GeoJSON
- OpenStreetMap
- Point-in-polygon validation
- Satellite imagery
- Planned Sentinel-2 / Landsat integration

---

## 🗂️ Project Structure

```text
jammu-reclaim-ai/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── maps/
│   │   ├── charts/
│   │   ├── services/
│   │   └── data/
│   └── public/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   ├── services/
│   │   ├── models/
│   │   └── scoring/
│   └── requirements.txt
│
├── data/
│   ├── sites.json
│   ├── jammu_district_boundary.geojson
│   ├── generate.py
│   └── test_geo.py
│
└── README.md
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/jammu-reclaim-ai.git
cd jammu-reclaim-ai
```

### Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

### Run Backend

In a new terminal:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

---

## 🧪 Testing

### Geographic Boundary Validation

```bash
python3 data/test_geo.py
```

This validates candidate coordinates against the **Jammu District boundary**.

### Frontend Tests

```bash
cd frontend
npm test
```

---

## 🔌 API Endpoints

```text
GET /api/sites
GET /api/sites/{id}
GET /api/statistics
GET /api/recommendations/{id}
GET /api/rankings
GET /api/encroachments
GET /api/regions
```

---

## 🛰️ Planned Satellite Integration

The architecture is designed to support future integration with:

- **Sentinel-2**
- **Landsat**
- NDVI
- NDWI
- NDBI
- Land-cover classification
- Change detection

The current prototype should **not** claim live satellite processing until the integration is actually connected and validated.

---

## 📍 Geographic Scope

### STRICTLY:

**Jammu District, Jammu & Kashmir, India**

The system ensures:

- Candidate sites are validated against the Jammu District boundary.
- Spatial analysis is restricted to the district.
- Locations outside the boundary are excluded.
- Surrounding areas visible on the basemap are **context only**.
- Pakistan and neighbouring districts are **not included in project analysis**.

---

## ⚠️ Data Honesty & Limitations

The current prototype uses:

> **Prototype / Demonstration Data**

It does not claim official:

- JMC land ownership data
- Municipal vacant-land records
- Confirmed illegal construction records
- Official flood-risk data
- Official impact statistics

The current recommendation engine is **rule-based**, not a trained ML model.

Urban change detection is currently a **prototype/simulated module**.

All potential encroachment/change alerts require:

> **Field verification by the relevant authority.**

Prototype impact estimates should be validated using authoritative datasets before real-world implementation.

---

## 💰 Estimated Prototype Cost

### **₹15,000 – ₹25,000**

The first prototype can be developed primarily using:

- Open-source software
- OpenStreetMap
- Freely accessible satellite/geospatial datasets
- Open-source GIS tools

Full-scale deployment may require additional investment in:

- High-resolution imagery
- Cloud infrastructure
- Official datasets
- Field surveys
- Municipal integrations
- Automated monitoring

---

## 🗺️ Roadmap

### Phase 1 — Prototype

- Jammu District pilot
- Candidate-site database
- Site prioritisation
- Recommendation engine
- Interactive GIS dashboard

### Phase 2 — Real-Data Pilot

- Official municipal datasets
- Higher-resolution imagery
- Field verification
- Real GIS/OSM integration
- Ward-level planning

### Phase 3 — Urban Intelligence Platform

- Automated satellite analysis
- Advanced change detection
- Trained ML models
- Continuous monitoring
- Municipal system integration
- Predictive urban planning

---

## 🌟 Vision

> **JAMMU RECLAIM AI turns overlooked urban spaces into data-driven opportunities — helping Jammu discover where to act, prioritise what matters most, and plan what should come next.**

### **DISCOVER. PRIORITISE. TRANSFORM.**

---

## 📜 Disclaimer

JAMMU RECLAIM AI is a **hackathon prototype and decision-support concept**. It is not intended to replace official land records, municipal surveys, legal processes, engineering assessments, environmental clearances, or field verification.

---

### 🏙️ Built for the Jammu Smart City Hackathon

**Focus:** Urban Planning, Green Spaces & Public Realm  
**Geographic Scope:** Jammu District, Jammu & Kashmir, India
