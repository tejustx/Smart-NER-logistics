"""
Government / Control-Room API Router
Regional risk oversight, critical corridor accessibility, and What-If disruption simulation
"""

from fastapi import APIRouter
from typing import Dict, Any, List
from datetime import datetime
import uuid
from backend.models.schemas import WhatIfSimulationRequest, WhatIfSimulationResult
from backend.services.state_store import state_store
from backend.services.ner_network import CORRIDORS, NER_HUBS

router = APIRouter(prefix="/api/gov", tags=["Government / Control-Room"])

@router.get("/regional-overview")
def get_regional_overview() -> Dict[str, Any]:
    """
    Returns high-level regional risk situation, corridor states, and critical facility metrics.
    Data tags clearly reflect LIVE, HISTORICAL, and SIMULATED data streams.
    """
    active_trips_count = len(state_store.trips)
    active_disruptions = [d for d in state_store.disruptions.values() if d.status == "Active"]
    
    # Calculate regional accessibility score (0-100%)
    # Base 92% minus penalties for active critical disruptions
    penalty = sum(12.0 if d.severity == "Critical" else 6.0 for d in active_disruptions)
    accessibility_score = max(round(92.0 - penalty, 1), 40.0)

    return {
        "regional_accessibility_index": accessibility_score,
        "accessibility_rating": "Moderate Stress" if accessibility_score < 75 else "Stable Operation",
        "active_freight_trips": active_trips_count,
        "active_disruptions_count": len(active_disruptions),
        "monitored_corridors_count": len(CORRIDORS),
        "critical_supply_lines": CORRIDORS,
        "affected_districts": [
            {"district": "Papum Pare (Arunachal Pradesh)", "vulnerability": "High", "risk_factor": "Foothill Slope Mudslides", "isolated_facilities": 2},
            {"district": "Sonitpur (Assam)", "vulnerability": "Medium", "risk_factor": "Brahmaputra Bank Surge", "isolated_facilities": 0},
            {"district": "Kohima (Nagaland)", "vulnerability": "High", "risk_factor": "Pagla Pahar Subsidence", "isolated_facilities": 1},
            {"district": "East Khasi Hills (Meghalaya)", "vulnerability": "Low", "risk_factor": "Dense Mountain Fog", "isolated_facilities": 0}
        ],
        "data_transparency_summary": {
            "live_streams": ["GPS Telemetry", "Driver Status Sync", "Brahmaputra Water Gauges"],
            "historical_models": ["30-Year Landslide Frequency Atlas", "Slope Gradient Contours", "Road Pavement Degradation"],
            "simulated_inputs": ["Monsoon Cloudburst Telemetry (84mm/hr)", "Banderdewa Landslide Trigger Event"]
        }
    }

@router.post("/what-if-simulate", response_model=WhatIfSimulationResult)
def run_what_if_simulation(req: WhatIfSimulationRequest):
    """
    What-If Disruption Simulator:
    Temporarily blocks a chosen corridor and calculates ripple impacts:
    affected shipments, stranded tonnage, average detour km, added delay hours,
    additional fuel surcharge, and alternate recommended corridors.
    """
    corridor = next((c for c in CORRIDORS if c["id"] == req.blocked_corridor_id), CORRIDORS[0])

    if req.blocked_corridor_id == "CORR-NH27":
        tonnage = 8400.0
        shipments = 6
        detour_km = 94.0
        delay_hours = 3.8
        fuel_cost = 24500.0
        alt_route = "NH-715 via Kaliabhomora -> North Bank Elevated Spur"
        accessibility_drop = "Drops by 16.5% (Severe Inter-State Choke)"
    elif req.blocked_corridor_id == "CORR-NH415":
        tonnage = 3200.0
        shipments = 3
        detour_km = 62.6
        delay_hours = 1.9
        fuel_cost = 14200.0
        alt_route = "Route B: Southern Bypass via Tezpur Bridge & Naharlagun Expressway"
        accessibility_drop = "Drops by 8.4% (Papum Pare Hill Ingress Restrained)"
    else:
        tonnage = 4200.0
        shipments = 4
        detour_km = 75.0
        delay_hours = 2.4
        fuel_cost = 18000.0
        alt_route = "Secondary BRO Ridge Feeder Axis (Restricted to 4x4)"
        accessibility_drop = "Drops by 11.2% (Moderate Corridor Restriction)"

    return WhatIfSimulationResult(
        simulation_id=f"SIM-{uuid.uuid4().hex[:6].upper()}",
        blocked_corridor_id=corridor["id"],
        blocked_corridor_name=corridor["name"],
        highway_ref=corridor["highway"],
        affected_shipments_count=shipments,
        stranded_tonnage_kg=tonnage,
        avg_detour_increase_km=detour_km,
        avg_delay_hours=delay_hours,
        additional_fuel_cost_inr=fuel_cost,
        suggested_alternative_route=alt_route,
        regional_accessibility_index_change=accessibility_drop
    )
