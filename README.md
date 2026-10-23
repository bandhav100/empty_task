El Niño-Aware Water Stress and Air Quality Advisor for Telangana

A Machine Learning-Based Environmental Decision-Support Prototype for Citizens, Farmers, and Urban Communities

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-Web%20Application-FF4B4B?logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/ML-Random%20Forest-green" alt="Random Forest">
  <img src="https://img.shields.io/badge/Climate-ENSO%20%2F%20ONI-orange" alt="Climate">
  <img src="https://img.shields.io/badge/Languages-English%20%7C%20Telugu%20%7C%20Hindi-purple" alt="Multilingual">
  <img src="https://img.shields.io/badge/Status-Research%20Prototype-lightgrey" alt="Research Prototype">
</p>Project Theme: Swachh & Sustainable Bharat — Water, Environment & Climate
Geographic Coverage: All 33 districts of Telangana, India
Application Type: Interactive environmental monitoring and decision support
Deployment: Local Python environment / Streamlit Community Cloud

«Disclaimer: This is an independent research prototype, not an official government portal. Its predictions and recommendations are informational and must not replace official weather forecasts, flood warnings, medical advice, or emergency instructions.»

---

Table of Contents

1. "Overview" (#overview)
2. "Problem Statement" (#problem-statement)
3. "Objectives" (#objectives)
4. "Key Features" (#key-features)
5. "System Architecture" (#system-architecture)
6. "Machine Learning Methodology" (#machine-learning-methodology)
7. "Model Evaluation" (#model-evaluation)
8. "Data Sources" (#data-sources)
9. "Technology Stack" (#technology-stack)
10. "Project Structure" (#project-structure)
11. "Installation and Setup" (#installation-and-setup)
12. "Model Training" (#model-training)
13. "Testing" (#testing)
14. "Running the Application" (#running-the-application)
15. "Multilingual Support" (#multilingual-support)
16. "Privacy and Security" (#privacy-and-security)
17. "Limitations" (#limitations)
18. "Future Enhancements" (#future-enhancements)
19. "Research Significance" (#research-significance)
20. "Author" (#author)

---

1. Overview

The El Niño-Aware Water Stress and Air Quality Advisor for Telangana is a software-only environmental research prototype that combines machine learning, climate data, live environmental APIs, and interactive geospatial visualization.

The application aims to make environmental information more accessible to citizens, farmers, and urban residents across Telangana.

It brings together three major areas:

- Seasonal rainfall-deficit risk: Uses a Random Forest classifier and climate-index information to classify potential rainfall-deficit risk based on historical seasonal rainfall patterns.
- Air-quality monitoring: Retrieves available air-quality information, including US AQI, PM2.5, PM10, and ozone, through the Open-Meteo Air Quality API.
- River and flood information: Connects users with water-level and flood-related information through the Central Water Commission (CWC) Flood Forecasting System integration.

The application also provides interactive district maps, environmental recommendations, location-based exploration, and a multilingual interface in English, Telugu, and Hindi.

2. Problem Statement

Rainfall variability, water stress, air pollution, and flood risk are important environmental concerns. However, relevant information is often distributed across separate websites, datasets, and APIs.

This project explores how these sources can be combined into one accessible platform that helps users:

- Explore environmental information for Telangana's 33 districts.
- Understand historical rainfall patterns and seasonal rainfall-deficit categories.
- Investigate the contribution of El Niño–Southern Oscillation (ENSO) information to rainfall-risk classification.
- Monitor available air-quality measurements.
- Access river-monitoring and flood-related resources.
- Understand environmental information in their preferred supported language.

The project focuses on environmental awareness and research rather than providing authoritative forecasts or emergency warnings.

3. Objectives

- Develop a centralized environmental information dashboard for Telangana.
- Build a machine learning workflow for seasonal rainfall-deficit classification.
- Investigate whether Oceanic Niño Index (ONI) features improve classification performance.
- Integrate weather, historical precipitation, and air-quality data.
- Provide access to relevant CWC river and flood information.
- Visualize district boundaries through interactive maps.
- Support English, Telugu, and Hindi interfaces.
- Provide practical water-conservation and air-quality recommendations.
- Minimize unnecessary collection and retention of personal location information.

4. Key Features

4.1 El Niño-Aware Rainfall-Deficit Risk

The application uses historical precipitation data and climate-index information to estimate seasonal rainfall-deficit risk.

Features include:

- Historical rainfall analysis.
- District-oriented environmental exploration.
- ONI-based climate context.
- Random Forest classification.
- Three research-defined rainfall-risk categories.

Risk categories

Class| Risk level| Definition
Class 0| Low Risk| Seasonal rainfall above the 40th historical percentile
Class 1| Medium Risk| Seasonal rainfall between the 20th and 40th percentiles
Class 2| High Risk| Seasonal rainfall in the driest 20% of historical seasons

These categories are defined for this research prototype and are not official drought classifications.

4.2 Air-Quality Monitoring

The application retrieves available air-quality data from Open-Meteo.

Supported measurements include:

- US Air Quality Index (US AQI).
- PM2.5 concentration.
- PM10 concentration.
- Ozone (O₃).

Where implemented, the application provides health-related guidance based on air-quality categories.

Data availability and update frequency depend on the upstream API. API-derived values should not be confused with direct measurements from a nearby regulatory monitoring station unless their source is verified.

4.3 River Water-Level and Flood Information

The application integrates with the Central Water Commission Flood Forecasting System for river and flood-related information associated with the Godavari and Krishna river basins.

Reference portal: https://ffs.india-water.gov.in/#/

The integration helps users explore available water-monitoring information. Coverage depends on the source portal and the implemented integration.

Important: The application is not an official flood-warning system. Users should follow CWC, local authorities, and official emergency communications for safety decisions.

4.4 Interactive Map of Telangana

- Geographic coverage of all 33 districts.
- GeoJSON-based district polygon boundaries.
- Interactive maps rendered using Plotly.
- District-oriented exploration of environmental information.

Map accuracy depends on the quality, provenance, and version of the geographic dataset.

4.5 Multilingual Interface

The application supports three languages:

Language| Purpose
English| Interface for English-speaking users
తెలుగు (Telugu)| Interface for Telugu-speaking users
हिन्दी (Hindi)| Interface for Hindi-speaking users

The language-selection feature is intended to make environmental information more accessible to users with different language preferences.

Translations are managed through the application's localization module.

4.6 Location-Based District Selection

The application supports browser geolocation and manual district selection.

Where permission is granted, location information can be used to identify a relevant district. Users can also select a district manually without sharing their current location.

4.7 Environmental Recommendations

The application presents practical guidance related to water conservation and air-quality awareness, based on the information and categories supported by the implementation.

Recommendations are educational and should be interpreted alongside local conditions and official advice.

---

5. System Architecture

The application follows a modular architecture that separates the user interface, external data sources, preprocessing, machine learning, and visualization.

                 USER
                   |
                   v
          Streamlit Application
                   |
          +--------+---------+
          |        |         |
          v        v         v
       District  Weather   Air Quality
       Selection   API        API
          |        |         |
          +--------+---------+
                   |
          +--------+---------+
          |                  |
          v                  v
   Historical Climate   CWC Flood Forecast
   Data and NOAA ONI    System Integration
          |
          v
   Data Preprocessing
          |
          v
   Feature Engineering
          |
          v
   Random Forest Model
          |
          v
   Rainfall-Risk Classification
          |
          v
  Interactive Maps, Charts,
  Environmental Insights
  and Recommendations

This is a conceptual architecture. The exact execution path depends on the application's implementation.

Main Components

Component| Responsibility
"app.py"| Main Streamlit application
"train_model.py"| Training and data-preparation workflow
"utils/weather_api.py"| Weather archive and forecast API integration
"utils/air_quality_api.py"| Air-quality data integration
"utils/climate_data.py"| NOAA ONI parsing and ENSO classification
"utils/feature_engineering.py"| Environmental feature transformations
"utils/prediction.py"| Model inference and risk classification
"utils/cwc_ffs.py"| CWC Flood Forecasting System integration
"utils/location.py"| Location processing and district lookup
"utils/map_renderer.py"| Interactive geographic visualization
"utils/recommendations.py"| Environmental recommendations
"utils/translations.py"| English, Telugu, and Hindi localization
"utils/data_loader.py"| Data and artifact loading utilities

---

6. Machine Learning Methodology

6.1 Model Used

Random Forest Classifier

Random Forest is an ensemble machine learning algorithm that combines multiple decision trees to perform classification.

It is suitable for structured environmental datasets because it can capture nonlinear relationships and interactions among input features.

6.2 Workflow

Step 1 — Data Collection

Historical precipitation records are collected through the Open-Meteo Historical Weather API. Climate-index information is obtained from NOAA's Climate Prediction Center.

Step 2 — Data Preprocessing

The training workflow prepares the collected data for analysis and aligns environmental observations with their relevant dates, seasons, and district identifiers.

Step 3 — Feature Engineering

The project includes environmental feature transformations, cyclical month encoding, and empirical CDF percentile calculations.

The exact model inputs must match the features used during training.

Step 4 — Target Classification

Historical seasonal rainfall is classified using the project's percentile-based risk definitions:

- Low Risk: rainfall above the 40th percentile.
- Medium Risk: rainfall between the 20th and 40th percentiles.
- High Risk: rainfall in the driest 20%.

Step 5 — Model Training

The training script fits a Random Forest classifier using the prepared features and target labels. The trained artifact is saved for use by the application.

Step 6 — Chronological Validation

The supplied methodology uses an out-of-time validation strategy:

- Training period: observations before 2020.
- Testing period: observations from 2020 onward.

This evaluates model performance on a later period rather than relying only on random data splitting.

Step 7 — Prediction and Visualization

The trained model is loaded by the application to produce a risk classification, which is presented through the Streamlit interface.

6.3 Why Random Forest?

- Handles nonlinear relationships.
- Combines multiple decision trees.
- Supports multiclass classification.
- Can model interactions among environmental features.
- Provides a useful baseline for structured environmental data.

Feature engineering and data preprocessing are supporting techniques, not separate trained ML models.

---

7. Model Evaluation

The following results are the reported experimental results supplied for this project.

Model configuration| Macro F1-score| Accuracy
Random Forest with ONI features| 0.369| 44.2%
Random Forest without ONI features| 0.260| 37.0%

Results Interpretation

The reported results show:

- Macro F1 increased from 0.260 to 0.369.
- Absolute Macro F1 improvement: 0.109.
- Relative Macro F1 improvement: approximately 41.9%.
- Accuracy increased by 7.2 percentage points.

Macro F1 calculates the average F1-score across classes, giving each class equal weight.

The results suggest that ONI features improved performance in the reported experiment. However, the model still has substantial classification error, and the results do not establish operationally reliable rainfall-risk prediction.

Further evaluation should include:

- Per-class precision, recall, and F1-score.
- Confusion matrix.
- Class distribution and sample counts.
- Comparison with a historical-climatology baseline.
- Repeated chronological validation.
- Independent reproduction of the reported metrics.

These figures should be retained in the project documentation only while they remain consistent with the actual training output and evaluation artifacts.

---

8. Data Sources

8.1 Open-Meteo Historical Weather API

Purpose: Historical weather and precipitation data for climate analysis and model development.

The project methodology describes daily precipitation data for district-centroid coordinates, covering 2005 onward where available.

Documentation: https://open-meteo.com/en/docs/historical-weather-api

8.2 Open-Meteo Weather Forecast API

Purpose: Weather forecasts for supported application features.

Documentation: https://open-meteo.com/en/docs

8.3 Open-Meteo Air Quality API

Purpose: Air-quality measurements and forecast information, including supported variables such as US AQI, PM2.5, PM10, and ozone.

Documentation: https://open-meteo.com/en/docs/air-quality-api

8.4 NOAA Climate Prediction Center — Oceanic Niño Index

Purpose: Climate-index information used to represent ENSO conditions in the rainfall-risk research.

The ONI is based on a three-month running mean of sea-surface-temperature anomalies in the Niño 3.4 region of the tropical Pacific.

Data: https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt

8.5 Central Water Commission Flood Forecasting System

Purpose: River water-level and flood-related information where available through the implemented integration.

Portal: https://ffs.india-water.gov.in/#/

8.6 Telangana District Geographic Data

Purpose: Geographic visualization and district selection.

The project uses a GeoJSON dataset containing Telangana's district boundaries. The dataset's original source, licensing terms, and boundary version should be documented alongside the file.

8.7 Local Climate and Rainfall Datasets

The repository may contain locally stored datasets and artifacts such as:

- "rain_monthly.csv" — monthly rainfall data.
- "clim.json" — climate or climatology data.
- "oni.txt" — locally stored ONI data.
- "data/raw/" — raw source datasets, where present.
- "data/processed/" — processed climate data, where present.
- "model.pkl" or "models/model.pkl" — trained model artifact, depending on the repository version.
- "metrics.json" or "models/metrics.json" — model evaluation output, depending on the repository version.

The exact files used by the application depend on the current repository structure.

---

9. Technology Stack

Technology| Purpose
Python| Main programming language
Streamlit| Interactive web interface
scikit-learn| Random Forest training and inference
pandas| Data processing
NumPy| Numerical computation
Plotly| Interactive maps and charts
GeoJSON| Geographic boundary representation
Open-Meteo APIs| Weather and air-quality data
NOAA CPC ONI| Climate-index data
CWC Flood Forecasting System| River and flood information
pytest| Automated testing

---

10. Project Structure

The following is a representative structure based on the documented project modules. Adjust the tree to match the actual files in the repository.

TG W&AIR/
├── app.py
├── common.py
├── districts.py
├── fetch_data.py
├── train_model.py
├── requirements.txt
├── pytest.ini
├── README.md
├── .gitignore
│
├── assets/
│   └── telangana_districts.geojson
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   └── model.pkl
│
├── utils/
│   ├── __init__.py
│   ├── air_quality_api.py
│   ├── climate_data.py
│   ├── data_loader.py
│   ├── districts.py
│   ├── feature_engineering.py
│   ├── location.py
│   ├── map_renderer.py
│   ├── prediction.py
│   ├── recommendations.py
│   ├── translations.py
│   ├── water_resources_data.py
│   ├── water_directory.py
│   ├── weather_api.py
│   └── cwc_ffs.py
│
├── pages/
│   └── [Streamlit pages, if present]
│
└── tests/
    ├── test_districts.py
    ├── test_climate_data.py
    ├── test_features.py
    ├── test_prediction.py
    ├── test_cwc_ffs.py
    └── test_api_integrations.py

---

11. Installation and Setup

Prerequisites

- Python version supported by the dependencies.
- Git.
- Internet connectivity for live API features.

Step 1 — Clone the Repository

git clone https://github.com/bandhav100/empty_task.git
cd empty_task

Step 2 — Create a Virtual Environment

Windows:

python -m venv .venv
.venv\Scripts\activate

macOS/Linux:

python3 -m venv .venv
source .venv/bin/activate

Step 3 — Install Dependencies

python -m pip install --upgrade pip
pip install -r requirements.txt

Step 4 — Run the Application

streamlit run app.py

Open the local address printed by Streamlit in your browser if the application does not open automatically.

---

12. Model Training

The project includes a training script for preparing the data and training the Random Forest model.

Run:

python train_model.py

Training may retrieve historical data and regenerate model artifacts. Check the script's configuration and output paths before running it.

After training, verify that:

- The model artifact is saved to the expected location.
- The application loads that same artifact.
- The training and prediction feature sets match.
- Evaluation metrics correspond to the intended chronological split.

If a valid pre-trained model is included, retraining is not necessarily required just to launch the application.

---

13. Testing

Run the test suite from the project root:

pytest tests/

For verbose output:

pytest -v tests/

The documented test areas include district mappings, climate-index parsing, feature transformations, prediction, CWC integration, and API behavior.

Live API tests may require internet connectivity or mocked responses, depending on their implementation.

---

14. Running the Application

Once the dependencies are installed, start the application with:

streamlit run app.py

The application provides an interactive interface for exploring available district-level environmental information, rainfall-risk classifications, air-quality measurements, maps, and recommendations.

Available functionality depends on the active code, data artifacts, and external API availability.

---

15. Multilingual Support

The application supports three languages: English, Telugu, and Hindi.

Language| Script| Intended audience
English| Latin| English-speaking users
Telugu| తెలుగు| Telugu-speaking users
Hindi| हिन्दी| Hindi-speaking users

The localization module maintains translated interface content and supports switching the application language.

The multilingual interface aims to improve accessibility for citizens with different languag
