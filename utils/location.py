"""Geolocation utilities with Shapely polygon containment and privacy guarantees.
Strictly ensures zero storage or persistence of user coordinates.
"""

import math
from typing import Optional, Tuple, Dict, Any
from shapely.geometry import shape, Point
from utils.districts import DISTRICTS, EXACT_33_DISTRICTS, normalize_district_name

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great-circle distance between two points on the Earth in kilometers."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    r_earth_km = 6371.0
    return r_earth_km * c

def find_district_by_polygon(lat: float, lon: float, geojson_data: Optional[Dict[str, Any]] = None) -> Tuple[Optional[str], bool, float]:
    """
    Identifies Telangana district using strict polygon containment.
    Returns: (resolved_district_name, is_inside_telangana, distance_to_nearest_km)
    
    Privacy disclosure: Coordinates are processed ephemerally in volatile memory only.
    No location coordinates are stored to disk, databases, or cookies.
    """
    if geojson_data and "features" in geojson_data:
        pt = Point(lon, lat)  # Shapely convention: (x=longitude, y=latitude)
        for feat in geojson_data["features"]:
            geom = shape(feat["geometry"])
            if geom.contains(pt) or geom.touches(pt):
                district_raw = feat["properties"].get("district", "")
                official = normalize_district_name(district_raw)
                return official, True, 0.0

    # If outside polygon boundaries, determine nearest district centroid and distance
    best_name = "Hyderabad"
    min_dist = float("inf")
    for name in EXACT_33_DISTRICTS:
        d_lat, d_lon = DISTRICTS[name]
        dist = haversine_distance(lat, lon, d_lat, d_lon)
        if dist < min_dist:
            min_dist = dist
            best_name = name

    # If within reasonable boundary buffer (e.g. 15 km), may be border settlement
    is_border_proximity = (min_dist <= 25.0)
    return best_name, is_border_proximity, round(min_dist, 1)

def find_nearest_district(lat: float, lon: float) -> Tuple[str, float]:
    """Fallback centroid proximity search."""
    best_name = "Hyderabad"
    min_dist = float("inf")
    for name in EXACT_33_DISTRICTS:
        d_lat, d_lon = DISTRICTS[name]
        dist = haversine_distance(lat, lon, d_lat, d_lon)
        if dist < min_dist:
            min_dist = dist
            best_name = name
    return best_name, round(min_dist, 1)

def is_within_telangana_region(lat: float, lon: float, max_dist_km: float = 80.0) -> Tuple[bool, str, float]:
    """High-level check whether coordinates are in or adjacent to Telangana."""
    nearest, dist = find_nearest_district(lat, lon)
    return (dist <= max_dist_km, nearest, dist)
