import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os


# File CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "..", "data", "clean", "earthquake_1201_cleaned_final.csv")
data = pd.read_csv(CSV_FILE, sep=";", decimal=",", encoding="utf-8-sig")

st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

st.title("Dashboard")
data["time"] = pd.to_datetime(data["time"])
waktu_terawal = data["time"].min()

st.caption("Pemantauan aktivitas seismik sejak " + waktu_terawal.strftime("%B %Y"))

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Gempa Bumi", len(data), "Sejak " + waktu_terawal.strftime("%B %Y"), delta_arrow="off", delta_color="inverse", border=True)

data["magnitude"] = pd.to_numeric(data["magnitude"], errors="coerce")
idx_mag_max = data["magnitude"].idxmax()
magnitude_max = data.loc[idx_mag_max]
col2.metric("Magnitudo Terbesar", magnitude_max["magnitude"], magnitude_max["city"] + ", " + magnitude_max["country"], delta_arrow="off", delta_color="inverse", border=True)

data["depth"] = pd.to_numeric(data["depth"], errors="coerce")
idx_depth_max = data["depth"].idxmax()
depth_max = data.loc[idx_depth_max]
col3.metric("Gempa Bumi Terdalam", f"{int(depth_max["depth"])} km", depth_max["city"] + ", " + depth_max["country"], delta_arrow="off", delta_color="inverse", border=True)

data["tsunami"] = (
    data["tsunami"]
    .astype(str)
    .str.strip()
    .str.lower()
)
jumlah_tsunami = (data["tsunami"] == "ya").sum()
col4.metric("Berpotensi Tsunami", jumlah_tsunami, "Bahaya Tsunami", delta_arrow="off", delta_color="inverse", border=True)

col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Peta Gempa Bumi Terbaru")

    m = folium.Map(location=[20, 0], zoom_start=1)

    latest_5_eq = data.sort_values("time", ascending=False).head(5)

    for _, row in latest_5_eq.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=8,
            color="red",
            fill=True,
            fill_opacity=0.75,
            popup=f"""
            <b>Negara:</b> {row.get('country', 'Tidak diketahui')}<br>
            <b>Waktu:</b> {row['time'].strftime('%d %B %Y %H:%M')}
            <b>Magnitudo:</b> {row.get('magnitude', '-')}<br>
            <b>Kedalaman:</b> {row.get('depth', '-')} km<br>
            <b>Skor Dampak:</b> {row.get('sig', '-')}<br>
            <b>Potensi Tsunami:</b> {row.get('tsunami', '-')}<br>
            """
        ).add_to(m)

    st_folium(m, width="100%", height=300)

with col2:
    st.subheader("Tips Keselamatan")

    st.markdown("""
    - Berlindung dengan posisi **menunduk, lindungi kepala, dan berpegangan** di bawah meja atau furnitur yang kokoh  
    - Jauhi jendela, kaca, dan benda-benda yang mudah jatuh atau roboh  
    - Lindungi kepala dan leher dari kemungkinan runtuhan atau serpihan  
    - Jika berada di luar ruangan, menjauhlah dari bangunan, tiang listrik, dan pohon  
    - Siapkan **perlengkapan darurat** seperti P3K, senter, air minum, dan makanan siap saji  
    """)
