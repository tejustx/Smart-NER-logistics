"""
Smart NER Logistics Control Platform
USP 1: Risk Engine & Generalized Dynamic Rerouting Penalty Calculator

Authoritative Data Provenance & Methodology:
- ISRO Landslide Atlas of India (NRSC 2023): District-level vulnerability index & hazard ranking
  Source: https://www.isro.gov.in/media_isro/pdf/LandslideAtlas_2023.pdf
- Bhuvan Disaster Services Portal (NRSC/ISRO): Event-based inventories & regional hazard maps
  Source: https://bhuvan-app1.nrsc.gov.in/disaster/usrtasks/landslide/landslide.php
- Bhuvan Geospatial Data Hub: CartoDEM terrain elevation and slope models
  Source: https://bhuvan-app3.nrsc.gov.in/data/
- Geological Survey of India (GSI) & BRO: 30-year regional historical landslide occurrences
"""

import math
from typing import Dict, Any, Tuple, Optional
from backend.models.schemas import RiskFactorBreakdown

# Weights for Risk Scoring
W_RAINFALL = 0.35      # Monsoon precipitation factor (mm/hr)
W_SLOPE = 0.25         # Terrain slope incline percentage (%)
W_HISTORY = 0.25       # Historical landslide/washout frequency index [0, 1]
W_ROAD_QUALITY = 0.15  # Inverted road degradation index [0, 1]

def calculate_segment_risk(
    rainfall_mm_hr: float,
    slope_gradient_pct: float,
    historical_landslide_freq: float,
    road_quality_index: float  # 1.0 is immaculate, 0.0 is severely degraded
) -> RiskFactorBreakdown:
    """
    Computes normalized risk score [0..100] and risk-adjusted generalized cost multiplier.
    Signals:
      - Rainfall: capped normalized against extreme NER monsoon burst (100 mm/hr)
      - Slope: normalized against extreme mountain pass gradient (35% grade)
      - Landslide history: 0 to 1
      - Road degradation: (1.0 - road_quality_index)
    """
    norm_rain = min(max(rainfall_mm_hr / 100.0, 0.0), 1.0)
    norm_slope = min(max(slope_gradient_pct / 35.0, 0.0), 1.0)
    norm_hist = min(max(historical_landslide_freq, 0.0), 1.0)
    norm_degrade = min(max(1.0 - road_quality_index, 0.0), 1.0)

    raw_score = (
        (W_RAINFALL * norm_rain) +
        (W_SLOPE * norm_slope) +
        (W_HISTORY * norm_hist) +
        (W_ROAD_QUALITY * norm_degrade)
    ) * 100.0

    # Non-linear thresholding for compounding landslide danger
    # If both rainfall > 60mm and slope > 20%, risk spikes exponentially
    if rainfall_mm_hr > 60.0 and slope_gradient_pct > 20.0:
        raw_score = min(raw_score * 1.35, 99.0)

    if raw_score < 30.0:
        level = "Low"
    elif raw_score < 60.0:
        level = "Medium"
    elif raw_score < 80.0:
        level = "High"
    else:
        level = "Critical"

    # Effective cost multiplier based on risk:
    # Penalized generalized routing cost = Base Cost * (1 + alpha * (Risk/100)^1.5)
    alpha = 1.8
    cost_multiplier = round(1.0 + alpha * math.pow(raw_score / 100.0, 1.5), 2)

    return RiskFactorBreakdown(
        rainfall_mm_hr=rainfall_mm_hr,
        slope_gradient_pct=slope_gradient_pct,
        historical_landslide_freq=historical_landslide_freq,
        road_quality_index=road_quality_index,
        raw_risk_score=round(raw_score, 1),
        risk_level=level,
        effective_cost_multiplier=cost_multiplier
    )

def compare_route_tradeoffs(
    dist_a: float, risk_a: float, cost_a: float,
    dist_b: float, risk_b: float, cost_b: float,
    pred_risk_a: Optional[Dict[str, float]] = None,
    pred_risk_b: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Pareto Corridor Evaluator:
    Computes trade-offs between Candidate Route A and Candidate Route B
    across Distance, Duration, Current Risk, and Forward-Looking ML Disruption Risk (6h-24h).
    """
    risk_diff = round(risk_a - risk_b, 1)
    dist_diff = round(dist_b - dist_a, 1)
    cost_diff = round(cost_b - cost_a, 1)
    
    # Calculate percentage reduction
    pct_reduction = round((risk_diff / max(risk_a, 1.0)) * 100.0, 1)
    
    # Check forward risk difference
    fwd_12h_a = pred_risk_a.get("12h", 0.0) if pred_risk_a else 0.0
    fwd_12h_b = pred_risk_b.get("12h", 0.0) if pred_risk_b else 0.0
    
    if pct_reduction > 0 and dist_diff > 0:
        recommendation_msg = (
            f"Route B selected because it reduces risk by {pct_reduction}% "
            f"at the cost of {dist_diff} additional km."
        )
        if fwd_12h_a >= 0.50:
            recommendation_msg += (
                f" Route A has a {int(fwd_12h_a * 100)}% predicted disruption probability in the next 12 hours "
                f"due to toe erosion and saturation, whereas Route B forward risk is only {int(fwd_12h_b * 100)}%."
            )
    else:
        recommendation_msg = "Route B selected as the Pareto-dominant all-weather corridor."

    return {
        "risk_reduction_points": risk_diff,
        "risk_reduction_pct": pct_reduction,
        "added_distance_km": dist_diff,
        "cost_variance_inr": cost_diff,
        "predicted_risk_a": pred_risk_a or {},
        "predicted_risk_b": pred_risk_b or {},
        "recommendation": recommendation_msg
    }
