import streamlit as st
import pandas as pd 
import numpy as np
import plotly.express as px 
import os
from utils.gpx_parser import load_gpx_data

st.set_page_config(layout="wide")

activities = pd.read_csv("data/garmin_activities.csv")
steps = pd.read_csv("data/garmin_steps.csv")

st.title("My New Zealand Working Holiday Journey")
#st.sidebar.title("Contents")
#section = st.sidebar.radio(
#    "Go to",
#    ["Intro", "Overview", "North Island", "Winter", "South Island"]
#)

st.markdown("""    
Kia Ora! I am Xavier, a Singaporean who left his corporate job in 2025 to embark on a year-long journey in New Zealand 
on the Working Holiday Visa (WHV) scheme. Having worked in Singapore for five years, I decided to take a leap of faith to venture abroad to experience life in ways I couldn't back in Singapore.
This journey ultimately proved to be enriching, fulfilling and it definitely broadened my horizons. 

I wanted to create this website to unpack my year of adventure in NZ and to pay tribute to the beautiful memories created along this journey - which I will always hold close to my heart.
            
In this page, I have compiled some high level figures, graphs and maps to summarize my journey.
If you are interested to read more about my journey in detail, please check out the *blog* portion! 
            """)

st.header("🇳🇿 Wrapped")

col1, col2, col3 = st.columns(3)

col1.metric("⏱️ Days in NZ", "359")
col1.caption("Almost an entire year")

col2.metric("💼 Days Worked (Hours)", "145 (1,283)")
col2.caption("40% of time spent working 💰")

col3.metric("🏂 Days Snowboarding (Runs)", "21 (263)")
col3.caption("Remarkables, Coronet Peak, Cardrona")


col4, col5, col6 = st.columns(3)

col4.metric("🚶 Distance", "3,401 km")
col4.caption("Singapore - Taiwan")

col5.metric("💼 Jobs", "7")
col5.caption("Horticulture, Hospitality and Construction")

col6.metric("🏔️ Hikes", "61")
col6.caption("Out of 1,500 hikes in NZ")

st.markdown(" ")
st.markdown(" ")

#Calendar graph
st.markdown("### 📅 Timeline Of My Year In NZ")

calendar = pd.read_csv("data/calendar.csv")
calendar["date"] = pd.to_datetime(calendar["date"])

calendar = calendar.sort_values("date").reset_index(drop=True)
calendar["day_index"] = range(len(calendar))

color_map = {
    "Work": 0,
    "Travel": 1,
    "Volunteer": 2,
    "Snowboard": 3
}

calendar["label"] = calendar["date"].dt.strftime("%b-%y")
calendar["type_num"] = calendar["type"].map(color_map)

fig = px.imshow(
    [calendar["type_num"]],  # single row
    aspect="auto"
)

fig.update_layout(
    coloraxis=dict(
        colorscale=[
            [0.00, "#E02222"], [0.24, "#E02222"],   # Work
            [0.25, "#1EFC01"], [0.49, "#1EFC01"],   # Travel
            [0.50, "#00098A"], [0.74, "#00098A"],   # Volunteer 
            [0.75, "#E775C7"], [1.00, "#E775C7"],   # Snowboard 
        ],
        cmin=0,
        cmax=3,
        colorbar=dict(
            tickvals=[0, 1, 2, 3],
            ticktext=["Work", "Travel", "Volunteer", "Snowboard"]
        )
    ),
    height=150,
    margin=dict(l=0, r=0, t=20, b=20),
    yaxis=dict(showticklabels=False)
)


month_starts = calendar.groupby("label")["day_index"].min()

fig.update_xaxes(
tickvals=list(month_starts.values),
ticktext=list(month_starts.index),
tickangle=0
)

fig.update_layout(
    coloraxis_colorbar=dict(
        tickvals=[0, 1, 2, 3],
        ticktext=["Work", "Travel", "Volunteer", "Snowboard"],
        len=0.8,              # makes it taller
        thickness=20,         # wider bar
        tickfont=dict(size=12)
    )
)

for x in month_starts.values:
    fig.add_vline(x=x, line_width=1, line_dash="dot", opacity=0.3)

st.plotly_chart(fig, use_container_width=True)

st.markdown(" ")

#Breakdown of jobs and volunteering 
jobs = {
    "Job": ["Kiwifruit Picking", "Kiwifruit Packing", "F&B Attendant", "General Labour", "Housekeeping", "Onion Seed Harvesting", "Cherry Picking"],
    "Location": ["Te Puke", "Te Puke", "Queenstown", "Queenstown", "Queenstown", "Ashburton", "Cromwell"],
    "Industry": ["Horticulture", "Horticulture", "Hospitality", "Construction & Building", "Hospitality", "Horticulture", "Horticulture"]
}

volunteer = {
    "Type": ["Lifestyle Block", "Livestock Farm", "Lifestyle Block", "Dog Breeding Farm"],
    "Location": ["Levin", "Seddon", "Christchurch", "Clarkville"],
    "Duties": ["Gardening, Lawn Mowing", "Herding, Gardening, Cooking", "Gardening, Babysitting", "Painting, Cleaning"]
}

jobs_df = pd.DataFrame(jobs)
volunteer_df = pd.DataFrame(volunteer)

col1, col2 = st.columns(2)
with col1:
    st.caption("**Jobs**")
    st.dataframe(jobs_df, hide_index=True)

with col2:
    st.caption("**Volunteering**")
    st.dataframe(volunteer_df, hide_index=True)

st.markdown(" " \
"")


###Activity Section
#Hiking map
st.subheader("📍 Hiking Activity Map")

island_choice = st.radio(
    "",
    ["North Island", "South Island"],
    horizontal=True
)
st.caption(f"Showing {island_choice} activities, hover for more details")

df = load_gpx_data()
df_filtered = df[df["island"] == island_choice]
if island_choice == "North Island":
    center = {"lat": -38.5, "lon": 175.5}
    zoom = 6.0
else:
    center = {"lat": -43.5, "lon": 168.5}
    zoom = 6.0


activities["activity"] = activities["activity"].str.lower().str.strip()
df["activity"] = df["activity"].str.lower().str.strip()

df_merged = df.merge(activities, on="activity", how="left")
df_merged["activity_display"] = (df_merged["activity"].str.replace("_", " ").str.title())
df_merged.to_csv("merged_data.csv")

fig = px.line_mapbox(
    df_merged,
    lat="lat",
    lon="lon",
    color="activity",
    color_discrete_sequence=["#FF4B4B"],
    height=700,
    hover_name="activity_display",
    hover_data={
        "Distance (km)": True,
        "Time": True,
        "Total Ascent (m)": True,
        "Steps": True,
        "lat": False,
        "lon": False,
        "activity": False,
    }
)

fig.update_traces(line=dict(width=7), opacity=0.9)

fig.update_layout(
    mapbox_style="open-street-map",
    mapbox_center=center,
    mapbox_zoom=zoom,
    margin={"r":0,"t":0,"l":0,"b":0},
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

#Distance v elevation scatter plot 
hiking_df = activities[activities["Activity Type"] == "Hiking"]
hiking_df['activity_title'] = hiking_df['activity'].str.title()

fig = px.scatter(
hiking_df,
x="Distance (km)",
y="Total Ascent (m)",
hover_name="activity_title",
title="Hikes: By elevation and distance"
)
st.plotly_chart(fig, use_container_width=True)


#new graph testing
#activities["Date"] = pd.to_datetime(activities["Date"])

#monthly = activities.groupby([
#    activities["Date"].dt.month,
#    "Activity Type"
#]).size().reset_index(name="count")

#fig = px.bar(
#    monthly,
#    x="Date",
#    y="count",
#    color="Activity Type",
#    title="Activities by Month"
#)

#st.plotly_chart(fig, use_container_width=True)

#another chart 
#top = activities.sort_values("Total Ascent (m)", ascending=False).head(10)

#fig = px.bar(
#    top,
#    x="Total Ascent (m)",
#    y="activity",
#    orientation="h",
#    title="Top 10 Toughest Hikes"
#)

#st.plotly_chart(fig, use_container_width=True)


#fav hikes
st.markdown("### 👣 My Favourite Hikes")

st.markdown("#### Routeburn Tack to Harris Saddle | 9.5/ 10 | Fiordland National Park | 23.54km")
st.write("")

st.markdown("#### Lake Marian Track | 9.5/ 10 | Fiordland National Park | 6.94km")
st.write("")

st.markdown("#### Tongariro Alpine Crossing | 9/ 10 | Tongariro National Park | 20.54km")
st.write("")

st.markdown("#### Rob Roy Glacier Tack | 9/ 10 | Mount Aspiring National Park | 23.54km")
st.write("")

st.markdown("#### Mount Sunday Track | 9/ 10 | Ashburton Lakes | 2.01km")
st.write("")
