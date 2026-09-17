"""
Smart NER Logistics Control Platform
In-Memory and Persistent State Store with Realistic NER Seed Data
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from backend.models.schemas import (
    Vehicle, Driver, Shipment, Trip, Disruption,
    CargoItem, AllocationResult, Checkpoint, RouteOption
)
from backend.services.ner_network import generate_route_options, CORRIDORS

try:
    from backend.db.database import SessionLocal
    from backend.db.models import (
        VehicleModel, DriverModel, ShipmentModel, TripModel, DisruptionModel
    )
    DB_AVAILABLE = True
except Exception:
    DB_AVAILABLE = False

class StateStore:
    def __init__(self):
        self.vehicles: Dict[str, Vehicle] = {}
        self.drivers: Dict[str, Driver] = {}
        self.shipments: Dict[str, Shipment] = {}
        self.trips: Dict[str, Trip] = {}
        self.disruptions: Dict[str, Disruption] = {}
        self.sync_logs: List[Dict] = []
        self._seed_initial_data()
        self._load_from_db()

    def _seed_initial_data(self):
        # 1. Vehicles
        v1 = Vehicle(
            id="VEH-NER-01",
            name="Mountain Freight 4x4 Cruiser (5T)",
            model="Tata LPTA 715 4x4 High-Torque",
            max_payload_kg=4800.0,
            max_volume_m3=22.0,
            hill_grade_rating="Grade A (35% Incline Certified)",
            fuel_type="Heavy Diesel",
            current_status="Assigned (Trip #1024)",
            license_plate="AS-01-GB-4192"
        )
        v2 = Vehicle(
            id="VEH-NER-02",
            name="Heavy Hill Hauler (10T)",
            model="Ashok Leyland 1618 6x4 Heavy Cargo",
            max_payload_kg=10500.0,
            max_volume_m3=45.0,
            hill_grade_rating="Grade B (22% Incline Safe)",
            fuel_type="Diesel",
            current_status="Available",
            license_plate="AS-03-CC-8821"
        )
        v3 = Vehicle(
            id="VEH-NER-03",
            name="Rapid Valley Feeder (3T)",
            model="Mahindra Furio 7 High Clearance",
            max_payload_kg=3200.0,
            max_volume_m3=14.5,
            hill_grade_rating="Grade A (30% Slope AWD)",
            fuel_type="Diesel",
            current_status="Available",
            license_plate="AR-01-K-3390"
        )
        for v in [v1, v2, v3]:
            self.vehicles[v.id] = v

        # Additional vehicles
        v4 = Vehicle(
            id="VEH-NER-04",
            name="All-Weather Mountain 4x4 (2.5T)",
            model="Force Gurkha High-Altitude Cargo Spec",
            max_payload_kg=2500.0,
            max_volume_m3=11.0,
            hill_grade_rating="Grade A (38% Alpine Gradient Certified)",
            fuel_type="Diesel",
            current_status="Available",
            license_plate="ML-05-J-4910"
        )
        v5 = Vehicle(
            id="VEH-NER-05",
            name="Multi-Axle Heavy Hill Hauler (16T)",
            model="Tata Signa 2823 Hill Heavy Transporter",
            max_payload_kg=16000.0,
            max_volume_m3=58.0,
            hill_grade_rating="Grade B (20% Highway Incline Safe)",
            fuel_type="Diesel",
            current_status="Available",
            license_plate="AS-01-HC-1940"
        )
        v6 = Vehicle(
            id="VEH-NER-06",
            name="High-Mobility Light Carrier (1.8T)",
            model="Mahindra Bolero Maxi Camper 4x4",
            max_payload_kg=1800.0,
            max_volume_m3=8.5,
            hill_grade_rating="Grade A (35% High Ridge Incline)",
            fuel_type="Diesel",
            current_status="Available",
            license_plate="MZ-01-A-7721"
        )
        for v in [v1, v2, v3, v4, v5, v6]:
            self.vehicles[v.id] = v

        # 2. Certified Mountain Drivers Fleet (25 Authentic North East Region Mountain Drivers)
        now_dt = datetime.now()
        tashi_assigned = now_dt - timedelta(minutes=35)
        tashi_busy_until = now_dt + timedelta(hours=8, minutes=25)  # 9-hour total deadline

        d1 = Driver(
            id="DRV-NER-101",
            name="Tashi Norbu",
            phone="+91 94351-88291",
            experience_years=14,
            hill_driving_certified=True,
            languages=["Assamese", "Hindi", "English", "Monpa"],
            status="Busy",
            rating=4.95,
            current_trip_id="TRIP-1024",
            assigned_at=tashi_assigned.isoformat(),
            busy_until=tashi_busy_until.isoformat(),
            deadline_hours=9.0
        )
        d2 = Driver(
            id="DRV-NER-102",
            name="Bikram Roy",
            phone="+91 98640-12948",
            experience_years=9,
            hill_driving_certified=True,
            languages=["Bengali", "Assamese", "Hindi"],
            status="Available",
            rating=4.78
        )
        d3 = Driver(
            id="DRV-NER-103",
            name="Debajit Bora",
            phone="+91 97060-77123",
            experience_years=11,
            hill_driving_certified=True,
            languages=["Assamese", "Hindi"],
            status="Available",
            rating=4.88
        )
        d4 = Driver(
            id="DRV-NER-104",
            name="Dorjee Khandu",
            phone="+91 94360-33412",
            experience_years=16,
            hill_driving_certified=True,
            languages=["Monpa", "Hindi", "English"],
            status="Available",
            rating=4.96
        )
        d5 = Driver(
            id="DRV-NER-105",
            name="Zonunmawia Ralte",
            phone="+91 98623-88190",
            experience_years=10,
            hill_driving_certified=True,
            languages=["Mizo", "English", "Hindi"],
            status="Available",
            rating=4.82
        )
        d6 = Driver(
            id="DRV-NER-106",
            name="Temjen Jamir",
            phone="+91 94362-55019",
            experience_years=13,
            hill_driving_certified=True,
            languages=["Nagamese", "English", "Hindi"],
            status="Available",
            rating=4.91
        )
        d7 = Driver(
            id="DRV-NER-107",
            name="Pema Lhamu",
            phone="+91 94340-99214",
            experience_years=8,
            hill_driving_certified=True,
            languages=["Bhutia", "Nepali", "Hindi", "English"],
            status="Available",
            rating=4.89
        )
        d8 = Driver(
            id="DRV-NER-108",
            name="Bhabesh Kalita",
            phone="+91 98540-66712",
            experience_years=15,
            hill_driving_certified=True,
            languages=["Assamese", "Bodo", "Hindi"],
            status="Available",
            rating=4.85
        )
        d9 = Driver(
            id="DRV-NER-109",
            name="Sangay Wangdi",
            phone="+91 94361-22876",
            experience_years=12,
            hill_driving_certified=True,
            languages=["Tibetan", "Hindi", "English"],
            status="Available",
            rating=4.92
        )
        d10 = Driver(
            id="DRV-NER-110",
            name="Lalhmingthanga",
            phone="+91 98625-11043",
            experience_years=7,
            hill_driving_certified=True,
            languages=["Mizo", "Assamese", "English"],
            status="Available",
            rating=4.79
        )
        d11 = Driver(
            id="DRV-NER-111",
            name="Wungnaoshang Shimray",
            phone="+91 94363-71822",
            experience_years=12,
            hill_driving_certified=True,
            languages=["Manipuri", "Tangkhul", "English", "Hindi"],
            status="Available",
            rating=4.87
        )
        d12 = Driver(
            id="DRV-NER-112",
            name="Kangkan Deka",
            phone="+91 98541-33019",
            experience_years=6,
            hill_driving_certified=True,
            languages=["Assamese", "Hindi"],
            status="Available",
            rating=4.72
        )
        d13 = Driver(
            id="DRV-NER-113",
            name="Rinchen Namgyal",
            phone="+91 94360-88123",
            experience_years=17,
            hill_driving_certified=True,
            languages=["Monpa", "Hindi", "English", "Tibetan"],
            status="Available",
            rating=4.98
        )
        d14 = Driver(
            id="DRV-NER-114",
            name="Mebanshan Khongwir",
            phone="+91 98630-44910",
            experience_years=10,
            hill_driving_certified=True,
            languages=["Khasi", "English", "Hindi"],
            status="Available",
            rating=4.84
        )
        d15 = Driver(
            id="DRV-NER-115",
            name="Kevichusa Angami",
            phone="+91 94361-99234",
            experience_years=14,
            hill_driving_certified=True,
            languages=["Tenhyidie", "Nagamese", "English", "Hindi"],
            status="Available",
            rating=4.93
        )
        d16 = Driver(
            id="DRV-NER-116",
            name="Sanjoy Debbarma",
            phone="+91 94364-55102",
            experience_years=8,
            hill_driving_certified=True,
            languages=["Kokborok", "Bengali", "Hindi"],
            status="Available",
            rating=4.76
        )
        d17 = Driver(
            id="DRV-NER-117",
            name="Karma Tshering Lepcha",
            phone="+91 94341-66789",
            experience_years=15,
            hill_driving_certified=True,
            languages=["Lepcha", "Nepali", "Hindi", "English"],
            status="Available",
            rating=4.94
        )
        d18 = Driver(
            id="DRV-NER-118",
            name="Haobam Ningthouja",
            phone="+91 98620-33418",
            experience_years=11,
            hill_driving_certified=True,
            languages=["Meitei", "Hindi", "English"],
            status="Available",
            rating=4.83
        )
        d19 = Driver(
            id="DRV-NER-119",
            name="Banrilang Marbaniang",
            phone="+91 98631-77290",
            experience_years=9,
            hill_driving_certified=True,
            languages=["Khasi", "Assamese", "Hindi"],
            status="Available",
            rating=4.81
        )
        d20 = Driver(
            id="DRV-NER-120",
            name="Pranab Jyoti Saikia",
            phone="+91 97061-44589",
            experience_years=13,
            hill_driving_certified=True,
            languages=["Assamese", "Hindi", "Bengali"],
            status="Available",
            rating=4.89
        )
        d21 = Driver(
            id="DRV-NER-121",
            name="Lalthlamuana Sailo",
            phone="+91 98624-88310",
            experience_years=8,
            hill_driving_certified=True,
            languages=["Mizo", "English", "Hindi"],
            status="Available",
            rating=4.77
        )
        d22 = Driver(
            id="DRV-NER-122",
            name="Nani Opo",
            phone="+91 94362-11945",
            experience_years=11,
            hill_driving_certified=True,
            languages=["Apatani", "Hindi", "Assamese", "English"],
            status="Available",
            rating=4.88
        )
        d23 = Driver(
            id="DRV-NER-123",
            name="Bendangwati Ao",
            phone="+91 94360-66432",
            experience_years=16,
            hill_driving_certified=True,
            languages=["Ao", "Nagamese", "English", "Hindi"],
            status="Available",
            rating=4.95
        )
        d24 = Driver(
            id="DRV-NER-124",
            name="Partha Pratim Nath",
            phone="+91 98542-99014",
            experience_years=7,
            hill_driving_certified=True,
            languages=["Bengali", "Assamese", "Hindi"],
            status="Available",
            rating=4.74
        )
        d25 = Driver(
            id="DRV-NER-125",
            name="Dawa Tamang",
            phone="+91 94342-88190",
            experience_years=10,
            hill_driving_certified=True,
            languages=["Nepali", "Hindi", "English"],
            status="Available",
            rating=4.86
        )

        all_drivers = [
            d1, d2, d3, d4, d5, d6, d7, d8, d9, d10,
            d11, d12, d13, d14, d15, d16, d17, d18, d19, d20,
            d21, d22, d23, d24, d25
        ]
        for d in all_drivers:
            self.drivers[d.id] = d

        # 3. Initial Canonical Active Trip (Trip #1024 from the MVP specification!)
        sample_cargo = [
            CargoItem(
                id="CRG-001",
                name="Emergency Cardiac & Antivenom Medicines",
                tier=1,
                tier_name="Tier 1 Medical/Emergency",
                weight_kg=240.0,
                volume_m3=1.2,
                deadline_hours=8.0,
                status="Priority",
                recipient_facility="Tomo Riba Institute of Health Sciences, Naharlagun"
            ),
            CargoItem(
                id="CRG-002",
                name="Deep Freeze Vaccine Ampoules & Diluents",
                tier=1,
                tier_name="Tier 1 Medical/Emergency",
                weight_kg=180.0,
                volume_m3=0.9,
                deadline_hours=6.0,
                status="Priority",
                recipient_facility="Papum Pare District Cold Storage, Itanagar"
            ),
            CargoItem(
                id="CRG-003",
                name="High-Calorie Flood Relief Nutrition Kits",
                tier=2,
                tier_name="Tier 2 Essential Goods",
                weight_kg=1400.0,
                volume_m3=5.5,
                deadline_hours=14.0,
                status="Selected",
                recipient_facility="State Emergency Relief Center, Itanagar"
            ),
            CargoItem(
                id="CRG-004",
                name="Potable Water Filtration Chlorine Packs",
                tier=2,
                tier_name="Tier 2 Essential Goods",
                weight_kg=850.0,
                volume_m3=3.8,
                deadline_hours=18.0,
                status="Selected",
                recipient_facility="Capital Civil Supplies Depot"
            ),
            CargoItem(
                id="CRG-005",
                name="Bailey Bridge Modular Steel Pins & Plates",
                tier=3,
                tier_name="Tier 3 Construction/Infrastructure",
                weight_kg=1200.0,
                volume_m3=2.4,
                deadline_hours=48.0,
                status="Waiting",
                recipient_facility="BRO Border Infrastructure Division"
            ),
            CargoItem(
                id="CRG-006",
                name="Commercial Packaged Goods & Electronics",
                tier=4,
                tier_name="Tier 4 General/Commercial Cargo",
                weight_kg=950.0,
                volume_m3=4.2,
                deadline_hours=72.0,
                status="Waiting",
                recipient_facility="Ganga Market Wholesale Complex"
            )
        ]

        # Manifest
        allocated_items = sample_cargo[0:4]
        waiting_items = sample_cargo[4:6]
        tot_wt = sum(i.weight_kg for i in allocated_items)
        tot_vol = sum(i.volume_m3 for i in allocated_items)

        mnf = AllocationResult(
            manifest_id="MNF-NER-1024",
            vehicle_id="VEH-NER-01",
            vehicle_name="Mountain Freight 4x4 Cruiser (5T)",
            max_payload_kg=4800.0,
            allocated_payload_kg=tot_wt,
            payload_utilization_pct=round((tot_wt / 4800.0) * 100, 1),
            max_volume_m3=22.0,
            allocated_volume_m3=tot_vol,
            volume_utilization_pct=round((tot_vol / 22.0) * 100, 1),
            allocated_items=allocated_items,
            waiting_items=waiting_items,
            tier_counts={"Tier 1": 2, "Tier 2": 2, "Tier 3": 0, "Tier 4": 0},
            loading_instructions=[
                "1. Temperature-sensitive vaccines loaded in forward air-conditioned bay.",
                "2. Emergency antivenom secured in quick-dispatch emergency hatch.",
                "3. Food relief ration pallets center-aligned above dual rear axle.",
                "4. Construction materials staged at Guwahati depot for Trip #1025."
            ],
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        initial_trip = Trip(
            id="TRIP-1024",
            shipment_id="SHP-NER-9901",
            route_id="RO-NER-B",
            route_name="Route B: NH-27 Southern Engineered Corridor via Tezpur Bridge (RECOMMENDED)",
            driver_id="DRV-NER-101",
            driver_name="Tashi Norbu",
            vehicle_id="VEH-NER-01",
            vehicle_name="Mountain Freight 4x4 Cruiser (5T)",
            origin="Guwahati",
            destination="Itanagar",
            manifest=mnf,
            current_status="En Route",
            connectivity_mode="Online",
            checkpoints=[
                Checkpoint(name="Guwahati Central Depot", distance_km=0.0, status="Passed", estimated_time="06:00 AM", passed_at="06:12 AM"),
                Checkpoint(name="Nagaon Toll Plaza (NH-27)", distance_km=122.0, status="Passed", estimated_time="08:20 AM", passed_at="08:28 AM"),
                Checkpoint(name="Tezpur Kaliabhomora Brahmaputra Bridge", distance_km=187.0, status="Passed", estimated_time="09:50 AM", passed_at="09:54 AM"),
                Checkpoint(name="Naharlagun Foothill Ingress", distance_km=345.0, status="Pending", estimated_time="02:15 PM"),
                Checkpoint(name="Itanagar State Hospital & Relief Terminal", distance_km=385.0, status="Pending", estimated_time="03:00 PM")
            ],
            offline_sync_pending=False,
            last_sync_time=datetime.now().strftime("%H:%M:%S"),
            active_alert="Clear route verified by BRO highway dispatch. Low risk index 21.4."
        )
        self.trips[initial_trip.id] = initial_trip

        # 4. Disruptions
        disr1 = Disruption(
            id="DISR-01",
            title="Major Landslide & Rockfall on NH-15 Foothill Pass",
            corridor_name="Northern Bank Subansiri Axis",
            highway_ref="NH-15 / Gohpur Section",
            affected_segment="Km 142 to 148 near Banderdewa border",
            disruption_type="Landslide",
            severity="Critical",
            status="Active",
            coordinates=[26.9800, 93.7100],
            estimated_clearance_hours=14.5,
            recommended_reroute_id="RO-NER-B",
            reported_at="35 mins ago",
            source_type="SIMULATED DATA"
        )
        disr2 = Disruption(
            id="DISR-02",
            title="High Water Level & Bank Erosion on Brahmaputra Crossing",
            corridor_name="East-West Trunk Corridor",
            highway_ref="NH-27 Low Bypass",
            affected_segment="Kaziranga Southern Culvert Sector",
            disruption_type="Flash Flood",
            severity="High",
            status="Monitoring",
            coordinates=[26.5800, 93.1800],
            estimated_clearance_hours=6.0,
            recommended_reroute_id=None,
            reported_at="1 hour ago",
            source_type="SIMULATED DATA"
        )
        disr3 = Disruption(
            id="DISR-03",
            title="Sinking Roadbed & Mud Slide at Pagla Pahar",
            corridor_name="Dimapur - Kohima Supply Line",
            highway_ref="NH-29",
            affected_segment="Km 38 Hill Section",
            disruption_type="Road Subsidence",
            severity="Critical",
            status="Active",
            coordinates=[25.7900, 93.9200],
            estimated_clearance_hours=22.0,
            recommended_reroute_id=None,
            reported_at="2 hours ago",
            source_type="LIVE DATA"
        )
        for disr in [disr1, disr2, disr3]:
            self.disruptions[disr.id] = disr

    def _load_from_db(self):
        """Loads vehicles, drivers, shipments, trips, and disruptions from database if available."""
        if not DB_AVAILABLE:
            return
        try:
            db = SessionLocal()
            try:
                # 1. Load Vehicles
                db_vehs = db.query(VehicleModel).all()
                for v in db_vehs:
                    self.vehicles[v.id] = Vehicle(
                        id=v.id,
                        name=v.name,
                        model=v.model,
                        max_payload_kg=float(v.max_payload_kg),
                        max_volume_m3=float(v.max_volume_m3),
                        hill_grade_rating=v.hill_grade_rating or "",
                        fuel_type=v.fuel_type or "Diesel",
                        current_status=v.current_status,
                        license_plate=v.license_plate
                    )

                # 2. Load Drivers
                db_drvs = db.query(DriverModel).all()
                for d in db_drvs:
                    self.drivers[d.id] = Driver(
                        id=d.id,
                        name=d.name,
                        phone=d.phone,
                        experience_years=d.experience_years,
                        hill_driving_certified=d.hill_driving_certified,
                        languages=d.languages or [],
                        status=d.status,
                        rating=float(d.rating),
                        avatar_url=d.avatar_url,
                        current_trip_id=getattr(d, "current_trip_id", None),
                        busy_until=d.busy_until.isoformat() if getattr(d, "busy_until", None) else None,
                        assigned_at=d.assigned_at.isoformat() if getattr(d, "assigned_at", None) else None,
                        deadline_hours=float(d.deadline_hours) if getattr(d, "deadline_hours", None) else None
                    )

                # 3. Load Shipments
                db_shipments = db.query(ShipmentModel).all()
                for s in db_shipments:
                    cargo_items = [CargoItem(**item) if isinstance(item, dict) else item for item in (s.cargo_items or [])]
                    self.shipments[s.id] = Shipment(
                        id=s.id,
                        origin=s.origin,
                        destination=s.destination,
                        cargo_items=cargo_items,
                        required_delivery_hours=float(s.required_delivery_hours),
                        selected_vehicle_id=s.selected_vehicle_id or "",
                        selected_route_id=s.selected_route_id,
                        status=s.status,
                        created_at=s.created_at
                    )

                # 4. Load Trips
                db_trips = db.query(TripModel).all()
                for t in db_trips:
                    cps = [Checkpoint(**cp) if isinstance(cp, dict) else cp for cp in (t.checkpoints or [])]
                    mnf = AllocationResult(**t.manifest) if isinstance(t.manifest, dict) else t.manifest
                    if mnf:
                        self.trips[t.id] = Trip(
                            id=t.id,
                            shipment_id=t.shipment_id or "",
                            route_id=t.route_id or "",
                            route_name=t.route_name or "",
                            driver_id=t.driver_id or "",
                            driver_name=t.driver_name or "",
                            vehicle_id=t.vehicle_id or "",
                            vehicle_name=t.vehicle_name or "",
                            origin=t.origin,
                            destination=t.destination,
                            manifest=mnf,
                            current_status=t.current_status,
                            connectivity_mode=t.connectivity_mode,
                            checkpoints=cps,
                            offline_sync_pending=t.offline_sync_pending,
                            last_sync_time=t.last_sync_time or "",
                            active_alert=t.active_alert
                        )

                # 5. Load Disruptions
                db_disr = db.query(DisruptionModel).all()
                for d in db_disr:
                    self.disruptions[d.id] = Disruption(
                        id=d.id,
                        title=d.title,
                        corridor_name=d.corridor_name,
                        highway_ref=d.highway_ref,
                        affected_segment=d.affected_segment,
                        disruption_type=d.disruption_type,
                        severity=d.severity,
                        status=d.status,
                        coordinates=d.coordinates or [],
                        estimated_clearance_hours=float(d.estimated_clearance_hours),
                        recommended_reroute_id=d.recommended_reroute_id,
                        reported_at=d.reported_at,
                        source_type=d.source_type
                    )
            finally:
                db.close()
        except Exception as e:
            print(f"[StateStore] Database load bypassed: {e}")

    def save_shipment(self, shipment: Shipment):
        """Saves a shipment in memory and persists to database if available."""
        self.shipments[shipment.id] = shipment
        if DB_AVAILABLE:
            try:
                db = SessionLocal()
                try:
                    cargo_list = [c.model_dump() if hasattr(c, "model_dump") else c.dict() if hasattr(c, "dict") else c for c in shipment.cargo_items]
                    existing = db.query(ShipmentModel).filter(ShipmentModel.id == shipment.id).first()
                    if existing:
                        existing.status = shipment.status
                    else:
                        db_shipment = ShipmentModel(
                            id=shipment.id,
                            origin=shipment.origin,
                            destination=shipment.destination,
                            cargo_items=cargo_list,
                            required_delivery_hours=shipment.required_delivery_hours,
                            selected_vehicle_id=shipment.selected_vehicle_id,
                            selected_route_id=shipment.selected_route_id,
                            status=shipment.status,
                            created_at=shipment.created_at
                        )
                        db.add(db_shipment)
                    db.commit()
                finally:
                    db.close()
            except Exception as e:
                print(f"[StateStore] Database shipment sync bypassed: {e}")

    def save_trip(self, trip: Trip):
        """Saves a trip in memory and persists to database if available."""
        self.trips[trip.id] = trip
        if DB_AVAILABLE:
            try:
                db = SessionLocal()
                try:
                    manifest_dict = trip.manifest.model_dump() if hasattr(trip.manifest, "model_dump") else trip.manifest.dict() if hasattr(trip.manifest, "dict") else trip.manifest
                    checkpoints_list = [cp.model_dump() if hasattr(cp, "model_dump") else cp.dict() if hasattr(cp, "dict") else cp for cp in trip.checkpoints]
                    existing = db.query(TripModel).filter(TripModel.id == trip.id).first()
                    if existing:
                        existing.current_status = trip.current_status
                        existing.connectivity_mode = trip.connectivity_mode
                        existing.last_sync_time = trip.last_sync_time
                        existing.checkpoints = checkpoints_list
                        existing.active_alert = trip.active_alert
                    else:
                        db_trip = TripModel(
                            id=trip.id,
                            shipment_id=trip.shipment_id,
                            route_id=trip.route_id,
                            route_name=trip.route_name,
                            driver_id=trip.driver_id,
                            driver_name=trip.driver_name,
                            vehicle_id=trip.vehicle_id,
                            vehicle_name=trip.vehicle_name,
                            origin=trip.origin,
                            destination=trip.destination,
                            manifest=manifest_dict,
                            current_status=trip.current_status,
                            connectivity_mode=trip.connectivity_mode,
                            checkpoints=checkpoints_list,
                            offline_sync_pending=trip.offline_sync_pending,
                            last_sync_time=trip.last_sync_time,
                            active_alert=trip.active_alert
                        )
                        db.add(db_trip)
                    db.commit()
                finally:
                    db.close()
            except Exception as e:
                print(f"[StateStore] Database trip sync bypassed: {e}")

    def save_driver(self, driver: Driver):
        """Saves driver status and deadline lock in memory and database if available."""
        self.drivers[driver.id] = driver
        if DB_AVAILABLE:
            try:
                db = SessionLocal()
                try:
                    existing = db.query(DriverModel).filter(DriverModel.id == driver.id).first()
                    if existing:
                        existing.status = driver.status
                        existing.current_trip_id = driver.current_trip_id
                        existing.busy_until = datetime.fromisoformat(driver.busy_until) if driver.busy_until else None
                        existing.assigned_at = datetime.fromisoformat(driver.assigned_at) if driver.assigned_at else None
                        existing.deadline_hours = driver.deadline_hours
                        db.commit()
                finally:
                    db.close()
            except Exception as e:
                print(f"[StateStore] Database driver sync bypassed: {e}")

    def update_driver_availabilities(self):
        """
        Checks busy drivers; if current time has passed their deadline, frees the driver back to 'Available'.
        """
        now = datetime.now()
        for d in self.drivers.values():
            if d.status in ["Busy", "On Trip"] and d.busy_until:
                try:
                    busy_dt = datetime.fromisoformat(d.busy_until)
                    if now >= busy_dt:
                        d.status = "Available"
                        d.busy_until = None
                        d.current_trip_id = None
                        d.assigned_at = None
                        d.deadline_hours = None
                        self.save_driver(d)
                except Exception as e:
                    print(f"[StateStore] Error parsing driver busy_until: {e}")

# Global singleton
state_store = StateStore()
