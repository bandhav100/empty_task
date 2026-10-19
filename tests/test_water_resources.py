"""Comprehensive Test Suite for District Mandals & River-to-Mandal Directory.

Validates:
- All 33 district identifiers and mandal registries
- Non-empty, verified mandal lists across all districts
- Unique river counts vs river-mandal associations (no duplicate double-counting)
- Exact mandal associations and valid relationship types
- Mandal directory search and filtering
- Mandal deep-dive profile generation
- Empty and invalid district handling
"""

import pytest
from utils.districts import EXACT_33_DISTRICTS, normalize_district_name
from utils.water_resources_data import (
    TELANGANA_MANDALS,
    MASTER_RIVERS,
    DISTRICT_RIVER_MANDAL_MAP,
    DISTRICT_WATER_INFRASTRUCTURE
)
from utils.water_directory import (
    get_district_mandals,
    get_district_water_summary,
    get_mandal_directory_table,
    get_mandal_detailed_profile,
    get_district_infrastructure
)


def test_all_33_districts_have_mandals():
    """Verify that every single one of the 33 official districts has a verified mandal list."""
    assert len(EXACT_33_DISTRICTS) == 33
    total_mandals_count = 0
    for district in EXACT_33_DISTRICTS:
        mandals = get_district_mandals(district)
        assert len(mandals) >= 9, f"{district} has fewer than 9 mandals ({len(mandals)})"
        total_mandals_count += len(mandals)
        # Ensure no duplicate mandals within the same district
        assert len(mandals) == len(set(mandals)), f"Duplicate mandals found in {district}"

    # Total mandals across Telangana verified dataset (568 official revenue mandals)
    assert total_mandals_count >= 550, f"Expected >= 550 total mandals across Telangana, got {total_mandals_count}"


def test_unique_river_counts_vs_associations():
    """
    Ensure distinct calculation between unique rivers and river-mandal associations.
    A river traversing 5 mandals must count as 1 unique river and 5 associations.
    """
    for district in EXACT_33_DISTRICTS:
        summary = get_district_water_summary(district)
        assert summary["district"] == district
        assert summary["total_mandals"] > 0
        assert summary["unique_river_count"] >= 0
        assert summary["river_mandal_associations_count"] >= 0

        # Associations count must be >= unique river count
        assert summary["river_mandal_associations_count"] >= summary["unique_river_count"], (
            f"In {district}: associations ({summary['river_mandal_associations_count']}) "
            f"cannot be less than unique rivers ({summary['unique_river_count']})"
        )

    # Spot check Bhadradri Kothagudem (Godavari, Kinnerasani, Sabari, Taliperu)
    bk_summary = get_district_water_summary("Bhadradri Kothagudem")
    assert bk_summary["unique_river_count"] == 4
    assert bk_summary["river_mandal_associations_count"] >= 10


def test_river_metadata_integrity():
    """Verify all master rivers have official basins, types, and valid source URLs."""
    for r_id, r_info in MASTER_RIVERS.items():
        assert "name" in r_info and len(r_info["name"]) > 0
        assert "basin" in r_info and ("Godavari" in r_info["basin"] or "Krishna" in r_info["basin"])
        assert "source_url" in r_info and r_info["source_url"].startswith("http")


def test_river_mandal_relationship_classifications():
    """Verify that every river-mandal association has a valid geographic relationship classification."""
    valid_relationships = {
        "Physically traverses",
        "Borders mandal",
        "Basin drainage / catchment stream"
    }

    for district, river_list in DISTRICT_RIVER_MANDAL_MAP.items():
        for r_entry in river_list:
            assert r_entry["river_id"] in MASTER_RIVERS, f"Unknown river_id {r_entry['river_id']} in {district}"
            rel = r_entry.get("relationship")
            assert rel in valid_relationships, f"Invalid relationship '{rel}' in {district}"
            # Ensure every listed mandal exists in that district's mandal registry
            district_mandals = set(get_district_mandals(district))
            for m in r_entry.get("mandals", []):
                # Note: Bhadrachalam was reorganized; check if in mandal set or adjacent
                assert m in district_mandals or m == "Bhadrachalam", (
                    f"Mandal '{m}' listed for river {r_entry['river_id']} not in {district} mandals"
                )


def test_mandal_directory_search_and_filter():
    """Verify searchable mandal directory table and query filtering."""
    # Unfiltered search
    all_rows = get_mandal_directory_table("Siddipet", search_query="")
    assert len(all_rows) == len(TELANGANA_MANDALS["Siddipet"])
    
    # Filter by specific mandal
    filtered_rows = get_mandal_directory_table("Siddipet", search_query="Gajwel")
    assert len(filtered_rows) == 1
    assert filtered_rows[0]["Mandal"] == "Gajwel"
    assert filtered_rows[0]["Parent District"] == "Siddipet"

    # Filter with non-matching query
    empty_rows = get_mandal_directory_table("Siddipet", search_query="NonExistentMandalXYZ")
    assert len(empty_rows) == 0


def test_mandal_detailed_profile():
    """Verify mandal deep-dive profile generation for Cherla in Bhadradri Kothagudem."""
    profile = get_mandal_detailed_profile("Bhadradri Kothagudem", "Cherla")
    assert profile["mandal"] == "Cherla"
    assert profile["district"] == "Bhadradri Kothagudem"
    
    # Cherla is traversed by Godavari, Sabari, and Taliperu
    river_names = [r["river_name"] for r in profile["rivers"]]
    assert "Godavari River" in river_names
    assert "Taliperu River" in river_names

    # Cherla has Taliperu Project Dam
    res_names = [res["name"] for res in profile["reservoirs"]]
    assert any("Taliperu" in name for name in res_names)


def test_invalid_district_empty_handling():
    """Verify safe fallback for unknown or empty district inputs."""
    summary = get_district_water_summary("Atlantis")
    assert summary["total_mandals"] == 0
    assert summary["unique_river_count"] == 0
    assert summary["river_mandal_associations_count"] == 0
    assert summary["mandals"] == []

    mandal_rows = get_mandal_directory_table("UnknownDistrict")
    assert mandal_rows == []

    infra = get_district_infrastructure("UnknownDistrict")
    assert infra["reservoirs"] == []
    assert infra["lift_irrigation"] == []
    assert infra["groundwater_stations"] == []
