import streamlit as st
import pandas as pd
import plotly.express as px

# Load cleaned storm data
df = pd.read_csv("cache/storm_data_2024_filtered.csv")

# Sidebar: metric selector
metric = st.sidebar.selectbox(
    "Select a metric to visualize on the US map:",
    [
        "DAMAGE_PROPERTY", "DAMAGE_CROPS",
        "INJURIES_DIRECT", "INJURIES_INDIRECT",
        "DEATHS_DIRECT", "DEATHS_INDIRECT"
    ]
)

# Group by state and calculate total value
state_summary = (
    df.groupby(["state", "STATE"])[metric]
    .sum()
    .reset_index()
    .rename(columns={metric: "VALUE"})
)

# Title
st.title("Storm Impact by US State")
st.markdown(f"### Total {metric.replace('_', ' ').title()} by State (2024)")

# Plotly choropleth map
fig = px.choropleth(
    state_summary,
    locations="state",               # two-letter state code
    locationmode="USA-states",
    color="VALUE",
    hover_name="STATE",
    color_continuous_scale="Reds",
    scope="usa",
    labels={"VALUE": metric.replace('_', ' ').title()},
)

fig.update_layout(
    geo=dict(bgcolor='rgba(0,0,0,0)'),
    margin={"r":0,"t":30,"l":0,"b":0}
)

st.plotly_chart(fig, use_container_width=True)
