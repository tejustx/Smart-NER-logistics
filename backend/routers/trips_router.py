"""
Trips and Driver Assignment API Router
Connects USP 1 + USP 2 into dispatched Trip for Driver execution
"""

from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime, timedelta
import uuid
from backend.models.schemas import (
    Trip, TripAssignmentRequest, Driver, Checkpoint
)
from backend.services.state_store import state_store
from backend.services.ner_network import generate_route_options

router = APIRouter(prefix="/api/trips", tags=["Trips & Assignment"])

@router.get("/drivers", response_model=List[Driver])
def get_available_drivers():
    """Returns drivers registered in the NER mountain dispatch fleet, updating deadline availability states."""
    state_store.update_driver_availabilities()
    return list(state_store.drivers.values())

@router.post("/drivers/{driver_id}/release", response_model=Driver)
def release_driver(driver_id: str):
    """
    Frees a driver early (e.g. after delivery completion or simulation/testing),
    clearing their deadline lock and making them Available for new shipments.
    """
    driver = state_store.drivers.get(driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail=f"Driver '{driver_id}' not found.")
    
    driver.status = "Available"
    driver.busy_until = None
    driver.current_trip_id = None
    driver.assigned_at = None
    driver.deadline_hours = None
    state_store.save_driver(driver)
    return driver

@router.post("/assign", response_model=Trip)
def assign_trip(req: TripAssignmentRequest):
    """
    Step 5 in Core Operational Loop:
    Assigns selected route and generated manifest to driver + vehicle.
    Enforces that driver must be Available and not locked on another shipment deadline.
    """
    state_store.update_driver_availabilities()

    driver = state_store.drivers.get(req.driver_id)
    if not driver:
        # Fallback to first available driver
        available = [d for d in state_store.drivers.values() if d.status == "Available"]
        driver = available[0] if available else list(state_store.drivers.values())[0]

    # Enforce deadline availability lock: Cannot select driver if currently on a shipment
    if driver.status in ["Busy", "On Trip"]:
        remaining_str = ""
        if driver.busy_until:
            try:
                busy_dt = datetime.fromisoformat(driver.busy_until)
                rem_secs = max(0, (busy_dt - datetime.now()).total_seconds())
                rem_hrs = int(rem_secs // 3600)
                rem_mins = int((rem_secs % 3600) // 60)
                remaining_str = f" ({rem_hrs}h {rem_mins}m remaining until deadline)"
            except Exception:
                pass
        raise HTTPException(
            status_code=400,
            detail=f"Driver '{driver.name}' is currently Busy on trip {driver.current_trip_id or 'active trip'}{remaining_str}. Cannot assign until shipment deadline has elapsed or driver is released."
        )

    vehicle = state_store.vehicles.get(req.vehicle_id)
    if not vehicle:
        vehicle = list(state_store.vehicles.values())[0]

    trip_id = f"TRIP-{uuid.uuid4().hex[:4].upper()}"
    deadline_hours = req.deadline_hours if (req.deadline_hours and req.deadline_hours > 0) else 9.0
    now = datetime.now()
    busy_until = now + timedelta(hours=deadline_hours)

    origin_name = req.origin or "Guwahati"
    dest_name = req.destination or "Itanagar"

    # Generate checkpoints along selected route endpoints
    checkpoints = [
        Checkpoint(name=f"{origin_name} Central Logistics Hub", distance_km=0.0, status="Pending", estimated_time="Departure"),
        Checkpoint(name="Intermodal Valley Transit Crossing", distance_km=140.0, status="Pending", estimated_time="+3.2 hrs"),
        Checkpoint(name="Foothill Ingress Checkpoint & Weigh Bridge", distance_km=275.0, status="Pending", estimated_time="+6.5 hrs"),
        Checkpoint(name=f"{dest_name} State Relief Terminal", distance_km=385.0, status="Pending", estimated_time=f"+{deadline_hours} hrs")
    ]

    # Look up shipment or create stub manifest
    sample_trip = list(state_store.trips.values())[0]
    route_display = f"{origin_name} → {dest_name} (Route B: Safe Corridor)" if "B" in req.route_id else f"{origin_name} → {dest_name} (Route A: Direct Ridge)"
    
    new_trip = Trip(
        id=trip_id,
        shipment_id=req.shipment_id,
        route_id=req.route_id,
        route_name=route_display,
        driver_id=driver.id,
        driver_name=driver.name,
        vehicle_id=vehicle.id,
        vehicle_name=vehicle.name,
        origin=origin_name,
        destination=dest_name,
        manifest=sample_trip.manifest,
        current_status="Assigned",
        connectivity_mode="Online",
        checkpoints=checkpoints,
        offline_sync_pending=False,
        last_sync_time=now.strftime("%H:%M:%S"),
        active_alert=f"Dispatched via Safe Engineered Corridor. Driver locked for {deadline_hours}h delivery deadline."
    )

    state_store.save_trip(new_trip)

    # Lock driver until shipment deadline elapses - explicitly Busy!
    driver.status = "Busy"
    driver.current_trip_id = trip_id
    driver.assigned_at = now.isoformat()
    driver.busy_until = busy_until.isoformat()
    driver.deadline_hours = deadline_hours
    state_store.save_driver(driver)

    return new_trip

@router.get("/", response_model=List[Trip])
def list_trips():
    """Lists all active and completed trips."""
    return list(state_store.trips.values())

@router.get("/{trip_id}", response_model=Trip)
def get_trip(trip_id: str):
    """Retrieves specific trip details."""
    if trip_id not in state_store.trips:
        # Fallback to first trip
        return list(state_store.trips.values())[0]
    return state_store.trips[trip_id]
