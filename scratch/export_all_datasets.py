"""
Smart NER Logistics Control Platform
Exports all project datasets into clean, inspectable CSV and JSON files in backend/data/
so the team can directly open and show them to SIH judges.
"""

import os
import sys
import json
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
DATA_DIR = os.path.join(BASE_DIR, "backend", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# 1. Export the 1,600 Sample ML Training Dataset
from backend.services.ml_risk_pipeline import generate_historical_dataset, ISRO_BHUVAN_DISTRICT_ATLAS, NER_SEGMENT_GEODATA
from backend.services.weather_service import IMD_HISTORICAL_NORMALS
from backend.services.ner_network import NER_HUBS

df_train = generate_historical_dataset(n_samples=1600, random_state=42)
train_csv_path = os.path.join(DATA_DIR, "training_geohazard_dataset.csv")
df_train.to_csv(train_csv_path, index=False)
print(f"[1] Exported ML Training Dataset: {train_csv_path} ({len(df_train)} rows)")

# 2. Export ISRO Bhuvan Landslide Atlas (NER Districts)
isro_rows = []
for district, data in ISRO_BHUVAN_DISTRICT_ATLAS.items():
    row = {"district": district}
    row.update(data)
    isro_rows.append(row)

df_isro = pd.DataFrame(isro_rows)
isro_csv_path = os.path.join(DATA_DIR, "isro_bhuvan_landslide_atlas_ner.csv")
df_isro.to_csv(isro_csv_path, index=False)
print(f"[2] Exported ISRO Bhuvan District Atlas: {isro_csv_path} ({len(df_isro)} districts)")

# 3. Export IMD 30-Year Monsoon Precipitation Normals
imd_rows = []
for state, data in IMD_HISTORICAL_NORMALS.items():
    row = {"state": state}
    row.update(data)
    imd_rows.append(row)

df_imd = pd.DataFrame(imd_rows)
imd_csv_path = os.path.join(DATA_DIR, "imd_monsoon_normals_ner.csv")
df_imd.to_csv(imd_csv_path, index=False)
print(f"[3] Exported IMD Historical Normals: {imd_csv_path} ({len(df_imd)} states)")

# 4. Export NER Highway Segments Geodata
segment_rows = []
for seg_id, data in NER_SEGMENT_GEODATA.items():
    row = {"segment_id": seg_id}
    row.update(data)
    segment_rows.append(row)

df_segments = pd.DataFrame(segment_rows)
segments_csv_path = os.path.join(DATA_DIR, "ner_highway_corridors_geodata.csv")
df_segments.to_csv(segments_csv_path, index=False)
print(f"[4] Exported NER Highway Segments Geodata: {segments_csv_path} ({len(df_segments)} segments)")

# 5. Export NER 13 Logistics Hubs
hub_rows = []
for hub_name, data in NER_HUBS.items():
    hub_rows.append({
        "hub_name": hub_name,
        "state": data.get("state", "Assam"),
        "district": data.get("district", ""),
        "latitude": data["coords"][0],
        "longitude": data["coords"][1],
        "elevation_m": data.get("elevation_m", 100),
        "is_primary_depot": data.get("is_primary_depot", False)
    })

df_hubs = pd.DataFrame(hub_rows)
hubs_csv_path = os.path.join(DATA_DIR, "ner_logistics_hubs.csv")
df_hubs.to_csv(hubs_csv_path, index=False)
print(f"[5] Exported NER Logistics Hubs: {hubs_csv_path} ({len(df_hubs)} hubs)")

# 6. Export NDMA 4-Tier Emergency Relief Manifest
ndma_items = [
    {"item_id": "MED-01", "item_name": "Polyvalent Snake Antivenom Crate", "category": "Emergency Medical", "tier": 1, "priority_weight": 10000, "weight_kg": 180.0, "volume_m3": 0.45, "deadline_hours": 8, "storage_instruction": "Floor center-line, shock mounts, 2-8 C cold-chain"},
    {"item_id": "MED-02", "item_name": "Emergency Cardiac Injectables & ICU Kits", "category": "Emergency Medical", "tier": 1, "priority_weight": 10000, "weight_kg": 220.0, "volume_m3": 0.55, "deadline_hours": 12, "storage_instruction": "Forward cabin vibration-isolated mounting harness"},
    {"item_id": "MED-03", "item_name": "Liquid Medical Oxygen Cylinders (B-Type)", "category": "Emergency Medical", "tier": 1, "priority_weight": 10000, "weight_kg": 650.0, "volume_m3": 1.20, "deadline_hours": 14, "storage_instruction": "Upright strap harness anchored to vehicle chassis bed"},
    {"item_id": "MED-04", "item_name": "Trauma Surgery Surgical Packs & Blood Plasma", "category": "Emergency Medical", "tier": 1, "priority_weight": 10000, "weight_kg": 310.0, "volume_m3": 0.85, "deadline_hours": 10, "storage_instruction": "Cold-chain cooler box on low chassis platform"},
    {"item_id": "FOOD-01", "item_name": "Fortified Infant Nutrition Packs (Baby Formula)", "category": "Essential Goods", "tier": 2, "priority_weight": 5000, "weight_kg": 450.0, "volume_m3": 1.80, "deadline_hours": 24, "storage_instruction": "Reinforced waterproof tarpaulin cover"},
    {"item_id": "FOOD-02", "item_name": "High-Calorie Ready-to-Eat Emergency Meals", "category": "Essential Goods", "tier": 2, "priority_weight": 5000, "weight_kg": 1200.0, "volume_m3": 3.40, "deadline_hours": 36, "storage_instruction": "Moisture-isolated middle bay pallet stack"},
    {"item_id": "FOOD-03", "item_name": "Water Purification Chemical Kits & Tablets", "category": "Essential Goods", "tier": 2, "priority_weight": 5000, "weight_kg": 280.0, "volume_m3": 0.90, "deadline_hours": 24, "storage_instruction": "Elevated pallet to prevent water ingress"},
    {"item_id": "INFRA-01", "item_name": "Bailey Bridge Steel Transom Pins & Hardware", "category": "Infrastructure", "tier": 3, "priority_weight": 1000, "weight_kg": 1800.0, "volume_m3": 2.20, "deadline_hours": 48, "storage_instruction": "Direct floor anchor bolts along vehicle axle center"},
    {"item_id": "INFRA-02", "item_name": "Diesel Generator Set (25 kVA Compact Skid)", "category": "Infrastructure", "tier": 3, "priority_weight": 1000, "weight_kg": 950.0, "volume_m3": 2.80, "deadline_hours": 48, "storage_instruction": "Chassis center tied down with heavy-duty ratchets"},
    {"item_id": "INFRA-03", "item_name": "Excavator Tow Winch Cables & Snatch Blocks", "category": "Infrastructure", "tier": 3, "priority_weight": 1000, "weight_kg": 420.0, "volume_m3": 0.70, "deadline_hours": 72, "storage_instruction": "Rear bay floor containment"},
    {"item_id": "COMM-01", "item_name": "General Commercial FMCG Dry Groceries", "category": "Commercial Cargo", "tier": 4, "priority_weight": 100, "weight_kg": 1400.0, "volume_m3": 6.50, "deadline_hours": 96, "storage_instruction": "Upper deck or staged for Convoy Wave 2"},
    {"item_id": "COMM-02", "item_name": "Regional Hardware & Construction Material", "category": "Commercial Cargo", "tier": 4, "priority_weight": 100, "weight_kg": 2100.0, "volume_m3": 8.20, "deadline_hours": 120, "storage_instruction": "Staged for Convoy Wave 2 (Deferred if truck full)"}
]

df_ndma = pd.DataFrame(ndma_items)
ndma_csv_path = os.path.join(DATA_DIR, "ndma_relief_cargo_manifest.csv")
df_ndma.to_csv(ndma_csv_path, index=False)
print(f"[6] Exported NDMA Relief Cargo Manifest: {ndma_csv_path} ({len(df_ndma)} items)")

print("\nALL 6 DATASETS SUCCESSFULLY EXPORTED TO backend/data/ AS INSPECTABLE CSV FILES!")
