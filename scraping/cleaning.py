import pandas as pd

def extract_city_country(place):
    try:
        parts = place.split(",")
        country = parts[-1].strip()

        location_part = parts[0]
        if " of " in location_part:
            city = location_part.split(" of ")[-1].strip()
        else:
            city = location_part.strip()

        return pd.Series([city, country])
    except:
        return pd.Series(["Unknown", "Unknown"])

# ===============================
# 1. Load Dataset
# ===============================
df = pd.read_csv("earthquake_1201.csv")

# Tampilkan informasi awal dataset
print("Data awal:")
print(df.info())
print(df.head())

# ===============================
# 2. Menghapus Data Duplikat
# ===============================
df = df.drop_duplicates()

# ===============================
# 3. Menangani Missing Value
# ===============================
# Baris akan dihapus jika kolom penting bernilai kosong
df = df.dropna(subset=[
    "latitude",
    "longitude",
    "magnitude",
    "depth",
    "time"
])

# ===============================
# 4. Konversi Tipe Data
# ===============================
# Konversi kolom numerik
numeric_columns = ["latitude", "longitude", "magnitude", "depth"]
df[numeric_columns] = df[numeric_columns].apply(
    pd.to_numeric, errors="coerce"
)

# Hapus baris dengan nilai numerik tidak valid
df = df.dropna(subset=numeric_columns)

# ===============================
# 5. Konversi Waktu
# ===============================
# Konversi timestamp (ms) menjadi datetime
df["time"] = pd.to_datetime(df["time"], unit="ms")

# 5.5 Feature Engineering (DI SINI)
df[["city", "country"]] = df["place"].apply(extract_city_country)

# 5.6 Mengatur Ulang Posisi Kolom
# ===============================
cols = df.columns.tolist()

# Pindahkan city dan country tepat setelah place
new_order = (
    ["place", "city", "country"] +
    [c for c in cols if c not in ["place", "city", "country"]]
)

df = df[new_order]

# ===============================
# 6. Reset Index
# ===============================
df = df.reset_index(drop=True)

# ===============================
# 7. Simpan Data Bersih
# ===============================
df.to_csv("earthquake_1201_cleanedupd.csv", index=False)

# ===============================
# 8. Informasi Dataset Akhir
# ===============================
print("\nData setelah cleaning:")
print(df.info())
print(df.head())
