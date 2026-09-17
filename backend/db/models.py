"""
Smart NER Logistics Control Platform
SQLAlchemy ORM Models for PostgreSQL (Supabase) and SQLite Fallback
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, JSON, DateTime, text
from backend.db.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(String(64), primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(50), nullable=True)
    role = Column(String(50), nullable=False)  # admin, fleet_manager, driver, logistics_planner, government_monitor
    organization = Column(String(255), nullable=True)
    encrypted_password = Column(String(255), nullable=False)
    status = Column(String(50), default="Active")
    created_at = Column(String(50), nullable=True)
    last_login = Column(String(50), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.full_name,
            "email": self.email,
            "phone": self.phone or "",
            "role": self.role,
            "organization": self.organization or "",
            "encrypted_password": self.encrypted_password,
            "status": self.status,
            "created_at": self.created_at or "",
            "last_login": self.last_login
        }

class VehicleModel(Base):
    __tablename__ = "vehicles"

    id = Column(String(64), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    model = Column(String(255), nullable=False)
    max_payload_kg = Column(Float, nullable=False)
    max_volume_m3 = Column(Float, nullable=False)
    hill_grade_rating = Column(String(255), nullable=True)
    fuel_type = Column(String(50), nullable=True)
    current_status = Column(String(100), default="Available")
    license_plate = Column(String(50), unique=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "max_payload_kg": float(self.max_payload_kg),
            "max_volume_m3": float(self.max_volume_m3),
            "hill_grade_rating": self.hill_grade_rating or "",
            "fuel_type": self.fuel_type or "",
            "current_status": self.current_status,
            "license_plate": self.license_plate
        }

class DriverModel(Base):
    __tablename__ = "drivers"

    id = Column(String(64), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    experience_years = Column(Integer, default=0)
    hill_driving_certified = Column(Boolean, default=True)
    languages = Column(JSON, default=list)
    status = Column(String(50), default="Available")
    rating = Column(Float, default=4.8)
    avatar_url = Column(String(500), nullable=True)
    current_trip_id = Column(String(64), nullable=True)
    busy_until = Column(DateTime, nullable=True)
    assigned_at = Column(DateTime, nullable=True)
    deadline_hours = Column(Float, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "experience_years": self.experience_years,
            "hill_driving_certified": self.hill_driving_certified,
            "languages": self.languages or [],
            "status": self.status,
            "rating": float(self.rating),
            "avatar_url": self.avatar_url,
            "current_trip_id": self.current_trip_id,
            "busy_until": self.busy_until.isoformat() if self.busy_until else None,
            "assigned_at": self.assigned_at.isoformat() if self.assigned_at else None,
            "deadline_hours": float(self.deadline_hours) if self.deadline_hours else None
        }

class ShipmentModel(Base):
    __tablename__ = "shipments"

    id = Column(String(64), primary_key=True, index=True)
    origin = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    cargo_items = Column(JSON, nullable=False)
    required_delivery_hours = Column(Float, nullable=False)
    selected_vehicle_id = Column(String(64), nullable=True)
    selected_route_id = Column(String(64), nullable=True)
    status = Column(String(50), default="Draft")
    created_at = Column(String(50), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "origin": self.origin,
            "destination": self.destination,
            "cargo_items": self.cargo_items,
            "required_delivery_hours": float(self.required_delivery_hours),
            "selected_vehicle_id": self.selected_vehicle_id,
            "selected_route_id": self.selected_route_id,
            "status": self.status,
            "created_at": self.created_at
        }

class TripModel(Base):
    __tablename__ = "trips"

    id = Column(String(64), primary_key=True, index=True)
    shipment_id = Column(String(64), nullable=True)
    route_id = Column(String(64), nullable=True)
    route_name = Column(String(255), nullable=True)
    driver_id = Column(String(64), nullable=True)
    driver_name = Column(String(255), nullable=True)
    vehicle_id = Column(String(64), nullable=True)
    vehicle_name = Column(String(255), nullable=True)
    origin = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    manifest = Column(JSON, nullable=True)
    current_status = Column(String(100), default="Assigned")
    connectivity_mode = Column(String(50), default="Online")
    checkpoints = Column(JSON, nullable=True)
    offline_sync_pending = Column(Boolean, default=False)
    last_sync_time = Column(String(50), nullable=True)
    active_alert = Column(String(500), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "shipment_id": self.shipment_id or "",
            "route_id": self.route_id or "",
            "route_name": self.route_name or "",
            "driver_id": self.driver_id or "",
            "driver_name": self.driver_name or "",
            "vehicle_id": self.vehicle_id or "",
            "vehicle_name": self.vehicle_name or "",
            "origin": self.origin,
            "destination": self.destination,
            "manifest": self.manifest,
            "current_status": self.current_status,
            "connectivity_mode": self.connectivity_mode,
            "checkpoints": self.checkpoints or [],
            "offline_sync_pending": self.offline_sync_pending,
            "last_sync_time": self.last_sync_time or "",
            "active_alert": self.active_alert
        }

class DisruptionModel(Base):
    __tablename__ = "disruptions"

    id = Column(String(64), primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    corridor_name = Column(String(255), nullable=False)
    highway_ref = Column(String(100), nullable=False)
    affected_segment = Column(String(255), nullable=False)
    disruption_type = Column(String(100), nullable=False)
    severity = Column(String(50), nullable=False)
    status = Column(String(50), default="Active")
    coordinates = Column(JSON, nullable=True)
    estimated_clearance_hours = Column(Float, default=4.0)
    recommended_reroute_id = Column(String(64), nullable=True)
    reported_at = Column(String(50), nullable=False)
    source_type = Column(String(100), default="SIMULATED DATA")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "corridor_name": self.corridor_name,
            "highway_ref": self.highway_ref,
            "affected_segment": self.affected_segment,
            "disruption_type": self.disruption_type,
            "severity": self.severity,
            "status": self.status,
            "coordinates": self.coordinates,
            "estimated_clearance_hours": float(self.estimated_clearance_hours),
            "recommended_reroute_id": self.recommended_reroute_id,
            "reported_at": self.reported_at,
            "source_type": self.source_type
        }
