import pandas as pd
import pydeck as pdk
import streamlit as st
from geopy.geocoders import Nominatim
from geopy.location import Location

from streamlit_examples.utils.theme import initPage

initPage("News Map")
st.markdown("All the good news from [Future Crunch](https://futurecrunch.com/)")


@st.cache_data(ttl="1h")
def load_data():
    # loads the data from this google sheet as pandas dataframe
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTbFkKZ2wAxPEuHZWd1BdRMG4ZKslrVfayeFze0PKI736-pGQPz8OSzaJcElZQOEvgtoZAZi6j5sjk4/pub?gid=0&single=true&output=csv"
    df = pd.read_csv(url)
    # for each entry in the dataframe, get the value from "Location" and do
    # a reverse geo lookup to retrieve the lat/lng values
    geolocator = Nominatim(user_agent="news_map")
    for index, row in df.iterrows():
        loc: Location = geolocator.geocode(row["Location"])
        df.at[index, "lat"] = loc.latitude if loc else None
        df.at[index, "lng"] = loc.longitude if loc else None
    return df


df = load_data()
editions = df["Edition"].unique()
edition = st.selectbox("Select Edition", options=editions)

filtered_df = df.loc[df["Edition"] == edition]

layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_df,
    get_position="[lng, lat]",
    get_color="[200, 30, 0, 160]",
    get_radius=200000,
    auto_highlight=True,
    pickable=True,
)
st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        layers=[layer],
        tooltip={
            "html": "{Summary}",
            "style": {"color": "white"},
        },
    )
)
