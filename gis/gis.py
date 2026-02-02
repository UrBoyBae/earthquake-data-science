import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import os

# PAGE CONFIG 
st.set_page_config(layout="wide", page_title="Peta Gempa Global")
st.title("🌍 Persebaran Spasial Gempa Global")

# LOAD DATA 
CSV_FILE = "earthquake_1201_cleaned_final.csv"

if not os.path.exists(CSV_FILE):
    st.error(f"File tidak ditemukan: {CSV_FILE}")
    st.stop()

# CSV yang di pakai separator ;
df = pd.read_csv(CSV_FILE, sep=";")

#  VALIDASI DATA 
required_cols = [
    "place", "city", "country", "magnitude", "sig",
    "time", "latitude", "longitude", "depth", "tsunami"
]

missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Kolom hilang di CSV: {missing}")
    st.write("Kolom terbaca:", list(df.columns))
    st.stop()

#  KONVERSI NUMERIK 
num_cols = ["latitude", "longitude", "magnitude", "depth", "sig"]

for c in num_cols:
    df[c] = (
        df[c]
        .astype(str)
        .str.replace(",", ".", regex=False)
    )
    df[c] = pd.to_numeric(df[c], errors="coerce")

df["tsunami"] = df["tsunami"].fillna(0).astype(int)

# FEATURE ENGINEERING
df["depth_km"] = df["depth"]

df["depth_category"] = df["depth_km"].apply(
    lambda x: "Dangkal" if x < 70 else "Menengah" if x < 300 else "Dalam"
)

df["sig_category"] = df["sig"].apply(
    lambda x: "Rendah" if x < 100 else "Sedang" if x < 500 else "Tinggi" if x < 800 else "Sangat Tinggi"
)


df["tsunami_potential"] = df["tsunami"].apply(
    lambda x: "Berpotensi" if x == 1 else "Tidak"
)

# SUMMARY
st.success(
    f"**Total {len(df)} kejadian gempa dari {df['country'].nunique()} negara**"
)

# METRICS
c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Gempa", len(df))
c2.metric("Max Magnitude", f"{df['magnitude'].max():.1f}")
c3.metric("Rata-rata Depth", f"{df['depth_km'].mean():.1f} km")

dominant_depth = (
    df["depth_category"].mode().iloc[0]
    if not df["depth_category"].mode().empty
    else "-"
)
c4.metric("Dominan Kedalaman", dominant_depth)

# LEGEND EMOJI
col_legend1, col_legend2 = st.columns(2)
with col_legend1:
    st.markdown("""
    **🗺️ Persebaran Magnitude**
    - 🔴 Merah = M6.0+
    - 🟠 Orange = M5.0-5.9  
    - 🟡 Kuning = M4.0-4.9
    """)
with col_legend2:
    st.markdown("""
      📏 Kedalaman  
    - 🔴 Merah = Dangkal 
    - 🟡 Kuning = Menengah 
    - 🔵 Biru = Dalam 
    """)

#  SELECT COUNTRY 
st.markdown("---")
st.subheader("🗺️ Pilih Negara")

countries = sorted(
    df["country"].unique(),
    key=lambda x: len(df[df["country"] == x]),
    reverse=True
)

col_left, _ = st.columns([3, 9])
with col_left:
    selected_country = st.selectbox(
        "",
        countries,
        label_visibility="collapsed"
    )

df_country = df[df["country"] == selected_country]

#  MAP PER NEGARA
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader(selected_country)
    st.metric("Total Gempa", len(df_country))
    st.metric("Max Mag", f"{df_country['magnitude'].max():.1f}")
    st.metric("Avg Depth", f"{df_country['depth_km'].mean():.1f} km")

with col2:
    m_country = folium.Map(
        location=[
            df_country["latitude"].mean(),
            df_country["longitude"].mean()
        ],
        zoom_start=5
    )

    for _, r in df_country.iterrows():
        color = (
            "red" if r["magnitude"] >= 6 else
            "orange" if r["magnitude"] >= 5 else
            "yellow"
        )

        folium.CircleMarker(
            [r["latitude"], r["longitude"]],
            radius=8,
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.8,
            popup=f"""
            <div style="width:320px">
            <b>📍 {r['place']} ({r['city']})</b><br>
            🌍 Negara: {r['country']}<br>
            ⏰ Waktu: {r['time']}<br>
            🌡️ Magnitude: {r['magnitude']}<br>
            📏 Depth: {r['depth_km']} km ({r['depth_category']})<br>
            ⚠️ Significance: {r['sig']} ({r['sig_category']})<br>
            🌊 Tsunami: {r['tsunami_potential']}
            </div>
            """
        ).add_to(m_country)

    st_folium(m_country, width=850, height=420)

#  GLOBAL TABS 
tab1, tab2, tab3 = st.tabs(
    ["🗺️ Global Magnitude", "📏 Global Depth", "📊 Statistik & Tabel"]
)

# TAB 1
with tab1:
    m1 = folium.Map(
        location=[df["latitude"].mean(), df["longitude"].mean()],
        zoom_start=2
    )

    for _, r in df.iterrows():
        color = "red" if r["magnitude"] >= 6 else "orange" if r["magnitude"] >= 5 else "yellow"
        folium.CircleMarker(
            [r["latitude"], r["longitude"]],
            radius=5,
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.7
        ).add_to(m1)

    st_folium(m1, width=1200, height=600)

# TAB 2 
with tab2:
    m2 = folium.Map(
        location=[df["latitude"].mean(), df["longitude"].mean()],
        zoom_start=2
    )

    for _, r in df.iterrows():
        fill = (
            "red" if r["depth_category"] == "Dangkal" else
            "yellow" if r["depth_category"] == "Menengah" else
            "blue"
        )

        folium.CircleMarker(
            [r["latitude"], r["longitude"]],
            radius=6,
            color="black",
            fill=True,
            fillColor=fill,
            fillOpacity=0.8
        ).add_to(m2)

    st_folium(m2, width=1200, height=600)

# TAB 3
with tab3:

    st.subheader("📋 Tabel Data Lengkap")
    st.dataframe(df, use_container_width=True)
