"""Tests verifying Plotly Choropleth map rendering under complete and missing risk conditions."""

import pytest
from utils.data_loader import load_telangana_geojson
from utils.map_renderer import render_telangana_interactive_map

def test_map_renders_with_complete_risk_data():
    geo = load_telangana_geojson()
    district_risks = {"Hyderabad": 2, "Warangal": 1, "Adilabad": 0}
    fig = render_telangana_interactive_map(geo, "Hyderabad", district_risks=district_risks, lang="en")
    assert fig is not None
    assert len(fig.data) >= 2  # Choropleth trace + selected marker trace

def test_map_renders_with_missing_risk_values():
    """Requirement 4: Verify the map gracefully renders even when risk values are missing/None."""
    geo = load_telangana_geojson()
    
    # Test case 1: None passed for district_risks
    fig_none = render_telangana_interactive_map(geo, "Nalgonda", district_risks=None, lang="en")
    assert fig_none is not None
    assert len(fig_none.data) >= 2

    # Test case 2: Empty dictionary passed
    fig_empty = render_telangana_interactive_map(geo, "Khammam", district_risks={}, lang="te")
    assert fig_empty is not None
    assert len(fig_empty.data) >= 2
