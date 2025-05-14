import streamlit as st
import pandas as pd
import altair as alt

# Load cleaned data
df = pd.read_csv("cache/storm_data_2024_filtered.csv")

# Sidebar: Event type selection
all_events = sorted(df["EVENT_TYPE"].unique().tolist())
default_event = all_events[0]
selected_events = st.sidebar.multiselect("Select event types (storm types):", all_events, default=[default_event])

# Sidebar: Exact column selection
numeric_columns = [
    "INJURIES_DIRECT", "INJURIES_INDIRECT",
    "DEATHS_DIRECT", "DEATHS_INDIRECT",
    "DAMAGE_PROPERTY", "DAMAGE_CROPS"
]
selected_column = st.sidebar.selectbox("Select a variable to visualize:", numeric_columns)

# Filter data by selected event types
filtered_df = df[df["EVENT_TYPE"].isin(selected_events)].copy()

# Ensure MONTH_NAME is ordered correctly
month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
filtered_df["MONTH_NAME"] = pd.Categorical(filtered_df["MONTH_NAME"], categories=month_order, ordered=True)

# Monthly summary
monthly_summary = (
    filtered_df.groupby(["EVENT_TYPE", "MONTH_NAME"])[selected_column]
    .sum()
    .reset_index()
    .sort_values("MONTH_NAME")
    .rename(columns={selected_column: "VALUE"})
)

# Total summary per event type
total_summary = (
    filtered_df.groupby("EVENT_TYPE")[selected_column]
    .sum()
    .reset_index()
    .rename(columns={selected_column: "TOTAL"})
)

# Main content
st.title("Storm Events Dashboard by Event Type")
st.markdown(f"### Monthly {selected_column} by Event Type")

# Line chart
line_chart = alt.Chart(monthly_summary).mark_line(point=True).encode(
    x=alt.X("MONTH_NAME", title="Month"),
    y=alt.Y("VALUE", title=selected_column),
    color=alt.Color("EVENT_TYPE", title="Event Type"),
    tooltip=["EVENT_TYPE", "MONTH_NAME", "VALUE"]
).properties(
    width=800,
    height=400
)
st.altair_chart(line_chart, use_container_width=True)

# Bar chart for totals
st.markdown(f"### Total {selected_column} by Event Type")

bar_chart = alt.Chart(total_summary).mark_bar().encode(
    x=alt.X("EVENT_TYPE", sort="-y", title="Event Type"),
    y=alt.Y("TOTAL", title=f"Total {selected_column}"),
    color=alt.Color("EVENT_TYPE", legend=None),
    tooltip=["EVENT_TYPE", "TOTAL"]
).properties(
    width=800,
    height=300
)
st.altair_chart(bar_chart, use_container_width=True)
