# El Niño-Aware Water Stress and Air Quality Advisor for Citizens of Telangana

**Theme:** Swachh & Sustainable Bharat — Water, Environment & Climate  
**Target:** Citizens, farmers, and urban residents across all 33 districts of Telangana  
**Deployment:** Streamlit Community Cloud / Local Python

---

## 🌟 Overview

The **Telangana Water Stress & Air Quality Advisor** is a free, open-access, software-only decision support tool designed to empower citizens of Telangana with actionable intelligence regarding:
1. **3-Month Rainfall-Deficit Risk:** An El Niño-aware machine learning model forecasting whether the upcoming season will be among the driest 20% on historical record for each district.
2. **Real-Time Air Quality Monitoring:** Live US AQI, PM2.5, PM10, and ozone metrics retrieved directly from Open-Meteo with EPA-standard health recommendations.
3. **CWC River Water Level & Flood Early Warning:** Seamless integration with Central Water Commission (CWC) Flood Forecast System (https://ffs.india-water.gov.in/#/) for Godavari and Krishna river basins.
4. **Genuine 33-District Boundary Map:** Full interactive spatial boundary visualization of Telangana's 33 districts using GeoJSON and Plotly.
5. **Bilingual Localization:** Comprehensive English and Telugu (తెలుగు) interface.
6. **Strict Privacy Architecture:** Zero persistence of personal location coordinates; browser geolocation is processed ephemerally with full fallback to manual district selection.

---

## 🏗️ Architecture & Project Structure

```
telangana_advisor/
├── app.py                      # Main Streamlit web application shell
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # VCS exclusion rules
├── data/
│   ├── raw/                    # Raw historical Open-Meteo precipitation CSVs & NOAA ONI table
│   └── processed/              # Aggregated monthly precipitation & climatology distributions
├── models/
│   ├── model.pkl               # Trained Random Forest classifier bundle
│   └── metrics.json            # Model evaluation metrics (Macro F1 with vs without El Niño)
├── utils/
│   ├── __init__.py
│   ├── districts.py            # 33 Telangana districts coordinates & bilingual metadata
│   ├── location.py             # Haversine distance, nearest district lookup, privacy logic
│   ├── cwc_ffs.py              # Central Water Commission Flood Forecast System integration (ffs.india-water.gov.in)
│   ├── weather_api.py          # Open-Meteo Archive & Forecast API clients
│   ├── air_quality_api.py      # Open-Meteo Air Quality client & EPA categorizations
│   ├── climate_data.py         # NOAA CPC ONI parser and ENSO phase classification
│   ├── data_loader.py          # Resilient caching loaders for artifacts and maps
│   ├── feature_engineering.py  # Cyclical month encoding and empirical CDF percentiles
│   ├── prediction.py           # Random Forest inference & predictive uncertainty classification
│   ├── recommendations.py      # Practical citizen water & air quality action plans
│   ├── translations.py         # Complete English & Telugu localization dictionary
│   └── map_renderer.py         # Plotly choropleth boundary map renderer
├── assets/
│   └── telangana_districts.geojson # Official 33-district polygon boundaries
├── tests/
│   ├── test_districts.py       # Unit tests for district mappings and coordinates
│   ├── test_climate_data.py    # Unit tests for NOAA ONI parsing
│   ├── test_features.py        # Unit tests for feature transforms and percentiles
│   ├── test_prediction.py      # Unit tests for inference pipeline
│   ├── test_cwc_ffs.py         # Unit tests for CWC Flood Forecast System
│   └── test_api_integrations.py # Unit tests for live APIs and error boundaries
└── train_model.py              # Automated data fetch and model training script
```

---

## 🔬 Scientific Methodology & Model Evaluation

### Data Sources
* **Precipitation Data:** Open-Meteo Historical Weather API (2005 to present), recording daily precipitation sums for the centroid coordinates of each of Telangana's 33 districts.
* **Climate Index:** NOAA Climate Prediction Center (CPC) Oceanic Niño Index (ONI), measuring 3-month running mean sea surface temperature anomalies in the Niño 3.4 region (5°N–5°S, 120°–170°W).
* **Live Air Quality:** Open-Meteo Air Quality API measuring hourly US AQI, PM2.5, and PM10.

### Training & Validation
* **Split Strategy:** Out-of-time chronological validation. Trained on data before 2020; tested on unseen data from 2020 onwards.
* **Target Classes:** 
  * `Class 0 (Low Risk)`: Projected rainfall > 40th percentile of historical seasons.
  * `Class 1 (Medium Risk)`: Projected rainfall between 20th and 40th percentiles.
  * `Class 2 (High Risk)`: Projected rainfall in the driest 20% on record.
* **Empirical Validation Results:**
  * **With El Niño (ONI features):** Macro F1 = **0.369** (Accuracy = 44.2%)
  * **Without El Niño:** Macro F1 = **0.260** (Accuracy = 37.0%)
  * *Incorporating Pacific sea surface temperature signals yields a +41.9% improvement in balanced Macro-F1 across multi-class rainfall deficit detection.*

---

## 🚀 Quickstart & Local Execution

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Model Training (Optional, pre-trained artifacts included)
```bash
python train_model.py
```

### 3. Run Automated Tests
```bash
pytest tests/
```

### 4. Launch Application
```bash
streamlit run app.py
```
