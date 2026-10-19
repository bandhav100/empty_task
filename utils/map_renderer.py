"""Interactive SVG Choropleth Map for Telangana 33 Administrative Districts.
Strictly isolated Telangana state map, with all 33 districts named inside
their boundary outlines and colored according to user's choice:
1. Vibrant District Atlas Palette (matching the official Telangana administrative map)
2. Early Warning Alert Levels (Rainfall Deficit Risk: Green / Amber / Red)

Fully supports multilingual dynamic labeling in English, Telugu (తెలుగు), and Hindi (हिंदी).
"""

from typing import Dict, Any, Optional
import plotly.graph_objects as go
from utils.districts import (
    DISTRICTS,
    EXACT_33_DISTRICTS,
    DISTRICT_TELUGU,
    DISTRICT_HINDI,
    get_internal_id,
    normalize_district_name
)

# Geographic center for Telangana State
TELANGANA_CENTER = {"lat": 17.8748, "lon": 79.1008}

# Accessible alert color scheme
RISK_COLOR_MAP = {
    "Low Risk": "#2e7d32",          # Forest Emerald Green
    "Medium Risk": "#f57f17",       # Warm Amber
    "High Risk": "#c62828",         # Deep Crimson Red
    "Data Unavailable": "#64748b",  # Slate Grey
}

# Distinct vibrant administrative palette matching the Telangana State District Map
DISTRICT_ATLAS_COLORS: Dict[str, str] = {
    "Adilabad": "#60a5fa",                # sky blue
    "Kumuram Bheem": "#fef08a",           # bright yellow
    "Nirmal": "#cffafe",                  # pale cyan
    "Mancherial": "#1d4ed8",              # deep royal blue
    "Nizamabad": "#c084fc",               # vibrant lavender purple
    "Jagtial": "#84cc16",                 # bright lime green
    "Peddapalli": "#2dd4bf",              # mint cyan
    "Kamareddy": "#fb7185",               # coral red
    "Rajanna Sircilla": "#ca8a04",        # warm olive
    "Karimnagar": "#facc15",              # bright yellow
    "Jayashankar Bhupalpally": "#4ade80", # neon light green
    "Mulugu": "#60a5fa",                  # cornflower blue
    "Medak": "#0284c7",                   # steel blue
    "Siddipet": "#06b6d4",                # cyan
    "Sangareddy": "#15803d",              # deep forest green
    "Hanumakonda": "#3b82f6",             # vibrant blue
    "Warangal": "#22c55e",                # emerald green
    "Jangaon": "#f97316",                 # coral orange
    "Mahabubabad": "#e879f9",             # orchid pink
    "Bhadradri Kothagudem": "#a3e635",    # bright lime green
    "Medchal-Malkajgiri": "#ef4444",      # bright crimson red
    "Hyderabad": "#ede9fe",               # soft white lavender
    "Yadadri Bhuvanagiri": "#fb923c",     # orange
    "Rangareddy": "#facc15",              # golden yellow
    "Vikarabad": "#14b8a6",               # turquoise teal
    "Nalgonda": "#f43f5e",                # rose pink
    "Suryapet": "#ea580c",                # fiery orange
    "Khammam": "#38bdf8",                 # royal sky blue
    "Mahabubnagar": "#2563eb",            # royal blue
    "Narayanpet": "#d97706",              # amber brown
    "Wanaparthy": "#06b6d4",              # bright cyan
    "Nagarkurnool": "#22c55e",            # lawn green
    "Jogulamba Gadwal": "#eab308"         # golden yellow
}

# Full official district display names matching the reference map
CLEAN_DISTRICT_MAP_LABELS = {
    "en": {
        "Adilabad": "Adilabad",
        "Bhadradri Kothagudem": "Bhadradri Kothagudem",
        "Hanumakonda": "Hanumakonda",
        "Hyderabad": "Hyderabad",
        "Jagtial": "Jagtial",
        "Jangaon": "Jangaon",
        "Jayashankar Bhupalpally": "Jayashankar Bhupalpally",
        "Jogulamba Gadwal": "Jogulamba Gadwal",
        "Kamareddy": "Kamareddy",
        "Karimnagar": "Karimnagar",
        "Khammam": "Khammam",
        "Kumuram Bheem": "Kumuram Bheem Asifabad",
        "Mahabubabad": "Mahabubabad",
        "Mahabubnagar": "Mahabubnagar",
        "Mancherial": "Mancherial",
        "Medak": "Medak",
        "Medchal-Malkajgiri": "Medchal Malkajgiri",
        "Mulugu": "Mulugu",
        "Nagarkurnool": "Nagarkurnool",
        "Nalgonda": "Nalgonda",
        "Narayanpet": "Narayanpet",
        "Nirmal": "Nirmal",
        "Nizamabad": "Nizamabad",
        "Peddapalli": "Peddapalli",
        "Rajanna Sircilla": "Rajanna Sircilla",
        "Rangareddy": "Rangareddy",
        "Sangareddy": "Sangareddy",
        "Siddipet": "Siddipet",
        "Suryapet": "Suryapet",
        "Vikarabad": "Vikarabad",
        "Wanaparthy": "Wanaparthy",
        "Warangal": "Warangal",
        "Yadadri Bhuvanagiri": "Yadadri Bhuvanagiri"
    },
    "te": {
        "Adilabad": "ఆదిలాబాద్",
        "Bhadradri Kothagudem": "భద్రాద్రి కొత్తగూడెం",
        "Hanumakonda": "హనుమకొండ",
        "Hyderabad": "హైదరాబాద్",
        "Jagtial": "జగిత్యాల",
        "Jangaon": "జనగాం",
        "Jayashankar Bhupalpally": "జయశంకర్ భూపాలపల్లి",
        "Jogulamba Gadwal": "జోగులాంబ గద్వాల",
        "Kamareddy": "కామారెడ్డి",
        "Karimnagar": "కరీంనగర్",
        "Khammam": "ఖమ్మం",
        "Kumuram Bheem": "కుమురం భీమ్ ఆసిఫాబాద్",
        "Mahabubabad": "మహబూబాబాద్",
        "Mahabubnagar": "మహబూబ్‌నగర్",
        "Mancherial": "మంచిర్యాల",
        "Medak": "మెదక్",
        "Medchal-Malkajgiri": "మేడ్చల్ మల్కాజ్‌గిరి",
        "Mulugu": "ములుగు",
        "Nagarkurnool": "నాగర్‌కర్నూల్",
        "Nalgonda": "నల్గొండ",
        "Narayanpet": "నారాయణపేట",
        "Nirmal": "నిర్మల్",
        "Nizamabad": "నిజామాబాద్",
        "Peddapalli": "పెద్దపల్లి",
        "Rajanna Sircilla": "రాజన్న సిరిసిల్ల",
        "Rangareddy": "రంగారెడ్డి",
        "Sangareddy": "సంగారెడ్డి",
        "Siddipet": "సిద్దిపేట",
        "Suryapet": "సూర్యాపేట",
        "Vikarabad": "వికారాబాద్",
        "Wanaparthy": "వనపర్తి",
        "Warangal": "వరంగల్",
        "Yadadri Bhuvanagiri": "యాదాద్రి భువనగిరి"
    },
    "hi": {
        "Adilabad": "आदिलाबाद",
        "Bhadradri Kothagudem": "भद्राद्री कोठागुडेम",
        "Hanumakonda": "हनुमकोंडा",
        "Hyderabad": "हैदराबाद",
        "Jagtial": "जगित्याल",
        "Jangaon": "जनगांव",
        "Jayashankar Bhupalpally": "जयशंकर भूपालपल्ली",
        "Jogulamba Gadwal": "जोगुलाम्बा गडवाल",
        "Kamareddy": "कामारेड्डी",
        "Karimnagar": "करीमनगर",
        "Khammam": "खम्मम",
        "Kumuram Bheem": "कुमुराम भीम आसिफाबाद",
        "Mahabubabad": "महबूबाबाद",
        "Mahabubnagar": "महबूबनगर",
        "Mancherial": "मंचिरियाल",
        "Medak": "मेदक",
        "Medchal-Malkajgiri": "मेदचल मलकाजगिरी",
        "Mulugu": "मुलुगु",
        "Nagarkurnool": "नागरकुरनूल",
        "Nalgonda": "नलगोंडा",
        "Narayanpet": "नारायणपेट",
        "Nirmal": "निर्मल",
        "Nizamabad": "निजामाबाद",
        "Peddapalli": "पेद्दापल्ली",
        "Rajanna Sircilla": "राजन्ना सिरसिल्ला",
        "Rangareddy": "रंगारेड्डी",
        "Sangareddy": "संगारेड्डी",
        "Siddipet": "सिद्दिपेट",
        "Suryapet": "सूर्यापेट",
        "Vikarabad": "विकाराबाद",
        "Wanaparthy": "वनपर्ती",
        "Warangal": "वारंगल",
        "Yadadri Bhuvanagiri": "यादाद्री भुवनगिरी"
    }
}

def get_district_display_label(name: str, lang: str = "en") -> str:
    """Returns official label for polygon labeling in English, Telugu, or Hindi."""
    custom = CLEAN_DISTRICT_MAP_LABELS.get(lang, {}).get(name)
    if custom:
        return custom
    if lang == "te":
        return DISTRICT_TELUGU.get(name, name)
    elif lang == "hi":
        return DISTRICT_HINDI.get(name, name)
    return name

def render_telangana_interactive_map(
    geojson_data: Dict[str, Any],
    selected_district: str = "ALL",
    district_risks: Optional[Dict[str, int]] = None,
    lang: str = "en",
    color_mode: str = "atlas"
) -> go.Figure:
    """
    Renders an isolated interactive SVG Choropleth Map of Telangana (33 Districts).
    
    Features:
    - Pure Telangana state visualization on dark backdrop (no external state clutter).
    - Every single one of the 33 districts labeled directly inside its boundary outline.
    - Full multilingual support: labels switch dynamically to English, Telugu, or Hindi.
    - Two color modes:
        1. 'atlas': Vibrant administrative colors matching the official Telangana district map.
        2. 'alert': Real-time Early Warning Rainfall-Deficit risk coloring (Green/Amber/Red).
    - High-visibility highlight on active district (luminous 4.5px gold border + beacon pin).
    - Muted soft background opacity (30%) for non-selected districts when inspecting an individual district.
    - Full statewide view when selected_district == 'ALL'.
    """
    is_all_selected = (selected_district == "ALL" or not selected_district)
    canonical_selected = normalize_district_name(selected_district) if not is_all_selected else "ALL"

    fig = go.Figure()

    # Build individual Choropleth traces for each district to guarantee precise styling & clickability
    for name in EXACT_33_DISTRICTS:
        norm_id = get_internal_id(name)
        is_selected = (name == canonical_selected and not is_all_selected)
        te_name = DISTRICT_TELUGU.get(name, name)
        hi_name = DISTRICT_HINDI.get(name, name)

        # Determine district color based on active color_mode
        if color_mode == "alert":
            if district_risks and name in district_risks:
                r_val = district_risks[name]
                if r_val == 0:
                    base_color = RISK_COLOR_MAP["Low Risk"]
                    cat_name = "Low Risk" if lang == "en" else ("తక్కువ ప్రమాదం" if lang == "te" else "कम जोखिम")
                elif r_val == 1:
                    base_color = RISK_COLOR_MAP["Medium Risk"]
                    cat_name = "Medium Risk" if lang == "en" else ("మధ్యస్థ ప్రమాదం" if lang == "te" else "मध्यम जोखिम")
                elif r_val == 2:
                    base_color = RISK_COLOR_MAP["High Risk"]
                    cat_name = "High Risk" if lang == "en" else ("అధిక ప్రమాదం" if lang == "te" else "उच्च जोखिम")
                else:
                    base_color = RISK_COLOR_MAP["Data Unavailable"]
                    cat_name = "N/A"
            else:
                base_color = RISK_COLOR_MAP["Low Risk"]
                cat_name = "Low Risk"
        else:
            base_color = DISTRICT_ATLAS_COLORS.get(name, "#3b82f6")
            cat_name = name

        # Calculate opacity and border width
        if is_all_selected:
            op = 0.95
            line_w = 1.4
            line_c = "#0f172a"
        elif is_selected:
            op = 1.0
            line_w = 4.5
            line_c = "#fbbf24"  # Luminous gold border
        else:
            op = 0.28          # Soft muted background
            line_w = 1.0
            line_c = "#334155"

        # Tooltip display name
        if lang == "en":
            disp_name = f"{name} ({te_name})"
        elif lang == "te":
            disp_name = f"{te_name} ({name})"
        else:
            disp_name = f"{hi_name} ({name})"

        fig.add_trace(
            go.Choropleth(
                geojson=geojson_data,
                locations=[norm_id],
                z=[1],
                featureidkey="properties.id",
                colorscale=[[0, base_color], [1, base_color]],
                showscale=False,
                marker_opacity=op,
                marker_line_width=line_w,
                marker_line_color=line_c,
                name=disp_name,
                hovertemplate=f"<b>{disp_name}</b><br>{cat_name}<extra></extra>"
            )
        )

    # Add Scattergeo trace for names of all 33 districts inside boundary outlines
    label_lats = []
    label_lons = []
    label_texts = []
    label_sizes = []

    for name in EXACT_33_DISTRICTS:
        lat, lon = DISTRICTS[name]
        lbl = get_district_display_label(name, lang)
        label_lats.append(lat)
        label_lons.append(lon)
        label_texts.append(lbl)

        # Dynamically scale font size for long district names so everything fits cleanly
        if len(lbl) > 18:
            label_sizes.append(8.0)
        elif len(lbl) > 13:
            label_sizes.append(8.5)
        elif len(lbl) > 8:
            label_sizes.append(9.5)
        else:
            label_sizes.append(10.5)

    text_color = "#000000" if color_mode == "atlas" else "#ffffff"

    fig.add_trace(
        go.Scattergeo(
            lat=label_lats,
            lon=label_lons,
            mode="text",
            text=label_texts,
            textposition="middle center",
            textfont=dict(
                size=label_sizes,
                color=text_color,
                family="Arial Black, Helvetica, sans-serif"
            ),
            hoverinfo="skip",
            showlegend=False
        )
    )

    # Beacon label on the selected district when inspecting (clean text label without any star-diamond icon)
    if not is_all_selected and canonical_selected in DISTRICTS:
        sel_lat, sel_lon = DISTRICTS[canonical_selected]
        if lang == "en":
            sel_label = canonical_selected
        elif lang == "te":
            sel_label = DISTRICT_TELUGU.get(canonical_selected, canonical_selected)
        else:
            sel_label = DISTRICT_HINDI.get(canonical_selected, canonical_selected)

        fig.add_trace(
            go.Scattergeo(
                lat=[sel_lat],
                lon=[sel_lon],
                mode="text",
                text=[f"📍 {sel_label.upper()}"],
                textposition="top center",
                textfont=dict(size=14, color="#fbbf24", family="Arial Black"),
                hoverinfo="skip",
                showlegend=False
            )
        )

    fig.update_geos(
        fitbounds="locations",
        visible=False,
        bgcolor="#0b0f19"
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=10),
        height=680,
        paper_bgcolor="#0b0f19",
        plot_bgcolor="#0b0f19",
        showlegend=False,
        clickmode="event+select"
    )

    return fig
