"""Unit tests for NOAA ONI parsing and ENSO classification."""

import pytest
import pandas as pd
from utils.climate_data import parse_oni, classify_enso_state, get_oni_at

SAMPLE_ONI_TEXT = """
SEAS  YR   TOTAL   ANOM
DJF 2023   26.85  -0.75
JFM 2023   27.20  -0.42
FMA 2023   27.75  -0.11
MAM 2023   28.32   0.24
AMJ 2023   28.80   0.58
MJJ 2023   29.02   0.89
JJA 2023   29.08   1.12
JAS 2023   29.11   1.35
ASO 2023   29.20   1.61
SON 2023   29.35   1.88
OND 2023   29.41   1.95
NDJ 2023   29.32   1.82
"""

def test_parse_oni():
    df = parse_oni(SAMPLE_ONI_TEXT)
    assert len(df) == 12
    assert "date" in df.columns
    assert "oni" in df.columns
    # Check AMJ (month 5): 0.58
    amj_row = df[df["date"].dt.month == 5]
    assert not amj_row.empty
    assert round(float(amj_row["oni"].iloc[0]), 2) == 0.58

def test_classify_enso_state():
    assert classify_enso_state(1.8)[0] == "strong_elnino"
    assert classify_enso_state(1.1)[0] == "moderate_elnino"
    assert classify_enso_state(0.6)[0] == "weak_elnino"
    assert classify_enso_state(0.1)[0] == "neutral"
    assert classify_enso_state(-0.8)[0] == "weak_lanina"
    assert classify_enso_state(-1.6)[0] == "strong_lanina"

def test_get_oni_at():
    df = parse_oni(SAMPLE_ONI_TEXT)
    series = df.set_index("date")["oni"]
    val = get_oni_at(series, pd.Timestamp("2023-05-15"))
    assert round(val, 2) == 0.58
