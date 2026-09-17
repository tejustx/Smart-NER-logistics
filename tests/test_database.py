"""
Smart NER Logistics Control Platform
Automated Database & ORM Integration Test Suite
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db.database import check_db_connection, SessionLocal, engine, Base
from backend.db.models import UserModel, VehicleModel, DriverModel, ShipmentModel, TripModel
from backend.services.user_service import UserService, hash_password, verify_password
from backend.services.state_store import state_store
from backend.models.schemas import Shipment, CargoItem

class TestDatabaseIntegration(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()

    def tearDown(self):
        self.db.close()

    def test_database_connection_check(self):
        status = check_db_connection()
        self.assertEqual(status["status"], "connected")
        self.assertIn("type", status)

    def test_user_orm_crud_and_encryption(self):
        email = f"orm_test_{os.urandom(4).hex()}@mountainlogistics.in"
        encrypted = hash_password("DbSecretPass@2026")

        user = UserModel(
            id=f"usr_{os.urandom(4).hex()}",
            full_name="Lobzang Wangchuk",
            email=email,
            phone="+91 94360-11223",
            role="planner",
            organization="Tawang Mountain Division",
            encrypted_password=encrypted,
            status="Active"
        )
        self.db.add(user)
        self.db.commit()

        # Query back
        queried = self.db.query(UserModel).filter(UserModel.email == email).first()
        self.assertIsNotNone(queried)
        self.assertEqual(queried.full_name, "Lobzang Wangchuk")
        self.assertTrue(queried.encrypted_password.startswith("pbkdf2:sha256:100000$"))
        self.assertTrue(verify_password("DbSecretPass@2026", queried.encrypted_password))

    def test_state_store_shipment_persistence(self):
        shipment_id = f"SHP-TEST-{os.urandom(3).hex().upper()}"
        shipment = Shipment(
            id=shipment_id,
            origin="Guwahati",
            destination="Itanagar",
            cargo_items=[
                CargoItem(
                    id="C-TEST-01",
                    name="Insulin Coolers",
                    tier=1,
                    tier_name="Tier 1 Medical",
                    weight_kg=120.0,
                    volume_m3=0.8,
                    deadline_hours=6.0,
                    status="Priority"
                )
            ],
            required_delivery_hours=8.0,
            selected_vehicle_id="VEH-NER-01",
            status="Planned",
            created_at="2026-09-05 12:00:00"
        )

        state_store.save_shipment(shipment)
        self.assertIn(shipment_id, state_store.shipments)

        # Check in DB
        db_shp = self.db.query(ShipmentModel).filter(ShipmentModel.id == shipment_id).first()
        self.assertIsNotNone(db_shp)
        self.assertEqual(db_shp.origin, "Guwahati")
        self.assertEqual(db_shp.destination, "Itanagar")
        self.assertEqual(len(db_shp.cargo_items), 1)

if __name__ == "__main__":
    unittest.main()
