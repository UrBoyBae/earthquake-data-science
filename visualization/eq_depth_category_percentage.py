import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# File CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "..", "data", "clean", "earthquake_1201_cleaned_final.csv")

# ================= LOAD DATA =================
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_FILE, sep=';')

    # Ubah ke numerik agar tidak error perbandingan
    df["sig"] = pd.to_numeric(df["sig"], errors="coerce")

    # Kategori signifikansi
    df["sig_category"] = df["sig"].apply(
        lambda x: "Rendah" if pd.notna(x) and x < 500 
        else "Sedang" if pd.notna(x) and x < 1000 
        else "Tinggi"
    )

    df['depth_category'] = df['depth_category'].astype(str).str.strip().str.title()
    df['country'] = df['country'].astype(str).str.strip()

    return df

df = load_data()

# ================= HALAMAN =================
st.set_page_config(layout="wide", page_title="Analisis Kedalaman Gempa")
st.title("📊 Analisis Karakteristik Kedalaman Gempa per Negara")

# ================= FILTER =================
st.subheader("🗺️ Filter Data")

col1, col2 = st.columns(2)

with col1:
    countries = sorted(df['country'].dropna().unique())
    selected_countries = st.multiselect(
        "Pilih negara (kosong = semua negara):",
        countries
    )

with col2:
    min_events = st.slider(
        "Minimal jumlah gempa per negara",
        0, 200, 0
    )

# ================= VISUALISASI =================
def plot_kedalaman_gempa(region_list=None, min_events=0):

    df_filtered = df[df['depth_category'].isin(['Dangkal', 'Menengah', 'Dalam'])]

    if region_list:
        df_filtered = df_filtered[df_filtered['country'].isin(region_list)]

    if df_filtered.empty:
        st.warning("Tidak ada data setelah filter.")
        return

    ct_all = pd.crosstab(df_filtered['country'], df_filtered['depth_category'])
    ct_all['Total'] = ct_all.sum(axis=1)

    if min_events > 0:
        ct_all = ct_all[ct_all['Total'] >= min_events]

    if ct_all.empty:
        st.warning("Tidak ada negara yang memenuhi minimal jumlah kejadian.")
        return

    ct_all_pct = ct_all.reindex(columns=['Dangkal', 'Menengah', 'Dalam'], fill_value=0)
    ct_all_pct = ct_all_pct.div(ct_all['Total'], axis=0) * 100
    ct_all_pct = ct_all_pct.sort_values(by='Dangkal', ascending=False)

    # ================= PLOT =================
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(14, 8))

    ct_all_pct.plot(kind='bar', ax=ax, color=['#2E86C1', '#F1C40F', '#C0392B'], edgecolor='white')
    ax.set_title('Perbandingan Karakteristik Kedalaman Gempa per Negara', fontsize=14, fontweight='bold')
    ax.set_ylabel('Proporsi (%)')

    labels_all = [f"{c}\n(n={int(ct_all.loc[c, 'Total'])})" for c in ct_all_pct.index]
    ax.set_xticklabels(labels_all, rotation=45, ha='right')

    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f'{height:.0f}%',
                        (p.get_x() + p.get_width()/2, height + 1),
                        ha='center', va='bottom',
                        fontsize=8, fontweight='bold')

    ax.legend(title='Kategori Kedalaman')
    ax.set_ylim(0, 100)

    plt.tight_layout()
    st.pyplot(fig)

# ================= JALANKAN =================
plot_kedalaman_gempa(selected_countries if selected_countries else None, min_events)
