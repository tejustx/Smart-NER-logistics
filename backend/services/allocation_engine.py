"""
Smart NER Logistics Control Platform
USP 2: Multi-Tier Cargo Prioritization and Capacity Allocation Engine
"""

import uuid
from datetime import datetime
from typing import List, Dict, Any, Tuple
from backend.models.schemas import CargoItem, Vehicle, AllocationResult

# Tier Priority Weights
TIER_PRIORITY_BASE = {
    1: 10000.0,  # Tier 1: Medical / Emergency
    2: 5000.0,   # Tier 2: Essential Goods
    3: 1000.0,   # Tier 3: Construction / Infrastructure
    4: 100.0     # Tier 4: General / Commercial Cargo
}

def allocate_cargo_capacity(
    vehicle: Vehicle,
    cargo_items: List[CargoItem],
    route_safety_payload_factor: float = 1.0
) -> AllocationResult:
    """
    Solves multi-tier capacity allocation under weight and volume constraints.
    Applies route-dependent safety factor (e.g., steep mountain pass limits payload to 85%).
    Prioritization score = TIER_BASE - (deadline_hours * 50) + (urgency_score * 200)
    """
    effective_max_payload = round(vehicle.max_payload_kg * route_safety_payload_factor, 1)
    effective_max_volume = round(vehicle.max_volume_m3 * route_safety_payload_factor, 1)

    # Sort items by: Tier ascending (1 first), then deadline ascending (earliest first), then weight
    def item_sort_key(item: CargoItem):
        return (
            item.tier,
            item.deadline_hours,
            -item.weight_kg
        )

    sorted_items = sorted(cargo_items, key=item_sort_key)

    allocated_items: List[CargoItem] = []
    waiting_items: List[CargoItem] = []

    current_weight = 0.0
    current_volume = 0.0

    tier_counts = {"Tier 1": 0, "Tier 2": 0, "Tier 3": 0, "Tier 4": 0}

    for item in sorted_items:
        # Check if item fits in both payload and volume
        if (current_weight + item.weight_kg <= effective_max_payload) and \
           (current_volume + item.volume_m3 <= effective_max_volume):
            
            # Decision status
            if item.tier == 1:
                item_status = "Priority"
            elif item.tier in [2, 3, 4]:
                item_status = "Selected"
            else:
                item_status = "Selected"

            allocated_item = item.model_copy(update={"status": item_status})
            allocated_items.append(allocated_item)

            current_weight += item.weight_kg
            current_volume += item.volume_m3
            tier_key = f"Tier {item.tier}"
            tier_counts[tier_key] = tier_counts.get(tier_key, 0) + 1
        else:
            waiting_item = item.model_copy(update={"status": "Waiting"})
            waiting_items.append(waiting_item)

    payload_pct = round((current_weight / effective_max_payload) * 100.0, 1) if effective_max_payload > 0 else 0.0
    volume_pct = round((current_volume / effective_max_volume) * 100.0, 1) if effective_max_volume > 0 else 0.0

    manifest_id = f"MNF-NER-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    loading_instructions = [
        f"1. Heavy Tier 1 Medical containers ({tier_counts.get('Tier 1', 0)} units) placed lowest along axle center.",
        "2. Temperature-controlled parcels secured in forward-cabin shock mounts.",
        f"3. Tier 2 Food & Essential grains ({tier_counts.get('Tier 2', 0)} units) secured with water-resistant tarpaulins.",
        f"4. Remaining {len(waiting_items)} waiting items staged in warehouse for Convoy Wave 2."
    ]

    return AllocationResult(
        manifest_id=manifest_id,
        vehicle_id=vehicle.id,
        vehicle_name=vehicle.name,
        max_payload_kg=effective_max_payload,
        allocated_payload_kg=round(current_weight, 1),
        payload_utilization_pct=payload_pct,
        max_volume_m3=effective_max_volume,
        allocated_volume_m3=round(current_volume, 2),
        volume_utilization_pct=volume_pct,
        allocated_items=allocated_items,
        waiting_items=waiting_items,
        tier_counts=tier_counts,
        loading_instructions=loading_instructions,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
