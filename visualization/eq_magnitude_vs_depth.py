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

    dataDepth = data["depth"].to_numpy()
    dataMagnitude = data["magnitude"].to_numpy()
    
    fig, ax = plt.subplots()
    ax.scatter(dataDepth, dataMagnitude)
    ax.set_xlabel("Depth (km)")
    ax.set_ylabel("Magnitude")
    ax.set_title("Magnitude vs Depth")

    return fig

file_path = getFilePath("clean", "earthquake_1201_cleaned_final.csv")
fig = magnitudeDepthScatter(file_path)
st.pyplot(fig)