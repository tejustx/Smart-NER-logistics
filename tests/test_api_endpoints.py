"""
End-to-End API and Static Serving Verification Script
"""

import urllib.request
import json

BASE_URL = "http://127.0.0.1:8000"

def test_endpoint(name, url, method="GET", data=None):
    try:
        req = urllib.request.Request(url, method=method)
        if data:
            req.add_header("Content-Type", "application/json")
            req_data = json.dumps(data).encode("utf-8")
        else:
            req_data = None
        
        with urllib.request.urlopen(req, data=req_data) as resp:
            status = resp.getcode()
            body = resp.read().decode("utf-8")
            print(f"[{name}] -> Status: {status} | Bytes: {len(body)}")
            return status == 200
    except Exception as e:
        print(f"[{name}] -> ERROR: {e}")
        return False

if __name__ == "__main__":
    print("Testing Smart NER Logistics Control Platform Endpoints:")
    
    # 1. Health
    test_endpoint("Health Check", f"{BASE_URL}/api/health")
    
    # 2. Frontend HTML
    test_endpoint("Frontend Web UI", f"{BASE_URL}/")
    
    # 3. Static CSS
    test_endpoint("Frontend CSS", f"{BASE_URL}/static/css/style.css")
    
    # 4. Static JS
    test_endpoint("Frontend JS App", f"{BASE_URL}/static/js/app.js")
    test_endpoint("Frontend JS Sync", f"{BASE_URL}/static/js/offline_sync.js")
    
    # 5. USP 1 Routes
    test_endpoint("USP 1 Routes Analysis", f"{BASE_URL}/api/routes/analyze?origin=Guwahati&destination=Itanagar")
    
    # 6. Shipments & Vehicles
    test_endpoint("Vehicles List", f"{BASE_URL}/api/shipments/vehicles")
    test_endpoint("Sample Cargo", f"{BASE_URL}/api/shipments/sample-cargo")
    
    # 7. USP 2 Allocation
    test_endpoint("USP 2 Allocation Engine", f"{BASE_URL}/api/allocation/optimize", method="POST", data={
        "vehicle_id": "VEH-NER-01",
        "cargo_items": [
            {"id": "C-1", "name": "Vaccines", "tier": 1, "tier_name": "Tier 1", "weight_kg": 200, "volume_m3": 1, "deadline_hours": 6},
            {"id": "C-2", "name": "Rice Grains", "tier": 2, "tier_name": "Tier 2", "weight_kg": 800, "volume_m3": 3, "deadline_hours": 14}
        ],
        "route_id": "RO-NER-B"
    })
    
    # 8. Drivers & Trips
    test_endpoint("Drivers List", f"{BASE_URL}/api/trips/drivers")
    test_endpoint("Assigned Trip (USP 3)", f"{BASE_URL}/api/driver/assigned-trip")
    
    # 9. USP 3 Sync Telemetry
    test_endpoint("USP 3 Offline Reconnection Sync", f"{BASE_URL}/api/driver/sync-telemetry", method="POST", data={
        "trip_id": "TRIP-1024",
        "driver_id": "DRV-NER-101",
        "current_lat": 27.0844,
        "current_lng": 93.6053,
        "timestamp": "2026-09-03T00:30:00Z",
        "completed_checkpoint_names": ["Nagaon Toll Plaza (NH-27)"],
        "delivered_cargo_item_ids": ["CRG-001"],
        "local_offline_notes": "Verification test sync",
        "battery_level_pct": 95
    })
    
    # 10. Regional Control Room & What-If
    test_endpoint("Regional Overview", f"{BASE_URL}/api/gov/regional-overview")
    test_endpoint("What-If Simulator", f"{BASE_URL}/api/gov/what-if-simulate", method="POST", data={
        "blocked_corridor_id": "CORR-NH415",
        "simulated_rainfall_mm_hr": 75
    })
    
    # 11. Alerts
    test_endpoint("Disruptions Feed", f"{BASE_URL}/api/alerts/")
