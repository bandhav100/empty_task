"""Telangana Water Stress & Air Quality Advisor.
Swachh & Sustainable Bharat — El Niño-Aware Citizen Early Warning System.
Full GIS Map, Polygon Containment, and Real-Time Multi-API Integration Layer.
"""

import math
import datetime as dt
from pathlib import Path
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from streamlit_js_eval import get_geolocation

from utils.districts import (
    DISTRICTS,
    EXACT_33_DISTRICTS,
    DISTRICT_NAMES,
    DISTRICT_TELUGU,
    DISTRICT_HINDI,
    normalize_district_name,
    format_district_name,
    get_coords
)
from utils.location import find_district_by_polygon, find_nearest_district
from utils.climate_data import (
    load_or_fetch_oni_bundle,
    get_oni_at,
    classify_enso_state
)
from utils.weather_api import (
    fetch_recent_3month_rainfall,
    fetch_weather_forecast
)
from utils.air_quality_api import fetch_current_air_quality
from utils.data_loader import (
    load_model_bundle,
    load_climatology,
    load_clim_normals,
    load_metrics,
    load_model_metadata,
    load_telangana_geojson,
    load_rain_monthly_df
)
from utils.feature_engineering import build_inference_features, calculate_rainfall_percentile
from utils.prediction import predict_water_stress, predict_all_districts
from utils.recommendations import get_water_recommendations, get_el_nino_precautions
from utils.translations import get_text
from utils.map_renderer import render_telangana_interactive_map
from utils.cwc_ffs import (
    CWC_FFS_PORTAL_URL,
    DISTRICT_BASIN_MAP,
    get_cwc_stations_for_district,
    check_cwc_portal_status
)
from utils.water_directory import (
    get_district_mandals,
    get_district_water_summary,
    get_mandal_directory_table,
    get_mandal_detailed_profile,
    get_district_infrastructure
)

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Telangana Water & Air Advisor (Prototype)",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- CUSTOM CSS -----------------
st.markdown("""
<style>
    .metric-card {
        background: #f8fafc;
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 0.8rem;
    }
    .risk-banner {
        color: #ffffff;
        padding: 18px 24px;
        border-radius: 12px;
        font-size: 1.45rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .badge-chip {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-right: 8px;
    }
    .weather-card {
        background: #ffffff;
        border-radius: 10px;
        padding: 12px 14px;
        border: 1px solid #cbd5e1;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 14px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 18px;
        font-weight: 600;
        font-size: 1.0rem;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- DATA CACHING -----------------
@st.cache_resource(show_spinner=False)
def get_cached_resources():
    model_bundle = load_model_bundle()
    climatology = load_climatology()
    clim_normals = load_clim_normals()
    metrics = load_metrics()
    model_metadata = load_model_metadata()
    geojson = load_telangana_geojson()
    rain_df = load_rain_monthly_df()
    return model_bundle, climatology, clim_normals, metrics, model_metadata, geojson, rain_df

@st.cache_data(ttl=86400, show_spinner=False)
def get_cached_oni_bundle():
    return load_or_fetch_oni_bundle()

@st.cache_data(ttl=6 * 3600, show_spinner=False)
def get_cached_recent_rainfall(lat: float, lon: float):
    return fetch_recent_3month_rainfall(lat, lon)

@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_forecast(lat: float, lon: float):
    return fetch_weather_forecast(lat, lon)

@st.cache_data(ttl=1800, show_spinner=False)
def get_cached_aqi(lat: float, lon: float):
    return fetch_current_air_quality(lat, lon)

# ----------------- APP INITIALIZATION -----------------
try:
    model_bundle, clim_data, clim_normals, model_metrics, model_metadata, telangana_geo, rain_df = get_cached_resources()
except Exception as e:
    st.error(f"Error loading system assets: {e}")
    st.info("Run `python train_model.py` to regenerate model and climatology artifacts.")
    st.stop()

# Initialize session state for selected district
if "selected_district" not in st.session_state:
    st.session_state["selected_district"] = "ALL"


# ----------------- SIDEBAR CONTROLS -----------------
with st.sidebar:
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, rgba(2,132,199,0.08), rgba(14,165,233,0.04)); border: 1px solid rgba(2,132,199,0.25); border-radius: 10px; padding: 12px 14px; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="font-size: 1.15rem; font-weight: 700; color: #0284c7;">💧 TG W&AIR</span>
                <span style="background: #fef3c7; color: #92400e; font-size: 0.68rem; font-weight: 700; padding: 2px 8px; border-radius: 6px; letter-spacing: 0.5px; border: 1px solid #fde68a;">PROTOTYPE</span>
            </div>
            <div style="font-size: 0.8rem; font-weight: 600; color: var(--text-color, #334155); margin-top: 4px;">
                Water & Air Advisory System
            </div>
            <div style="font-size: 0.74rem; color: var(--text-color, #64748b); opacity: 0.85; margin-top: 2px; line-height: 1.3;">
                Research & Decision-Support Prototype
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.markdown("### 🌐 Language / భాష / भाषा")
    lang_choice = st.radio(
        "Select Language",
        ["English", "తెలుగు", "हिंदी"],
        horizontal=True,
        label_visibility="collapsed"
    )
    if lang_choice == "తెలుగు":
        lang = "te"
    elif lang_choice == "हिंदी":
        lang = "hi"
    else:
        lang = "en"

    st.markdown("---")
    st.markdown(f"### 📍 {get_text('location_header', lang)}")
    st.caption(get_text("loc_permission_info", lang))

    use_gps = st.checkbox(get_text("use_location_checkbox", lang), value=False)
    detected_district = None

    if use_gps:
        with st.spinner("Requesting browser GPS permission (strictly in-memory)..."):
            loc = get_geolocation()
            if loc and "coords" in loc:
                u_lat = loc["coords"]["latitude"]
                u_lon = loc["coords"]["longitude"]
                resolved_d, is_inside, dist_km = find_district_by_polygon(u_lat, u_lon, telangana_geo)
                
                if is_inside and resolved_d:
                    detected_district = resolved_d
                    st.session_state["selected_district"] = resolved_d
                    st.session_state["_sync_district_dropdown"] = True
                    st.success(get_text("loc_detected_inside", lang).format(district=format_district_name(resolved_d, lang)))
                else:
                    st.warning(get_text("loc_outside", lang).format(
                        lat=u_lat, lon=u_lon, dist=dist_km,
                        district=format_district_name(resolved_d, lang)
                    ))
            else:
                st.info("Awaiting browser location approval. If denied, select your district manually below.")

    # 33 Official Districts dropdown + All Districts option
    if lang == "en":
        all_option_label = "🌟 All Districts (Statewide Overview)"
        district_display_list = [f"{d} ({DISTRICT_TELUGU.get(d, d)})" for d in EXACT_33_DISTRICTS]
    elif lang == "te":
        all_option_label = "🌟 అన్ని జిల్లాలు (రాష్ట్ర వ్యాప్త పరిశీలన)"
        district_display_list = [f"{DISTRICT_TELUGU.get(d, d)} ({d})" for d in EXACT_33_DISTRICTS]
    else:
        all_option_label = "🌟 सभी जिले (राज्यव्यापी अवलोकन)"
        district_display_list = [f"{DISTRICT_HINDI.get(d, d)} ({d})" for d in EXACT_33_DISTRICTS]

    display_options = [all_option_label] + district_display_list

    if "selected_district" not in st.session_state:
        st.session_state["selected_district"] = "ALL"

    curr_dist = st.session_state["selected_district"]
    if curr_dist == "ALL" or curr_dist not in EXACT_33_DISTRICTS:
        target_display = all_option_label
    else:
        if lang == "en":
            target_display = f"{curr_dist} ({DISTRICT_TELUGU.get(curr_dist, curr_dist)})"
        elif lang == "te":
            target_display = f"{DISTRICT_TELUGU.get(curr_dist, curr_dist)} ({curr_dist})"
        else:
            target_display = f"{DISTRICT_HINDI.get(curr_dist, curr_dist)} ({curr_dist})"

    if (
        "district_selector_dropdown" not in st.session_state
        or st.session_state.get("_sync_district_dropdown")
        or st.session_state["district_selector_dropdown"] not in display_options
    ):
        st.session_state["district_selector_dropdown"] = target_display
        st.session_state["_sync_district_dropdown"] = False

    def on_dropdown_change():
        selected_disp = st.session_state["district_selector_dropdown"]
        if selected_disp == all_option_label:
            st.session_state["selected_district"] = "ALL"
        else:
            idx = display_options.index(selected_disp)
            st.session_state["selected_district"] = EXACT_33_DISTRICTS[idx - 1]

    st.selectbox(
        get_text("district_select_label", lang),
        display_options,
        key="district_selector_dropdown",
        on_change=on_dropdown_change
    )

    chosen_district = st.session_state["selected_district"]
    if chosen_district == "ALL":
        st.caption("Statewide: Telangana (33 Administrative Districts)")
    else:
        lat, lon = get_coords(chosen_district)
        st.caption(get_text("district_coordinates", lang).format(lat=lat, lon=lon))

    st.markdown("---")
    st.markdown(f"**{get_text('badge_theme', lang)}**")
    st.caption("Theme: Swachh & Sustainable Bharat\nResearch Prototype • 33 Districts GIS Boundary Coverage")

# ----------------- LIVE DATA & PREDICTION PIPELINE -----------------
active_district = st.session_state["selected_district"]
is_all_mode = (active_district == "ALL")
rep_district = "Hyderabad" if is_all_mode else active_district
active_lat, active_lon = get_coords(rep_district)

try:
    with st.spinner("Fetching live climate, forecast, and air quality feeds..."):
        oni_series, oni_metadata = get_cached_oni_bundle()
        recent_rain_mm, rain_month, rain_year = get_cached_recent_rainfall(active_lat, active_lon)
        weather_forecast = get_cached_forecast(active_lat, active_lon)
        air_quality = get_cached_aqi(active_lat, active_lon)

        # Batch prediction for all 33 districts so every polygon is colored by alert
        all_district_preds = predict_all_districts(
            model=model_bundle["model"],
            expected_features=model_bundle["features"],
            oni_series=oni_series,
            clim_data=clim_data,
            rain_df=rain_df,
            month=rain_month,
            year=rain_year
        )
        district_risk_dict = {d: info["predicted_class"] for d, info in all_district_preds.items()}

        target_d = "Hyderabad" if is_all_mode else active_district
        prediction = all_district_preds.get(target_d, all_district_preds["Hyderabad"])

        X_df = build_inference_features(
            district=target_d,
            rain3_mm=prediction.get("recent_rain3_mm", recent_rain_mm),
            month=rain_month,
            year=rain_year,
            oni_series=oni_series,
            clim=clim_data,
            expected_features=model_bundle["features"]
        )

        # Climatology empirical percentile
        hist_samples = clim_data.get(target_d, {}).get(str(rain_month), [])
        if not hist_samples and "Kumuram Bheem Asifabad" in clim_data and target_d == "Kumuram Bheem":
            hist_samples = clim_data["Kumuram Bheem Asifabad"].get(str(rain_month), [])
        rain_percentile = calculate_rainfall_percentile(recent_rain_mm, hist_samples)

        # ENSO status at observation date
        ts_now = pd.Timestamp(year=rain_year, month=rain_month, day=1)
        current_oni = get_oni_at(oni_series, ts_now)
        prev_oni = get_oni_at(oni_series, ts_now - pd.DateOffset(months=3))
        oni_delta = current_oni - prev_oni
        _, enso_label_en = classify_enso_state(current_oni)

except Exception as err:
    st.error(f"{get_text('err_fetch', lang)} (Details: {err})")
    st.stop()

# ----------------- MAIN TITLE & BRANDING -----------------
st.title(f"💧 {get_text('app_title', lang)}")
st.markdown(
    f"*{get_text('app_subtitle', lang)}* &nbsp;&nbsp;"
    f"<span style='background:#fef3c7; color:#92400e; font-size:0.75rem; font-weight:700; padding:3px 9px; border-radius:6px; border:1px solid #fde68a; vertical-align:middle;'>RESEARCH PROTOTYPE</span>",
    unsafe_allow_html=True
)

# ----------------- NAVIGATION TABS -----------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    f"📊 {get_text('tab_overview', lang)}",
    f"🗺️ {get_text('tab_map', lang)}",
    f"🌤️ {get_text('tab_weather', lang)}",
    f"🌊 {get_text('tab_cwc_flood', lang)}",
    f"🔬 {get_text('tab_model_evaluation', lang)}",
    f"ℹ️ {get_text('tab_about', lang)}"
])

# ----------------- EL NIÑO PRECAUTIONS COMPONENT -----------------
def render_el_nino_precautions_section(lang: str, key_suffix: str = ""):
    st.markdown("---")
    st.subheader(f"{get_text('elnino_precautions_title', lang)}")
    st.caption(f"{get_text('elnino_precautions_subtitle', lang)}")

    categories = get_el_nino_precautions(lang=lang)

    if lang == "en":
        all_label = "🌟 All 5 Domains"
    elif lang == "te":
        all_label = "🌟 అన్ని 5 విభాగాలు"
    else:
        all_label = "🌟 सभी 5 श्रेणियां"

    cat_labels = [all_label] + [f"{c['icon']} {c['title']}" for c in categories]

    selected_filter = st.radio(
        "Precaution Domain Filter",
        cat_labels,
        horizontal=True,
        key=f"precautions_filter_{key_suffix}",
        label_visibility="collapsed"
    )

    displayed_cats = categories if selected_filter == all_label else [c for c in categories if f"{c['icon']} {c['title']}" == selected_filter]

    for cat in displayed_cats:
        exp_title = f"{cat['icon']} **{cat['title']}** ({len(cat['precautions'])} " + ("Key Measures" if lang == "en" else ("కీలక రక్షణ చర్యలు" if lang == "te" else "प्रमुख सुरक्षा उपाय")) + ")"
        with st.expander(exp_title, expanded=True):
            cols = st.columns(2)
            for idx, pt in enumerate(cat["precautions"], 1):
                col_target = cols[(idx - 1) % 2]
                with col_target:
                    st.markdown(
                        f"""
                        <div style="background: rgba(255,255,255,0.03); border-left: 4px solid {cat['color']}; padding: 10px 14px; margin-bottom: 8px; border-radius: 6px; border: 1px solid rgba(226, 232, 240, 0.15);">
                            <span style="font-weight: 800; color: {cat['color']}; font-size: 0.88rem; letter-spacing: 0.5px;">MEASURE #{idx}</span>
                            <div style="font-size: 0.92rem; line-height: 1.45; margin-top: 4px; color: var(--text-color, #334155);">
                                {pt}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

# ================= TAB 1: OVERVIEW & RISK =================
with tab1:
    if is_all_mode:
        st.subheader("🌟 " + ("Telangana Statewide 33-Districts Alert Overview" if lang == "en" else "తెలంగాణ రాష్ట్ర వ్యాప్త 33 జిల్లాల హెచ్చరికల సమీక్ష"))

        high_cnt = sum(1 for r in district_risk_dict.values() if r == 2)
        med_cnt = sum(1 for r in district_risk_dict.values() if r == 1)
        low_cnt = sum(1 for r in district_risk_dict.values() if r == 0)

        banner_color = "#c62828" if high_cnt > 15 else ("#f57f17" if med_cnt > 10 else "#2e7d32")
        st.markdown(
            f"""
            <div class="risk-banner" style="background: {banner_color};">
                <span style="font-size: 0.9rem; letter-spacing: 1px; display: block; opacity: 0.9;">
                    STATEWIDE CITIZEN EARLY WARNING • ALL 33 DISTRICTS
                </span>
                {"High Deficit Alert across Telangana" if lang == "en" else "తెలంగాణ అంతటా అధిక వర్షపాత లోటు హెచ్చరిక"} — {high_cnt}/33 {"Districts in Severe Deficit Risk" if lang == "en" else "జిల్లాలు అధిక ప్రమాదంలో ఉన్నాయి"}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(f"🛡️ **{get_text('risk_proxy_disclaimer', lang)}**")

        # 4 Statewide Summary Metric Cards
        s1, s2, s3, s4 = st.columns(4)
        with s1:
            st.metric(
                label="🔴 High Deficit Risk" if lang == "en" else "🔴 అధిక ప్రమాదం",
                value=f"{high_cnt} / 33",
                delta=f"{high_cnt / 33:.0%} of districts"
            )
        with s2:
            st.metric(
                label="🟡 Medium Deficit Risk" if lang == "en" else "🟡 మధ్యస్థ ప్రమాదం",
                value=f"{med_cnt} / 33",
                delta=f"{med_cnt / 33:.0%} of districts"
            )
        with s3:
            st.metric(
                label="🟢 Low Deficit Risk" if lang == "en" else "🟢 తక్కువ ప్రమాదం",
                value=f"{low_cnt} / 33",
                delta=f"{low_cnt / 33:.0%} of districts"
            )
        with s4:
            st.metric(
                label="🌊 Pacific Climate (ONI)",
                value=f"{current_oni:+.2f}°C",
                delta=f"{enso_label_en} ({oni_delta:+.2f} 3M)"
            )

        st.markdown("---")
        st.markdown(f"#### 📋 " + ("District-by-District Alert Roster (All 33 Districts)" if lang == "en" else "జిల్లా వారీ హెచ్చరికల జాబితా (మొత్తం 33 జిల్లాలు)"))

        roster_cols = st.columns(3)
        for idx, d_name in enumerate(EXACT_33_DISTRICTS):
            r_cat = district_risk_dict.get(d_name, 0)
            col_target = roster_cols[idx % 3]
            d_display = format_district_name(d_name, lang)

            if r_cat == 2:
                badge_bg = "#fee2e2"
                badge_text_c = "#991b1b"
                badge_border = "#ef4444"
                label_txt = "HIGH RISK (>=25%)" if lang == "en" else "అధిక లోటు (>=25%)"
            elif r_cat == 1:
                badge_bg = "#fef3c7"
                badge_text_c = "#92400e"
                badge_border = "#f59e0b"
                label_txt = "MEDIUM RISK (10-25%)" if lang == "en" else "మధ్యస్థ లోటు (10-25%)"
            else:
                badge_bg = "#dcfce7"
                badge_text_c = "#166534"
                badge_border = "#22c55e"
                label_txt = "LOW RISK (<10%)" if lang == "en" else "తక్కువ లోటు (<10%)"

            with col_target:
                st.markdown(
                    f"""
                    <div style="background:{badge_bg}; border: 1.5px solid {badge_border}; border-radius: 8px; padding: 9px 14px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700; color: #0f172a; font-size: 0.95rem;">{d_display}</span>
                        <span style="font-weight: 800; font-size: 0.75rem; color: {badge_text_c}; text-transform: uppercase;">{label_txt}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.info("💡 " + (
            "Click on any district polygon in the 🗺️ Map tab or choose from the dropdown to inspect local rainfall percentiles, live weather forecasts, and CWC river gauges."
            if lang == "en" else
            "మరిన్ని వివరాల కోసం 🗺️ మ్యాప్ ట్యాబ్‌లోని జిల్లాపై క్లిక్ చేయండి లేదా సైడ్‌బార్ డ్రాప్‌డౌన్ ద్వారా ఎంచుకోండి."
        ))

        # Statewide El Niño Precautions Playbook
        render_el_nino_precautions_section(lang, key_suffix="statewide")

    else:
        col_water, col_air = st.columns([1.2, 0.8], gap="large")

        with col_water:
            st.subheader(f"💧 {get_text('water_section_title', lang)}")

            risk_level = prediction["predicted_class"]
            risk_name = prediction.get(f"risk_name_{lang}", prediction["risk_name_en"])
            badge_text = prediction.get(f"badge_{lang}", prediction["badge_en"])
            summary_text = prediction.get(f"summary_{lang}", prediction["summary_en"])
            color = prediction["color"]

            st.markdown(
                f"""
                <div class="risk-banner" style="background: {color};">
                    <span style="font-size: 0.9rem; letter-spacing: 1px; display: block; opacity: 0.9;">
                        {format_district_name(active_district, lang).upper()}
                    </span>
                    {risk_name} — {badge_text}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.caption(f"🛡️ **{get_text('risk_proxy_disclaimer', lang)}**")
            st.markdown(f"**{summary_text}**")

            # Compute target 3-month window and climatology metrics
            month_abbrs = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            m1 = (rain_month % 12) + 1
            m3 = ((rain_month + 2) % 12) + 1
            y1 = rain_year + (1 if rain_month >= 12 else 0)
            y3 = rain_year + (1 if rain_month >= 10 else 0)
            target_window_label = f"{month_abbrs[m1 - 1]} {y1} – {month_abbrs[m3 - 1]} {y3}"

            normal_val = float(X_df["normal_rain3"].iloc[0])
            deficit_val = float(X_df["recent_deficit"].iloc[0])
            ratio_pct = float(X_df["recent_ratio"].iloc[0]) * 100

            grid_col1, grid_col2, grid_col3, grid_col4 = st.columns(4)
            with grid_col1:
                st.metric(get_text("target_window_label", lang), target_window_label)
            with grid_col2:
                st.metric(get_text("seasonal_normal_label", lang), f"{normal_val:.1f} mm")
            with grid_col3:
                st.metric("Past 3M Rain", f"{recent_rain_mm:.1f} mm")
            with grid_col4:
                st.metric(get_text("recent_deficit_label", lang), f"{deficit_val:+.1f} mm ({ratio_pct:.0f}%)")

            # Probability breakdown
            st.markdown(f"**{get_text('chance_high_stress', lang)}**")
            st.progress(prediction["prob_high"], text=f"{prediction['prob_high']:.1%}")

            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.metric(
                    label=get_text("chance_medium_stress", lang),
                    value=f"{prediction['prob_medium']:.1%}"
                )
            with col_p2:
                st.metric(
                    label=get_text("chance_low_stress", lang),
                    value=f"{prediction['prob_low']:.1%}"
                )

            # Drivers & Climate Context
            st.markdown(f"#### 🔍 {get_text('why_title', lang)}")
            st.write(
                "- " + get_text("rainfall_driver", lang).format(
                    rain=recent_rain_mm,
                    pct=rain_percentile * 100
                )
            )
            st.write(
                "- " + get_text("oni_driver", lang).format(
                    oni=current_oni,
                    state=enso_label_en,
                    delta=oni_delta
                )
            )
            st.write(
                f"- 🌐 **{get_text('historical_oni_scenario_label', lang)}:** "
                f"{prediction.get(f'scenario_notice_{lang}', prediction['scenario_notice_en'])}"
            )

            # Uncertainty assessment
            u_label = prediction.get(f"uncertainty_label_{lang}", prediction["uncertainty_label_en"])
            u_desc = prediction.get(f"uncertainty_desc_{lang}", prediction["uncertainty_desc_en"])
            st.info(f"**{get_text('uncertainty_badge', lang)}:** {u_label} — *{u_desc}*")
            st.caption(
                f"📅 Model Version: `{model_metadata.get('model_version', 'v2.0.0-real-ml')}` | "
                f"Training Window: {model_metadata.get('training_period', '2005-2019')} | "
                f"Target: {model_metadata.get('target_definition', '3-month forward deficit')}"
            )

        with col_air:
            st.subheader(f"🍃 {get_text('air_section_title', lang)}")

            us_aqi_val = air_quality["us_aqi"]
            eu_aqi_val = air_quality["european_aqi"]
            us_color = air_quality["us_aqi_color"]
            us_bg = air_quality["us_aqi_bg"]
            us_cat_name = air_quality.get(f"us_aqi_category_{lang}", air_quality["us_aqi_category_en"])
            eu_cat_name = air_quality.get(f"european_aqi_category_{lang}", air_quality["european_aqi_category_en"])
            eu_color = air_quality["european_aqi_color"]

            col_us, col_eu = st.columns(2)
            with col_us:
                st.markdown(
                    f"""
                    <div style="background:{us_bg}; border: 2px solid {us_color}; border-radius: 10px; padding: 12px 14px; text-align: center;">
                        <div style="font-size: 0.8rem; font-weight: 700; color: #475569;">
                            {get_text('us_aqi_card_label', lang)}
                        </div>
                        <div style="font-size: 2.2rem; font-weight: 800; color: {us_color}; line-height: 1.1;">
                            {us_aqi_val if us_aqi_val is not None else 'N/A'}
                        </div>
                        <div style="font-size: 0.95rem; font-weight: 600; color: {us_color};">
                            {us_cat_name}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with col_eu:
                st.markdown(
                    f"""
                    <div style="background:#f8fafc; border: 2px solid {eu_color}; border-radius: 10px; padding: 12px 14px; text-align: center;">
                        <div style="font-size: 0.8rem; font-weight: 700; color: #475569;">
                            {get_text('eu_aqi_card_label', lang)}
                        </div>
                        <div style="font-size: 2.2rem; font-weight: 800; color: {eu_color}; line-height: 1.1;">
                            {eu_aqi_val if eu_aqi_val is not None else 'N/A'}
                        </div>
                        <div style="font-size: 0.95rem; font-weight: 600; color: {eu_color};">
                            {eu_cat_name}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            p1, p2, p3 = st.columns(3)
            with p1:
                st.metric("PM2.5", f"{air_quality['pm2_5']} µg/m³" if air_quality['pm2_5'] is not None else "N/A")
            with p2:
                st.metric("PM10", f"{air_quality['pm10']} µg/m³" if air_quality['pm10'] is not None else "N/A")
            with p3:
                st.metric("Ozone", f"{air_quality['ozone']} µg/m³" if air_quality['ozone'] is not None else "N/A")

            st.markdown(f"**{get_text('aqi_health_header', lang)}:**")
            st.write(air_quality.get(f"us_aqi_advice_{lang}", air_quality["us_aqi_advice_en"]))
            st.caption(f"🛡️ {get_text('aqi_disclaimer', lang)}")

        st.markdown("---")
        st.subheader(f"🛡️ {get_text('citizen_actions_title', lang)}")
        st.markdown(f"*{get_text('citizen_actions_subtitle', lang)}*")

        recommendations = get_water_recommendations(risk_level, lang=lang)
        rec_cols = st.columns(len(recommendations))
        for i, (col, rec) in enumerate(zip(rec_cols, recommendations), 1):
            with col:
                st.markdown(
                    f"""
                    <div class="metric-card" style="height: 100%;">
                        <div style="font-size: 1.1rem; font-weight: 700; color: #1e3a8a; margin-bottom: 8px;">
                            #{i}
                        </div>
                        <div style="font-size: 0.95rem; color: #334155; line-height: 1.4;">
                            {rec}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # District-specific El Niño Precautions Playbook
        render_el_nino_precautions_section(lang, key_suffix="district")

# ================= TAB 2: INTERACTIVE DISTRICT MAP =================
with tab2:
    if is_all_mode:
        if lang == "en":
            map_heading = "Telangana Statewide 33-Districts Map"
        elif lang == "te":
            map_heading = "తెలంగాణ రాష్ట్ర వ్యాప్త 33 జిల్లాల పటం"
        else:
            map_heading = "तेलंगाना राज्यव्यापी 33 जिलों का मानचित्र"
        st.subheader(f"🗺️ {map_heading}")
    else:
        st.subheader(f"🗺️ {format_district_name(active_district, lang)} — {get_text('tab_map', lang)}")
    st.info(f"💡 {get_text('map_instructions', lang)}")

    # Map visualization theme selector
    col_style, _ = st.columns([2.5, 1.5])
    with col_style:
        if lang == "en":
            style_opts = ["🌈 District Administrative Atlas", "⚠️ Rainfall-Deficit Alert Colors"]
        elif lang == "te":
            style_opts = ["🌈 జిల్లా అడ్మినిస్ట్రేటివ్ అట్లాస్", "⚠️ వర్షపాత లోటు హెచ్చరిక రంగులు"]
        else:
            style_opts = ["🌈 जिला प्रशासनिक एटलस", "⚠️ वर्षा-घाटा अलर्ट रंग"]
        
        sel_style = st.radio(
            "Map Color Palette" if lang == "en" else ("పటం రంగుల శైలి" if lang == "te" else "मानचित्र रंग शैली"),
            options=style_opts,
            index=0,
            horizontal=True,
            key="map_palette_mode"
        )
        color_mode = "atlas" if sel_style == style_opts[0] else "alert"

    if telangana_geo:
        # Pass color_mode and active language to ensure full multilingual labeling
        fig_map = render_telangana_interactive_map(
            geojson_data=telangana_geo,
            selected_district=active_district,
            district_risks=district_risk_dict,
            lang=lang,
            color_mode=color_mode
        )

        # Plotly chart with click-to-select support
        map_selection = st.plotly_chart(
            fig_map,
            use_container_width=True,
            on_select="rerun",
            selection_mode="points",
            key="tg_interactive_map"
        )

        # Check if user clicked on any district on the map
        if map_selection and "selection" in map_selection and "points" in map_selection["selection"]:
            pts = map_selection["selection"]["points"]
            if pts:
                clicked_pt = pts[0]
                clicked_location = clicked_pt.get("location")
                if clicked_location:
                    clicked_official = normalize_district_name(clicked_location)
                    if clicked_official != active_district:
                        st.session_state["selected_district"] = clicked_official
                        st.session_state["_sync_district_dropdown"] = True
                        st.rerun()

        c_bot1, c_bot2 = st.columns([1.2, 2.8])
        with c_bot1:
            if not is_all_mode:
                btn_lbl = "🌟 " + ("View All Districts" if lang == "en" else ("అన్ని జిల్లాలు చూపించు" if lang == "te" else "सभी जिले दिखाएं"))
                if st.button(btn_lbl, key="btn_show_all_map"):
                    st.session_state["selected_district"] = "ALL"
                    st.session_state["_sync_district_dropdown"] = True
                    st.rerun()
            else:
                success_lbl = "✅ " + (
                    "All 33 districts colored according to alert levels"
                    if lang == "en"
                    else ("అన్ని 33 జిల్లాలకు హెచ్చరిక రంగులు వర్తింపజేయబడ్డాయి" if lang == "te" else "सभी 33 जिलों को अलर्ट स्तर के अनुसार रंगा गया है")
                )
                st.success(success_lbl)

        with c_bot2:
            r_name = prediction.get(f"risk_name_{lang}", prediction["risk_name_en"])
            if not is_all_mode:
                if lang == "en":
                    inspect_txt = f"Currently inspecting: **{format_district_name(active_district, lang)}** | 3-Month Risk Category: **{r_name}**"
                elif lang == "te":
                    inspect_txt = f"ప్రస్తుత పరిశీలన: **{format_district_name(active_district, lang)}** | 3 నెలల ప్రమాద స్థితి: **{r_name}**"
                else:
                    inspect_txt = f"वर्तमान में चयनित: **{format_district_name(active_district, lang)}** | 3-माह जोखिम श्रेणी: **{r_name}**"
                st.caption(inspect_txt)
            else:
                if lang == "en":
                    all_caption = "All 33 districts are colored according to their model-predicted alert levels. District names are labeled directly inside each boundary outline."
                elif lang == "te":
                    all_caption = "అన్ని 33 జిల్లాలు మోడల్ అంచనా వేసిన హెచ్చరిక స్థాయిల ప్రకారం రంగులు వేయబడ్డాయి. సరిహద్దుల లోపలే జిల్లాల పేర్లు స్పష్టంగా కనిపిస్తాయి."
                else:
                    all_caption = "सभी 33 जिलों को मॉडल द्वारा अनुमानित अलर्ट स्तर के अनुसार रंगा गया है। प्रत्येक सीमा के अंदर जिले का नाम स्पष्ट रूप से अंकित है।"
                st.caption(all_caption)

        # ================= DISTRICT-WISE MANDALS AND RIVER-TO-MANDAL DIRECTORY =================
        st.markdown("---")
        
        # Determine district to display for water resources directory
        if not is_all_mode:
            target_district = active_district
        else:
            # When in statewide overview, provide an intuitive district picker
            c_sel_hdr, c_sel_box = st.columns([1.5, 2.5])
            with c_sel_hdr:
                st.markdown(
                    f"#### 🔍 {get_text('mandals_rivers_header', lang)}"
                )
            with c_sel_box:
                target_district = st.selectbox(
                    get_text("district_select_label", lang),
                    options=EXACT_33_DISTRICTS,
                    index=0,
                    key="tab2_district_water_picker"
                )

        # Calculate verified district water summary metrics
        water_summary = get_district_water_summary(target_district)

        # 1. District Heading & Subtitle
        st.markdown(
            f"""
            <div style="margin-top: 10px; margin-bottom: 16px;">
                <h3 style="margin: 0; color: #f8fafc; font-size: 1.4rem;">
                    📍 {format_district_name(target_district, lang)} — {get_text('mandals_rivers_header', lang)}
                </h3>
                <p style="margin: 4px 0 0 0; color: #94a3b8; font-size: 0.9rem;">
                    {get_text('mandals_rivers_sub', lang)}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # 2. Key Metric Cards (Total Mandals, Unique Rivers, River-to-Mandal Associations)
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.markdown(
                f"""
                <div class="metric-card" style="text-align: center; border-left: 4px solid #38bdf8;">
                    <div style="font-size: 0.85rem; font-weight: 700; color: #94a3b8; text-transform: uppercase;">
                        🏛️ {get_text('total_mandals_card', lang)}
                    </div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #38bdf8; margin: 4px 0;">
                        {water_summary['total_mandals']}
                    </div>
                    <div style="font-size: 0.8rem; color: #64748b;">
                        {"Official Revenue Mandals" if lang == "en" else ("అధికారిక రెవెన్యూ మండలాలు" if lang == "te" else "आधिकारिक राजस्व मंडल")}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with m_col2:
            st.markdown(
                f"""
                <div class="metric-card" style="text-align: center; border-left: 4px solid #10b981;">
                    <div style="font-size: 0.85rem; font-weight: 700; color: #94a3b8; text-transform: uppercase;">
                        🌊 {get_text('unique_rivers_card', lang)}
                    </div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #10b981; margin: 4px 0;">
                        {water_summary['unique_river_count']}
                    </div>
                    <div style="font-size: 0.8rem; color: #64748b;">
                        {"Distinct Verified River Basins/Streams" if lang == "en" else ("ప్రత్యేక నదులు & ఉపనదులు" if lang == "te" else "विशिष्ट सत्यापित नदियां / धाराएं")}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with m_col3:
            st.markdown(
                f"""
                <div class="metric-card" style="text-align: center; border-left: 4px solid #f59e0b;">
                    <div style="font-size: 0.85rem; font-weight: 700; color: #94a3b8; text-transform: uppercase;">
                        🔗 {get_text('river_associations_card', lang)}
                    </div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #f59e0b; margin: 4px 0;">
                        {water_summary['river_mandal_associations_count']}
                    </div>
                    <div style="font-size: 0.8rem; color: #64748b;">
                        {"Verified River–Mandal Pairs" if lang == "en" else ("నది-మండల సంబంధిత జంటలు" if lang == "te" else "सत्यापित नदी–मंडल युग्म")}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        # 3. River Directory & Exact Mandals Table
        st.markdown(f"#### 🌊 {get_text('river_table_title', lang)}")
        
        rivers_data = water_summary.get("rivers", [])
        if rivers_data:
            river_table_rows = []
            for r in rivers_data:
                mandals_str = ", ".join(r["mandals"]) if r["mandals"] else "Catchment basin"
                river_table_rows.append({
                    "River Name": r["river_name"],
                    "River Basin": r["basin"],
                    f"Mandals in {target_district}": mandals_str,
                    "Relationship": r["relationship"],
                    "Authoritative Source": r["source_url"]
                })
            df_rivers = pd.DataFrame(river_table_rows)
            st.dataframe(
                df_rivers,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "River Name": st.column_config.TextColumn("River Name", width="medium"),
                    "River Basin": st.column_config.TextColumn("River Basin", width="small"),
                    f"Mandals in {target_district}": st.column_config.TextColumn(f"Mandals in {target_district}", width="large"),
                    "Relationship": st.column_config.TextColumn("Relationship", width="medium"),
                    "Authoritative Source": st.column_config.LinkColumn("Authoritative Source", width="medium")
                }
            )
        else:
            st.info(get_text("no_rivers_notice", lang))

        # 4. Searchable Mandal Directory
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.markdown(f"#### 🏛️ {get_text('total_mandals_card', lang)} ({water_summary['total_mandals']})")
        
        m_search_query = st.text_input(
            f"🔍 {get_text('mandal_search_label', lang).format(district=target_district)}",
            placeholder="Search by mandal name, river, or reservoir...",
            key=f"search_mandal_{target_district}"
        )

        mandal_table_rows = get_mandal_directory_table(target_district, search_query=m_search_query)
        if mandal_table_rows:
            clean_mandal_rows = []
            for m_row in mandal_table_rows:
                clean_mandal_rows.append({
                    "Mandal": m_row["Mandal"],
                    "Parent District": m_row["Parent District"],
                    "Verified Rivers & Classification": m_row["Verified Rivers & Relationship"],
                    "Water Infrastructure & Assets": m_row["Key Water Assets & Infrastructure"]
                })
            df_mandals = pd.DataFrame(clean_mandal_rows)
            st.dataframe(
                df_mandals,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Mandal": st.column_config.TextColumn("Mandal", width="medium"),
                    "Parent District": st.column_config.TextColumn("Parent District", width="small"),
                    "Verified Rivers & Classification": st.column_config.TextColumn("Verified Rivers & Classification", width="large"),
                    "Water Infrastructure & Assets": st.column_config.TextColumn("Water Infrastructure & Assets", width="large")
                }
            )
        else:
            st.warning(f"No mandals matching query '{m_search_query}' in {target_district}.")

        # 5. Selected Mandal Deep-Dive Water Profile
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.markdown(f"#### 🔍 {get_text('mandal_select_label', lang)}")
        
        selected_mandal = st.selectbox(
            "Choose a Mandal to inspect local water assets:",
            options=water_summary["mandals"],
            index=0,
            key=f"mandal_deepdive_select_{target_district}"
        )

        if selected_mandal:
            m_profile = get_mandal_detailed_profile(target_district, selected_mandal)
            
            p_rivers = m_profile.get("rivers", [])
            p_res = m_profile.get("reservoirs", [])
            p_lift = m_profile.get("lift_schemes", [])
            p_gw = m_profile.get("groundwater_stations", [])

            st.markdown(
                f"""
                <div style="background: #1e293b; border: 1px solid #334155; border-radius: 10px; padding: 16px; margin-top: 8px;">
                    <div style="font-size: 1.15rem; font-weight: 700; color: #38bdf8; margin-bottom: 8px;">
                        📌 {get_text('mandal_profile_title', lang).format(mandal=selected_mandal)} ({target_district})
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            c_p1, c_p2 = st.columns(2)
            with c_p1:
                st.markdown("**🌊 Verified River Connections:**")
                if p_rivers:
                    for riv in p_rivers:
                        st.markdown(
                            f"- **{riv['river_name']}** ({riv['basin']}) — *{riv['relationship']}*\n"
                            f"  *Notes:* {riv['notes']} | [Official Source]({riv['source_url']})"
                        )
                else:
                    st.write("No major rivers cross this mandal directly; served by local minor streams and tank chains.")

            with c_p2:
                st.markdown("**🏗️ Local Water Assets & Infrastructure:**")
                has_any_asset = False
                if p_res:
                    has_any_asset = True
                    for r in p_res:
                        st.markdown(f"- 🚰 **Dam/Reservoir:** {r['name']} ({r.get('type', '')}) — *Capacity: {r.get('capacity_tmc', 'N/A')} TMC* [Source]({r['source_url']})")
                if p_lift:
                    has_any_asset = True
                    for l in p_lift:
                        st.markdown(f"- ⚡ **Lift Irrigation/Barrage:** {l['name']} ({l.get('type', '')}) [Source]({l['source_url']})")
                if p_gw:
                    has_any_asset = True
                    for g in p_gw:
                        st.markdown(f"- 📊 **Groundwater Station:** {g['station_name']} — *Depth to Water: {g.get('water_level_mbgl', 'N/A')}* [Status: {g.get('status', 'Safe')}] [Source]({g['source_url']})")
                
                if not has_any_asset:
                    st.write("Mission Kakatiya minor irrigation tanks and local groundwater extraction.")

        # 6. Additional District Water Infrastructure Sections
        infra = get_district_infrastructure(target_district)
        res_list = infra.get("reservoirs", [])
        lift_list = infra.get("lift_irrigation", [])
        gw_list = infra.get("groundwater_stations", [])

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        st.markdown(f"#### 🏗️ Water Infrastructure & Monitoring Directory for {target_district}")

        with st.expander(f"🌊 {get_text('reservoirs_dams_title', lang)} ({len(res_list)})", expanded=True):
            if res_list:
                df_res = pd.DataFrame(res_list)
                st.dataframe(
                    df_res,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "name": st.column_config.TextColumn("Asset Name", width="medium"),
                        "mandal": st.column_config.TextColumn("Mandal", width="small"),
                        "type": st.column_config.TextColumn("Category", width="medium"),
                        "capacity_tmc": st.column_config.TextColumn("Capacity (TMC)", width="small"),
                        "purpose": st.column_config.TextColumn("Purpose", width="medium"),
                        "source_url": st.column_config.LinkColumn("Official Reference", width="medium"),
                        "date": st.column_config.TextColumn("Record Date", width="small")
                    }
                )
            else:
                st.write(f"No major irrigation storage reservoirs recorded in {target_district}; served by inter-district canal distribution.")

        with st.expander(f"⚡ {get_text('lift_irrigation_title', lang)} ({len(lift_list)})", expanded=True):
            if lift_list:
                df_lift = pd.DataFrame(lift_list)
                st.dataframe(
                    df_lift,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "name": st.column_config.TextColumn("Project / Scheme Name", width="medium"),
                        "mandal": st.column_config.TextColumn("Mandal", width="small"),
                        "type": st.column_config.TextColumn("Project Type", width="medium"),
                        "river": st.column_config.TextColumn("River Source Link", width="medium"),
                        "source_url": st.column_config.LinkColumn("Official Reference", width="medium"),
                        "date": st.column_config.TextColumn("Record Date", width="small")
                    }
                )
            else:
                st.write(f"No major lift irrigation pump stations located in {target_district}; served by gravity canal networks.")

        with st.expander(f"🚰 {get_text('groundwater_stations_title', lang)} ({len(gw_list)})", expanded=True):
            if gw_list:
                df_gw = pd.DataFrame(gw_list)
                st.dataframe(
                    df_gw,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "station_name": st.column_config.TextColumn("Station Name", width="medium"),
                        "mandal": st.column_config.TextColumn("Mandal", width="small"),
                        "water_level_mbgl": st.column_config.TextColumn("Depth to Water Level (mbgl)", width="medium"),
                        "status": st.column_config.TextColumn("Aquifer Exploitation Category", width="medium"),
                        "source_url": st.column_config.LinkColumn("CGWB Source", width="medium"),
                        "date": st.column_config.TextColumn("Observation Date", width="small")
                    }
                )
            else:
                st.write(f"Central Ground Water Board (CGWB) observation wells being compiled for {target_district}.")
    else:
        st.warning("Telangana GeoJSON boundary asset not found in assets/telangana_districts.geojson")

# ================= TAB 3: 7-DAY WEATHER FORECAST =================
with tab3:
    st.subheader(f"🌤️ {format_district_name(active_district, lang)} — {get_text('weather_section_title', lang)}")
    st.warning(f"⚠️ {get_text('weather_synoptic_disclaimer', lang)}")

    if weather_forecast["status"] == "success":
        wf_col1, wf_col2, wf_col3, wf_col4 = st.columns(4)
        with wf_col1:
            st.metric(get_text("temp_label", lang), f"{weather_forecast['temperature_2m']} °C")
        with wf_col2:
            st.metric(get_text("humidity_label", lang), f"{weather_forecast['relative_humidity_2m']} %")
        with wf_col3:
            st.metric(get_text("wind_label", lang), f"{weather_forecast['wind_speed_10m']} km/h")
        with wf_col4:
            st.metric(get_text("current_precip_label", lang), f"{weather_forecast['precipitation_mm']} mm")

        st.markdown("#### 📅 7-Day Synoptic Outlook")
        daily_days = weather_forecast.get("daily_forecast", [])
        if daily_days:
            cols = st.columns(min(len(daily_days), 7))
            for c, day in zip(cols, daily_days):
                with c:
                    d_obj = dt.date.fromisoformat(day["date"])
                    day_str = d_obj.strftime("%a, %b %d")
                    st.markdown(
                        f"""
                        <div class="weather-card">
                            <div style="font-weight: 700; font-size: 0.85rem; color: #1e293b;">{day_str}</div>
                            <div style="font-size: 1.1rem; font-weight: 800; color: #0284c7; margin: 4px 0;">
                                {day['temp_max_c']}° / {day['temp_min_c']}°
                            </div>
                            <div style="font-size: 0.8rem; color: #64748b;">
                                🌧️ {day['precip_sum_mm']} mm<br>
                                💧 {day['precip_prob_pct']}% prob
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        st.caption(f"Source: {weather_forecast['source']} ({weather_forecast['source_url']}) | Observed at {weather_forecast['timestamp']}")
    else:
        st.info("Weather forecast feed temporarily unavailable. Please retry in a few moments.")

# ================= TAB 4: MODEL & SCIENCE =================
# ================= TAB 4: CWC FLOOD & RIVER WATER LEVELS =================
with tab4:
    st.subheader(f"🌊 {get_text('cwc_section_title', lang)}")
    st.markdown(f"*{get_text('cwc_section_subtitle', lang)}*")

    cwc_col1, cwc_col2 = st.columns([1.2, 0.8], gap="large")

    with cwc_col1:
        basin_name = DISTRICT_BASIN_MAP.get(active_district, "Godavari Basin")
        st.markdown(
            f"""
            <div class="metric-card" style="border-left: 5px solid #0284c7;">
                <div style="font-size: 0.85rem; font-weight: 700; color: #64748b; text-transform: uppercase;">
                    {get_text('cwc_basin_label', lang)}
                </div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #0f172a; margin-top: 4px;">
                    {basin_name}
                </div>
                <div style="font-size: 0.95rem; color: #475569; margin-top: 6px;">
                    {format_district_name(active_district, lang)} falls under the <b>{basin_name}</b> drainage and inflow monitoring system.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.link_button(
            f"🔗 {get_text('cwc_portal_btn', lang)}",
            CWC_FFS_PORTAL_URL,
            type="primary"
        )

    with cwc_col2:
        st.markdown(
            """
            <div class="metric-card">
                <div style="font-weight: 700; font-size: 0.95rem; color: #1e3a8a; margin-bottom: 6px;">
                    CWC Flood Stage Benchmarks
                </div>
                <div style="font-size: 0.85rem; color: #334155; line-height: 1.5;">
                    🟢 <b>Normal:</b> River level within safe embankments.<br>
                    🟡 <b>Warning Level:</b> River nearing flood stage; alertness advised.<br>
                    🟠 <b>Danger Level:</b> River in flood; inundation of low-lying floodplains.<br>
                    🔴 <b>Extreme Situation:</b> Water level exceeding historical High Flood Level (HFL).
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown(f"#### 📍 {get_text('cwc_stations_header', lang).format(district=format_district_name(active_district, lang))}")

    stations = get_cwc_stations_for_district(active_district)
    if stations:
        s_cols = st.columns(len(stations)) if len(stations) <= 3 else st.columns(3)
        for idx, stn in enumerate(stations):
            col_target = s_cols[idx % len(s_cols)]
            with col_target:
                river_display = stn['river_te'] if lang == 'te' else stn['river']
                name_display = stn['station_name_te'] if lang == 'te' else stn['station_name']
                st.markdown(
                    f"""
                    <div class="metric-card" style="height: 100%;">
                        <div style="font-size: 1.15rem; font-weight: 800; color: #0369a1;">
                            {name_display}
                        </div>
                        <div style="font-size: 0.85rem; color: #64748b; font-weight: 600; margin-bottom: 6px;">
                            River: {river_display} ({stn['basin']})
                        </div>
                        <div style="font-size: 0.85rem; color: #334155;">
                            • <b>{get_text('cwc_warning_level', lang)}:</b> {stn['warning_level_m']} m ({stn['warning_level_m'] * 3.28084:.1f} ft)<br>
                            • <b>{get_text('cwc_danger_level', lang)}:</b> {stn['danger_level_m']} m ({stn['danger_level_m'] * 3.28084:.1f} ft)<br>
                            • <b>{get_text('cwc_hfl_level', lang)}:</b> {stn['hfl_m']} m ({stn['hfl_m'] * 3.28084:.1f} ft)
                        </div>
                        <div style="font-size: 0.8rem; color: #64748b; margin-top: 8px; font-style: italic;">
                            {stn['description']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info("No dedicated CWC forecasting gauges registered in this immediate municipal boundary; check regional river basin gauges.")

    st.caption(f"🛡️ {get_text('cwc_authority_notice', lang)}")

# ================= TAB 5: MODEL & SCIENCE =================
with tab5:
    st.subheader(f"🔬 {get_text('model_comparison_title', lang)}")
    st.markdown(get_text("model_comparison_intro", lang))

    meta_without = model_metadata.get("metrics_without_oni", {})
    meta_with = model_metadata.get("metrics_with_oni", {})
    f1_without = meta_without.get("macro_f1", 0.3813)
    f1_with = meta_with.get("macro_f1", 0.4458)
    acc_without = meta_without.get("accuracy", 0.4200)
    acc_with = meta_with.get("accuracy", 0.5043)
    f1_diff = model_metadata.get("macro_f1_difference", f1_with - f1_without)
    rel_gain = model_metadata.get("macro_f1_relative_gain_pct", 16.92)
    test_period = model_metadata.get("test_period", "2020-01-01 to 2026-06-01")
    train_period = model_metadata.get("training_period", "2005-01-01 to 2019-09-01 (embargoed)")
    test_samples = model_metadata.get("test_samples_count", 2574)
    train_samples = model_metadata.get("train_samples_count", 5478)
    class_dist = model_metadata.get("test_class_distribution", {"Low": 1609, "Medium": 240, "High": 725})
    feature_imps = model_metadata.get("feature_importances", {})
    cm_without = meta_without.get("confusion_matrix", [[495, 567, 547], [36, 90, 114], [128, 101, 496]])
    cm_with = meta_with.get("confusion_matrix", [[587, 380, 642], [32, 88, 120], [51, 51, 623]])
    per_class_without = meta_without.get("per_class", {})
    per_class_with = meta_with.get("per_class", {})
    limitations = model_metadata.get("known_limitations", [])

    # 1. Executive Metrics Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(
            label="Model B (With ONI) Macro-F1",
            value=f"{f1_with:.4f}",
            delta=f"Accuracy: {acc_with:.1%}"
        )
    with c2:
        st.metric(
            label="Model A (Without ONI) Macro-F1",
            value=f"{f1_without:.4f}",
            delta=f"Accuracy: {acc_without:.1%}",
            delta_color="inverse"
        )
    with c3:
        st.metric(
            label="Macro-F1 Difference",
            value=f"{f1_diff:+.4f}",
            delta=f"+{rel_gain:.1f}% relative gain"
        )
    with c4:
        st.metric(
            label="Test Evaluation Samples",
            value=f"{test_samples:,}",
            delta=f"33 Districts ({test_period})"
        )

    # 2. Honest Finding Callout
    st.success(
        f"**Empirical Evaluation Result:** Incorporating NOAA ONI Pacific sea surface temperature signals "
        f"increases balanced Macro-F1 from **{f1_without:.4f}** to **{f1_with:.4f}** (an absolute difference of **{f1_diff:+.4f}**, "
        f"representing a **+{rel_gain:.1f}%** relative gain). "
        f"Crucially, High-deficit recall increases from **68.4%** to **85.9%**, significantly enhancing early warnings "
        f"for severe dry seasons across Telangana districts. Transitional Medium-deficit precision remains lower (17.0%) "
        f"due to severe class imbalance (only 9.3% of historical periods)."
        if lang == "en" else
        f"**వాస్తవ పరిశీలనా ఫలితం:** పసిఫిక్ సముద్ర ఉష్ణోగ్రత సూచిక (ONI) చేర్చడం ద్వారా మోడల్ సమతుల్య Macro-F1 స్కోరు "
        f"**{f1_without:.4f}** నుండి **{f1_with:.4f}** కు పెరిగింది (నికర వ్యత్యాసం: **{f1_diff:+.4f}**, **+{rel_gain:.1f}%** పెరుగుదల). "
        f"ప్రత్యేకంగా తీవ్ర వర్షపాత లోటును (High Deficit) గుర్తించే సామర్థ్యం 68.4% నుండి 85.9% కు మెరుగైంది."
    )

    # 3. Class Distribution & Sample Counts
    st.markdown("---")
    st.markdown("#### 📊 Dataset Partitions & Test Class Imbalance")
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <b>Chronological Splitting (Anti-Data Leakage):</b><br>
                • <b>Training Period:</b> {train_period} (<b>{train_samples:,}</b> district-month samples)<br>
                • <b>Embargo Window:</b> 3-month lookahead separation before 2020<br>
                • <b>Test Period:</b> {test_period} (<b>{test_samples:,}</b> district-month samples across all 33 districts)<br>
                • <b>Climatological Normals:</b> Computed strictly from pre-2020 training records.
            </div>
            """,
            unsafe_allow_html=True
        )
    with d_col2:
        low_cnt = class_dist.get('Low', 1609)
        med_cnt = class_dist.get('Medium', 240)
        hi_cnt = class_dist.get('High', 725)
        st.markdown(
            f"""
            <div class="metric-card">
                <b>Out-of-Time Test Class Distribution:</b><br>
                • <b>Low Deficit (&lt;10%):</b> {low_cnt:,} ({low_cnt / test_samples:.1%})<br>
                • <b>Medium Deficit (10–25%):</b> {med_cnt:,} ({med_cnt / test_samples:.1%}) <i>[Severe Imbalance]</i><br>
                • <b>High Deficit (&ge;25%):</b> {hi_cnt:,} ({hi_cnt / test_samples:.1%})<br>
                • <b>Always-Low Majority Baseline:</b> {low_cnt / test_samples:.1%} Accuracy.
            </div>
            """,
            unsafe_allow_html=True
        )

    # 4. Detailed Per-Class Results Table
    st.markdown("---")
    st.markdown(f"#### 📋 {get_text('eval_metrics_table_title', lang)}")
    
    per_class_rows = [
        {
            "Risk Category": "Low Deficit (<10%)",
            "Test Records": f"{low_cnt:,}",
            "Model A (No ONI) Prec": f"{per_class_without.get('Low', {}).get('precision', 0):.1%}",
            "Model A Rec": f"{per_class_without.get('Low', {}).get('recall', 0):.1%}",
            "Model A F1": f"{per_class_without.get('Low', {}).get('f1', 0):.4f}",
            "Model B (With ONI) Prec": f"{per_class_with.get('Low', {}).get('precision', 0):.1%}",
            "Model B Rec": f"{per_class_with.get('Low', {}).get('recall', 0):.1%}",
            "Model B F1": f"{per_class_with.get('Low', {}).get('f1', 0):.4f}",
        },
        {
            "Risk Category": "Medium Deficit (10–25%)",
            "Test Records": f"{med_cnt:,}",
            "Model A (No ONI) Prec": f"{per_class_without.get('Medium', {}).get('precision', 0):.1%}",
            "Model A Rec": f"{per_class_without.get('Medium', {}).get('recall', 0):.1%}",
            "Model A F1": f"{per_class_without.get('Medium', {}).get('f1', 0):.4f}",
            "Model B (With ONI) Prec": f"{per_class_with.get('Medium', {}).get('precision', 0):.1%}",
            "Model B Rec": f"{per_class_with.get('Medium', {}).get('recall', 0):.1%}",
            "Model B F1": f"{per_class_with.get('Medium', {}).get('f1', 0):.4f}",
        },
        {
            "Risk Category": "High Deficit (>=25%)",
            "Test Records": f"{hi_cnt:,}",
            "Model A (No ONI) Prec": f"{per_class_without.get('High', {}).get('precision', 0):.1%}",
            "Model A Rec": f"{per_class_without.get('High', {}).get('recall', 0):.1%}",
            "Model A F1": f"{per_class_without.get('High', {}).get('f1', 0):.4f}",
            "Model B (With ONI) Prec": f"{per_class_with.get('High', {}).get('precision', 0):.1%}",
            "Model B Rec": f"{per_class_with.get('High', {}).get('recall', 0):.1%}",
            "Model B F1": f"{per_class_with.get('High', {}).get('f1', 0):.4f}",
        }
    ]
    st.dataframe(pd.DataFrame(per_class_rows), use_container_width=True, hide_index=True)

    # 5. Side-by-Side Confusion Matrices
    st.markdown("---")
    st.markdown(f"#### 🎯 {get_text('confusion_matrix_title', lang)}")
    cm_col1, cm_col2 = st.columns(2)
    
    classes = ["Low", "Medium", "High"]
    with cm_col1:
        st.markdown("**Model A: Baseline (Without ONI)**")
        df_cm_a = pd.DataFrame(
            cm_without,
            index=[f"Actual {c}" for c in classes],
            columns=[f"Pred {c}" for c in classes]
        )
        st.dataframe(df_cm_a, use_container_width=True)
        st.caption("Rows: True Class | Columns: Predicted Class")

    with cm_col2:
        st.markdown("**Model B: El Niño-Aware (With ONI)**")
        df_cm_b = pd.DataFrame(
            cm_with,
            index=[f"Actual {c}" for c in classes],
            columns=[f"Pred {c}" for c in classes]
        )
        st.dataframe(df_cm_b, use_container_width=True)
        st.caption("Rows: True Class | Columns: Predicted Class")

    # 6. Feature Importance & Explainability
    st.markdown("---")
    st.markdown(f"#### 📈 {get_text('feature_importance_title', lang)}")
    if feature_imps:
        imp_items = sorted(feature_imps.items(), key=lambda x: x[1], reverse=False)
        fig_imp = go.Figure(go.Bar(
            x=[score for _, score in imp_items],
            y=[feat for feat, _ in imp_items],
            orientation="h",
            marker=dict(
                color=["#0284c7" if "oni" not in f else "#ef4444" for f, _ in imp_items]
            )
        ))
        fig_imp.update_layout(
            title="Random Forest Feature Gini Importances (Red = Pacific ONI Signals)",
            xaxis_title="Relative Feature Importance Score",
            yaxis_title="Feature Name",
            height=460,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_imp, use_container_width=True)

    st.warning(f"⚠️ **Scientific Disclaimer:** {get_text('causation_disclaimer', lang)}")

    # 7. Documented Limitations
    st.markdown("---")
    st.markdown("#### 🛡️ Documented Scientific Limitations")
    for lim in limitations:
        st.markdown(f"• {lim}")

    # 8. ENSO Educational Context
    st.markdown("---")
    st.markdown(f"#### 🌊 {get_text('elnino_explanation_title', lang)}")
    st.write(get_text("elnino_explanation_body", lang))
    st.caption(
        f"NOAA ONI Dataset: {oni_metadata.get('version')} | "
        f"Observation Range: {oni_metadata.get('first_period')} to {oni_metadata.get('latest_period')} | "
        f"Official NOAA Portal: {oni_metadata.get('source_page')}"
    )

    # 9. Practical El Niño Precautionary Playbook
    render_el_nino_precautions_section(lang, key_suffix="science")

# ================= TAB 6: ABOUT & DISCLAIMERS =================
with tab6:
    st.subheader(f"ℹ️ {get_text('disclaimer_title', lang)}")
    st.caption("Research & Decision-Support Prototype • Not an Official Government Portal • Swachh & Sustainable Bharat")
    st.markdown(get_text("disclaimer_text", lang))

    st.markdown("---")
    st.caption(f"🛡️ {get_text('source_attribution', lang)}")
