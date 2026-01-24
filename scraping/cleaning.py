import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_PATH = os.path.join(BASE_DIR, "..", "data", "raw", "earthquake_1201.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "..", "data", "clean", "earthquake_1201_cleaned_final.csv")


# ===============================
# HELPER
# ===============================

def extract_city_country(place):
    try:
        parts = str(place).split(",")

        country_raw = parts[-1].lower().strip()

        for w in ["region", "earthquake", "area"]:
            country_raw = country_raw.replace(w, "")

        country = country_raw.strip().title()

        loc = parts[0]
        city = loc.split(" of ")[-1].strip().title()

        return city, country

    except:
        return "Unknown", "Unknown"


def classify_depth(d):
    if pd.isna(d):
        return "Unknown"
    if d < 70:
        return "Dangkal"
    elif d < 300:
        return "Menengah"
    else:
        return "Dalam"


def classify_sig(s):
    if pd.isna(s):
        return "Unknown"
    if s < 100:
        return "Rendah"
    elif s < 500:
        return "Sedang"
    elif s < 800:
        return "Tinggi"
    else:
        return "Sangat Tinggi"


# ===============================
# LOAD
# ===============================

df = pd.read_csv(INPUT_PATH)
df.columns = df.columns.str.lower().str.strip()

print("DATA RAW:", len(df))


# ===============================
# CLEAN BASIC
# ===============================

df = df.loc[:, ~df.columns.str.contains("^unnamed")]
df = df.drop_duplicates()


# ===============================
# NUMERIC FIX
# ===============================

num_cols = ["latitude", "longitude", "magnitude", "depth", "sig"]
num_cols = [c for c in num_cols if c in df.columns]

for c in num_cols:
    df[c] = (
        df[c]
        .astype(str)
        .str.replace(",", ".", regex=False)
    )

df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce")


# ===============================
# TIME FIX (AUTO DETECT)
# ===============================

if "time" in df.columns:

    df["time"] = pd.to_datetime(
        df["time"],
        errors="coerce",
    )


# ===============================
# TSUNAMI
# ===============================

if "tsunami" in df.columns:
    df["tsunami"] = pd.to_numeric(df["tsunami"], errors="coerce")
    df["tsunami"] = df["tsunami"].map({0: "Tidak", 1: "Ya"})


# ===============================
# FEATURE ENGINEERING
# ===============================

if "place" in df.columns:

    loc = df["place"].apply(extract_city_country)

    loc_df = pd.DataFrame(
        loc.tolist(),
        columns=["city", "country"]
    )

    df["city"] = loc_df["city"]
    df["country"] = loc_df["country"]


# ===============================
# DEPTH FEATURE
# ===============================

if "depth" in df.columns:
    df["depth"] = df["depth"].round(2)
    df["depth_km"] = df["depth"].astype(str) + " km"
    df["depth_category"] = df["depth"].apply(classify_depth)


# ===============================
# SIG FEATURE
# ===============================

if "sig" in df.columns:
    df["sig_category"] = df["sig"].apply(classify_sig)


# ===============================
# KOORDINAT FILTER (SAFE)
# ===============================

if "latitude" in df.columns:
    df = df[df["latitude"].between(-90, 90, inclusive="both") | df["latitude"].isna()]

if "longitude" in df.columns:
    df = df[df["longitude"].between(-180, 180, inclusive="both") | df["longitude"].isna()]


# ===============================
# FINAL COLUMN ORDER
# ===============================

final_cols = [
    "place","city","country",
    "time",
    "magnitude","sig","sig_category",
    "depth","depth_km","depth_category",
    "latitude","longitude",
    "tsunami"
]

final_cols = [c for c in final_cols if c in df.columns]

df = df[final_cols]


# ===============================
# SAVE
# ===============================

df.reset_index(drop=True, inplace=True)

df.to_csv(
    OUTPUT_PATH,
    index=False,
    sep=";",
    decimal=",",
    encoding="utf-8-sig"
)

print("==============================")
print("CLEANING SELESAI")
print("DATA AKHIR:", len(df))
print("OUTPUT:", OUTPUT_PATH)
print("==============================")
