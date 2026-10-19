"""Feature engineering functions for training and inference.
Implements multi-scale rainfall lags, seasonal normals, and ENSO signals.
"""

import math
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import json
import numpy as np
import pandas as pd
from utils.districts import DISTRICTS, normalize_district_name
from utils.climate_data import get_oni_at

def cyclical_month_encoding(month: int) -> Tuple[float, float]:
    """Sinusoidal cyclical encoding for calendar month (1-12)."""
    angle = 2.0 * math.pi * month / 12.0
    return math.sin(angle), math.cos(angle)

def get_season_code(month: int) -> int:
    """Classifies month into 4 Indian Meteorological Department seasonal windows."""
    if month in [1, 2]:
        return 1  # Winter
    elif month in [3, 4, 5]:
        return 2  # Pre-Monsoon
    elif month in [6, 7, 8, 9]:
        return 3  # Southwest Monsoon
    else:
        return 4  # Post-Monsoon

def calculate_rainfall_percentile(rain3_mm: float, hist_rain3_list: List[float]) -> float:
    """Computes empirical CDF percentile (0.0 to 1.0) against historical seasonal distribution."""
    if not hist_rain3_list:
        return 0.5
    hist = np.array(hist_rain3_list)
    pct = float((hist < rain3_mm).mean() + 0.5 * (hist == rain3_mm).mean())
    return min(max(pct, 0.0), 1.0)

def load_seasonal_normals() -> Dict[str, Dict[str, float]]:
    """Loads training-only climatological normals (2005-2019) per district and calendar month."""
    candidates = [
        Path("data/processed/clim_normals.json"),
        Path(__file__).parent.parent / "data" / "processed" / "clim_normals.json"
    ]
    for p in candidates:
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    return {}

def build_ml_inference_features(
    district: str,
    recent_rain_1m: float,
    recent_rain_3m: float,
    month: int,
    year: int,
    oni_series: pd.Series,
    expected_features: List[str],
    recent_rain_6m: Optional[float] = None,
    recent_rain_12m: Optional[float] = None,
    normals_dict: Optional[Dict[str, Dict[str, float]]] = None
) -> pd.DataFrame:
    """
    Constructs the exact feature row required by the production Random Forest model.
    Strictly prevents future leakage by calculating features relative to training-only normals.
    """
    canonical_district = normalize_district_name(district)
    lat, lon = DISTRICTS[canonical_district]

    if normals_dict is None:
        normals_dict = load_seasonal_normals()

    month_str = str(month)
    district_normals = normals_dict.get(canonical_district, {})
    if not district_normals and "Kumuram Bheem Asifabad" in normals_dict and canonical_district == "Kumuram Bheem":
        district_normals = normals_dict["Kumuram Bheem Asifabad"]
    
    # Retrieve training normal for this season
    normal_rain3 = district_normals.get(month_str, max(recent_rain_3m, 50.0))

    # Fallbacks for multi-month accumulation if not provided
    if recent_rain_6m is None:
        recent_rain_6m = max(recent_rain_3m * 1.8, 10.0)
    if recent_rain_12m is None:
        recent_rain_12m = max(recent_rain_6m * 1.9, 20.0)

    # Anomaly / deficit relative to training normal
    clamped_norm = max(normal_rain3, 5.0)
    recent_deficit = (clamped_norm - recent_rain_3m) / clamped_norm
    recent_ratio = recent_rain_3m / clamped_norm

    msin, mcos = cyclical_month_encoding(month)
    season = get_season_code(month)

    # ONI features (strictly as of prediction timestamp t)
    ts = pd.Timestamp(year=year, month=month, day=1)
    oni_now = get_oni_at(oni_series, ts)
    oni_prev_3m = get_oni_at(oni_series, ts - pd.DateOffset(months=3))
    oni_delta = oni_now - oni_prev_3m

    feature_dict = {
        "rain1": round(float(recent_rain_1m), 2),
        "rain3": round(float(recent_rain_3m), 2),
        "rain6": round(float(recent_rain_6m), 2),
        "rain12": round(float(recent_rain_12m), 2),
        "normal_rain3": round(float(normal_rain3), 2),
        "recent_deficit": round(float(recent_deficit), 4),
        "recent_ratio": round(float(recent_ratio), 4),
        "msin": round(float(msin), 4),
        "mcos": round(float(mcos), 4),
        "season": int(season),
        "lat": round(float(lat), 4),
        "lon": round(float(lon), 4),
        "oni_now": round(float(oni_now), 3),
        "oni_prev_3m": round(float(oni_prev_3m), 3),
        "oni_delta": round(float(oni_delta), 3)
    }

    # Verify that all expected features exist
    missing = [f for f in expected_features if f not in feature_dict]
    if missing:
        raise KeyError(f"Feature schema mismatch. Missing required features: {missing}")

    df = pd.DataFrame([feature_dict])
    return df[expected_features]

# Backward compatibility alias
def build_inference_features(
    district: str,
    rain3_mm: float,
    month: int,
    year: int,
    oni_series: pd.Series,
    clim: Dict[str, Dict[str, list[float]]],
    expected_features: List[str]
) -> pd.DataFrame:
    """Wrapper ensuring backward compatibility with earlier calling conventions."""
    recent_1m = rain3_mm * 0.33
    return build_ml_inference_features(
        district=district,
        recent_rain_1m=recent_1m,
        recent_rain_3m=rain3_mm,
        month=month,
        year=year,
        oni_series=oni_series,
        expected_features=expected_features
    )
