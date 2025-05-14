# About My Project

Student Name:  josh elman
Student Email:  jdelman@syr.edu

### What it does


In this project, we will create a streamlit dashboard to visualize our data. This dashboard provides an interactive visualization of storm events across the United States in the year 2024, based on data from the National Weather Service's Storm Events Database. It allows users to explore the human and economic impact of various severe weather phenomena—including tornadoes, floods, hurricanes, thunderstorms, and more—throughout the year.

Specifically, the dashboard enables users to:

* **Analyze injuries** (both direct and indirect) caused by storms, filtered by storm type, state, and month.
* **Explore fatalities** (direct and indirect) associated with different weather events across states and over time.
* **Visualize property and crop damage**, showing the financial impact of storms by category and location.
* **View a U.S. map** displaying average injuries, deaths, and damages by state, offering a geographic perspective on storm severity.

This tool is designed to support emergency planners, researchers, and the general public in understanding the scope and distribution of storm impacts, helping to inform disaster preparedness and response efforts.

**Data Source:**
[NOAA Storm Events Database on Data.gov](https://catalog.data.gov/dataset/storm-events-database)



### How you run my project


This project provides interactive dashboards for exploring storm event data in the United States. It includes tools to visualize injuries, deaths, and property/crop damages by **state**, **storm type**, and on a **US map**. First, install the required Python packages: using this command `pip install -r requirements.txt`. Run the data processing script to clean and prepare the storm dataset
using this command: `python get_data.py`

This script

* Loads storm data from `cache/storm_data_2024.csv`
* Filters required columns and valid state FIPS codes
* Converts damage fields to numeric USD values
* Merges state-level coordinate data
* Outputs cleaned data to `cache/storm_data_2024_filtered.csv`


### Visualize by State

You can launch any of the dashboards using Streamlit using this command `streamlit run states_dashboard.py`. The dashboard compares multiple states, Select metric (injuries, deaths, damages) by visualizing Line plot by month and barplot of Total values by state (bar plot)



###  Visualize by Storm Type

The dashboard for storm type can be initiated by running `streamlit run storm_dashboard.py`. This interactive dashboard compares multiple storm types by Select metric (injuries, deaths, damages) and visualize lineplot of totals by Monthly trends. 


###  Visualize on US Map
To visualize interactive map run this script `streamlit run map_dashboard.py`. You can View total injuries, deaths, or damages by state in a choropleth map. 



### Other things you need to know