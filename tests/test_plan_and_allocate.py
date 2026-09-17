"""
Unit and Integration Tests for Feature A (Merged Plan & Allocate)
and Feature B (Micro-Climate & Toe-Erosion ML Predictive Pipeline)
"""

import os
import unittest
from backend.main import unified_plan_and_allocate
from backend.routers.risk_router import predict_segment_risk, get_ml_metrics
from backend.models.schemas import CargoItem, PlanAndAllocateRequest
from backend.services.ml_risk_pipeline import (
    get_or_load_model,
    get_model_metrics,
    predict_disruption_window,
    MODEL_FILE_PATH,
    METRICS_FILE_PATH
)

class TestPlanAndAllocateIntegration(unittest.TestCase):

    def test_feature_b_model_and_metrics_integrity(self):
        """Verify the trained ML model exists on disk with real evaluated metrics."""
        self.assertTrue(os.path.exists(MODEL_FILE_PATH), "Model joblib file must exist")
        self.assertTrue(os.path.exists(METRICS_FILE_PATH), "Model metrics JSON must exist")

        metrics = get_model_metrics()
        self.assertIn("overall_accuracy", metrics)
        self.assertIn("overall_macro_f1", metrics)
        self.assertGreater(metrics["overall_accuracy"], 0.75, "Model accuracy should be sound")
        self.assertGreater(metrics["overall_macro_f1"], 0.70, "Macro F1 should be sound")
        self.assertIn("6h", metrics["horizons"])
        self.assertIn("12h", metrics["horizons"])
        self.assertIn("24h", metrics["horizons"])

        # Check feature importances
        importances = metrics["feature_importances"]
        self.assertIn("river_proximity_km", importances)
        self.assertIn("rainfall_intensity_mm_hr", importances)
        self.assertIn("slope_gradient_pct", importances)

    def test_feature_b_toe_erosion_inference(self):
        """Verify forward predictions reflect toe-erosion physics."""
        pred_a2 = predict_disruption_window("SEG-A2")
        pred_b1 = predict_disruption_window("SEG-B1")

        self.assertIn("6h", pred_a2["disruption_probability"])
        self.assertIn("12h", pred_a2["disruption_probability"])
        self.assertIn("24h", pred_a2["disruption_probability"])

        # SEG-A2 (high rain + 28% slope + close river toe) must be significantly riskier than SEG-B1
        self.assertGreater(
            pred_a2["disruption_probability"]["12h"],
            pred_b1["disruption_probability"]["12h"]
        )
        self.assertGreater(
            pred_a2["disruption_probability"]["24h"],
            pred_b1["disruption_probability"]["24h"]
        )

    def test_api_risk_predict_endpoint(self):
        """Test GET /api/risk/predict?segment_id=SEG-A2 endpoint."""
        data = predict_segment_risk(segment_id="SEG-A2")
        self.assertEqual(data["segment_id"], "SEG-A2")
        self.assertIn("disruption_probability", data)
        self.assertIn("6h", data["disruption_probability"])
        self.assertIn("12h", data["disruption_probability"])
        self.assertIn("24h", data["disruption_probability"])
        self.assertIn("toe_erosion_diagnostic", data)

    def test_api_model_metrics_endpoint(self):
        """Test GET /api/risk/model-metrics endpoint."""
        data = get_ml_metrics()
        self.assertIn("overall_accuracy", data)
        self.assertIn("overall_macro_f1", data)
        self.assertIn("data_provenance", data)

    def test_combined_plan_and_allocate_endpoint(self):
        """
        Test POST /api/plan-and-allocate (Feature A + Feature B unified core).
        Verifies single response schema and Tier 1 medical cargo priority knapsack packing.
        """
        req = PlanAndAllocateRequest(
            origin="Guwahati",
            destination="Itanagar",
            cargo_items=[
                CargoItem(
                    id="C-MED-01",
                    name="Emergency Vaccines & Plasma",
                    tier=1,
                    tier_name="Tier 1 Medical/Emergency",
                    weight_kg=350.0,
                    volume_m3=1.2,
                    deadline_hours=6.0,
                    status="Waiting"
                ),
                CargoItem(
                    id="C-FOOD-02",
                    name="Disaster Relief Rations",
                    tier=2,
                    tier_name="Tier 2 Essential Goods",
                    weight_kg=2100.0,
                    volume_m3=8.5,
                    deadline_hours=14.0,
                    status="Waiting"
                ),
                CargoItem(
                    id="C-CONST-03",
                    name="Bailey Bridge Reinforced Pins",
                    tier=3,
                    tier_name="Tier 3 Construction",
                    weight_kg=3200.0,
                    volume_m3=5.0,
                    deadline_hours=48.0,
                    status="Waiting"
                )
            ],
            vehicle_id="VEH-NER-01"
        )

        data = unified_plan_and_allocate(req)

        # 1. Verify route block
        self.assertIn("route", data)
        route = data["route"]
        self.assertIn("selected_route", route)
        self.assertIn("distance_km", route)
        self.assertIn("risk_score", route)
        self.assertIn("predicted_risk", route)
        self.assertIn("alt_routes", route)
        self.assertIn("6h", route["predicted_risk"])
        self.assertIn("12h", route["predicted_risk"])
        self.assertIn("24h", route["predicted_risk"])

        # 2. Verify allocation block
        self.assertIn("allocation", data)
        alloc = data["allocation"]
        self.assertIn("manifest_id", alloc)
        self.assertIn("packed_items", alloc)
        self.assertIn("waiting_items", alloc)
        self.assertIn("utilization", alloc)

        # 3. Verify Tier 1 Priority Packing
        packed_ids = [item.id if hasattr(item, "id") else item["id"] for item in alloc["packed_items"]]
        self.assertIn("C-MED-01", packed_ids, "Tier 1 medical cargo must be packed")

        # 4. Verify Route explainability
        sel_route = route["selected_route"]
        rec_reason = getattr(sel_route, "recommendation_reason", None) or sel_route.get("recommendation_reason", "")
        self.assertTrue(
            "reduces risk by" in rec_reason.lower() or "selected" in rec_reason.lower(),
            "Recommendation reason must explain why route was chosen"
        )

    def test_selected_route_prediction_distinct_from_alt(self):
        """
        Verify that microclimate & toe-erosion risk predictions are generated
        for the selected route as well as candidate alternate routes.
        """
        req = PlanAndAllocateRequest(
            origin="Guwahati",
            destination="Itanagar",
            cargo_items=[],
            vehicle_id="VEH-NER-01"
        )
        data = unified_plan_and_allocate(req)
        sel_route = data["route"]["selected_route"]
        alt_routes = data["route"]["alt_routes"]

        # Verify selected route has dynamic risk prediction
        sel_pred = sel_route.predicted_risk if hasattr(sel_route, "predicted_risk") else sel_route["predicted_risk"]
        self.assertIn("6h", sel_pred)
        self.assertIn("12h", sel_pred)
        self.assertIn("24h", sel_pred)

        # Verify alternate route also has dynamic risk prediction
        self.assertTrue(len(alt_routes) > 0)
        alt_0 = alt_routes[0]
        alt_pred = alt_0.predicted_risk if hasattr(alt_0, "predicted_risk") else alt_0["predicted_risk"]
        self.assertIn("6h", alt_pred)
        self.assertIn("12h", alt_pred)
        self.assertIn("24h", alt_pred)

        # Safe route risk should be lower than high-hazard alternate route
        self.assertLess(sel_pred["12h"], alt_pred["12h"])

    def test_feature_b_live_weather_service(self):
        """Verify real-time meteorological observations are returned with valid fields."""
        from backend.services.weather_service import get_live_weather
        wx = get_live_weather(26.1445, 91.7362, "Kamrup Metropolitan")
        self.assertIn("temperature_c", wx)
        self.assertIn("relative_humidity_pct", wx)
        self.assertIn("precipitation_mm_hr", wx)
        self.assertIn("precipitation_24h_mm", wx)
        self.assertIn("weather_condition", wx)
        self.assertIn("source", wx)

    def test_feature_b_every_route_has_segments_and_toe_erosion(self):
        """Verify that every route corridor generates concrete segments and toe-erosion data."""
        from backend.services.ner_network import generate_route_options
        test_corridors = [
            ("Guwahati", "Itanagar"),
            ("Guwahati", "Shillong"),
            ("Tezpur", "Tawang"),
            ("Silchar", "Aizawl"),
            ("Dimapur", "Kohima"),
            ("Guwahati", "Gangtok")
        ]
        for orig, dest in test_corridors:
            routes = generate_route_options(orig, dest)
            self.assertEqual(len(routes), 2, f"Corridor {orig}->{dest} must return 2 routes")
            for r in routes:
                self.assertGreater(len(r.segments), 0, f"Route {r.name} must have non-empty segments")
                self.assertIsNotNone(r.predicted_risk, f"Route {r.name} must have predicted_risk")
                self.assertIn("6h", r.predicted_risk)
                self.assertIn("12h", r.predicted_risk)
                self.assertIn("24h", r.predicted_risk)
                self.assertIsNotNone(r.toe_erosion_hazard, f"Route {r.name} must have toe_erosion_hazard")
                self.assertIsNotNone(r.primary_river, f"Route {r.name} must have primary_river")
                self.assertIsNotNone(r.geotechnical_explanation, f"Route {r.name} must have geotechnical_explanation")

    def test_feature_b_historical_catalog_and_route_analysis_endpoints(self):
        """Verify historical catalog and route analysis endpoints return verified data."""
        from backend.routers.risk_router import analyze_route_risk, get_historical_provenance_catalog
        catalog = get_historical_provenance_catalog()
        self.assertIn("isro_bhuvan_landslide_atlas", catalog)
        self.assertIn("imd_climatological_normals", catalog)
        self.assertGreaterEqual(len(catalog["isro_bhuvan_landslide_atlas"]), 10)

        analysis = analyze_route_risk("RO-NER-B", "Guwahati", "Itanagar")
        self.assertIn("disruption_probability", analysis)
        self.assertIn("toe_erosion_hazard", analysis)
        self.assertIn("geotechnical_explanation", analysis)
        self.assertIn("isro_bhuvan_data", analysis)


if __name__ == "__main__":
    unittest.main()
