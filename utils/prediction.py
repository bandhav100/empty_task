"""Random Forest inference pipeline, schema validation, and explainability.
Predicts 3-month rainfall-deficit risk categories with uncertainty assessment.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

RISK_LEVEL_METADATA = {
    0: {
        "level_code": "low",
        "name_en": "Low Deficit Risk",
        "name_te": "తక్కువ లోటు ప్రమాదం",
        "name_hi": "कम घाटा जोखिम",
        "color": "#2e7d32",   # Forest Green
        "bg_color": "#e8f5e9",
        "badge_en": "NORMAL / SURPLUS EXPECTED (<10% DEFICIT)",
        "badge_te": "సాధారణ / సమృద్ధిగా వర్షపాతం (<10% లోటు)",
        "badge_hi": "सामान्य / प्रचुर वर्षा की संभावना (<10% घाटा)",
        "summary_en": "Projected 3-month rainfall is within 10% of the district seasonal normal or higher. Normal municipal water supply conditions expected.",
        "summary_te": "రాబోయే 3 నెలల వర్షపాతం జిల్లా సాధారణ మట్టానికి 10% లోపు లేదా అంతకంటే ఎక్కువ ఉండే అవకాశం ఉంది.",
        "summary_hi": "अनुमानित 3-माह की वर्षा जिले के मौसमी सामान्य स्तर के 10% के भीतर या अधिक रहने की संभावना है। सामान्य जलापूर्ति की उम्मीद है।"
    },
    1: {
        "level_code": "medium",
        "name_en": "Medium Deficit Risk",
        "name_te": "మధ్యస్థ లోటు ప్రమాదం",
        "name_hi": "मध्यम घाटा जोखिम",
        "color": "#ef8f00",   # Warm Amber
        "bg_color": "#fff8e1",
        "badge_en": "MODERATE DEFICIT RISK (10% - 25% SHORTFALL)",
        "badge_te": "మధ్యస్థ లోటు ప్రమాదం (10% - 25% లోటు)",
        "badge_hi": "मध्यम घाटा जोखिम (10% - 25% कमी)",
        "summary_en": "Projected 3-month rainfall shows a 10% to 25% deficit below district seasonal normal. Prudent domestic water management advised.",
        "summary_te": "రాబోయే 3 నెలల్లో వర్షపాతం సాధారణం కంటే 10% నుండి 25% తక్కువగా నమోదయ్యే అవకాశం ఉంది. నీటిని పొదుపుగా వాడండి.",
        "summary_hi": "अनुमानित 3-माह की वर्षा में मौसमी सामान्य से 10% से 25% की कमी की संभावना है। पानी का संयमित उपयोग करने की सलाह दी जाती है।"
    },
    2: {
        "level_code": "high",
        "name_en": "High Deficit Risk",
        "name_te": "అధిక లోటు ప్రమాదం",
        "name_hi": "उच्च घाटा जोखिम",
        "color": "#c62828",   # Crimson Red
        "bg_color": "#ffebee",
        "badge_en": "SEVERE DEFICIT RISK (>=25% SHORTFALL)",
        "badge_te": "తీవ్ర లోటు ప్రమాదం (>=25% లోటు)",
        "badge_hi": "गंभीर घाटा जोखिम (>=25% कमी)",
        "summary_en": "Projected 3-month rainfall has high risk of falling 25% or more below the district normal. Preemptive storage and tanker planning strongly recommended.",
        "summary_te": "రాబోయే 3 నెలల్లో వర్షపాతం సాధారణం కంటే 25% లేదా అంతకంటే ఎక్కువ తగ్గే అవకాశం ఉంది. ముందస్తు నీటి నిల్వ ఏర్పాట్లు చేసుకోండి.",
        "summary_hi": "अनुमानित 3-माह की वर्षा में सामान्य से 25% या अधिक की कमी का उच्च जोखिम है। अग्रिम जल संचयन और टैंकर प्रबंधन की सिफारिश की जाती है।"
    }
}

def load_pipeline_metadata() -> Dict[str, Any]:
    """Loads model metadata containing evaluation metrics and feature definitions."""
    candidates = [
        Path("models/model_metadata.json"),
        Path(__file__).parent.parent / "models" / "model_metadata.json"
    ]
    for p in candidates:
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    return {}

def verify_feature_schema(X_features: pd.DataFrame, expected_features: List[str]) -> bool:
    """Verifies that the incoming feature schema matches the saved model exactly."""
    if not isinstance(X_features, pd.DataFrame):
        raise TypeError(f"Expected pandas DataFrame for features, got {type(X_features)}")
    
    missing = [f for f in expected_features if f not in X_features.columns]
    if missing:
        raise ValueError(f"Feature schema mismatch. Missing features: {missing}")
    return True

def predict_water_stress(
    model: RandomForestClassifier,
    X_features: pd.DataFrame,
    expected_features: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Executes inference and evaluates predictive uncertainty.
    
    Validates schema, extracts class probabilities, and determines
    uncertainty boundaries.
    """
    if expected_features:
        verify_feature_schema(X_features, expected_features)
        X_eval = X_features[expected_features]
    else:
        X_eval = X_features

    probas = model.predict_proba(X_eval)[0]
    classes = model.classes_
    proba_dict = {int(c): float(p) for c, p in zip(classes, probas)}

    for c in [0, 1, 2]:
        proba_dict.setdefault(c, 0.0)

    predicted_class = int(max(proba_dict, key=proba_dict.get))
    max_prob = proba_dict[predicted_class]

    sorted_probs = sorted(proba_dict.values(), reverse=True)
    margin = sorted_probs[0] - sorted_probs[1] if len(sorted_probs) > 1 else sorted_probs[0]

    # Uncertainty classification
    if max_prob >= 0.55 and margin >= 0.20:
        uncertainty_level = "low"
        uncertainty_label_en = "High Model Confidence"
        uncertainty_label_te = "మోడల్ విశ్వసనీయత ఎక్కువ"
        uncertainty_label_hi = "मॉडल विश्वसनीयता उच्च"
        uncertainty_desc_en = f"Clear probability separation ({max_prob:.0%} dominant class)."
        uncertainty_desc_te = f"స్పష్టమైన ఫలితం ({max_prob:.0%} సంభావ్యత)."
        uncertainty_desc_hi = f"स्पष्ट प्रायिकता अंतर ({max_prob:.0%} प्रमुख श्रेणी)।"
    elif max_prob >= 0.40:
        uncertainty_level = "moderate"
        uncertainty_label_en = "Moderate Uncertainty"
        uncertainty_label_te = "మధ్యస్థ అనిశ్చితి"
        uncertainty_label_hi = "मध्यम अनिश्चितता"
        uncertainty_desc_en = "Model identifies a leading tendency, but seasonal shifts may influence totals."
        uncertainty_desc_te = "ప్రధాన ధోరణి కనిపించినప్పటికీ, కాలానుగుణ మార్పుల ప్రభావం ఉండవచ్చు."
        uncertainty_desc_hi = "मॉडल एक प्रमुख रुझान दिखाता है, लेकिन मौसमी बदलाव कुल वर्षा को प्रभावित कर सकते हैं।"
    else:
        uncertainty_level = "high"
        uncertainty_label_en = "Elevated Uncertainty"
        uncertainty_label_te = "ఎక్కువ అనిశ్చితి"
        uncertainty_label_hi = "उच्च अनिश्चितता"
        uncertainty_desc_en = "Probabilities are distributed across multiple outcomes. Monitor monthly updates."
        uncertainty_desc_te = "అంచనా సమానంగా విస్తరించి ఉంది. నెలవారీ తాజా సమాచారాన్ని గమనించండి."
        uncertainty_desc_hi = "प्रायिकताएं कई परिणामों में बंटी हैं। मासिक अपडेट पर नजर रखें।"

    meta = RISK_LEVEL_METADATA.get(predicted_class, RISK_LEVEL_METADATA[0])

    return {
        "predicted_class": predicted_class,
        "probabilities": proba_dict,
        "prob_low": proba_dict[0],
        "prob_medium": proba_dict[1],
        "prob_high": proba_dict[2],
        "margin": round(margin, 3),
        "uncertainty_level": uncertainty_level,
        "uncertainty_label_en": uncertainty_label_en,
        "uncertainty_label_te": uncertainty_label_te,
        "uncertainty_label_hi": uncertainty_label_hi,
        "uncertainty_desc_en": uncertainty_desc_en,
        "uncertainty_desc_te": uncertainty_desc_te,
        "uncertainty_desc_hi": uncertainty_desc_hi,
        "risk_name_en": meta["name_en"],
        "risk_name_te": meta["name_te"],
        "risk_name_hi": meta["name_hi"],
        "color": meta["color"],
        "bg_color": meta["bg_color"],
        "badge_en": meta["badge_en"],
        "badge_te": meta["badge_te"],
        "badge_hi": meta["badge_hi"],
        "summary_en": meta["summary_en"],
        "summary_te": meta["summary_te"],
        "summary_hi": meta["summary_hi"],
        "scenario_notice_en": "Scenario: Persistence of currently observed Pacific ONI climate anomaly. Not a 3-month ENSO forecast.",
        "scenario_notice_te": "సన్నివేశం: ప్రస్తుతం నమోదైన పసిఫిక్ ONI ఆధారంగా అంచనా. ఇది భవిష్యత్ ఎల్ నినో సూచన కాదు.",
        "scenario_notice_hi": "परिदृश्य: वर्तमान में दर्ज प्रशांत ONI जलवायु विसंगति का स्थायित्व। यह 3-माह का ENSO पूर्वानुमान नहीं है।"
    }

def predict_all_districts(
    model: RandomForestClassifier,
    expected_features: List[str],
    oni_series: pd.Series,
    clim_data: Dict[str, Any],
    rain_df: Optional[pd.DataFrame] = None,
    month: int = 9,
    year: int = 2026
) -> Dict[str, Dict[str, Any]]:
    """
    Computes rainfall-deficit risk predictions for all 33 Telangana districts.
    Returns: Dict[district_name, Dict[str, Any]] containing prediction object,
             predicted_class, probabilities, and rainfall values.
    """
    from utils.districts import EXACT_33_DISTRICTS
    from utils.feature_engineering import build_inference_features

    results = {}
    for d in EXACT_33_DISTRICTS:
        if rain_df is not None and not rain_df.empty:
            sub = rain_df[rain_df["district"] == d].sort_values("date")
            recent_3m = float(sub.tail(3)["rain"].sum()) if len(sub) >= 3 else 100.0
        else:
            recent_3m = 100.0

        X_df = build_inference_features(
            district=d,
            rain3_mm=recent_3m,
            month=month,
            year=year,
            oni_series=oni_series,
            clim=clim_data,
            expected_features=expected_features
        )
        res = predict_water_stress(model, X_df, expected_features=expected_features)
        res["recent_rain3_mm"] = recent_3m
        results[d] = res

    return results

