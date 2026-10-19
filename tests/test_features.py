"""Unit tests for feature engineering transformations and lag calculations."""

import pytest
import math
import pandas as pd
from utils.feature_engineering import (
    calculate_rainfall_percentile,
    cyclical_month_encoding,
    get_season_code,
    load_seasonal_normals,
    build_ml_inference_features
)
from utils.districts import EXACT_33_DISTRICTS

def test_calculate_rainfall_percentile():
    hist = [10.0, 20.0, 30.0, 40.0, 50.0]
    
    # Driest possible value
    pct_min = calculate_rainfall_percentile(5.0, hist)
    assert pct_min == 0.0

    # Wettest possible value
    pct_max = calculate_rainfall_percentile(60.0, hist)
    assert pct_max == 1.0

    # Median value (30.0 has 2 below, 1 equal -> (2 + 0.5)/5 = 0.5)
    pct_mid = calculate_rainfall_percentile(30.0, hist)
    assert abs(pct_mid - 0.5) < 1e-4

def test_cyclical_month_encoding():
    # Month 12: sin(2pi) = 0, cos(2pi) = 1
    sin_12, cos_12 = cyclical_month_encoding(12)
    assert abs(sin_12) < 1e-5
    assert abs(cos_12 - 1.0) < 1e-5

    # Month 6: sin(pi) = 0, cos(pi) = -1
    sin_6, cos_6 = cyclical_month_encoding(6)
    assert abs(sin_6) < 1e-5
    assert abs(cos_6 - (-1.0)) < 1e-5

def test_get_season_code():
    assert get_season_code(1) == 1  # Jan = Winter
    assert get_season_code(4) == 2  # Apr = Pre-monsoon
    assert get_season_code(7) == 3  # Jul = Monsoon
    assert get_season_code(10) == 4 # Oct = Post-monsoon

def test_load_seasonal_normals():
    normals = load_seasonal_normals()
    assert len(normals) >= 33
    for d in EXACT_33_DISTRICTS:
        assert d in normals or (d == "Kumuram Bheem" and "Kumuram Bheem Asifabad" in normals)

def test_build_ml_inference_features():
    dummy_oni = pd.Series([0.5, 0.4, 0.2], index=pd.date_range("2024-01-01", "2024-03-01", freq="MS"))
    feats = [
        "rain1", "rain3", "rain6", "rain12", "normal_rain3",
        "recent_deficit", "recent_ratio", "msin", "mcos", "season", "lat", "lon",
        "oni_now", "oni_prev_3m", "oni_delta"
    ]
    df = build_ml_inference_features(
        district="Hyderabad",
        recent_rain_1m=15.0,
        recent_rain_3m=85.0,
        month=3,
        year=2024,
        oni_series=dummy_oni,
        expected_features=feats
    )
    assert len(df) == 1
    assert list(df.columns) == feats
    assert not df.isna().any().any()
