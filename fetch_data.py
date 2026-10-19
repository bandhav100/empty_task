"""STEP 1 - download free data. Needs internet. Safe to re-run: it resumes."""
import os, time, requests, pandas as pd
from districts import DISTRICTS

START, END = "2005-01-01", "2026-09-30"
os.makedirs("raw", exist_ok=True)

# El Nino index (NOAA)
oni = requests.get("https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt", timeout=60)
oni.raise_for_status()
open("oni.txt", "w").write(oni.text)
print("ONI saved")

for name, (lat, lon) in DISTRICTS.items():
    f = f"raw/{name}.csv"
    if os.path.exists(f):
        continue
    for attempt in range(6):
        r = requests.get("https://archive-api.open-meteo.com/v1/archive", timeout=90, params=dict(
            latitude=lat, longitude=lon, start_date=START, end_date=END,
            daily="precipitation_sum", timezone="Asia/Kolkata"))
        if r.status_code == 200:
            break
        print(f"{name}: HTTP {r.status_code}, waiting 65s (rate limit)...")
        time.sleep(65)
    else:
        raise SystemExit("Rate limit hit. Wait some time and run again - it will resume.")
    d = r.json()["daily"]
    df = pd.DataFrame({"date": pd.to_datetime(d["time"]), "rain": d["precipitation_sum"]})
    m = df.set_index("date")["rain"].resample("MS").sum(min_count=1).reset_index()
    m.to_csv(f, index=False)
    print("done", name)
    time.sleep(3)

parts = []
for name in DISTRICTS:
    m = pd.read_csv(f"raw/{name}.csv", parse_dates=["date"])
    m["district"] = name
    parts.append(m)
pd.concat(parts).to_csv("rain_monthly.csv", index=False)
print("rain_monthly.csv ready")
