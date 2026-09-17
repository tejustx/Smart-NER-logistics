"""
Unit Tests for Multiple Drivers Fleet & Deadline Availability Lock
"""

import unittest
from datetime import datetime, timedelta
from backend.services.state_store import state_store
from backend.models.schemas import Driver, TripAssignmentRequest
from backend.routers.trips_router import assign_trip, get_available_drivers, release_driver
from fastapi import HTTPException

class TestDriversDeadlineLock(unittest.TestCase):
    def setUp(self):
        # Reset drivers to clean testing state
        state_store.__init__()
        d1 = state_store.drivers.get("DRV-NER-101")
        if d1:
            d1.status = "Busy"
            d1.current_trip_id = "TRIP-1024"
            d1.deadline_hours = 9.0
            now_dt = datetime.now()
            d1.assigned_at = (now_dt - timedelta(minutes=35)).isoformat()
            d1.busy_until = (now_dt + timedelta(hours=8, minutes=25)).isoformat()
            state_store.save_driver(d1)
        state_store.update_driver_availabilities()

    def test_multi_driver_fleet_count_and_profiles(self):
        """Verify that at least 25 certified drivers exist in the fleet with complete attributes."""
        drivers = get_available_drivers()
        self.assertGreaterEqual(len(drivers), 25)
        
        # Check required fields
        for d in drivers:
            self.assertTrue(d.id.startswith("DRV-NER-"))
            self.assertTrue(len(d.name) > 0)
            self.assertTrue(d.experience_years > 0)
            self.assertTrue(d.hill_driving_certified)
            self.assertGreaterEqual(d.rating, 4.0)
            self.assertIn(d.status, ["Available", "On Trip", "Busy"])

    def test_initial_driver_lockout(self):
        """Verify DRV-NER-101 (Tashi Norbu) is initially locked on TRIP-1024 with deadline."""
        d1 = state_store.drivers.get("DRV-NER-101")
        self.assertIsNotNone(d1)
        self.assertIn(d1.status, ["Busy", "On Trip"])
        self.assertTrue(d1.current_trip_id.startswith("TRIP-"))
        self.assertIsNotNone(d1.busy_until)
        self.assertEqual(d1.deadline_hours, 9.0)

        # Attempting to assign Tashi Norbu must raise HTTP 400
        req = TripAssignmentRequest(
            shipment_id="SHP-TEST-01",
            route_id="RO-NER-B",
            driver_id="DRV-NER-101",
            vehicle_id="VEH-NER-01",
            manifest_id="MNF-TEST-01",
            deadline_hours=9.0
        )
        with self.assertRaises(HTTPException) as cm:
            assign_trip(req)
        self.assertEqual(cm.exception.status_code, 400)
        self.assertIn("Tashi Norbu", cm.exception.detail)
        self.assertIn("Busy", cm.exception.detail)
        self.assertIn("TRIP-", cm.exception.detail)

    def test_assign_available_driver_locks_until_deadline(self):
        """Assigning an available driver must lock them for the requested deadline hours."""
        # Release DRV-NER-102 if needed
        release_driver("DRV-NER-102")
        d2 = state_store.drivers.get("DRV-NER-102")
        self.assertEqual(d2.status, "Available")

        # Assign with 9.0 hours deadline
        req = TripAssignmentRequest(
            shipment_id="SHP-TEST-02",
            route_id="RO-NER-B",
            driver_id="DRV-NER-102",
            vehicle_id="VEH-NER-01",
            manifest_id="MNF-TEST-02",
            deadline_hours=9.0
        )
        trip = assign_trip(req)
        self.assertIsNotNone(trip)
        self.assertEqual(trip.driver_id, "DRV-NER-102")

        # Driver must now be "Busy" and locked
        d2_after = state_store.drivers.get("DRV-NER-102")
        self.assertIn(d2_after.status, ["Busy", "On Trip"])
        self.assertEqual(d2_after.current_trip_id, trip.id)
        self.assertEqual(d2_after.deadline_hours, 9.0)
        self.assertIsNotNone(d2_after.busy_until)

        # Attempting immediate re-assignment of DRV-NER-102 must fail
        with self.assertRaises(HTTPException) as cm:
            assign_trip(req)
        self.assertEqual(cm.exception.status_code, 400)
        self.assertIn("Cannot assign until shipment deadline has elapsed", cm.exception.detail)

    def test_automatic_release_after_deadline_elapses(self):
        """Simulate time advancing past busy_until: driver must automatically become Available."""
        # Release and set driver with an expired deadline
        release_driver("DRV-NER-103")
        d3 = state_store.drivers.get("DRV-NER-103")
        
        # Manually simulate a 9-hour trip that started 9.5 hours ago
        past_start = datetime.now() - timedelta(hours=9, minutes=30)
        past_deadline = datetime.now() - timedelta(minutes=30) # Expired 30 mins ago
        d3.status = "Busy"
        d3.current_trip_id = "TRIP-PAST"
        d3.assigned_at = past_start.isoformat()
        d3.busy_until = past_deadline.isoformat()
        d3.deadline_hours = 9.0
        state_store.save_driver(d3)

        # Before update, status is Busy
        self.assertIn(state_store.drivers["DRV-NER-103"].status, ["Busy", "On Trip"])

        # Running update_driver_availabilities should auto-free the driver
        state_store.update_driver_availabilities()
        d3_freed = state_store.drivers.get("DRV-NER-103")
        self.assertEqual(d3_freed.status, "Available")
        self.assertIsNone(d3_freed.busy_until)
        self.assertIsNone(d3_freed.current_trip_id)

    def test_manual_release_driver_endpoint(self):
        """Verify release_driver frees any committed driver immediately."""
        d4 = state_store.drivers.get("DRV-NER-104")
        d4.status = "Busy"
        d4.busy_until = (datetime.now() + timedelta(hours=9)).isoformat()
        d4.current_trip_id = "TRIP-TEST-104"
        state_store.save_driver(d4)

        # Call release endpoint
        freed = release_driver("DRV-NER-104")
        self.assertEqual(freed.status, "Available")
        self.assertIsNone(freed.busy_until)
        self.assertIsNone(freed.current_trip_id)

if __name__ == "__main__":
    unittest.main()
