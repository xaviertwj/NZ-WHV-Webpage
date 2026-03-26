import streamlit as st
import pandas as pd 
import numpy as np
import plotly.express as px
from streamlit_carousel import carousel 

st.set_page_config(layout="wide")

st.session_state.setdefault("init", False)

if not st.session_state.init:
    st.session_state.init = True
    st.rerun()

st.header("Chapter 1: 🌿 North Island adventures")
st.subheader("1.1 Purchasing a car | Exploring Northland & Bay of Plenty")
st.markdown("""**Arriving in Auckland** 
         
I felt a rush of :rainbow[**excitement**] as soon as I arrived at Auckland airport - the experience of living and travelling alone for a year finally felt **real**.  
My intention was to stay in Auckland for a week, just enough time to settle some administrative tasks. 
Setting up my bank account and IRD was pretty straightforward, however, my car purchase journey was not as smooth-sailing.
Shopping for a suitable car within such a tight (self-imposed) timeline proved *harder than expected* due to my inexperience.
Eventually, I decided to purchase a Nissan Serena from a local car dealership to be my trusty travel companion over the next year.""")

st.markdown("""**Adventures around Northland & Bay of Plenty**

My first destination was Whangarei, two hours drive north of Auckland. As I drove out of the city, I was amazed by the scenic and vast landscape that New Zealand had to offer.
In true Singaporean fashion I thought to myself: *"imagine what we could do in Singapore if we had that much land, there's so much potential for commercialization"*. 
I spent a night in Whangarei and did two hikes around the area before heading furhter north to Paihia. At Paihia, I then figured it would be more efficient to take a day-tour with a tour group to visit Cape Reinga and ninety-mile beach (the beach isn't actually 90 miles).  
\nCape Reinga is located at the tip of the north island, where you can see the iconic lighthouse and the majestic convergence of the Tasman Sea and the Pacific Ocean.  \nNinety mile beach was also fascinating (fun fact: if you have a 4wd you can drive on the beach!), I've never seen such a vast beach that seems to never end and to top it off, you can sandboard at the sand dunes there!

I then journeyed on towarrds Mount Maunganui in Bay of Plenty, where I spent a few nights at my ex-colleague's place (thank you Carl!). 
The next few days were spent exploring pristine beaches, great eateries and of course, hiking up Mauao; Mount Maunganui is a small suburb but a really beautiful place!
         
Papamoa was my next destination since I was heading towards Te Puke, in anticipation of starting my first job in New Zealand.
I then thought to myself: "why buy such a big car if I didn't intend to sleep in it?" And so I did, I spent the next couple nights sleeping in my car at a holiday park by Papamoa Beach. 
Waking up by the beachfront to the sounds of gentle waves and being greeted by majestic views of the sunrise every morning felt surreal. 
As for the comfort of sleeping in my car... let's just say that my 30 year-old back was not too happy about it.
         """)  

st.markdown("""
**🏔️ Honourable Hikes**
- Mount Manaia Track  
- Hakarimata Summit Track  
- Wairere Falls Trail  
- Mount Maunganui Summit  
- Papamoa Hills  
""")

#Image Carousel
items = [
    {"title": "", "text": "", "img":"images/1.1/last_meal.jpg",},
    {"title": "", "text": "", "img":"images/1.1/bye.jpeg",},
    {"title": "", "text": "","img":"images/1.1/car.jpg",},
    {"title": "", "text": "","img":"images/1.1/oth.jpeg",},
    {"title": "", "text": "","img":"images/1.1/manaia.jpeg",},
    {"title": "", "text": "","img":"images/1.1/rainbow.jpeg",},
    {"title": "", "text": "","img":"images/1.1/wairere.jpeg",},
    {"title": "", "text": "","img":"images/1.1/paihia.jpeg",},
    {"title": "", "text": "","img":"images/1.1/90_mile.jpeg",},
    {"title": "", "text": "", "img":"images/1.1/mauao.jpeg",},
    {"title": "", "text": "", "img":"images/1.1/papamoa.jpeg",},

]
st.markdown("<br><br>", unsafe_allow_html=True)
with st.container():
    carousel(items=items)


st.divider()

st.subheader("1.2 Kiwifruit Picking + Packing | Rotorua | Tongariro Alpine Crossing")
st.write("""**My first job in NZ**

Alas, my short holiday came to an end and it was time to start my first job as a kiwifruit picker in Te Puke; the kiwifruit capital of the world. 
To say that fruit picking was an eye-opening experience is an understatement.... **everything** about this job is drastically different from what I did back home.
 """)

data = {
    "": ["Comfy chair", "Air conditioning", "Physically exhausting", "Fixed hours", "Weather dependent", "Switch off after work", "Free kiwifruits"],
    "**Kiwifruit Picking**": ["❌", "❌", "✅", "❌", "✅", "✅", "✅"],
    "**Office Job**": ["✅", "✅", "❌", "✅", "❌", "❌", "❌"]
}
df = pd.DataFrame(data).set_index("")
st.table(df, width=600)

st.write("""
Fruit picking was an interesting and refreshing experience, it was fun working and interacting with fellow travellers from all across the world.
However, the hours of work offered each week was extremely volatile and largely at the mercy of externalities such as the weather and the maturity of the fruit.
The working hours soon proved to be unsustainable and I decided to apply for a job at a kiwifruit packhouse since they provided more stable working hours (or so I thought).

I decided to sign a casual contract (as and when required basis) with the packhouse so that I could do both picking and packing.
Things got off to a good start, I had 5 days of work for the first week across the packhouse and picking. This was good enough for me and I expected that it would continue like this throughout the entire season. 
Unfortunately, by the second week, I was only getting a combined of 1-2 days of work and it continued like this for the subsequent weeks. **I was desperate and felt defeated, nothing was going according to my plan.**

To make matters worse, I was not able to convert from a casual to a part-time employee at the packhouse because by that time, they had already hired enough people. 
Despite being recognized as a good and dillgent employee by the managers and trainers at the packhouse, at this point, I was not getting called to work at the packhouse **at all** due to my casual employment contract.  \nI decided that I had to take matters into my own hands instead of sitting on my ass all day waiting to get called. 
I sat around at the packhouse's canteen every evening, asking if the managers / trainers knew of any teams that needed help. 
Surprisingly, through my peseverence (or stubbornness), I managed to get a few days of work by doing this. 
I continuted doing so till it was time for me to leave Te Puke and continue on my journey.""")

st.write("""**Smells Like Teen Spirit (or sulphur)**

Rotorua (pronounced Rrrraw-toe-rroo-ah) was my next destination - a city built within a 20km-wide ancient volcanic caldera (which often smells like sulphur due to the hydrogen sulphide emissions).  
         
My first stop was a geothermal reserve called Hell's Gate, they have walking trails for you to admire the geothermal landscape, a mud bath and also hot pools for you to indulge in after your walk **(Adult ticket :NZD90)**.  \nI then went to Skyline Rotorua and tried everything that they had to offer to get my adrenaline fix - luge rides, skyswing and zipline. 
I thoroughly enjoyed my experience there, the views were magnificent, a huge contrast to riding the luge at say.... Sentosa. 
         
Rotorua is known to be NZ's hub for Māori Culture, so I had to book a tour to Mitai Maori Village's cultural experience and dinner buffet. 
I was treated to a feast of traditional Hangi ("earth oven") food, Māori warriors canoeing, a cultural Māori show (yes they performed the Haka) and a walk through the village to end the night; a truly *immersive experience* for both my soul and tummy.
         """)

st.write("""**Tongariro Alpine Crossing**

After leaving Rotorua, I continued travelling south towards Taupo, where I visited the iconic.... McDonald's. Yes you read that right, the McDonald's at Taupo features an actual decommissioned aircraft (which you can dine in) and has been voted as the world's coolest McDonald's.
Fret not, I did show Lake Taupo some love as well. 
         
My next adventure was to hike Tongariro Alpine Crossing, I was really looking forward to this one since I've heard so many nice things about it and some even quoted “World's Greatest Day Hike” on Alltrails. 
This track is also part of the Tongariro Northern Circuit - one of the great walks in NZ.
         """)

data_1 = {
    "**Metrics**": ["Distance", "Elevation Gain", "Type", "Duration", "Difficulty"],
    "**🏔️ Tongariro Alpine Crossing**": ["20.3km", "853m", "Point to Point", "6 to 8 hrs", "Hard"]
}

df_1 = pd.DataFrame(data_1).set_index("**Metrics**")
st.table(df_1, width=600)

st.write("""For most of my hikes that I have done up till this point, I usually have to walk through forests filled with vegetation, where I spend 80% of my time in before it clears nearing the summit.  \nTongariro Alpine Crossing however, was completely different. 
If you start the walk at Mangatepopo carpark like I did, you'll be greeted with vast vocanic landscape from the moment you begin your walk, which is absolutely breathtaking.
The key landmarks along this trail - red crater and emerald lakes each had its unique charm and was unlike anything I've ever seen.
I would consider myself to be lucky since the weather was cooperative throughout my hike. I've heard stories of people who made it to red crater but could not see anything at all due to low visibility. 
Overall, I really enjoyed this hike and it remains one my favourites in NZ!

         """)


st.divider()

st.subheader("1.3 First WWOOFing Experience | Leaving North Island")

