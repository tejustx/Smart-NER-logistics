"""
Driver and Offline Navigation API Router
USP 3: Low-Bandwidth Offline-First Driver Navigation & Telemetry Sync
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from datetime import datetime
from backend.models.schemas import Trip, SyncTelemetryPayload
from backend.services.state_store import state_store

router = APIRouter(prefix="/api/driver", tags=["Driver & Offline Navigation"])

@router.get("/assigned-trip", response_model=Trip)
def get_driver_assigned_trip():
    """
    Returns the most recent active trip assigned in the platform.
    This payload is packaged for offline local caching (IndexedDB/localStorage)
    containing full route segments, cargo manifest, checkpoints, and emergency alerts.
    """
    # Return latest assigned trip or fallback to canonical trip
    if state_store.trips:
        trip = list(state_store.trips.values())[-1]
    else:
        trip = state_store.trips.get("TRIP-1024")
    if not trip:
        raise HTTPException(status_code=404, detail="No active trips found.")
    return trip

@router.post("/toggle-connectivity")
def toggle_connectivity(mode: str = "Offline") -> Dict[str, Any]:
    """
    Simulates entering or exiting low-connectivity mountain zone (e.g. Bhalukpong Gorge / Sela Pass).
    Mode: "Offline" or "Online"
    """
    trip = state_store.trips.get("TRIP-1024") or list(state_store.trips.values())[0]
    trip.connectivity_mode = mode
    trip.last_sync_time = datetime.now().strftime("%H:%M:%S")
    return {
        "status": "success",
        "trip_id": trip.id,
        "new_connectivity_mode": mode,
        "message": f"Driver connectivity mode updated to {mode}."
    }

@router.post("/sync-telemetry")
def sync_offline_telemetry(payload: SyncTelemetryPayload) -> Dict[str, Any]:
    """
    USP 3 Reconnection Handler:
    Called when connectivity returns. Batches queued delivery checkpoints,
    delivery confirmations, offline driver notes, and GPS breadcrumbs to the platform.
    """
    trip = state_store.trips.get(payload.trip_id) or list(state_store.trips.values())[0]

    # Update passed checkpoints
    for chk in trip.checkpoints:
        if chk.name in payload.completed_checkpoint_names:
            chk.status = "Passed"
            if not chk.passed_at:
                chk.passed_at = datetime.now().strftime("%I:%M %p")

    # Update delivered items in manifest
    for item in trip.manifest.allocated_items:
        if item.id in payload.delivered_cargo_item_ids:
            item.status = "Delivered"

    # Check if all delivered
    all_delivered = all(item.status == "Delivered" for item in trip.manifest.allocated_items)
    if all_delivered:
        trip.current_status = "Delivered"
    else:
        trip.current_status = "En Route"

    trip.connectivity_mode = "Online"
    trip.offline_sync_pending = False
    trip.last_sync_time = datetime.now().strftime("%H:%M:%S")
    state_store.save_trip(trip)

    sync_record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "trip_id": trip.id,
        "driver_id": payload.driver_id,
        "checkpoints_synced": len(payload.completed_checkpoint_names),
        "deliveries_synced": len(payload.delivered_cargo_item_ids),
        "notes": payload.local_offline_notes or "Regular sync on cellular recovery.",
        "battery_pct": payload.battery_level_pct
    }
    state_store.sync_logs.append(sync_record)

    return {
        "status": "synchronized",
        "trip_id": trip.id,
        "current_status": trip.current_status,
        "synced_checkpoints": payload.completed_checkpoint_names,
        "synced_deliveries": payload.delivered_cargo_item_ids,
        "sync_time": trip.last_sync_time,
        "message": f"Successfully synced {len(payload.completed_checkpoint_names)} checkpoints and {len(payload.delivered_cargo_item_ids)} delivery confirmations back to Control Room."
    }

@router.get("/sync-logs")
def get_sync_logs() -> List[Dict[str, Any]]:
    """Returns telemetry sync audit records from drivers."""
    return state_store.sync_logs
