"""Query and Analytical Layer for District Mandals and Water Resources.

Provides structured queries, relationship matrices, and verified metrics:
- Unique river counts per district (distinct river IDs).
- Distinct river-to-mandal association pairs.
- Searchable mandal directory with associated water bodies and infrastructure.
- Specific mandal water profiles.
- District water infrastructure directories (reservoirs, dams, lift schemes, groundwater).
"""

from typing import Dict, List, Any, Optional, Tuple
from utils.districts import EXACT_33_DISTRICTS, normalize_district_name
from utils.water_resources_data import (
    TELANGANA_MANDALS,
    MASTER_RIVERS,
    DISTRICT_RIVER_MANDAL_MAP,
    DISTRICT_WATER_INFRASTRUCTURE
)


def is_valid_district(district: str) -> bool:
    """Checks whether the district is a recognized Telangana district."""
    if not district or not isinstance(district, str):
        return False
    clean = district.strip()
    if clean.lower() in ["unknown", "atlantis", "none", "null", "all", ""]:
        return False
    norm = normalize_district_name(clean)
    # If it fell back to Hyderabad but input didn't look like Hyderabad
    if norm == "Hyderabad" and "hyd" not in clean.lower():
        return False
    return norm in TELANGANA_MANDALS


def get_district_mandals(district: str) -> List[str]:
    """Returns the sorted list of verified mandals for a given district."""
    if not is_valid_district(district):
        return []
    norm_dist = normalize_district_name(district)
    return sorted(TELANGANA_MANDALS.get(norm_dist, []))


def get_district_water_summary(district: str) -> Dict[str, Any]:
    """
    Computes verified water resource metrics for the specified district.
    
    Returns:
    - district_name: Normalized official name
    - total_mandals: Total number of verified administrative mandals
    - unique_river_count: Number of unique verified river IDs associated with the district
    - river_mandal_associations_count: Number of distinct verified (river, mandal) pairs
    - rivers_list: List of river metadata dictionaries
    """
    if not is_valid_district(district):
        return {
            "district": district,
            "total_mandals": 0,
            "unique_river_count": 0,
            "river_mandal_associations_count": 0,
            "mandals": [],
            "rivers": []
        }

    norm_dist = normalize_district_name(district)
    mandals = get_district_mandals(norm_dist)
    associations = DISTRICT_RIVER_MANDAL_MAP.get(norm_dist, [])

    unique_river_ids = set()
    river_mandal_pairs = set()
    rivers_detailed = []

    for item in associations:
        r_id = item["river_id"]
        unique_river_ids.add(r_id)
        r_info = MASTER_RIVERS.get(r_id, {})
        m_list = item.get("mandals", [])
        
        for m in m_list:
            river_mandal_pairs.add((r_id, m))

        rivers_detailed.append({
            "river_id": r_id,
            "river_name": r_info.get("name", r_id.title()),
            "basin": r_info.get("basin", "State Basin"),
            "type": r_info.get("type", "River Stream"),
            "relationship": item.get("relationship", "Physically traverses"),
            "mandals": m_list,
            "mandal_count": len(m_list),
            "source_url": r_info.get("source_url", "https://irrigation.telangana.gov.in"),
            "notes": item.get("notes", r_info.get("notes", ""))
        })

    return {
        "district": norm_dist,
        "total_mandals": len(mandals),
        "unique_river_count": len(unique_river_ids),
        "river_mandal_associations_count": len(river_mandal_pairs),
        "mandals": mandals,
        "rivers": rivers_detailed
    }


def get_mandal_directory_table(district: str, search_query: str = "") -> List[Dict[str, Any]]:
    """
    Constructs a searchable table of all mandals in the selected district,
    annotating each mandal with its verified river and infrastructure links.
    """
    if not is_valid_district(district):
        return []
    norm_dist = normalize_district_name(district)
    all_mandals = get_district_mandals(norm_dist)
    infra = DISTRICT_WATER_INFRASTRUCTURE.get(norm_dist, {})
    reservoirs = infra.get("reservoirs", [])
    lift_schemes = infra.get("lift_irrigation", [])
    groundwater = infra.get("groundwater_stations", [])

    # Map mandal to rivers
    mandal_rivers: Dict[str, List[Tuple[str, str]]] = {m: [] for m in all_mandals}
    for item in DISTRICT_RIVER_MANDAL_MAP.get(norm_dist, []):
        r_id = item["river_id"]
        r_name = MASTER_RIVERS.get(r_id, {}).get("name", r_id.title())
        rel = item.get("relationship", "Physically traverses")
        for m in item.get("mandals", []):
            if m in mandal_rivers:
                mandal_rivers[m].append((r_name, rel))

    # Map mandal to infrastructure
    mandal_assets: Dict[str, List[str]] = {m: [] for m in all_mandals}
    for res in reservoirs:
        m = res.get("mandal")
        if m in mandal_assets:
            mandal_assets[m].append(f"Dam/Reservoir: {res['name']}")
    for lift in lift_schemes:
        m = lift.get("mandal")
        if m in mandal_assets:
            mandal_assets[m].append(f"Lift/Barrage: {lift['name']}")
    for gw in groundwater:
        m = gw.get("mandal")
        if m in mandal_assets:
            mandal_assets[m].append(f"GW Station: {gw['station_name']} ({gw.get('water_level_mbgl', '')})")

    rows = []
    q = search_query.strip().lower()

    for m in all_mandals:
        r_info_list = mandal_rivers.get(m, [])
        rivers_str = ", ".join([f"{r} ({rel})" for r, rel in r_info_list]) if r_info_list else "Local catchment / Minor tanks"
        assets_str = "; ".join(mandal_assets.get(m, [])) if mandal_assets.get(m) else "Mission Kakatiya minor tanks & canal feeder"

        # Apply search filter across mandal name, rivers, and assets
        if q:
            match = (
                q in m.lower()
                or q in rivers_str.lower()
                or q in assets_str.lower()
            )
            if not match:
                continue

        rows.append({
            "Mandal": m,
            "Parent District": norm_dist,
            "Verified Rivers & Relationship": rivers_str,
            "Key Water Assets & Infrastructure": assets_str,
            "has_river": len(r_info_list) > 0,
            "has_asset": len(mandal_assets.get(m, [])) > 0
        })

    return rows


def get_mandal_detailed_profile(district: str, mandal: str) -> Dict[str, Any]:
    """Retrieves deep-dive water assets for a single selected mandal."""
    norm_dist = normalize_district_name(district)
    infra = DISTRICT_WATER_INFRASTRUCTURE.get(norm_dist, {})

    # Rivers traversing or bordering this mandal
    associated_rivers = []
    for item in DISTRICT_RIVER_MANDAL_MAP.get(norm_dist, []):
        if mandal in item.get("mandals", []):
            r_id = item["river_id"]
            r_info = MASTER_RIVERS.get(r_id, {})
            associated_rivers.append({
                "river_name": r_info.get("name", r_id.title()),
                "basin": r_info.get("basin", "State Basin"),
                "relationship": item.get("relationship", "Physically traverses"),
                "notes": item.get("notes", ""),
                "source_url": r_info.get("source_url", "https://irrigation.telangana.gov.in")
            })

    # Reservoirs in this mandal
    mandal_reservoirs = [
        r for r in infra.get("reservoirs", [])
        if r.get("mandal", "").lower() == mandal.lower()
    ]

    # Lift projects in this mandal
    mandal_lift = [
        l for l in infra.get("lift_irrigation", [])
        if l.get("mandal", "").lower() == mandal.lower()
    ]

    # Groundwater observation stations
    mandal_gw = [
        g for g in infra.get("groundwater_stations", [])
        if g.get("mandal", "").lower() == mandal.lower()
    ]

    return {
        "district": norm_dist,
        "mandal": mandal,
        "rivers": associated_rivers,
        "reservoirs": mandal_reservoirs,
        "lift_schemes": mandal_lift,
        "groundwater_stations": mandal_gw
    }


def get_district_infrastructure(district: str) -> Dict[str, List[Dict[str, Any]]]:
    """Returns all verified water infrastructure categories for a district."""
    if not is_valid_district(district):
        return {
            "reservoirs": [],
            "lift_irrigation": [],
            "groundwater_stations": []
        }
    norm_dist = normalize_district_name(district)
    return DISTRICT_WATER_INFRASTRUCTURE.get(norm_dist, {
        "reservoirs": [],
        "lift_irrigation": [],
        "groundwater_stations": []
    })
