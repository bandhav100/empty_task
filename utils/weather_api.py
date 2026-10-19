"""Open-Meteo Weather API integration (Forecast and Historical Archive).
Uses documented free API endpoints with retries, caching, and explicit forecast horizon disclosures.
"""

import time
import datetime as dt
from typing import Dict, Any, Tuple, Optional, List
import pandas as pd
import requests

OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# WMO Weather interpretation codes
WMO_WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
}

def fetch_weather_forecast(lat: float, lon: float, timeout: int = 15, max_retries: int = 3) -> Dict[str, Any]:
    """
    Fetches real-time weather and 7-day forecast from official Open-Meteo forecast API.
    
    IMPORTANT SCIENTIFIC DISCLOSURE:
    This endpoint provides a limited synoptic horizon (up to 7-14 days max) and is NOT
    a 3-month seasonal climate forecast. Do NOT extrapolate short-range forecasts into
    a multi-month water stress outlook.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m",
        "daily": "precipitation_sum,precipitation_probability_max,temperature_2m_max,temperature_2m_min,weather_code",
        "forecast_days": 7,
        "timezone": "Asia/Kolkata"
    }

    last_exc = None
    for attempt in range(max_retries):
        try:
            resp = requests.get(OPEN_METEO_FORECAST_URL, params=params, timeout=timeout)
            if resp.status_code == 200:
                data = resp.json()
                current = data.get("current", {})
                daily = data.get("daily", {})

                weather_code = current.get("weather_code", 0)
                weather_desc = WMO_WEATHER_CODES.get(weather_code, "Partly cloudy")

                # Parse daily forecast cards
                daily_cards = []
                dates = daily.get("time", [])
                p_sums = daily.get("precipitation_sum", [])
                p_probs = daily.get("precipitation_probability_max", [])
                t_maxs = daily.get("temperature_2m_max", [])
                t_mins = daily.get("temperature_2m_min", [])

                for i in range(len(dates)):
                    daily_cards.append({
                        "date": dates[i],
                        "precip_sum_mm": p_sums[i] if i < len(p_sums) else 0.0,
                        "precip_prob_pct": p_probs[i] if i < len(p_probs) else 0,
                        "temp_max_c": t_maxs[i] if i < len(t_maxs) else None,
                        "temp_min_c": t_mins[i] if i < len(t_mins) else None,
                    })

                return {
                    "status": "success",
                    "timestamp": current.get("time", dt.datetime.now().isoformat()),
                    "temperature_2m": current.get("temperature_2m", 0.0),
                    "apparent_temperature": current.get("apparent_temperature", 0.0),
                    "relative_humidity_2m": current.get("relative_humidity_2m", 0.0),
                    "precipitation_mm": current.get("precipitation", 0.0),
                    "wind_speed_10m": current.get("wind_speed_10m", 0.0),
                    "weather_desc": weather_desc,
                    "daily_forecast": daily_cards,
                    "source": "Open-Meteo Weather Forecast API",
                    "source_url": "https://open-meteo.com/en/docs",
                    "horizon_notice": "7-day forecast only. Not a 3-month projection."
                }
            elif resp.status_code == 429:
                time.sleep(2 * (attempt + 1))
        except Exception as e:
            last_exc = e
            time.sleep(1)

    return {
        "status": "error",
        "error_message": f"Could not retrieve weather forecast: {last_exc}",
        "timestamp": dt.datetime.now().isoformat(),
        "temperature_2m": None,
        "relative_humidity_2m": None,
        "precipitation_mm": 0.0,
        "weather_desc": "Data unavailable",
        "daily_forecast": []
    }

def fetch_recent_3month_rainfall(lat: float, lon: float, timeout: int = 25, max_retries: int = 3) -> Tuple[float, int, int]:
    """
    Fetches accumulated precipitation over the most recent complete 3 calendar months
    from the Open-Meteo historical archive API.
    Returns: (total_precipitation_mm, last_complete_month, last_complete_year)
    """
    ref_date = dt.date.today() - dt.timedelta(days=5)
    end_date = ref_date.replace(day=1) - dt.timedelta(days=1)
    start_date = (pd.Timestamp(end_date).replace(day=1) - pd.DateOffset(months=2)).date()

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "daily": "precipitation_sum",
        "timezone": "Asia/Kolkata"
    }

    for attempt in range(max_retries):
        try:
            resp = requests.get(OPEN_METEO_ARCHIVE_URL, params=params, timeout=timeout)
            if resp.status_code == 200:
                data = resp.json()
                daily_rain = data.get("daily", {}).get("precipitation_sum", [])
                valid_vals = [v for v in daily_rain if v is not None]
                total_mm = round(float(sum(valid_vals)), 1)
                return total_mm, end_date.month, end_date.year
            elif resp.status_code == 429:
                time.sleep(3 * (attempt + 1))
        except Exception:
            time.sleep(1)

    # Return safe fallback if network temporarily unavailable
    return 0.0, end_date.month, end_date.year
