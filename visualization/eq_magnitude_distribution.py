import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import csv

st.title("Magnitude Gempa per Region")

CSV_FILE = "earthquake_1201_cleaned_final.csv"

if not os.path.exists(CSV_FILE):
    st.error(f"File tidak ditemukan: {CSV_FILE}")
    st.stop()

try:
    df = pd.read_csv(CSV_FILE, sep=";", decimal=",", encoding="utf-8-sig", engine="python", on_bad_lines='skip', quoting=csv.QUOTE_MINIMAL)
except Exception as e:
    st.error(f"Error membaca file: {e}")
    st.stop()

# Tampilkan kolom
st.subheader("Preview Data")
df_preview = df.drop(columns=['place'], errors='ignore')
st.dataframe(df_preview.head())

# Ganti nama kolom
kolom_magnitude = "magnitude" 
kolom_region = "place"         

if kolom_magnitude not in df.columns or kolom_region not in df.columns:
    st.error(f"Kolom '{kolom_magnitude}' atau '{kolom_region}' tidak ditemukan.")
else:
    df[kolom_magnitude] = pd.to_numeric(df[kolom_magnitude], errors='coerce')
    df = df.dropna(subset=[kolom_magnitude, kolom_region])

    
    # Tampilkan jumlah data setelah clean
    st.write(f"**Jumlah Data Setelah Clean:** {len(df)}")
    
    
    regions = df[kolom_region].unique()
    st.write("**Region yang Tersedia:**")  
    
    selected_region = st.selectbox("Pilih Region:", regions)
    
    df_region = df[df[kolom_region] == selected_region]
    
    # Cek data region
    st.write(f"**Jumlah Data untuk {selected_region}:** {len(df_region)}")
    st.write("**Preview Data Region:**")
    
    # Menghapus kolom 'place' agar tidak double/terlalu panjang di preview region
    df_region_preview = df_region.drop(columns=['place'], errors='ignore')
    st.dataframe(df_region_preview.head())
    
    if df_region.empty:
        st.warning(f"Tidak ada data untuk region: {selected_region}")
    else:
        # Cek tipe data magnitude
        st.write(f"**Tipe Data Magnitude:** {df_region[kolom_magnitude].dtype}")
        st.write(f"**Sample Magnitude:** {df_region[kolom_magnitude].head().tolist()}")
        
        # Histogram
        try:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.hist(df_region[kolom_magnitude], bins=20, edgecolor='black', alpha=0.7, color='skyblue')
            ax.set_title(f"Distribusi Magnitude Gempa di {selected_region}")
            ax.set_xlabel("Magnitude")
            ax.set_ylabel("Frekuensi (Jumlah Kejadian)")
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Error plotting histogram: {e}")
        
        # Info mayoritas
        mean_mag = df_region[kolom_magnitude].mean()
        mode_mag = df_region[kolom_magnitude].mode()[0] if not df_region[kolom_magnitude].mode().empty else "N/A"
        st.write(f"**Rata-rata Magnitude (Mayoritas sekitar):** {mean_mag:.2f}")
        st.write(f"**Mode Magnitude (Nilai paling sering):** {mode_mag}")
        st.write(f"**Jumlah Data:** {len(df_region)} kejadian")