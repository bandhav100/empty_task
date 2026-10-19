"""Central Water Commission (CWC) Flood Forecast System (FFS) Integration.
Official Government of India portal: https://ffs.india-water.gov.in/
Monitors river stages, inflow forecasts, warning and danger levels across Telangana basins.
"""

from typing import Dict, Any, List, Optional
import requests
import urllib3
urllib3.disable_warnings()

CWC_FFS_PORTAL_URL = "https://ffs.india-water.gov.in/#/"
CWC_FFS_BASE_URL = "https://ffs.india-water.gov.in"

# Key CWC Hydrological & Flood Forecasting Stations across Telangana's 33 districts
# Covering both Godavari Basin and Krishna Basin
CWC_TELANGANA_STATIONS: List[Dict[str, Any]] = [
    {
        "station_name": "Bhadrachalam",
        "station_name_te": "భద్రాచలం",
        "district": "Bhadradri Kothagudem",
        "river": "Godavari",
        "river_te": "గోదావరి",
        "basin": "Godavari Basin",
        "warning_level_m": 13.11,   # 43.0 ft
        "danger_level_m": 14.63,    # 48.0 ft
        "hfl_m": 16.89,             # Historic High Flood Level (55.4 ft)
        "station_type": "Level Forecast Station",
        "description": "Crucial downstream flood gauge monitoring inflows from northern and central Telangana catchments."
    },
    {
        "station_name": "Perur",
        "station_name_te": "పేరూరు",
        "district": "Jayashankar Bhupalpally",
        "river": "Godavari",
        "river_te": "గోదావరి",
        "basin": "Godavari Basin",
        "warning_level_m": 76.50,
        "danger_level_m": 77.50,
        "hfl_m": 80.20,
        "station_type": "Level Forecast Station",
        "description": "Monitors Godavari river flood wave before confluence with Pranahita."
    },
    {
        "station_name": "Mancherial (Gudem)",
        "station_name_te": "మంచిర్యాల (గూడెం)",
        "district": "Mancherial",
        "river": "Godavari",
        "river_te": "గోదావరి",
        "basin": "Godavari Basin",
        "warning_level_m": 132.50,
        "danger_level_m": 134.00,
        "hfl_m": 136.80,
        "station_type": "Level & Inflow Gauge",
        "description": "Monitors upper Godavari river flow and local runoff from northern districts."
    },
    {
        "station_name": "Medigadda (Lakshmi Barrage)",
        "station_name_te": "మేడిగడ్డ (లక్ష్మి బ్యారేజి)",
        "district": "Jayashankar Bhupalpally",
        "river": "Pranahita / Godavari",
        "river_te": "ప్రాణహిత / గోదావరి",
        "basin": "Godavari Basin",
        "warning_level_m": 99.00,
        "danger_level_m": 100.50,
        "hfl_m": 102.10,
        "station_type": "Barrage Inflow Station",
        "description": "Major lift irrigation barrage site tracking massive monsoon discharge from Maharashtra & MP catchments."
    },
    {
        "station_name": "Sripada Yellampalli",
        "station_name_te": "ఎల్లంపల్లి ప్రాజెక్ట్",
        "district": "Peddapalli",
        "river": "Godavari",
        "river_te": "గోదావరి",
        "basin": "Godavari Basin",
        "warning_level_m": 147.00,
        "danger_level_m": 148.00,
        "hfl_m": 148.80,
        "station_type": "Reservoir Inflow Station",
        "description": "Key storage reservoir supplying municipal water to Greater Hyderabad and northern agricultural belts."
    },
    {
        "station_name": "Jurala Project (PJP)",
        "station_name_te": "జూరాల ప్రాజెక్ట్",
        "district": "Jogulamba Gadwal",
        "river": "Krishna",
        "river_te": "కృష్ణా",
        "basin": "Krishna Basin",
        "warning_level_m": 317.00,
        "danger_level_m": 318.52,
        "hfl_m": 319.20,
        "station_type": "Reservoir Inflow & Outflow",
        "description": "First major entry reservoir on River Krishna into Telangana receiving discharges from Karnataka."
    },
    {
        "station_name": "Srisailam Dam",
        "station_name_te": "శ్రీశైలం ప్రాజెక్ట్",
        "district": "Nagarkurnool",
        "river": "Krishna",
        "river_te": "కృష్ణా",
        "basin": "Krishna Basin",
        "warning_level_m": 268.00,
        "danger_level_m": 269.75,
        "hfl_m": 272.50,
        "station_type": "Major Hydel Reservoir",
        "description": "Major inter-state multipurpose reservoir regulating irrigation and power supplies for southern Telangana."
    },
    {
        "station_name": "Nagarjuna Sagar",
        "station_name_te": "నాగార్జున సాగర్",
        "district": "Nalgonda",
        "river": "Krishna",
        "river_te": "కృష్ణా",
        "basin": "Krishna Basin",
        "warning_level_m": 178.00,
        "danger_level_m": 179.83,
        "hfl_m": 181.50,
        "station_type": "Major Storage Reservoir",
        "description": "Critical drinking water and canal irrigation reservoir supplying Nalgonda, Suryapet, and Hyderabad."
    },
    {
        "station_name": "Singur Reservoir",
        "station_name_te": "సింగూరు ప్రాజెక్ట్",
        "district": "Sangareddy",
        "river": "Manjira",
        "river_te": "మంజీరా",
        "basin": "Godavari Basin",
        "warning_level_m": 522.50,
        "danger_level_m": 523.60,
        "hfl_m": 524.00,
        "station_type": "Reservoir Storage Station",
        "description": "Key storage on Manjira river sustaining drinking water for Sangareddy and Hyderabad city."
    },
    {
        "station_name": "Musi Anicut (Hyderabad)",
        "station_name_te": "మూసీ ఆనికట్ (హైదరాబాద్)",
        "district": "Hyderabad",
        "river": "Musi",
        "river_te": "మూసీ",
        "basin": "Krishna Basin",
        "warning_level_m": 510.50,
        "danger_level_m": 512.00,
        "hfl_m": 514.20,
        "station_type": "Urban River Gauge",
        "description": "Monitors urban runoff, flash flood crests, and Osman Sagar / Himayat Sagar gate discharges."
    }
]

# Mapping districts to primary river basin
DISTRICT_BASIN_MAP: Dict[str, str] = {
    "Adilabad": "Godavari Basin",
    "Bhadradri Kothagudem": "Godavari Basin",
    "Hanumakonda": "Godavari Basin",
    "Hyderabad": "Krishna Basin (Musi Sub-basin)",
    "Jagtial": "Godavari Basin",
    "Jangaon": "Godavari Basin",
    "Jayashankar Bhupalpally": "Godavari Basin",
    "Jogulamba Gadwal": "Krishna Basin",
    "Kamareddy": "Godavari Basin",
    "Karimnagar": "Godavari Basin",
    "Khammam": "Godavari Basin (Munneru Sub-basin)",
    "Kumuram Bheem": "Godavari Basin (Pranahita Sub-basin)",
    "Mahabubabad": "Godavari Basin",
    "Mahabubnagar": "Krishna Basin",
    "Mancherial": "Godavari Basin",
    "Medak": "Godavari Basin (Manjira Sub-basin)",
    "Medchal-Malkajgiri": "Godavari / Krishna Border Catchment",
    "Mulugu": "Godavari Basin",
    "Nagarkurnool": "Krishna Basin",
    "Nalgonda": "Krishna Basin",
    "Narayanpet": "Krishna Basin",
    "Nirmal": "Godavari Basin",
    "Nizamabad": "Godavari Basin",
    "Peddapalli": "Godavari Basin",
    "Rajanna Sircilla": "Godavari Basin",
    "Rangareddy": "Krishna Basin (Musi Sub-basin)",
    "Sangareddy": "Godavari Basin (Manjira Sub-basin)",
    "Siddipet": "Godavari Basin",
    "Suryapet": "Krishna Basin (Musi / Krishna Sub-basin)",
    "Vikarabad": "Krishna Basin (Kagna Sub-basin)",
    "Wanaparthy": "Krishna Basin",
    "Warangal": "Godavari Basin",
    "Yadadri Bhuvanagiri": "Krishna Basin (Musi Sub-basin)"
}

def get_cwc_stations_for_district(district_name: str) -> List[Dict[str, Any]]:
    """Retrieve CWC monitoring stations located in or immediately adjacent to a district."""
    stations = [s for s in CWC_TELANGANA_STATIONS if s["district"].lower() == district_name.lower()]
    if not stations:
        # If no station in the exact district, return stations in the same river basin
        target_basin = DISTRICT_BASIN_MAP.get(district_name, "Godavari Basin")
        stations = [s for s in CWC_TELANGANA_STATIONS if target_basin.split()[0] in s["basin"]]
    return stations

def check_cwc_portal_status() -> Dict[str, Any]:
    """Verify live connectivity to Central Water Commission Flood Forecast System."""
    try:
        r = requests.get(CWC_FFS_BASE_URL, timeout=8, verify=False)
        is_up = (r.status_code == 200)
    except Exception:
        is_up = False

    return {
        "portal_name": "Central Water Commission (CWC) Flood Forecast System",
        "portal_url": CWC_FFS_PORTAL_URL,
        "is_online": is_up,
        "authority": "Ministry of Jal Shakti, Department of Water Resources, Govt. of India",
        "scope": "National real-time hydrological observation, water levels, flood early warning & inflow forecasting"
    }
