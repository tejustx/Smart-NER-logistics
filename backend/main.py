"""
Smart NER Logistics Control Platform
Main FastAPI Backend Server & Static Application Host
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.routers.routes_router import router as routes_router
from backend.routers.shipments_router import router as shipments_router
from backend.routers.allocation_router import router as allocation_router
from backend.routers.trips_router import router as trips_router
from backend.routers.driver_router import router as driver_router
from backend.routers.government_router import router as government_router
from backend.routers.alerts_router import router as alerts_router
from backend.routers.auth_router import router as auth_router
from backend.routers.risk_router import router as risk_router
from backend.models.schemas import PlanAndAllocateRequest
from backend.services.ner_network import generate_unified_plan_and_allocation
from backend.db.database import check_db_connection

app = FastAPI(
    title="Smart NER Logistics Control Platform API",
    description="Risk-Weighted Dynamic Freight Rerouting, Multi-Tier Cargo Prioritization & Low-Bandwidth Offline Navigation for India's North Eastern Region (NER).",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(auth_router)
app.include_router(routes_router)
app.include_router(risk_router)
app.include_router(shipments_router)
app.include_router(allocation_router)
app.include_router(trips_router)
app.include_router(driver_router)
app.include_router(government_router)
app.include_router(alerts_router)

# Unified Execution Core Endpoint (Feature A + Feature B)
@app.post("/api/plan-and-allocate")
def unified_plan_and_allocate(payload: PlanAndAllocateRequest):
    """
    Combined Planning & Knapsack Cargo Allocation Endpoint (SIH PS 26002 Feature A + B).
    Generates Pareto-dominant route with ML forward risk predictions (6h/12h/24h)
    and executes Greedy Knapsack packing prioritizing Tier 1 emergency cargo.
    """
    return generate_unified_plan_and_allocation(
        origin=payload.origin,
        destination=payload.destination,
        cargo_items=payload.cargo_items,
        vehicle_id=payload.vehicle_id
    )

@app.get("/api/health")
def health_check():
    db_info = check_db_connection()
    return {
        "status": "healthy",
        "platform": "Smart NER Logistics Control Platform",
        "region": "North Eastern Region (NER) - Assam, Arunachal Pradesh, Meghalaya, Nagaland, Manipur, Mizoram, Tripura, Sikkim",
        "database": db_info,
        "version": "1.0.0"
    }

# Mount Static Files (CSS, JS, Assets)
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")

if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/")
    @app.get("/signup")
    @app.get("/register")
    @app.get("/login")
    def serve_frontend_index():
        index_file = os.path.join(frontend_dir, "index.html")
        return FileResponse(
            index_file,
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
