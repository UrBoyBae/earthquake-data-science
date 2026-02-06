import streamlit as st

# Overview
dashboardPage = st.Page("overview/dashboard.py", title="Dashboard", icon=":material/dashboard:")

# Temporal Analysis
earthquakePage = st.Page("visualization/eq_trend.py", title="Tren Gempa Bumi", icon=":material/line_axis:")

# Magnitude & Depth
magnitudeDistributionPage = st.Page("visualization/eq_magnitude_distribution.py", title="Distribusi Magnitudo Gempa", icon=":material/stacked_bar_chart:")
depthCategoryPage = st.Page("visualization/eq_depth_category_percentage.py", title="Kategori Kedalaman", icon=":material/bar_chart:")
magnitudeDepthPage = st.Page("visualization/eq_magnitude_vs_depth.py", title="Magnitudo vs Kedalaman", icon=":material/scatter_plot:")

# Impact & Risk
tsunamiPotentialPage = st.Page("visualization/eq_tsunami_potential.py", title="Potensi Tsunami", icon=":material/waves:")

# Correlation Analysis
magnitudeDepthSignificancePage = st.Page("visualization/eq_magnitude_depth_significance.py", title="Magnitudo-Kedalaman-DampakGempa", icon=":material/schema:")

# Spatial Analysis
gisPage = st.Page("gis/gis.py", title="GIS", icon=":material/map:")

pg = st.navigation(
    {
        "Ringkasan" : [dashboardPage],
        "Analisis Temporal" : [earthquakePage],
        "Magnitudo vs Kedalaman" : [magnitudeDistributionPage, depthCategoryPage, magnitudeDepthPage],
        "Dampak & Risiko" : [tsunamiPotentialPage],
        "Analisis Korelasi" : [magnitudeDepthSignificancePage],
        "Analisis Spasial" : [gisPage]
    }
)

pg.run()