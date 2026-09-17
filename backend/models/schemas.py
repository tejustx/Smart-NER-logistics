"""
Smart NER Logistics Control Platform
Pydantic Schemas and Data Models
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class CargoItem(BaseModel):
    id: str
    name: str
    tier: int = Field(..., ge=1, le=4, description="Tier 1: Emergency, Tier 2: Essential, Tier 3: Construction, Tier 4: General")
    tier_name: str
    weight_kg: float
    volume_m3: float
    deadline_hours: float
    status: str = "Waiting"  # "Priority", "Selected", "Waiting"
    recipient_facility: Optional[str] = None
    urgency_score: Optional[float] = 0.0

class Vehicle(BaseModel):
    id: str
    name: str
    model: str
    max_payload_kg: float
    max_volume_m3: float
    hill_grade_rating: str  # e.g., "Grade A (Up to 35% slope, 4x4 AWD)"
    fuel_type: str
    current_status: str = "Available"
    license_plate: str

class RiskFactorBreakdown(BaseModel):
    rainfall_mm_hr: float
    slope_gradient_pct: float
    historical_landslide_freq: float  # 0.0 to 1.0
    road_quality_index: float  # 0.0 (damaged) to 1.0 (excellent)
    raw_risk_score: float  # 0 to 100
    risk_level: str  # "Low", "Medium", "High", "Critical"
    effective_cost_multiplier: float

class RouteSegment(BaseModel):
    id: str
    from_hub: str
    to_hub: str
    highway_ref: str
    distance_km: float
    base_duration_hours: float
    elevation_gain_m: float
    risk: RiskFactorBreakdown
    coordinates: List[List[float]]  # [[lat, lng], ...]

class RouteOption(BaseModel):
    id: str
    name: str
    tag: str  # e.g. "Route A (Direct)", "Route B (Safer Alternative)"
    is_recommended: bool
    recommendation_reason: str
    total_distance_km: float
    estimated_duration_hours: float
    risk_score: float
    risk_level: str
    estimated_logistics_cost_inr: float
    risk_penalty_cost_inr: float
    segments: List[RouteSegment]
    warning_alerts: List[str]
    path_coordinates: List[List[float]]
    predicted_risk: Optional[Dict[str, float]] = None  # {"6h": 0.23, "12h": 0.61, "24h": 0.78}
    toe_erosion_hazard: Optional[str] = None
    forward_risk_summary: Optional[str] = None
    primary_river: Optional[str] = None
    river_proximity_km: Optional[float] = None
    geotechnical_explanation: Optional[str] = None
    isro_bhuvan_data: Optional[Dict[str, Any]] = None
    live_weather: Optional[Dict[str, Any]] = None

class DisruptionProbability(BaseModel):
    h6: float = Field(..., alias="6h")
    h12: float = Field(..., alias="12h")
    h24: float = Field(..., alias="24h")

class PlanAndAllocateRequest(BaseModel):
    origin: str = "Guwahati"
    destination: str = "Itanagar"
    cargo_items: List[CargoItem] = []
    vehicle_id: str = "VEH-NER-01"

class PlanAndAllocateResponse(BaseModel):
    route: Dict[str, Any]
    allocation: Dict[str, Any]

class ShipmentCreate(BaseModel):
    origin: str
    destination: str
    cargo_items: List[CargoItem]
    required_delivery_hours: float
    selected_vehicle_id: str

class Shipment(BaseModel):
    id: str
    origin: str
    destination: str
    cargo_items: List[CargoItem]
    required_delivery_hours: float
    selected_vehicle_id: str
    selected_route_id: Optional[str] = None
    status: str = "Draft"
    created_at: str

class AllocationRequest(BaseModel):
    shipment_id: Optional[str] = None
    vehicle_id: str
    cargo_items: List[CargoItem]
    route_id: Optional[str] = None

class AllocationResult(BaseModel):
    manifest_id: str
    vehicle_id: str
    vehicle_name: str
    max_payload_kg: float
    allocated_payload_kg: float
    payload_utilization_pct: float
    max_volume_m3: float
    allocated_volume_m3: float
    volume_utilization_pct: float
    allocated_items: List[CargoItem]
    waiting_items: List[CargoItem]
    tier_counts: Dict[str, int]
    loading_instructions: List[str]
    generated_at: str

class Driver(BaseModel):
    id: str
    name: str
    phone: str
    experience_years: int
    hill_driving_certified: bool
    languages: List[str]
    status: str = "Available"
    rating: float = 4.8
    avatar_url: Optional[str] = None
    current_trip_id: Optional[str] = None
    busy_until: Optional[str] = None
    assigned_at: Optional[str] = None
    deadline_hours: Optional[float] = None

class TripAssignmentRequest(BaseModel):
    shipment_id: str
    route_id: str
    driver_id: str
    vehicle_id: str
    manifest_id: str
    deadline_hours: Optional[float] = 9.0
    origin: Optional[str] = "Guwahati"
    destination: Optional[str] = "Itanagar"

class Checkpoint(BaseModel):
    name: str
    distance_km: float
    status: str  # "Pending", "Passed", "Delayed"
    estimated_time: str
    passed_at: Optional[str] = None

class Trip(BaseModel):
    id: str
    shipment_id: str
    route_id: str
    route_name: str
    driver_id: str
    driver_name: str
    vehicle_id: str
    vehicle_name: str
    origin: str
    destination: str
    manifest: AllocationResult
    current_status: str  # "Assigned", "En Route", "Arrived", "Delivered"
    connectivity_mode: str = "Online"  # "Online", "Offline"
    checkpoints: List[Checkpoint]
    offline_sync_pending: bool = False
    last_sync_time: str
    active_alert: Optional[str] = None

class Disruption(BaseModel):
    id: str
    title: str
    corridor_name: str
    highway_ref: str
    affected_segment: str
    disruption_type: str  # "Landslide", "Flash Flood", "Road Subsidence", "Bridge Washout"
    severity: str  # "Critical", "High", "Moderate"
    status: str  # "Active", "Monitoring", "Cleared"
    coordinates: List[float]  # [lat, lng]
    estimated_clearance_hours: float
    recommended_reroute_id: Optional[str] = None
    reported_at: str
    source_type: str = "SIMULATED DATA"  # "LIVE DATA", "HISTORICAL DATA", "SIMULATED DATA"

class WhatIfSimulationRequest(BaseModel):
    blocked_corridor_id: str
    simulated_rainfall_mm_hr: float = 60.0

class WhatIfSimulationResult(BaseModel):
    simulation_id: str
    blocked_corridor_id: str
    blocked_corridor_name: str
    highway_ref: str
    affected_shipments_count: int
    stranded_tonnage_kg: float
    avg_detour_increase_km: float
    avg_delay_hours: float
    additional_fuel_cost_inr: float
    suggested_alternative_route: str
    regional_accessibility_index_change: str

class SyncTelemetryPayload(BaseModel):
    trip_id: str
    driver_id: str
    current_lat: Optional[float] = None
    current_lng: Optional[float] = None
    timestamp: str
    completed_checkpoint_names: List[str] = []
    delivered_cargo_item_ids: List[str] = []
    local_offline_notes: Optional[str] = None
    battery_level_pct: Optional[int] = 85
