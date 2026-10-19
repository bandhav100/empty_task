"""Unit tests verifying district registry and canonical alias mappings."""

import pytest
from utils.districts import (
    EXACT_33_DISTRICTS,
    DISTRICTS,
    DISTRICT_TELUGU,
    normalize_district_name,
    get_internal_id,
    validate_district_name,
    get_coords
)

REQUIRED_33_DISTRICTS = [
    "Adilabad", "Bhadradri Kothagudem", "Hanumakonda", "Hyderabad", "Jagtial", "Jangaon",
    "Jayashankar Bhupalpally", "Jogulamba Gadwal", "Kamareddy", "Karimnagar", "Khammam",
    "Kumuram Bheem", "Mahabubabad", "Mahabubnagar", "Mancherial", "Medak", "Medchal-Malkajgiri",
    "Mulugu", "Nagarkurnool", "Nalgonda", "Narayanpet", "Nirmal", "Nizamabad", "Peddapalli",
    "Rajanna Sircilla", "Rangareddy", "Sangareddy", "Siddipet", "Suryapet", "Vikarabad",
    "Wanaparthy", "Warangal", "Yadadri Bhuvanagiri"
]

def test_exact_33_unique_districts():
    """Requirement 1: Verify exactly 33 unique official districts."""
    assert len(EXACT_33_DISTRICTS) == 33
    assert len(set(EXACT_33_DISTRICTS)) == 33
    assert sorted(EXACT_33_DISTRICTS) == sorted(REQUIRED_33_DISTRICTS)

def test_every_required_district_maps_correctly():
    """Requirement 2: Every required district maps to itself and has valid coordinates."""
    for district in REQUIRED_33_DISTRICTS:
        norm = normalize_district_name(district)
        assert norm == district
        assert validate_district_name(district) is True
        lat, lon = get_coords(district)
        assert 15.5 <= lat <= 20.0
        assert 77.0 <= lon <= 81.8

def test_alias_and_telugu_mappings():
    """Test normalization of former names and Telugu transliterations."""
    assert normalize_district_name("Kumuram Bheem Asifabad") == "Kumuram Bheem"
    assert normalize_district_name("Komaram Bheem") == "Kumuram Bheem"
    assert normalize_district_name("Warangal Urban") == "Hanumakonda"
    assert normalize_district_name("Warangal Rural") == "Warangal"
    assert normalize_district_name("Ranga Reddy") == "Rangareddy"
    assert normalize_district_name("హైదరాబాద్") == "Hyderabad"
    assert normalize_district_name("కుమురం భీమ్") == "Kumuram Bheem"

def test_internal_ids_are_unique():
    ids = [get_internal_id(d) for d in EXACT_33_DISTRICTS]
    assert len(ids) == 33
    assert len(set(ids)) == 33
    for slug in ids:
        assert "_" in slug or slug.isalnum()

def test_hindi_mappings():
    """Test normalization of Hindi transliterations."""
    from utils.districts import DISTRICT_HINDI, format_district_name
    assert len(DISTRICT_HINDI) >= 33
    assert normalize_district_name("हैदराबाद") == "Hyderabad"
    assert normalize_district_name("हनुमकोंडा") == "Hanumakonda"
    assert normalize_district_name("कुमुरम भीम") == "Kumuram Bheem"
    assert format_district_name("Hyderabad", lang="hi") == "हैदराबाद"
    assert format_district_name("Hanumakonda", lang="hi") == "हनुमकोंडा"
    assert format_district_name("ALL", lang="hi") == "सभी जिले (राज्यव्यापी)"
