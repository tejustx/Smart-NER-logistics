"""
Cargo Allocation API Router
USP 2: Multi-Tier Cargo Prioritization & Capacity Allocation
"""

from fastapi import APIRouter, HTTPException
from backend.models.schemas import AllocationRequest, AllocationResult
from backend.services.allocation_engine import allocate_cargo_capacity
from backend.services.state_store import state_store

router = APIRouter(prefix="/api/allocation", tags=["Cargo Allocation & Manifest"])

@router.post("/optimize", response_model=AllocationResult)
def optimize_allocation(req: AllocationRequest):
    """
    Solves USP 2:
    Given limited vehicle payload/volume and route conditions, prioritizes Tier 1 (Medical),
    then Tier 2 (Essential), allocating capacity and staging excess into waiting state.
    """
    vehicle = state_store.vehicles.get(req.vehicle_id)
    if not vehicle:
        # Fallback to default vehicle if not found
        vehicle = list(state_store.vehicles.values())[0]

    # Check if route has hazard constraints
    route_safety_factor = 1.0
    if req.route_id == "RO-NER-A":
        # High risk route restricts safety payload by 20% to avoid axle breakage on mud
        route_safety_factor = 0.80

    result = allocate_cargo_capacity(
        vehicle=vehicle,
        cargo_items=req.cargo_items,
        route_safety_payload_factor=route_safety_factor
    )
    return result
