import streamlit as st

# Overview
dashboardPage = st.Page("overview/dashboard.py", title="Dashboard", icon=":material/dashboard:")

# Temporal Analysis
earthquakePage = st.Page("visualization/eq_trend.py", title="Earthquake Trend", icon=":material/line_axis:")

# Magnitude & Depth
magnitudeDistributionPage = st.Page("visualization/eq_magnitude_distribution.py", title="Magnitude Distribution", icon=":material/stacked_bar_chart:")
depthCategoryPage = st.Page("visualization/eq_depth_category_percentage.py", title="Depth Category", icon=":material/bar_chart:")
magnitudeDepthPage = st.Page("visualization/eq_magnitude_vs_depth.py", title="Magnitude vs Depth", icon=":material/scatter_plot:")

# Impact & Risk
tsunamiPotentialPage = st.Page("visualization/eq_tsunami_potential.py", title="Tsunami Potential", icon=":material/waves:")

# Correlation Analysis
magnitudeDepthSignificancePage = st.Page("visualization/eq_magnitude_depth_significance.py", title="Magnitude-Depth-Significance", icon=":material/schema:")

# Spatial Analysis
gisPage = st.Page("gis/gis.py", title="GIS", icon=":material/map:")

pg = st.navigation(
    {
        "Overview" : [dashboardPage],
        "Temporal Analysis" : [earthquakePage],
        "Magnitude & Depth" : [magnitudeDistributionPage, depthCategoryPage, magnitudeDepthPage],
        "Impact & Risk" : [tsunamiPotentialPage],
        "Correlation Analysis" : [magnitudeDepthSignificancePage],
        "Spatial Analysis" : [gisPage]
    }
)

pg.run()