"""Comprehensive bilingual translation dictionary (English & Telugu) for the application."""

TRANSLATIONS = {
    "en": {
        "app_title": "Telangana Water Stress & Air Quality Advisor",
        "app_subtitle": "Swachh & Sustainable Bharat — El Niño-Aware Citizen Early Warning System",
        "badge_theme": "Govt. Citizen Advisory • Free & Open-Access",
        "lang_selector_label": "Language / భాష",
        
        # Location & Selection
        "location_header": "Location & District Selection",
        "use_location_checkbox": "Detect my location via Browser GPS (Polygon Containment)",
        "loc_permission_info": (
            "Why we request location: To automatically identify your exact Telangana district "
            "using boundary polygon containment. Your coordinates are processed ephemerally "
            "in active memory only and are never saved or shared."
        ),
        "loc_detected_inside": "Exact district match via boundary polygon: **{district}**.",
        "loc_outside": (
            "Your detected coordinates ({lat:.2f}°N, {lon:.2f}°E) fall outside Telangana territory "
            "({dist} km to boundary). Showing closest Telangana district: **{district}**. "
            "You can pick any district using the dropdown below."
        ),
        "loc_denied_or_manual": "Using manual district selection.",
        "district_select_label": "Select Telangana District (33 Official Districts)",
        "district_coordinates": "Administrative Centroid: Lat {lat:.2f}°N, Lon {lon:.2f}°E",
        
        # Navigation / Tabs
        "tab_overview": "Overview & Risk",
        "tab_map": "Telangana 33-District Map",
        "tab_weather": "7-Day Weather Forecast",
        "tab_model_evaluation": "Model & Climate Science",
        "tab_about": "Disclaimers & Methodology",

        # Water Stress
        "water_section_title": "3-Month Rainfall-Deficit & Water Stress Outlook",
        "water_card_caption": "Probability of seasonal precipitation falling into the driest 20% on historical record",
        "risk_label": "Projected Risk Level",
        "chance_high_stress": "Probability of Severe Deficit (Driest 20%):",
        "chance_medium_stress": "Probability of Moderate Deficit (20-40%):",
        "chance_low_stress": "Probability of Normal / Abundant (>40%):",
        "why_title": "Why This Outlook?",
        "rainfall_driver": "Past 3-Month Rainfall: **{rain:.1f} mm**, ranking at the **{pct:.0f}th percentile** for this season (0 = driest on record, 100 = wettest).",
        "oni_driver": "Oceanic Niño Index (ONI): **{oni:+.2f}** ({state}). 3-month trend: **{delta:+.2f}**.",
        "uncertainty_badge": "Predictive Confidence",

        # Weather Forecast Section
        "weather_section_title": "Local Weather Conditions & 7-Day Synoptic Outlook",
        "weather_synoptic_disclaimer": (
            "Notice: The weather forecast provides a short-range synoptic horizon (7 days) from the Open-Meteo Weather API. "
            "It is NOT a 3-month seasonal forecast. Short-range weather forecasts should never be extrapolated into seasonal water risk."
        ),
        "temp_label": "Temperature",
        "humidity_label": "Relative Humidity",
        "wind_label": "Wind Speed",
        "current_precip_label": "Precipitation Now",

        # Air Quality Section
        "air_section_title": "Live Air Quality Monitor (Open-Meteo)",
        "us_aqi_card_label": "US AQI (EPA Standard)",
        "eu_aqi_card_label": "European AQI (EEA Standard)",
        "pollutant_pm25": "PM2.5: {val:.1f} µg/m³",
        "pollutant_pm10": "PM10: {val:.1f} µg/m³",
        "pollutant_co": "CO: {val:.1f} µg/m³",
        "pollutant_no2": "NO₂: {val:.1f} µg/m³",
        "pollutant_ozone": "Ozone: {val:.1f} µg/m³",
        "aqi_health_header": "Health & Protective Advisory",
        "aqi_disclaimer": (
            "Open-Meteo air quality readings are derived from global atmospheric reanalysis (Copernicus CAMS & SILAM models). "
            "They are separate from Central Pollution Control Board (CPCB) India AQI and do not represent a direct physical ground-station monitor."
        ),

        # CWC Flood Forecast System
        "tab_cwc_flood": "CWC River & Flood Stages",
        "cwc_section_title": "Central Water Commission (CWC) Flood Forecast System",
        "cwc_section_subtitle": "Official hydrological observation and flood early warning by Ministry of Jal Shakti, Govt. of India",
        "cwc_portal_btn": "Launch Official CWC Flood Forecast Portal (ffs.india-water.gov.in)",
        "cwc_basin_label": "River Basin Jurisdiction",
        "cwc_stations_header": "Key Hydrological Monitoring & Inflow Stations for {district}",
        "cwc_warning_level": "Warning Level",
        "cwc_danger_level": "Danger Level",
        "cwc_hfl_level": "Highest Flood Level (HFL)",
        "cwc_authority_notice": "National Flood Forecast & Reservoir Storage Data from Central Water Commission (CWC) • https://ffs.india-water.gov.in/#/",

        # Map Section
        "map_instructions": "Click any district boundary polygon on the map to inspect its local profile, or use the dropdown.",
        "map_legend_title": "Rainfall-Deficit Risk Category",

        # Recommendations
        "citizen_actions_title": "Practical Citizen Action Plan",
        "citizen_actions_subtitle": "Targeted conservation, storage, and health actions for households and communities:",
        "elnino_precautions_title": "🌊 El Niño Special Precautions & Resilience Playbook",
        "elnino_precautions_subtitle": "Targeted safety, agricultural, and conservation measures for citizens, farmers, and communities across Telangana:",
        "elnino_warning_badge": "PACIFIC ENSO ALERT: ADAPTIVE PRECAUTIONARY ADVISORY",

        # Science & Model Comparison
        "model_comparison_title": "Machine Learning Validation & Pacific ENSO Coupling",
        "model_comparison_intro": "Empirical evaluation on unseen out-of-time test records (2020 onwards) with and without NOAA ONI Pacific climate indices:",
        "metric_with_elnino": "With El Niño Features (Macro F1)",
        "metric_without_elnino": "Without El Niño Features (Macro F1)",
        "metric_baseline": "Always-Low Baseline Accuracy",
        "test_period_label": "Evaluation Window",
        "elnino_explanation_title": "What is El Niño and How Does It Affect Telangana?",
        "elnino_explanation_body": (
            "El Niño represents anomalous sea surface warming in the central and eastern equatorial Pacific Ocean.\n\n"
            "• **Monsoon Disruption:** In historical Indian climate records, El Niño events frequently weaken the southwest monsoon branch, causing prolonged dry spells across central and southern Telangana.\n"
            "• **Evaporative Stress:** Higher regional temperatures and increased solar radiation accelerate reservoir and soil moisture drawdown.\n"
            "• **The ONI Metric:** NOAA calculates the Oceanic Niño Index (ONI)—the 3-month running mean SST anomaly in the Niño 3.4 region. An anomaly of +0.5°C or higher denotes El Niño; +1.5°C indicates Strong El Niño.\n"
            "• **Historical ONI Disclosure:** Past ONI observations are used as historical analogs and must not be interpreted as a forecast of future ocean temperatures."
        ),

        # Disclaimers & Ethics
        "disclaimer_title": "Scientific Transparency, Data Provenance & Privacy",
        "disclaimer_text": (
            "1. **Meteorological Proxy, Not Tap Sensor:** 3-month rainfall deficit indicates climatological water stress. It does not directly monitor reservoir gates, municipal pipe pressure, or groundwater bore levels.\n"
            "2. **Correlation vs Causation:** Adding El Niño data improves multi-month prediction accuracy, but does not claim that El Niño alone causes local water shortages.\n"
            "3. **Zero Location Persistence:** Geolocation coordinates are used strictly inside volatile browser session memory for polygon containment. No user coordinates or history are logged or stored.\n"
            "4. **Distinct Air Quality Standards:** US AQI and European AQI are reported using their respective official scales and are not converted to or labeled as CPCB India AQI.\n"
            "5. **Data Sources:** Open-Meteo Weather & Air Quality APIs | NOAA Climate Prediction Center ONI Index | Government of Telangana Administrative GIS Boundaries."
        ),
        "risk_proxy_disclaimer": (
            "Scientific Notice: This is a meteorological rainfall-deficit risk proxy based on precipitation history "
            "and ocean-atmosphere anomalies. It is NOT a direct measurement of household tap water availability, "
            "groundwater aquifer drawdown, or local reservoir storage."
        ),
        "target_window_label": "Forward 3-Month Target Window",
        "seasonal_normal_label": "District Seasonal Normal (Training Climatology)",
        "recent_deficit_label": "Recent Rainfall Anomaly",
        "historical_oni_scenario_label": "Pacific Climate Context (Observed ONI Persistence Scenario)",
        "eval_metrics_table_title": "Baseline (Model A) vs. El Niño-Aware (Model B) Empirical Test Metrics",
        "confusion_matrix_title": "Out-of-Time Test Set Confusion Matrices (2020–2026)",
        "feature_importance_title": "Feature Importance (Tree Split Contribution)",
        "causation_disclaimer": "Tree-based feature importance reflects split utility within the random forest ensemble and does NOT establish hydrological causation.",
        "source_attribution": "Official Data Sources: Open-Meteo Forecast & Archive APIs | NOAA Climate Prediction Center | Telangana GIS Boundaries",
        "err_fetch": "Unable to retrieve live API data at this moment. Please verify your connection or try again shortly.",

        # District Mandals & Water Resources Directory
        "mandals_rivers_header": "District Mandals & Water Resources Directory",
        "mandals_rivers_sub": "Verified spatial directory of administrative mandals, river traversals, and critical water infrastructure.",
        "total_mandals_card": "Verified Mandals",
        "unique_rivers_card": "Unique Verified Rivers",
        "river_associations_card": "River–Mandal Associations",
        "mandal_search_label": "Search Mandal, River, or Asset",
        "mandal_select_label": "Select a Specific Mandal for Deep-Dive Water Profile",
        "river_table_title": "Verified River Traversal & Basin Directory",
        "reservoirs_dams_title": "Major Reservoirs, Dams & Barrages",
        "lift_irrigation_title": "Lift Irrigation Projects & Major Canals",
        "groundwater_stations_title": "Groundwater Monitoring Stations (CGWB / State Registry)",
        "mandal_profile_title": "Mandal Water Profile: {mandal}",
        "no_rivers_notice": "No major river physically crosses this mandal boundary. Local agriculture is supported by minor streams, Mission Kakatiya tanks, and canal distributaries.",
        "source_reference_header": "Authoritative Source & Notes"
    },
    "te": {
        "app_title": "తెలంగాణ నీటి ఒత్తిడి & గాలి నాణ్యత సలహాదారు",
        "app_subtitle": "స్వచ్ఛ & సుస్థిర భారత్ — ఎల్ నినో ఆధారిత పౌర ముందస్తు హెచ్చరిక వ్యవస్థ",
        "badge_theme": "ప్రజా ప్రయోజన సలహాదారు • ఉచిత & పారదర్శక సేవ",
        "lang_selector_label": "భాష / Language",
        
        # Location & Selection
        "location_header": "లొకేషన్ & జిల్లా ఎంపిక",
        "use_location_checkbox": "బ్రౌజర్ GPS ద్వారా నా లొకేషన్ గుర్తించండి (పాలిగాన్ సరిహద్దుల ద్వారా)",
        "loc_permission_info": (
            "లొకేషన్ ఎందుకు అడుగుతున్నాము: అధికారిక జిల్లా సరిహద్దుల ద్వారా మీరు ఉన్న జిల్లాను ఖచ్చితంగా గుర్తించడానికి. "
            "మీ అక్షాంశ, రేఖాంశ వివరాలు ఎక్కడా దాచబడవు లేదా రికార్డ్ చేయబడవు."
        ),
        "loc_detected_inside": "సరిహద్దుల ద్వారా గుర్తించిన మీ జిల్లా: **{district}**.",
        "loc_outside": (
            "మీ లొకేషన్ ({lat:.2f}°N, {lon:.2f}°E) తెలంగాణ సరిహద్దులకు వెలుపల ({dist} కి.మీ దూరంలో) ఉంది. "
            "సమీప తెలంగాణ జిల్లా చూపిస్తున్నాము: **{district}**. మీరు క్రింది డ్రాప్‌డౌన్ ద్వారా కూడా జిల్లాను ఎంచుకోవచ్చు."
        ),
        "loc_denied_or_manual": "జిల్లాను మాన్యువల్‌గా ఎంచుకోండి.",
        "district_select_label": "తెలంగాణ జిల్లాను ఎంచుకోండి (మొత్తం 33 అధికారిక జిల్లాలు)",
        "district_coordinates": "జిల్లా కేంద్రం: అక్షాంశం {lat:.2f}°N, రేఖాంశం {lon:.2f}°E",

        # Navigation / Tabs
        "tab_overview": "సమీక్ష & ప్రమాద స్థాయి",
        "tab_map": "తెలంగాణ 33 జిల్లాల పటం",
        "tab_weather": "7 రోజుల వాతావరణ సమాచారం",
        "tab_model_evaluation": "మోడల్ & వాతావరణ విశ్లేషణ",
        "tab_about": "శాస్త్రీయ వివరాలు & నిబంధనలు",

        # Water Stress
        "water_section_title": "రాబోయే 3 నెలల నీటి ఒత్తిడి & వర్షపాత లోటు అంచనా",
        "water_card_caption": "ఈ సీజన్‌లో చారిత్రక రికార్డులలో అత్యంత పొడి 20% లోకి పడిపోయే సంభావ్యత",
        "risk_label": "అంచనా వేసిన ప్రమాద స్థాయి",
        "chance_high_stress": "తీవ్ర నీటి లోటు అవకాశం (అత్యంత పొడి 20%):",
        "chance_medium_stress": "మధ్యస్థ నీటి లోటు అవకాశం (20-40%):",
        "chance_low_stress": "సాధారణ / సమృద్ధిగా ఉండే అవకాశం (>40%):",
        "why_title": "ఈ ఫలితం వెనుక కారణాలు?",
        "rainfall_driver": "గత 3 నెలల వర్షపాతం: **{rain:.1f} మి.మీ**, ఇది చారిత్రకంగా **{pct:.0f}వ పర్సంటైల్** వద్ద ఉంది (0 = అత్యంత పొడి, 100 = అత్యంత తడి).",
        "oni_driver": "ఓషియానిక్ నినో సూచిక (ONI): **{oni:+.2f}** ({state}). గత 3 నెలల మార్పు: **{delta:+.2f}**.",
        "uncertainty_badge": "మోడల్ విశ్వసనీయత",

        # Weather Forecast Section
        "weather_section_title": "ప్రస్తుత వాతావరణం & 7 రోజుల అంచనా",
        "weather_synoptic_disclaimer": (
            "గమనిక: ఈ వాతావరణ సమాచారం ఓపెన్-మెటియో ద్వారా 7 రోజుల తాత్కాలిక అంచనా మాత్రమే. "
            "ఇది 3 నెలల భవిష్యత్ వాతావరణ సూచన కాదు. స్వల్పకాలిక వాతావరణాన్ని దీర్ఘకాలిక నీటి అంచనాలకు వర్తింపజేయరాదు."
        ),
        "temp_label": "ఉష్ణోగ్రత",
        "humidity_label": "తేమ శాతం",
        "wind_label": "గాలి వేగం",
        "current_precip_label": "ప్రస్తుత వర్షపాతం",

        # Air Quality Section
        "air_section_title": "తాజా గాలి నాణ్యత (ఓపెన్-మెటియో ఆధారంగా)",
        "us_aqi_card_label": "US AQI (అమెరికా ప్రమాణం)",
        "eu_aqi_card_label": "European AQI (యూరోపియన్ ప్రమాణం)",
        "pollutant_pm25": "PM2.5: {val:.1f} µg/m³",
        "pollutant_pm10": "PM10: {val:.1f} µg/m³",
        "pollutant_co": "CO: {val:.1f} µg/m³",
        "pollutant_no2": "NO₂: {val:.1f} µg/m³",
        "pollutant_ozone": "ఓజోన్: {val:.1f} µg/m³",
        "aqi_health_header": "ఆరోగ్య & రక్షణ సలహా",
        "aqi_disclaimer": (
            "ఓపెన్-మెటియో ఎయిర్ క్వాలిటీ రీడింగ్‌లు వాతావరణ మోడలింగ్ (Copernicus CAMS & SILAM) ద్వారా సేకరించబడినవి. "
            "ఇవి కేంద్ర కాలుష్య నియంత్రణ మండలి (CPCB) ఇండియా AQI కి సమానం కావు మరియు నేలమీది గ్రౌండ్ స్టేషన్ ప్రత్యక్ష కొలతలు కావు."
        ),
        # CWC Flood Forecast System
        "tab_cwc_flood": "CWC నదీ ప్రవాహాలు & వరద మట్టాలు",
        "cwc_section_title": "కేంద్ర జల సంఘం (CWC) వరద హెచ్చరికల వ్యవస్థ",
        "cwc_section_subtitle": "భారత ప్రభుత్వ జల్ శక్తి మంత్రిత్వ శాఖ అధికారిక నదీ జలమాపక & వరద ముందస్తు సమాచారం",
        "cwc_portal_btn": "అధికారిక CWC వరద పోర్టల్ చూడండి (ffs.india-water.gov.in)",
        "cwc_basin_label": "నదీ పరీవాహక ప్రాంతం",
        "cwc_stations_header": "{district} పరిధిలోని ప్రధాన జలమాపక కేంద్రాలు",
        "cwc_warning_level": "హెచ్చరిక మట్టం",
        "cwc_danger_level": "ప్రమాద మట్టం",
        "cwc_hfl_level": "చారిత్రక గరిష్ట వరద మట్టం (HFL)",
        "cwc_authority_notice": "జాతీయ వరద సూచనలు & రిజర్వాయర్ నిల్వల డేటా: కేంద్ర జల సంఘం (CWC) • https://ffs.india-water.gov.in/#/",

        # Map Section
        "map_instructions": "పటంపై ఉన్న ఏదైనా జిల్లా సరిహద్దుపై క్లిక్ చేసి దాని సమాచారం చూడండి, లేదా డ్రాప్‌డౌన్ వాడండి.",
        "map_legend_title": "వర్షపాత లోటు ప్రమాద స్థాయి",

        # Recommendations
        "citizen_actions_title": "పౌరులు తీసుకోవలసిన ఆచరణాత్మక చర్యలు",
        "citizen_actions_subtitle": "గృహాలు, అపార్ట్‌మెంట్లు మరియు రైతుల కోసం సూచించిన కార్యాచరణ:",
        "elnino_precautions_title": "🌊 ఎల్ నినో ప్రత్యేక జాగ్రత్తలు & కార్యాచరణ ప్రణాళిక",
        "elnino_precautions_subtitle": "తెలంగాణ పౌరులు, రైతులు మరియు కాలనీల కోసం వ్యవసాయ, తాగునీరు, వడగాల్పుల ప్రత్యేక జాగ్రత్తలు:",
        "elnino_warning_badge": "పసిఫిక్ ఎన్సో హెచ్చరిక: ముందస్తు భద్రతా మార్గదర్శకాలు",

        # Science & Model Comparison
        "model_comparison_title": "మెషిన్ లెర్నింగ్ మోడల్ పనితీరు & ఎల్ నినో ప్రభావం",
        "model_comparison_intro": "2020 తర్వాతి సరికొత్త డేటాపై ఎల్ నినో సూచిక ఉన్నప్పుడు మరియు లేనప్పుడు రాండమ్ ఫారెస్ట్ మోడల్ ఫలితాలు:",
        "metric_with_elnino": "ఎల్ నినో డేటాతో (Macro F1)",
        "metric_without_elnino": "ఎల్ నినో డేటా లేకుండా (Macro F1)",
        "metric_baseline": "బేస్‌లైన్ ఖచ్చితత్వం",
        "test_period_label": "పరీక్షించిన కాలం",
        "elnino_explanation_title": "ఎల్ నినో అంటే ఏమిటి? తెలంగాణపై దీని ప్రభావం ఎలా ఉంటుంది?",
        "elnino_explanation_body": (
            "ఎల్ నినో అనేది పసిఫిక్ మహాసముద్రంలో ఉపరితల నీరు అసాధారణంగా వేడెక్కే సహజ భౌగోళిక ప్రక్రియ.\n\n"
            "• **వర్షపాతం తగ్గడం:** చారిత్రక రికార్డుల ప్రకారం, ఎల్ నినో ఏర్పడిన సంవత్సరాల్లో భారతదేశంలో నైరుతి రుతుపవనాలు బలహీనపడి, తెలంగాణ ప్రాంతంలో వర్షాలు తగ్గే ప్రమాదం ఉంటుంది.\n"
            "• **ఎండలు & ఆవిరి తీవ్రత:** ఎల్ నినో వల్ల ఉష్ణోగ్రతలు పెరిగి, భూగర్భ జలాలు త్వరగా అడుగంటుతాయి.\n"
            "• **ONI కొలమానం:** అమెరికా NOAA సంస్థ దీనిని ONI (Oceanic Niño Index) ద్వారా లెక్కిస్తుంది. ఈ సూచిక +0.5°C కంటే ఎక్కువ ఉంటే ఎల్ నినోగా, +1.5°C మించితే బలమైన ఎల్ నినోగా పరిగణిస్తారు.\n"
            "• **గమనిక:** గతం నాటి ONI డేటా చరిత్రను అధ్యయనం చేయడానికి మాత్రమే ఉపయోగపడుతుంది, ఇది భవిష్యత్ సముద్ర ఉష్ణోగ్రతల సూచన కాదు."
        ),

        # Disclaimers & Ethics
        "disclaimer_title": "శాస్త్రీయ పారదర్శకత & గోప్యతా విధానం",
        "disclaimer_text": (
            "1. **ఇది వాతావరణ సూచిక మాత్రమే:** వర్షపాత లోటు అనేది వాతావరణ కరువు సూచిక. ఇది రిజర్వాయర్ల నీరు లేదా భూగర్భ జలాల ప్రత్యక్ష లభ్యతను నేరుగా కొలవదు.\n"
            "2. **ప్రత్యక్ష కారణ సంబంధం ఆపాదించలేము:** ఎల్ నినో డేటా చేర్చడం వల్ల అంచనా ఖచ్చితత్వం పెరుగుతుంది, కానీ ప్రతీ నీటి కొరతకూ ఎల్ నినో ఒక్కటే కారణం అని నిర్ధారించలేము.\n"
            "3. **పూర్తి లొకేషన్ గోప్యత:** మీ బ్రౌజర్ లొకేషన్ మీకు దగ్గరి జిల్లాను గుర్తించడానికి మాత్రమే మెమరీలో తాత్కాలికంగా ఉపయోగపడుతుంది. ఎలాంటి వ్యక్తిగత డేటా నిల్వ చేయబడదు.\n"
            "4. **వేర్వేరు ఎయిర్ క్వాలిటీ ప్రమాణాలు:** US AQI మరియు యూరోపియన్ AQI లు వాటి అధికారిక పద్ధతిలోనే చూపబడుతున్నాయి, వీటిని CPCB ఇండియా AQI గా మార్చలేదు.\n"
            "5. **అధికారిక వనరులు:** ఓపెన్-మెటియో API | NOAA CPC ONI | తెలంగాణ అధికారిక జియో-స్పేషియల్ సరిహద్దులు."
        ),
        "risk_proxy_disclaimer": (
            "శాస్త్రీయ గమనిక: ఇది చారిత్రక వర్షపాతం మరియు సముద్ర-వాతావరణ ధోరణుల ఆధారంగా అంచనా వేసిన వర్షపాత లోటు ప్రమాద సూచిక మాత్రమే. "
            "ఇది మీ గృహ కుళాయి నీటి లభ్యత, భూగర్భ జల మట్టం లేదా రిజర్వాయర్ నిల్వల ప్రత్యక్ష భౌతిక కొలత కాదు."
        ),
        "target_window_label": "రాబోయే 3 నెలల లక్ష్య కాలవ్యవధి",
        "seasonal_normal_label": "జిల్లా కాలానుగుణ సాధారణ వర్షపాతం (ట్రైనింగ్ ఆధారితం)",
        "recent_deficit_label": "ఇటీవలి వర్షపాత లోటు / వ్యత్యాసం",
        "historical_oni_scenario_label": "పసిఫిక్ వాతావరణ సందర్భం (నమోదైన ONI స్థిరత్వ దృశ్యం)",
        "eval_metrics_table_title": "బేస్‌లైన్ (మోడల్ A) vs. ఎల్ నినో ఆధారిత (మోడల్ B) వాస్తవ పరీక్షా ఫలితాలు",
        "confusion_matrix_title": "పరీక్షా కాలం నాటి కన్‌ఫ్యూజన్ మ్యాట్రిక్స్ (2020–2026)",
        "feature_importance_title": "మోడల్ ఫీచర్ ప్రాముఖ్యత (ట్రీ స్ప్లిట్ కాంట్రిబ్యూషన్)",
        "causation_disclaimer": "ఫీచర్ ప్రాముఖ్యత రాండమ్ ఫారెస్ట్ మోడల్ విభజనలో దోహదపడే స్థాయిని చూపుతుంది; ఇది నేరుగా వాతావరణ లేదా జల సంబంధ కారణాన్ని రుజువు చేయదు.",
        "source_attribution": "సమాచార వనరులు: ఓపెన్-మెటియో వెదర్ & ఎయిర్ క్వాలిటీ API | NOAA CPC ONI | తెలంగాణ అధికారిక సరిహద్దులు",
        "err_fetch": "ప్రస్తుతం లైవ్ డేటా పొందలేకపోతున్నాము. దయచేసి ఇంటర్నెట్ కనెక్షన్‌ని పరిశీలించి, కొద్దిసేపటి తర్వాత మళ్ళీ ప్రయత్నించండి.",

        # District Mandals & Water Resources Directory
        "mandals_rivers_header": "జిల్లా మండలాలు & జల వనరుల డైరెక్టరీ",
        "mandals_rivers_sub": "పరిపాలనా మండలాలు, నదీ ప్రవాహ మార్గాలు మరియు కీలక నీటి మౌలిక సదుపాయాల ధృవీకరించబడిన డైరెక్టరీ.",
        "total_mandals_card": "ధృవీకరించబడిన మండలాలు",
        "unique_rivers_card": "ప్రత్యేక ధృవీకరించబడిన నదులు",
        "river_associations_card": "నది-మండల అనుసంధానాలు",
        "mandal_search_label": "మండలం, నది లేదా జలాశయం శోధించండి",
        "mandal_select_label": "లోతైన నీటి ప్రొఫైల్ కోసం నిర్దిష్ట మండలాన్ని ఎంచుకోండి",
        "river_table_title": "ధృవీకరించబడిన నదీ ప్రవాహాలు & బేసిన్ డైరెక్టరీ",
        "reservoirs_dams_title": "ప్రధాన రిజర్వాయర్లు, డ్యామ్‌లు & బ్యారేజీలు",
        "lift_irrigation_title": "ఎత్తిపోతల పథకాలు (లిఫ్ట్ ఇరిగేషన్) & ప్రధాన కాలువలు",
        "groundwater_stations_title": "భూగర్భ జల పరిశీలన కేంద్రాలు (CGWB నివేదిక)",
        "mandal_profile_title": "మండల జల ప్రొఫైల్: {mandal}",
        "no_rivers_notice": "ఈ మండల సరిహద్దు గుండా ప్రధాన నదులేవీ ప్రవహించవు. స్థానిక వ్యవసాయం మిషన్ కాకతీయ చెరువులు మరియు కాలువల నెట్‌వర్క్‌పై ఆధారపడి ఉంటుంది.",
        "source_reference_header": "అధికారిక ఆధారం & గమనికలు"
    },
    "hi": {
        "app_title": "तेलंगाना जल संकट एवं वायु गुणवत्ता सलाहकार",
        "app_subtitle": "स्वच्छ एवं संधारणीय भारत — अल नीनो-जागरूक नागरिक पूर्व चेतावनी प्रणाली",
        "badge_theme": "शासकीय नागरिक परामर्श • निःशुल्क एवं खुला उपयोग",
        "lang_selector_label": "Language / भाषा / భాష",
        
        # Location & Selection
        "location_header": "स्थान एवं जिला चयन",
        "use_location_checkbox": "ब्राउज़र GPS द्वारा मेरा जिला पहचानें (सीमा पॉलीगॉन)",
        "loc_permission_info": (
            "हम स्थान की अनुमति क्यों मांगते हैं: सीमा पॉलीगॉन द्वारा आपके तेलंगाना जिले की पहचान के लिए। "
            "निर्देशांक केवल सक्रिय मेमोरी में संसाधित होते हैं और कभी सहेजे नहीं जाते।"
        ),
        "loc_detected_inside": "सीमा पॉलीगॉन द्वारा सटीक जिला मिलान: **{district}**।",
        "loc_outside": (
            "आपके निर्देशांक ({lat:.2f}°N, {lon:.2f}°E) तेलंगाना सीमा से बाहर हैं "
            "({dist} किमी दूर)। निकटतम तेलंगाना जिला: **{district}**। "
            "आप नीचे ड्रॉपडाउन से कोई भी जिला चुन सकते हैं।"
        ),
        "loc_denied_or_manual": "मैन्युअल जिला चयन का उपयोग किया जा रहा है।",
        "district_select_label": "तेलंगाना जिला चुनें (33 आधिकारिक जिले)",
        "district_coordinates": "प्रशासनिक केंद्र: अक्षांश {lat:.2f}°N, देशांतर {lon:.2f}°E",
        
        # Navigation / Tabs
        "tab_overview": "अवलोकन एवं जोखिम",
        "tab_map": "तेलंगाना 33-जिला मानचित्र",
        "tab_weather": "7-दिवसीय मौसम पूर्वानुमान",
        "tab_model_evaluation": "मॉडल एवं जलवायु विज्ञान",
        "tab_about": "अस्वीकरण एवं कार्यप्रणाली",

        # Water Stress
        "water_section_title": "3-माह वर्षा-घाटा एवं जल संकट परिदृश्य",
        "water_card_caption": "ऐतिहासिक रिकॉर्ड में मौसमी वर्षा के सबसे सूखे 20% में रहने की संभावना",
        "risk_label": "अनुमानित जोखिम स्तर",
        "chance_high_stress": "गंभीर घाटे की संभावना (सबसे सूखा 20%):",
        "chance_medium_stress": "मध्यम घाटे की संभावना (20-40%):",
        "chance_low_stress": "सामान्य / प्रचुर वर्षा की संभावना (>40%):",
        "why_title": "यह परिदृश्य क्यों?",
        "rainfall_driver": "पिछले 3 माह की वर्षा: **{rain:.1f} मिमी**, इस मौसम के लिए **{pct:.0f}वें प्रतिशतक** पर (0 = सबसे सूखा, 100 = सबसे अधिक)।",
        "oni_driver": "ओशनिक नीनो इंडेक्स (ONI): **{oni:+.2f}** ({state})। 3-माह का रुझान: **{delta:+.2f}**।",
        "uncertainty_badge": "पूर्वानुमान विश्वसनीयता",

        # Weather Forecast Section
        "weather_section_title": "स्थानीय मौसम एवं 7-दिवसीय पूर्वानुमान",
        "weather_synoptic_disclaimer": (
            "सूचना: यह Open-Meteo API से प्राप्त 7 दिनों का अल्पकालिक पूर्वानुमान है। "
            "यह 3-महीने का मौसमी जल पूर्वानुमान नहीं है।"
        ),
        "temp_label": "तापमान",
        "humidity_label": "आपेक्षिक आर्द्रता",
        "wind_label": "हवा की गति",
        "current_precip_label": "वर्तमान वर्षा",

        # Air Quality Section
        "air_section_title": "लाइव वायु गुणवत्ता निगरानी (Open-Meteo)",
        "us_aqi_card_label": "यूएस AQI (EPA मानक)",
        "eu_aqi_card_label": "यूरोपीय AQI (EEA मानक)",
        "pollutant_pm25": "PM2.5: {val:.1f} µg/m³",
        "pollutant_pm10": "PM10: {val:.1f} µg/m³",
        "pollutant_co": "CO: {val:.1f} µg/m³",
        "pollutant_no2": "NO₂: {val:.1f} µg/m³",
        "pollutant_ozone": "ओज़ोन: {val:.1f} µg/m³",
        "aqi_health_header": "स्वास्थ्य एवं सुरक्षा सलाह",
        "aqi_disclaimer": (
            "Open-Meteo वायु गुणवत्ता आंकड़े वैश्विक वायुमंडलीय मॉडल (Copernicus CAMS) पर आधारित हैं। "
            "यह CPCB भारत AQI से अलग हैं।"
        ),

        # CWC Flood Forecast System
        "tab_cwc_flood": "केंद्रीय जल आयोग (CWC) जल स्तर एवं बाढ़",
        "cwc_section_title": "केंद्रीय जल आयोग (CWC) बाढ़ पूर्वानुमान प्रणाली",
        "cwc_section_subtitle": "जल शक्ति मंत्रालय, भारत सरकार द्वारा आधिकारिक बाढ़ चेतावनी एवं निगरानी",
        "cwc_portal_btn": "आधिकारिक CWC बाढ़ पूर्वानुमान पोर्टल खोलें (ffs.india-water.gov.in)",
        "cwc_basin_label": "नदी बेसिन अधिकार क्षेत्र",
        "cwc_stations_header": "{district} के लिए प्रमुख जल मापक एवं प्रवाह स्टेशन",
        "cwc_warning_level": "चेतावनी स्तर",
        "cwc_danger_level": "खतरे का निशान",
        "cwc_hfl": "उच्चतम ऐतिहासिक बाढ़ स्तर (HFL)",
        "cwc_current_level": "वर्तमान जल स्तर",
        "cwc_status": "हाइड्रोलॉजिकल स्थिति",
        "cwc_last_update": "अंतिम रीडिंग समय",
        "cwc_no_stations": "इस जिले के बेसिन में वर्तमान में कोई सक्रिय CWC प्रवाह स्टेशन नहीं मिला।",
        "cwc_portal_status_online": "CWC FFS पोर्टल ऑनलाइन एवं सक्रिय है",
        "cwc_portal_status_offline": "CWC पोर्टल प्रतिक्रिया में विलंब",

        # Citizen Actions
        "citizen_actions_title": "नागरिक जल संरक्षण एवं सुरक्षा कार्य योजना",
        "citizen_actions_subtitle": "अल नीनो जल दबाव के लिए स्थानीय स्तर पर अनुशंसित कार्य",
        "elnino_precautions_title": "🌊 अल नीनो विशेष सावधानियां एवं आपदा प्रबंधन मार्गदर्शिका",
        "elnino_precautions_subtitle": "तेलंगाना के नागरिकों, किसानों एवं समुदायों के लिए कृषि, पेयजल, लू और पशुधन सुरक्षा के व्यावहारिक उपाय:",
        "elnino_warning_badge": "प्रशांत महासागरीय चेतावनी: पूर्व-आपदा अनुकूलन निर्देशिका",

        # Map Specific
        "map_instructions": "मानचित्र पर किसी भी जिले पर क्लिक करें या ड्रॉपडाउन से चुनकर स्थानीय प्रोफाइल देखें।",
        "map_title_state": "तेलंगाना 33 प्रशासनिक जिले",
        "map_legend_high": "उच्च घाटा जोखिम",
        "map_legend_medium": "मध्यम घाटा जोखिम",
        "map_legend_low": "कम घाटा जोखिम",
        "map_legend_na": "डेटा उपलब्ध नहीं",
        "map_inspecting": "वर्तमान में चयनित: **{district}** | जोखिम: **{risk}**",

        # Science & Model Comparison
        "model_comparison_title": "मशीन लर्निंग मॉडल प्रदर्शन एवं अल नीनो प्रभाव",
        "model_comparison_intro": "2020 के बाद के नए डेटा पर अल नीनो सूचकांक के साथ और बिना रैंडम फ़ॉरेस्ट मॉडल के परिणाम:",
        "metric_with_elnino": "अल नीनो डेटा के साथ (Macro F1)",
        "metric_without_elnino": "अल नीनो डेटा के बिना (Macro F1)",
        "metric_baseline": "बेसलाइन सटीकता",
        "test_period_label": "परीक्षण अवधि",
        "elnino_explanation_title": "अल नीनो क्या है? तेलंगाना पर इसका क्या प्रभाव पड़ता है?",
        "elnino_explanation_body": (
            "अल नीनो प्रशांत महासागर में सतही पानी के असामान्य रूप से गर्म होने की एक प्राकृतिक प्रक्रिया है।\n\n"
            "• **वर्षा में कमी:** ऐतिहासिक आंकड़ों के अनुसार, अल नीनो के वर्षों में दक्षिण-पश्चिम मानसून कमजोर पड़ता है, जिससे तेलंगाना में वर्षा कम होने का जोखिम रहता है।\n"
            "• **गर्मी और वाष्पीकरण:** तापमान बढ़ने से भूजल स्तर तेजी से गिरता है।\n"
            "• **ONI सूचकांक:** NOAA इसे Oceanic Niño Index (ONI) से मापता है। +0.5°C से अधिक होने पर अल नीनो माना जाता है।\n"
            "• **सूचना:** ऐतिहासिक ONI डेटा केवल अध्ययन के लिए है, यह भविष्य के तापमान का पूर्वानुमान नहीं है।"
        ),

        # Disclaimers & Ethics
        "disclaimer_title": "वैज्ञानिक पारदर्शिता एवं गोपनीयता नीति",
        "disclaimer_text": (
            "1. **मौसम संबंधी सूचक:** यह वर्षा घाटे का मौसम विज्ञान मॉडल है। यह सीधे भूजल या पाइपलाइन जल आपूर्ति की माप नहीं है।\n"
            "2. **सीधा कारण नहीं:** अल नीनो डेटा मॉडल सटीकता बढ़ाता है, पर हर कमी का एकमात्र कारण नहीं है।\n"
            "3. **स्थान गोपनीयता:** निर्देशांक केवल मेमोरी में उपयोग होते हैं, कभी सहेजे नहीं जाते।\n"
            "4. **आधिकारिक स्रोत:** Open-Meteo API | NOAA CPC ONI | तेलंगाना आधिकारिक GIS सीमाएं।"
        ),
        "risk_proxy_disclaimer": (
            "वैज्ञानिक सूचना: यह ऐतिहासिक वर्षा एवं समुद्री रुझानों पर आधारित वर्षा-घाटा जोखिम अनुमान है। "
            "यह घरेलू नल जल आपूर्ति या भूजल का प्रत्यक्ष भौतिक मापन नहीं है।"
        ),
        "target_window_label": "आगामी 3-माह लक्षित अवधि",
        "seasonal_normal_label": "जिले की मौसमी सामान्य वर्षा (प्रशिक्षण आधारित)",
        "recent_deficit_label": "हालिया वर्षा घाटा / अंतर",
        "historical_oni_scenario_label": "प्रशांत जलवायु संदर्भ (दर्ज ONI परिदृश्य)",
        "eval_metrics_table_title": "बेसलाइन (मॉडल A) बनाम अल नीनो-आधारित (मॉडल B) वास्तविक परीक्षण परिणाम",
        "confusion_matrix_title": "परीक्षण अवधि कन्फ्यूजन मैट्रिक्स (2020–2026)",
        "feature_importance_title": "मॉडल फ़ीचर महत्व (ट्री स्प्लिट योगदान)",
        "causation_disclaimer": "फ़ीचर महत्व रैंडम फ़ॉरेस्ट विभाजन में योगदान दर्शाता है; यह जल संबंधी कारण सिद्ध नहीं करता।",
        "source_attribution": "डेटा स्रोत: Open-Meteo Weather & AQI API | NOAA CPC ONI | तेलंगाना आधिकारिक सीमाएं",
        "err_fetch": "वर्तमान में लाइव डेटा प्राप्त नहीं हो पा रहा है। कृपया इंटरनेट कनेक्शन जांचें और कुछ समय बाद पुनः प्रयास करें।",

        # District Mandals & Water Resources Directory
        "mandals_rivers_header": "जिला मंडल एवं जल संसाधन निर्देशिका",
        "mandals_rivers_sub": "प्रशासनिक मंडलों, नदी मार्गों एवं प्रमुख जल अवसंरचना की सत्यापित स्थानिक निर्देशिका।",
        "total_mandals_card": "सत्यापित मंडल",
        "unique_rivers_card": "विशिष्ट सत्यापित नदियां",
        "river_associations_card": "नदी–मंडल संबंध",
        "mandal_search_label": "मंडल, नदी या जल संरचना खोजें",
        "mandal_select_label": "विस्तृत जल प्रोफ़ाइल के लिए विशिष्ट मंडल चुनें",
        "river_table_title": "सत्यापित नदी प्रवाह एवं बेसिन तालिका",
        "reservoirs_dams_title": "प्रमुख जलाशय, बांध एवं बैराज",
        "lift_irrigation_title": "उद्वहन सिंचाई (लिफ्ट इरिगेशन) एवं प्रमुख नहरें",
        "groundwater_stations_title": "भूजल निगरानी केंद्र (CGWB / राज्य रजिस्ट्री)",
        "mandal_profile_title": "मंडल जल प्रोफ़ाइल: {mandal}",
        "no_rivers_notice": "इस मंडल सीमा से कोई प्रमुख नदी नहीं गुजरती। स्थानीय कृषि मिशन काकतीय तालाबों एवं नहर वितरिकाओं पर आधारित है।",
        "source_reference_header": "आधिकारिक स्रोत एवं संदर्भ"
    }
}

def get_text(key: str, lang: str = "en") -> str:
    """Safely fetch translation string for given key and language."""
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, TRANSLATIONS["en"].get(key, key))
