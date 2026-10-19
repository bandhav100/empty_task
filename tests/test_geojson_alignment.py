"""Tests verifying GeoJSON boundary integrity and 33-district alignment."""

import json
from pathlib import Path
import pytest
from shapely.geometry import shape
from utils.districts import EXACT_33_DISTRICTS, get_internal_id
from utils.data_loader import load_telangana_geojson

def test_geojson_asset_exists_and_loads():
    geo = load_telangana_geojson()
    assert geo is not None
    assert "features" in geo
    assert len(geo["features"]) == 33

def test_geojson_district_names_match_registry():
    """Requirement 3: GeoJSON district names and IDs strictly match the district registry."""
    geo = load_telangana_geojson()
    geo_names = [f["properties"].get("district") for f in geo["features"]]
    geo_ids = [f.get("id") for f in geo["features"]]

    assert sorted(geo_names) == sorted(EXACT_33_DISTRICTS)
    
    expected_ids = [get_internal_id(d) for d in EXACT_33_DISTRICTS]
    assert sorted(geo_ids) == sorted(expected_ids)

def test_all_geojson_geometries_are_valid():
    """Verify that all 33 district boundary geometries are topologically valid."""
    geo = load_telangana_geojson()
    for feat in geo["features"]:
        name = feat["properties"]["district"]
        geom = shape(feat["geometry"])
        assert geom.is_valid, f"Geometry for {name} is topologically invalid"
        assert geom.area > 0.0, f"Geometry area for {name} is zero"
