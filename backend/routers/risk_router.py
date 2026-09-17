"""
Smart NER Logistics Intelligence Platform
Microclimate and Toe-Erosion Predictive Risk API Router

Provides:
- Machine Learning disruption inference (6h, 12h, 24h horizons)
- Physical Toe Erosion & Lacey's hydraulic scouring diagnostics
- Real-time live meteorological telemetry (Open-Meteo & IMD AWS Synced)
- Authoritative ISRO Bhuvan (1998-2022) & IMD historical catalogs for judicial audit
"""

from fastapi import APIRouter, Query
from typing import Dict, Any, Optional, List
from backend.services.ml_risk_pipeline import (
    predict_disruption_window,
    predict_route_disruption,
    get_model_metrics,
    train_and_save_model,
    ISRO_BHUVAN_DISTRICT_ATLAS
)
from backend.services.weather_service import get_live_weather, IMD_HISTORICAL_NORMALS

router = APIRouter(prefix="/api/risk", tags=["Microclimate and Toe-Erosion Risk"])

@router.get("/predict")
def predict_segment_risk(
    segment_id: str = Query(..., description="Corridor segment identifier (e.g., SEG-A1, SEG-A2, SEG-B1)")
) -> Dict[str, Any]:
    """
    Queries the trained scikit-learn toe-erosion predictive pipeline for a given road segment.
    Returns forward-looking disruption probabilities (6h/12h/24h), Lacey scour factor,
    river proximity, and ISRO Bhuvan district provenance.
    """
    prediction = predict_disruption_window(segment_id)
    return prediction

@router.get("/route-analysis")
def analyze_route_risk(
    route_id: str = Query("RO-NER-B", description="Route ID string"),
    origin: str = Query("Guwahati", description="Origin hub name"),
    destination: str = Query("Itanagar", description="Destination hub name")
) -> Dict[str, Any]:
    """
    Full Route-Level Microclimate & Toe-Erosion Evaluation:
    Combines live meteorological observations (temperature, humidity, precipitation)
    with trained RandomForest forward-looking disruption predictions and Lacey scour physics.
    """
    result = predict_route_disruption(
        route_id=route_id,
        origin=origin,
        destination=destination
    )
    return result

@router.get("/live-weather")
def get_corridor_live_weather(
    lat: float = Query(26.1445, description="Latitude of corridor waypoint"),
    lon: float = Query(91.7362, description="Longitude of corridor waypoint"),
    district: Optional[str] = Query(None, description="Optional district name hint")
) -> Dict[str, Any]:
    """
    Returns real-time meteorological observations from Open-Meteo API (synced with IMD AWS),
    with automatic in-memory caching and historical climate fallback.
    """
    return get_live_weather(lat, lon, district_hint=district)

@router.get("/historical-catalog")
def get_historical_provenance_catalog() -> Dict[str, Any]:
    """
    Judicial & Government Audit API:
    Returns the complete official ISRO Bhuvan Landslide Atlas of India (1998-2022)
    and IMD 30-Year Monsoon Precipitation Normals for all 14 NER districts and corridors.
    """
    return {
        "isro_bhuvan_landslide_atlas": ISRO_BHUVAN_DISTRICT_ATLAS,
        "imd_climatological_normals": IMD_HISTORICAL_NORMALS,
        "standards_compliance": {
            "isro_source": "ISRO/NRSC Landslide Atlas of India (NRSC 2023, ~80,000 national events)",
            "imd_source": "India Meteorological Department Historical Gridded Archives (1995-2024)",
            "elevation_model": "CartoDEM / SRTM 30m Digital Elevation Model",
            "river_network": "Central Water Commission (CWC) & OSM Hydrographic Network",
            "live_weather": "Open-Meteo High-Resolution Numerical Forecasts (IMD AWS Synced)"
        }
    }

@router.get("/model-metrics")
def get_ml_metrics() -> Dict[str, Any]:
    """
    Returns genuine evaluated validation metrics (Accuracy, Macro F1, Feature Importances,
    Data Provenance) of the trained Random Forest / MultiOutputClassifier model.
    """
    return get_model_metrics()

@router.post("/retrain")
def retrain_model() -> Dict[str, Any]:
    """Retrains and re-evaluates the toe-erosion risk model against the historical dataset."""
    return train_and_save_model(force_retrain=True)
