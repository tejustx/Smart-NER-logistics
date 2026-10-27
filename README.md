# NexTerra — Smart NER Logistics Control Platform

> An intelligent logistics and route-risk management platform designed for safer and more resilient transportation across the North Eastern Region (NER) of India.

##  Overview

**NexTerra** is a logistics decision-support platform designed to help logistics planners evaluate transportation routes using multiple real-world risk factors.

Instead of considering only distance or travel time, the platform combines information related to **weather, terrain, road conditions, disruptions, and geographic risk** to identify safer and more reliable routes.

The system is designed with resilience in mind, including support for connectivity-constrained environments.

---

##  Problem

Logistics movement across the North Eastern Region can be affected by:

- Heavy rainfall and adverse weather
- Landslides and terrain instability
- Road and corridor disruptions
- Difficult mountainous terrain
- Connectivity limitations
- Changing transportation conditions

Traditional navigation systems primarily optimize for factors such as distance and travel time. NexTerra focuses on **route safety and logistics risk** in addition to conventional routing factors.

---

##  Solution

NexTerra provides a centralized platform where logistics planners can:

1. Create and manage shipments
2. Evaluate transportation routes
3. Assess route risk
4. Consider environmental and geographic hazards
5. Identify safer alternative routes
6. Monitor active trips
7. Manage drivers and vehicles
8. Handle disruption information
9. Support operations during limited connectivity

---

##  Key Features

###  Risk-Aware Route Evaluation
Routes are evaluated using multiple factors instead of relying only on distance.

###  Weather Risk
Weather information can be incorporated into route-risk assessment to identify potentially hazardous conditions.

###  Terrain & Slope Analysis
Terrain information and slope gradients are considered when evaluating corridor risk.

###  Road & Disruption Information
Road conditions and reported disruptions can influence route recommendations.

###  Hazard Compounding
Multiple hazards can interact rather than being treated as completely independent risks. NexTerra uses a non-linear risk approach to represent compounding hazards.

###  MCDA Risk Engine
A Multi-Criteria Decision Analysis (MCDA) approach combines multiple risk factors into an overall route-risk score.

### Safer Route Recommendation
When a route has significant risk, the system can evaluate alternatives and recommend a safer corridor.

###  Shipment Management
Users an create shipments and associate them with vehicles, routes, and transportation information.

###  Driver & Vehicle Management
The platform maintains information about available drivers and vehicles for logistics operations.

###  Offline-First Resilience
The system is designed to support store-and-forward operation when connectivity is temporarily unavailable.

---

##  System Architecture

```text
                    ┌─────────────────────┐
                    │      Frontend       │
                    │  Web Dashboard/UI   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     FastAPI API     │
                    │      Backend        │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        ┌───────────┐    ┌────────────┐   ┌─────────────┐
        │ Supabase  │    │ Risk Engine│   │ External    │
        │ PostgreSQL│    │   / GIS    │   │ Data Sources│
        └───────────┘    └────────────┘   └─────────────┘
                               │
                               ▼
                       ┌────────────────┐
                       │ Route Evaluation│
                       │ & Recommendation│
                       └────────────────┘
```

---

##  Technology Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Supabase

### Frontend
- HTML
- CSS
- JavaScript
- MapLibre GL JS

### Geospatial & Mapping
- GIS
- MapLibre GL JS
- CartoDEM
- PostGIS

### Data & Risk Analysis
- Weather data
- Terrain and slope information
- Landslide/disruption information
- Road-risk information
- MCDA-based risk evaluation

### Data Sources / APIs
- Open-Meteo
- ISRO Bhuvan Geo-Platform
- IMD Automatic Weather Stations
- CartoDEM

---

##  Project Structure

```text
NexTerra/
│
├── backend/
│   ├── db/
│   ├── routers/
│   ├── services/
│   ├── data/
│   └── ...
│
├── frontend/
│   ├── css/
│   ├── js/
│   └── index.html
│
├── tests/
│
├── scratch/
│
├── .env.example
├── .gitignore
├── config.yml
├── DATASETS_DOCUMENTATION.md
├── SMART_NER_LOGISTICS_DATASETS.xlsx
├── start_server.bat
└── README.md
```

> Local databases, environment variables, generated files, and other development-only artifacts are excluded from version control.

---

##  Getting Started

### 1. Clone the repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd <YOUR-REPOSITORY-NAME>
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r backend/requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example` as a reference.

Add the required database configuration, including the Supabase PostgreSQL connection string.

**Never commit `.env` to GitHub.**

### 5. Start the backend

Use the project's startup script:

```powershell
.\start_server.bat
```

Or start FastAPI manually according to the backend configuration.

### 6. Open the application

Once the server is running, open the local frontend/application URL provided by the project.

---

##  Security

The repository intentionally excludes sensitive and local development files such as:

- `.env`
- Database files
- Virtual environments
- Python cache files
- Generated test outputs

Database credentials and API keys should always be stored in environment variables.

---

##  Risk Evaluation Concept

NexTerra evaluates route safety using multiple criteria.

A conceptual route-risk model can be represented as:

```text
Route Risk
    │
    ├── Weather Risk
    ├── Terrain / Slope Risk
    ├── Landslide Risk
    ├── Road Condition Risk
    └── Disruption Risk
             │
             ▼
       Risk Engine
             │
             ▼
      Overall Risk Score
             │
             ▼
    Route Comparison
             │
             ▼
   Safer Route Recommendation
```

The system can also model **non-linear hazard compounding**, where the combined effect of multiple hazards may be greater than simply adding their individual contributions.

---

##  Database

The application uses **PostgreSQL through Supabase** for persistent application data.

The current database structure includes entities such as:

- Users
- Drivers
- Vehicles
- Shipments
- Trips
- Disruptions

Local SQLite data is used only for development/fallback scenarios and is not committed to the repository.

---

##  Future Scope

Potential future improvements include:

- Machine-learning-based risk prediction
- Real-time hazard updates
- More detailed landslide prediction
- Dynamic route optimization
- Advanced predictive maintenance
- Improved offline synchronization
- Additional regional datasets
- Real-time logistics analytics
- More advanced multi-objective optimization

---

##  Project

**Project:** NexTerra — Smart NER Logistics Control Platform

**Domain:** Logistics & Transportation

**Region:** North Eastern Region (NER), India

**Purpose:** Safer, risk-aware and resilient logistics planning

---

##  Documentation

Additional project documentation and datasets are available within this repository.

- Dataset documentation
- Frontend documentation
- Dataset workbook
- Technical project files

---

##  Project Vision

> **Making logistics decisions safer, smarter, and more resilient in challenging terrains.**