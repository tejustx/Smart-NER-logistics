"""
Alerts and Disruptions API Router
Dynamic alerts, road blockages, and reroute trigger events
"""

from fastapi import APIRouter
from typing import List, Dict, Any
from backend.models.schemas import Disruption
from backend.services.state_store import state_store

router = APIRouter(prefix="/api/alerts", tags=["Alerts & Disruptions"])

@router.get("/", response_model=List[Disruption])
def list_disruptions():
    """Returns all active road hazards, landslides, and flash flood alerts across NER."""
    return list(state_store.disruptions.values())

@router.post("/trigger-reroute")
def trigger_reroute_event(disruption_id: str = "DISR-01") -> Dict[str, Any]:
    """
    Simulates section 12 in MVP spec:
    Road Closure / Rising Risk / Critical Warning -> Alert Generated -> Route Recalculation -> New Recommended Route
    """
    disruption = state_store.disruptions.get(disruption_id) or list(state_store.disruptions.values())[0]

    return {
        "status": "reroute_triggered",
        "alert_id": disruption.id,
        "hazard": disruption.title,
        "affected_corridor": disruption.corridor_name,
        "action_taken": "Route A penalized into CRITICAL state (Risk Score 94.2/100).",
        "mandatory_reroute": "Switching dispatched convoys to Route B: NH-27 Southern Corridor.",
        "driver_impact": "Dispatched dynamic reroute packet. Driver will receive on next cellular heartbeat or view cached detour instructions.",
        "time_penalty_avoided_hours": 12.5
    }
