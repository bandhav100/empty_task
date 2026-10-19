"""Normalize and validate Telangana districts GeoJSON."""

import json
from shapely.geometry import shape
from shapely.validation import make_valid

EXACT_33 = [
    "Adilabad", "Bhadradri Kothagudem", "Hanumakonda", "Hyderabad", "Jagtial", "Jangaon",
    "Jayashankar Bhupalpally", "Jogulamba Gadwal", "Kamareddy", "Karimnagar", "Khammam",
    "Kumuram Bheem", "Mahabubabad", "Mahabubnagar", "Mancherial", "Medak", "Medchal-Malkajgiri",
    "Mulugu", "Nagarkurnool", "Nalgonda", "Narayanpet", "Nirmal", "Nizamabad", "Peddapalli",
    "Rajanna Sircilla", "Rangareddy", "Sangareddy", "Siddipet", "Suryapet", "Vikarabad",
    "Wanaparthy", "Warangal", "Yadadri Bhuvanagiri"
]

def normalize_geojson():
    with open("assets/telangana_districts.geojson", "r", encoding="utf-8") as f:
        geo = json.load(f)

    for feat in geo["features"]:
        name = feat["properties"].get("district")
        if name in ["Kumuram Bheem Asifabad", "Komaram Bheem", "Komaram Bheem Asifabad"]:
            feat["properties"]["district"] = "Kumuram Bheem"
            name = "Kumuram Bheem"

        # Check geometry validity using Shapely
        geom = shape(feat["geometry"])
        if not geom.is_valid:
            print(f"Repairing invalid geometry for {name}")
            repaired = make_valid(geom)
            feat["geometry"] = repaired.__geo_interface__

        norm_id = name.lower().replace("-", "_").replace(" ", "_")
        feat["id"] = norm_id
        feat["properties"]["id"] = norm_id

    with open("assets/telangana_districts.geojson", "w", encoding="utf-8") as f:
        json.dump(geo, f)

    geo_names = [f["properties"]["district"] for f in geo["features"]]
    print("GeoJSON updated successfully.")
    print("Feature count:", len(geo_names))
    print("Exact 33 match:", sorted(geo_names) == sorted(EXACT_33))

if __name__ == "__main__":
    normalize_geojson()
