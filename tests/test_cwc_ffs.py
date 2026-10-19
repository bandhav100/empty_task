"""Unit tests for Central Water Commission (CWC) Flood Forecast System (FFS) integration."""

import pytest
from utils.cwc_ffs import (
    CWC_FFS_PORTAL_URL,
    CWC_TELANGANA_STATIONS,
    DISTRICT_BASIN_MAP,
    get_cwc_stations_for_district,
    check_cwc_portal_status
)
from utils.districts import EXACT_33_DISTRICTS

def test_cwc_portal_url():
    """Verify that official CWC Flood Forecast System URL is configured."""
    assert CWC_FFS_PORTAL_URL == "https://ffs.india-water.gov.in/#/"

def test_all_33_districts_mapped_to_river_basins():
    """Verify that every single one of the 33 districts is mapped to Godavari or Krishna basin."""
    for d in EXACT_33_DISTRICTS:
        assert d in DISTRICT_BASIN_MAP
        basin = DISTRICT_BASIN_MAP[d]
        assert "Godavari" in basin or "Krishna" in basin

def test_cwc_telangana_stations():
    """Verify that key Telangana flood warning stations exist with threshold levels."""
    station_names = [s["station_name"] for s in CWC_TELANGANA_STATIONS]
    assert "Bhadrachalam" in station_names
    assert "Srisailam Dam" in station_names
    assert "Jurala Project (PJP)" in station_names
    assert "Nagarjuna Sagar" in station_names
    assert "Musi Anicut (Hyderabad)" in station_names

    # Check warning levels
    for s in CWC_TELANGANA_STATIONS:
        assert s["warning_level_m"] > 0
        assert s["danger_level_m"] >= s["warning_level_m"]
        assert s["hfl_m"] >= s["danger_level_m"]

def test_get_cwc_stations_for_district():
    # Bhadradri Kothagudem should return Bhadrachalam
    kothagudem_stations = get_cwc_stations_for_district("Bhadradri Kothagudem")
    assert any(s["station_name"] == "Bhadrachalam" for s in kothagudem_stations)

    # Hyderabad should return Musi
    hyd_stations = get_cwc_stations_for_district("Hyderabad")
    assert any("Musi" in s["station_name"] for s in hyd_stations)

def test_check_cwc_portal_status():
    status = check_cwc_portal_status()
    assert "portal_name" in status
    assert status["portal_url"] == CWC_FFS_PORTAL_URL
    assert "Ministry of Jal Shakti" in status["authority"]
