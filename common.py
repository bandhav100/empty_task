import pandas as pd

SEAS = ["DJF", "JFM", "FMA", "MAM", "AMJ", "MJJ", "JJA", "JAS", "ASO", "SON", "OND", "NDJ"]

def parse_oni(text):
    """Parse NOAA oni.ascii.txt -> DataFrame(date = centre month, oni)."""
    rows = []
    for line in text.strip().splitlines():
        p = line.split()
        if len(p) < 4 or p[0] not in SEAS:
            continue
        rows.append((pd.Timestamp(year=int(p[1]), month=SEAS.index(p[0]) + 1, day=1), float(p[3])))
    return pd.DataFrame(rows, columns=["date", "oni"])
