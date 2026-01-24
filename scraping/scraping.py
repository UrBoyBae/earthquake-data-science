import requests
import pandas as pd
import os

BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

params = {
    "format": "geojson",
    "starttime": "2024-01-01",
    "endtime": "2025-12-31",
    "minmagnitude": 4,
    "limit": 1201,
    "orderby": "time"
}

print("Mengambil data dari USGS...")

response = requests.get(BASE_URL, params=params, timeout=30)

if response.status_code != 200:
    raise Exception("Gagal mengambil data USGS")

data = response.json()["features"]

rows = []

for d in data:
    prop = d["properties"]
    geo = d["geometry"]["coordinates"]

    time_fixed = pd.to_datetime(prop["time"], unit="ms")

    rows.append({
        "place": prop["place"],
        "magnitude": prop["mag"],
        "time": time_fixed,

        "latitude": geo[1],
        "longitude": geo[0],
        "depth": geo[2],

        "tsunami": prop.get("tsunami", 0),
        "sig": prop.get("sig", None)
    })

df = pd.DataFrame(rows)

# pastikan numeric
numeric_cols = ["magnitude", "latitude", "longitude", "depth", "sig"]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ===============================
# SIMPAN KE FOLDER RAW
# ===============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_PATH = os.path.join(
    BASE_DIR, "..", "data", "raw", "earthquake_1201.csv"
)

os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)

df.to_csv(RAW_PATH, index=False, encoding="utf-8-sig")

print("================================")
print("SCRAPING SELESAI")
print("Total data:", len(df))
print("File raw:", RAW_PATH)
print("================================")
