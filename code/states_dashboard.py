import streamlit as st
import pandas as pd
import altair as alt

# Load cleaned data
df = pd.read_csv("cache/storm_data_2024_filtered.csv")

# Sidebar: State selection
all_states = df["STATE"].unique().tolist()
default_state = all_states[0]
selected_states = st.sidebar.multiselect("Select states:", all_states, default=[default_state])

# Sidebar: Exact column selection
numeric_columns = [
    "INJURIES_DIRECT", "INJURIES_INDIRECT",
    "DEATHS_DIRECT", "DEATHS_INDIRECT",
    "DAMAGE_PROPERTY", "DAMAGE_CROPS"
]
selected_column = st.sidebar.selectbox("Select a variable to visualize:", numeric_columns)

# Filter data by selected states
filtered_df = df[df["STATE"].isin(selected_states)].copy()

# Ensure MONTH_NAME is ordered correctly
month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
filtered_df["MONTH_NAME"] = pd.Categorical(filtered_df["MONTH_NAME"], categories=month_order, ordered=True)

# Monthly summary
monthly_summary = (
    filtered_df.groupby(["STATE", "MONTH_NAME"])[selected_column]
    .sum()
    .reset_index()
    .sort_values("MONTH_NAME")
    .rename(columns={selected_column: "VALUE"})
)

# Total summary per state
total_summary = (
    filtered_df.groupby("STATE")[selected_column]
    .sum()
    .reset_index()
    .rename(columns={selected_column: "TOTAL"})
)

# Main content
st.title("Storm Events Dashboard")
st.markdown(f"### Monthly {selected_column} by State")

# Line chart
line_chart = alt.Chart(monthly_summary).mark_line(point=True).encode(
    x=alt.X("MONTH_NAME", title="Month"),
    y=alt.Y("VALUE", title=selected_column),
    color=alt.Color("STATE", title="State"),
    tooltip=["STATE", "MONTH_NAME", "VALUE"]
).properties(
    width=800,
    height=400
)
st.altair_chart(line_chart, use_container_width=True)

# Bar chart for totals
st.markdown(f"### Total {selected_column} by State")

bar_chart = alt.Chart(total_summary).mark_bar().encode(
    x=alt.X("STATE", sort="-y", title="State"),
    y=alt.Y("TOTAL", title=f"Total {selected_column}"),
    color=alt.Color("STATE", legend=None),
    tooltip=["STATE", "TOTAL"]
).properties(
    width=800,
    height=300
)
st.altair_chart(bar_chart, use_container_width=True)
