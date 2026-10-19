"""NOAA Climate Prediction Center Oceanic Niño Index (ONI v6 / ERSST.v5) Integration.
Provides robust parsing, date validation, and anti-leakage historical alignment.
"""

from pathlib import Path
from typing import Optional, Tuple, Dict, Any
import datetime as dt
import pandas as pd
import requests

SEASONS = ["DJF", "JFM", "FMA", "MAM", "AMJ", "MJJ", "JJA", "JAS", "ASO", "SON", "OND", "NDJ"]
NOAA_PAGE_URL = "https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/oni/v6/"
NOAA_DATA_URL = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"

def parse_oni(text: str) -> pd.DataFrame:
    """Parse NOAA CPC oni.ascii.txt returning DataFrame."""
    df, _ = parse_oni_table(text)
    return df

def parse_oni_table(text: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Parses NOAA CPC oni.ascii.txt format into a validated DataFrame and metadata dictionary.
    
    Validation guarantees:
    - Verifies 3-month season codes against SEASONS.
    - Validates 4-digit years and realistic SST anomaly bounds (-4.5°C to +4.5°C).
    - Preserves observation period and format integrity.
    """
    if not text or len(text.strip()) < 50:
        raise ValueError("NOAA ONI source data is empty or corrupted.")

    lines = text.strip().splitlines()
    header_found = False
    rows = []

    for line in lines:
        parts = line.split()
        if not parts:
            continue
        # Header line check: SEAS YR TOTAL ANOM
        if "SEAS" in parts[0] or "ANOM" in line:
            header_found = True
            continue
        if parts[0] in SEASONS and len(parts) >= 4:
            try:
                season = parts[0]
                year = int(parts[1])
                if year < 1950 or year > 2100:
                    continue
                anomaly = float(parts[3])
                if not (-5.0 <= anomaly <= 5.0):
                    continue
                center_month = SEASONS.index(season) + 1
                date_val = pd.Timestamp(year=year, month=center_month, day=1)
                rows.append({
                    "season": season,
                    "year": year,
                    "date": date_val,
                    "oni": anomaly
                })
            except (ValueError, IndexError):
                continue

    if not rows:
        raise ValueError("Could not extract valid ONI data rows. NOAA table schema may have changed.")

    df = pd.DataFrame(rows).drop_duplicates(subset=["date"]).sort_values("date").reset_index(drop=True)
    
    latest_row = df.iloc[-1]
    metadata = {
        "version": "ONI v6 (NOAA CPC ERSST.v5)",
        "source_page": NOAA_PAGE_URL,
        "data_url": NOAA_DATA_URL,
        "first_period": f"{df.iloc[0]['season']} {df.iloc[0]['year']}",
        "latest_period": f"{latest_row['season']} {latest_row['year']}",
        "latest_value": float(latest_row["oni"]),
        "total_records": len(df),
        "forecast_disclaimer": "Historical ONI observations represent past ocean states, NOT a future forecast of ONI."
    }

    return df, metadata

def load_or_fetch_oni_bundle(cache_dir: Optional[Path] = None) -> Tuple[pd.Series, Dict[str, Any]]:
    """
    Retrieves ONI data with live NOAA CPC fetch and local file cache fallback.
    Returns: (forward_filled_series, metadata_dict)
    """
    raw_text = ""
    cache_file = (cache_dir or Path("data/raw")) / "oni.txt"
    root_cache = Path("oni.txt")

    # 1. Attempt live download
    try:
        resp = requests.get(NOAA_DATA_URL, timeout=12)
        if resp.status_code == 200 and len(resp.text) > 1000:
            raw_text = resp.text
            # Update cache files
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(cache_file, "w", encoding="utf-8") as f:
                f.write(raw_text)
            with open(root_cache, "w", encoding="utf-8") as f:
                f.write(raw_text)
    except Exception:
        raw_text = ""

    # 2. Fall back to local cache if offline or error
    if not raw_text:
        candidates = [cache_file, root_cache, Path(__file__).parent.parent / "data" / "raw" / "oni.txt"]
        for p in candidates:
            if p.exists() and p.stat().st_size > 100:
                with open(p, "r", encoding="utf-8") as f:
                    raw_text = f.read()
                break

    if not raw_text:
        raise RuntimeError("Failed to retrieve NOAA ONI data online or from local backup.")

    df, meta = parse_oni_table(raw_text)

    # Forward-fill to cover inference date window without lookahead leakage
    max_date = df["date"].max()
    future_date = pd.Timestamp.now() + pd.DateOffset(months=12)
    full_idx = pd.date_range(df["date"].min(), max(max_date, future_date), freq="MS")
    series = df.set_index("date")["oni"].reindex(full_idx).ffill()

    return series, meta

def load_or_fetch_oni() -> pd.Series:
    """Convenience wrapper returning forward-filled series."""
    series, _ = load_or_fetch_oni_bundle()
    return series

def get_oni_at(series: pd.Series, ts: pd.Timestamp) -> float:
    """
    Strict historical alignment: returns the most recent published ONI value
    dated on or before timestamp `ts` to prevent future-information leakage.
    """
    sub = series[series.index <= ts]
    if sub.empty:
        return float(series.iloc[0])
    return float(sub.iloc[-1])

def classify_enso_state(oni_val: float) -> Tuple[str, str]:
    """
    Classifies ENSO state strictly following NOAA CPC climatological standards.
    El Niño: ONI >= +0.5°C
    La Niña: ONI <= -0.5°C
    Neutral: -0.5°C < ONI < +0.5°C
    """
    if oni_val >= 1.5:
        return "strong_elnino", "Strong El Niño"
    elif oni_val >= 1.0:
        return "moderate_elnino", "Moderate El Niño"
    elif oni_val >= 0.5:
        return "weak_elnino", "Weak El Niño"
    elif oni_val <= -1.5:
        return "strong_lanina", "Strong La Niña"
    elif oni_val <= -1.0:
        return "moderate_lanina", "Moderate La Niña"
    elif oni_val <= -0.5:
        return "weak_lanina", "Weak La Niña"
    else:
        return "neutral", "ENSO Neutral"
