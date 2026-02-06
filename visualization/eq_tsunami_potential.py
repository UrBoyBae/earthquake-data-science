import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import csv
import folium
from streamlit_folium import st_folium

st.title("Visualisasi Potensi Tsunami")

# File CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_FILE = os.path.join(BASE_DIR, "..", "data", "clean", "earthquake_1201_cleaned_final.csv")


if not os.path.exists(CSV_FILE):
    st.error(f"File tidak ditemukan: {CSV_FILE}")
    st.stop()

# Read CSV
try:
    df = pd.read_csv(
        CSV_FILE,
        sep=";",
        decimal=",",
        encoding="utf-8-sig",
        engine="python",
        on_bad_lines="skip",
        quoting=csv.QUOTE_MINIMAL
    )
    # st.success("File berhasil dibaca")
except Exception as e:
    st.error(f"Gagal membaca file: {e}")
    st.stop()


# Folium Map
m = folium.Map(
    location=[-2.5, 118],
    zoom_start=5,
    tiles="OpenStreetMap"
)


# Normalisasi Data Tsunami
df["tsunami"] = (
    df["tsunami"]
    .astype(str)
    .str.strip()
    .str.lower()
)

# Preview Data
st.subheader("Preview Data")
df_preview = df.drop(columns=['place'], errors='ignore')
st.dataframe(df_preview.head())

# Status Tsunami
st.subheader("Status Tsunami")

if "tsunami" not in df.columns:
    st.error("Kolom 'tsunami' tidak ditemukan")
    st.stop()

# Kita bagi jadi 2 kolom: kolom kiri untuk tabel (lebar kecil), kolom kanan dikosongkan
col_tabel, col_kosong = st.columns([1, 2]) 

with col_tabel:
    # Menghitung data
    tsunami_count = df["tsunami"].value_counts().reset_index()
    tsunami_count.columns = ['Status', 'Jumlah']
    
    # Menampilkan tabel di kolom yang sempit supaya angka & teks berdekatan
    st.dataframe(tsunami_count, hide_index=True, use_container_width=True)

# Definisikan variabel untuk grafik agar tidak error
status = tsunami_count['Status'].astype(str)
jumlah = tsunami_count['Jumlah'].values

# Visualisasi
st.subheader("Grafik Potensi Tsunami")

# Warna Bar + Peta
warna_bar = []
for s in status:
    if s.lower() == "ya":
        warna_bar.append("#ef240e")   
    else:
        warna_bar.append("#00ac48")   

fig, ax = plt.subplots(figsize=(6, 4))

bars = ax.bar(status, jumlah, color=warna_bar)

# kasih angka di atas bar
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        str(int(height)),
        ha='center',
        va='bottom',
        fontsize=10
    )

ax.set_xlabel("Status Tsunami")
ax.set_ylabel("Jumlah Kejadian")
ax.set_title("Distribusi Potensi Tsunami")

st.pyplot(fig)

# Peta Potensi Tsunami
st.subheader("Peta Status Potensi Tsunami")
def warna_tsunami(val):
    if val in ["ya", "1", "yes", "true"]:
        return "#ed160a"
    else:
        return "#2DDA23"

# pastikan latitude & longitude angka
df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

# buang data kosong
df_map = df.dropna(subset=["latitude", "longitude", "tsunami"])

# titik tengah peta
map_center = [
    df_map["latitude"].mean(),
    df_map["longitude"].mean()
]

# buat peta
m = folium.Map(location=map_center, zoom_start=5)

# warna berdasarkan status tsunami
for _, row in df_map.iterrows():
    status = str(row["tsunami"]).lower()

    if status == "ya":
        warna = "#ef240e"   
    else:
        warna = "#00ac48"


    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=5,                 
        color=None,               
        fill=True,
        fill_color=warna,
        fill_opacity=0.7,         
        popup=f"Status Tsunami: {row['tsunami']}"
    ).add_to(m)

st_folium(m, width=800, height=500)

#Keterangan
st.markdown("**Keterangan:**")
st.markdown(
        """
        - 🔴 *Berpotensi*
        - 🟢 *Tidak Berpotensi*
        """
    )
