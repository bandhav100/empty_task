"""Unit tests for citizen recommendations and El Niño precautions."""

import pytest
from utils.recommendations import (
    CITIZEN_WATER_RECOMMENDATIONS,
    get_water_recommendations,
    EL_NINO_PRECAUTIONS,
    get_el_nino_precautions
)


def test_water_recommendations_levels():
    """Verify water recommendations exist for all 3 risk levels (0, 1, 2) across all languages."""
    for level in (0, 1, 2):
        for lang in ("en", "te", "hi"):
            recs = get_water_recommendations(level, lang=lang)
            assert isinstance(recs, list)
            assert len(recs) >= 3
            for r in recs:
                assert isinstance(r, str) and len(r.strip()) > 10


def test_water_recommendations_fallback():
    """Verify fallback to level 0 and English if invalid args passed."""
    recs = get_water_recommendations(999, lang="invalid_lang")
    assert isinstance(recs, list)
    assert len(recs) >= 3


def test_el_nino_precautions_structure():
    """Verify all 5 El Niño precaution domains are structured with required fields."""
    expected_domains = {"agriculture", "groundwater", "heatwave", "livestock", "community"}
    found_domains = {cat["id"] for cat in EL_NINO_PRECAUTIONS}
    assert expected_domains == found_domains

    for cat in EL_NINO_PRECAUTIONS:
        assert "icon" in cat and len(cat["icon"]) > 0
        assert "color" in cat and cat["color"].startswith("#")
        assert "title" in cat
        assert set(cat["title"].keys()) >= {"en", "te", "hi"}
        assert "precautions" in cat
        assert set(cat["precautions"].keys()) >= {"en", "te", "hi"}

        for lang in ("en", "te", "hi"):
            pts = cat["precautions"][lang]
            assert isinstance(pts, list)
            assert len(pts) >= 4  # At least 4-5 actionable measures per domain
            for pt in pts:
                assert isinstance(pt, str) and len(pt.strip()) > 15


def test_get_el_nino_precautions_accessor():
    """Test get_el_nino_precautions returns properly localized lists."""
    for lang in ("en", "te", "hi"):
        cats = get_el_nino_precautions(lang=lang)
        assert len(cats) == 5
        for cat in cats:
            assert "id" in cat
            assert "icon" in cat
            assert "color" in cat
            assert "title" in cat and isinstance(cat["title"], str)
            assert "precautions" in cat and isinstance(cat["precautions"], list)
            assert len(cat["precautions"]) >= 4


def test_get_el_nino_precautions_invalid_lang_fallback():
    """Test invalid language fallback defaults to English."""
    cats = get_el_nino_precautions(lang="fr")
    assert len(cats) == 5
    # Should fallback to English titles
    assert cats[0]["title"] == "Farming & Agriculture Safeguards"
