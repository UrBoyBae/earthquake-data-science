import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(layout="wide")
st.title("📊 Dashboard Tren Frekuensi Gempa Dunia")

# File CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "..", "data", "clean", "earthquake_1201_cleaned_final.csv")

# ================== LOAD & CLEAN DATA ==================
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_FILE, sep=";")

    # Bersihkan kolom angka
    df["depth_km"] = (
        df["depth_km"]
        .astype(str)
        .str.replace("km", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )
    df["depth_km"] = pd.to_numeric(df["depth_km"], errors="coerce")

    df["sig"] = pd.to_numeric(df["sig"], errors="coerce")

    # Kategori depth
    df["depth_category"] = df["depth_km"].apply(
        lambda x: "Dangkal" if pd.notna(x) and x < 70
        else "Menengah" if pd.notna(x) and x < 300
        else "Dalam"
    )

    # Kategori sig
    df["sig_category"] = df["sig"].apply(
        lambda x: "Rendah" if pd.notna(x) and x < 500
        else "Sedang" if pd.notna(x) and x < 1000
        else "Tinggi"
    )

    # Waktu
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    df = df.dropna(subset=["time"])
    df["month_year"] = df["time"].dt.to_period("M").astype(str)

    return df


df = load_data()
sns.set_style("whitegrid")

# ================== PILIH NEGARA ==================
st.subheader("🗺️ Pilih Satu atau Lebih Negara")

col1, col2, col3 = st.columns([2, 3, 2])

with col2:
    countries = sorted(
        df["country"].dropna().unique(),
        key=lambda x: len(df[df["country"] == x]),
        reverse=True
    )

    selected_countries = st.multiselect(
        "Pilih negara:",
        countries,
        default=countries[:3]
    )

# ================== DATA TREN ==================
trend_df = df.groupby(["month_year", "country"]).size().unstack(fill_value=0)

df_selected = df[df["country"].isin(selected_countries)]
trend_selected = (
    df_selected.groupby(["month_year", "country"])
    .size()
    .unstack(fill_value=0)
)

# ================== PLOT ==================
fig, axes = plt.subplots(2, 1, figsize=(14, 12), sharex=True)

# ---- Semua Negara ----
for country in trend_df.columns:
    axes[0].plot(trend_df.index, trend_df[country], linewidth=1, alpha=0.4)

axes[0].set_title("Tren Frekuensi Gempa per Wilayah (Bulanan) - Semua Negara", fontsize=14, fontweight="bold")
axes[0].set_ylabel("Jumlah Gempa")
axes[0].grid(True, linestyle="--", alpha=0.5)

# ---- Negara Dipilih ----
if not trend_selected.empty:
    for country in trend_selected.columns:
        axes[1].plot(trend_selected.index, trend_selected[country], marker="o", linewidth=2, label=country)
    axes[1].set_title("Tren Gempa Bulanan - Negara Terpilih", fontsize=14, fontweight="bold")
    axes[1].set_xlabel("Periode (Tahun-Bulan)")
    axes[1].set_ylabel("Jumlah Gempa")
    axes[1].legend(title="Negara Dipilih", bbox_to_anchor=(1.05, 1), loc="upper left")
    axes[1].grid(True, linestyle="--", alpha=0.6)
else:
    axes[1].text(0.5, 0.5, "Pilih minimal satu negara", horizontalalignment="center", verticalalignment="center", transform=axes[1].transAxes, fontsize=12)

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)
