"""Unit tests for model inference, schema validation, and prediction utilities."""

import pytest
import pandas as pd
from utils.data_loader import load_model_bundle, load_metrics
from utils.prediction import predict_water_stress, verify_feature_schema, load_pipeline_metadata

def test_load_model_bundle():
    bundle = load_model_bundle()
    assert "model" in bundle
    assert "features" in bundle
    assert len(bundle["features"]) == 15
    assert "oni_now" in bundle["features"]
    assert "normal_rain3" in bundle["features"]

def test_schema_verification_detects_missing_features():
    bundle = load_model_bundle()
    features = bundle["features"]

    # Incomplete dataframe (missing oni_delta)
    bad_df = pd.DataFrame([{f: 1.0 for f in features if f != "oni_delta"}])
    with pytest.raises(ValueError) as exc:
        verify_feature_schema(bad_df, features)
    assert "oni_delta" in str(exc.value)

def test_prediction_output_format():
    bundle = load_model_bundle()
    model = bundle["model"]
    features = bundle["features"]

    sample_dict = {
        "rain1": 25.0,
        "rain3": 110.0,
        "rain6": 280.0,
        "rain12": 650.0,
        "normal_rain3": 140.0,
        "recent_deficit": 0.214,
        "recent_ratio": 0.786,
        "msin": 0.5,
        "mcos": 0.866,
        "season": 3,
        "lat": 17.385,
        "lon": 78.487,
        "oni_now": 0.8,
        "oni_prev_3m": 0.4,
        "oni_delta": 0.4
    }
    sample_df = pd.DataFrame([sample_dict])[features]

    res = predict_water_stress(model, sample_df, expected_features=features)
    assert res["predicted_class"] in [0, 1, 2]
    assert "prob_high" in res
    assert "prob_medium" in res
    assert "prob_low" in res
    assert "uncertainty_level" in res
    assert 0.0 <= res["prob_high"] <= 1.0
    assert abs((res["prob_low"] + res["prob_medium"] + res["prob_high"]) - 1.0) < 1e-4

def test_load_pipeline_metadata():
    meta = load_pipeline_metadata()
    assert "model_version" in meta
    assert "macro_f1_difference" in meta
    assert meta["macro_f1_difference"] > 0.0
    assert meta["metrics_with_oni"]["macro_f1"] > meta["metrics_without_oni"]["macro_f1"]
    assert "confusion_matrix" in meta["metrics_with_oni"]
    assert "known_limitations" in meta

def test_load_model_metadata_and_normals():
    from utils.data_loader import load_model_metadata, load_clim_normals
    meta = load_model_metadata()
    assert meta["model_version"] == "v2.0.0-real-ml"
    assert meta["test_samples_count"] == 2574
    assert meta["train_samples_count"] == 5478

    normals = load_clim_normals()
    assert len(normals) >= 33
    assert "Hyderabad" in normals
    assert len(normals["Hyderabad"]) == 12

