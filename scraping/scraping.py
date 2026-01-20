import requests
import pandas as pd

url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

params = {
    "format": "geojson",
    "starttime": "2024-01-01",
    "endtime": "2025-12-31",
    "minmagnitude": 4,
    "limit": 1201
}

r = requests.get(url, params=params)
data = r.json()["features"]

rows = []
for d in data:
    rows.append({
        "place": d["properties"]["place"],
        "magnitude": d["properties"]["mag"],
        "time": d["properties"]["time"],
        "latitude": d["geometry"]["coordinates"][1],
        "longitude": d["geometry"]["coordinates"][0],
        "depth": d["geometry"]["coordinates"][2]
    })

df = pd.DataFrame(rows)
df.to_csv("earthquake_1201.csv", index=False)

print("SELESAI:", len(df))
