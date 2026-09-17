"""
Unit Tests for Smart NER Logistics Control Platform Backend
"""

import unittest
from backend.services.risk_engine import calculate_segment_risk, compare_route_tradeoffs
from backend.services.allocation_engine import allocate_cargo_capacity
from backend.models.schemas import Vehicle, CargoItem
from backend.services.state_store import state_store
from backend.services.ner_network import generate_route_options

class TestNERPlatform(unittest.TestCase):
    def test_risk_calculation(self):
        # High rainfall + high slope -> high risk
        risk_high = calculate_segment_risk(
            rainfall_mm_hr=85.0,
            slope_gradient_pct=28.0,
            historical_landslide_freq=0.85,
            road_quality_index=0.40
        )
        self.assertGreaterEqual(risk_high.raw_risk_score, 80.0)
        self.assertIn(risk_high.risk_level, ["High", "Critical"])
        self.assertGreater(risk_high.effective_cost_multiplier, 1.5)

        # Mild conditions -> low risk
        risk_low = calculate_segment_risk(
            rainfall_mm_hr=15.0,
            slope_gradient_pct=4.0,
            historical_landslide_freq=0.10,
            road_quality_index=0.90
        )
        self.assertLess(risk_low.raw_risk_score, 30.0)
        self.assertEqual(risk_low.risk_level, "Low")

    def test_route_generation_recommendation(self):
        routes = generate_route_options("Guwahati", "Itanagar")
        self.assertEqual(len(routes), 2)
        route_a = routes[0]
        route_b = routes[1]

        # Route A: Shorter but High Risk
        self.assertFalse(route_a.is_recommended)
        self.assertGreater(route_a.risk_score, 70.0)
        self.assertLess(route_a.total_distance_km, route_b.total_distance_km)

        # Route B: Longer but Low Risk -> RECOMMENDED
        self.assertTrue(route_b.is_recommended)
        self.assertLess(route_b.risk_score, 35.0)

    def test_cargo_allocation_usp2(self):
        vehicle = Vehicle(
            id="TEST-VEH",
            name="Test 5T Truck",
            model="Tata 715",
            max_payload_kg=1000.0,
            max_volume_m3=5.0,
            hill_grade_rating="Grade A",
            fuel_type="Diesel",
            license_plate="AS-01-TEST"
        )
        cargo_items = [
            CargoItem(id="1", name="Medicines", tier=1, tier_name="Tier 1", weight_kg=200.0, volume_m3=1.0, deadline_hours=6.0),
            CargoItem(id="2", name="Food", tier=2, tier_name="Tier 2", weight_kg=500.0, volume_m3=2.0, deadline_hours=12.0),
            CargoItem(id="3", name="Cement", tier=3, tier_name="Tier 3", weight_kg=600.0, volume_m3=2.0, deadline_hours=48.0),
            CargoItem(id="4", name="Retail Goods", tier=4, tier_name="Tier 4", weight_kg=400.0, volume_m3=2.0, deadline_hours=72.0),
        ]

        result = allocate_cargo_capacity(vehicle, cargo_items)
        allocated_ids = [i.id for i in result.allocated_items]
        waiting_ids = [i.id for i in result.waiting_items]

        # Tier 1 (200kg) and Tier 2 (500kg) fit in 1000kg (total 700kg)
        self.assertIn("1", allocated_ids)
        self.assertIn("2", allocated_ids)
        # Tier 3 (600kg) does not fit (700+600 > 1000) so must be in waiting
        self.assertIn("3", waiting_ids)
        self.assertIn("4", waiting_ids)
        self.assertEqual(result.allocated_payload_kg, 700.0)

    def test_offline_sync(self):
        trip = state_store.trips.get("TRIP-1024")
        self.assertIsNotNone(trip)
        self.assertEqual(trip.origin, "Guwahati")
        self.assertEqual(trip.destination, "Itanagar")

if __name__ == "__main__":
    unittest.main()
