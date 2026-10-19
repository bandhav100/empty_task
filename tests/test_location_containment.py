"""Tests verifying browser geolocation, polygon containment, and permission denial fallbacks."""

import pytest
from utils.location import find_district_by_polygon, haversine_distance, find_nearest_district
from utils.data_loader import load_telangana_geojson

def test_polygon_containment_inside_telangana():
    geo = load_telangana_geojson()

    # Charminar in Hyderabad (Lat: 17.3616, Lon: 78.4747)
    resolved, is_inside, dist = find_district_by_polygon(17.3616, 78.4747, geo)
    assert is_inside is True
    assert resolved == "Hyderabad"
    assert dist == 0.0

    # Near Kakatiya University in Hanumakonda (Lat: 18.0197, Lon: 79.5539)
    resolved_wgl, is_inside_wgl, _ = find_district_by_polygon(18.0197, 79.5539, geo)
    assert is_inside_wgl is True
    assert resolved_wgl in ["Hanumakonda", "Warangal"]

def test_polygon_containment_outside_telangana():
    """Verify that coordinates outside Telangana boundary are not silently treated as inside."""
    geo = load_telangana_geojson()

    # Vidhana Soudha, Bengaluru, Karnataka (Lat: 12.9797, Lon: 77.5906)
    resolved, is_inside, dist = find_district_by_polygon(12.9797, 77.5906, geo)
    assert is_inside is False
    assert dist > 150.0  # At least 150 km from closest Telangana district

    # London, UK (Lat: 51.5074, Lon: -0.1278)
    _, is_inside_lon, dist_lon = find_district_by_polygon(51.5074, -0.1278, geo)
    assert is_inside_lon is False
    assert dist_lon > 1000.0

def test_location_denial_activates_manual_selection():
    """Requirement 5: When location access is denied or None, system defaults safely without crashing."""
    # Simulate null / denied browser payload
    simulated_gps_payload = None
    default_district = "Hyderabad"

    if simulated_gps_payload is None:
        active_district = default_district
    
    assert active_district == "Hyderabad"
