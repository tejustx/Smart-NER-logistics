"""
Smart NER Logistics Control Platform
Database Initialization & Seeding Script (Supabase PostgreSQL / Local Fallback)
"""

import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.db.database import engine, Base, SessionLocal, check_db_connection, IS_POSTGRES
from backend.db.models import (
    UserModel, VehicleModel, DriverModel,
    ShipmentModel, TripModel, DisruptionModel
)
from backend.services.user_service import hash_password

def init_db(seed_data: bool = True):
    """
    Creates all database tables defined in SQLAlchemy ORM models.
    Optionally seeds baseline accounts, vehicles, drivers, and disruptions.
    """
    print("=" * 65)
    print("  Smart NER Logistics Control Platform - Database Initializer")
    print("=" * 65)

    conn_status = check_db_connection()
    print(f"[*] Target Database : {conn_status['type']}")
    if conn_status.get("url_masked"):
        print(f"[*] Endpoint        : {conn_status['url_masked']}")
    print(f"[*] Status          : {conn_status['status'].upper()}")

    if conn_status["status"] != "connected":
        print(f"[!] Warning: Could not connect to database: {conn_status.get('error')}")
        return False

    print("\n[*] Creating database tables if they do not exist...")
    Base.metadata.create_all(bind=engine)
    print("    [OK] users")
    print("    [OK] vehicles")
    print("    [OK] drivers")
    print("    [OK] shipments")
    print("    [OK] trips")
    print("    [OK] disruptions")

    if not seed_data:
        print("\n[OK] Database schema initialized successfully.")
        return True

    db = SessionLocal()
    try:
        # 1. Seed Users if empty
        user_count = db.query(UserModel).count()
        if user_count == 0:
            print("\n[*] Seeding initial administrative & operations accounts...")
            defaults = [
                {
                    "id": "usr_planner01",
                    "full_name": "Dr. Anamika Barman",
                    "email": "planner@nerlogistics.in",
                    "phone": "+91 94350-11223",
                    "role": "planner",
                    "organization": "NER Freight Control Hub, Guwahati",
                    "raw_pwd": "Planner@123"
                },
                {
                    "id": "usr_gov01",
                    "full_name": "Col. Ranjit Gogoi (Retd.)",
                    "email": "gov@nerlogistics.in",
                    "phone": "+91 98640-33445",
                    "role": "government",
                    "organization": "North Eastern Council / Disaster Relief Cell",
                    "raw_pwd": "Gov@123"
                },
                {
                    "id": "usr_driver01",
                    "full_name": "Tashi Norbu",
                    "email": "driver@nerlogistics.in",
                    "phone": "+91 94351-88291",
                    "role": "driver",
                    "organization": "Arunachal Hill Express Convoy",
                    "raw_pwd": "Driver@123"
                },
                {
                    "id": "usr_admin01",
                    "full_name": "System Administrator",
                    "email": "admin@nerlogistics.in",
                    "phone": "+91 98640-99999",
                    "role": "admin",
                    "organization": "Smart NER Logistics Technical Operations",
                    "raw_pwd": "Admin@123"
                }
            ]
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for u in defaults:
                user_obj = UserModel(
                    id=u["id"],
                    full_name=u["full_name"],
                    email=u["email"],
                    phone=u["phone"],
                    role=u["role"],
                    organization=u["organization"],
                    encrypted_password=hash_password(u["raw_pwd"]),
                    status="Active",
                    created_at=now,
                    last_login=None
                )
                db.add(user_obj)
            db.commit()
            print(f"    [OK] Seeded {len(defaults)} baseline accounts.")
        else:
            print(f"\n[*] Users table already has {user_count} records; skipping seed.")

        # 2. Seed Vehicles if empty
        veh_count = db.query(VehicleModel).count()
        if veh_count == 0:
            print("\n[*] Seeding initial mountain freight fleet...")
            vehicles = [
                VehicleModel(
                    id="VEH-NER-01",
                    name="Mountain Freight 4x4 Cruiser (5T)",
                    model="Tata LPTA 715 4x4 High-Torque",
                    max_payload_kg=4800.0,
                    max_volume_m3=22.0,
                    hill_grade_rating="Grade A (35% Incline Certified)",
                    fuel_type="Heavy Diesel",
                    current_status="Assigned (Trip #1024)",
                    license_plate="AS-01-GB-4192"
                ),
                VehicleModel(
                    id="VEH-NER-02",
                    name="Heavy Hill Hauler (10T)",
                    model="Ashok Leyland 1618 6x4 Heavy Cargo",
                    max_payload_kg=10500.0,
                    max_volume_m3=45.0,
                    hill_grade_rating="Grade B (22% Incline Safe)",
                    fuel_type="Diesel",
                    current_status="Available",
                    license_plate="AS-03-CC-8821"
                ),
                VehicleModel(
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
            ]
            db.add_all(vehicles)
            db.commit()
            print(f"    [OK] Seeded {len(vehicles)} vehicles.")
        else:
            print(f"[*] Vehicles table already has {veh_count} records.")

        # 3. Seed Drivers if empty
        drv_count = db.query(DriverModel).count()
        if drv_count < 25:
            print("\n[*] Seeding certified mountain drivers (25 regional drivers)...")
            db.query(DriverModel).delete()
            now_dt = datetime.now()
            tashi_assigned = now_dt - timedelta(minutes=35)
            tashi_busy = now_dt + timedelta(hours=8, minutes=25)

            drivers = [
                DriverModel(
                    id="DRV-NER-101",
                    name="Tashi Norbu",
                    phone="+91 94351-88291",
                    experience_years=14,
                    hill_driving_certified=True,
                    languages=["Assamese", "Hindi", "English", "Monpa"],
                    status="Busy",
                    rating=4.95,
                    current_trip_id="TRIP-1024",
                    assigned_at=tashi_assigned,
                    busy_until=tashi_busy,
                    deadline_hours=9.0
                ),
                DriverModel(
                    id="DRV-NER-102",
                    name="Bikram Roy",
                    phone="+91 98640-12948",
                    experience_years=9,
                    hill_driving_certified=True,
                    languages=["Bengali", "Assamese", "Hindi"],
                    status="Available",
                    rating=4.78
                ),
                DriverModel(
                    id="DRV-NER-103",
                    name="Debajit Bora",
                    phone="+91 97060-77123",
                    experience_years=11,
                    hill_driving_certified=True,
                    languages=["Assamese", "Hindi"],
                    status="Available",
                    rating=4.88
                ),
                DriverModel(
                    id="DRV-NER-104",
                    name="Dorjee Khandu",
                    phone="+91 94360-33412",
                    experience_years=16,
                    hill_driving_certified=True,
                    languages=["Monpa", "Hindi", "English"],
                    status="Available",
                    rating=4.96
                ),
                DriverModel(
                    id="DRV-NER-105",
                    name="Zonunmawia Ralte",
                    phone="+91 98623-88190",
                    experience_years=10,
                    hill_driving_certified=True,
                    languages=["Mizo", "English", "Hindi"],
                    status="Available",
                    rating=4.82
                ),
                DriverModel(
                    id="DRV-NER-106",
                    name="Temjen Jamir",
                    phone="+91 94362-55019",
                    experience_years=13,
                    hill_driving_certified=True,
                    languages=["Nagamese", "English", "Hindi"],
                    status="Available",
                    rating=4.91
                ),
                DriverModel(
                    id="DRV-NER-107",
                    name="Pema Lhamu",
                    phone="+91 94340-99214",
                    experience_years=8,
                    hill_driving_certified=True,
                    languages=["Bhutia", "Nepali", "Hindi", "English"],
                    status="Available",
                    rating=4.89
                ),
                DriverModel(
                    id="DRV-NER-108",
                    name="Bhabesh Kalita",
                    phone="+91 98540-66712",
                    experience_years=15,
                    hill_driving_certified=True,
                    languages=["Assamese", "Bodo", "Hindi"],
                    status="Available",
                    rating=4.85
                ),
                DriverModel(
                    id="DRV-NER-109",
                    name="Sangay Wangdi",
                    phone="+91 94361-22876",
                    experience_years=12,
                    hill_driving_certified=True,
                    languages=["Tibetan", "Hindi", "English"],
                    status="Available",
                    rating=4.92
                ),
                DriverModel(
                    id="DRV-NER-110",
                    name="Lalhmingthanga",
                    phone="+91 98625-11043",
                    experience_years=7,
                    hill_driving_certified=True,
                    languages=["Mizo", "Assamese", "English"],
                    status="Available",
                    rating=4.79
                ),
                DriverModel(
                    id="DRV-NER-111",
                    name="Wungnaoshang Shimray",
                    phone="+91 94363-71822",
                    experience_years=12,
                    hill_driving_certified=True,
                    languages=["Manipuri", "Tangkhul", "English", "Hindi"],
                    status="Available",
                    rating=4.87
                ),
                DriverModel(
                    id="DRV-NER-112",
                    name="Kangkan Deka",
                    phone="+91 98541-33019",
                    experience_years=6,
                    hill_driving_certified=True,
                    languages=["Assamese", "Hindi"],
                    status="Available",
                    rating=4.72
                ),
                DriverModel(
                    id="DRV-NER-113",
                    name="Rinchen Namgyal",
                    phone="+91 94360-88123",
                    experience_years=17,
                    hill_driving_certified=True,
                    languages=["Monpa", "Hindi", "English", "Tibetan"],
                    status="Available",
                    rating=4.98
                ),
                DriverModel(
                    id="DRV-NER-114",
                    name="Mebanshan Khongwir",
                    phone="+91 98630-44910",
                    experience_years=10,
                    hill_driving_certified=True,
                    languages=["Khasi", "English", "Hindi"],
                    status="Available",
                    rating=4.84
                ),
                DriverModel(
                    id="DRV-NER-115",
                    name="Kevichusa Angami",
                    phone="+91 94361-99234",
                    experience_years=14,
                    hill_driving_certified=True,
                    languages=["Tenhyidie", "Nagamese", "English", "Hindi"],
                    status="Available",
                    rating=4.93
                ),
                DriverModel(
                    id="DRV-NER-116",
                    name="Sanjoy Debbarma",
                    phone="+91 94364-55102",
                    experience_years=8,
                    hill_driving_certified=True,
                    languages=["Kokborok", "Bengali", "Hindi"],
                    status="Available",
                    rating=4.76
                ),
                DriverModel(
                    id="DRV-NER-117",
                    name="Karma Tshering Lepcha",
                    phone="+91 94341-66789",
                    experience_years=15,
                    hill_driving_certified=True,
                    languages=["Lepcha", "Nepali", "Hindi", "English"],
                    status="Available",
                    rating=4.94
                ),
                DriverModel(
                    id="DRV-NER-118",
                    name="Haobam Ningthouja",
                    phone="+91 98620-33418",
                    experience_years=11,
                    hill_driving_certified=True,
                    languages=["Meitei", "Hindi", "English"],
                    status="Available",
                    rating=4.83
                ),
                DriverModel(
                    id="DRV-NER-119",
                    name="Banrilang Marbaniang",
                    phone="+91 98631-77290",
                    experience_years=9,
                    hill_driving_certified=True,
                    languages=["Khasi", "Assamese", "Hindi"],
                    status="Available",
                    rating=4.81
                ),
                DriverModel(
                    id="DRV-NER-120",
                    name="Pranab Jyoti Saikia",
                    phone="+91 97061-44589",
                    experience_years=13,
                    hill_driving_certified=True,
                    languages=["Assamese", "Hindi", "Bengali"],
                    status="Available",
                    rating=4.89
                ),
                DriverModel(
                    id="DRV-NER-121",
                    name="Lalthlamuana Sailo",
                    phone="+91 98624-88310",
                    experience_years=8,
                    hill_driving_certified=True,
                    languages=["Mizo", "English", "Hindi"],
                    status="Available",
                    rating=4.77
                ),
                DriverModel(
                    id="DRV-NER-122",
                    name="Nani Opo",
                    phone="+91 94362-11945",
                    experience_years=11,
                    hill_driving_certified=True,
                    languages=["Apatani", "Hindi", "Assamese", "English"],
                    status="Available",
                    rating=4.88
                ),
                DriverModel(
                    id="DRV-NER-123",
                    name="Bendangwati Ao",
                    phone="+91 94360-66432",
                    experience_years=16,
                    hill_driving_certified=True,
                    languages=["Ao", "Nagamese", "English", "Hindi"],
                    status="Available",
                    rating=4.95
                ),
                DriverModel(
                    id="DRV-NER-124",
                    name="Partha Pratim Nath",
                    phone="+91 98542-99014",
                    experience_years=7,
                    hill_driving_certified=True,
                    languages=["Bengali", "Assamese", "Hindi"],
                    status="Available",
                    rating=4.74
                ),
                DriverModel(
                    id="DRV-NER-125",
                    name="Dawa Tamang",
                    phone="+91 94342-88190",
                    experience_years=10,
                    hill_driving_certified=True,
                    languages=["Nepali", "Hindi", "English"],
                    status="Available",
                    rating=4.86
                )
            ]
            db.add_all(drivers)
            db.commit()
            print(f"    [OK] Seeded {len(drivers)} certified drivers.")
        else:
            print(f"[*] Drivers table already has {drv_count} records.")

        # 4. Seed Disruptions if empty
        dis_count = db.query(DisruptionModel).count()
        if dis_count == 0:
            print("\n[*] Seeding active NER monsoon road disruptions...")
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            disruptions = [
                DisruptionModel(
                    id="DIS-01",
                    title="Active Landslide & Mudslip on NH-15 Near Bhalukpong",
                    corridor_name="Guwahati - Itanagar Primary Corridor",
                    highway_ref="NH-15 / NH-13",
                    affected_segment="Bhalukpong Gorge (KM 42-48)",
                    disruption_type="Landslide",
                    severity="Critical",
                    status="Active",
                    coordinates=[27.0125, 92.6418],
                    estimated_clearance_hours=12.0,
                    recommended_reroute_id="RT-GHY-ITA-02",
                    reported_at=now,
                    source_type="LIVE SENSOR TELEMETRY"
                ),
                DisruptionModel(
                    id="DIS-02",
                    title="Culvert Submersion Risk at Lower Subansiri Border",
                    corridor_name="Tezpur - Ziro Valley Link",
                    highway_ref="NH-229",
                    affected_segment="Potin - Yazali Stretch",
                    disruption_type="Flash Flood",
                    severity="High",
                    status="Monitoring",
                    coordinates=[27.3512, 93.7821],
                    estimated_clearance_hours=6.5,
                    recommended_reroute_id="RT-GHY-ITA-03",
                    reported_at=now,
                    source_type="BORDER ROADS ORG (BRO)"
                )
            ]
            db.add_all(disruptions)
            db.commit()
            print(f"    [OK] Seeded {len(disruptions)} road disruptions.")
        else:
            print(f"[*] Disruptions table already has {dis_count} records.")

        print("\n" + "=" * 65)
        print("  Database initialization completed successfully!")
        print("=" * 65)
        return True

    except Exception as e:
        db.rollback()
        print(f"\n[!] Error during database seeding: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
