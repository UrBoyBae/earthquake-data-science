from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.lines import Line2D

def getFilePath(type, file_name):
    basePath = Path(__file__).parent.parent
    file_path = basePath / "data" / type / file_name

    return file_path

def magnitudeDepthSignificanceDataframe(file_path) :
    data = pd.read_csv(file_path, sep=";", decimal=",", encoding="utf-8-sig")
    df = pd.DataFrame(data)

    return df

def magnitudeDepthSignificanceScatter(file_path) :
    data = pd.read_csv(file_path, sep=";", decimal=",", encoding="utf-8-sig")

    dataDepth = data["depth"].to_numpy()
    dataMagnitude = data["magnitude"].to_numpy()
    dataSig = data["sig"].to_numpy()
    
    fig, ax = plt.subplots(figsize=(16, 6))
    
    scatter = ax.scatter(dataDepth, dataMagnitude, c=dataSig, cmap="RdYlGn_r")
    ax.set_xlabel("Kedalaman (km)", fontsize="13")
    ax.set_ylabel("Magnitudo", fontsize="13")
    ax.set_title("Korelasi Magnitudo, Kedalaman, Skor dampak gempa", loc="left", fontsize="16", y=1.03)
    
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Sangat Tinggi (>800)', markerfacecolor='red', markersize=8),
        Line2D([0], [0], marker='o', color='w', label='Tinggi (<800)', markerfacecolor='orange', markersize=8),
        Line2D([0], [0], marker='o', color='w', label='Sedang (<500)', markerfacecolor='yellow', markersize=8),
        Line2D([0], [0], marker='o', color='w', label='Rendah (<100)', markerfacecolor='green', markersize=8),
    ]

    ax.legend(
        handles=legend_elements,
        title="Kategori Skor Dampak",
        loc="upper right",
        fontsize="small",
        framealpha=0
    )

    ax.grid(alpha=0.2)

    fig.colorbar(scatter, label="Skor dampak gempa")

    return fig

file_path = getFilePath("clean", "earthquake_1201_cleaned_final.csv")

st.set_page_config(
    page_title="Magnitudo-Kedalaman-DampakGempa",
    layout="wide"
)

st.header("Korelasi Magnitudo, Kedalaman, Skor dampak gempa")
st.write("Berdasarkan scatter plot menunjukkan bahwa gempa dengan skor dampak gempa tinggi didominasi oleh kejadian dangkal dengan magnitudo besar. Gempa dalam cenderung memiliki skor dampak gempa rendah meskipun magnitudonya sedang. Hal ini mengindikasikan bahwa dampak gempa lebih dipengaruhi oleh kedalaman dan magnitudo secara bersamaan, bukan oleh salah satu faktor secara terpisah.")

tab1, tab2 = st.tabs(["Scatter Plot", "Data"])

with tab1:
    fig = magnitudeDepthSignificanceScatter(file_path)
    st.pyplot(fig, use_container_width="true")
with tab2:
    df = magnitudeDepthSignificanceDataframe(file_path)
    st.dataframe(df, hide_index="true", column_order=("place", "city", "country", "magnitude", "depth_km", "sig"))

