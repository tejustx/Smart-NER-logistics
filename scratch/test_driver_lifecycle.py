import urllib.request
import urllib.error
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = "http://127.0.0.1:8000/api/trips"

print("1. Attempting to assign busy driver DRV-NER-101...")
req_data = json.dumps({
    "shipment_id": "SHP-NER-1024",
    "route_id": "RO-NER-B",
    "driver_id": "DRV-NER-101",
    "vehicle_id": "VEH-NER-01",
    "manifest_id": "MNF-NER-1024",
    "deadline_hours": 9.0
}).encode("utf-8")

req = urllib.request.Request(f"{BASE}/assign", data=req_data, headers={"Content-Type": "application/json"})
try:
    urllib.request.urlopen(req)
    print("FAILED: Expected HTTP 400, but request succeeded!")
except urllib.error.HTTPError as e:
    err = json.loads(e.read().decode())
    print(f"SUCCESS: Got expected HTTP {e.code}: {err['detail']}")

print("\n2. Releasing DRV-NER-102...")
rel_req = urllib.request.Request(f"{BASE}/drivers/DRV-NER-102/release", data=b"", headers={"Content-Type": "application/json"})
rel_res = urllib.request.urlopen(rel_req)
rel_driver = json.loads(rel_res.read().decode())
print(f"SUCCESS: Driver {rel_driver['name']} is now: {rel_driver['status']}")

print("\n3. Assigning freshly released DRV-NER-102 with 9-hour deadline...")
req_data_102 = json.dumps({
    "shipment_id": "SHP-NER-1024",
    "route_id": "RO-NER-B",
    "driver_id": "DRV-NER-102",
    "vehicle_id": "VEH-NER-01",
    "manifest_id": "MNF-NER-1024",
    "deadline_hours": 9.0
}).encode("utf-8")

req_102 = urllib.request.Request(f"{BASE}/assign", data=req_data_102, headers={"Content-Type": "application/json"})
res_102 = urllib.request.urlopen(req_102)
trip = json.loads(res_102.read().decode())
print(f"SUCCESS: Dispatched trip {trip['id']} with driver {trip['driver_name']}!")

print("\n4. Checking that DRV-NER-102 is now locked again...")
req = urllib.request.urlopen(f"{BASE}/drivers")
drivers = {d["id"]: d for d in json.loads(req.read().decode())}
d102 = drivers["DRV-NER-102"]
print(f"DRV-NER-102 status: {d102['status']}, busy_until: {d102['busy_until']}, deadline: {d102['deadline_hours']}h")
assert d102["status"] == "On Trip"
assert d102["deadline_hours"] == 9.0
print("ALL LIFECYCLE HTTP CHECKS PASSED!")
