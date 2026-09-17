"""
Shipments API Router
Handles shipment planning, cargo definition, and vehicle selection.
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from datetime import datetime
import uuid
from backend.models.schemas import Shipment, ShipmentCreate, Vehicle, CargoItem
from backend.services.state_store import state_store

router = APIRouter(prefix="/api/shipments", tags=["Shipment Planning"])

@router.get("/vehicles", response_model=List[Vehicle])
def get_available_vehicles():
    """Returns list of transport vehicles suitable for mountain terrain."""
    return list(state_store.vehicles.values())

@router.get("/sample-cargo", response_model=List[CargoItem])
def get_sample_cargo():
    """Returns preset 4-tier cargo data for instant demo initialization."""
    return [
        CargoItem(
            id="CRG-DEMO-01",
            name="Emergency Pediatric Vaccines & Antivenom",
            tier=1,
            tier_name="Tier 1 Medical/Emergency",
            weight_kg=220.0,
            volume_m3=1.1,
            deadline_hours=7.0,
            status="Waiting",
            recipient_facility="Papum Pare District General Hospital"
        ),
        CargoItem(
            id="CRG-DEMO-02",
            name="Whole Blood Units & Plasma Coolers",
            tier=1,
            tier_name="Tier 1 Medical/Emergency",
            weight_kg=140.0,
            volume_m3=0.8,
            deadline_hours=5.0,
            status="Waiting",
            recipient_facility="TRIHMS Emergency Trauma Wing"
        ),
        CargoItem(
            id="CRG-DEMO-03",
            name="Flood Relief Grain Bags & Fortified Rice",
            tier=2,
            tier_name="Tier 2 Essential Goods",
            weight_kg=1850.0,
            volume_m3=6.8,
            deadline_hours=16.0,
            status="Waiting",
            recipient_facility="State Civil Supplies Warehouse"
        ),
        CargoItem(
            id="CRG-DEMO-04",
            name="Packaged Drinking Water & Water Purification Tablets",
            tier=2,
            tier_name="Tier 2 Essential Goods",
            weight_kg=980.0,
            volume_m3=4.2,
            deadline_hours=20.0,
            status="Waiting",
            recipient_facility="Disaster Management Logistics Depot"
        ),
        CargoItem(
            id="CRG-DEMO-05",
            name="Reinforced Cement & Geotextile Fabric",
            tier=3,
            tier_name="Tier 3 Construction/Infrastructure",
            weight_kg=2400.0,
            volume_m3=5.0,
            deadline_hours=72.0,
            status="Waiting",
            recipient_facility="BRO Border Road Repair Section"
        ),
        CargoItem(
            id="CRG-DEMO-06",
            name="Commercial Electronics & Hardware Tools",
            tier=4,
            tier_name="Tier 4 General/Commercial Cargo",
            weight_kg=1600.0,
            volume_m3=6.5,
            deadline_hours=96.0,
            status="Waiting",
            recipient_facility="Naharlagun Commercial Market Association"
        )
    ]

@router.post("/create", response_model=Shipment)
def create_shipment(payload: ShipmentCreate):
    """Creates a new shipment plan."""
    shipment_id = f"SHP-NER-{uuid.uuid4().hex[:6].upper()}"
    new_shipment = Shipment(
        id=shipment_id,
        origin=payload.origin,
        destination=payload.destination,
        cargo_items=payload.cargo_items,
        required_delivery_hours=payload.required_delivery_hours,
        selected_vehicle_id=payload.selected_vehicle_id,
        status="Planned",
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    state_store.save_shipment(new_shipment)
    return new_shipment

@router.get("/", response_model=List[Shipment])
def list_shipments():
    """Returns all active and planned shipments."""
    return list(state_store.shipments.values())
