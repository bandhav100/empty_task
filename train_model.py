"""MASTER PROMPT 3 — Production Machine Learning Pipeline.
Estimates district-level 3-month rainfall-deficit risk (Low, Medium, High).
Performs chronological out-of-time evaluation comparing baseline vs El Niño-aware models.
"""

import json
import sys
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    accuracy_score,
    precision_score,
    recall_score
)

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils.districts import DISTRICTS, EXACT_33_DISTRICTS
from utils.climate_data import parse_oni

RANDOM_SEED = 42
MODEL_VERSION = "v2.0.0-real-ml"

def run_ml_pipeline():
    print("=" * 70)
    print("STARTING TELANGANA RAINFALL-DEFICIT ML TRAINING & EVALUATION PIPELINE")
    print("=" * 70)

    # 1. Load Data
    rain_path = Path("data/processed/rain_monthly.csv")
    oni_path = Path("data/raw/oni.txt")

    if not rain_path.exists() or not oni_path.exists():
        raise FileNotFoundError("Missing data files. Ensure rain_monthly.csv and oni.txt exist.")

    rain_df = pd.read_csv(rain_path, parse_dates=["date"]).sort_values(["district", "date"])
    with open(oni_path, "r", encoding="utf-8") as f:
        oni_df = parse_oni(f.read())

    # Build forward-filled monthly ONI series up to 2027
    idx = pd.date_range(oni_df["date"].min(), "2027-12-01", freq="MS")
    oni_series = oni_df.set_index("date")["oni"].reindex(idx).ffill()

    print(f"Loaded {len(rain_df)} monthly rainfall records across {rain_df['district'].nunique()} districts.")
    print(f"Date range: {rain_df['date'].min().date()} to {rain_df['date'].max().date()}")

    # 2. Historical Lag Features (strict backward-looking from prediction date t)
    rain_df["rain1"] = rain_df["rain"]
    rain_df["rain3"] = rain_df.groupby("district")["rain"].transform(lambda s: s.rolling(3, min_periods=3).sum())
    rain_df["rain6"] = rain_df.groupby("district")["rain"].transform(lambda s: s.rolling(6, min_periods=6).sum())
    rain_df["rain12"] = rain_df.groupby("district")["rain"].transform(lambda s: s.rolling(12, min_periods=12).sum())
    rain_df["month"] = rain_df["date"].dt.month

    # Season indicator (1: Winter, 2: Pre-Monsoon, 3: SW Monsoon, 4: Post-Monsoon)
    def get_season(m: int) -> int:
        if m in [1, 2]:
            return 1
        elif m in [3, 4, 5]:
            return 2
        elif m in [6, 7, 8, 9]:
            return 3
        else:
            return 4

    rain_df["season"] = rain_df["month"].map(get_season)

    # Cyclical trigonometric encoding of month
    rain_df["msin"] = np.sin(2 * np.pi * rain_df["month"] / 12)
    rain_df["mcos"] = np.cos(2 * np.pi * rain_df["month"] / 12)

    # Geographic coordinates (centroid)
    rain_df["lat"] = rain_df["district"].map(lambda d: DISTRICTS[d][0])
    rain_df["lon"] = rain_df["district"].map(lambda d: DISTRICTS[d][1])

    # ENSO Oceanic Niño Index (strictly as of prediction date t)
    rain_df["oni_now"] = rain_df["date"].map(oni_series)
    rain_df["oni_prev_3m"] = (rain_df["date"] - pd.DateOffset(months=3)).map(oni_series)
    rain_df["oni_delta"] = rain_df["oni_now"] - rain_df["oni_prev_3m"]

    # Target window: rainfall over the upcoming 3 months (shift -3)
    rain_df["rain3_future"] = rain_df.groupby("district")["rain3"].shift(-3)
    rain_df["target_month"] = rain_df.groupby("district")["month"].shift(-3)

    # 3. Chronological Anti-Leakage Split
    # Training: 2005 to 2019 (embargo after 2019-09-01 so 3-month target window does not overlap into 2020)
    # Test: 2020-01-01 to 2026-06-01
    train_mask = (rain_df["date"] < "2019-10-01") & rain_df["rain12"].notna() & rain_df["rain3_future"].notna()
    test_mask = (rain_df["date"] >= "2020-01-01") & (rain_df["date"] <= "2026-06-01") & rain_df["rain12"].notna() & rain_df["rain3_future"].notna()

    # 4. Seasonal Normals (STRICTLY FROM TRAINING SET)
    train_only = rain_df[train_mask]
    seasonal_normals = train_only.groupby(["district", "month"])["rain3"].mean().rename("normal_rain3")
    target_normals = train_only.groupby(["district", "target_month"])["rain3_future"].mean().rename("normal_future_rain3")

    # Save climatological normals dictionary for inference lookups
    clim_normals_dict = {}
    for (d, m), val in seasonal_normals.items():
        clim_normals_dict.setdefault(d, {})[str(m)] = round(float(val), 2)
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    with open("data/processed/clim_normals.json", "w", encoding="utf-8") as f:
        json.dump(clim_normals_dict, f, indent=2)

    # Merge normals back into dataset
    rain_df = rain_df.merge(seasonal_normals, on=["district", "month"], how="left")
    rain_df = rain_df.merge(target_normals, on=["district", "target_month"], how="left")

    # Past deficit and ratio relative to training normal
    rain_df["recent_deficit"] = (rain_df["normal_rain3"] - rain_df["rain3"]) / rain_df["normal_rain3"].clip(lower=5.0)
    rain_df["recent_ratio"] = rain_df["rain3"] / rain_df["normal_rain3"].clip(lower=5.0)

    # Target future deficit: percentage shortfall relative to training normal
    rain_df["future_deficit"] = (rain_df["normal_future_rain3"] - rain_df["rain3_future"]) / rain_df["normal_future_rain3"].clip(lower=5.0)

    # Target class labeling based on proposed thresholds:
    # 0: Low Risk (< 10% deficit)
    # 1: Medium Risk (10% to < 25% deficit)
    # 2: High Risk (>= 25% deficit)
    def to_deficit_class(deficit_fraction: float) -> int:
        if deficit_fraction >= 0.25:
            return 2  # High deficit (>= 25%)
        elif deficit_fraction >= 0.10:
            return 1  # Medium deficit (10% to 25%)
        else:
            return 0  # Low deficit (< 10%)

    rain_df["y"] = rain_df["future_deficit"].map(to_deficit_class)

    # Define Feature Sets
    FEATURES_A = [
        "rain1", "rain3", "rain6", "rain12", "normal_rain3",
        "recent_deficit", "recent_ratio", "msin", "mcos", "season", "lat", "lon"
    ]
    FEATURES_B = FEATURES_A + ["oni_now", "oni_prev_3m", "oni_delta"]

    train_data = rain_df[train_mask].copy()
    test_data = rain_df[test_mask].copy()

    print(f"\nTraining set size: {len(train_data)} observations (2005 to Sep 2019)")
    print(f"Test set size:     {len(test_data)} observations (Jan 2020 to Jun 2026)")
    print("\nTest Class Distribution:")
    test_dist = test_data["y"].value_counts(normalize=True).to_dict()
    test_counts = test_data["y"].value_counts().to_dict()
    for c, name in [(0, "Low (<10% deficit)"), (1, "Medium (10-25% deficit)"), (2, "High (>=25% deficit)")]:
        print(f"  Class {c} ({name:25s}): {test_counts.get(c, 0):4d} ({test_dist.get(c, 0):.1%})")

    # 5. Train Model A (Baseline: Without ONI)
    rf_a = RandomForestClassifier(
        n_estimators=300,
        max_depth=8,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=RANDOM_SEED,
        n_jobs=-1
    )
    rf_a.fit(train_data[FEATURES_A], train_data["y"])
    pred_a = rf_a.predict(test_data[FEATURES_A])

    # 6. Train Model B (El Niño-Aware: With ONI)
    rf_b = RandomForestClassifier(
        n_estimators=300,
        max_depth=8,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=RANDOM_SEED,
        n_jobs=-1
    )
    rf_b.fit(train_data[FEATURES_B], train_data["y"])
    pred_b = rf_b.predict(test_data[FEATURES_B])

    # 7. Evaluate Metrics
    macro_f1_a = float(f1_score(test_data["y"], pred_a, average="macro"))
    macro_f1_b = float(f1_score(test_data["y"], pred_b, average="macro"))
    acc_a = float(accuracy_score(test_data["y"], pred_a))
    acc_b = float(accuracy_score(test_data["y"], pred_b))
    diff_f1 = macro_f1_b - macro_f1_a

    cm_a = confusion_matrix(test_data["y"], pred_a).tolist()
    cm_b = confusion_matrix(test_data["y"], pred_b).tolist()

    # Per-class metrics
    class_names = ["Low", "Medium", "High"]
    per_class_a = {}
    per_class_b = {}
    for c_idx, c_name in enumerate(class_names):
        per_class_a[c_name] = {
            "precision": round(float(precision_score(test_data["y"], pred_a, labels=[c_idx], average="macro", zero_division=0)), 4),
            "recall": round(float(recall_score(test_data["y"], pred_a, labels=[c_idx], average="macro", zero_division=0)), 4),
            "f1": round(float(f1_score(test_data["y"], pred_a, labels=[c_idx], average="macro", zero_division=0)), 4)
        }
        per_class_b[c_name] = {
            "precision": round(float(precision_score(test_data["y"], pred_b, labels=[c_idx], average="macro", zero_division=0)), 4),
            "recall": round(float(recall_score(test_data["y"], pred_b, labels=[c_idx], average="macro", zero_division=0)), 4),
            "f1": round(float(f1_score(test_data["y"], pred_b, labels=[c_idx], average="macro", zero_division=0)), 4)
        }

    # Feature Importance
    feat_importances_b = {
        feat: round(float(imp), 4)
        for feat, imp in sorted(zip(FEATURES_B, rf_b.feature_importances_), key=lambda x: x[1], reverse=True)
    }

    # 8. Print Official Model Summary Report
    print("\n" + "=" * 70)
    print("FINAL MACHINE LEARNING EVALUATION REPORT")
    print("=" * 70)
    print(f"Model without ONI — actual macro-F1: {macro_f1_a:.4f} (Accuracy: {acc_a:.4f})")
    print(f"Model with ONI    — actual macro-F1: {macro_f1_b:.4f} (Accuracy: {acc_b:.4f})")
    print(f"Macro-F1 difference — actual calculated value: {diff_f1:+.4f} ({diff_f1/macro_f1_a:+.1%})")
    print(f"Test period: 2020-01-01 to 2026-06-01")
    print(f"Number of test examples: {len(test_data)}")
    print("\nPer-class results (Model A - Without ONI):")
    print(f"  {'Class':<8} {'Precision':<10} {'Recall':<10} {'F1-Score':<10}")
    for name, m in per_class_a.items():
        print(f"  {name:<8} {m['precision']:<10.4f} {m['recall']:<10.4f} {m['f1']:<10.4f}")

    print("\nPer-class results (Model B - With ONI):")
    print(f"  {'Class':<8} {'Precision':<10} {'Recall':<10} {'F1-Score':<10}")
    for name, m in per_class_b.items():
        print(f"  {name:<8} {m['precision']:<10.4f} {m['recall']:<10.4f} {m['f1']:<10.4f}")

    print("\nConfusion Matrix (Model A - Without ONI):")
    print("   Pred Low  Pred Med  Pred High")
    for r_idx, row in enumerate(cm_a):
        print(f"Act {class_names[r_idx]:<4} {row[0]:6d}    {row[1]:6d}     {row[2]:6d}")

    print("\nConfusion Matrix (Model B - With ONI):")
    print("   Pred Low  Pred Med  Pred High")
    for r_idx, row in enumerate(cm_b):
        print(f"Act {class_names[r_idx]:<4} {row[0]:6d}    {row[1]:6d}     {row[2]:6d}")

    print("\nTop Feature Importances (Model B - Gini MDI):")
    for f_name, f_val in list(feat_importances_b.items())[:8]:
        print(f"  {f_name:18s}: {f_val:.4f}")

    print("\nKnown Limitations:")
    print("  1. Meteorological proxy: Rainfall deficit is not equal to municipal pipe pressure or groundwater levels.")
    print("  2. Historical ONI is past climate state, not a 3-month future forecast of ENSO.")
    print("  3. Non-causal: Tree splits demonstrate statistical association, not mechanistic hydrological proof.")
    print("=" * 70)

    # 9. Train Production Model on Full Historical Data
    full_mask = rain_df["rain12"].notna() & rain_df["rain3_future"].notna()
    full_data = rain_df[full_mask].copy()

    production_model_b = RandomForestClassifier(
        n_estimators=300,
        max_depth=8,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=RANDOM_SEED,
        n_jobs=-1
    )
    production_model_b.fit(full_data[FEATURES_B], full_data["y"])

    production_model_a = RandomForestClassifier(
        n_estimators=300,
        max_depth=8,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=RANDOM_SEED,
        n_jobs=-1
    )
    production_model_a.fit(full_data[FEATURES_A], full_data["y"])

    # 10. Save Artifacts & Metadata
    Path("models").mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": production_model_b, "features": FEATURES_B}, "models/model_with_oni.pkl")
    joblib.dump({"model": production_model_a, "features": FEATURES_A}, "models/model_without_oni.pkl")
    joblib.dump({"model": production_model_b, "features": FEATURES_B}, "models/model.pkl")
    joblib.dump({"model": production_model_b, "features": FEATURES_B}, "model.pkl")

    metadata = {
        "model_version": MODEL_VERSION,
        "random_seed": RANDOM_SEED,
        "target_definition": "3-month forward rainfall deficit relative to district seasonal normal (Low: <10%, Medium: 10-25%, High: >=25%)",
        "training_period": "2005-01-01 to 2019-09-01 (embargoed before 2020)",
        "test_period": "2020-01-01 to 2026-06-01",
        "train_samples_count": len(train_data),
        "test_samples_count": len(test_data),
        "test_class_distribution": {
            "Low": test_counts.get(0, 0),
            "Medium": test_counts.get(1, 0),
            "High": test_counts.get(2, 0)
        },
        "features_without_oni": FEATURES_A,
        "features_with_oni": FEATURES_B,
        "metrics_without_oni": {
            "macro_f1": round(macro_f1_a, 4),
            "accuracy": round(acc_a, 4),
            "per_class": per_class_a,
            "confusion_matrix": cm_a
        },
        "metrics_with_oni": {
            "macro_f1": round(macro_f1_b, 4),
            "accuracy": round(acc_b, 4),
            "per_class": per_class_b,
            "confusion_matrix": cm_b
        },
        "macro_f1_difference": round(diff_f1, 4),
        "macro_f1_relative_gain_pct": round(diff_f1 / macro_f1_a * 100, 2),
        "feature_importances": feat_importances_b,
        "known_limitations": [
            "Meteorological rainfall deficit is a proxy for water stress, not a direct sensor of municipal piped supply or borewell drawdown.",
            "Historical ONI indicates oceanic conditions at the prediction date; it is not a 3-month forecast of future Pacific SST anomalies.",
            "Feature importance indicates split contribution in decision trees and does not constitute hydrological proof of causation."
        ]
    }

    with open("models/model_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    with open("models/metrics.json", "w", encoding="utf-8") as f:
        json.dump({
            "with_elnino": {"accuracy": round(acc_b, 3), "macro_f1": round(macro_f1_b, 3)},
            "without_elnino": {"accuracy": round(acc_a, 3), "macro_f1": round(macro_f1_a, 3)},
            "baseline_always_low": round(float((test_data['y'] == 0).mean()), 3),
            "test_period": "2020-01-01 to 2026-06-01 (trained on data before 2020)"
        }, f, indent=2)

    print("\nSaved models/model_with_oni.pkl, models/model_without_oni.pkl, models/model_metadata.json, and data/processed/clim_normals.json")

if __name__ == "__main__":
    run_ml_pipeline()
