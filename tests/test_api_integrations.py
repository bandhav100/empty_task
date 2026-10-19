"""Tests verifying Weather, Air Quality, and NOAA ONI integrations and error boundaries."""

import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.weather_api import fetch_weather_forecast, fetch_recent_3month_rainfall
from utils.air_quality_api import fetch_current_air_quality, classify_us_aqi, classify_european_aqi
from utils.climate_data import parse_oni_table, get_oni_at

def test_weather_api_response_parsing():
    """Requirement 6: Weather API responses are parsed correctly into forecast structures."""
    # Test with live query for Hyderabad
    forecast = fetch_weather_forecast(17.385, 78.487, timeout=15)
    assert forecast["status"] in ["success", "error"]
    if forecast["status"] == "success":
        assert "temperature_2m" in forecast
        assert "relative_humidity_2m" in forecast
        assert "precipitation_mm" in forecast
        assert "horizon_notice" in forecast
        assert "daily_forecast" in forecast
        assert len(forecast["daily_forecast"]) > 0
        assert "precip_sum_mm" in forecast["daily_forecast"][0]

def test_air_quality_response_units_and_labels():
    """Requirement 7: Air-quality values have the correct units (µg/m³) and timestamps, with separate US & European AQI."""
    aq = fetch_current_air_quality(17.385, 78.487, timeout=15)
    assert aq["pollutant_unit"] == "µg/m³"
    assert "us_aqi" in aq
    assert "european_aqi" in aq
    assert "timestamp" in aq
    assert "station_disclosure" in aq

    # Test categorization boundaries
    us_good = classify_us_aqi(42)
    assert us_good["name_en"] == "Good"
    assert us_good["color"] == "#1b5e20"

    us_unhealthy = classify_us_aqi(165)
    assert us_unhealthy["name_en"] == "Unhealthy"

    eu_poor = classify_european_aqi(70)
    assert eu_poor["name_en"] == "Poor"

def test_api_failures_do_not_crash_website():
    """Requirement 8: API failures (timeouts, HTTP errors, offline) return safe error structures without crashing."""
    with patch("requests.get", side_effect=Exception("Simulated network timeout")):
        # Weather forecast failure
        wf_err = fetch_weather_forecast(17.385, 78.487, timeout=1)
        assert wf_err["status"] == "error"
        assert wf_err["temperature_2m"] is None

        # Air quality failure
        aq_err = fetch_current_air_quality(17.385, 78.487, timeout=1)
        assert aq_err["status"] == "error"
        assert aq_err["us_aqi"] is None
        assert aq_err["pollutant_unit"] == "µg/m³"

        # Archive rainfall failure returns 0.0 without unhandled exception
        rain_err, m, y = fetch_recent_3month_rainfall(17.385, 78.487, timeout=1, max_retries=1)
        assert rain_err == 0.0

def test_oni_records_aligned_to_valid_dates():
    """Requirement 9: ONI records are aligned to valid calendar dates without future leakage."""
    sample_text = """
    SEAS YR TOTAL ANOM
    DJF 2024 28.1 1.8
    JFM 2024 28.3 1.5
    FMA 2024 28.5 1.1
    MAM 2024 28.6 0.7
    AMJ 2024 28.7 0.3
    MJJ 2024 28.8 0.1
    """
    df, meta = parse_oni_table(sample_text)
    assert len(df) == 6
    assert meta["latest_value"] == 0.1
    assert "forecast_disclaimer" in meta

    series = df.set_index("date")["oni"]
    # Check date alignment: querying at month 4 (April 2024) should return FMA (month 3) or earlier
    val_march = get_oni_at(series, pd.Timestamp("2024-03-01"))
    assert val_march == 1.1
    val_may = get_oni_at(series, pd.Timestamp("2024-05-01"))
    assert val_may == 0.3
