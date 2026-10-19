"""Cached loaders for machine learning models, climatology tables, and spatial assets."""

import json
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

def find_file(candidates: list[Path]) -> Optional[Path]:
    """Search a list of candidate paths and return the first existing file."""
    for p in candidates:
        if p.exists() and p.is_file():
            return p
    return None

def load_model_bundle() -> Dict[str, Any]:
    """
    Load the trained Random Forest model artifact.
    Looks in models/model.pkl, model.pkl, etc.
    """
    candidates = [
        BASE_DIR / "models" / "model.pkl",
        BASE_DIR / "model.pkl",
        Path("models/model.pkl"),
        Path("model.pkl")
    ]
    target = find_file(candidates)
    if not target:
        raise FileNotFoundError("Model file 'model.pkl' not found. Please run train_model.py first.")
    return joblib.load(target)

def load_clim_normals() -> Dict[str, Dict[str, float]]:
    """
    Load training-derived 3-month seasonal rainfall normals per district and month.
    Looks in data/processed/clim_normals.json, clim_normals.json, etc.
    """
    candidates = [
        BASE_DIR / "data" / "processed" / "clim_normals.json",
        BASE_DIR / "clim_normals.json",
        Path("data/processed/clim_normals.json"),
        Path("clim_normals.json")
    ]
    target = find_file(candidates)
    if not target:
        return {}
    with open(target, "r", encoding="utf-8") as f:
        return json.load(f)

def load_climatology() -> Dict[str, Dict[str, list[float]]]:
    """
    Load the district historical climatological distribution (sorted 3-month rainfall).
    Looks in data/processed/clim.json, clim.json, etc.
    """
    candidates = [
        BASE_DIR / "data" / "processed" / "clim.json",
        BASE_DIR / "clim.json",
        Path("data/processed/clim.json"),
        Path("clim.json")
    ]
    target = find_file(candidates)
    if not target:
        raise FileNotFoundError("Climatology file 'clim.json' not found. Please run train_model.py first.")
    with open(target, "r", encoding="utf-8") as f:
        return json.load(f)


def load_model_metadata() -> Dict[str, Any]:
    """
    Load comprehensive model metadata, evaluation metrics, and limitations.
    Looks in models/model_metadata.json, model_metadata.json, etc.
    """
    candidates = [
        BASE_DIR / "models" / "model_metadata.json",
        BASE_DIR / "model_metadata.json",
        Path("models/model_metadata.json"),
        Path("model_metadata.json")
    ]
    target = find_file(candidates)
    if not target:
        return {}
    with open(target, "r", encoding="utf-8") as f:
        return json.load(f)

def load_metrics() -> Dict[str, Any]:
    """
    Load model validation metrics comparing with/without El Niño.
    Looks in models/metrics.json or extracts from models/model_metadata.json.
    """
    candidates = [
        BASE_DIR / "models" / "metrics.json",
        BASE_DIR / "metrics.json",
        Path("models/metrics.json"),
        Path("metrics.json")
    ]
    target = find_file(candidates)
    if target:
        with open(target, "r", encoding="utf-8") as f:
            return json.load(f)
    meta = load_model_metadata()
    if meta:
        return {
            "with_elnino": meta.get("metrics_with_oni", {}),
            "without_elnino": meta.get("metrics_without_oni", {}),
            "baseline_always_low": 0.625,
            "test_period": meta.get("test_period", "")
        }
    return {
        "with_elnino": {"accuracy": 0.0, "macro_f1": 0.0},
        "without_elnino": {"accuracy": 0.0, "macro_f1": 0.0},
        "baseline_always_low": 0.0,
        "test_period": "Not yet trained"
    }


def load_rain_monthly_df() -> pd.DataFrame:
    """
    Load historical monthly precipitation dataset for all 33 districts.
    """
    candidates = [
        BASE_DIR / "data" / "processed" / "rain_monthly.csv",
        BASE_DIR / "rain_monthly.csv",
        Path("data/processed/rain_monthly.csv"),
        Path("rain_monthly.csv")
    ]
    target = find_file(candidates)
    if not target:
        return pd.DataFrame()
    return pd.read_csv(target)

def load_telangana_geojson() -> Optional[Dict[str, Any]]:
    """
    Load genuine Telangana 33 districts GeoJSON boundary map.
    Looks in assets/telangana_districts.geojson.
    """
    candidates = [
        BASE_DIR / "assets" / "telangana_districts.geojson",
        Path("assets/telangana_districts.geojson")
    ]
    target = find_file(candidates)
    if not target:
        return None
    with open(target, "r", encoding="utf-8") as f:
        return json.load(f)

