from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def getFilePath(type, file_name):
    basePath = Path(__file__).parent.parent
    file_path = basePath / "data" / type / file_name

    return file_path

def magnitudeDepthScatter(file_path) :
    data = pd.read_csv(file_path, sep=";", decimal=",", encoding="utf-8-sig")

    # depth kategori
    dangkal = data[data["depth"] < 70]
    menengah = data[(data["depth"] >= 70) & (data["depth"] <= 300)]
    dalam = data[data["depth"] > 300]
    
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.scatter(dangkal["depth"], dangkal["magnitude"], c="red", label="Dangkal (<70km)", alpha=0.7)
    ax.scatter(menengah["depth"], menengah["magnitude"], c="gold", label="Menengah (70-300km)", alpha=0.7)
    ax.scatter(dalam["depth"], dalam["magnitude"], c="green", label="Dalam (>300km)", alpha=0.7)

    ax.set_xlabel("Kedalaman (km)", fontsize="13")
    ax.set_ylabel("Magnitudo", fontsize="13")
    ax.set_title("Magnitudo vs Kedalaman", loc="left", fontsize="16", y=1.03)
    ax.legend(title="Kategori Kedalaman", fontsize="small", framealpha=0, title_fontsize="medium", columnspacing=4.0)
    ax.grid(alpha=0.2)

    return fig

def magnitudeDepthDataframe(file_path) :
    data = pd.read_csv(file_path, sep=";", decimal=",", encoding="utf-8-sig")
    df = pd.DataFrame(data)

    return df

file_path = getFilePath("clean", "earthquake_1201_cleaned_final.csv")

st.set_page_config(
    page_title="Magnitudo vs Kedalaman",
    layout="wide"
)

st.header("Magnitudo vs Kedalaman")
st.write("Berdasarkan scatter plot Magnitudo vs Kedalaman, terlihat bahwa sebagian besar gempa terjadi pada kedalaman dangkal (<100 km) dengan variasi magnitudo yang lebih besar. Gempa bermagnitudo tinggi umumnya terjadi di kedalaman rendah, sedangkan gempa dalam cenderung memiliki magnitudo lebih stabil dan lebih kecil.")

tab1, tab2 = st.tabs(["Scatter Plot", "Data"])

with tab1:
    fig = magnitudeDepthScatter(file_path)
    st.pyplot(fig, use_container_width="true")
with tab2:
    df = magnitudeDepthDataframe(file_path)
    st.dataframe(df, hide_index="true", column_order=("place", "city", "country", "magnitude", "depth_km"))