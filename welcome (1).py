
import pandas as pd
import folium
from streamlit_folium import st_folium
import streamlit as st
import matplotlib.pyplot as plt

# Load data
# df = pd.read_csv("Loan-Portfolio-data.csv")
df = pd.read_csv("Loan-Portfolio-Mapping-Data-2.csv")

st.title("Loan Portfolio Map Dashboard")

# Filters
state_filter = st.multiselect(
    "Select State",
    options=df["State"].unique(),
    default=df["State"].unique()
)

area_filter = st.multiselect(
    "Select Area",
    options=df["Area"].unique(),
    default=df["Area"].unique()
)

city_filter = st.multiselect(
    "Select Branch",
    options=df["Branch"].unique(),
    default=df["Branch"].unique()
)

status_filter = st.multiselect(
    "Select Status",
    options=df["Status"].unique(),
    default=df["Status"].unique()
)

dpd_range = st.slider(
    "Select DPD Range",
    min_value=int(df["DPD"].min()),
    max_value=int(df["DPD"].max()),
    value=(0, 90)
)

asset_range = st.slider(
    "Select Property Range",
    min_value=int(df["Asset_Colleteral_Value"].min()),
    max_value=int(df["Asset_Colleteral_Value"].max()),
    value=(100000, 2000000)
)

# filtered_df = df[
#     (df["DPD"] >= dpd_range[0]) &
#     (df["DPD"] <= dpd_range[1])
# ]

# Apply filters
filtered_df = df[
    (df["State"].isin(state_filter)) &
    (df["Area"].isin(area_filter)) &
    (df["Branch"].isin(city_filter)) &
    (df["Status"].isin(status_filter)) &
    # (df["DPD"].isin(filtered_df))
    (df["DPD"] >= dpd_range[0]) &
    (df["DPD"] <= dpd_range[1]) &
    (df["Asset_Colleteral_Value"] >= asset_range[0]) &
    (df["Asset_Colleteral_Value"] <= asset_range[1])
    ]

# Create map
m = folium.Map(location=[22.5, 78.9], zoom_start=5)
st_folium(m,width = 700)

# color_map = {
#     "A": "green",
#     "C": "gray",
#     "X": "red"
# }

color_map = {
    "NCR": "green",
    "HR": "gray",
    "RJ-UP-1": "Yellow",
    "RJ-UP-2": "Purple",
    "RJ-UP-3": "Blue",
    "AP": "Brown",
    "MP": "Cyan",
    "Telangana": "orange",
    "UK & UP": "Pink"
}

def risk_color(dpd):
    if dpd == 0:
        return "green"
    elif dpd <= 30:
        return "yellow"
    elif dpd <= 60:
        return "orange"
    elif dpd <= 90:
        return "red"
    else:
        return "darkred"

def circle_redius(Asset_Colleteral_Value):
    if Asset_Colleteral_Value <= 1000000:
        return 4
    elif Asset_Colleteral_Value <= 2000000:
        return 6
    elif Asset_Colleteral_Value <= 3000000:
        return 8
    else:
        return 10

# Plot points
for _, row in filtered_df.iterrows():
    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=circle_redius(row["Asset_Colleteral_Value"]),
        # radius=6,
        # color=color_map[row["Status"]],
        color=color_map[row["State"]],
        fill=True,
        fill_color=risk_color(row["DPD"]),
        fill_opacity=0.7,
        # popup=f"{row['City']} | {row['Status']}"
        # popup=f"{row['Branch']} | {row['Status']}"
        popup = f"{row['Branch']} | {row['Status']} | {row['DPD']}"
    ).add_to(m)

m.save("risk_map.html")

# heat_data = filtered[filtered["DPD"] > 90][["Latitude", "Longitude"]].values
# HeatMap(heat_data).add_to(m)

legend_html = '''
<div style="
position: fixed; 
bottom: 10px; left: 10px; width: 200px; height: 150px; 
background-color: white; 
border:2px solid grey; z-index:9999; font-size:14px;
padding: 10px;
">
<b>DPD Risk Level</b><br>
<span style="color:green;">●</span> Current<br>
<span style="color:yellow;">●</span> 1–30 DPD<br>
<span style="color:orange;">●</span> 31–60 DPD<br>
<span style="color:red;">●</span> 61–90 DPD<br>
<span style="color:darkred;">●</span> 90+ DPD
</div>
'''

m.get_root().html.add_child(folium.Element(legend_html))

# Show map
st.components.v1.html(m._repr_html_(), height=600)
