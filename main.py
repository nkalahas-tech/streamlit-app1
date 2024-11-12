import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
data = pd.read_csv('pbp-2024.csv')

# -------------------------
# App Layout and Structure
# -------------------------

# 1. Introduction
st.title("NFL Play-by-Play Data Explorer")
st.write("""
Welcome to the NFL Play-by-Play Data Explorer! This app allows you to dive into detailed NFL play-by-play data from the current 2024 season. 
Explore team strategies, play types, and game trends interactively. Use the sidebar to filter the dataset, and scroll down for visual insights 
and summary statistics.
""")

# 2. Dataset Overview and Filtering
st.header("Dataset Exploration")

st.write("""
Use the sidebar filters to narrow down the dataset by season, team, and quarter. 
These filters help you focus on specific teams or scenarios in the game, such as analyzing how teams perform in particular quarters or seasons.
""")

# Sidebar Filters
season = st.sidebar.selectbox("Select Season", sorted(data["SeasonYear"].unique()), index=len(data["SeasonYear"].unique()) - 1)
team = st.sidebar.multiselect("Select Team(s)", sorted(data["OffenseTeam"].unique()))
quarter = st.sidebar.select_slider("Select Quarter", options=sorted(data["Quarter"].unique()))

# Apply Filters to Data
filtered_data = data[
    (data["SeasonYear"] == season) &
    (data["OffenseTeam"].isin(team) if team else True) &
    (data["Quarter"] == quarter if quarter else True)
]

# Display Filtered Dataset
st.subheader("Filtered Data Preview")
st.write("Here is a preview of the dataset based on your selected filters:")
st.dataframe(filtered_data)

# 3. Interactive Visualizations
st.header("Visualize the Data")

st.write("""
Explore visual trends in the filtered data. Use the following charts to analyze different aspects of the plays, such as play type distribution, 
yard line tendencies, and quarter performance. 
""")

# Play Type Distribution
st.subheader("Play Type Distribution")
st.write("This bar chart shows the breakdown of different play types (e.g., rush, pass) for the selected teams and game parameters.")
play_type_counts = filtered_data["PlayType"].value_counts()
fig_play_type = px.bar(play_type_counts, x=play_type_counts.index, y=play_type_counts.values, title="Play Type Distribution")
st.plotly_chart(fig_play_type)

# Yard Line Analysis
st.subheader("Yard Line Analysis")
yard_line = st.slider("Select Yard Line to Analyze", int(data["YardLine"].min()), int(data["YardLine"].max()))
yard_line_data = filtered_data[filtered_data["YardLine"] == yard_line]
st.write(f"Showing plays at Yard Line {yard_line}:")
st.dataframe(yard_line_data)

st.subheader("Top 5 Most Common Penalties")

# Count penalties and get the top 5
penalty_data = filtered_data["PenaltyType"].value_counts().head(5)

# Plot the data
fig_penalty = px.bar(
    penalty_data,
    x=penalty_data.index,
    y=penalty_data.values,
    title="Top 5 Most Common Penalties",
    labels={"y": "Count", "index": "Penalty Type"}
)

st.plotly_chart(fig_penalty)

# 4. Summary Statistics and Key Insights
st.header("Key Insights and Summary Statistics")

st.write("""
This section provides summary statistics and key insights based on your selections. You can see metrics like average yards per play, 
touchdown rates, and penalty counts. This summary offers a high-level view of team and game performance.
""")

# Summary Statistics
avg_yards = filtered_data["Yards"].mean()
touchdown_rate = (filtered_data["IsTouchdown"].sum() / len(filtered_data)) * 100
penalty_count = filtered_data["IsPenalty"].sum()

st.metric("Average Yards per Play", f"{avg_yards:.2f}")
st.metric("Touchdown Rate", f"{touchdown_rate:.2f}%")
st.metric("Total Penalties", penalty_count)

# 5. Download Option for Filtered Data
st.subheader("Download Filtered Data")
st.write("You can download the filtered data for further analysis.")
st.download_button("Download Filtered Data", data=filtered_data.to_csv(index=False), file_name="filtered_nfl_data.csv")
