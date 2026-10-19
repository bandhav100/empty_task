"""Open-Meteo Air Quality API Client.
Retrieves and categorizes both US AQI and European AQI separately with pollutant units in µg/m³.
Includes explicit scientific disclosures regarding satellite/CAMS model-based data vs physical CPCB ground monitors.
"""

from typing import Dict, Any, Optional
import requests
import datetime as dt

AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

# US EPA AQI Categories (0 - 500)
US_AQI_CATEGORIES = [
    {
        "name_en": "Good", "name_te": "మంచిది", "name_hi": "अच्छा",
        "color": "#1b5e20", "bg_color": "#e8f5e9",
        "min": 0, "max": 50,
        "advice_en": "Air quality is satisfactory. Air pollution poses little or no risk.",
        "advice_te": "గాలి స్వచ్ఛంగా ఉంది. బహిరంగ కార్యకలాపాలు ఎటువంటి ఇబ్బంది లేకుండా కొనసాగించవచ్చు.",
        "advice_hi": "वायु गुणवत्ता संतोषजनक है। वायु प्रदूषण से कोई विशेष जोखिम नहीं है।"
    },
    {
        "name_en": "Moderate", "name_te": "మధ్యస్థం", "name_hi": "मध्यम",
        "color": "#f57f17", "bg_color": "#fffde7",
        "min": 51, "max": 100,
        "advice_en": "Air quality is acceptable. Unusually sensitive individuals should consider reducing prolonged outdoor exertion.",
        "advice_te": "చాలామందికి సురక్షితం. శ్వాసకోశ సమస్యలు ఉన్నవారు ఎక్కువ సమయం ఆరుబయట శ్రమ చేయకుండా జాగ్రత్త పడాలి.",
        "advice_hi": "वायु गुणवत्ता स्वीकार्य है। संवेदनशील व्यक्ति लंबे समय तक बाहर अत्यधिक परिश्रम कम करें।"
    },
    {
        "name_en": "Unhealthy for Sensitive Groups", "name_te": "సున్నిత వర్గాలకు అనారోగ్యకరం", "name_hi": "संवेदनशील समूहों के लिए अस्वस्थ",
        "color": "#e65100", "bg_color": "#fff3e0",
        "min": 101, "max": 150,
        "advice_en": "Members of sensitive groups (children, elders, asthma patients) may experience health effects. General public is less likely affected.",
        "advice_te": "పిల్లలు, వృద్ధులు మరియు ఆస్తమా లేదా గుండె సమస్యలు ఉన్నవారు బయట ఎక్కువ సమయం గడపడం తగ్గించాలి.",
        "advice_hi": "संवेदनशील समूहों (बच्चों, बुजुर्गों, अस्थमा रोगियों) को स्वास्थ्य समस्याएं हो सकती हैं।"
    },
    {
        "name_en": "Unhealthy", "name_te": "అనారోగ్యకరం", "name_hi": "अस्वस्थ",
        "color": "#b71c1c", "bg_color": "#ffebee",
        "min": 151, "max": 200,
        "advice_en": "Everyone may begin to experience health effects; sensitive groups may experience serious health effects. Wear an N95 mask outside.",
        "advice_te": "ప్రతి ఒక్కరి ఆరోగ్యంపై ప్రభావం పడవచ్చు. అందరూ బయటకు వెళ్ళినప్పుడు N95 మాస్క్ ధరించడం మంచిది.",
        "advice_hi": "सभी लोग स्वास्थ्य प्रभाव महसूस कर सकते हैं। बाहर जाते समय N95 मास्क पहनें।"
    },
    {
        "name_en": "Very Unhealthy", "name_te": "తీవ్ర అనారోగ్యకరం", "name_hi": "बहुत अस्वस्थ",
        "color": "#4a148c", "bg_color": "#f3e5f5",
        "min": 201, "max": 300,
        "advice_en": "Health alert: risk of health effects is increased for everyone. Avoid prolonged outdoor exertion.",
        "advice_te": "ఆరోగ్య హెచ్చరిక: అందరికీ ఆరోగ్య సమస్యల ప్రమాదం ఉంది. బయట శారీరక శ్రమ చేయవద్దు, కిటికీలు మూసి ఉంచండి.",
        "advice_hi": "स्वास्थ्य चेतावनी: सभी के लिए गंभीर प्रभाव का जोखिम। बाहर शारीरिक श्रम से बचें।"
    },
    {
        "name_en": "Hazardous", "name_te": "ప్రమాదకరం", "name_hi": "खतरनाक",
        "color": "#3e2723", "bg_color": "#efebe9",
        "min": 301, "max": 9999,
        "advice_en": "Health warning of emergency conditions: everyone is more likely to be affected. Remain indoors with filtered air.",
        "advice_te": "అత్యవసర పరిస్థితి: ప్రతి ఒక్కరూ ఇళ్లలోనే ఉండండి. తలుపులు, కిటికీలు మూసివేయండి, అవసరమైతే వైద్య సలహా తీసుకోండి.",
        "advice_hi": "आपातकालीन स्वास्थ्य चेतावनी: सभी लोग घर के अंदर रहें और खिड़कियां बंद रखें।"
    }
]

# European Air Quality Index (EAQI - EEA)
EUROPEAN_AQI_CATEGORIES = [
    {"name_en": "Good", "name_te": "మంచిది", "name_hi": "अच्छा", "color": "#2e7d32", "min": 0, "max": 20},
    {"name_en": "Fair", "name_te": "పర్వాలేదు", "name_hi": "संतोषजनक", "color": "#689f38", "min": 21, "max": 40},
    {"name_en": "Moderate", "name_te": "మధ్యస్థం", "name_hi": "मध्यम", "color": "#fbc02d", "min": 41, "max": 60},
    {"name_en": "Poor", "name_te": "చెడ్డది", "name_hi": "खराब", "color": "#f57c00", "min": 61, "max": 80},
    {"name_en": "Very Poor", "name_te": "చాలా చెడ్డది", "name_hi": "बहुत खराब", "color": "#d32f2f", "min": 81, "max": 100},
    {"name_en": "Extremely Poor", "name_te": "తీవ్రంగా చెడ్డది", "name_hi": "अत्यधिक खराब", "color": "#7b1fa2", "min": 101, "max": 9999}
]

def classify_us_aqi(aqi_val: Optional[int]) -> Dict[str, Any]:
    """Categorize US AQI into EPA standard bands."""
    if aqi_val is None:
        return {
            "category_index": -1, "name_en": "Unavailable", "name_te": "లభ్యం కాలేదు", "name_hi": "उपलब्ध नहीं",
            "color": "#9e9e9e", "bg_color": "#f5f5f5",
            "advice_en": "Air quality readings currently unavailable.",
            "advice_te": "గాలి నాణ్యత సమాచారం ప్రస్తుతం లభ్యం కాలేదు.",
            "advice_hi": "वायु गुणवत्ता आंकड़े वर्तमान में उपलब्ध नहीं हैं।"
        }
    for i, cat in enumerate(US_AQI_CATEGORIES):
        if cat["min"] <= aqi_val <= cat["max"]:
            res = dict(cat)
            res["category_index"] = i
            return res
    res = dict(US_AQI_CATEGORIES[-1])
    res["category_index"] = len(US_AQI_CATEGORIES) - 1
    return res

def classify_european_aqi(aqi_val: Optional[int]) -> Dict[str, Any]:
    """Categorize European AQI into EEA standard bands."""
    if aqi_val is None:
        return {"name_en": "Unavailable", "name_te": "లభ్యం కాలేదు", "name_hi": "उपलब्ध नहीं", "color": "#9e9e9e"}
    for cat in EUROPEAN_AQI_CATEGORIES:
        if cat["min"] <= aqi_val <= cat["max"]:
            return cat
    return EUROPEAN_AQI_CATEGORIES[-1]

def fetch_current_air_quality(lat: float, lon: float, timeout: int = 15) -> Dict[str, Any]:
    """
    Fetches real-time air quality metrics from Open-Meteo Air Quality endpoint.
    
    IMPORTANT LABELS & DISCLOSURE:
    - US AQI and European AQI are clearly separated.
    - Neither index is labeled as CPCB India AQI. No invented conversions are applied.
    - Data represents atmospheric model reanalysis (Copernicus CAMS & SILAM),
      not a direct physical CPCB monitoring station sensor.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "us_aqi,european_aqi,pm2_5,pm10,carbon_monoxide,nitrogen_dioxide,ozone",
        "hourly": "us_aqi,european_aqi,pm2_5,pm10",
        "timezone": "Asia/Kolkata"
    }

    try:
        resp = requests.get(AIR_QUALITY_URL, params=params, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        raw = data.get("current", {})

        # Fallback to hourly if current is missing
        us_aqi = raw.get("us_aqi")
        european_aqi = raw.get("european_aqi")
        pm2_5 = raw.get("pm2_5")
        pm10 = raw.get("pm10")
        co = raw.get("carbon_monoxide")
        no2 = raw.get("nitrogen_dioxide")
        ozone = raw.get("ozone")
        time_str = raw.get("time", "")

        if us_aqi is None and "hourly" in data:
            hourly = data["hourly"]
            h_times = hourly.get("time", [])
            h_us_aqi = [v for v in hourly.get("us_aqi", []) if v is not None]
            if h_us_aqi:
                us_aqi = h_us_aqi[-1]
                time_str = h_times[-1] if h_times else dt.datetime.now().isoformat()
            h_eu_aqi = [v for v in hourly.get("european_aqi", []) if v is not None]
            if h_eu_aqi:
                european_aqi = h_eu_aqi[-1]
            h_pm25 = [v for v in hourly.get("pm2_5", []) if v is not None]
            if h_pm25:
                pm2_5 = h_pm25[-1]
            h_pm10 = [v for v in hourly.get("pm10", []) if v is not None]
            if h_pm10:
                pm10 = h_pm10[-1]

        us_cat = classify_us_aqi(us_aqi)
        eu_cat = classify_european_aqi(european_aqi)

        return {
            "status": "success",
            "us_aqi": us_aqi if us_aqi is not None else 0,
            "european_aqi": european_aqi if european_aqi is not None else 0,
            "pm2_5": round(float(pm2_5), 1) if pm2_5 is not None else 0.0,
            "pm10": round(float(pm10), 1) if pm10 is not None else 0.0,
            "carbon_monoxide": round(float(co), 1) if co is not None else 0.0,
            "nitrogen_dioxide": round(float(no2), 1) if no2 is not None else 0.0,
            "ozone": round(float(ozone), 1) if ozone is not None else 0.0,
            "timestamp": time_str,
            "us_aqi_category_en": us_cat["name_en"],
            "us_aqi_category_te": us_cat["name_te"],
            "us_aqi_category_hi": us_cat["name_hi"],
            "us_aqi_color": us_cat["color"],
            "us_aqi_bg": us_cat["bg_color"],
            "us_aqi_advice_en": us_cat["advice_en"],
            "us_aqi_advice_te": us_cat["advice_te"],
            "us_aqi_advice_hi": us_cat["advice_hi"],
            "european_aqi_category_en": eu_cat["name_en"],
            "european_aqi_category_te": eu_cat["name_te"],
            "european_aqi_category_hi": eu_cat["name_hi"],
            "european_aqi_color": eu_cat["color"],
            "pollutant_unit": "µg/m³",
            "source": "Open-Meteo Air Quality (Copernicus CAMS & SILAM reanalysis)",
            "source_url": "https://air-quality-api.open-meteo.com",
            "station_disclosure": "Atmospheric model reanalysis data; not a physical ground-level CPCB monitoring station."
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e),
            "us_aqi": None,
            "european_aqi": None,
            "pm2_5": None,
            "pm10": None,
            "carbon_monoxide": None,
            "nitrogen_dioxide": None,
            "ozone": None,
            "timestamp": dt.datetime.now().isoformat(),
            "us_aqi_category_en": "Unavailable",
            "us_aqi_category_te": "లభ్యం కాలేదు",
            "us_aqi_color": "#9e9e9e",
            "us_aqi_bg": "#f5f5f5",
            "us_aqi_advice_en": "Live air quality data could not be retrieved at this moment.",
            "us_aqi_advice_te": "లైవ్ ఎయిర్ క్వాలిటీ సమాచారం ప్రస్తుతం లభ్యం కాలేదు.",
            "european_aqi_category_en": "Unavailable",
            "european_aqi_category_te": "లభ్యం కాలేదు",
            "european_aqi_color": "#9e9e9e",
            "pollutant_unit": "µg/m³",
            "source": "Open-Meteo Air Quality",
            "source_url": "https://air-quality-api.open-meteo.com",
            "station_disclosure": "Data unavailable."
        }
