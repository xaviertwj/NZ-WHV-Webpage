import streamlit as st
import pandas as pd 
import numpy as np
import plotly.express as px 
import os
from utils.gpx_parser import load_gpx_data
from streamlit_carousel import carousel

st.components.v1.html("""
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0F2NJJP4NT"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-0F2NJJP4NT');
</script>
""")

st.set_page_config(layout="wide")
st.set_page_config(page_title="Home")

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
col4.caption("Equivalent to distance from SGP-TWN")

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
    st.markdown("##### **Jobs**")
    st.dataframe(jobs_df, hide_index=True)

with col2:
    st.markdown("##### **Volunteering**")
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

st.divider()

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

st.markdown("#### [Routeburn Track to Harris Saddle](https://www.alltrails.com/trail/new-zealand/otago/routeburn-track-to-lake-harris-and-harris-saddle-shelter) | 9.5/10 | Fiordland National Park | 23.54km | 7.2 Hours ")
st.markdown("" \
"[Routeburn Track](https://www.doc.govt.nz/parks-and-recreation/places-to-go/fiordland/places/fiordland-national-park/things-to-do/tracks/routeburn-track/)" \
" is one of the coveted Great Walks in NZ - the full track features a 33km point-to-point hike over 2-4 days. " \
"\n\nMy hike was a *truncated* version since one of the bridge was closed off due to avalanche risk. " \
"I started from Routeburn Track Car Park and turned back at the point of the bridge closure, just before Harris Saddle." \
"\n\nI've always heard others say that Routeburn is the 'best' Great Walk and honestly, it comes as no surprise. This was one of my most scenic hikes in New Zealand! " \
"Snow-capped mountains, vast valleys and occassional waterfalls await you at every corner of this track, I lost track of how many times I stopped along this track just to gaze and the scenary in awe. " \
"This is a hike that I'll strongly recommend and if you're even more adventurous, go for the full Routeburn Track!")

routeburn_pics = [
    {"title": "", "text": "", "img":"images/Routeburn/IMG_7180.JPEG",},
    {"title": "", "text": "", "img":"images/Routeburn/IMG_7181.JPEG",},
    {"title": "", "text": "", "img":"images/Routeburn/IMG_7183.JPEG",},
    {"title": "", "text": "", "img":"images/Routeburn/IMG_7195.JPEG",},
    {"title": "", "text": "", "img":"images/Routeburn/IMG_7199.JPEG",},
    {"title": "", "text": "", "img":"images/Routeburn/IMG_7211.JPEG",},
]

with st.container():
    carousel(items=routeburn_pics)
st.caption("*If the pictures fail to render fully, open and close the sidebar*")

st.divider()

st.markdown("#### [Lake Marian Track](https://www.alltrails.com/trail/new-zealand/otago/lake-marian-track) | 9.5/10 | Fiordland National Park | 6.94km | 3.5 Hours ")
st.markdown("" \
"Fiordland National Park is the biggest national park in New Zealand and home to a plethora of amazing hikes, and Lake Marian is one of them." \
"\n\nThis unsuspecting trail starts off easy, bringing you through various water features on a comfortable broadwalk. " \
"Before you know it, you'll be spending the next ~4kms navigating through a forest with uneven terrain, fallen rocks and dense trees." \
"A decent level of fitness is required to traverse through the forest, power through and you'll be rewarded with a pristine view of Lake Marian against the backdrop of a hanging valley, truly *magical*." \
"\n\nThis track is also conveniently located on the way to Milford Sound, I would highly recommend setting aside a day to do both Lake Marian and Key Summit (end of Routeburn Track)! ")

marian_pics = [
    {"title": "", "text": "", "img":"images/Lake Marian/IMG_7028.JPEG",},
    {"title": "", "text": "", "img":"images/Lake Marian/IMG_7029.JPEG",},
    {"title": "", "text": "", "img":"images/Lake Marian/IMG_7034.JPEG",},
    {"title": "", "text": "", "img":"images/Lake Marian/IMG_7037.JPEG",},
    {"title": "", "text": "", "img":"images/Lake Marian/IMG_7039.JPEG",},
    {"title": "", "text": "", "img":"images/Lake Marian/IMG_7060.JPEG",},
    {"title": "", "text": "", "img":"images/Lake Marian/IMG_7067.JPEG",},
]
with st.container():
    carousel(items=marian_pics)
st.divider()


st.markdown("#### [Tongariro Alpine Crossing](https://www.alltrails.com/trail/new-zealand/manawatu-wanganui/tongariro-alpine-crossing) | 9/10 | Tongariro National Park | 20.54km | 6.5 Hours")
st.markdown("" \
"Tongariro Alpine Crossing is part of the [Tongariro Northern Circuit](https://www.doc.govt.nz/parks-and-recreation/places-to-go/central-north-island/places/tongariro-national-park/things-to-do/tracks/tongariro-northern-circuit/) - another of NZ's Great Walks." \
"\n\nThis is the only hike in North Island to have made it to this list and probably one of my most memorable hikes." \
"When I first started this hike, I felt like I was walking on the moon due to the unique features of the volcanic landscape alongside the lack of vegetation." \
"This trail brings you through 3 active volanoes (Tongariro, Ngauruhoe and Ruapehu) and the views of the unique landforms (Red Crater, Emerald Lakes, Blue Lake) along the way will definitely leave you mesmerized." \
"\n\nA decent level of fitness is required to attempt this track, but the ultimate determinant is the weather. The weather at Tongariro can be extremely volatile so do check the latest weather forecast before making plans." \
"This hike alone is a very strong reason for you to plan your next holiday to New Zealand and opt to explore the North Island instead of the usual South Island! ")

tongariro_pics = [
    {"title": "", "text": "", "img":"images/Tongariro/IMG_3692.JPEG",},
    {"title": "", "text": "", "img":"images/Tongariro/IMG_3697.JPEG",},
    {"title": "", "text": "", "img":"images/Tongariro/IMG_3698.JPEG",},
    {"title": "", "text": "", "img":"images/Tongariro/IMG_3703.JPEG",},
    {"title": "", "text": "", "img":"images/Tongariro/IMG_3706.JPEG",},
    {"title": "", "text": "", "img":"images/Tongariro/IMG_3707.JPEG",},
    {"title": "", "text": "", "img":"images/Tongariro/IMG_3712.JPEG",},
    {"title": "", "text": "", "img":"images/Tongariro/IMG_3716.JPEG",},
    {"title": "", "text": "", "img":"images/Tongariro/IMG_3728.JPEG",},
    {"title": "", "text": "", "img":"images/Tongariro/IMG_3729.JPEG",},
    {"title": "", "text": "", "img":"images/Tongariro/IMG_3742.JPEG",},
    {"title": "", "text": "", "img":"images/Tongariro/IMG_3744.JPEG",},
    {"title": "", "text": "", "img":"images/Tongariro/IMG_3748.JPEG",},
    {"title": "", "text": "", "img":"images/Tongariro/IMG_3750.JPEG",},
    {"title": "", "text": "", "img":"images/Tongariro/IMG_3757.JPEG",},
]
with st.container():
    carousel(items=tongariro_pics)
st.divider()


st.markdown("#### [Rob Roy Glacier Track](https://www.alltrails.com/trail/new-zealand/otago/rob-roy-glacier-track) | 9/10 | Mount Aspiring National Park | 11.54km")
st.markdown("" \
"PSA: The road to this track singlehandedly took >$1000 off the value of my car thanks to the gravel-based river fords. GET A 4WD IF YOU ARE INTENDING TO HEAD HERE!!!" \
"\n\nYeah this track was definitely memorable for both the right and wrong reasons, but let's focus on the right reasons here. " \
"You will be spoilt with unreal views of snow-capped mountains from the moment you enter Mount Aspiring National Park." \
"The track starts at Raspberry Flat carpark, where you will make your way through a vast valley before entering a forest (yes yet another forest)." \
"Shortly after, you will find yourself at the Lower Lookout, **DO NOT** stop here, continue walking for another hour to the Upper Lookout (weather permitting), 100% worth it." \
"This is one of the hikes that brings you up close and personal with a glacier, which is a magical experience." \
"\n\nOne of the easier hikes on this list, distance and elevation profile of the hike are both moderate. Conviniently located an hour's drive away from Wanaka (which I know you'll visit because of that dumb tree), Rob Roy Glacier Track definitely deserves to be on your hiking list! ")
#insert rob roy pics 
rob_pics = [
    {"title": "", "text": "", "img":"images/Rob Roy/IMG_7261.JPEG",},
    {"title": "", "text": "", "img":"images/Rob Roy/IMG_7262.JPEG",},
    {"title": "", "text": "", "img":"images/Rob Roy/IMG_7277.JPEG",},
    {"title": "", "text": "", "img":"images/Rob Roy/IMG_7287.JPEG",},
]
with st.container():
    carousel(items=rob_pics)
st.divider()

st.markdown("#### [Mount Sunday Track](https://www.alltrails.com/trail/new-zealand/canterbury/mount-sunday-track--3) | 9/10 | Ashburton Lakes | 2.01km")
st.markdown("" \
"Forget about all the 'hidden gems' that those influencers talk about. Mount Sunday **IS THE REAL HIDDEN GEM**." 
"This one completely fell outside of my radar and was not on my list of to-do hikes until one of my friends suggested that we go check it out. " \
"And boy I'm glad we did because it is stunning!." \
"\n\n*Lord Of The Rings* fans will find this track especially familiar, as *Edoras* in the trilogy was filmed on Mount Sunday. There are even guided tours available inclusive of props for that perfect picture!" \
"\n\nThis track is the easiest of all in this list, at only 2km with less than 100m elevation gained, it is suitable for people of all fitness levels! ")

sunday_pics = [
    {"title": "", "text": "", "img":"images/Mount Sunday/IMG_9062.JPEG",},
    {"title": "", "text": "", "img":"images/Mount Sunday/IMG_9064.JPEG",},
    {"title": "", "text": "", "img":"images/Mount Sunday/IMG_9067.JPEG",},
    {"title": "", "text": "", "img":"images/Mount Sunday/IMG_9068.JPEG",},
    {"title": "", "text": "", "img":"images/Mount Sunday/IMG_9071.JPEG",},
    {"title": "", "text": "", "img":"images/Mount Sunday/IMG_9081.JPEG",},
    {"title": "", "text": "", "img":"images/Mount Sunday/IMG_9085.JPEG",},
]
with st.container():
    carousel(items=sunday_pics)